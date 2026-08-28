#!/usr/bin/env python3
"""
generate_changelog.py — build CHANGELOG.md from .changelog/ folder.

Reads:
  - .changelog/unreleased.md
  - .changelog/v1.0.0.md

Writes:
  - CHANGELOG.md (unreleased first, then v1.0.0)
  - Empties .changelog/unreleased.md after successful generation
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
CHANGELOG_DIR = BASE / '.changelog'
CHANGELOG_MD = BASE / 'CHANGELOG.md'
UNRELEASED_MD = CHANGELOG_DIR / 'unreleased.md'
V1_MD = CHANGELOG_DIR / 'v1.0.0.md'


def read_file(path):
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8')


def main():
    unreleased = read_file(UNRELEASED_MD)
    v1 = read_file(V1_MD)

    parts = []
    if unreleased.strip():
        parts.append(unreleased.strip())
    if v1.strip():
        parts.append(v1.strip())

    output = '\n\n'.join(parts)
    if not output:
        output = '# Changelog'

    CHANGELOG_MD.write_text(output + '\n', encoding='utf-8')

    if unreleased.strip():
        UNRELEASED_MD.write_text('', encoding='utf-8')

    print(f'Generated {CHANGELOG_MD}')
    if unreleased.strip():
        print(f'Cleared {UNRELEASED_MD}')


if __name__ == '__main__':
    main()
