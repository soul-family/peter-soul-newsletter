# Git Management

Git is the version control and collaboration backbone for this project. All git activity must be explicitly requested by the user; do not stage, commit, merge, push, or run git commands during normal file updates.

## Core Rule

When updating project files, do not perform any git activity unless the user explicitly asks for it. File edits are working-tree changes only until the user requests a commit or other git operation.

## Commit Preparation

Before any commit, the pre-commit audit must pass. Run it manually when the user asks for a commit:

```bash
python .dev-scripts/scripts/pre-commit/pre_commit_audit.py
```

The audit checks:
- Todo and changelog entry consistency
- Documentation link validity
- Session statistics integrity
- Privacy and encoding compliance
- Version synchronization between `VERSION` and `CHANGELOG.md`

Fix any issues the audit reports before proceeding with the commit.

## Changelog and Versioning

- Work-in-progress entries go in `.changelog/unreleased.md`
- The changelog generator promotes unreleased entries to a new patch version in `CHANGELOG.md`:
  ```bash
  python .dev-scripts/scripts/audit/generate_changelog.py
  ```
- The `VERSION` file and `CHANGELOG.md` must stay in sync
- Never edit `CHANGELOG.md` version sections directly; the generator is the single source of truth
- For minor or major version bumps, edit `.changelog/unreleased.md`, run the generator, then manually adjust the version header in `CHANGELOG.md` and update `VERSION`

## Commit Metadata

Record commit metadata in `.ai-activity/ai-logs/interactions.md` for session backups:
- Commit hash
- Author
- Date
- Message

View commit metadata in VS Code Source Control panel or on GitHub.com under the Commits tab.

## Branch and Pull Request Workflow

- Create branches for focused work
- Keep PRs small and descriptive
- Link issues using `Closes #XXX` in PR descriptions
- Request review from relevant contributors
- Ensure CI checks pass before merging
- Retire branches after merging

## Backdated Timestamps

The v1 migration used backdated Git timestamps matching original publication dates. This is a historical artifact of the migration process. Current development uses normal commit timestamps.

## Git History

Intermediate scripts, calculation code, and planning artifacts from completed work are preserved in Git history. Do not rewrite or filter history unless explicitly requested.

## What Not To Do

- Do not stage changes automatically
- Do not run `git add` during normal file updates
- Do not commit without explicit user request
- Do not auto-fix audit issues without user confirmation
- Do not rewrite Git history unless explicitly requested
