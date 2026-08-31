# Changelog Management

## Overview

The changelog records all notable changes to the project. Each version entry is goal-focused, concise, and free of transient background details.

The root `CHANGELOG.md` is the published, released changelog. It is regenerated automatically by the pre-commit audit from `.changelog/unreleased.md`. The only manual edit to `CHANGELOG.md` should be the file header (the first few lines describing format and versioning). All versioned entries are produced by the generator.

## Files

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Released changes grouped by version, in reverse chronological order (auto-generated) |
| `.changelog/unreleased.md` | Work-in-progress entries for the next version, manually maintained |

## Workflow

1. As work progresses, append new entries to `.changelog/unreleased.md` using the entry format below.
2. Run the pre-commit audit (`python .dev-scripts/scripts/pre_commit_audit.py`).
3. If `.changelog/unreleased.md` is non-empty, the audit automatically:
   - Promotes the entries to a new version section in `CHANGELOG.md` (next patch version, e.g. `v1.0.0` → `v1.0.1`)
   - Empties `.changelog/unreleased.md`
4. If `.changelog/unreleased.md` is empty, the audit makes no changelog changes.
5. Never edit `CHANGELOG.md` version sections directly — the generator is the single source of truth. If a release needs a different version (e.g., a major bump), edit `.changelog/unreleased.md` first and manually rename the version header after the audit runs.

The `unreleased.md` file is the single source of truth for "what is in progress" — never delete it; only the generator clears it after a successful release.

## Version Numbering

- **Patch** (e.g., `v1.0.0` → `v1.0.1`) for bug fixes and minor corrections
- **Minor** (e.g., `v1.0.0` → `v1.1.0`) for new features and non-breaking changes
- **Major** (e.g., `v1.x.x` → `v2.0.0`) for breaking changes or large rewrites

The generator always increments the patch number of the most recent version. To release a minor or major version, manually edit the version header in `CHANGELOG.md` after the audit promotes the entries.

## Rules

- Keep entries goal-focused: describe what changed, not why it changed
- Do not mention specific file paths, environment details, or OS-specific references
- Group related changes under the same heading
- Use present tense: "Add", "Change", "Fix"
- One version per section; reverse chronological order
- Version headers must be exactly `## [X.Y.Z]` with no additional title or description after the version number
- Every entry under an unreleased section will be moved to a new version heading on release — write entries assuming they will become part of a named version

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
