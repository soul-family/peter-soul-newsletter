#!/usr/bin/env python3
"""
session_archive_manager.py — Move old sessions to cold storage.

Moves session databases older than a threshold to an archive directory,
freeing up space in the primary backup location.

Usage:
  python session_archive_manager.py --dry-run --retention-days 90
  python session_archive_manager.py --retention-days 90 --archive-dir .ai-activity/ai-sessions/archive
"""

import argparse
import os
import shutil
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai-assistant', 'scripts', 'shared'))
from config_loader import get_developer_ids, get_developer_config


def get_session_age_days(db_path):
    """Get the most recent session age in days."""
    if not os.path.exists(db_path):
        return None
    
    mtime = os.path.getmtime(db_path)
    return (datetime.now().timestamp() - mtime) / 86400


def archive_database(db_path, archive_dir, dry_run=False):
    """Move database to archive directory."""
    db_name = os.path.basename(db_path)
    archive_path = os.path.join(archive_dir, db_name)
    
    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    age_days = get_session_age_days(db_path)
    
    if dry_run:
        print(f"  Would archive: {db_path} ({size_mb:.1f} MB, {age_days:.0f} days old)")
        return True
    
    try:
        os.makedirs(archive_dir, exist_ok=True)
        shutil.move(db_path, archive_path)
        print(f"  Archived: {db_path} -> {archive_path} ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  Error archiving {db_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Session archive manager for cold storage.'
    )
    parser.add_argument('--retention-days', type=int, default=90,
                        help='Move databases older than this many days to archive')
    parser.add_argument('--archive-dir', default='.ai-activity/ai-sessions/archive',
                        help='Archive directory path')
    parser.add_argument('--base-dir', default='.ai-activity/ai-sessions',
                        help='Base directory for session databases')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be archived')
    parser.add_argument('--developer', default=None,
                        help='Specific developer ID to archive')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE")
    print(f"Retention: {args.retention_days} days")
    print(f"Archive: {args.archive_dir}")
    print()
    
    developers = [args.developer] if args.developer else get_developer_ids('.dev-scripts/ai-assistant/scripts')
    
    archived = 0
    failed = 0
    
    for dev_id in developers:
        dev_config = get_developer_config('.dev-scripts/ai-assistant/scripts', dev_id)
        config_dir = dev_config.get('config_dir', dev_id)
        dev_dir = os.path.join(args.base_dir, config_dir)
        
        if not os.path.exists(dev_dir):
            continue
        
        for fname in os.listdir(dev_dir):
            if not fname.endswith('.db'):
                continue
            
            db_path = os.path.join(dev_dir, fname)
            age_days = get_session_age_days(db_path)
            
            if age_days is None or age_days < args.retention_days:
                continue
            
            if archive_database(db_path, args.archive_dir, args.dry_run):
                archived += 1
            else:
                failed += 1
    
    print(f"\nComplete: {archived} archived, {failed} failed")
    
    if failed > 0 and not args.dry_run:
        sys.exit(1)


if __name__ == '__main__':
    main()
