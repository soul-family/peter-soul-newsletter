# Session Stats Analysis Skill

## Goal

Research and document user behaviour, AI behaviour, and improvement opportunities from an individual AI co-developer session transcript, using the session analysis template.

## When to Use
- After completing or reviewing a single AI co-developer session
- When analyzing session effectiveness
- When preparing recommendations for process improvement
- When auditing user-AI interaction quality

## Prerequisites
- Session transcript file in `.ai-activity/ai-sessions/` directory
- Session contains at least 5 messages
- Session analysis template with the required metric fields

## Outputs
- A session analysis report in `.ai-activity/ai-reports/`
- Actionable user and process recommendations in `.ai-activity/ai-user-outcomes/`
- Reusable metric queries or summary data when SQLite analysis is needed

## Workflow

### Step 1: Load Session Transcript
1. Read the target session's transcript file from `.ai-activity/ai-sessions/`
2. Identify the session ID, title, and basic metadata from the file header
3. Count total messages and parts

### Step 2: Analyze User Behaviour

#### Turn Structure
- Count user text messages vs. AI messages
- Identify follow-up messages (messages that reference or build on previous content)
- Count clarification questions the user asked
- Note any user edits or revisions to requests

#### Communication Patterns
- Calculate average message length for user messages
- Assess prompt specificity: did the user provide clear, actionable instructions?
- Note whether the initial prompt included sufficient context
- Track how often the user had to correct or redirect the AI

#### Decision Patterns
- Count approvals vs. corrections in user responses
- Identify tasks that were started but not completed
- Note patterns in user request complexity (simple file edits vs. multi-step workflows)

### Step 3: Analyze AI Behaviour

#### Response Structure
- Count AI responses (text parts)
- Count non-user message types (reasoning, tool results, step-starts)
- Assess response consistency (on-topic vs. drifting)
- Note first-response quality (did the AI understand correctly on first attempt?)

#### Tool Usage
- List all unique tools called by the AI
- Count total tool calls and categorize by type
- Identify successful vs. failed tool invocations
- Note tool call efficiency: did the AI batch independent calls?
- Assess whether the AI used the right tools for the task

#### Code Quality (when applicable)
 - Count files created, modified, and retired from the codebase
- Assess code style consistency with project conventions
- Note lint or type check execution
- Track test execution and results

#### Error Handling
- Document errors encountered
- Assess retry strategies and fallback approaches
- Note whether errors were explained and resolved

### Step 4: Identify Improvement Opportunities

#### User Improvements
- Was the initial prompt clear enough?
- Could the user have provided more context upfront?
- Were there unnecessary iterations?
- Could requests have been batched?

#### AI Improvements
- Did the AI ask enough clarifying questions?
- Could the AI have been more efficient with tool calls?
- Were responses appropriately structured (concise vs. detailed)?
- Did the AI catch edge cases proactively?

#### General Process
- Were the right tools/skills available?
- Could the workflow be streamlined?
- Any repeated patterns that suggest automation opportunities?

## Output Format
Produce a markdown document following the project session analysis template. Fill in all applicable fields with concrete data from the session. Leave irrelevant sections blank or mark as N/A.

## Verification
- [ ] All message counts verified against transcript
- [ ] Tool call counts verified
- [ ] Improvement suggestions are specific and actionable
- [ ] At least 3 user and 3 AI behaviour observations documented
