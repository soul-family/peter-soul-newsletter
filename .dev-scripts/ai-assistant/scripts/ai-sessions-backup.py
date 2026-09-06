#!/usr/bin/env python3
"""
ai-sessions-backup.py - Export AI session data into project-specific SQLite
databases.

Reads session data (session, message, part tables) from a source SQLite
database and writes a new database filtered to the specified session IDs, with
all local filesystem paths replaced by _www_ to avoid exposing the local
directory structure.

Supports multiple AI co-developers with per-developer configuration.

Usage:
  python ai-sessions-backup.py --db-path <path to source.db>
  python ai-sessions-backup.py --db-path <path> --append
  python ai-sessions-backup.py --db-path <path> --developer <developer-id>
"""

import argparse
import datetime
import json
import os
import sys

# Add shared directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'shared'))

from session_utils import (
    get_schema,
    replace_paths,
)
from config_loader import (
    load_developers,
    get_developer_config,
    get_developer_ids,
    load_paths_to_replace,
    load_session_ids,
    get_output_dir,
)


def _get_ai_developers(script_dir):
    return get_developer_ids(script_dir)


def find_current_session_id(project_root, developer):
    """Find the most recent session ID from a developer's session knowledge folder."""
    import re

    session_dirs = [
        os.path.join(project_root, '.ai-activity', 'ai-sessions', developer),
        os.path.join(project_root, '_ai_session', developer),
    ]

    pattern = re.compile(r'_ses_([a-f0-9]+)')

    for base_dir in session_dirs:
        if not os.path.isdir(base_dir):
            continue

        best_sid = None
        best_mtime = 0

        for fname in os.listdir(base_dir):
            m = pattern.search(fname)
            if m:
                fpath = os.path.join(base_dir, fname)
                mtime = os.path.getmtime(fpath)
                if mtime > best_mtime:
                    best_mtime = mtime
                    best_sid = 'ses_' + m.group(1)

        if best_sid:
            return best_sid

    return None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ai_developers = _get_ai_developers(script_dir)
    default_developer = ai_developers[0] if ai_developers else 'default'
    
    parser = argparse.ArgumentParser(
        description='Export AI session data into anonymized SQLite databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the source SQLite database')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory (default: .ai-activity/ai-sessions/<developer>)')
    parser.add_argument('--output-name', default=None,
                        help='Output database filename (default: from developer config)')
    parser.add_argument('--developer', default=default_developer,
                        choices=ai_developers,
                        help='AI co-developer (default: %s)' % default_developer)
    parser.add_argument('--current-session', action='store_true',
                        help='Auto-discover and include the current/most-recent session ID')
    parser.add_argument('--sessions', default=None,
                        help='Comma-separated session IDs (overrides JSON config)')
    parser.add_argument('--paths-to-replace', default=None,
                        help='Comma-separated paths to replace with _www_ (overrides JSON config)')
    parser.add_argument('--append', action='store_true',
                        help='Append new sessions to existing database instead of recreating it')

    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"ERROR: Database not found at {args.db_path}")
        sys.exit(1)

    # Load path replacements
    if args.paths_to_replace:
        path_replacements = []
        for p in args.paths_to_replace.split(','):
            p = p.strip()
            if p:
                from session_utils import generate_path_variations
                path_replacements.extend(generate_path_variations(p, '_www_'))
        print(f"Using {len(path_replacements)} path replacements from command line")
    else:
        path_replacements_data = load_paths_to_replace(SCRIPT_DIR, args.developer)
        path_replacements = []
        for data in path_replacements_data:
            for base_path in data['paths']:
                from session_utils import generate_path_variations
                path_replacements.extend(generate_path_variations(base_path, data['replacement']))
        print(f"Loaded {len(path_replacements)} path replacements from config")

    # Load session IDs
    if args.sessions:
        session_ids = [s.strip() for s in args.sessions.split(',') if s.strip()]
    else:
        session_ids = load_session_ids(SCRIPT_DIR, args.developer)
        print(f"Loaded {len(session_ids)} session IDs from config")

    # Auto-discover current session if requested
    if args.current_session:
        project_root = os.path.dirname(os.path.dirname(SCRIPT_DIR))
        current_sid = find_current_session_id(project_root, args.developer)
        if current_sid and current_sid not in session_ids:
            session_ids.append(current_sid)
            print(f"Added current session: {current_sid}")
        elif not current_sid:
            print("WARNING: Could not discover current session")

    # Determine output path
    if args.output_dir:
        output_dir = args.output_dir
    else:
        dev_config = get_developer_config(SCRIPT_DIR, args.developer)
        output_dir = os.path.join(project_root, '.ai-activity', 'ai-sessions', dev_config.get('config_dir', args.developer))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_name = args.output_name or get_developer_config(SCRIPT_DIR, args.developer).get('database', 'sessions.db')
    output_path = os.path.join(output_dir, output_name)

    # Confirm overwrite
    if os.path.exists(output_path) and not args.append:
        print(f"WARNING: Output database already exists: {output_path}")
        confirm = prompt("Type 'yes' to overwrite, or 'append' to switch to append mode: ")
        if confirm == 'append':
            args.append = True
        elif confirm != 'yes':
            print("Aborted.")
            sys.exit(0)

    print(f"Source: {args.db_path}")
    print(f"Output: {output_path}")
    print(f"Developer: {args.developer}")
    print(f"Sessions: {len(session_ids)}")
    print(f"Mode: {'append' if args.append else 'create'}")
    print()

    if args.append:
        count, msg_count, part_count = append_sessions_to_db(args.db_path, output_path, session_ids, path_replacements)
    else:
        count, msg_count, part_count = backup_sessions(args.db_path, output_path, session_ids, path_replacements)

    print(f"\nBackup complete: {count} sessions, {msg_count} messages, {part_count} parts")


