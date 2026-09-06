# Todo — Hooks

Quick-reference workflow cards loaded at the start of a session or when a matching task arises. Each hook is a concise checklist, not a full guide.

## Session Start

- Load `ai-transparency` skill
- Review current task from `todo-next.md`
- Confirm no broken cross-references in planned work

## During Work

- Keep `ai-transparency` active
- Log significant decisions and file changes in `.ai-activity/ai-logs/`
- Avoid mentioning specific filenames, function names, or paths in permanent records

## Session Backup

- Load `ai-session-backup` skill
- Run backup with `--current-session --append`
- Regenerate stats with `ai-sessions-stats.py --incremental`

## Post-Session Analysis

- Load `ai-analysis` skill
- Review session transcript for behaviour patterns
- Update `.ai-activity/ai-reports/` if needed

## Before Commit

- Run `pre_commit_audit.py`
- Fix any todo, guide, changelog, or stats issues
- Confirm working tree is clean
