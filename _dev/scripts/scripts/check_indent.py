#!/usr/bin/env python3
"""Check indentation patterns in src-content HTML files."""

from pathlib import Path

for p in list(Path("src-content").rglob("*.html"))[:5]:
    text = p.read_text(encoding="utf-8")
    lines = text.split("\n")
    
    tab_lines = sum(1 for line in lines if "\t" in line)
    space2_lines = sum(1 for line in lines if line.startswith("  "))
    space4_lines = sum(1 for line in lines if line.startswith("    "))
    
    print(f"{p.relative_to(Path('src-content'))}: tabs={tab_lines}, spaces2={space2_lines}, spaces4={space4_lines}")
