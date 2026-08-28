#!/usr/bin/env python3
"""
rebuild_preps.py — build src-preps/ with per-commit referenced assets.
- commit0: README.md, LICENSE, .version
- commit1: non-blog pages + first blog post + only referenced assets
- commit2..N: each blog post + only NEW assets not in previous commits
- Preserves author text and encoding; fixes only links/paths for structure.
"""

import shutil
import re
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import BASE, SRC_CONTENT, PREPS
from shared.file_utils import read_enc, write_text
from shared.date_utils import blog_date, format_date_for_csv
from shared.csv_utils import load_date_map

NON_BLOG = [
    'content/columns/index.html','content/info.html','content/letters.html','content/escaping.html',
    'content/contact.html',
]
FIRST_BLOG = 'content/columns/july_2002.html'

def cp(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def src_of(rel):
    if rel == 'content/columns/index.html':
        return SRC_CONTENT/'html'/'links.html'
    if rel.startswith('content/columns/'):
        return SRC_CONTENT/'html'/rel[16:]
    if rel.startswith('content/'):
        return SRC_CONTENT/'html'/rel[8:]
    if rel == 'content/index.html':
        return SRC_CONTENT/'index.html'
    return SRC_CONTENT/rel

def dst_of(c, rel):
    return c/'src-content'/rel.replace('\\','/')

def assets_in(html):
    if not html.exists():
        return set()
    t = read_enc(html)
    return {s for s in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', t, re.I)
            if not s.startswith(('http://','https://','mailto:','#'))}

def norm(a):
    a = a.replace('../','').replace('./','')
    return a if a.startswith('assets/') else ('content/' + a[5:] if a.startswith('html/') else a)

def fix_href(text, kind):
    def sub(m):
        lk = m.group(2)
        if lk.startswith(('http://','https://','mailto:','#','file://')):
            return m.group(0)
        if kind == 'blog':
            if lk.startswith('../html/'): lk = '../' + lk[8:]
            elif lk.startswith('../html\\'): lk = '../' + lk[8:]
        elif kind == 'index':
            if lk.startswith('./html/'): lk = './' + lk[7:]
            elif lk.startswith('./html\\'): lk = './' + lk[7:]
        else:
            if lk.startswith('./html/'): lk = './' + lk[7:]
            elif lk.startswith('./html\\'): lk = './' + lk[7:]
            elif lk.startswith('../html/'): lk = '../' + lk[8:]
            elif lk.startswith('../html\\'): lk = '../' + lk[8:]
        return f'{m.group(1)}="{lk}"'
    return re.sub(r'(href)=["\']([^"\']+)["\']', sub, text, flags=re.I)

def process(src, dst, kind='non-blog'):
    t = read_enc(src)
    t = fix_href(t, kind)
    write_text(dst, t)

def build():
    # clear commits
    for d in PREPS.iterdir():
        if d.is_dir() and d.name.startswith('commit'):
            shutil.rmtree(d)

    # commit0
    c0 = PREPS/'commit0'
    c0.mkdir(parents=True, exist_ok=True)
    if (BASE/'README.md').exists():
        cp(BASE/'README.md', c0/'README.md')
    else:
        write_text(c0/'README.md', '# petersoul.co.uk\n\nOriginal website content published by Peter Soul on petersoul.co.uk\n')
    write_text(c0/'LICENSE', """Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License

Original website content published by Peter Soul on petersoul.co.uk

This is a human-readable summary of the full license at:
https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
""")
    write_text(c0/'.version', '1.0.0\n')
    print('Built commit0')

    # commit1
    c1 = PREPS/'commit1'
    c1.mkdir(parents=True, exist_ok=True)
    seen = set()

    for nb in NON_BLOG:
        s = src_of(nb)
        d = dst_of(c1, nb)
        kind = 'index' if nb == 'content/columns/index.html' else 'non-blog'
        process(s, d, kind)
        for a in assets_in(s):
            seen.add(norm(a))

    blog_src = src_of(FIRST_BLOG)
    blog_dst = dst_of(c1, FIRST_BLOG)
    process(blog_src, blog_dst, 'blog')
    for a in assets_in(blog_src):
        seen.add(norm(a))

    if (SRC_CONTENT/'index.html').exists():
        dst = dst_of(c1, 'content/index.html')
        process(SRC_CONTENT/'index.html', dst, 'index')
        text = dst.read_text(encoding='utf-8')
        text = re.sub(r'<U>Peter Soul<IMG[^>]*a_pscouk\.gif[^>]*></U>', '', text)
        dst.write_text(text, encoding='utf-8')

    for rf in ['.htaccess']:
        s = SRC_CONTENT/rf
        if s.exists():
            cp(s, dst_of(c1, rf))

    for a in sorted(seen):
        s = SRC_CONTENT/a
        if s.exists() and 'a_pscouk.gif' not in a:
            cp(s, dst_of(c1, a))
    print(f'Built commit1 with {len(NON_BLOG)} pages, 1 blog, {len(seen)} assets')

    # commit2..N
    posts = []
    dm = load_date_map(BASE/'.dev-scripts/date_map.csv')
    for r_file, r_date in dm.items():
        if r_file.startswith('content/columns/') and r_file != FIRST_BLOG:
            posts.append((r_file, r_date))
    posts.sort(key=lambda x: x[1])

    n = 2
    for bp, _ in posts:
        c = PREPS/f'commit{n}'
        c.mkdir(parents=True, exist_ok=True)
        s = src_of(bp)
        d = dst_of(c, bp)
        process(s, d, 'blog')
        new = 0
        for a in sorted(assets_in(s)):
            a = norm(a)
            if a in seen:
                continue
            s2 = SRC_CONTENT/a
            if s2.exists():
                cp(s2, dst_of(c, a))
                seen.add(a)
                new += 1
        n += 1

    print(f'Built commit2..{n-1} with {len(posts)} blog posts')
    print('Done')

if __name__ == '__main__':
    build()
