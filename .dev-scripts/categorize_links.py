from pathlib import Path
import re

preps = Path('src-preps')
broken = []

for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    for html_file in commit_dir.rglob('*.html'):
        if html_file.name == 'index.html':
            continue
        
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        for attr in ['SRC', 'HREF']:
            pattern = attr + '="([^"]+)"'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                url = match.group(1)
                if url.startswith('../') or url.startswith('./'):
                    base = html_file.parent
                    target = (base / url).resolve()
                    if not target.exists():
                        broken.append((str(html_file.relative_to(preps)), attr, url))

asset_issues = []
post_issues = []
other_issues = []

for filepath, attr, url in broken:
    if 'assets' in url or 'images' in url:
        asset_issues.append((filepath, attr, url))
    elif url.endswith('.html') or url.endswith('/'):
        post_issues.append((filepath, attr, url))
    else:
        other_issues.append((filepath, attr, url))

print('Asset links to files in other commits: ' + str(len(asset_issues)))
print('Links to other column posts: ' + str(len(post_issues)))
print('Other broken links: ' + str(len(other_issues)))
