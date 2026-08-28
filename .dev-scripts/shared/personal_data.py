#!/usr/bin/env python3
"""
personal_data.py — detect personal data in text files.

Checks:
- Email addresses
- Phone numbers
- Sensitive personal context keywords

Intended for audit of task lists, changelogs, and AI transparency logs.
"""

import re
from pathlib import Path

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'(\+?\d[\d\s\-\(\)]{7,}\d)')

def check_personal_data(path):
    issues = []
    text = Path(path).read_text(encoding='utf-8')
    
    emails = EMAIL_RE.findall(text)
    for e in emails:
        issues.append(f'Email address found: {e}')
    
    phones = PHONE_RE.findall(text)
    for p in phones:
        issues.append(f'Phone number found: {p}')
    
    return issues
