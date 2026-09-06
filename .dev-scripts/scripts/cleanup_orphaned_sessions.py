#!/usr/bin/env python3
"""
cleanup_orphaned_sessions.py — Clean up orphaned session files.

Scans session directories for files that no longer have corresponding
entries in the backup database and removes them.

Usage:
  python cleanup_orphaned_sessions.py --dry-run
  python cleanup_orphaned_sessions.py --developer kilo-code
"""

import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai-assistant', 'scripts', 'shared'))
from config_loader import get_developer_config


def get_backup_sessions(db_path):
    """Get set of session IDs from backup database."""
    if not os.path.exists(db_path):
        return set()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM session")
    sessions = {row[0] for row in cursor.fetchall()}
    conn.close()
    return sessions


def find_orphaned_files(session_dir, backup_sessions):
    """Find session files in directory that aren't in backup database."""
    orphans = []
    
    if not os.path.exists(session_dir):
        return orphans
    
    for fname in os.listdir(session_dir):
        fpath = os.path.join(session_dir, fname)
        if not os.path.isfile(fpath):
            continue
        
        # Extract session ID from filename
        if '_ses_' in fname:
            sid = 'ses_' + fname.split('_ses_')[1].split('.')[0].split('_')[0]
        elif fname.startswith('ses_'):
            sid = fname.split('.')[0]
        else:
            continue
        
        if sid not in backup_sessions:
            size_mb = os.path.getsize(fpath) / (1024 * 1024)
            orphans.append((fpath, sid, size_mb))
    
    return orphans


def main():
    parser = argparse.ArgumentParser(
        description='Clean up orphaned session files.'
    )
    parser.add_argument('--developer', default='kilo-code',
                        help='AI co-developer ID')
    parser.add_argument('--session-dir', default=None,
                        help='Path to session directory')
    parser.add_argument('--db-path', default=None,
                        help='Path to backup database')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be removed')
    
    args = parser.parse_args()
    
    if args.session_dir:
        session_dir = args.session_dir
    else:
        dev_config = get_developer_config('.dev-scripts/ai-assistant/scripts', args.developer)
        session_dir = os.path.join('.ai-activity', 'ai-sessions', dev_config.get('config_dir', args.developer))
    
    if args.db_path:
        db_path = args.db_path
    else:
        db_path = os.path.join(session_dir, 'website-sessions.db')
        if not os.path.exists(db_path):
            db_path = os.path.join(session_dir, f'{args.developer}-sessions.db')
    
    if not os.path.exists(db_path):
        print(f"ERROR: Backup database not found at {db_path}")
        sys.exit(1)
    
    print(f"Scanning: {session_dir}")
    print(f"Database: {db_path}")
    print()
    
    backup_sessions = get_backup_sessions(db_path)
    print(f"Backup contains {len(backup_sessions)} sessions")
    
    orphans = find_orphaned_files(session_dir, backup_sessions)
    
    if not orphans:
        print("No orphaned files found.")
        return
    
    print(f"Found {len(orphans)} orphaned files:")
    for fpath, sid, size_mb in orphans:
        print(f"  {fpath} ({size_mb:.1f} MB)")
    
    if args.dry_run:
        print("\nDRY RUN: No files deleted.")
        return
    
    removed = 0
    for fpath, sid, size_mb in orphans:
        try:
            os.remove(fpath)
            print(f"  Removed: {fpath}")
            removed += 1
        except Exception as e:
            print(f"  Error removing {fpath}: {e}")
    
    print(f"\nRemoved {removed} orphaned files.")


if __name__ == '__main__':
    main()
