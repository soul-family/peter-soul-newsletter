#!/usr/bin/env python3
"""
verify_dedup.py - Verify message and part deduplication in backup databases.

Checks for duplicate messages and parts within a backup database.
Duplicates can occur when the same session is backed up multiple times
without proper deduplication.

Usage:
  python verify_dedup.py --db-path .ai-activity/ai-sessions/<developer>/sessions.db
"""

import argparse
import sqlite3
import sys


def check_duplicates(db_path):
    """Check for duplicate messages and parts."""
    issues = []
    
    if not db_path or not db_path.exists():
        return [f"Database not found: {db_path}"]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check duplicate messages
    cursor.execute("""
        SELECT id, session_id, COUNT(*) as cnt 
        FROM message 
        GROUP BY id, session_id 
        HAVING cnt > 1
    """)
    dup_messages = cursor.fetchall()
    if dup_messages:
        for msg_id, session_id, cnt in dup_messages[:10]:
            issues.append(f"Duplicate message: {msg_id} in session {session_id} ({cnt} copies)")
        if len(dup_messages) > 10:
            issues.append(f"... and {len(dup_messages) - 10} more duplicate messages")
    
    # Check duplicate parts
    cursor.execute("""
        SELECT id, message_id, session_id, COUNT(*) as cnt 
        FROM part 
        GROUP BY id, message_id, session_id 
        HAVING cnt > 1
    """)
    dup_parts = cursor.fetchall()
    if dup_parts:
        for part_id, msg_id, session_id, cnt in dup_parts[:10]:
            issues.append(f"Duplicate part: {part_id} in message {msg_id} ({cnt} copies)")
        if len(dup_parts) > 10:
            issues.append(f"... and {len(dup_parts) - 10} more duplicate parts")
    
    # Check for sessions with duplicate message IDs across different sessions
    cursor.execute("""
        SELECT id, COUNT(DISTINCT session_id) as session_count 
        FROM message 
        GROUP BY id 
        HAVING session_count > 1
    """)
    shared_msg_ids = cursor.fetchall()
    if shared_msg_ids:
        for msg_id, count in shared_msg_ids[:10]:
            issues.append(f"Message ID {msg_id} appears in {count} different sessions")
    
    conn.close()
    
    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Verify message/part deduplication in backup databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the backup database')
    
    args = parser.parse_args()
    
    from pathlib import Path
    db_path = Path(args.db_path)
    
    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        sys.exit(1)
    
    print(f"Checking deduplication: {db_path}")
    print()
    
    issues = check_duplicates(db_path)
    
    if issues:
        print("DUPLICATION ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("NO DUPLICATES: Message and part IDs are unique")
        sys.exit(0)


if __name__ == '__main__':
    main()
