from pathlib import Path
import re
import json
from datetime import datetime

index_html = Path('src-preps/commit167/src-content/content/columns/index.html')
text = index_html.read_text(encoding='utf-8', errors='ignore')

href_pattern = re.compile(r'HREF="([^"]+\.html)"', re.IGNORECASE)
title_pattern = re.compile(r'\(([^)]+)\)')

href_matches = list(href_pattern.finditer(text))
titles_by_filename = {}

for match in href_matches:
    href = match.group(1)
    fname = href.replace('.html', '')
    start = match.end()
    search_text = text[start:start+300]
    title_match = title_pattern.search(search_text)
    if title_match:
        title = title_match.group(1)
        titles_by_filename[fname] = title

print('Found ' + str(len(titles_by_filename)) + ' titles')

rows = []

root_columns = Path('src-content/content/columns')
if root_columns.exists():
    for html_file in sorted(root_columns.iterdir()):
        if html_file.suffix.lower() != '.html':
            continue
        if html_file.name == 'index.html':
            continue
        fname = html_file.stem
        date_obj = None
        short_date = ''
        date_str = ''
        m = re.match(r'^(january|february|march|april|may|june|july|august|september|october|november|december)_?(\d{4})$', fname, re.IGNORECASE)
        if m:
            month_name = m.group(1).lower()
            year = int(m.group(2))
            try:
                date_obj = datetime.strptime(month_name + ' ' + str(year), '%B %Y')
                short_date = date_obj.strftime('%Y-%m')
                date_str = date_obj.strftime('%B %Y')
            except ValueError:
                pass
        if date_obj:
            title = titles_by_filename.get(fname, '')
            rows.append((date_obj, short_date, fname, date_str, title))

preps = Path('src-preps')
for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    columns_dir = commit_dir / 'src-content' / 'content' / 'columns'
    if not columns_dir.exists():
        continue
    for html_file in sorted(columns_dir.iterdir()):
        if html_file.suffix.lower() != '.html':
            continue
        if html_file.name == 'index.html':
            continue
        fname = html_file.stem
        date_obj = None
        short_date = ''
        date_str = ''
        m = re.match(r'^(january|february|march|april|may|june|july|august|september|october|november|december)_?(\d{4})$', fname, re.IGNORECASE)
        if m:
            month_name = m.group(1).lower()
            year = int(m.group(2))
            try:
                date_obj = datetime.strptime(month_name + ' ' + str(year), '%B %Y')
                short_date = date_obj.strftime('%Y-%m')
                date_str = date_obj.strftime('%B %Y')
            except ValueError:
                pass
        if date_obj:
            title = titles_by_filename.get(fname, '')
            rows.append((date_obj, short_date, fname, date_str, title))

seen = set()
unique_rows = []
for row in rows:
    if row[2] not in seen:
        seen.add(row[2])
        unique_rows.append(row)

unique_rows.sort(key=lambda x: x[0])

lines = ['# Columns Index', '', '| Short date | Date as written | Post title |', '|------------|-----------------|------------|']
for _, short_date, fname, date_str, title in unique_rows:
    lines.append('| ' + short_date + ' | ' + date_str + ' | ' + title + ' |')

md_path = Path('src-preps/_data/columns-index.md')
md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Wrote ' + str(len(unique_rows)) + ' rows to ' + str(md_path))

entries = []
for _, short_date, fname, date_str, title in unique_rows:
    entries.append({
        'short_date': short_date,
        'date_as_written': date_str,
        'post_title': title
    })

json_path = Path('src-preps/_data/columns-index.json')
json_path.write_text(json.dumps(entries, indent=2), encoding='utf-8')
print('Wrote ' + str(len(entries)) + ' entries to ' + str(json_path))
