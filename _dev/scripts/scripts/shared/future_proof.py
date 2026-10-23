#!/usr/bin/env python3
"""
shared/future_proof.py - Shared future-proof text checking utilities.

Provides functions to check text for implementation-specific details
that should not appear in permanent project records.
"""

import re

# Patterns that indicate implementation-specific details
FILE_EXTENSION_PATTERN = re.compile(r'\b[\w-]+\.(py|md|json|js|ts|html|css|db|sql|txt|yml|yaml|toml)\b')
PATH_PATTERN = re.compile(r'(?<!\w)(?:\./|\.\./)?[\w.-]+(?:/[\w./-]+){2,}(?!\w)')


def check_file_extensions(text):
    """Check for file extensions in text."""
    return sorted(set(FILE_EXTENSION_PATTERN.findall(text)))


def check_paths(text):
    """Check for path-like strings in text."""
    return sorted(set(PATH_PATTERN.findall(text)))


def check_future_proof(text, context_id=None):
    """Check if text uses future-proof language.
    
    Args:
        text: Text to check
        context_id: Optional identifier for error messages (e.g., 'T-123')
    
    Returns:
        List of issue strings
    """
    issues = []
    
    extensions = check_file_extensions(text)
    if extensions:
        prefix = f'{context_id}: ' if context_id else ''
        issues.append(f'{prefix}contains file extensions: {extensions}')
    
    paths = check_paths(text)
    if paths:
        prefix = f'{context_id}: ' if context_id else ''
        issues.append(f'{prefix}contains path-like strings: {paths}')
    
    return issues
