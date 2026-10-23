from pathlib import Path
import re

for p in Path('docs').rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    lines = text.split('\n')
    in_fm = False
    fm_ended = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                fm_ended = True
                continue
        if fm_ended and re.match(r'^#+\s', line):
            print(f'{p.relative_to(Path("docs"))}:{i+1} - {line}')
            break
