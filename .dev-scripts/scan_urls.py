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
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        
        # Find all SRC and HREF attributes
        for attr in ['SRC', 'HREF']:
            pattern = attr + '="([^"]+)"'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                url = match.group(1)
                # Check for paths that might be problematic
                if url.startswith('../') or url.startswith('./') or url.startswith('/'):
                    issues.append((str(html_file.relative_to(preps)), attr, url))

print('Found ' + str(len(issues)) + ' relative URLs')
print()
print('Sample issues:')
for filepath, attr, url in issues[:20]:
    print(filepath + ' -> ' + attr + '="' + url + '"')
