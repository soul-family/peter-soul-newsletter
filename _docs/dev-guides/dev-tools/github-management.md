# GitHub Dev Guide

Standalone reference for GitHub workflows using VS Code and the GitHub web interface.

## VS Code GitHub Extension

### Setup
1. Install "GitHub Pull Requests and Issues" extension in VS Code
2. Sign in via the Command Palette (`Ctrl+Shift+P` → "GitHub: Sign In")

### Branch Management
- **Create branch**: `Ctrl+Shift+P` → "Git: Create Branch"
- **Switch branch**: Click branch name in status bar, or `Ctrl+Shift+P` → "Git: Checkout to..."
- **Sync fork**: `Ctrl+Shift+P` → "GitHub: Sync Fork"

### Pull Requests

| Action | Method |
|--------|--------|
| Create PR | Source Control panel → "..." → "Create Pull Request" |
| View PRs | `Ctrl+Shift+P` → "GitHub: View Pull Requests" |
| Checkout PR | In PR view, click "Checkout" |
| Merge PR | In PR view, click "Merge" (options: merge/commit/squash) |
| Add reviewer | In PR description, assign reviewers |
| Resolve comments | Click "Resolve" on individual comments |

### Code Review
1. Open the PR in VS Code
2. Click on the "Files changed" tab
3. Add inline comments by clicking the `+` icon next to any line
4. Submit review: "Comment", "Approve", or "Request changes"
5. Use suggestions with the `</>` icon to propose code changes

### Issues
- **Create issue**: GitHub.com → Issues → "New Issue"
- **Link to PR**: Use keywords like `Closes #123` or `Fixes #123` in PR description
- **Manage issues**: GitHub.com → Issues tab

## GitHub Web Interface

### Quick PRs
1. Go to github.com → your repository
2. Click "Branch: main" → "New branch"
3. Make changes and commit
4. Click "Compare & pull request"
5. Fill in title, description, link issues
6. Add reviewers and create PR

### GitHub Actions
- View workflow runs: repository → "Actions" tab
- Re-run failed jobs: click the run → "Re-run jobs"
- View logs: click any job → "View logs"

## Best Practices
- Keep PRs small and focused (under 400 lines changed)
- Write descriptive PR titles using conventional format: `Fix:`, `Add:`, `Refactor:`
- Link issues with `Closes #123` in PR description
- Request review from relevant team members
- Ensure CI checks pass before merging
- Use draft PRs for work-in-progress
- Delete branch after merging

## Commit Metadata

Document commit metadata for session backups and significant changes:

```
Commit: [hash]
Author: [name]
Date: [YYYY-MM-DD HH:MM:SS]
Committer: [name]
Date: [YYYY-MM-DD HH:MM:SS]
Message: [commit message]
```

### View in VS Code
- Source Control panel → click any commit in history
- Hover over author/date in the timeline gutter

### View on GitHub.com
- Repository → "Commits" tab → click commit hash
- Shows author, committer, both dates, and full message

- Record commit metadata in `.ai-activity/ai-logs/interactions.md` for session backups

---

See also: [kilo-code.md](../ai-dev-tools/kilo-code.md) | [ai-transparency.md](../ai-dev-guides/ai-transparency.md) | [skills-guide.md](../ai-dev-guides/skills-guide.md)
