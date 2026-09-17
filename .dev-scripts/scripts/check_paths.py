#!/usr/bin/env python3
"""Check current relative paths in markdown files."""

from pathlib import Path
import re

DOCS = Path("docs")

for p in sorted(DOCS.rglob("*.md")):
    text = p.read_text(encoding="utf-8")
    # Find all markdown links with ../
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    for text_content, url in links:
        if '..' in url:
            print(f"{p.relative_to(DOCS)}: [{text_content}]({url})")
