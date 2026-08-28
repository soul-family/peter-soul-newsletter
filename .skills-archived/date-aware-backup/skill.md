> **Archived**: This skill was used for v1 backup preparation and is preserved for historical reference. The v1 migration is complete.

# Date-Aware GitHub Backup Skill

## Goal
Back up local files to GitHub using backdated Git commits reflecting original publish/update dates rather than corrupted filesystem timestamps.

## When to Use
- Fresh git repo with existing source files
- Filesystem dates are unreliable (e.g., archive extraction reset CreationTime)
- Blog posts encode publish dates in filenames
- User wants chronological Git history matching original content dates

## Prerequisites
- Git repository initialized
- Source files available in a content directory
- Git available in PATH

## Migration Process

### Goal
Move a static website archive to GitHub with backdated Git commits matching original publish dates, using preparation folders for review.

### Workflow
1. **Map dates** — classify files and derive candidate commit dates
2. **Build prep folders** — create `src-preps/commit0/` to `commitN/` with files staged per commit
3. **Verify** — check prep folder structure, duplicates, and date anomalies
4. **Review** — user inspects prep folders
5. **Commit** — execute backdated commits in chronological order
6. **Push** — push to origin

### Output Structure
- `commit0/` — README, LICENSE, `.version`
- `commit1/` — `src-content/` containing non-blog pages in `content/`, first blog post in `content/columns/`, referenced assets, root files
- `commit2..N/` — `src-content/` containing remaining blog posts in `content/columns/` in chronological order

### Asset Deduplication
- Assets already present in a previous commit folder do not copy again into later commits.
- Each commit only contains the new assets referenced by its files that do not already commit.

### Encoding Preservation
- Author text preserve exactly as published.
- Only link paths rewrite for the new folder structure; grammar, wording, and characters remain untouched.
- Source files read with encoding fallback: UTF-8 → cp1252 → latin-1 → iso-8859-1.

### Commit Date Rules
- Blog posts: `YYYY-MM-01 13:00:00` from filename; if two posts in one month, use day 1 and day 15 at 13:00
- Individual pages: batch upload date, overridden by filesystem mtime if newer
- HTML annotation: append `<!-- Latest Updated on: YYYY-MM-DD -->` at end of visible content

## Date Derivation Rules

### Blog Posts
- Filename pattern: `month_YYYY.html` or `monthYYYY.html`
- Publish date = `YYYY-MM-01 13:00:00` (local time, 1pm)
- Month names: january–december (case-insensitive)
- **Multiple posts per month**: If a month contains two blog posts, assign the first to day 1 at 13:00 and the second to day 15 at 13:00.

### Individual Pages
- No date in filename
- Base candidate date = detect batch upload date
- Batch upload date = most common `LastWriteTime` date among individual files, within a 10-minute window
- If no cluster find, use content root folder mtime as proxy
- **Dating rules**:
  - If a non-blog file references in a blog post, its candidate date follows the blog post's publish date.
  - Newly added asset files inherit the date of the file they reference from.
  - Non-blog files not referenced from any blog post get the date of the first blog post.
  - At later commits, if a non-blog file's filesystem modification date is newer than its current candidate date, update its candidate date to the filesystem modification date when that commit reaches.
- **HTML annotation**: Append a "Latest Updated on: YYYY-MM-DD" line at the end of the visible content of each HTML file.

### Override Rule
- `candidate_date = max(initial_candidate, LastWriteTime)` for individual pages only
- Blog post dates derive from filenames and do not override by filesystem timestamps

## Algorithm

1. **Classify**: `IS_BLOG` if filename matches month+year pattern, else `INDIVIDUAL`
2. **Parse blog dates**: extract year/month, default day=1, time=13:00:00
3. **Detect batch date**: histogram of mtimes among INDIVIDUAL files, largest cluster within 10-min window
4. **Set individual candidate**: = batch date
5. **Cross-reference links** *(optional)*: scan blog HTML for `<a href>` to individual pages; if linked blog date > current candidate, update candidate
6. **Apply mtime override**: `candidate_date = max(candidate_date, LastWriteTime)` for individual pages only
7. **Commit**:
   - Sort files by `candidate_date` ascending
   - Group files sharing the same date
   - For each group:
     ```
     GIT_AUTHOR_DATE="<candidate_date>" GIT_COMMITTER_DATE="<candidate_date>" git commit -m "Backup: <date>"
     ```

## Preparation Folder Structure
- `commit0/` — README and LICENSE
- `commit1/` — `src-content/` with Non-blog pages in `content/`, first blog post in `content/columns/`, referenced assets, root files
- `commit2..N/` — `src-content/` with Remaining blog posts in `content/columns/` in chronological order

## Commit Strategy

### Commit 0 — Repository Metadata
- **Content**: README, LICENSE
- **Date**: Today
- **Message**: "Initial commit: README and license"
- **Rationale**: License and attribution must exist before content is added.

### Commit 1 — Initial Content (Non-Blog Pages + First Blog Post + Referenced Assets)
- **Content**: Non-blog pages in `src-content/content/`, first blog post in `src-content/content/columns/`, referenced assets, root files
- **Date**: First blog post publish date = `YYYY-MM-01 13:00:00` (1st of month at 1pm)
- **Rule**:
  - Blog post date comes from filename, not filesystem mtime.
  - All other files in this commit get the blog post date if the new file references in the blog post. All newly added asset file date follows the file referenced from. Non-blog files if not referenced from a blog post and there is no parent post, then add date of the first blog post. At later stage if non-blog files have newer modification date, then when commits reach the modification date then touch those file to mark the date.
  - As an additional content to each html file add the Latest Updated on date line at the end of the visible content.
  - Assets already present in this commit do not duplicate in later commits.
- **Message**: "Backup: YYYY-MM-DD"

### Commits 2..N — Blog Progression
- **Content**: Remaining blog posts in `src-content/content/columns/` in chronological order, plus any newly referenced files not present in earlier commits.
- **Date**: Blog post publish date (from filename), default `YYYY-MM-01 13:00:00`. If two posts in the same month, use `YYYY-MM-01 13:00:00` for the first and `YYYY-MM-15 13:00:00` for the second.
- **Rule**: Only include assets not already present in previous commits.
- **Message**: "Backup: YYYY-MM-DD"

### Final Commits — Recent Edits
- Any files whose `LastWriteTime` is newer than their candidate date get their mtime as commit date.
- These may batch into one "recent updates" commit or keep separate.

## Git Strategy

```powershell
# Stage all
git add .

# Unstage all (we will re-stage in date order)
git reset HEAD

# Sort files by candidate_date, then for each unique date:
$date = <candidate_date>
$files = <files with this date>
git add $files
$env:GIT_AUTHOR_DATE = $date.ToString("yyyy-MM-dd HH:mm:ss")
$env:GIT_COMMITTER_DATE = $date.ToString("yyyy-MM-dd HH:mm:ss")
git commit -m "Backup: $date"
```

## Validation
- `git log --pretty=fuller` show earliest commits ~2002, latest ~current year
- No individual-page commit date < detect batch upload date
- Blog commit dates match filename month/year
- Each HTML file contain a "Latest Updated on: YYYY-MM-DD" line at the end of visible content
- Spot-check 3–5 files against known history

## Edge Cases
- **Future mtimes**: Flag in dry-run; commit as-is if requested
- **Duplicate dates**: One commit per date, group all files
- **Time zones**: Use local filesystem time; Git stores as-is
- **Exact day/time**: If FTP/hosting details available, compare remote mtime; otherwise day=1 13:00 fallback
