# Session Stats Template

> Template for building per-session analytics. Apply to each individual session transcript independently, not aggregated across sessions.

## Session Metadata

- **Session ID**: `ses_`
- **Title**:
- **Directory**:
- **Created**:
- **Updated**:
- **Total Messages**:
- **Total Parts**:
- **Total Tokens** (approx):

## User Behaviour

### Turn Structure
- User messages count
- AI messages count
- User turns with tool calls
- User follow-up rate (% of turns that are follow-ups vs. new topics)
- Clarification requests made by user

### Communication Patterns
- Average tokens per user message
- Average chars per user message
- Prompt specificity score (1-10)
- Context provided in initial prompt (yes/no, size in chars)
- Revision frequency (how often the user revises/edits their request)

### Tool Usage (User)
- Tools invoked directly by user (if applicable)
- Tool usage frequency

### Decision Patterns
- Approvals vs. rejections of AI suggestions
- Iterations on a single task (how many back-and-forth cycles)
- Abandonment rate (tasks started but not completed within session)

## AI Behaviour

### Response Structure
- AI messages count
- Non-user messages count (reasoning, tool results, step-starts)
- Average tokens per AI response
- First-response latency (if available)

### Tool Usage (AI)
- Unique tools called
- Total tool calls
- Successful tool calls
- Failed tool calls
- Most frequently used tool
- Tool call efficiency (ratio of tool calls to task completions)

### Code Quality (when applicable)
- Files created
- Files modified
 - Files retired from the codebase
- Lines of code added (approx)
 - Lines of code retired from the codebase (approx)
- Lint checks run
- Tests run
- Commits made

### Error Handling
- Errors encountered
- Retries attempted
- Fallback strategies used

## Outcome Metrics

- **Tasks completed**:
- **Tasks failed/abandoned**:
- **Session duration** (approx):
- **Success rate**:

## Improvement Opportunities

### User Could
- Be more specific in initial prompt
- Provide more context upfront
- Reduce back-and-forth iterations
- Batch independent requests

### AI Could
- Ask clarifying questions earlier
- Reduce tool call overhead
- Provide more structured summaries
- Anticipate edge cases proactively

### General
- Suggestions for process improvement
- Recommendations for skill/tool usage

## Raw Counts

| Metric | Count |
|--------|-------|
| User text parts | |
| AI text parts | |
| Reasoning parts | |
| Tool-uses parts | |
| Tool-results parts | |
| Total parts | |
