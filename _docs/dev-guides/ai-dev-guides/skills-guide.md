# Skills Guide

How to use AI co-developer skills for the archive project — benefits, calling syntax, inputs, and workflow guidance.

## What Are Skills

Skills are pre-written markdown workflows stored in `.skills/` (active) and `.skills-archived/` (historical). Each skill defines a **Goal**, **When to Use**, **Prerequisites**, **Workflow**, and **Verification** checklist. Loading a skill injects its instructions into the current session.

### Project Benefits

| Benefit | Active Skills |
|---------|--------------|
| Transparency audit | `ai-transparency` enforces consistent logging in `.ai-activity/` |
| Session preservation | `ai-session-backup` exports sessions with local paths anonymized |
| Self-improvement | `ai-analysis` reviews session transcripts for behavioural insights |
| Knowledge retention | All decisions, sources, and tools persist in version-controlled logs |

## How to Call a Skill

Load a skill at the start of a session or when a matching task arises:

```
skill(name="ai-transparency")
skill(name="ai-session-backup")
skill(name="ai-analysis")
```

The skill name matches the folder name under `.skills/`. Archived skills are not loaded but can be read for reference.

## Active Skills

### ai-transparency

**Benefits for the project:** Ensures every AI interaction is logged consistently; creates a verifiable audit trail for all decisions and file changes.

**When to use:**
- At the start of every AI interaction
- When making planning decisions
- When creating or modifying files
- When reviewing or auditing project history

**Inputs to give:**
- Task description (one sentence)
- Key decisions made (bulleted, concise)
- Files modified (role-based, not exact paths)
- Outcome or next step

**What it produces:**
- Entries in `.ai-activity/ai-logs/interactions.md`
- Source references in `sources.md`
- Tool usage in `tools.md`
- Session summaries in `sessions.md`

**Verification checklist:**
- [ ] `interactions.md` updated with current task
- [ ] `sources.md` reflects all consulted sources
- [ ] `tools.md` updated with tools used
- [ ] `sessions.md` updated with outcome

---

### ai-session-backup

**Benefits for the project:** Preserves session data in portable SQLite databases with local paths anonymized; enables offline analysis without exposing filesystem structure.

**When to use:**
- Before pushing session data to a shared repository
- When archiving sessions for long-term storage
- When local paths must be hidden from collaborators
- When offline analysis of session transcripts is needed
- When adding new sessions to an existing database (use `--append`)

**Script:** `.dev-scripts/ai-assistant/scripts/ai-sessions-backup.py`

**What it produces:**
- `<project>-sessions.db` and matching `.stats.json` files in `.ai-activity/ai-sessions/<developer>/`
- Each database contains `session`, `message`, and `part` tables
- All local paths replaced with `_www_`

**Verification checklist:**
- [ ] Database files exist in `.ai-activity/ai-sessions/<developer>/`
- [ ] Stats JSON files exist alongside databases
- [ ] Session directories show `_www_` (not local paths)
- [ ] No local path strings found in any database column
- [ ] Session, message, and part counts match source database

---

### ai-analysis

**Benefits for the project:** Reveals usage patterns, identifies improvement opportunities, and generates actionable recommendations from individual session transcripts.

**When to use:**
- After completing or reviewing a single AI co-developer session
- When analyzing session effectiveness
- When preparing recommendations for process improvement

**Inputs to give:**
- Session transcript file from `.ai-activity/ai-sessions/`
- Session ID, title, and basic metadata
- The session analysis template for metrics structure

**What it produces:**
- Report documents in `.ai-activity/ai-reports/`
- Recommendations in `.ai-activity/ai-user-outcomes/`
- Metrics dashboard queries for SQLite analysis

**Verification checklist:**
- [ ] All message counts verified against transcript
- [ ] Tool call counts verified
- [ ] Improvement suggestions are specific and actionable
- [ ] At least 3 user and 3 AI behaviour observations documented

## Archived Skills

These skills were used for the v1 backup migration, which is complete. They are preserved in `.skills-archived/` for historical reference:

| Skill | Purpose |
|-------|---------|
| `date-aware-backup` | Derives publish dates from filenames and creates backdated Git commits |
| `commit-prep-verifier` | Validates preparation folder structure and file dates |
| `commit-preparation-to-staged` | Moves prep folder content to root and commits with backdated timestamps |
| `date-aware-pre-commit-from-prep-folder` | Sets file/folder timestamps for backdated commits |

## Skill Loading in Context

| Phase | Skill to load |
|-------|---------------|
| Session start | `ai-transparency` |
| During work | `ai-transparency` |
| Before commit | `pre_commit_audit` script |
| Session backup | `ai-session-backup` |
| Post-session analysis | `ai-analysis` |
