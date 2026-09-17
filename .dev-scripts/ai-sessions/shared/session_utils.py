#!/usr/bin/env python3
"""
shared/session_utils.py - Shared utilities for AI session backup and stats.

This module provides common functions used by both the backup script
and the stats generation script.
"""

import datetime
import glob
import json
import os
import re
import sqlite3

# Time constants for user input activities
USER_INPUT_TIME_TIERS = [
    (9, 15),
    (49, 60),
    (199, 180),
    (499, 360),
    (float('inf'), 600),
]

INITIAL_WAITING_SECONDS = 10
REVIEW_INITIAL_SECONDS = 10
REVIEW_PER_5_PARTS_SECONDS = 5
VERIFICATION_SECONDS = 180

REGEX_INDICATORS = re.compile(r'(?<!\\)\\(?:d|w|s|b|D|W|S|A|Z|z)|^\^.*\$$|^\^.*\$')


def is_regex_pattern(pattern):
    """Check if a string looks like a regex pattern."""
    return bool(REGEX_INDICATORS.search(str(pattern)))


def get_repo_root():
    """Dynamically determine the repository root from the script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    return repo_root


def get_repo_name():
    """Dynamically determine the repository folder name."""
    return os.path.basename(get_repo_root())


def strip_jsonc_comments(text):
    """Remove // and /* */ comments from JSONC text."""
    result = []
    in_string = False
    escape_next = False
    i = 0
    while i < len(text):
        char = text[i]
        if escape_next:
            result.append(char)
            escape_next = False
            i += 1
            continue
        if char == '\\' and in_string:
            result.append(char)
            escape_next = True
            i += 1
            continue
        if char == '"' and not in_string:
            in_string = True
            result.append(char)
            i += 1
            continue
        if char == '"' and in_string:
            in_string = False
            result.append(char)
            i += 1
            continue
        if not in_string and char == '/' and i + 1 < len(text) and text[i + 1] == '/':
            while i < len(text) and text[i] != '\n':
                i += 1
            continue
        if not in_string and char == '/' and i + 1 < len(text) and text[i + 1] == '*':
            i += 2
            while i < len(text) and not (text[i] == '*' and i + 1 < len(text) and text[i + 1] == '/'):
                i += 1
            i += 2
            continue
        result.append(char)
        i += 1
    return ''.join(result)


def parse_jsonc(text):
    """Parse JSONC text by stripping comments then loading JSON."""
    clean = strip_jsonc_comments(text)
    return json.loads(clean)


def humanize(seconds):
    """Convert seconds to human-readable format."""
    if seconds is None or seconds == 0:
        return '0m'
    h = seconds // 3600
    m = (seconds % 3600) // 60
    if h > 0:
        return f'{h}h {m}m'
    return f'{m}m'


def ms_to_dt(ms):
    """Convert milliseconds to datetime."""
    if ms is None:
        return None
    try:
        return datetime.datetime.fromtimestamp(ms / 1000)
    except (ValueError, OSError, OverflowError):
        return None


def format_dt(dt):
    """Format datetime as string."""
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%d %H:%M')


def user_input_seconds_for_text(text):
    """Estimate user input time based on text length."""
    if not text:
        return 0
    words = len(text.split())
    for max_words, seconds in USER_INPUT_TIME_TIERS:
        if words <= max_words:
            return seconds
    return USER_INPUT_TIME_TIERS[-1][1]


