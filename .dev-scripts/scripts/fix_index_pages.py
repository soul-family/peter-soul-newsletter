#!/usr/bin/env python3
"""
fix_index_pages.py — generate per-commit index pages with progressive column listings.

For each column commit (except commit0-familytree):
- content/columns/index.html: shows only columns up to this commit's date
- content/index.html: shows only columns up to this commit's date
- All relative paths fixed for commit structure
- Source files read as cp1252 (Windows-1252) to preserve original encoding

Also handles commit0-familytree:
- letters.html → letters/index.html conversion
"""

import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.paths import PREPS, BASE
from shared.csv_utils import load_date_map
from shared.date_utils import parse_dt
from shared.link_utils import transform_link, verify_links, is_blog_post

SRC_INDEX = BASE / 'src-prep-last' / 'index.html'
SRC_LINKS = BASE / 'src-prep-last' / 'html' / 'links.html'

MONTH_RE = re.compile(r'^(january|february|march|april|may|june|july|august|september|october|november|december)[_\-]?(\d{4})\.html$', re.IGNORECASE)
MONTHS = {m: i for i, m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'], 1)}

def parse_blog_date(fname):
    m = MONTH_RE.match(fname)
    if not m:
        return None
    return datetime(int(m.group(2)), MONTHS[m.group(1).lower()], 1, 13, 0, 0)

def get_commit_dates():
    dm = load_date_map(BASE / '.dev-scripts' / 'date_map.csv')
    commits = {}
    for rel, dt in dm.items():
        parts = rel.split('/')
        if len(parts) >= 2 and parts[0].startswith('commit') and parts[1] == 'src-content':
            rel = '/'.join(parts[2:])
        if rel.startswith('content/columns/'):
            fname = rel.split('/')[-1]
            commits[fname] = dt
    return commits

def extract_fname(href):
    m = re.search(r'/([^/"#]+)\.html', href)
    if m:
        return m.group(1) + '.html'
    return None

def process_page(source_text, commit_date, is_columns_page):
    lines = source_text.split('\n')
    output = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if '<TD WIDTH=599  BGCOLOR="#CCCCCC">' in line or '<TD WIDTH=599 BGCOLOR="#CCCCCC">' in line or \
           '<TD WIDTH=599  BGCOLOR="#CCFFFF">' in line or '<TD WIDTH=599 BGCOLOR="#CCFFFF">' in line:
            output.append(line)
            i += 1
            content_lines = []
            
            while i < len(lines):
                if '</TD>' in lines[i]:
                    if i + 1 < len(lines) and '</TR>' in lines[i + 1]:
                        filtered = filter_content_block(content_lines, commit_date, is_columns_page)
                        output.extend(filtered)
                        output.append(lines[i])
                        output.append(lines[i + 1])
                        i += 2
                        break
                content_lines.append(lines[i])
                i += 1
            continue
        
        output.append(line)
        i += 1
    
    result = '\n'.join(output)
    result = fix_navigation_links(result, is_columns_page)
    return result

def fix_navigation_links(text, is_columns_page):
    lines = text.split('\n')
    output = []
    
    for line in lines:
        hrefs = re.findall(r'HREF="([^"]*)"', line)
        if not hrefs:
            output.append(line)
            continue
        
        new_line = line
        for href in hrefs:
            new_href = transform_link(href, is_columns_page, set())
            if new_href != href:
                new_line = new_line.replace(f'HREF="{href}"', f'HREF="{new_href}"')
        output.append(new_line)
    
    return '\n'.join(output)

def filter_content_block(lines, commit_date, is_columns_page):
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        year_match = re.search(r'<A NAME="(\d{4})"></A>', line)
        if year_match:
            year = int(year_match.group(1))
            year_header = line
            posts = []
            i += 1
            
            while i < len(lines):
                if re.search(r'<A NAME="\d{4}"></A>', lines[i]):
                    break
                if 'HREF=' in lines[i] and '</P>' in lines[i]:
                    hrefs = re.findall(r'HREF="([^"]*)"', lines[i])
                    fname = None
                    for href in hrefs:
                        fname = extract_fname(href)
                        if fname:
                            break
                    if fname:
                        dt = parse_blog_date(fname)
                        if dt and dt <= commit_date:
                            posts.append((dt, lines[i]))
                    i += 1
                else:
                    i += 1
            
            if posts:
                result.append(year_header)
                posts.sort(key=lambda x: x[0])
                for _, post_line in posts:
                    new_line = post_line
                    for href in re.findall(r'HREF="([^"]*)"', post_line):
                        fname = extract_fname(href)
                        if fname:
                            if is_columns_page:
                                new_href = fname
                            else:
                                new_href = './columns/' + fname
                            new_line = new_line.replace(f'HREF="{href}"', f'HREF="{new_href}"')
                    result.append(new_line)
            continue
        
        if 'HREF=' in line:
            hrefs = re.findall(r'HREF="([^"]*)"', line)
            for href in hrefs:
                fname = extract_fname(href)
                if fname:
                    dt = parse_blog_date(fname)
                    if dt and dt <= commit_date:
                        new_line = line
                        if is_columns_page:
                            new_href = fname
                        else:
                            new_href = './columns/' + fname
                        new_line = new_line.replace(f'HREF="{href}"', f'HREF="{new_href}"')
                        result.append(new_line)
                        i += 1
                        break
                    elif dt and dt > commit_date:
                        i += 1
                        break
                    else:
                        new_href = transform_link(href, is_columns_page, set())
                        new_line = line.replace(f'HREF="{href}"', f'HREF="{new_href}"')
                        result.append(new_line)
                        i += 1
                        break
                else:
                    new_href = transform_link(href, is_columns_page, set())
                    new_line = line.replace(f'HREF="{href}"', f'HREF="{new_href}"')
                    result.append(new_line)
                    i += 1
                    break
            else:
                i += 1
                continue
            continue
        
        result.append(line)
        i += 1
    
    return result

def convert_letters_to_dir():
    ftree = PREPS / 'commit0-familytree' / 'src-content'
    letters_file = ftree / 'letters.html'
    letters_dir = ftree / 'letters'
    letters_index = letters_dir / 'index.html'
    
    if letters_file.exists() and not letters_dir.exists():
        letters_dir.mkdir(parents=True, exist_ok=True)
        content = letters_file.read_text(encoding='cp1252')
        content = content.replace('HREF="../familytree.html"', 'HREF="../familytree.html"')
        letters_index.write_text(content, encoding='cp1252')
        letters_file.unlink()
        print(f'commit0-familytree: converted letters.html to letters/index.html')
    elif letters_dir.exists():
        print(f'commit0-familytree: letters/ already exists')
    else:
        print(f'commit0-familytree: no letters.html found')

def verify_commit_links(cdir):
    links_dst = cdir / 'src-content' / 'content' / 'columns' / 'index.html'
    index_dst = cdir / 'src-content' / 'content' / 'index.html'
    
    for dst in [links_dst, index_dst]:
        if dst.exists():
            content = dst.read_text(encoding='cp1252')
            issues = verify_links(content, dst.parent)
            if issues:
                print(f'{cdir.name}: LINK ISSUES in {dst.name}:')
                for issue in issues:
                    print(f'  {issue}')
                return False
    return True

def main():
    dm = get_commit_dates()
    
    links_text = SRC_LINKS.read_text(encoding='cp1252')
    index_text = SRC_INDEX.read_text(encoding='cp1252')
    
    commits = sorted([d for d in PREPS.iterdir() if d.is_dir() and d.name.startswith('commit')])
    
    for cdir in commits:
        name = cdir.name
        if name == 'commit0':
            continue
        
        if name == 'commit0-familytree':
            convert_letters_to_dir()
            continue
        
        blog_files = list(cdir.rglob('*.html'))
        blog_dates = []
        for bf in blog_files:
            fname = bf.name
            if fname in dm:
                blog_dates.append(dm[fname])
        
        if not blog_dates:
            print(f'{name}: no blog post found, skipping')
            continue
        
        commit_date = min(blog_dates)
        
        links_dst = cdir / 'src-content' / 'content' / 'columns' / 'index.html'
        index_dst = cdir / 'src-content' / 'content' / 'index.html'
        
        links_dst.parent.mkdir(parents=True, exist_ok=True)
        index_dst.parent.mkdir(parents=True, exist_ok=True)
        
        links_result = process_page(links_text, commit_date, is_columns_page=True)
        links_dst.write_text(links_result, encoding='cp1252')
        print(f'{name}: updated columns/index.html ({commit_date.date()})')
        
        index_result = process_page(index_text, commit_date, is_columns_page=False)
        index_dst.write_text(index_result, encoding='cp1252')
        print(f'{name}: updated index.html ({commit_date.date()})')
        
        if not verify_commit_links(cdir):
            print(f'{name}: link verification failed')

if __name__ == '__main__':
    main()
