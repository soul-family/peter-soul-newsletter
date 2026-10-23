#!/usr/bin/env python3
"""
ai-sessions-stats.py - Generate statistics for AI session databases.

Reads session data from project-specific SQLite databases and generates
stats JSON files with per-session breakdowns including:
- Message counts, parts, thinking length
- User request counts and word distribution
- AI processing time (wall-clock)
- User activity time (input phase + output phase)

Can run in two modes:
  Full:    Regenerates stats for all sessions (default)
  Incremental: Only processes sessions not already in the stats file

Usage:
  python .dev-scripts/ai-sessions/ai-sessions-stats.py --db-path <path to .db>
  python .dev-scripts/ai-sessions/ai-sessions-stats.py --db-path <path> --incremental
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys

# Add shared directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'shared'))

from session_utils import (
    humanize,
    ms_to_dt,
    format_dt,
    user_input_seconds_for_text,
    calculate_response_review_seconds,
    INITIAL_WAITING_SECONDS,
    VERIFICATION_SECONDS,
)
from config_loader import get_developer_config, get_developer_ids


def process_all_sessions(conn, session_rows):
    """Process all sessions efficiently with pre-loaded data."""
    # Pre-load all messages and parts for all sessions
    sids = [row[0] for row in session_rows]
    placeholders = ','.join(['?' for _ in sids])

    c = conn.cursor()

    # Get all messages for all sessions
    c.execute(f'''
        SELECT id, session_id, data
        FROM message
        WHERE session_id IN ({placeholders})
    ''', sids)
    all_messages = c.fetchall()

    # Organize messages by session
    messages_by_session = {}
    for msg in all_messages:
        sid = msg[1]
        if sid not in messages_by_session:
            messages_by_session[sid] = []
        messages_by_session[sid].append(msg)

    # Get all parts for all messages
    msg_ids = [msg[0] for msg in all_messages]
    if msg_ids:
        placeholders = ','.join(['?' for _ in msg_ids])
        c.execute(f'''
            SELECT id, message_id, session_id, data
            FROM part
            WHERE message_id IN ({placeholders})
        ''', msg_ids)
        all_parts = c.fetchall()
    else:
        all_parts = []

    # Organize parts by message
    parts_by_message = {}
    for part in all_parts:
        mid = part[1]
        if mid not in parts_by_message:
            parts_by_message[mid] = []
        parts_by_message[mid].append(part)

    # Process each session
    results = []
    for row in session_rows:
        sid = row[0]
        directory = row[1]
        created_ms = row[2]
        updated_ms = row[3]

        session_messages = messages_by_session.get(sid, [])
        msg_count = len(session_messages)
        part_count = sum(len(parts_by_message.get(msg[0], [])) for msg in session_messages)

        # Get user messages with text parts
        user_msgs = []
        for msg in session_messages:
            msg_data = json.loads(msg[2])
            if msg_data.get('role') == 'user':
                # Get text parts for this message
                for part in parts_by_message.get(msg[0], []):
                    part_data = json.loads(part[3])
                    if part_data.get('type') == 'text':
                        user_msgs.append(part_data.get('text', ''))

        # Get assistant messages
        assistant_msgs = []
        for msg in session_messages:
            msg_data = json.loads(msg[2])
            if msg_data.get('role') == 'assistant':
                assistant_msgs.append((msg[0], msg_data))

        writing_time_s = 0
        waiting_time_s = 0
        review_time_s = 0
        verification_time_s = 0
        word_count_distribution = {'1-9': 0, '10-49': 0, '50-199': 0, '200-499': 0, '500+': 0}
        word_count_total = 0

        for text in user_msgs:
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

            writing_time_s += user_input_seconds_for_text(text)
            waiting_time_s += INITIAL_WAITING_SECONDS
            verification_time_s += VERIFICATION_SECONDS

        for msg_id, asst_data in assistant_msgs:
            # Count parts for this assistant message
            asst_parts = parts_by_message.get(msg_id, [])
            asst_part_count = len(asst_parts)

            # Get final message text (last text part)
            final_text = ''
            for part in reversed(asst_parts):
                part_data = json.loads(part[3])
                if part_data.get('type') == 'text':
                    final_text = part_data.get('text', '')
                    break

            review_time_s += calculate_response_review_seconds(asst_part_count, final_text)

        user_activity_total_s = writing_time_s + waiting_time_s + review_time_s + verification_time_s

        ai_total_ms = 0
        ai_count = 0
        tokens_input = 0
        tokens_output = 0
        tokens_reasoning = 0
        for msg_id, asst_data in assistant_msgs:
            t = asst_data.get('time', {})
            created = t.get('created')
            completed = t.get('completed')
            if created and completed and completed > created:
                ai_count += 1
                ai_total_ms += (completed - created)
            tk = asst_data.get('tokens', {})
            tokens_input += tk.get('input', 0)
            tokens_output += tk.get('output', 0)
            tokens_reasoning += tk.get('reasoning', 0)

        total_active_s = int(ai_total_ms / 1000) + user_activity_total_s

        # Individual sessions store seconds and human-readable durations
        d = {
            'total_seconds': total_active_s,
            'total_human': humanize(total_active_s),
            'ai_processing_seconds': int(ai_total_ms / 1000),
            'ai_processing_human': humanize(int(ai_total_ms / 1000)),
            'ai_processing_count': ai_count,
            'user_activity_seconds': user_activity_total_s,
            'user_activity_human': humanize(user_activity_total_s),
            'user_activity_word_total': word_count_total,
            'user_activity_word_distribution': word_count_distribution,
            'user_activity_avg_seconds': user_activity_total_s // max(1, len(user_msgs)),
            'user_activity_avg_words': word_count_total // max(1, len(user_msgs)),
            'user_activity_writing_seconds': writing_time_s,
            'user_activity_writing_human': humanize(writing_time_s),
            'user_activity_waiting_seconds': waiting_time_s,
            'user_activity_waiting_human': humanize(waiting_time_s),
            'user_activity_review_seconds': review_time_s,
            'user_activity_review_human': humanize(review_time_s),
            'user_activity_verification_seconds': verification_time_s,
            'user_activity_verification_human': humanize(verification_time_s),
        }

        results.append({
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

    return results


def _normalize_session(s):
    """Normalize a session from old stats format to new format."""
    import copy
    s = copy.deepcopy(s)

    d = s.get('durations', {})

    # Old format had tokens and thinking_length inside durations
    # Move them to top level if they're there
    for key in ['tokens_input', 'tokens_output', 'tokens_reasoning', 'thinking_length', 'user_request_count']:
        if key in d and key not in s:
            s[key] = d[key]
            d.pop(key)

    # Ensure top-level fields exist
    if 'user_request_count' not in s:
        s['user_request_count'] = d.get('user_request_count', 0)

    # Map ALL old field names to new field names
    field_mappings = {
        'user_input_phase_seconds': 'user_activity_writing_seconds',
        'user_output_phase_seconds': 'user_activity_review_seconds',
        'user_activity_seconds': 'user_activity_seconds',
        'user_writing_seconds': 'user_activity_writing_seconds',
        'user_waiting_seconds': 'user_activity_waiting_seconds',
        'user_review_seconds': 'user_activity_review_seconds',
        'user_verification_seconds': 'user_activity_verification_seconds',
        'user_word_total': 'user_activity_word_total',
        'user_word_distribution': 'user_activity_word_distribution',
        'user_input_seconds': 'user_activity_seconds',
        'user_input_word_total': 'user_activity_word_total',
        'user_input_word_distribution': 'user_activity_word_distribution',
        'user_input_avg_seconds': 'user_activity_avg_seconds',
        'user_input_writing_seconds': 'user_activity_writing_seconds',
        'user_input_waiting_seconds': 'user_activity_waiting_seconds',
        'user_input_review_seconds': 'user_activity_review_seconds',
        'user_input_verification_seconds': 'user_activity_verification_seconds',
        'user_input_avg_words': 'user_activity_avg_words',
    }

    for old_key, new_key in field_mappings.items():
        if old_key in d:
            d[new_key] = d[old_key]

    # Remove old field names from durations to keep output clean
    # Only remove keys that were actually old field names, not identity mappings
    for old_key, new_key in field_mappings.items():
        if old_key != new_key and old_key in d:
            d.pop(old_key)

    # Ensure all required fields exist with defaults
    defaults = {
        'user_activity_seconds': 0,
        'user_activity_writing_seconds': 0,
        'user_activity_waiting_seconds': 0,
        'user_activity_review_seconds': 0,
        'user_activity_verification_seconds': 0,
        'user_activity_word_total': 0,
        'user_activity_word_distribution': {'1-9': 0, '10-49': 0, '50-199': 0, '200-499': 0, '500+': 0},
        'user_activity_avg_seconds': 0,
        'user_activity_avg_words': 0,
        'total_seconds': 0,
        'ai_processing_seconds': 0,
        'ai_processing_count': 0,
    }

    for key, default in defaults.items():
        if key not in d:
            d[key] = default

    s['durations'] = d
    return s


def generate_stats(db_path, stats_path=None, incremental=False):
    """Generate stats JSON file for a session database.
    
    Args:
        db_path: Path to the session database
        stats_path: Path to write stats JSON (default: db_path.replace('.db', '.stats.json'))
        incremental: Only process new sessions not in existing stats file
    """
    if not stats_path:
        stats_path = db_path.replace('.db', '.stats.json')

    existing_sessions = {}
    if incremental and os.path.exists(stats_path):
        try:
            with open(stats_path, 'r', encoding='utf-8') as f:
                old_stats = json.load(f)
            for s in old_stats.get('sessions', []):
                existing_sessions[s['id']] = s
            print(f"Loaded {len(existing_sessions)} existing session stats")
        except (json.JSONDecodeError, IOError):
            pass

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    stats = {
        'database': os.path.basename(db_path),
        'generated_at': datetime.datetime.now().isoformat(),
        'totals': {},
        'sessions': []
    }

    c.execute('SELECT COUNT(*) FROM session')
    stats['totals']['sessions'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM message')
    stats['totals']['messages'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM part')
    stats['totals']['parts'] = c.fetchone()[0]

    c.execute('SELECT id, directory, time_created, time_updated FROM session ORDER BY time_created')
    session_rows = c.fetchall()

    # Separate sessions into cached and new
    cached_sessions = []
    new_session_rows = []
    for row in session_rows:
        sid = row[0]
        if incremental and sid in existing_sessions:
            cached_sessions.append(existing_sessions[sid])
        else:
            new_session_rows.append(row)

    # Add cached sessions (normalized)
    for old_session in cached_sessions:
        normalized = _normalize_session(old_session)
        stats['sessions'].append(normalized)
        print(f"  Session {normalized['id']}: CACHED")

    # Process new sessions efficiently
    if new_session_rows:
        new_stats = process_all_sessions(conn, new_session_rows)
        stats['sessions'].extend(new_stats)
        for s in new_stats:
            print(f"  Session {s['id']}: PROCESSED ({s['message_count']} messages)")

    # Calculate thinking length
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
        # user_request_count may not be present in cached sessions
        req_count = s.get('user_request_count', d.get('user_activity_word_total', 0))
        d['user_activity_avg_words'] = d.get('user_activity_word_total', 0) // max(1, req_count)

    # Calculate totals
    total_thinking = sum(thinking_by_session.values())
    total_active = sum(s['durations']['total_seconds'] for s in stats['sessions'])
    total_ai = sum(s['durations']['ai_processing_seconds'] for s in stats['sessions'])
    total_user_activity = sum(s['durations'].get('user_activity_seconds', s['durations'].get('user_input_seconds', 0)) for s in stats['sessions'])
    total_user_words = sum(s['durations'].get('user_activity_word_total', s['durations'].get('user_input_word_total', 0)) for s in stats['sessions'])
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
    stats['totals']['total_user_activity_seconds'] = total_user_activity
    stats['totals']['total_user_activity_human'] = humanize(total_user_activity)
    stats['totals']['total_user_activity_words'] = total_user_words
    stats['totals']['total_user_activity_writing_seconds'] = sum(s['durations'].get('user_activity_writing_seconds', s['durations'].get('user_input_writing_seconds', 0)) for s in stats['sessions'])
    stats['totals']['total_user_activity_writing_human'] = humanize(stats['totals']['total_user_activity_writing_seconds'])
    stats['totals']['total_user_activity_waiting_seconds'] = sum(s['durations'].get('user_activity_waiting_seconds', s['durations'].get('user_input_waiting_seconds', 0)) for s in stats['sessions'])
    stats['totals']['total_user_activity_waiting_human'] = humanize(stats['totals']['total_user_activity_waiting_seconds'])
    stats['totals']['total_user_activity_review_seconds'] = sum(s['durations'].get('user_activity_review_seconds', s['durations'].get('user_input_review_seconds', 0)) for s in stats['sessions'])
    stats['totals']['total_user_activity_review_human'] = humanize(stats['totals']['total_user_activity_review_seconds'])
    stats['totals']['total_user_activity_verification_seconds'] = sum(s['durations'].get('user_activity_verification_seconds', s['durations'].get('user_input_verification_seconds', 0)) for s in stats['sessions'])
    stats['totals']['total_user_activity_verification_human'] = humanize(stats['totals']['total_user_activity_verification_seconds'])
    stats['totals']['user_activity_tier_distribution'] = {}
    for s in stats['sessions']:
        for tier, count in s['durations'].get('user_activity_word_distribution', s['durations'].get('user_input_word_distribution', {})).items():
            stats['totals']['user_activity_tier_distribution'][tier] = \
                stats['totals']['user_activity_tier_distribution'].get(tier, 0) + count

    conn.close()

    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\nStats written: {stats_path}")
    print(f"  Sessions: {stats['totals']['sessions']}")
    print(f"  Messages: {stats['totals']['messages']}")
    print(f"  Parts: {stats['totals']['parts']}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ai_developers = get_developer_ids(script_dir)
    default_developer = ai_developers[0] if ai_developers else 'default'
    
    parser = argparse.ArgumentParser(
        description='Generate statistics for AI session databases.'
    )
    parser.add_argument('--db-path', required=True,
                        help='Path to the session database (.db)')
    parser.add_argument('--incremental', action='store_true',
                        help='Only process new sessions not in existing stats file')
    parser.add_argument('--developer', default=default_developer,
                        choices=ai_developers,
                        help='AI co-developer (default: %s)' % default_developer)

    args = parser.parse_args()

    if not os.path.exists(args.db_path):
        print(f"ERROR: Database not found at {args.db_path}")
        sys.exit(1)

    print(f"Database: {args.db_path}")
    print(f"Developer: {args.developer}")
    print(f"Mode: {'incremental' if args.incremental else 'full'}")
    print()

    # Load developer config
    dev_config = get_developer_config(SCRIPT_DIR, args.developer)
    db_filename = os.path.basename(args.db_path)
    
    # If developer config doesn't match the actual database, derive stats filename from db
    if dev_config.get('database') != db_filename:
        output_name = db_filename.replace('.db', '.stats.json')
    else:
        output_name = dev_config.get('stats_file', db_filename.replace('.db', '.stats.json'))
    
    stats_path = os.path.join(os.path.dirname(args.db_path), output_name)

    generate_stats(args.db_path, stats_path=stats_path, incremental=args.incremental)


if __name__ == '__main__':
    main()
