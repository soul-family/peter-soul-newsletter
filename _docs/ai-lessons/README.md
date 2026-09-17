# AI User Training & Outcomes

This folder contains two types of AI-assisted development guidance:

1. **User Training Guides** - Measurable rules for getting the most out of AI coding assistants
2. **AI Outcomes** - Recommendations and analysis from reviewing project sessions

## User Training Guides

Operational manual for getting the most out of AI coding assistants. These guides teach **user behaviour**, not AI behaviour: how to phrase, what to feed in, how to steer, when to stop and verify.

Every rule here is measurable - each one maps 1:1 to a field in session stats, so your session stats double as a compliance report. If a stat is red (high re-requests, lots of corrections), the fix is in one of the numbered rules below.

### Contents

| File | Covers | Stats it fixes |
| --- | --- | --- |
| `quick-reference.md` | Pre-flight checklist, card-per-rule cheat sheet, common anti-patterns | all |
| `prompts-and-task-encoding.md` | Writing one task per message, clear goals, killing hedges | 3.Clarity, 6 |
| `context-and-constraints.md` | File paths, error logs, stack, constraints, acceptance criteria | 3.Clarity, 4.Steering |
| `steering-and-iteration.md` | Correcting early, avoiding re-requests, scoping extensions | 3.Steering |
| `verification-and-acceptance.md` | Tests/lint/build gates, reviewing the diff, "done" definitions | 5.Outcome |
| `session-hygiene-and-meta.md` | Session splitting, task replacing, focus, freshness | 1, 3.Volume, 4.Process |
| `hooks-and-automation.md` | Service/prompt hooks to automate the rules, telemetry for stats | all (persistently) |

### How to use

1. **Before any session**: run the 2-minute pre-flight in `quick-reference.md`.
2. **During**: if the AI stalls, look up the matching rule card (each is ~30s to re-read).
3. **After**: export the session, run the stats script, and check which improvements from the analysis point back here.
4. **Persist**: for any red stat you see 3+ times, stop fixing it by memory and hook it - see `hooks-and-automation.md`.

### Golden rules (the whole manual in 7 lines)

1. One task per message. If you want three things, send three messages.
2. Name the files. Give the paths up front, not after four turns of guessing.
3. State constraints before work starts: stack, deps, "no new libraries", performance, platform.
4. Define "done": what to test, what command proves it works.
5. Correct direction within one or two turns - never let it build the whole wrong thing.
6. Say yes/no, not "maybe". Hedges invite hedged output.
7. Treat AI output as a draft. Review, test, and only then accept.

## AI Outcomes

Recommendation and outcome documents produced from AI analysis activities on the project.

### Contents

- Per-session improvement recommendations
- Process improvement suggestions from session reviews
- Skill usage analysis and optimization notes

### Output Location

Analysis documents are generated as markdown files in this folder, following the analysis workflow from `.skills/ai-analysis/skill.md`.

Current contents:

- `ai-recommendations.md` - Session-specific AI reasoning and recommendations
