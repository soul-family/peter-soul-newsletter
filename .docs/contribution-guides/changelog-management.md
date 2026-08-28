# Changelog Management

## Overview

The changelog records all notable changes to the project. Each version entry is goal-focused, concise, and free of transient background details.

## File

- `CHANGELOG.md` at repository root
- `.changelog/` folder contains the unreleased changelog entries

## Changelog Folder Structure

The `.changelog/` folder contains one file:

- `.changelog/unreleased.md` — Unreleased changes

## Generating CHANGELOG.md

Run the changelog generator to update `CHANGELOG.md` from `.changelog/`:

```bash
python .dev-scripts/scripts/generate_changelog.py
```

This command:
1. Reads `.changelog/unreleased.md`
2. Prepends entries to `CHANGELOG.md` with `[unreleased]` first, then next minor version eg. `[v1.1.0]` unless explicitly asked for major version eg. then `[v2.0.0]`.
3. Empties `.changelog/unreleased.md` after successful changelog file update.

## Rules

- Keep entries goal-focused: describe what changed, not why it changed
- Do not mention specific file paths, environment details, or OS-specific references
- Group related changes under the same heading
- Use present tense: "Add", "Change", "Fix"
- One version per section; reverse chronological order
- Version headers must be exactly `## [X.Y.Z]` with no additional title or description after the version number

## Entry Format

```markdown
## [X.Y.Z]

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
