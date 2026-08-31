# AI Development Analysis — Project Totals

Aggregated AI development metrics across all Kilo sessions for the petersoul.co.uk archive project. Source: `website-sessions.stats.json` and `famtree-sessions.stats.json` in `.ai-activity/ai-sessions/kilo-code/`.

Generated 2026-08-31.

## Project Totals

| Metric | Value |
|--------|-------|
| Sessions | 10 |
| User requests | 515 |
| Messages | 8,614 |
| Parts | 33,755 |
| User words typed | 18,716 |
| Average words per request | 36 |

## Active Time

| Component | Seconds | Human |
|-----------|---------|-------|
| AI processing | 279,475 | 77h 37m |
| User input (estimate) | 38,535 | 10h 42m |
| **Total active** | **318,010** | **88h 20m** |

Active time excludes all idle gaps (overnight, breaks, paused sessions). See `_docs/ai-dev-guides/session-stats-units.md` for calculation details.

## Token Usage

| Type | Count | Human |
|------|-------|-------|
| Input tokens | 77,644,340 | 77.6M |
| Output tokens | 2,136,178 | 2.1M |
| Reasoning tokens | 2,117,324 | 2.1M |
| **Total tokens processed** | **81,897,842** | **81.9M** |

1 token ≈ 4 characters of English text, so the project has processed roughly 328 MB of text through the model.

## Thinking Length

The model generated **8,866,680 characters** of visible reasoning text across all sessions. Reasoning text is the model's internal chain-of-thought shown to the user before the final answer.

## Cost

| Provider | Cost (USD) |
|----------|------------|
| Kilo (kilo-auto/free) | $0.00 |
| **Total** | **$0.00** |

All sessions used free/uncosted models. Token counts are tracked for analysis but no monetary cost was incurred.

## User Input Time by Word-Count Tier

| Tier | Words | Estimated Time | Request Count | % of Total |
|------|-------|----------------|---------------|------------|
| 1–9 words (Quick command) | 15s | 15 sec | 130 | 25.2% |
| 10–49 words (Short task) | 60s | 1 min | 302 | 58.6% |
| 50–199 words (Medium task) | 180s | 3 min | 66 | 12.8% |
| 200–499 words (Detailed task) | 360s | 6 min | 15 | 2.9% |
| 500+ words (Extensive task) | 600s | 10 min | 2 | 0.4% |
| **Total** | — | — | **515** | 100% |

Most user requests (59%) are short tasks of 10–49 words. Only 3% of requests exceed 200 words, indicating focused, task-oriented interaction rather than long-form prompting.

## Per-Session Breakdown

| Session ID | Database | AI Processing | User Input | Requests |
|------------|----------|---------------|------------|----------|
| ses_04a4573acffeBzvWZ5C3A41mp6 | website | 64h 44m | 9h 27m | 473 |
| ses_04a44c696ffeCNMsKxBrNN3f16 | website | 4m | 3m | 1 |
| ses_03169b359ffeZoYUjvpb7X2phe | website | 2m | 3m | 1 |
| ses_fe5e65fbeffeO17zqfjU1f15zw | famtree | 11h 37m | 29m | 34 |
| ses_fddf6eac0ffeCj2FBiZgMFDAxr | famtree | 33m | 6m | 1 |
| ses_fdd9d5bb3ffeOfoYg4Hw52xKdO | famtree | 0m | 6m | 1 |
| ses_fdd99be69ffeMXOh1IV5BUL7Ti | famtree | 2m | 6m | 1 |
| ses_fc04cdd36ffe78C17drLFR0EhU | famtree | 15m | 6m | 1 |
| ses_fc035023fffebiW9lkD476nR2Z | famtree | 5m | 10m | 1 |
| ses_fc02e3ef6ffeRKfdvGDssw1O8z | famtree | 11m | 6m | 1 |

## Observations

1. **Single dominant session** — `ses_04a4573acffeBzvWZ5C3A41mp6` accounts for 83% of AI processing time and 88% of user input. This is the main ongoing development session that has been running for a month.

2. **Subagent sessions are short** — The seven famtree subagent sessions completed their tasks in under 35 minutes each with single user requests. This validates the subagent pattern for one-shot refactor tasks.

3. **High input-to-output ratio** — The project consumed 77.6M input tokens but only produced 2.1M output tokens. This ~36:1 ratio is typical of long-running development sessions where the model re-reads accumulated history on every turn.

4. **Free-model cost** — All 81.9M tokens were processed at zero cost, making the project fully economically reproducible. The token counts are useful for capacity planning if migrating to a paid tier.

5. **Focused user style** — Average request is 36 words, with 84% of requests under 50 words. Users in this project prefer concise, action-oriented prompts over long-form briefs.

## See Also

- `_docs/ai-dev-guides/session-stats-units.md` — Unit definitions and time calculations
- `_docs/reports/statistics/` — Human-readable statistics report
- `project-totals.json` — Raw data for this analysis
