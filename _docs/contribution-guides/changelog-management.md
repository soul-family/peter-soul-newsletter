# Changelog Management

## Overview

The changelog records all notable changes to the project. Each version entry is goal-focused, concise, and free of transient background details.

The root `CHANGELOG.md` is the published, released changelog. It is generated from `.changelog/unreleased.md` by running the changelog generator script manually. The pre-commit audit verifies version synchronization but does not automatically promote entries. The only manual edit to `CHANGELOG.md` should be the file header (the first few lines describing format and versioning). All versioned entries are produced by the generator.

## Files

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Released changes grouped by version, in reverse chronological order (generated) |
| `VERSION` | Single line containing the current version number in semver format |
| `.changelog/unreleased.md` | Work-in-progress entries for the next version, manually maintained |

## Workflow

1. As work progresses, append new entries to `.changelog/unreleased.md` using the entry format below.
2. When ready to release, run the changelog generator: `python .dev-scripts/scripts/audit/generate_changelog.py`
3. The generator will:
   - Promote the entries to a new version section in `CHANGELOG.md` (next patch version)
   - Update the `VERSION` file if it exists
   - Empty `.changelog/unreleased.md`
4. If `.changelog/unreleased.md` is empty, no changes are made.
5. Never edit `CHANGELOG.md` version sections directly — the generator is the single source of truth. If a release needs a different version (e.g., a minor or major bump), edit `.changelog/unreleased.md` first, run the generator, then manually edit `CHANGELOG.md`.

The `unreleased.md` file is the single source of truth for "what is in progress" — never delete it; only the generator clears it after a successful release.

## Version Numbering

- **Patch** (e.g., `v1.0.0` → `v1.0.1`) for bug fixes and minor corrections
- **Minor** (e.g., `v1.0.0` → `v1.1.0`) for new features and non-breaking changes
- **Major** (e.g., `v1.x.x` → `v2.0.0`) for breaking changes or large rewrites

The generator always increments the patch number of the most recent version. To release a minor or major version:
1. Edit `.changelog/unreleased.md` with your entries
2. Run the generator to promote to a patch version
3. Manually edit the version header in `CHANGELOG.md` to the desired version
4. Update the `VERSION` file manually if it exists

## Version File

The `VERSION` file is optional. If present:
- It should contain only the version number without the `v` prefix (e.g., `1.7.0`)
- The changelog generator will update it automatically when promoting unreleased entries
- The pre-commit audit will verify it matches `CHANGELOG.md` if it exists, but will not auto-promote

If not present:
- Version tracking is manual via `CHANGELOG.md` only
- No validation errors are generated

## Rules

- Keep entries goal-focused: describe what changed, not why it changed
- **Future-proof entries**: Do not mention specific filenames, function names, script names, or file paths — these can change and make the changelog inaccurate
- Describe capabilities and features, not implementation details
- Group related changes under the same heading
- Use present tense: "Add", "Change", "Fix"
- One version per section; reverse chronological order
- Version headers must be exactly `## [X.Y.Z]` with no additional title or description after the version number
- Every entry under an unreleased section will be moved to a new version heading on release — write entries assuming they will become part of a named version
- **Only record completed work**: `.changelog/unreleased.md` is for changes that have already been implemented. Do not add planned work, future ideas, or todo items here. Use `todo-next.md` for planned tasks instead.

## Entry Format

Append entries to `.changelog/unreleased.md` like this:

```markdown
## [unreleased]

### Added
- New feature or capability

### Changed
- Existing behavior modified

### Fixed
- Bug fixes or corrections

### Deprecated
- Features marked for removal

### Removed
- Features removed in this version

### Security
- Security-related changes
```

Only include the section headings that have entries; remove empty ones.

## Examples

**Good (future-proof):**
- "Add multi-AI co-developer support to session backup"
- "Add tiered word-count user input time calculation"
- "Consolidate session databases in shared co-developer directory"

**Bad (will become outdated):**
- "Add `--developer` flag to `ai-sessions-backup.py`"
- "Update `generate_path_variations()` function"
- "Move databases to developer-specific subdirectories under `.ai-activity/ai-sessions/`"

## See Also

- `_docs/dev-guides/version-management.md` — Version file management and synchronization
- `.dev-scripts/scripts/audit/generate_changelog.py` — Changelog generator script
- `.dev-scripts/scripts/pre-commit/pre_commit_audit.py` — Pre-commit audit with version checks

## Recommit Checklist

Before committing, verify:

- [ ] `.changelog/unreleased.md` is empty (or contains entries you want to release)
- [ ] `CHANGELOG.md` has a version header for every release
- [ ] `VERSION` file exists and matches the latest version in `CHANGELOG.md` (if VERSION file is used)
- [ ] Pre-commit audit passes (`python .dev-scripts/scripts/pre-commit/pre_commit_audit.py`)
