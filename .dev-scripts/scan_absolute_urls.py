from pathlib import Path
import re

preps = Path('src-preps')
issues = []

for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    for html_file in commit_dir.rglob('*.html'):
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        for attr in ['SRC', 'HREF']:
            pattern = attr + '="([^"]+)"'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                url = match.group(1)
                if url.startswith('/') or url.startswith('http://') or url.startswith('https://'):
                    issues.append((str(html_file.relative_to(preps)), attr, url))

print('Found ' + str(len(issues)) + ' absolute/external URLs')
for filepath, attr, url in issues[:10]:
    print(filepath + ' -> ' + attr + '="' + url + '"')