def calculate_response_review_seconds(part_count, final_message_text):
    """Calculate user review time based on response parts and final message length."""
    review_seconds = REVIEW_INITIAL_SECONDS
    if part_count > 5:
        review_seconds += REVIEW_PER_5_PARTS_SECONDS * ((part_count - 1) // 5)
    review_seconds += user_input_seconds_for_text(final_message_text)
    return review_seconds


def get_schema(conn):
    """Return table schemas for session, message, and part tables."""
    c = conn.cursor()
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name IN ('session', 'message', 'part')")
    return {name: sql for name, sql in c.fetchall()}


def generate_path_variations(base_path, replacement='_www_'):
    """Generate all slash-form variations of a local path for replacement."""
    if is_regex_pattern(base_path):
        return [(re.compile(base_path), replacement, True)]

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


def replace_paths(data, replacements):
    """Recursively replace local paths in any data structure."""
    if data is None:
        return None
    if isinstance(data, str):
        for item in replacements:
            if len(item) == 3:
                old, new, is_regex = item
                if is_regex:
                    data = old.sub(new, data)
                else:
                    data = data.replace(old, new)
            else:
                old, new = item
                data = data.replace(old, new)
        return data
    if isinstance(data, bytes):
        for item in replacements:
            if len(item) == 3:
                old, new, is_regex = item
                if is_regex:
                    data = old.sub(new.encode('utf-8'), data)
                else:
                    data = data.replace(old.encode('utf-8'), new.encode('utf-8'))
            else:
                old, new = item
                data = data.replace(old.encode('utf-8'), new.encode('utf-8'))
        return data
    if isinstance(data, dict):
        return {k: replace_paths(v, replacements) for k, v in data.items()}
    if isinstance(data, list):
        return [replace_paths(v, replacements) for v in data]
    return data


def load_paths_from_json_dir(directory):
    """Load and expand path replacement patterns from all paths-to-replace files."""
    patterns = [
        os.path.join(directory, 'readonly-paths-to-replace.jsonc'),
        os.path.join(directory, 'readonly-paths-to-replace.json'),
        os.path.join(directory, 'paths-to-replace.jsonc'),
        os.path.join(directory, 'paths-to-replace.json'),
        os.path.join(directory, 'readonly-paths-to-replace-*.jsonc'),
        os.path.join(directory, 'readonly-paths-to-replace-*.json'),
        os.path.join(directory, 'paths-to-replace-*.jsonc'),
        os.path.join(directory, 'paths-to-replace-*.json'),
    ]
    all_replacements = []
    for pattern in patterns:
        for jsonc_path in sorted(glob.glob(pattern)):
            try:
                with open(jsonc_path, 'r', encoding='utf-8') as f:
                    data = parse_jsonc(f.read())
            except FileNotFoundError:
                continue
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: invalid JSONC in {jsonc_path}: {e}")
                continue

            rules = data.get('rules')
            if rules is not None:
                for rule in rules:
                    paths = rule.get('paths', [])
                    replacement = rule.get('replacement', '_www_')
                    if isinstance(paths, str):
                        paths = [paths]
                    for base_path in paths:
                        variations = generate_path_variations(base_path, replacement)
                        all_replacements.extend(variations)
            else:
                paths = data.get('paths', [])
                replacement = data.get('replacement', '_www_')
                if isinstance(paths, str):
                    paths = [paths]
                for base_path in paths:
                    variations = generate_path_variations(base_path, replacement)
                    all_replacements.extend(variations)

    has_catch_all = any(
        len(item) > 2 and item[2] and hasattr(item[0], 'pattern') and item[0].pattern in ('^.*$', '.*')
        for item in all_replacements
    )
    if not has_catch_all:
        repo_name = get_repo_name()
        if repo_name:
            escaped = re.escape(repo_name)
            default_pattern = re.compile(f'^.*{escaped}$')
            all_replacements.append((default_pattern, '_www_', True))

    seen = set()
    unique = []
    for item in all_replacements:
        old, new = item[0], item[1]
        is_regex = item[2] if len(item) > 2 else False
        key = (old.pattern if hasattr(old, 'pattern') else old, new)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def load_session_ids_from_json_dir(directory):
    """Load session IDs from all session-ids files."""
    patterns = [
        os.path.join(directory, 'session-ids.jsonc'),
        os.path.join(directory, 'session-ids.json'),
        os.path.join(directory, 'session-ids-*.jsonc'),
        os.path.join(directory, 'session-ids-*.json'),
    ]
    seen = set()
    ids = []
    for pattern in patterns:
        for jsonc_path in sorted(glob.glob(pattern)):
            try:
                with open(jsonc_path, 'r', encoding='utf-8') as f:
                    data = parse_jsonc(f.read())
            except FileNotFoundError:
                continue
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: invalid JSONC in {jsonc_path}: {e}")
                continue
            file_ids = data.get('session_ids', [])
            for sid in file_ids:
                if sid not in seen:
                    seen.add(sid)
                    ids.append(sid)
    return ids
