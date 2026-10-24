# Version Management

## Overview

This project uses [Semantic Versioning](https://semver.org/) with a single source of truth for the current version number.

## Version Sources

| File | Purpose |
| --- | --- |
| `VERSION` | Current version number (e.g., `1.7.0`) |
| `CHANGELOG.md` | Released versions with change descriptions |
| `.changelog/unreleased.md` | Pending changes for next version |

## Version Format

- The `VERSION` file contains only the version number without the `v` prefix (e.g., `1.7.0`, not `v1.7.0`)
- `CHANGELOG.md` uses `v` prefix in headers (e.g., `## [v1.7.0]`)
- Versions follow `MAJOR.MINOR.PATCH` format

## Synchronization

The `VERSION` file and `CHANGELOG.md` must always be in sync:

- The pre-commit audit checks that `VERSION` matches the latest version in `CHANGELOG.md`
- The changelog generator (`generate_changelog.py`) updates both files atomically when promoting unreleased entries
- If they don't match, the commit will fail

> **Note:** The pre-commit audit reports issues but does not automatically fix them. Run the changelog generator manually when ready to release.

When the `VERSION` file does not exist:

- Version tracking is manual via `CHANGELOG.md` only
- No validation errors are generated

## Version Bumps

### Patch

Run the changelog generator manually when ready to release:

```bash
python .dev-scripts/scripts/audit/generate_changelog.py
```

If `.changelog/unreleased.md` is non-empty, the generator will:

1. Promote entries to a new patch version in `CHANGELOG.md`
2. Update `VERSION` to match (if VERSION file exists)
3. Clear `.changelog/unreleased.md`

### Minor/Major

For minor or major version bumps:

1. Edit `.changelog/unreleased.md` with your entries
2. Run the generator to promote to a patch version
3. Manually edit `CHANGELOG.md` version header to desired version
4. Update root `VERSION` file
