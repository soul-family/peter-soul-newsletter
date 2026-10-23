#!/usr/bin/env python3
"""
tests/test_stats_normalization.py - Unit tests for stats normalization.

Tests the _normalize_session function from ai-sessions-stats.py to ensure
old field names are correctly mapped to new user_activity_* names, old
names are removed, and missing fields get sensible defaults.
"""

import importlib.util
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

stats_path = os.path.join(os.path.dirname(__file__), '..', 'ai-sessions-stats.py')
spec = importlib.util.spec_from_file_location('ai-sessions-stats', stats_path)
stats_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stats_module)
_normalize_session = stats_module._normalize_session


class TestNormalizeSession(unittest.TestCase):
    def test_old_input_output_phase_mapping(self):
        session = {
            'id': 'test-session',
            'durations': {
                'user_input_phase_seconds': 100,
                'user_output_phase_seconds': 200,
                'total_seconds': 500,
                'ai_processing_seconds': 300,
            }
        }
        result = _normalize_session(session)
        d = result['durations']
        self.assertEqual(d['user_activity_writing_seconds'], 100)
        self.assertEqual(d['user_activity_review_seconds'], 200)
        self.assertNotIn('user_input_phase_seconds', d)
        self.assertNotIn('user_output_phase_seconds', d)

    def test_old_user_input_fields_mapping(self):
        session = {
            'id': 'test-session',
            'durations': {
                'user_input_seconds': 50,
                'user_input_word_total': 100,
                'user_input_word_distribution': {'1-9': 5, '10-49': 10},
                'user_input_avg_seconds': 25,
                'user_input_writing_seconds': 30,
                'user_input_waiting_seconds': 10,
                'user_input_review_seconds': 5,
                'user_input_verification_seconds': 5,
                'user_input_avg_words': 20,
                'total_seconds': 200,
                'ai_processing_seconds': 150,
            }
        }
        result = _normalize_session(session)
        d = result['durations']
        self.assertEqual(d['user_activity_seconds'], 50)
        self.assertEqual(d['user_activity_word_total'], 100)
        self.assertEqual(d['user_activity_word_distribution'], {'1-9': 5, '10-49': 10})
        self.assertEqual(d['user_activity_avg_seconds'], 25)
        self.assertEqual(d['user_activity_writing_seconds'], 30)
        self.assertEqual(d['user_activity_waiting_seconds'], 10)
        self.assertEqual(d['user_activity_review_seconds'], 5)
        self.assertEqual(d['user_activity_verification_seconds'], 5)
        self.assertEqual(d['user_activity_avg_words'], 20)

    def test_old_writing_review_fields_mapping(self):
        session = {
            'id': 'test-session',
            'durations': {
                'user_writing_seconds': 40,
                'user_waiting_seconds': 20,
                'user_review_seconds': 60,
                'user_verification_seconds': 30,
                'user_word_total': 150,
                'user_word_distribution': {'50-199': 8},
                'total_seconds': 300,
                'ai_processing_seconds': 250,
            }
        }
        result = _normalize_session(session)
        d = result['durations']
        self.assertEqual(d['user_activity_writing_seconds'], 40)
        self.assertEqual(d['user_activity_waiting_seconds'], 20)
        self.assertEqual(d['user_activity_review_seconds'], 60)
        self.assertEqual(d['user_activity_verification_seconds'], 30)
        self.assertEqual(d['user_activity_word_total'], 150)
        self.assertEqual(d['user_activity_word_distribution'], {'50-199': 8})

    def test_old_names_removed_from_durations(self):
        session = {
            'id': 'test-session',
            'durations': {
                'user_input_phase_seconds': 10,
                'user_output_phase_seconds': 20,
                'user_input_seconds': 30,
                'user_writing_seconds': 40,
                'user_waiting_seconds': 50,
                'user_review_seconds': 60,
                'user_verification_seconds': 70,
                'user_word_total': 80,
                'user_word_distribution': {},
                'user_input_word_total': 90,
                'user_input_word_distribution': {},
                'user_input_avg_seconds': 100,
                'user_input_writing_seconds': 110,
                'user_input_waiting_seconds': 120,
                'user_input_review_seconds': 130,
                'user_input_verification_seconds': 140,
                'user_input_avg_words': 150,
                'total_seconds': 500,
                'ai_processing_seconds': 400,
            }
        }
        result = _normalize_session(session)
        d = result['durations']
        for old_key in [
            'user_input_phase_seconds',
            'user_output_phase_seconds',
            'user_input_seconds',
            'user_writing_seconds',
            'user_waiting_seconds',
            'user_review_seconds',
            'user_verification_seconds',
            'user_word_total',
            'user_word_distribution',
            'user_input_word_total',
            'user_input_word_distribution',
            'user_input_avg_seconds',
            'user_input_writing_seconds',
            'user_input_waiting_seconds',
            'user_input_review_seconds',
            'user_input_verification_seconds',
            'user_input_avg_words',
        ]:
            self.assertNotIn(old_key, d, f"Old key {old_key} should be removed from durations")

    def test_missing_fields_get_defaults(self):
        session = {
            'id': 'test-session',
            'durations': {
                'total_seconds': 100,
                'ai_processing_seconds': 80,
            }
        }
        result = _normalize_session(session)
        d = result['durations']
        self.assertEqual(d['user_activity_seconds'], 0)
        self.assertEqual(d['user_activity_writing_seconds'], 0)
        self.assertEqual(d['user_activity_waiting_seconds'], 0)
        self.assertEqual(d['user_activity_review_seconds'], 0)
        self.assertEqual(d['user_activity_verification_seconds'], 0)
        self.assertEqual(d['user_activity_word_total'], 0)
        self.assertEqual(d['user_activity_word_distribution'], {
            '1-9': 0, '10-49': 0, '50-199': 0, '200-499': 0, '500+': 0
        })
        self.assertEqual(d['user_activity_avg_seconds'], 0)
        self.assertEqual(d['user_activity_avg_words'], 0)

    def test_tokens_moved_from_durations_to_top_level(self):
        session = {
            'id': 'test-session',
            'durations': {
                'tokens_input': 1000,
                'tokens_output': 2000,
                'tokens_reasoning': 500,
                'thinking_length': 3000,
                'user_request_count': 10,
                'total_seconds': 400,
                'ai_processing_seconds': 350,
            }
        }
        result = _normalize_session(session)
        self.assertEqual(result['tokens_input'], 1000)
        self.assertEqual(result['tokens_output'], 2000)
        self.assertEqual(result['tokens_reasoning'], 500)
        self.assertEqual(result['thinking_length'], 3000)
        self.assertEqual(result['user_request_count'], 10)
        self.assertNotIn('tokens_input', result['durations'])
        self.assertNotIn('tokens_output', result['durations'])
        self.assertNotIn('tokens_reasoning', result['durations'])
        self.assertNotIn('thinking_length', result['durations'])
        self.assertNotIn('user_request_count', result['durations'])

    def test_top_level_user_request_count_preserved(self):
        session = {
            'id': 'test-session',
            'user_request_count': 5,
            'durations': {
                'total_seconds': 100,
                'ai_processing_seconds': 80,
            }
        }
        result = _normalize_session(session)
        self.assertEqual(result['user_request_count'], 5)

    def test_user_request_count_from_durations_if_missing(self):
        session = {
            'id': 'test-session',
            'durations': {
                'user_request_count': 7,
                'total_seconds': 100,
                'ai_processing_seconds': 80,
            }
        }
        result = _normalize_session(session)
        self.assertEqual(result['user_request_count'], 7)


if __name__ == '__main__':
    unittest.main()