def find_current_session_id_from_db(db_path):
    """Find the most recent session ID by querying the source SQLite database directly."""
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM session ORDER BY time_created DESC LIMIT 1")
        row = c.fetchone()
        if row:
            return row['id']
    except sqlite3.Error:
        pass
    conn.close()
    return None


SCHEMA_VERSION = 1

SCHEMA_VERSION_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT
)
'''


def generate_path_variations(base_path, replacement='_www_'):
    """Generate all slash-form variations of a local path for replacement."""
    import sys
    sys.path.insert(0, os.path.join(SCRIPT_DIR, 'shared'))
    from session_utils import generate_path_variations as _gen
    return _gen(base_path, replacement)


def backup_sessions(db_path, output_path, session_ids, path_replacements):
    """Create a filtered, path-anonymized backup database."""
    import sqlite3

    if os.path.exists(output_path):
        os.remove(output_path)

    src_conn = sqlite3.connect(db_path)
    src_conn.row_factory = sqlite3.Row
    src_c = src_conn.cursor()

    schema = get_schema(src_conn)

    dst_conn = sqlite3.connect(output_path)
    dst_c = dst_conn.cursor()

    for table_name, sql in schema.items():
        if sql:
            dst_c.execute(sql)
    
    # Create indexes for frequently queried columns
    indexes = schema.get('indexes', [])
    for idx in indexes:
        table = idx.get('table')
        columns = idx.get('columns', [])
        if table and columns:
            idx_name = f'idx_{table}_{"_".join(columns)}'
            idx_sql = f'CREATE INDEX IF NOT EXISTS {idx_name} ON {table} ({", ".join(columns)})'
            dst_c.execute(idx_sql)
    
    dst_c.execute(SCHEMA_VERSION_TABLE_SQL)
    dst_c.execute(
        'INSERT INTO schema_version (version, applied_at, description) VALUES (?, ?, ?)',
        (SCHEMA_VERSION, datetime.datetime.now().isoformat(), 'Initial schema version')
    )
    dst_conn.commit()

    for sid in session_ids:
        src_c.execute("SELECT * FROM session WHERE id=?", (sid,))
        row = src_c.fetchone()
        if row is None:
            print(f"  Session {sid}: NOT FOUND")
            continue

        cols = [d[0] for d in src_c.description]
        values = [replace_paths(row[col], path_replacements) for col in cols]
        
        # Enrich with backup metadata
        if 'metadata' in cols:
            metadata_idx = cols.index('metadata')
            import json
            existing_metadata = {}
            if values[metadata_idx]:
                try:
                    existing_metadata = json.loads(values[metadata_idx])
                except (json.JSONDecodeError, TypeError):
                    existing_metadata = {}
            existing_metadata.update({
                'backup_timestamp': datetime.datetime.now().isoformat(),
                'backup_source': str(db_path),
                'backup_developer': args.developer,
                'backup_version': SCHEMA_VERSION,
            })
            values[metadata_idx] = json.dumps(existing_metadata)
        
        placeholders = ', '.join(['?' for _ in cols])
        col_names = ', '.join([f'"{c}"' for c in cols])
        dst_c.execute(f'INSERT INTO session ({col_names}) VALUES ({placeholders})', values)

        src_c.execute("SELECT * FROM message WHERE session_id=?", (sid,))
        msg_rows = src_c.fetchall()
        msg_cols = [d[0] for d in src_c.description]
        msg_placeholders = ', '.join(['?' for _ in msg_cols])
        msg_col_names = ', '.join([f'"{c}"' for c in msg_cols])
        for msg_row in msg_rows:
            msg_values = [replace_paths(msg_row[col], path_replacements) for col in msg_cols]
            dst_c.execute(f'INSERT INTO message ({msg_col_names}) VALUES ({msg_placeholders})', msg_values)

            msg_id = msg_row['id']

            src_c2 = src_conn.cursor()
            src_c2.execute("SELECT * FROM part WHERE message_id=?", (msg_id,))
            part_rows = src_c2.fetchall()
            part_cols = [d[0] for d in src_c2.description]
            part_placeholders = ', '.join(['?' for _ in part_cols])
            part_col_names = ', '.join([f'"{c}"' for c in part_cols])
            for part_row in part_rows:
                part_values = [replace_paths(part_row[col], path_replacements) for col in part_cols]
                dst_c.execute(f'INSERT INTO part ({part_col_names}) VALUES ({part_placeholders})', part_values)

        print(f"  Session {sid}: OK ({len(msg_rows)} messages)")

    dst_conn.commit()
    dst_conn.close()
    src_conn.close()

    verify_conn = sqlite3.connect(output_path)
    count = verify_conn.execute("SELECT COUNT(*) FROM session").fetchone()[0]
    msg_count = verify_conn.execute("SELECT COUNT(*) FROM message").fetchone()[0]
    part_count = verify_conn.execute("SELECT COUNT(*) FROM part").fetchone()[0]
    verify_conn.close()

    optimize_conn = sqlite3.connect(output_path)
    optimize_conn.execute('VACUUM')
    integrity = optimize_conn.execute('PRAGMA integrity_check').fetchone()[0]
    optimize_conn.close()

    print(f"  Database optimized: VACUUM complete, integrity={integrity}")

    return count, msg_count, part_count


def append_sessions_to_db(db_path, output_path, session_ids, path_replacements):
    """Append new sessions to an existing backup database with path replacement."""
    import sqlite3

    src_conn = sqlite3.connect(db_path)
    src_conn.row_factory = sqlite3.Row
    src_c = src_conn.cursor()

    dst_conn = sqlite3.connect(output_path)
    dst_c = dst_conn.cursor()

    # Ensure schema_version table exists in existing databases
    dst_c.execute(SCHEMA_VERSION_TABLE_SQL)
    dst_c.execute(
        'INSERT OR IGNORE INTO schema_version (version, applied_at, description) VALUES (?, ?, ?)',
        (SCHEMA_VERSION, datetime.datetime.now().isoformat(), 'Schema versioning added')
    )
    dst_conn.commit()

    for sid in session_ids:
        dst_c.execute("SELECT COUNT(*) FROM session WHERE id=?", (sid,))
        if dst_c.fetchone()[0] > 0:
            print(f"  Session {sid}: ALREADY EXISTS, skipping")
            continue

        src_c.execute("SELECT * FROM session WHERE id=?", (sid,))
        row = src_c.fetchone()
        if row is None:
            print(f"  Session {sid}: NOT FOUND")
            continue

        cols = [d[0] for d in src_c.description]
        values = [replace_paths(row[col], path_replacements) for col in cols]
        placeholders = ', '.join(['?' for _ in cols])
        col_names = ', '.join([f'"{c}"' for c in cols])
        dst_c.execute(f'INSERT INTO session ({col_names}) VALUES ({placeholders})', values)

        src_c.execute("SELECT * FROM message WHERE session_id=?", (sid,))
        msg_rows = src_c.fetchall()
        msg_cols = [d[0] for d in src_c.description]
        msg_placeholders = ', '.join(['?' for _ in msg_cols])
        msg_col_names = ', '.join([f'"{c}"' for c in msg_cols])
        for msg_row in msg_rows:
            msg_values = [replace_paths(msg_row[col], path_replacements) for col in msg_cols]
            dst_c.execute(f'INSERT INTO message ({msg_col_names}) VALUES ({msg_placeholders})', msg_values)

            msg_id = msg_row['id']

            src_c2 = src_conn.cursor()
            src_c2.execute("SELECT * FROM part WHERE message_id=?", (msg_id,))
            part_rows = src_c2.fetchall()
            part_cols = [d[0] for d in src_c2.description]
            part_placeholders = ', '.join(['?' for _ in part_cols])
            part_col_names = ', '.join([f'"{c}"' for c in part_cols])
            for part_row in part_rows:
                part_values = [replace_paths(part_row[col], path_replacements) for col in part_cols]
                dst_c.execute(f'INSERT INTO part ({part_col_names}) VALUES ({part_placeholders})', part_values)

        print(f"  Session {sid}: OK ({len(msg_rows)} messages)")

    dst_conn.commit()
    dst_conn.close()
    src_conn.close()

    verify_conn = sqlite3.connect(output_path)
    count = verify_conn.execute("SELECT COUNT(*) FROM session").fetchone()[0]
    msg_count = verify_conn.execute("SELECT COUNT(*) FROM message").fetchone()[0]
    part_count = verify_conn.execute("SELECT COUNT(*) FROM part").fetchone()[0]
    verify_conn.close()

    optimize_conn = sqlite3.connect(output_path)
    optimize_conn.execute('VACUUM')
    integrity = optimize_conn.execute('PRAGMA integrity_check').fetchone()[0]
    optimize_conn.close()

    print(f"  Database optimized: VACUUM complete, integrity={integrity}")

    return count, msg_count, part_count


def prompt(prompt_text):
    val = input(prompt_text).strip()
    return val if val else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ai_developers = _get_ai_developers(script_dir)
    default_developer = ai_developers[0] if ai_developers else 'default'
    
    parser = argparse.ArgumentParser(
        description='Export AI session data into anonymized SQLite databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the source SQLite database')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory (default: .ai-activity/ai-sessions/<developer>)')
    parser.add_argument('--output-name', default=None,
                        help='Output database filename (default: from developer config)')
    parser.add_argument('--developer', default=default_developer,
                        choices=ai_developers,
                        help='AI co-developer (default: %s)' % default_developer)
    parser.add_argument('--current-session', action='store_true',
                        help='Auto-discover and include the current/most-recent session ID')
    parser.add_argument('--sessions', default=None,
                        help='Comma-separated session IDs (overrides JSON config)')
    parser.add_argument('--paths-to-replace', default=None,
                        help='Comma-separated paths to replace with _www_ (overrides JSON config)')
    parser.add_argument('--append', action='store_true',
                        help='Append new sessions to existing database instead of recreating it')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview sessions and path replacements without writing to disk')

    args = parser.parse_args()

    if args.dry_run:
        args.append = True

    if not os.path.exists(args.db_path):
        print(f"ERROR: Database not found at {args.db_path}")
        sys.exit(1)

    # Load path replacements
    if args.paths_to_replace:
        path_replacements = []
        for p in args.paths_to_replace.split(','):
            p = p.strip()
            if p:
                from session_utils import generate_path_variations
                path_replacements.extend(generate_path_variations(p, '_www_'))
        print(f"Using {len(path_replacements)} path replacements from command line")
    else:
        path_replacements_data = load_paths_to_replace(SCRIPT_DIR, args.developer)
        path_replacements = []
        for data in path_replacements_data:
            for base_path in data['paths']:
                from session_utils import generate_path_variations
                path_replacements.extend(generate_path_variations(base_path, data['replacement']))
        print(f"Loaded {len(path_replacements)} path replacements from config")

    # Load session IDs
    if args.sessions:
        session_ids = [s.strip() for s in args.sessions.split(',') if s.strip()]
    else:
        session_ids = load_session_ids(SCRIPT_DIR, args.developer)
        print(f"Loaded {len(session_ids)} session IDs from config")

    # Auto-discover current session if requested
    if args.current_session:
        project_root = os.path.dirname(os.path.dirname(SCRIPT_DIR))
        current_sid = find_current_session_id(project_root, args.developer)
        if not current_sid:
            current_sid = find_current_session_id_from_db(args.db_path)
        if current_sid:
            print(f"Auto-discovered current session: {current_sid}")
            if current_sid not in session_ids:
                session_ids.append(current_sid)
                print(f"  Added current session {current_sid} to backup")

    if not session_ids:
        print("\nNo session IDs found in config or arguments.")
        print("Enter session IDs (one per line, empty line to finish):")
        while True:
            sid = prompt("  Session ID: ")
            if not sid:
                break
            session_ids.append(sid)

    if not session_ids:
        print("ERROR: No session IDs provided.")
        sys.exit(1)

    # Determine output location
    if args.output_dir:
        output_dir = args.output_dir
    else:
        dev_config = get_developer_config(SCRIPT_DIR, args.developer)
        config_dir = dev_config.get('config_dir', args.developer)
        output_dir = os.path.join(os.getcwd(), '.ai-activity', 'ai-sessions', config_dir)
    
    os.makedirs(output_dir, exist_ok=True)

    # Determine output filename
    if args.output_name:
        output_name = args.output_name
    else:
        dev_config = get_developer_config(SCRIPT_DIR, args.developer)
        output_name = dev_config.get('database', 'sessions.db')

    output_db = os.path.join(output_dir, output_name)

    print(f"\nSource DB: {args.db_path}")
    print(f"Output dir: {output_dir}")
    print(f"Developer:  {args.developer}")
    print(f"Sessions:   {len(session_ids)} IDs")
    print(f"Path replacements: {len(path_replacements)} patterns")
    print()

    # Verify sessions exist in source
    import sqlite3
    src_conn = sqlite3.connect(args.db_path)
    src_c = src_conn.cursor()
    found = []
    print("=== Sessions ===")
    for sid in session_ids:
        src_c.execute("SELECT id, title, directory FROM session WHERE id=?", (sid,))
        row = src_c.fetchone()
        if row:
            found.append(sid)
        else:
            print(f"  NOT FOUND: {sid}")
    print(f"  Found {len(found)} of {len(session_ids)} sessions\n")
    src_conn.close()

    # Check if output database already exists
    existing_sessions = []
    if os.path.exists(output_db):
        existing_conn = sqlite3.connect(output_db)
        existing_cursor = existing_conn.cursor()
        existing_cursor.execute("SELECT id, title FROM session")
        existing_sessions = existing_cursor.fetchall()
        existing_conn.close()
        print(f"  Existing database has {len(existing_sessions)} sessions")

    # Safeguard: Confirm overwrite if not in append mode and database exists
    if existing_sessions and not args.append:
        print(f"\nWARNING: Output database already exists with {len(existing_sessions)} sessions:")
        for sid, title in existing_sessions[:5]:
            print(f"  - {sid}: {title}")
        if len(existing_sessions) > 5:
            print(f"  ... and {len(existing_sessions) - 5} more")
        print("\nProceeding will DELETE these sessions and replace with the new selection.")
        response = input("Type 'yes' to confirm overwrite, or 'append' to add new sessions: ").strip().lower()
        if response not in ('yes', 'append'):
            print("Aborted.")
            sys.exit(0)
        if response == 'append':
            args.append = True
            print("Switching to append mode")

    # Use append mode if --append flag is set and database already exists
    if args.dry_run:
        print("\n=== DRY RUN ===")
        print(f"Would append {len(found)} sessions to {output_db}")
        print(f"Path replacements: {len(path_replacements)} patterns")
        print("No data written to disk.")
        sys.exit(0)
    elif args.append and os.path.exists(output_db):
        print("\nAppending to existing database (--append mode)")
        count, msg_count, part_count = append_sessions_to_db(args.db_path, output_db, found, path_replacements)
    else:
        print("\nCreating new database")
        count, msg_count, part_count = backup_sessions(args.db_path, output_db, found, path_replacements)
    print(f"  Done: {count} sessions, {msg_count} messages, {part_count} parts")
    print()
    print("Database updated successfully.")
    print("Run ai-sessions-stats.py to generate/update statistics.")


if __name__ == '__main__':
    main()
