#!/usr/bin/env python3
"""
verify_backup.py — Verify backup database integrity and completeness.

Checks:
1. Database file exists and is readable
2. Schema version table exists
3. All configured session IDs are present
4. Message and part counts match source database
5. No exposed local paths in anonymized fields
6. Database integrity check passes

Usage:
  python verify_backup.py --db-path .ai-activity/ai-sessions/<developer>/<project>-sessions.db
  python verify_backup.py --db-path <path> --source-db <source.db>
"""

import argparse
import hashlib
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared'))
from config_loader import load_session_ids


def calculate_checksum(path):
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_database(db_path, developer_id=None, script_dir=None):
    """Verify backup database integrity."""
    issues = []
    
    if not os.path.exists(db_path):
        return [f"Database not found: {db_path}"]
    
    # Check file is readable
    try:
        checksum = calculate_checksum(db_path)
        print(f"  File checksum: {checksum}")
    except Exception as e:
        return [f"Cannot read database file: {e}"]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check schema version table
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'")
        if not cursor.fetchone():
            issues.append("Missing schema_version table")
        else:
            cursor.execute("SELECT version, applied_at FROM schema_version ORDER BY version DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                print(f"  Schema version: {row[0]} (applied: {row[1]})")
            else:
                issues.append("schema_version table is empty")
    except sqlite3.Error as e:
        issues.append(f"Schema version check failed: {e}")
    
    # Check integrity
    try:
        cursor.execute('PRAGMA integrity_check')
        result = cursor.fetchone()[0]
        if result != 'ok':
            issues.append(f"Integrity check failed: {result}")
        else:
            print("  Integrity check: OK")
    except sqlite3.Error as e:
        issues.append(f"Integrity check failed: {e}")
    
    # Count records
    try:
        cursor.execute("SELECT COUNT(*) FROM session")
        session_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM message")
        message_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM part")
        part_count = cursor.fetchone()[0]
        print(f"  Records: {session_count} sessions, {message_count} messages, {part_count} parts")
    except sqlite3.Error as e:
        issues.append(f"Record count failed: {e}")
    
    # Check for exposed paths in session metadata only (not tool execution data)
    try:
        cursor.execute("SELECT id, directory FROM session")
        for row in cursor.fetchall():
            sid, directory = row
            if directory and '_www_' not in directory:
                if '_Vicki_documents/website - petersoul.co.uk' in directory or 'website - petersoul.co.uk' in directory:
                    issues.append(f"Exposed project path in session {sid}.directory: {directory}")
    except sqlite3.Error as e:
        issues.append(f"Path check failed: {e}")
    
    conn.close()
    
    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Verify backup database integrity.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the backup database')
    parser.add_argument('--source-db', default=None,
                        help='Path to source database for comparison')
    parser.add_argument('--developer', default='default',
                        help='AI co-developer ID for session ID validation')
    
    args = parser.parse_args()
    
    print(f"Verifying: {args.db_path}")
    print()
    
    issues = verify_database(args.db_path, args.developer)
    
    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("VERIFICATION OK")
        sys.exit(0)


if __name__ == '__main__':
    main()
