#!/usr/bin/env python3
"""
verify_path_anonymization.py — Verify session databases have no exposed project paths.

Checks that configured path replacement rules were applied correctly by scanning
all text columns for any remaining instances of the original paths. Reports any
matches as potential privacy leaks.
"""

import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shared'))
from config_loader import load_paths_to_replace


def get_text_columns(conn, table_name):
    """Return list of text column names for a table."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = []
    for row in cursor.fetchall():
        col_type = row[2].upper()
        if col_type in ('TEXT', 'BLOB'):
            columns.append(row[1])
    return columns


def scan_table(conn, table_name, patterns):
    """Scan a table for exposed paths in text columns."""
    cursor = conn.cursor()
    text_columns = get_text_columns(conn, table_name)
    
    if not text_columns:
        return []
    
    issues = []
    col_list = ', '.join([f'"{c}"' for c in text_columns])
    cursor.execute(f"SELECT rowid, {col_list} FROM {table_name}")
    
    for row in cursor.fetchall():
        row_id = row[0]
        for col_idx, col_name in enumerate(text_columns):
            value = row[col_idx + 1]
            if not value or not isinstance(value, str):
                continue
            
            for pattern in patterns:
                if pattern in value:
                    snippet = value[:200].replace('\n', ' ')
                    issues.append({
                        'table': table_name,
                        'row_id': row_id,
                        'column': col_name,
                        'pattern': pattern,
                        'snippet': snippet,
                    })
                    break
    
    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Verify session databases have no exposed project paths.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the session database (.db)')
    parser.add_argument('--script-dir', default=None,
                        help='Path to scripts directory for config loading')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.db_path):
        print(f"ERROR: Database not found at {args.db_path}")
        sys.exit(1)
    
    script_dir = args.script_dir
    if not script_dir:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load replacements from all developer configs
    replacements = []
    replacements.extend(load_paths_to_replace(script_dir))
    
    # Also load from developer-specific config directories
    ai_assistant_root = os.path.dirname(script_dir)
    for config_dir_name in os.listdir(ai_assistant_root):
        config_dir_path = os.path.join(ai_assistant_root, config_dir_name)
        if os.path.isdir(config_dir_path) and config_dir_name not in ('scripts', 'shared', '__pycache__'):
            dev_replacements = load_paths_to_replace(config_dir_path)
            replacements.extend(dev_replacements)
    
    patterns = []
    for replacement in replacements:
        for path in replacement.get('paths', []):
            patterns.append(path)
    
    if not patterns:
        print("PATH ANONYMIZATION OK: no patterns to check")
        sys.exit(0)
    
    conn = sqlite3.connect(args.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    all_issues = []
    for table in tables:
        if table.startswith('sqlite_'):
            continue
        issues = scan_table(conn, table, patterns)
        all_issues.extend(issues)
    
    conn.close()
    
    if all_issues:
        print(f"PATH ANONYMIZATION ISSUES: {len(all_issues)} found in {args.db_path}")
        for issue in all_issues[:20]:
            print(f"  - {issue['table']} row {issue['row_id']} column {issue['column']}: "
                  f"contains '{issue['pattern']}' -> {issue['snippet']}")
        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more")
        sys.exit(1)
    else:
        print(f"PATH ANONYMIZATION OK: {args.db_path}")
        sys.exit(0)


if __name__ == '__main__':
    main()
