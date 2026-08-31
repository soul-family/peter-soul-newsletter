#!/usr/bin/env python3
"""
ai-sessions-backup.py - Export Kilo session data into project-specific SQLite
databases.

Reads session data (session, message, part tables) from the local Kilo SQLite
database and writes a new database filtered to the specified session IDs, with
all local filesystem paths replaced by _www_ to avoid exposing the local
directory structure.

Configuration is loaded from JSON files so no local paths are hardcoded in the
script itself. This script is shared between co-developer repositories
(website, familytree, etc.) — each repo provides its own session-ids-*.json.

JSON config files (placed next to this script):
  - session-ids-*.json      Files with {"session_ids": [...]}
  - paths-to-replace-*.json  Files with {"paths": [...], "replacement": "_www_"}

Slash form variations are generated automatically from the base paths in the
JSON files — you only need to provide each path in one form.

Usage:
  python .dev-scripts/ai-assistant/ai-sessions-backup.py --db-path <path to kilo.db>

Optional:
  --db-path PATH          Path to the Kilo SQLite database (kilo.db)
  --output-dir DIR        Output directory (default: .ai-activity/ai-sessions/<developer>)
  --developer NAME        AI co-developer to source session IDs from
                          (kilo-code, github-copilot, opencode; default: kilo-code)
  --current-session       Automatically include the most recent session from
                          the selected developer's session directories
  --output-name NAME      Output database name (default: sessions.db)
  --sessions IDS          Comma-separated session IDs (overrides JSON config)
  --paths-to-replace PATHS  Comma-separated paths to replace with _www_ (overrides JSON config)
"""

import argparse
import datetime
import glob
import json
import sqlite3
import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

AI_DEVELOPERS = ['kilo-code', 'opencode', 'github-copilot']


def find_current_session_id(project_root, developer):
    """Find the most recent session ID from a developer's session knowledge folder.

    Looks in `.ai-activity/ai-sessions/<developer>/` directory for session
    transcript files and returns the session ID from the most recently
    modified file. Falls back to the older `_ai_session/<developer>/` path
    for backward compatibility.
    """
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


