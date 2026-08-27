# Agents.md — AI Guidelines and Knowledge Focus

## Purpose

This document defines how AI agents should behave when working with knowledge in this workspace. It establishes language focus, knowledge preservation rules, communication style, and AI transparency requirements.

## Knowledge Focus Language

### Core Principle
**Minimize loss of information, preserve the original text.**

Every AI interaction should preserve, organize, and spread knowledge — never lose it.

### Author's Accurate Content Preservation Rules

| Rule | Description | Example |
|------|-------------|---------|
| Preserve exact wording | Keep original phrases where possible | "Use cadence to command attention" not "Cadence helps you command attention" |
| Tag additions | Mark inferred content with [CLARIFIED] | [CLARIFIED — inferred from subject context] |
| Flag gaps | Mark unfillable gaps with [GAP] | [GAP — needs source] |
| No invention | Never create knowledge that wasn't in the input | Don't add statistics, frameworks, or facts not present |

### Documentation
| Self-containment | Each file must work standalone | No "see other file" without summary |
| Provenance | Track where each item came from | [EXTRACTED — line 45] |

## Communication Style in Non-Author Contents

### Be Concise
- Short sentences
- Clear structure
- No unnecessary preamble
- Direct answers

### Be Precise
- Use specific terms
- Avoid vague language
- Include numbers where possible
- Define acronyms

### Be Helpful
- Answer the question asked
- Don't add tangential information
- Provide actionable next steps
- Flag when you're uncertain

## Delegation Model

### Lead Agent Responsibilities
1. Read and understand the full input
2. Plan the work (what needs to be done)
3. Assign tasks to subagents
4. Merge outputs
5. Run verification
6. Report results

### Subagent Responsibilities
1. Receive assigned task
2. Execute the task completely
3. Return output with tags
4. Flag any issues

### Communication
- Lead agent provides: full input + assigned sections + rules
- Subagent returns: completed output + notes
- Lead agent merges: all subagent outputs into final result

## Quality Standards

### Minimum Quality
- All knowledge preserved
- No invented content
- Tags on all additions
- Self-contained files
- Knowledge Completeness Report present

### Excellent Quality
- Undefined terms defined
- Incomplete processes completed
- Thin sections expanded
- Cross-references added
- Key People section populated

## AI Interaction Transparency

### Mandatory Logging
Every AI interaction must log to `.ai-activity/` folder:
- **INTERACTIONS.md** — Task details, files modified, decisions made
- **SOURCES.md** — All sources consulted during research
- **TOOLS.md** — Tools and techniques used
- **SESSIONS.md** — Session summaries with outcomes

### Granularity Rules
- **One event per entry**: each decision, file modification, or milestone gets its own entry
- **Time-boxed entries**: group related micro-decisions into a single session entry when they happen within one continuous interaction
- **Avoid background noise**: do not log routine operations unless they affect project state or decisions
- **Structured format**: use consistent markdown tables and bullet formats for readability in long logs

### When to Log
| Phase | Action |
|-------|--------|
| Session Start | Review previous session in SESSIONS.md |
| During Research | Log queries to TOOLS.md, sources to SOURCES.md |
| During Work | Log file changes to INTERACTIONS.md |
| Session End | Update all files with session summary |

### Format Standards
- Use consistent markdown tables
- Include source URLs
- Rate source reliability (High/Medium/Low)
- Cross-reference related sessions
- No dates needed (git provides timestamps)

### Skill Reference
- Skill: `.skills/ai-transparency/skill.md`
- Database: `.ai-activity/` folder
- Run at beginning of every AI interaction

## Skills

### Available Skills

| Skill | Path | Description |
|-------|------|-------------|
| Date-Aware GitHub Backup | `.skills/date-aware-backup/skill.md` | Derives original publish/update dates from filenames and filesystem timestamps, then creates backdated Git commits for a static HTML site archive. |
| Commit Prep Verifier | `.skills/commit-prep-verifier/skill.md` | Validates `src-preps/` folder structure, checks for duplicate/missing files, and verifies file Created/Modified/Accessed dates before migration. |
| AI Transparency | `.skills/ai-transparency/skill.md` | Logs AI interactions, preserves planning artifacts, and maintains a clear audit trail of decisions, sources, and tools used. |

### Skill Usage
When a task matches a skill description, load the skill file and follow its workflow. Do not improvise beyond the skill's defined steps unless the user explicitly requests deviation.
