# AI Development Statistics - Project Report

Human-readable report of AI development activity across the archive project. This report aggregates the raw data from the session statistics JSON files into a presentation suitable for project stakeholders, contributors, and external collaborators.

**Source data**: `.ai-activity/ai-sessions/` **Generated**: 2026-09-03 **Reporting period**: 2026-07-31 to 2026-09-03

## Executive Summary

The project accumulated **174 hours of active work** across 16 sessions and 524 user prompts. All work was completed using free models, so the total monetary cost was **$0**. The bulk of the work (87%) was performed in a single long-running development session.

| Headline | Value |
| --- | --- |
| Active time invested | 174h 23m |
| User prompts written | 524 |
| Average prompt length | 31 words |
| Total tokens processed | 77.9M |
| Total cost | $0.00 |
| Subagent tasks completed | 7 |

## What Was Built

The AI development work supported the following project activities:

- **Documentation reorganization** - Restructured 30+ docs into topic-based folders
- **Script development** - Created session backup, changelog generator, and audit scripts
- **Archive modernization** - HTML5 conversion, CSS3 variables, and folder structure
- **Pre-migration preparation** - v1 prep files consolidated and obsolete gitignore entries retired
- **Skills system** - Authored three active AI skills and preserved four archived
- **Database back-up infrastructure** - Configurable, path-anonymized session export

## Time Investment

### Where the Time Went

| Activity Type | Hours | % of Total |
| --- | --- | --- |
| AI processing (model compute) | 78h 24m | 45% |
| User activity (writing + waiting + review + verification) | 95h 58m | 55% |
| **Total active work** | **174h 23m** | **100%** |

The AI did 45% of the time-on-task. The remaining 55% was user activity split between writing prompts and reviewing/verifying AI output.

### How Time Was Spent per Session

| Session | Type | Duration | User Prompts |
| --- | --- | --- | --- |
| Main development session | Long-running | 151h 43m | 473 |
| Famtree: Combine commits | One-shot | 14h 18m | 34 |
| Famtree: HTML5 conversion | One-shot | 39 min | 1 |
| Famtree: HTML amendments (×2) | One-shot | 14 min total | 2 |
| Famtree: HTML transform | One-shot | 21 min | 1 |
| Famtree: Style optimization (×2) | One-shot | 32 min total | 2 |
| Repo exploration (×2) | One-shot | 12 min total | 2 |
| Documentation audit (×2) | One-shot | 25 min total | 2 |

The subagent pattern is highly effective: seven discrete tasks completed in under 2 hours of total active time, freeing the main session for strategic work.

## Prompt Style Analysis

The user has a focused, action-oriented prompting style. Most prompts are short and direct:

| Prompt Length | Frequency | Total Time Est. |
| --- | --- | --- |
| 1–9 words (e.g., "Continue.") | 24% | 31 min |
| 10–49 words (typical task) | 53% | 4h 37m |
| 50–199 words (with context) | 13% | 3h 30m |
| 200–499 words (detailed brief) | 2% | 1h 30m |
| 500+ words (extensive spec) | <1% | 10 min |

77% of prompts are under 50 words. This pattern suggests a workflow where the user provides concise direction and trusts the AI to fill in implementation details.

## Token Economics

The model processed 77.9 million tokens during the project, with the following split:

| Token Type | Count | What It Represents |
| --- | --- | --- |
| Input | 77.9M | Context sent to the model (history, files, prompts) |
| Output | 2.2M | Text the model generated (code, docs, answers) |
| Reasoning | 2.1M | Internal chain-of-thought before answers |

The ~36:1 input-to-output ratio is characteristic of long-running development sessions where the model re-reads accumulated history on every turn. A short session would typically show 5:1 or 10:1.

All tokens were processed at **$0** because the project uses the primary AI co-developer's free tier. If migrated to a paid tier at typical pricing of $3/M input tokens and $15/M output tokens, the equivalent cost would be approximately **$267** ($233 input + $34 output).

## Cost-Benefit Summary

| Investment | Value |
| --- | --- |
| Active time | 174h 23m |
| Hypothetical cost (if paid tier) | $267 |
| Actual cost (free tier) | $0 |
| Subagent tasks delivered | 7 |
| Skills documented | 3 active + 4 archived |
| Documentation pages authored/maintained | 30+ |

The free-tier cost makes the project reproducible by any developer with similar tool access. The token economy (input-heavy) indicates the bottleneck is context window size, not generation cost.

## Subagent Performance

The project used subagents (`@explore` and `@general`) for 7 of 16 sessions. Subagent characteristics:

- **Average duration**: 19 minutes per task (vs. 151h for the main session)
- **Average user prompts**: 1 (vs. 473 for the main session)
- **Tasks per hour**: 14x faster than the main session rate

This validates the subagent pattern for one-shot research and refactor tasks where the user does not need to iterate.

## Recommendations for Future Projects

1. **Use the subagent pattern liberally** - One-shot research and refactor tasks are dramatically faster when isolated to dedicated subagent sessions.

2. **Front-load context** - Even with concise 31-word average prompts, the model consumed ~36x more input than output tokens. Pre-loading relevant files into the context (rather than expecting the model to discover them) reduces the input burden.

3. **Batch related work** - Isolating one-off analysis tasks into their own dedicated sessions keeps the main development flow focused on strategic work.

4. **Watch session length** - The main session at 7,872 messages is approaching the limits of comfortable context navigation. Periodic session breaks (and starting fresh sessions for new work phases) would improve focus.

## Reproducibility

This report was generated from the session statistics JSON files using the project scripts. To regenerate:

1. Run the session backup script to export and anonymize session data
2. Run the stats script to generate statistics
3. Run the totals script to combine stats and regenerate this report

See session stats tools documentation for AI development tools guides.

## See Also

- Project stats totals markdown - Internal analysis with full session breakdown
- Project stats totals JSON - Raw aggregate data
- Session stats units documentation - Definitions of all stats fields
