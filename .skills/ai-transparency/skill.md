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
- `.skills/` directory exists for active skill definitions

## Logging Rules

### Granularity and Focus
- **One event per log entry**: each decision, file modification, or milestone gets its own entry
- **Time-boxed entries**: group related micro-decisions into a single session entry when they happen within one continuous interaction
- **Focus on meaningful events**: log only operations that affect project state or decisions
- **Structured format**: use consistent markdown tables and bullet formats for readability in long logs

### interactions.md
Log per task or per significant change:
- Task description
- Decisions made (bulleted, concise)
- Files modified (paths only, no OS-specific details)
- Outcome or next step

### sources.md
Log per research action:
- Source description
- Purpose or what was extracted
- Reliability rating (High/Medium/Low)
- Keep entries grouped by research session

### tools.md
Log per operation type:
- Tool category (file browser, text editor, version control, terminal)
- Purpose
- Keep generic; do not log exact command paths or OS-specific shell details

### sessions.md
One row per interaction:
- Date
- Session ID
- Outcome summary (1 line)
- Link to detailed entries in interactions.md if needed

## Planning Preservation
- Planning documents preserve in version control, not in local folders
- No planning artifact should discard; intermediate files are in git history
- All intermediate scripts and calculation code are preserved in git history
- Use file naming that preserves chronology: `planning-original.md`, `date-mapping-v2`

## Skill Organization
- Active skills stored in `.skills/` directory
- v1 migration skills documented in `_docs/reports/` for historical reference
- Each skill has a clear Goal, When to Use, Prerequisites, and workflow steps
- Skills are loaded at the start of matching tasks

## Migration Transparency

The v1 backup migration is complete. All decisions, intermediate files, and scripts are preserved in git history and documented in the AI activity logs. The following phases document the completed v1 migration process:

### Consulting Phase
- Document site structure analysis in interactions.md
- Log earliest content date and batch upload date detection
- Record cross-reference findings (blog posts linking to individual pages)
- Capture user preferences: commit granularity, license type, day/time recovery needs

### Planning Phase
- Create plan document outlining migration strategy
- Define preparation folder structure for user review
- Choose skills and reusable scripts
- Log all planning decisions in interactions.md

### Execution Phase
- Log all file operations in interactions.md
- Preserve intermediate scripts in version control (git history)
- Run verification and log results
- Document any issues or deviations from the plan

## File Management

### Temporary Files
- Active planning files may reside in `_temp/` during development
- Completed planning artifacts are logged in AI activity and changelog; intermediate code is preserved in git history
- Planning artifacts require explicit user instruction before retirement

### Reusable Code
- Essential scripts go in the `.dev-scripts/` folder
- Scripts must document with usage instructions
- Intermediate calculation scripts are preserved in git history

## Verification Standards

### Transparency Checklist
- [ ] interactions.md updated with current task
- [ ] sources.md reflects all consulted sources
- [ ] tools.md updated with tools used
- [ ] sessions.md updated with outcome
- [ ] Intermediate code remains intact unless reviewed and approved for retirement

### Audit Trail
- Every decision must trace to a session log
- File modifications must record with timestamps
- User preferences and approvals must document
