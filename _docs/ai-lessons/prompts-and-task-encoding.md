# Prompts & Task Encoding

The prompt is a spec, not a wish. The AI answers the message you wrote, not
the message you meant. Every gap in the message is paid for in turns.

## One task per message

The highest-leverage rule. A single message should contain exactly one
complete task.

Why: the stat `request cramming` measures multiple asks in one message. A
crammed message gets descoped, partially done, or re-ordered by the AI - it
will complete the cheapest interpretation first. Then you send a follow-up,
which reads as a *scope extension* or a *correction*, both of which are
red stats.

Rule:

- One message = one deliverable + its constraints + its "done" (see C4).
- Two related sub-tasks → two messages, even back-to-back.
- A long message that lists three things → split it into three messages and
  send them in sequence, not one batch. No, batching them does not make it
  faster; it makes it sloppier.

Bad (cramming): `"add a login page, also fix the logout bug from yesterday, and can you make the hero section nicer too"`
Good: `"add a login page at src/pages/login.tsx using the existing auth hook, form validation like register, and run the login tests when done"`

## State the goal as a result, not an action keyword

"Fix it", "clean up", "refactor", "improve" are action words with no target.
The AI has no idea what "it" or "better" means, so it guesses - and guess
= re-request later.

Rule: state the **end state** plus a **measurement**, or the expected
behaviour, or the failing input.

| Instead of | Write |
| --- | --- |
| "fix it" | "`login()` throws `TypeError` on empty password. Expected: friendly validation message, no throw." |
| "make it better" | "response time on `/search` should drop below 200ms; it's at 1.4s now" |
| "clean up this code" | "extract the DB connection into `src/db.ts`, wire the two existing users of it there" |
| "optimize" | "this loop runs 3× per keystroke; make it run once and cache the result" |

## Be specific enough to constrain, specific enough to verify

Three diagnostic questions before sending:

1. **What exactly is the output?** (a file, a function, a decision, a diff)
2. **What are the boundaries?** (language, deps, perf, platform, style)
3. **How will I know it worked?** (a test, a command, a visual)

If all three have answers, the message almost writes itself.

## Kill the hedges

Hedges - "maybe", "if possible", "I think", "you could", "roughly", "perhaps"
- are the second-highest-leverage fix. In stats they appear as the
`hedges` count under 3.Clarity.

Why it matters: the AI matches your confidence. "Maybe add a retry?" returns
"optional maybe-implemented" work. Committed language returns committed work.

Rules:

- Yes or no. If you actually don't care, write `"either is fine"` - that's a
  commitment, not a hedge, and it removes decision overhead.
- Don't tag "this is just an idea" - ideas become skeletons.
- When you genuinely want options, ask for options *explicitly*:
  `"give me 3 options with trade-offs, then I'll pick"` - then pick.

## Include the "why" for anything non-obvious

If a decision looks wrong on its face (weird name, unusual approach), the AI
will "correct" it back. One sentence of *why* prevents that entire class of
battle:

`"keep it in the current file even though it's growing - the deploy script greps that file"`
`"use the legacy endpoint even though the new one exists - the new one lacks tenant support"`

## Length sweet spot

- < 10 words: almost always too vague (keyword-only). It's a search query, not a spec.
- 10–60 words: ideal for a well-scoped task.
- 60–120 words: fine IF it's one task with context. Re-read for cramming.
- > 120 words: split it. It either contains multiple tasks or contains
  material that belongs in the context guide rather than the ask.

## Practice

Rewrite these to target (then check the cheat sheet):

1. `"do the auth thing better"` → ___
2. `"maybe we could add dark mode, and also fix the footer, if it's not too much trouble"` → ___
3. `"it's broken"` → ___