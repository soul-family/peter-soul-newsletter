#!/usr/bin/env python3
"""Fix overly long relative paths in markdown files."""

from pathlib import Path
import re

DOCS = Path("docs")

fixed = []

for p in sorted(DOCS.rglob("*.md")):
    text = p.read_text(encoding="utf-8")
    new_text = text
    
    rel_path = p.relative_to(DOCS).as_posix()
    rel_parts = p.relative_to(DOCS).parts
    
    # Fix paths like ../../../content/columns/2013/xxx.md
    # These appear in files under docs/content/columns/YYYY/
    if "content/columns" in rel_path:
        # Replace ../../../content/columns/YYYY/ with ../
        new_text = re.sub(
            r'\.\./\.\./\.\./content/columns/(\d{4})/',
            r'../\1/',
            new_text
        )
        # Replace ../../../content/ with ../
        new_text = re.sub(
            r'\.\./\.\./\.\./content/',
            r'../',
            new_text
        )
        # Replace ../../../assets/ with ../../assets/
        new_text = re.sub(
            r'\.\./\.\./\.\./assets/',
            r'../../assets/',
            new_text
        )
    
    # Fix paths in root content files (docs/content/*.md)
    if len(rel_parts) == 2 and rel_parts[0] == "content":
        # ../content/escaping.md -> escaping.md
        new_text = re.sub(
            r'\.\./content/(escaping\.md|info\.md)',
            r'\1',
            new_text
        )
        # ../content/columns/ -> columns/
        new_text = re.sub(
            r'\.\./content/columns/',
            r'columns/',
            new_text
        )
    
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
        fixed.append(str(p.relative_to(DOCS)))

print(f"Fixed paths in {len(fixed)} files")
for f in fixed[:10]:
    print(f"  - {f}")
if len(fixed) > 10:
    print(f"  ... and {len(fixed) - 10} more")
