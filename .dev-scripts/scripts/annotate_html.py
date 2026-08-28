#!/usr/bin/env python3
"""
annotate_html.py — append <!-- Latest Updated on: YYYY-MM-DD --> to every HTML file
in each commit folder, using the commit folder's blog post date.
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import BASE, PREPS, DATE_MAP
from shared.date_utils import format_date_for_tag
from shared.csv_utils import load_date_map

def annotate(path, date):
    t = path.read_text(encoding='utf-8', errors='ignore')
    tag = f'\n<!-- Latest Updated on: {date} -->\n'
    if 'Latest Updated on:' in t:
        t = re.sub(r'\n<!-- Latest Updated on: \d{4}-\d{2}-\d{2} -->\n?', tag, t)
    else:
        low = t.lower()
        if '</html>' in low:
            t = t.replace('</html>', tag + '</html>', 1)
        elif '</body>' in low:
            t = t.replace('</body>', tag + '</body>', 1)
        else:
            t += tag
    path.write_text(t, encoding='utf-8')

def get_commit_blog_date(commit_dir, dm):
    blog_files = list((commit_dir/'src-content').rglob('content/columns/*.html'))
    if not blog_files:
        return None
    for bf in blog_files:
        rel = bf.relative_to(commit_dir/'src-content').as_posix()
        if rel in dm:
            return format_date_for_tag(dm[rel])
    return None

def main():
    dm = load_date_map(DATE_MAP)
    for cd in sorted(PREPS.iterdir()):
        if not cd.is_dir() or not cd.name.startswith('commit'):
            continue
        blog_date = get_commit_blog_date(cd, dm)
        if not blog_date:
            print(f'{cd.name}: no blog post found, skipping')
            continue
        base = cd/'src-content'
        html_files = list(base.rglob('content/*.html')) + list(base.rglob('content/columns/*.html'))
        for hf in html_files:
            annotate(hf, blog_date)
            print(f'Annotated {cd.name}/{hf.relative_to(cd).as_posix()} with {blog_date}')

if __name__ == '__main__':
    main()
