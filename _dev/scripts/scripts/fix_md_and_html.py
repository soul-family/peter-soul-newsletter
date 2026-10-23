#!/usr/bin/env python3
"""
1. Remove markdown title headings from docs/ md files
2. Fix all local paths to be relative
3. Beautify src-content HTML files
"""

import re
from pathlib import Path

DOCS = Path("docs")
SRC = Path("src-content")


def remove_title_headings():
    """Remove the first markdown heading after front matter in all md files."""
    removed = []
    for p in sorted(DOCS.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        
        in_fm = False
        fm_ended = False
        new_lines = []
        heading_removed = False
        
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_fm:
                    in_fm = True
                else:
                    fm_ended = True
                new_lines.append(line)
                continue
            
            if fm_ended and not heading_removed and re.match(r"^#+\s", line):
                # Skip this heading line
                heading_removed = True
                removed.append(str(p.relative_to(DOCS)))
                continue
            
            new_lines.append(line)
        
        new_text = "\n".join(new_lines)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
    
    print(f"Removed title headings from {len(removed)} files")
    for f in removed:
        print(f"  - {f}")


def fix_absolute_paths():
    """Convert absolute paths to relative paths in markdown files."""
    fixed = []
    
    for p in sorted(DOCS.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        new_text = text
        
        # Find all absolute paths
        abs_paths = re.findall(r'\]\((/[^)]+)\)', text)
        if not abs_paths:
            continue
        
        # Calculate relative path from file to docs root
        rel_to_root = p.relative_to(DOCS)
        depth = len(rel_to_root.parts) - 1  # e.g., content/columns/2002/ = 2
        
        # Convert absolute paths to relative
        for abs_path in abs_paths:
            if abs_path.startswith("/content/") or abs_path.startswith("/assets/"):
                # Remove leading / and make relative
                rel_path = abs_path[1:]  # Remove leading /
                if depth > 0:
                    # Need to go up depth levels
                    up_path = "../" * depth
                    rel_path = up_path + rel_path
                
                # Replace in text
                new_text = new_text.replace(f"]({abs_path})", f"]({rel_path})")
        
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            fixed.append(str(p.relative_to(DOCS)))
    
    print(f"Fixed absolute paths in {len(fixed)} files")
    for f in fixed[:10]:
        print(f"  - {f}")
    if len(fixed) > 10:
        print(f"  ... and {len(fixed) - 10} more")


def beautify_src_html():
    """Beautify HTML files in src-content/."""
    beautified = []
    
    for p in sorted(SRC.rglob("*.html")):
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        
        # Remove trailing whitespace
        lines = [line.rstrip() for line in lines]
        
        # Remove excessive blank lines (keep max 2)
        cleaned = []
        blank_count = 0
        for line in lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:
                    cleaned.append(line)
            else:
                blank_count = 0
                cleaned.append(line)
        
        new_text = "\n".join(cleaned)
        new_text = new_text.rstrip("\n") + "\n"
        
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            beautified.append(str(p.relative_to(SRC)))
    
    print(f"Beautified {len(beautified)} src-content HTML files")


def main():
    print("Processing Jekyll markdown and src-content HTML files...")
    
    print("\n1. Removing markdown title headings...")
    remove_title_headings()
    
    print("\n2. Fixing absolute paths to relative...")
    fix_absolute_paths()
    
    print("\n3. Beautifying src-content HTML files...")
    beautify_src_html()
    
    print("\nDone!")


if __name__ == "__main__":
    main()
