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
                    # Resolve relative to the HTML file's directory
                    base = html_file.parent
                    target = (base / url).resolve()
                    
                    # Check if target exists
                    if not target.exists():
                        broken.append((str(html_file.relative_to(preps)), attr, url))

print('Found ' + str(len(broken)) + ' broken relative URLs')
for filepath, attr, url in broken[:30]:
    print(filepath + ' -> ' + attr + '="' + url + '"')
