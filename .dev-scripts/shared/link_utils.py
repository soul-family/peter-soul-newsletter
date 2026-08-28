#!/usr/bin/env python3
"""
link_utils.py — shared utilities for HTML link transformation and verification.

Provides:
- is_blog_post(fname): detect blog post filenames
- transform_link(href, is_columns_page, blog_posts): transform original site links to prep commit links
- verify_links(html_content, base_path): verify all links in HTML content point to existing files
"""

import re
from pathlib import Path

MONTH_RE = re.compile(r'^(january|february|march|april|may|june|july|august|september|october|november|december)[_\-]?(\d{4})\.html$', re.IGNORECASE)

BLOG_ALIKE = {
    'escaping.html', 'contact.html', 'info.html', 'links.html', 'letters.html',
    'familytree.html', 'lettersfamilytree.html',
    'baileyfamilytree.html', 'clark_unwinfamilytrees.html', 'cockinfamilytree.html',
    'colesfamilytree.html', 'fletcherfamilytree.html', 'gilesfamilytree.html',
    'handleyfamilytree.html', 'hankinfamilytree.html', 'holtfamilytree.html',
    'honefamilytree.html', 'jacobsohn_cohenfamilytrees.html', 'robertsfamilytree.html',
    'simmondsfamilytree.html', 'smithfamilytree.html', 'soulfamilytree.html',
    'wilsonfamilytree.html',
}

def is_blog_post(fname):
    m = MONTH_RE.match(fname)
    return m is not None

def transform_link(href, is_columns_page, blog_posts):
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

def verify_links(html_content, base_path):
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
