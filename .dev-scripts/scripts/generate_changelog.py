#!/usr/bin/env python3
"""
generate_changelog.py — update CHANGELOG.md from .changelog/ folder.

Reads:
  - .changelog/unreleased.md

Updates:
  - Prepends unreleased entries to CHANGELOG.md
  - Empties .changelog/unreleased.md after successful update
"""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
CHANGELOG_DIR = BASE / '.changelog'
CHANGELOG_MD = BASE / 'CHANGELOG.md'
UNRELEASED_MD = CHANGELOG_DIR / 'unreleased.md'


def read_file(path):
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8')


def main():
    unreleased = read_file(UNRELEASED_MD)
    existing = read_file(CHANGELOG_MD)

    parts = []
    if unreleased.strip():
        parts.append(unreleased.strip())
    if existing.strip():
        parts.append(existing.strip())

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
