from pathlib import Path
import re

preps = Path('src-preps')
fixes = 0

for commit_dir in sorted(preps.iterdir()):
    if not commit_dir.is_dir():
        continue
    for html_file in commit_dir.rglob('*.html'):
        if html_file.name == 'index.html':
            continue
        
        rel_path = html_file.relative_to(preps)
        parts = rel_path.parts
        
        # Find src-content index
        src_idx = -1
        for i, part in enumerate(parts):
            if part == 'src-content':
                src_idx = i
                break
        
        if src_idx == -1:
            continue
        
        # Depth within src-content (0 = directly in src-content, 1 = in a subfolder, etc.)
        depth = len(parts) - src_idx - 1
        
        # Check if file is in content/columns/
        in_columns = 'content' in parts and 'columns' in parts
        
        text = html_file.read_text(encoding='utf-8', errors='ignore')
        original_text = text
        
        # Fix SRC paths
        if in_columns:
            # In content/columns/, assets should be ../../assets/
            text = re.sub(r'SRC="\.\./assets/', 'SRC="../../assets/', text, flags=re.IGNORECASE)
        
        # Fix HREF paths for assets (if any)
        if in_columns:
            text = re.sub(r'HREF="\.\./assets/', 'HREF="../../assets/', text, flags=re.IGNORECASE)
        
        if text != original_text:
            html_file.write_text(text, encoding='utf-8')
            fixes += 1
            print('Fixed: ' + str(rel_path))

print('Fixed ' + str(fixes) + ' files')
