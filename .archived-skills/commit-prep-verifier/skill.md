> **Archived**: This skill was used for v1 backup preparation and is preserved for historical reference. The v1 migration is complete.

# Commit Prep Verifier Skill

## Goal
Verify that preparation folders have correct structure, contain the right files, and that file dates (Created, Modified, Accessed) properly set before migration to Git.

## When to Use
- After populating preparation commit folders
- Before executing the Git migration
- When user asks to "review the prep folders"

## Prerequisites
- Preparation directory exists with numbered commit subfolders
- Python 3 available

## Verification Steps

### 1. Structure Check
- The first commit folder must contain README and LICENSE files.
- Subsequent commit folders contain only files that should add in that commit.
- No file appears in more than one commit folder.
- All paths inside prep folders match the final content structure.

### 2. Date Validation
For every file in every prep folder:
- **Created** ≤ **Modified** (filesystem constraint)
- **Modified** ≥ batch upload date (if individual page) or ≥ filename-derived month (if blog)
- **Modified** ≤ today (no future dates unless explicitly flagged)
- If a reference folder exists, compare each file against its counterpart there:
  - Content must match exactly
  - **Modified** in prep folder ≤ **Modified** in reference folder (prep should not be newer than final)

### 3. Content Check
- Blog HTML contain valid links if individual pages reference
- No broken relative links (optional: crawl all links and verify target exists in some commit)
- README mention: original website, author, site URL, license type

### 4. Dry-Run Report
Generate a table:

| Commit | Files | Date Range | Issues |
|--------|-------|------------|--------|
| commit0 | README and LICENSE | N/A | — |
| commit1 | index.html, assets/... | 2002-07-01 | None |
| ... | ... | ... | ... |

## Verification Script

Run the pre-commit audit tool to verify preparation folder structure, file dates, and completeness before migration.

## Common Issues
- **Future dates**: File **Modified** > today — ask user if intentional
- **Missing README**: First commit folder lacks README
- **Duplicate files**: Same file in multiple commit folders
- **Date inversion**: **Created** > **Modified** (expected after archive extraction; treat as warning)
