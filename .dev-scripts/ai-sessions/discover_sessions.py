#!/usr/bin/env python3
"""
discover_sessions.py - Auto-discover sessions from AI co-developer databases.

Queries the source SQLite database and outputs session IDs for the current
project, optionally filtering by project-specific criteria. Replaces manual
session ID lists in JSON config files.
"""

import argparse
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared'))
from config_loader import get_developer_config


def discover_sessions(db_path, developer_id='default', limit=None):
    """Discover sessions from the source database.
    
    Args:
        db_path: Path to the source SQLite database
        developer_id: Developer ID for config resolution
        limit: Optional maximum number of sessions to return
    
    Returns:
        List of session IDs
    """
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = "SELECT id FROM session ORDER BY time_created DESC"
    params = []
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    
    c.execute(query, params)
    sessions = [row['id'] for row in c.fetchall()]
    conn.close()
    
    return sessions


def main():
    parser = argparse.ArgumentParser(
        description='Auto-discover sessions from AI co-developer databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the source SQLite database')
    parser.add_argument('--developer', default='default',
                        help='AI co-developer ID (for config resolution)')
    parser.add_argument('--limit', type=int, default=None,
                        help='Maximum number of sessions to return')
    parser.add_argument('--output', default=None,
                        help='Output file path (default: stdout)')
    parser.add_argument('--format', choices=['json', 'list'], default='list',
                        help='Output format: json or plain list')
    
    args = parser.parse_args()
    
    sessions = discover_sessions(args.db_path, args.developer, args.limit)
    
    if args.format == 'json':
        output = json.dumps({'session_ids': sessions}, indent=2)
    else:
        output = '\n'.join(sessions)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
            f.write('\n')
        print(f"Wrote {len(sessions)} session IDs to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
