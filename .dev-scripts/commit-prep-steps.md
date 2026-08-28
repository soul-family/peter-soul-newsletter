# Commit Preparation Steps

## Determine the backdated commit date:
- Use the first column post date (`2002-07-01 13:00:00`) for initial commits
- For subsequent commits, use the date from `date_map.csv` corresponding to that commit's blog posts
- The commit date must match the earliest blog post date in that commit

## Move the next prep folder's content to root:
- `Move-Item -Path "src-preps\commitN\*" -Destination "." -Force`
- This moves the entire `src-content` folder and any other files from the prep folder into the root
- If `src-content` already exists at root, contents merge
- New or updated files become visible in `git status` as staged changes

## Update file meta date values:
- **Newly staged files**: update created, modified, and accessed dates
- **Existing folders containing new files**: update only modified and accessed dates (NOT created)
- **Existing files already committed**: do NOT update any dates
- Use the backdated commit date from step 1
- Include `LICENSE`, `README.md`, and all newly added/modified files under `src-content/`
- Use pywin32 or ctypes Windows API only for newly created folders if creation time must be updated
- Verify all dates are set correctly before committing

## Stage everything except the prep folders:
- `git add -A`
- `git reset HEAD -- src-preps/`

## Verify staged state:
- `git status --short`
- Staged files show as `A  src-content/...` or modified files
- `src-preps/` remains `?? src-preps/` (untracked)

## Commit with backdated author/date when instructed:
- `GIT_AUTHOR_NAME="Peter Soul" GIT_AUTHOR_EMAIL="vicki.soul+peter.soul@gmail.com" git commit --no-verify --date="YYYY-MM-DD HH:MM:SS" -m "Backup: YYYY-MM-DD (archive backup back-dated; pages written between July 2002 and March 2019)"`
- **Commit message**: one-liner about the committed content, usually the blog column post title
- **Author**: `Peter Soul <vicki.soul+peter.soul@gmail.com>`
- **Date**: backdated to the commit's blog post date from step 1

## Key rules:
- Always move `src-preps\commitN\*` → root `.`
- Never flatten or remove the `src-content` folder at root
- Never stage `src-preps/`
- Always backdate the commit date to match the earliest blog post date in that commit
- Commit message is a one-liner about the committed content, usually the blog column post title
- Only update dates for newly staged files and modified folders
- Never change dates on already-committed files
- Wait for explicit instruction between commits
