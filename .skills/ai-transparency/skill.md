# AI Transparency Skill

## Goal
Ensure consistent AI transparency throughout the project by logging interactions, preserving planning artifacts, and maintaining a clear, granular audit trail.

## When to Use
- At the beginning of every AI interaction
- When making planning decisions
- When creating or modifying files
- When running migration or verification workflows
- When reviewing or auditing project history

## Prerequisites
- `.ai-activity/` directory exists with required log files
- `.skills/` directory exists for skill definitions

## Logging Rules

### Granularity and Focus
- **One event per log entry**: each decision, file modification, or milestone gets its own entry
- **Time-boxed entries**: group related micro-decisions into a single session entry when they happen within one continuous interaction
- **Avoid background noise**: do not log routine operations unless they affect project state or decisions
- **Structured format**: use consistent markdown tables and bullet formats for readability in long logs

### INTERACTIONS.md
Log per task or per significant change:
- Task description
- Decisions made (bulleted, concise)
- Files modified (paths only, no OS-specific details)
- Outcome or next step

### SOURCES.md
Log per research action:
- Source description
- Purpose or what was extracted
- Reliability rating (High/Medium/Low)
- Keep entries grouped by research session

### TOOLS.md
Log per operation type:
- Tool category (file browser, text editor, version control, terminal)
- Purpose
- Keep generic; do not log exact command paths or OS-specific shell details

### SESSIONS.md
One row per interaction:
- Date
- Session ID
- Outcome summary (1 line)
- Link to detailed entries in INTERACTIONS.md if needed

## Planning Preservation
- Original planning documents must preserve in `.dev-scripts/` or `_temp/` folders
- No planning artifact should discard; move to archive if no longer active
- All intermediate scripts and calculation code must preserve in `.dev-scripts/`
- Use file naming that preserves chronology: `planning-original.md`, `date_mapper_v2.py`

## Skill Organization
- Skills are stored in `.skills/` directory
- Each skill has a clear Goal, When to Use, Prerequisites, and workflow steps
- Skills are loaded at the start of matching tasks

## Migration Transparency

### Consulting Phase
- Document site structure analysis in INTERACTIONS.md
- Log earliest content date and batch upload date detection
- Record cross-reference findings (blog posts linking to individual pages)
- Capture user preferences: commit granularity, license type, day/time recovery needs

### Planning Phase
- Create plan document outlining migration strategy
- Define preparation folder structure for user review
- Choose skills and reusable scripts
- Log all planning decisions in INTERACTIONS.md

### Execution Phase
- Log all file operations in INTERACTIONS.md
- Preserve intermediate scripts in `.dev-scripts/`
- Run verification and log results
- Document any issues or deviations from the plan

## File Management

### Temporary Files
- Active planning files may reside in `_temp/` during development
- Completed planning artifacts should move to `.dev-scripts/` for preservation
- Never delete planning artifacts without explicit user instruction

### Reusable Code
- All Python scripts for date mapping, prep verification, and git migration go in `.dev-scripts/`
- Scripts must document with usage instructions
- Intermediate calculation scripts must preserve even if superseded

## Verification Standards

### Transparency Checklist
- [ ] INTERACTIONS.md updated with current task
- [ ] SOURCES.md reflects all consulted sources
- [ ] TOOLS.md updated with tools used
- [ ] SESSIONS.md updated with outcome
- [ ] Planning artifacts preserved in `.dev-scripts/` or `_temp/`
- [ ] No intermediate code deleted without review

### Audit Trail
- Every decision must trace to a session log
- File modifications must record with timestamps
- User preferences and approvals must document
