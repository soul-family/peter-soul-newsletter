#!/usr/bin/env python3
"""
generate_changelog.py - promote .changelog/unreleased.md into CHANGELOG.md.

This is a standalone script. Run it manually when ready to release.

Reads:
  - .changelog/unreleased.md
  - CHANGELOG.md (existing released versions)

Writes:
  - CHANGELOG.md with the unreleased entries promoted to a new versioned section
  - .changelog/unreleased.md emptied
  - VERSION file updated

Behaviour:
  - If .changelog/unreleased.md is empty, no changes are made.
  - The next version is computed by incrementing the patch number of the
    highest existing version. If no versions exist, defaults to v0.1.0.
  - The new version section is inserted at the top of the released entries,
    after the file header. The header is preserved.
  - Only the unreleased entries that exist at the time the script runs are
    promoted; running the script twice will not duplicate entries.
"""

import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent
CHANGELOG_DIR = BASE / '.changelog'
CHANGELOG_MD = BASE / 'CHANGELOG.md'
UNRELEASED_MD = CHANGELOG_DIR / 'unreleased.md'
VERSION_MD = BASE / 'VERSION'

DEFAULT_VERSION = 'v0.1.0'
VERSION_PATTERN = re.compile(r'^##\s*\[(v?\d+\.\d+\.\d+)\]\s*$', re.MULTILINE)


def parse_latest_version(content):
    """Return the latest (highest) version string found in CHANGELOG.md, or None."""
    matches = VERSION_PATTERN.findall(content)
    if not matches:
        return None
    return matches[0]


def bump_patch(version):
    """Increment the patch number of a version like v1.2.3 -> v1.2.4."""
    v = version.lstrip('v')
    parts = v.split('.')
    if len(parts) != 3:
        return DEFAULT_VERSION
    try:
        major, minor, patch = (int(p) for p in parts)
    except ValueError:
        return DEFAULT_VERSION
    return f'v{major}.{minor}.{patch + 1}'


def split_header_and_versions(content):
    """Split CHANGELOG.md into (header, versions_text).

    Header is everything before the first ## [vX.Y.Z] heading.
    versions_text is the rest.
    """
    m = VERSION_PATTERN.search(content)
    if not m:
        return content.strip(), ''
    header = content[:m.start()].rstrip() + '\n'
    versions = content[m.start():].strip()
    return header, versions


def promote(unreleased_text, existing_content):
    """Promote unreleased entries to a new versioned section.

    Returns the new CHANGELOG.md content. If unreleased is empty, returns
    the existing content unchanged.
    """
    if not unreleased_text.strip():
        return existing_content

    # Strip the "## [unreleased]" header from the unreleased content
    body = re.sub(
        r'^##\s*\[unreleased\]\s*\n',
        '',
        unreleased_text.strip(),
        count=1,
    ).strip()

    if not body:
        return existing_content

    latest = parse_latest_version(existing_content)
    next_version = bump_patch(latest) if latest else DEFAULT_VERSION

    header, versions = split_header_and_versions(existing_content)

    new_section = f'## [{next_version}]\n\n{body}'
    if versions:
        new_content = f'{header}\n\n{new_section}\n\n{versions}\n'
    else:
        new_content = f'{header}\n\n{new_section}\n'

    return new_content


def main():
    if not UNRELEASED_MD.exists():
        print(f'No unreleased changelog at {UNRELEASED_MD}')
        return 0

    unreleased = UNRELEASED_MD.read_text(encoding='utf-8')
    if not unreleased.strip():
        print('No unreleased entries to promote')
        return 0

    existing = CHANGELOG_MD.read_text(encoding='utf-8') if CHANGELOG_MD.exists() else ''
    new_content = promote(unreleased, existing)

    CHANGELOG_MD.write_text(new_content, encoding='utf-8')
    UNRELEASED_MD.write_text('', encoding='utf-8')

    latest = parse_latest_version(new_content)
    if VERSION_MD.exists():
        VERSION_MD.write_text(latest.lstrip('v') + '\n', encoding='utf-8')
        print(f'Updated VERSION file to {latest}')
    else:
        print('Note: VERSION file not present; create it manually if version tracking is desired')
    print(f'Promoted unreleased entries to {latest}')
    print(f'Cleared {UNRELEASED_MD.name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
