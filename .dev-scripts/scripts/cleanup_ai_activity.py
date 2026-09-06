#!/usr/bin/env python3
"""
cleanup_ai_activity.py — Retention policy and cleanup for .ai-activity.

Applies retention rules to prevent unbounded growth:
- Session databases: keep last N days/configurable retention
- Stats files: keep in sync with databases
- Logs: rotate old entries
- Reports: regenerate from current data

Usage:
  python cleanup_ai_activity.py --dry-run
  python cleanup_ai_activity.py --retention-days 90
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI_ACTIVITY = os.path.join(BASE, '.ai-activity')


def get_file_age_days(path):
    """Get file age in days."""
    mtime = os.path.getmtime(path)
    return (datetime.now().timestamp() - mtime) / 86400


def cleanup_sessions(retention_days, dry_run=False):
    """Remove session databases older than retention period."""
    sessions_dir = os.path.join(AI_ACTIVITY, 'ai-sessions')
    if not os.path.exists(sessions_dir):
        return []
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    removed = []
    
    for root, dirs, files in os.walk(sessions_dir):
        for f in files:
            if f.endswith('.db'):
                path = os.path.join(root, f)
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < cutoff:
                    size_mb = os.path.getsize(path) / (1024 * 1024)
                    removed.append((path, size_mb, mtime))
                    if not dry_run:
                        os.remove(path)
                        stats_path = path.replace('.db', '.stats.json')
                        if os.path.exists(stats_path):
                            os.remove(stats_path)
    
    return removed


def cleanup_logs(retention_days, dry_run=False):
    """Remove log entries older than retention period."""
    logs_dir = os.path.join(AI_ACTIVITY, 'ai-logs')
    if not os.path.exists(logs_dir):
        return []
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    removed = []
    
    for f in ['interactions.md', 'sessions.md', 'sources.md', 'tools.md']:
        path = os.path.join(logs_dir, f)
        if not os.path.exists(path):
            continue
        
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if mtime < cutoff:
            size_kb = os.path.getsize(path) / 1024
            removed.append((path, size_kb, mtime))
            if not dry_run:
                os.remove(path)
    
    return removed


def cleanup_reports(retention_days, dry_run=False):
    """Regenerate reports from current data."""
    reports_dir = os.path.join(AI_ACTIVITY, 'ai-reports')
    if not os.path.exists(reports_dir):
        return []
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    removed = []
    
    for f in os.listdir(reports_dir):
        if f.endswith('.md') or f.endswith('.json'):
            path = os.path.join(reports_dir, f)
            if not os.path.isfile(path):
                continue
            
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime < cutoff:
                size_kb = os.path.getsize(path) / 1024
                removed.append((path, size_kb, mtime))
                if not dry_run:
                    os.remove(path)
    
    return removed


def main():
    parser = argparse.ArgumentParser(
        description='Apply retention policy to .ai-activity directory.'
    )
    parser.add_argument('--retention-days', type=int, default=90,
                        help='Retention period in days (default: 90)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be removed without deleting')
    
    args = parser.parse_args()
    
    print(f"AI Activity Cleanup (retention: {args.retention_days} days)")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    
    sessions_removed = cleanup_sessions(args.retention_days, args.dry_run)
    logs_removed = cleanup_logs(args.retention_days, args.dry_run)
    reports_removed = cleanup_reports(args.retention_days, args.dry_run)
    
    if sessions_removed:
        print(f"Sessions removed: {len(sessions_removed)}")
        for path, size_mb, mtime in sessions_removed:
            print(f"  {path} ({size_mb:.1f} MB, {mtime.date()})")
    else:
        print("Sessions: nothing to remove")
    
    if logs_removed:
        print(f"Logs removed: {len(logs_removed)}")
        for path, size_kb, mtime in logs_removed:
            print(f"  {path} ({size_kb:.1f} KB, {mtime.date()})")
    else:
        print("Logs: nothing to remove")
    
    if reports_removed:
        print(f"Reports removed: {len(reports_removed)}")
        for path, size_kb, mtime in reports_removed:
            print(f"  {path} ({size_kb:.1f} KB, {mtime.date()})")
    else:
        print("Reports: nothing to remove")
    
    if args.dry_run:
        print("\nDRY RUN complete. No files were deleted.")
    else:
        print("\nCleanup complete.")


if __name__ == '__main__':
    main()
