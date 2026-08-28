from pathlib import Path
import re

preps = Path('src-preps')
issues = []

for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    for html_file in commit_dir.rglob('*.html'):
        if html_file.name == 'index.html':
            continue
        
        rel_path = html_file.relative_to(preps)
        parts = rel_path.parts
        
        src_idx = -1
        for i, part in enumerate(parts):
            if part == 'src-content':
                src_idx = i
                break
        
        if src_idx == -1:
            continue
        
        depth = len(parts) - src_idx - 1
        
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        
        # Check for ../index.html from files directly in content/
        if depth == 1 and 'content' in parts:
            if re.search(r'HREF="\.\./index\.html"', text, re.IGNORECASE):
                issues.append((str(rel_path), 'HREF', '../index.html'))
            if re.search(r'SRC="\.\./index\.html"', text, re.IGNORECASE):
                issues.append((str(rel_path), 'SRC', '../index.html'))

print('Found ' + str(len(issues)) + ' potentially wrong ../index.html links from content/ files')
for filepath, attr, url in issues[:10]:
    print(filepath + ' -> ' + attr + '="' + url + '"')
