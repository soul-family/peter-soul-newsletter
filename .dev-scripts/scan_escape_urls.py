from pathlib import Path
import re

preps = Path('src-preps')
issues = []

for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    for html_file in commit_dir.rglob('*.html'):
        rel_path = html_file.relative_to(preps)
        # Skip index.html files
        if html_file.name == 'index.html':
            continue
        
        # Count depth in src-content tree
        parts = rel_path.parts
        src_content_index = -1
        for i, part in enumerate(parts):
            if part == 'src-content':
                src_content_index = i
                break
        
        if src_content_index == -1:
            continue
        
        depth = len(parts) - src_content_index - 1  # depth within src-content
        
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        for attr in ['SRC', 'HREF']:
            pattern = attr + '="([^"]+)"'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                url = match.group(1)
                if url.startswith('../'):
                    # Count ../ segments
                    segments = url.split('/')
                    up_count = 0
                    for seg in segments:
                        if seg == '..':
                            up_count += 1
                    
                    # If going up more than depth, it escapes src-content
                    if up_count > depth:
                        issues.append((str(rel_path), attr, url, up_count, depth))

print('Found ' + str(len(issues)) + ' URLs that escape src-content tree')
for filepath, attr, url, up_count, depth in issues[:20]:
    print(filepath + ' -> ' + attr + '="' + url + '" (up=' + str(up_count) + ', depth=' + str(depth) + ')')
