# AI Development Analysis — Project Totals

Aggregated AI development metrics across all AI co-developer sessions for the archive project. Source: per-database stats files in `.ai-activity/ai-sessions/`.

Generated 2026-09-03.

## Project Totals

| Metric | Value |
|--------|-------|
| Sessions | 16 |
| User requests | 524 |
| Messages | 8,750 |
| Parts | 34,411 |
| User words typed | 16,059 |
| Average words per request | 31 |

## Active Time

| Component | Seconds | Human |
|-----------|---------|-------|
| AI processing | 282,144 | 78h 24m |
| User activity | 345,532 | 95h 58m |
| **Total active** | **627,676** | **174h 23m** |

Active time excludes all idle gaps (overnight, breaks, paused sessions). See session stats units documentation for calculation details.

### User Activity Breakdown

| Phase | Component | Seconds | Human |
|-------|-----------|---------|-------|
| Input | Writing prompts | 39,600 | 11h 0m |
| Input | Waiting for AI | 5,220 | 1h 27m |
| Output | Reviewing AI responses | 205,650 | 57h 15m |
| Output | Verifying AI work | 94,650 | 26h 15m |

## Token Usage

| Type | Count | Human |
|------|-------|-------|
| Input tokens | 77,917,568 | 77.9M |
| Output tokens | 2,163,636 | 2.2M |
| Reasoning tokens | 2,122,391 | 2.1M |
| **Total tokens processed** | **82,203,595** | **82.2M** |

1 token ≈ 4 characters of English text, so the project has processed roughly 328 MB of text through the model.

## Thinking Length

The model generated **8,891,574 characters** of visible reasoning text across all sessions. Reasoning text is the model's internal chain-of-thought shown to the user before the final answer.

## Cost

| Provider | Cost (USD) |
|----------|------------|
| Primary AI co-developer (free tier) | $0.00 |
| **Total** | **$0.00** |

All sessions used free/uncosted models. Token counts are tracked for analysis but no monetary cost was incurred.

## User Activity Time by Word-Count Tier

| Tier | Words | Estimated Time | Request Count | % of Total |
|------|-------|----------------|---------------|------------|
| 1–9 words (Quick command) | 15s | 15 sec | 126 | 24.0% |
| 10–49 words (Short task) | 60s | 1 min | 277 | 52.9% |
| 50–199 words (Medium task) | 180s | 3 min | 70 | 13.4% |
| 200–499 words (Detailed task) | 360s | 6 min | 10 | 1.9% |
| 500+ words (Extensive task) | 600s | 10 min | 1 | 0.2% |
| **Total** | — | — | **524** | 100% |

Most user requests (53%) are short tasks of 10–49 words. Only 2% of requests exceed 200 words, indicating focused, task-oriented interaction rather than long-form prompting.

## Per-Session Breakdown

| Session ID | Database | AI Processing | User Activity | Requests |
|------------|----------|---------------|---------------|----------|
| ses_04a4573acffeBzvWZ5C3A41mp6 | website | 64h 44m | 86h 59m | 473 |
| ses_04a44c696ffeCNMsKxBrNN3f16 | website | 4m | 26m | 1 |
| ses_03169b359ffeZoYUjvpb7X2phe | website | 2m | 9m | 1 |
| ses_TsT735m7ksz0QBlScNRWGF3V | website | 0m | 4m | 0 |
| ses_fa38b5cfaffeOomJnrS26WT0i5 | website | 33m | 49m | 7 |
| ses_fa372bc85ffeQ1IFaDQ256DK5Z | website | 0m | 0m | 0 |
| ses_fa0f418b0ffeB2OatF2rNojLk3 | website | 4m | 11m | 1 |
| ses_fa0d54c05ffehKz5Zhv87IGgaC | website | 1m | 14m | 1 |
| ses_f9e4b2f73ffe2vJfeGwtI3NvOr | website | 6m | 25m | 1 |
| ses_fe5e65fbeffeO17zqfjU1f15zw | famtree | 11h 37m | 2h 41m | 34 |
| ses_fddf6eac0ffeCj2FBiZgMFDAxr | famtree | 33m | 15m | 1 |
| ses_fdd9d5bb3ffeOfoYg4Hw52xKdO | famtree | 0m | 7m | 1 |
| ses_fdd99be69ffeMXOh1IV5BUL7Ti | famtree | 2m | 12m | 1 |
| ses_fc04cdd36ffe78C17drLFR0EhU | famtree | 15m | 12m | 1 |
| ses_fc035023fffebiW9lkD476nR2Z | famtree | 5m | 11m | 1 |
| ses_fc02e3ef6ffeRKfdvGDssw1O8z | famtree | 11m | 11m | 1 |

## Observations

1. **Single dominant session** — `ses_04a4573acffeBzvWZ5C3A41mp6` accounts for 87% of AI processing time and 91% of user activity time. This is the main ongoing development session that has been running for over a month.

2. **Subagent sessions are short** — The famtree subagent sessions completed their tasks in under 35 minutes each with single user requests. This validates the subagent pattern for one-shot refactor tasks.

3. **High input-to-output ratio** — The project consumed 77.8M input tokens but only produced 2.2M output tokens. This ~36:1 ratio is typical of long-running development sessions where the model re-reads accumulated history on every turn.

4. **Free-model cost** — All 82.1M tokens were processed at zero cost, making the project fully economically reproducible. The token counts are useful for capacity planning if migrating to a paid tier.

5. **Focused user style** — Average request is 31 words, with 77% of requests under 50 words. Users in this project prefer concise, action-oriented prompts over long-form briefs.

6. **Output review dominates user time** — 77h 46m (84%) of user activity is spent reviewing and verifying AI output, compared to 11h 8m (16%) writing prompts. This reflects the iterative nature of AI-assisted development.

## Related Documentation

- Session stats units documentation — Unit definitions and time calculations
- AI development statistics report — Human-readable statistics report
- Project stats totals JSON — Raw data for this analysis
