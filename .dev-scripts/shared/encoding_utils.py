#!/usr/bin/env python3
"""
encoding_utils.py — shared utilities for HTML encoding detection, verification, and repair.

Provides:
- check_encoding_mismatch(preps_path): detect files declaring ISO-8859-1 but containing UTF-8 multibyte sequences
- check_charsets(preps_path): count charset declarations across HTML files
- restore_windows1252(preps_path): convert UTF-8-decoded text back to Windows-1252 bytes
- restore_charset_declarations(preps_path, expected_charset): restore original charset meta tags
- verify_encoding(preps_path, expected_charset): verify bytes match expected single-byte encoding
"""

import os
import re
import sys
from pathlib import Path

# UTF-8 multibyte sequences for smart quotes and dashes that indicate mismatch
UTF8_MARKERS = [
    b'\xe2\x80\x99',  # right single quotation mark (’)
    b'\xe2\x80\x98',  # left single quotation mark (‘)
    b'\xe2\x80\x9c',  # left double quotation mark (“)
    b'\xe2\x80\x9d',  # right double quotation mark (”)
    b'\xe2\x80\x93',  # en dash (–)
    b'\xe2\x80\x94',  # em dash (—)
    b'\xe2\x80\xa6',  # horizontal ellipsis (…)
]

# Windows-1252 single-byte markers
WIN1252_MARKERS = {
    0x91: 'left single quotation mark',
    0x92: 'right single quotation mark',
    0x93: 'left double quotation mark',
    0x94: 'right double quotation mark',
    0x96: 'en dash',
    0x97: 'em dash',
    0x85: 'ellipsis',
}


def _walk_html(preps_path):
    """Yield Path objects for every .html file under preps_path."""
    for root, dirs, files in os.walk(str(preps_path)):
        for f in files:
            if f.endswith('.html'):
                yield Path(root) / f


def check_encoding_mismatch(preps_path):
    """Return list of HTML files that declare ISO-8859-1/Windows-1252 but contain UTF-8 multibyte sequences."""
    issues = []
    for path in _walk_html(preps_path):
        try:
            raw = path.read_bytes()
            content = path.read_text(encoding='utf-8', errors='replace')
            if 'charset=ISO-8859-1' in content or 'charset=windows-1252' in content or \
               'charset="ISO-8859-1"' in content or 'charset="windows-1252"' in content:
                for marker in UTF8_MARKERS:
                    if marker in raw:
                        issues.append(str(path))
                        break
        except Exception:
            pass
    return issues


def check_charsets(preps_path):
    """Return dict mapping charset declaration -> count across all HTML files."""
    charsets = {}
    for path in _walk_html(preps_path):
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            m = re.search(r'charset=([^"\'>\s]+)', content, re.IGNORECASE)
            if m:
                cs = m.group(1)
                charsets[cs] = charsets.get(cs, 0) + 1
        except Exception:
            pass
    return charsets


def restore_windows1252(preps_path):
    """Convert HTML files that were mistakenly saved as UTF-8 back to Windows-1252 bytes.
    
    Uses a robust decoder: try UTF-8 first, fall back to cp1252 on decode errors.
    Replaces Unicode replacement characters (U+FFFD) with ASCII apostrophe.
    Returns (fixed_count, error_count).
    """
    fixed = 0
    errors = 0
    for path in _walk_html(preps_path):
        try:
            raw = path.read_bytes()
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                text = raw.decode('cp1252')
            text = text.replace('\ufffd', "'")
            path.write_bytes(text.encode('cp1252'))
            fixed += 1
        except Exception as e:
            print(f'Error processing {path}: {e}', file=sys.stderr)
            errors += 1
    return fixed, errors


def restore_charset_declarations(preps_path, expected_charset='ISO-8859-1'):
    """Restore original charset declarations that may have been changed to UTF-8.
    
    Replaces 'charset=UTF-8' or 'charset="UTF-8"' with expected_charset in all HTML files.
    Returns count of files modified.
    """
    count = 0
    for path in _walk_html(preps_path):
        try:
            text = path.read_text(encoding='cp1252', errors='ignore')
            if 'charset=UTF-8' in text:
                text = text.replace('charset=UTF-8', f'charset={expected_charset}')
                path.write_text(text, encoding='cp1252')
                count += 1
            elif 'charset="UTF-8"' in text:
                text = text.replace('charset="UTF-8"', f'charset={expected_charset}')
                path.write_text(text, encoding='cp1252')
                count += 1
        except Exception as e:
            print(f'Error processing {path}: {e}', file=sys.stderr)
    return count


def verify_encoding(preps_path, expected_charset='ISO-8859-1'):
    """Verify that HTML files contain valid Windows-1252 bytes and correct charset declaration.
    
    Returns dict with:
      - 'valid_windows1252': list of files with valid cp1252 bytes
      - 'invalid_encoding': list of files that can't be read as cp1252
      - 'charset_mismatch': list of files whose declared charset != expected
      - 'smart_quotes_present': list of files containing smart quote characters
    """
    results = {
        'valid_windows1252': [],
        'invalid_encoding': [],
        'charset_mismatch': [],
        'smart_quotes_present': [],
    }
    
    for path in _walk_html(preps_path):
        try:
            raw = path.read_bytes()
            try:
                text = raw.decode('cp1252')
                results['valid_windows1252'].append(str(path))
            except UnicodeDecodeError:
                results['invalid_encoding'].append(str(path))
                continue
            
            m = re.search(r'charset=([^"\'>\s]+)', text, re.IGNORECASE)
            if m and m.group(1).lower() != expected_charset.lower():
                results['charset_mismatch'].append(
                    f'{path}: declared {m.group(1)}, expected {expected_charset}'
                )
            
            if '\u2019' in text or '\u201c' in text:
                results['smart_quotes_present'].append(str(path))
                
        except Exception as e:
            results['invalid_encoding'].append(f'{path}: {e}')
    
    return results
