#!/usr/bin/env python3
"""
aggregate_all_stats.py - Unified stats aggregator across all developer databases.

Combines statistics from all developer session databases into a single
project-wide report.

Usage:
  python aggregate_all_stats.py --base-dir .ai-activity/ai-sessions
  python aggregate_all_stats.py --output .ai-activity/ai-reports/project-stats-totals.json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ai-sessions', 'shared'))
from config_loader import get_developer_ids, get_developer_config
from session_utils import humanize


def load_stats_for_developer(base_dir, developer_id):
    """Load stats file for a developer if it exists."""
    dev_config = get_developer_config('.dev-scripts/ai-sessions', developer_id)
    config_dir = dev_config.get('config_dir', developer_id)
    stats_name = dev_config.get('stats_file', f'{developer_id}-sessions.stats.json')
    
    stats_path = os.path.join(base_dir, config_dir, stats_name)
    if not os.path.exists(stats_path):
        return None
    
    with open(stats_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def aggregate_all_stats(base_dir, output_path=None):
    """Aggregate stats from all developers."""
    developers = get_developer_ids('.dev-scripts/ai-sessions')
    
    all_sessions = []
    databases = []
    generated_at = None
    
    for dev_id in developers:
        stats = load_stats_for_developer(base_dir, dev_id)
        if stats is None:
            continue
        
        if generated_at is None:
            generated_at = stats.get('generated_at')
        
        for session in stats.get('sessions', []):
            session['_database'] = dev_id
            all_sessions.append(session)
        
        db_name = stats.get('database', f'{dev_id}-sessions.db')
        databases.append(db_name)
    
    if not all_sessions:
        print("No stats found for any developer.")
        return None
    
    # Calculate totals
    sessions = len(all_sessions)
    messages = sum(s['message_count'] for s in all_sessions)
    parts = sum(s['part_count'] for s in all_sessions)
    thinking = sum(s['thinking_length'] for s in all_sessions)
    user_requests = sum(s['user_request_count'] for s in all_sessions)
    tokens_input = sum(s['tokens_input'] for s in all_sessions)
    tokens_output = sum(s['tokens_output'] for s in all_sessions)
    tokens_reasoning = sum(s['tokens_reasoning'] for s in all_sessions)
    total_active = sum(s['durations']['total_seconds'] for s in all_sessions)
    total_ai = sum(s['durations']['ai_processing_seconds'] for s in all_sessions)
    total_user = sum(s['durations']['user_activity_seconds'] for s in all_sessions)
    total_user_words = sum(s['durations']['user_activity_word_total'] for s in all_sessions)
    total_writing = sum(s['durations']['user_activity_writing_seconds'] for s in all_sessions)
    total_waiting = sum(s['durations']['user_activity_waiting_seconds'] for s in all_sessions)
    total_review = sum(s['durations']['user_activity_review_seconds'] for s in all_sessions)
    total_verification = sum(s['durations']['user_activity_verification_seconds'] for s in all_sessions)
    
    combined = {
        'generated_at': generated_at,
        'databases': databases,
        'totals': {
            'sessions': sessions,
            'messages': messages,
            'parts': parts,
            'thinking_length_chars': thinking,
            'user_requests': user_requests,
            'tokens_input': tokens_input,
            'tokens_output': tokens_output,
            'tokens_reasoning': tokens_reasoning,
            'total_duration_seconds': total_active,
            'total_duration_human': humanize(total_active),
            'total_ai_processing_seconds': total_ai,
            'total_ai_processing_human': humanize(total_ai),
            'total_user_activity_seconds': total_user,
            'total_user_activity_human': humanize(total_user),
            'total_user_activity_words': total_user_words,
            'total_user_activity_writing_seconds': total_writing,
            'total_user_activity_writing_human': humanize(total_writing),
            'total_user_activity_waiting_seconds': total_waiting,
            'total_user_activity_waiting_human': humanize(total_waiting),
            'total_user_activity_review_seconds': total_review,
            'total_user_activity_review_human': humanize(total_review),
            'total_user_activity_verification_seconds': total_verification,
            'total_user_activity_verification_human': humanize(total_verification),
            'user_activity_tier_distribution': {},
            'avg_words_per_request': total_user_words // max(1, user_requests)
        },
        'sessions_breakdown': all_sessions
    }
    
    # Combine tier distributions
    for s in all_sessions:
        for tier, count in s['durations']['user_activity_word_distribution'].items():
            combined['totals']['user_activity_tier_distribution'][tier] = \
                combined['totals']['user_activity_tier_distribution'].get(tier, 0) + count
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(combined, f, indent=2, ensure_ascii=False)
        print(f"Combined stats written to {output_path}")
    
    return combined


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate stats from all developer databases.'
    )
    parser.add_argument('--base-dir', default='.ai-activity/ai-sessions',
                        help='Base directory for session databases')
    parser.add_argument('--output', default='.ai-activity/ai-reports/project-stats-totals.json',
                        help='Output file path')
    
    args = parser.parse_args()
    
    result = aggregate_all_stats(args.base_dir, args.output)
    
    if result:
        t = result['totals']
        print(f"Sessions: {t['sessions']}")
        print(f"Messages: {t['messages']}")
        print(f"Parts: {t['parts']}")
        print(f"Total duration: {t['total_duration_human']}")
        print(f"AI processing: {t['total_ai_processing_human']}")
        print(f"User activity: {t['total_user_activity_human']}")


if __name__ == '__main__':
    main()
