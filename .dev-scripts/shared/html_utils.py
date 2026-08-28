#!/usr/bin/env python3
"""
html_utils.py — shared utilities for HTML href transformation and verification.

Provides:
- fix_hrefs(preps_path): batch-fix broken href patterns to match updated folder structure
- check_href_issues(preps_path): detect remaining broken href patterns
- verify_links(html_content, base_path): verify all links in HTML content point to existing files
"""

import os
import re
import sys
from pathlib import Path

# Mapping of old href patterns to new href patterns
HREF_FIXES = {
    b'../links.html': b'../columns/',
    b'../html/links.html': b'../columns/',
    b'../html/info.html': b'../info.html',
}

MONTH_RE = re.compile(
    r'^(january|february|march|april|may|june|july|august|september|october|november|december)[_\-]?(\d{4})\.html$',
    re.IGNORECASE
)


def is_blog_post(fname):
    """Return True if filename matches a blog post pattern like july_2002.html."""
    return MONTH_RE.match(fname) is not None


def transform_link(href, is_columns_page, blog_posts):
    """Transform a single href from original site structure to prep commit structure.
    
    Args:
        href: raw href value from HTML
        is_columns_page: True if current page is under content/columns/
        blog_posts: set of blog post filenames for context
    
    Returns:
        transformed href string
    """
    fragment = ''
    if '#' in href:
        href, fragment = href.split('#', 1)
        fragment = '#' + fragment
    
    if is_columns_page:
        if href in ('../html/links.html', '../html\\links.html'):
            return './' + fragment
        if href.startswith('../html/'):
            fname = href[8:]
            if is_blog_post(fname):
                return fname + fragment
            return '../' + fname + fragment
        if href.startswith('../html\\'):
            fname = href[8:]
            if is_blog_post(fname):
                return fname + fragment
            return '../' + fname + fragment
    else:
        if href in ('./html/links.html', './html\\links.html'):
            return './columns/' + fragment
        if href in ('./html/info.html', './html\\info.html'):
            return './info.html' + fragment
        if href in ('./html/escaping.html', './html\\escaping.html',
                    './html/contact.html', './html\\contact.html'):
            return './' + href.split('/')[-1].split('\\')[-1] + fragment
        if href.startswith('./html/'):
            fname = href[7:]
            if is_blog_post(fname):
                return './columns/' + fname + fragment
            return './' + fname + fragment
        if href.startswith('./html\\'):
            fname = href[7:]
            if is_blog_post(fname):
                return './columns/' + fname + fragment
            return './' + fname + fragment
    return href + fragment


def fix_hrefs(preps_path):
    """Batch-fix broken href patterns in all HTML files under preps_path.
    
    Uses byte-level replacement for robustness with Windows-1252 encoded files.
    Returns (fixed_count, error_count).
    """
    fixed = 0
    errors = 0
    for root, dirs, files in os.walk(str(preps_path)):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = Path(root) / f
            try:
                raw = path.read_bytes()
                original = raw
                for old, new in HREF_FIXES.items():
                    raw = raw.replace(old, new)
                if raw != original:
                    path.write_bytes(raw)
                    fixed += 1
                    print(f'Fixed: {path}')
            except Exception as e:
                print(f'Error processing {path}: {e}', file=sys.stderr)
                errors += 1
    return fixed, errors


def check_href_issues(preps_path):
    """Detect remaining broken href patterns that should have been fixed.
    
    Returns list of (file_path, line_content) tuples for issues found.
    """
    issues = []
    patterns = [
        re.compile(r'HREF="\.\./html/links\.html"'),
        re.compile(r'HREF="\.\./html/info\.html"'),
    ]
    for path in _walk_html(preps_path):
        try:
            text = path.read_text(encoding='cp1252', errors='ignore')
            for line in text.splitlines():
                for pat in patterns:
                    if pat.search(line):
                        issues.append((str(path), line.strip()))
        except Exception:
            pass
    return issues


def verify_links(html_content, base_path):
    """Verify all relative links in HTML content point to existing files.
    
    Args:
        html_content: raw HTML string
        base_path: directory to resolve relative links against
    
    Returns:
        list of issue strings for broken links
    """
    issues = []
    hrefs = re.findall(r'HREF="([^"]+)"', html_content)
    for href in hrefs:
        if href.startswith(('./', '../')):
            target_href = href.split('#')[0]
            if not target_href or target_href.endswith('/'):
                target_href = target_href + 'index.html'
            target = (base_path / target_href).resolve()
            if not target.exists():
                issues.append(f'Broken link: {href} -> {target}')
    return issues


def _walk_html(preps_path):
    """Yield Path objects for every .html file under preps_path."""
    for root, dirs, files in os.walk(str(preps_path)):
        for f in files:
            if f.endswith('.html'):
                yield Path(root) / f