def find_current_session_id_from_db(db_path):
    """Find the most recent session ID by querying the Kilo SQLite database directly."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM session ORDER BY timestamp DESC, created_at DESC LIMIT 1")
        row = c.fetchone()
        if row:
            return row['id']
    except sqlite3.Error:
        pass
    conn.close()
    return None


def generate_path_variations(base_path, replacement='_www_'):
    """Generate all slash-form variations of a local path for replacement.

    Accepts base paths in any form — bare root (no drive), forward-slash,
    or backslash — and generates all variations so the human JSON config
    only needs to list each path once.
    """
    variations = []

    variations.append((base_path, replacement))

    if '/' in base_path:
        backslash_form = base_path.replace('/', '\\')
        if backslash_form != base_path:
            variations.append((backslash_form, replacement))
            json_form = backslash_form.replace('\\', '\\\\')
            variations.append((json_form, replacement))
    elif '\\' in base_path:
        forward_form = base_path.replace('\\', '/')
        if forward_form != base_path:
            variations.append((forward_form, replacement))
            json_form = base_path.replace('\\', '\\\\')
            variations.append((json_form, replacement))

    if base_path.startswith('C:/'):
        no_drive = base_path[3:]
        variations.append((no_drive, replacement))
        backslash_no_drive = no_drive.replace('/', '\\')
        if backslash_no_drive != no_drive:
            variations.append((backslash_no_drive, replacement))
        json_no_drive = backslash_no_drive.replace('\\', '\\\\')
        if json_no_drive not in variations:
            variations.append((json_no_drive, replacement))
    elif base_path.startswith('C:\\\\'):
        no_drive = base_path[3:]
        variations.append((no_drive, replacement))
    elif base_path.startswith('C:\\'):
        no_drive = base_path[3:]
        variations.append((no_drive, replacement))
    else:
        c_forward = 'C:/' + base_path
        c_backslash = 'C:\\' + base_path.replace('/', '\\')
        json_form = c_backslash.replace('\\', '\\\\')
        variations.append((c_forward, replacement))
        if c_backslash != c_forward:
            variations.append((c_backslash, replacement))
        variations.append((json_form, replacement))

    if '_Vicki_documents' in base_path and base_path != '_Vicki_documents':
        variations.append(('_Vicki_documents', replacement))

    seen = set()
    unique = []
    for old, new in variations:
        if old not in seen:
            seen.add(old)
            unique.append((old, new))
    return unique


def load_paths_from_json_dir(directory):
    """Load and expand path replacement patterns from all paths-to-replace-*.json files."""
    pattern = os.path.join(directory, 'paths-to-replace-*.json')
    all_replacements = []
    for json_path in sorted(glob.glob(pattern)):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            paths = data.get('paths', [])
            replacement = data.get('replacement', '_www_')
            for base_path in paths:
                variations = generate_path_variations(base_path, replacement)
                all_replacements.extend(variations)
            print(f"Loaded {len(paths)} base paths from {os.path.basename(json_path)} "
                  f"({len(variations)} variations)")
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            print(f"Warning: invalid JSON in {json_path}: {e}")

    seen = set()
    unique = []
    for old, new in all_replacements:
        if old not in seen:
            seen.add(old)
            unique.append((old, new))
    return unique


def load_session_ids_from_json_dir(directory):
    """Load session IDs from all session-ids-*.json files.

    Each file should contain {"session_ids": [...]}.
    The aggregate list is the union of all session_ids across files,
    deduplicated while preserving order.
    """
    pattern = os.path.join(directory, 'session-ids-*.json')
    seen = set()
    ids = []
    for json_path in sorted(glob.glob(pattern)):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            file_ids = data.get('session_ids', [])
            added = 0
            for sid in file_ids:
                if sid not in seen:
                    seen.add(sid)
                    ids.append(sid)
                    added += 1
            print(f"Loaded {added} session IDs from {os.path.basename(json_path)}")
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            print(f"Warning: invalid JSON in {json_path}: {e}")
    return ids


def replace_paths(data, replacements):
    """Recursively replace local paths in any data structure."""
    if data is None:
        return None
    if isinstance(data, str):
        for old, new in replacements:
            data = data.replace(old, new)
        return data
    if isinstance(data, bytes):
        for old, new in replacements:
            data = data.replace(old.encode('utf-8'), new.encode('utf-8'))
        return data
    if isinstance(data, dict):
        return {k: replace_paths(v, replacements) for k, v in data.items()}
    if isinstance(data, list):
        return [replace_paths(v, replacements) for v in data]
    return data


def get_schema(conn):
    """Return table schemas for session, message, and part tables."""
    c = conn.cursor()
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name IN ('session', 'message', 'part')")
    return {name: sql for name, sql in c.fetchall()}


def backup_sessions(db_path, output_path, session_ids, path_replacements):
    """Create a filtered, path-anonymized backup database."""
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
    dst_conn.commit()

    for sid in session_ids:
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

    return count, msg_count, part_count


def humanize(seconds):
    if seconds is None or seconds == 0:
        return '0m'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f'{h}h {m}m'
    return f'{m}m'


def ms_to_dt(ms):
    if ms is None:
        return None
    try:
        return datetime.datetime.fromtimestamp(ms / 1000)
    except (ValueError, OSError, OverflowError):
        return None


def format_dt(dt):
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%d %H:%M')


USER_INPUT_TIME_TIERS = [
    (9, 15),
    (49, 60),
    (199, 180),
    (499, 360),
    (float('inf'), 600),
]


def user_input_seconds_for_text(text):
    if not text:
        return 0
    words = len(text.split())
    for max_words, seconds in USER_INPUT_TIME_TIERS:
        if words <= max_words:
            return seconds
    return USER_INPUT_TIME_TIERS[-1][1]


def generate_stats(db_path, output_path):
    """Generate a stats JSON file alongside a backup database.

    Includes per-session breakdowns: message counts, parts, thinking length,
    user request count, durations (total, user input, AI processing), and totals.
    Title and cost are intentionally excluded to keep stats focused on
    activity metrics only.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    stats = {
        'database': os.path.basename(output_path),
        'generated_at': datetime.datetime.now().isoformat(),
        'totals': {},
        'sessions': []
    }

    c.execute('SELECT session_id, COUNT(*) FROM message GROUP BY session_id')
    msg_by_session = {row[0]: row[1] for row in c.fetchall()}

    c.execute('SELECT COUNT(*) FROM session')
    stats['totals']['sessions'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM message')
    stats['totals']['messages'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM part')
    stats['totals']['parts'] = c.fetchone()[0]

    c.execute('SELECT id, directory, time_created, time_updated FROM session ORDER BY time_created')
    for row in c.fetchall():
        sid = row[0]
        directory = row[1]
        created_ms = row[2]
        updated_ms = row[3]

        c2 = conn.cursor()

        c2.execute('SELECT COUNT(*) FROM message WHERE session_id=?', (sid,))
        msg_count = c2.fetchone()[0]
        c2.execute('SELECT COUNT(*) FROM part WHERE message_id IN (SELECT id FROM message WHERE session_id=?)', (sid,))
        part_count = c2.fetchone()[0]

        c2.execute('''
            SELECT m.time_created, p.data
            FROM message m
            JOIN part p ON p.message_id = m.id
            WHERE m.session_id=?
            AND json_extract(m.data, '$.role')='user'
            AND json_extract(p.data, '$.type')='text'
        ''', (sid,))
        user_msgs = c2.fetchall()

        user_input_total_s = 0
        word_count_distribution = {'1-9': 0, '10-49': 0, '50-199': 0, '200-499': 0, '500+': 0}
        word_count_total = 0
        for row in user_msgs:
            pdata = json.loads(row[1])
            text = pdata.get('text', '')
            words = len(text.split())
            word_count_total += words
            if words <= 9:
                word_count_distribution['1-9'] += 1
            elif words <= 49:
                word_count_distribution['10-49'] += 1
            elif words <= 199:
                word_count_distribution['50-199'] += 1
            elif words <= 499:
                word_count_distribution['200-499'] += 1
            else:
                word_count_distribution['500+'] += 1
            user_input_total_s += user_input_seconds_for_text(text)

        c2.execute(
            'SELECT data FROM message WHERE session_id=? AND json_extract(data, "$.role") = "assistant"',
            (sid,))
        ai_total_ms = 0
        ai_count = 0
        tokens_input = 0
        tokens_output = 0
        tokens_reasoning = 0
        for row in c2.fetchall():
            data = json.loads(row[0])
            t = data.get('time', {})
            created = t.get('created')
            completed = t.get('completed')
            if created and completed and completed > created:
                ai_count += 1
                ai_total_ms += (completed - created)
            tk = data.get('tokens', {})
            tokens_input += tk.get('input', 0)
            tokens_output += tk.get('output', 0)
            tokens_reasoning += tk.get('reasoning', 0)

        total_active_s = int(ai_total_ms / 1000) + user_input_total_s

        d = {
            'total_seconds': total_active_s,
            'total_human': humanize(total_active_s),
            'ai_processing_seconds': int(ai_total_ms / 1000),
            'ai_processing_human': humanize(int(ai_total_ms / 1000)),
            'ai_processing_count': ai_count,
            'user_input_seconds': user_input_total_s,
            'user_input_human': humanize(user_input_total_s),
            'user_input_word_total': word_count_total,
            'user_input_word_distribution': word_count_distribution,
            'user_input_avg_seconds': user_input_total_s // max(1, len(user_msgs)),
        }

        stats['sessions'].append({
            'id': sid,
            'directory': directory,
            'created': format_dt(ms_to_dt(created_ms)),
            'updated': format_dt(ms_to_dt(updated_ms)),
            'message_count': msg_count,
            'part_count': part_count,
            'user_request_count': len(user_msgs),
            'thinking_length': 0,
            'tokens_input': tokens_input,
            'tokens_output': tokens_output,
            'tokens_reasoning': tokens_reasoning,
            'durations': d,
        })

    c.execute('''
        SELECT p.session_id, p.data FROM part p
        WHERE json_extract(p.data, '$.type') = 'reasoning'
    ''')
    thinking_by_session = {}
    for row in c.fetchall():
        sid = row[0]
        pdata = json.loads(row[1])
        text = pdata.get('text', '')
        thinking_by_session[sid] = thinking_by_session.get(sid, 0) + len(text)

    for s in stats['sessions']:
        s['thinking_length'] = thinking_by_session.get(s['id'], 0)
        d = s['durations']
        d['user_input_avg_words'] = d.get('user_input_word_total', 0) // max(1, s['user_request_count'])

    total_thinking = sum(thinking_by_session.values())
    total_active = sum(s['durations']['total_seconds'] for s in stats['sessions'])
    total_ai = sum(s['durations']['ai_processing_seconds'] for s in stats['sessions'])
    total_user_input = sum(s['durations']['user_input_seconds'] for s in stats['sessions'])
    total_user_words = sum(s['durations']['user_input_word_total'] for s in stats['sessions'])
    total_tokens_input = sum(s['tokens_input'] for s in stats['sessions'])
    total_tokens_output = sum(s['tokens_output'] for s in stats['sessions'])
    total_tokens_reasoning = sum(s['tokens_reasoning'] for s in stats['sessions'])

    stats['totals']['thinking_length'] = total_thinking
    stats['totals']['user_requests'] = sum(s['user_request_count'] for s in stats['sessions'])
    stats['totals']['tokens_input'] = total_tokens_input
    stats['totals']['tokens_output'] = total_tokens_output
    stats['totals']['tokens_reasoning'] = total_tokens_reasoning
    stats['totals']['total_duration_seconds'] = total_active
    stats['totals']['total_duration_human'] = humanize(total_active)
    stats['totals']['total_ai_processing_seconds'] = total_ai
    stats['totals']['total_ai_processing_human'] = humanize(total_ai)
    stats['totals']['total_user_input_seconds'] = total_user_input
    stats['totals']['total_user_input_human'] = humanize(total_user_input)
    stats['totals']['total_user_input_words'] = total_user_words
    stats['totals']['user_input_tier_distribution'] = {}
    for s in stats['sessions']:
        for tier, count in s['durations'].get('user_input_word_distribution', {}).items():
            stats['totals']['user_input_tier_distribution'][tier] = \
                stats['totals']['user_input_tier_distribution'].get(tier, 0) + count

    conn.close()

    stats_path = output_path.replace('.db', '.stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"  Stats written: {stats_path}")


def prompt(prompt_text):
    val = input(prompt_text).strip()
    return val if val else None


def main():
    parser = argparse.ArgumentParser(
        description='Export Kilo session data into anonymized SQLite databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the Kilo SQLite database (kilo.db)')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory (default: .ai-activity/ai-sessions/<developer>)')
    parser.add_argument('--output-name', default='sessions.db',
                        help='Output database filename (default: sessions.db)')
    parser.add_argument('--developer', default='kilo-code',
                        choices=AI_DEVELOPERS,
                        help='AI co-developer whose session IDs to use (default: kilo-code)')
    parser.add_argument('--current-session', action='store_true',
                        help='Auto-discover and include the current/most-recent session ID')
    parser.add_argument('--sessions', default=None,
                        help='Comma-separated session IDs (overrides JSON config)')
    parser.add_argument('--paths-to-replace', default=None,
                        help='Comma-separated paths to replace with _www_ (overrides JSON config)')

    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"ERROR: Database not found at {args.db_path}")
        sys.exit(1)

    if args.paths_to_replace:
        path_replacements = [(p.strip(), '_www_') for p in args.paths_to_replace.split(',') if p.strip()]
        print(f"Using {len(path_replacements)} path replacements from command line")
    else:
        path_replacements = load_paths_from_json_dir(SCRIPT_DIR)
        if not path_replacements:
            print("No path replacements loaded. Provide --paths-to-replace or place paths-to-replace-*.json next to script.")
            sys.exit(1)

    session_ids = []
    if args.sessions:
        session_ids = [s.strip() for s in args.sessions.split(',') if s.strip()]
    else:
        session_ids = load_session_ids_from_json_dir(SCRIPT_DIR)

    if args.current_session:
        current_sid = find_current_session_id(PROJECT_ROOT, args.developer)
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

    output_dir = args.output_dir or os.path.join(os.getcwd(), '.ai-activity', 'ai-sessions', args.developer)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nSource DB: {args.db_path}")
    print(f"Output dir: {output_dir}")
    print(f"Developer:  {args.developer}")
    print(f"Sessions:   {len(session_ids)} IDs")
    print(f"Path replacements:    {len(path_replacements)} patterns")
    print()

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

    output_db = os.path.join(output_dir, args.output_name)
    print(f"Creating database: {output_db}")
    count, msg_count, part_count = backup_sessions(args.db_path, output_db, found, path_replacements)
    print(f"  Done: {count} sessions, {msg_count} messages, {part_count} parts")
    generate_stats(output_db, output_db)
    print()
    print("Database created successfully.")


if __name__ == '__main__':
    main()
