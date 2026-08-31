# 02 — Context & Constraints

The AI's biggest cost isn't thinking — it's **hunting**. Every turn it spends
looking for "the auth file" is a turn that produced nothing. Feed it the map
and the rules up front.

When the AI hunts anyway, your stats show it: reads/globs before the first
edit, `edit` attempts rejected with "oldString not found", re-runs. Most of
that is solvable from your keyboard in the first message.

## 2.1 Name the files, by path

Put real paths in the first message. Not "the auth file" — `src/services/auth.ts`.

If you don't know the path, spend one message directing the search and then
reset expectations: `"find the file that handles login (it's in src somewhere), then show me its path before you edit anything"`. That way the search is
*planned* — it's not drift.

Paste paths for anything the task touches: files to modify, files to match
(`"mirror the pattern in src/modules/users/store.ts"`), files that must not
change.

## 2.2 Give the error, verbatim

For bug tasks, the most valuable context you possess is the literal failure
text. The AI can't debug from "it's broken" — it will start re-running the
same command and failing the same way (your `identical re-runs` stat).

Rule: paste the **exact** error / stack / log line, and say which command
produced it and where you ran it.

Good: `"pytest src/test_orders.py fails: ...TypeError: 'NoneType' object is not subscriptable, at orders/pricing.py:88, called from discount()"`

Also say what you *expected*: `"expected price to be a float, got None"`. That
turns the task from "find the bug" into "price is None at line 88, why".

## 2.3 Constraints before work, not during

A constraint given after the build is a correction (red stat). A constraint
given before the build is free.

Standard constraint checklist to empty into the first message when relevant:

- Language / framework / version: `"TypeScript, no React — plain DOM"`.
- Dependency rules: `"no new packages", "use lodash, not a custom util"`.
- Environments: `"must run on Node 18", "Windows + Linux", "browser, no server"`.
- Performance: `"this runs on every keystroke", "keep it O(n)"`.
- Style: `"match the existing store pattern", "follow eslint config"`.
- Security: `"no secrets in code", "sanitize user input"`.
- Files that must not be touched: `"don't touch src/db/migrations"`.

## 2.4 Show the shape of the thing

If modifying something with structure — a data flow, an API, a schema — show
the shape rather than describing it:

- a 3-line excerpt of the relevant code,
- the schema/field list for data tasks,
- the public API surface for refactors.

3 lines of excerpt beats a paragraph of description. The AI's "oldString
not found" retry stat drops every time the file content is visible.

## 2.5 State assumptions you don't want questioned

Anything obvious-to-you but unknown-to-the-AI eventually gets an unnecessary
clarification question (counted in 3.Clarity) or a wrong guess (counted in
4.Process). Pre-empt:

`"assume the DB is already migrated", "both files already exist — do not create `npm init`", "reuse the existing error toast component, do not build UI"`

## 2.6 Background: relevant, recent, bounded

- Open-source tabs, docs, or a stub file you attach = excellent context.
- Three paragraphs of history = noise. The AI can't tell the relevant
  sentence from the anecdote. Give the *current* state and the *delta* you
  want, not the saga.
- If background is long, separate it clearly: `"Context (read-only): …\nTask: …"`.