#!/usr/bin/env python3
"""
shared/config_loader.py - Configuration loader for AI session tools.

Provides functions to load developer-specific configurations:
- Database schemas
- Path replacement rules
- Session ID lists
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_utils import parse_jsonc


def _load_jsonc(path):
    """Load a JSON or JSONC file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return parse_jsonc(f.read())
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Warning: invalid JSONC in {path}: {e}")
        return None


def load_developers(script_dir):
    """Load AI developer definitions from ai-developers.json."""
    config_path = os.path.join(script_dir, 'ai-developers.json')
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(script_dir), 'ai-developers.json')
    if not os.path.exists(config_path):
        config_path = os.path.join(script_dir, 'ai-developers.jsonc')
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(script_dir), 'ai-developers.jsonc')
    
    if not os.path.exists(config_path):
        return {'ai-tools': [{'id': 'default', 'name': 'Default', 'config_dir': '.'}]}
    
    data = _load_jsonc(config_path)
    return data if data else {'ai-tools': [{'id': 'default', 'name': 'Default', 'config_dir': '.'}]}


def get_developer_ids(script_dir):
    """Get list of available developer IDs from config."""
    devs = load_developers(script_dir)
    return [dev.get('id') for dev in devs.get('ai-tools', []) if isinstance(dev, dict)]


def get_developer_config(script_dir, developer_id):
    """Get configuration for a specific developer."""
    devs = load_developers(script_dir)
    
    for dev in devs.get('ai-tools', []):
        if isinstance(dev, dict):
            if dev.get('id') == developer_id:
                return dev
        elif dev == developer_id:
            return {'id': developer_id, 'config_dir': '.'}
    
    return {'id': developer_id, 'config_dir': '.'}


def _config_dir_path(script_dir, config_dir):
    """Resolve config directory path relative to ai-sessions root."""
    if os.path.isabs(config_dir):
        return config_dir
    # Config directories are siblings of scripts/, not children
    ai_assistant_root = os.path.dirname(script_dir)
    return os.path.join(ai_assistant_root, config_dir)


def load_schema(script_dir, developer_id=None):
    """Load database schema for a developer."""
    # First check for shared schema
    shared_schema = os.path.join(script_dir, 'shared', 'database-schema.jsonc')
    if os.path.exists(shared_schema):
        return _load_jsonc(shared_schema)
    
    # Fall back to developer-specific schema
    if developer_id:
        dev = get_developer_config(script_dir, developer_id)
        config_dir = dev.get('config_dir', '.')
        schema_dir = _config_dir_path(script_dir, config_dir)
        schema_path = os.path.join(schema_dir, 'database-schema.json')
        if not os.path.exists(schema_path):
            schema_path = os.path.join(schema_dir, 'database-schema.jsonc')
    else:
        schema_path = os.path.join(script_dir, 'database-schema.json')
        if not os.path.exists(schema_path):
            schema_path = os.path.join(script_dir, 'database-schema.jsonc')
    
    if not os.path.exists(schema_path):
        return None
    
    return _load_jsonc(schema_path)


def load_paths_to_replace(script_dir, developer_id=None):
    """Load path replacement rules for a developer.
    
    Canonical location: .dev-scripts/readonly-paths-to-replace.jsonc
    Falls back to developer config dir and script dir for backward compatibility.
    """
    patterns = []
    
    # Primary: .dev-scripts/readonly-paths-to-replace.jsonc
    # Search upward from script_dir to find .dev-scripts
    current_dir = os.path.abspath(script_dir)
    dev_scripts_root = None
    while current_dir and current_dir != os.path.dirname(current_dir):
        candidate = os.path.join(current_dir, 'readonly-paths-to-replace.jsonc')
        if os.path.exists(candidate):
            dev_scripts_root = current_dir
            break
        candidate = os.path.join(current_dir, 'paths-to-replace.jsonc')
        if os.path.exists(candidate):
            dev_scripts_root = current_dir
            break
        current_dir = os.path.dirname(current_dir)
    
    if dev_scripts_root:
        primary = os.path.join(dev_scripts_root, 'readonly-paths-to-replace.jsonc')
        if os.path.exists(primary):
            patterns.append(primary)
        else:
            fallback = os.path.join(dev_scripts_root, 'paths-to-replace.jsonc')
            if os.path.exists(fallback):
                patterns.append(fallback)
    
    # Fallback: developer config dir
    if developer_id:
        dev = get_developer_config(script_dir, developer_id)
        config_dir = dev.get('config_dir', '.')
        config_path = _config_dir_path(script_dir, config_dir)
        patterns.extend([
            os.path.join(config_path, 'readonly-paths-to-replace.jsonc'),
            os.path.join(config_path, 'readonly-paths-to-replace.json'),
        ])
    
    # Fallback: script dir
    patterns.extend([
        os.path.join(script_dir, 'readonly-paths-to-replace.jsonc'),
        os.path.join(script_dir, 'readonly-paths-to-replace.json'),
    ])
    
    all_replacements = []
    seen_paths = set()
    for pattern in patterns:
        for jsonc_path in sorted(glob.glob(pattern)):
            normalized_path = os.path.normpath(os.path.abspath(jsonc_path))
            if normalized_path in seen_paths:
                continue
            seen_paths.add(normalized_path)
            data = _load_jsonc(jsonc_path)
            if data is None:
                continue
            
            rules = data.get('rules')
            if rules is not None:
                for rule in rules:
                    paths = rule.get('paths', [])
                    replacement = rule.get('replacement', '_www_')
                    if isinstance(paths, str):
                        paths = [paths]
                    all_replacements.append({
                        'paths': paths,
                        'replacement': replacement,
                        'source': os.path.basename(jsonc_path)
                    })
            else:
                paths = data.get('paths', [])
                replacement = data.get('replacement', '_www_')
                if isinstance(paths, str):
                    paths = [paths]
                all_replacements.append({
                    'paths': paths,
                    'replacement': replacement,
                    'source': os.path.basename(jsonc_path)
                })
    
    return all_replacements


def load_session_ids(script_dir, developer_id=None):
    """Load session IDs for a developer."""
    if developer_id:
        dev = get_developer_config(script_dir, developer_id)
        config_dir = dev.get('config_dir', '.')
        config_path = _config_dir_path(script_dir, config_dir)
        patterns = [
            os.path.join(config_path, 'session-ids.jsonc'),
            os.path.join(config_path, 'session-ids.json'),
            os.path.join(config_path, 'session-ids-*.jsonc'),
            os.path.join(config_path, 'session-ids-*.json'),
        ]
    else:
        patterns = [
            os.path.join(script_dir, 'session-ids.jsonc'),
            os.path.join(script_dir, 'session-ids.json'),
            os.path.join(script_dir, 'session-ids-*.jsonc'),
            os.path.join(script_dir, 'session-ids-*.json'),
        ]
    
    all_ids = []
    for pattern in patterns:
        for jsonc_path in sorted(glob.glob(pattern)):
            data = _load_jsonc(jsonc_path)
            if data is None:
                continue
            ids = data.get('session_ids', [])
            all_ids.extend(ids)
    
    return all_ids


def get_output_dir(script_dir, developer_id, output_name='sessions.db'):
    """Get output directory and filename for a developer."""
    dev = get_developer_config(script_dir, developer_id)
    
    if output_name == 'sessions.db' and dev.get('database'):
        output_name = dev['database']
    
    config_dir = dev.get('config_dir', '.')
    return _config_dir_path(script_dir, config_dir), output_name
