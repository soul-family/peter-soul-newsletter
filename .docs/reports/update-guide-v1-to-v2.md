# Update Guide v1 to v2

## Overview

This document describes the full migration process from local backup to GitHub with backdated Git commits, organized in versioned phases. The migration begins with the v1.0.0 backup and includes extensive preparation: consultation, GitHub setup, VS setup, tools, AI setup, AI interactions, task tracking, date backdating, privacy cleanup, and index preparation. Task tracking follows `.docs/contribution-guides/task-management.md`.

## Current State

As of the latest work, the following complete:

- **v1.0.0 backup**: Original content preserve with backdated Git timestamps
- **v1.1.0 compatibility**: Doctype update and path restructuring
- **v2.1.0 archive separation & privacy**: Family trees separate, emails remove, meta dates backdate, progressive index pages create
- **v2.2.0 link management & documentation**: Shared link utilities create and test, URL references fix across all prep commits, guides reorganize into topic folders, personal data checks add to audit
- **Prep folders**: 167 column commits (`commit1` to `commit167`) plus `commit0-familytree`
- **Metadata**: All files and folders backdate to blog post creation dates (created, modified, accessed)
- **Index pages**: Each commit's `content/columns/index.html` and `content/index.html` list only posts available at that commit date

## v1.0.0 Backup Notes

### Commit Preparation Process
The commit preparation process involves creating sequential staging folders (`commit0`, `commit1`, etc.) in `src-preps/`, where each folder contains only the files added in that commit. File and directory metadata (created, modified, accessed) is backdated to each blog post's publication date. Prep folders are verified before migration to ensure completeness and correct dates.

### Known Issues and Lessons Learned
- **Missed links**: After restructuring `html/` to `content/` and `content/columns/`, some internal links were missed during the path rewrite. Progressive index pages were created to address navigation gaps.
- **Farewell text**: The farewell text from the final historical blog post was removed from intermediate commits and only preserved in the last commit to avoid appearing in earlier snapshots.
- **Family tree separation**: Family tree content was separated from newsletter columns data into `commit0-familytree` for independent migration to a dedicated repository.

## Prerequisites

- Git installed and configured
- GitHub repository created
- `.skills/date-aware-backup/skill.md` skill available

## Migration Phases

### Phase 1: Consulting

- Define archive purpose, audience, and success criteria, and archive preservation boundaries.
- Guide and create Github organisation for Soul Family with family tree, petersoul, documents repositories.

### Phase 2: Planning

- Establish project milestones and delivery timeline.
- Document transition and preservation decisions.
- Capture AI planning decisions, AI agent instruction structure, and AI skill file separation.
- Move AI skill definitions out of page content into a dedicated `.skills` folder.
- Create a recovery plan for archive updates and future review cycles.
- Incorporate AI-assisted planning for task breakdown and estimations.
  - Define AI transparency and logging requirements for decisions made or suggested by AI.
  - Track tools used for git history management, including `git filter` and [git-filter-repo](https://github.com/newren/git-filter-repo/) for history rewriting.
  - Establish task management, changelog practices, and roles for AI-assisted implementation.
- Preserve AI interactivity and generated code as part of archive provenance.

### Phase 3: Skills & Tools

- Review and update `.ai-activity` files to reflect maximum AI usage and transparency for this project.
- Create a `.skills` folder, move AI skill definitions out of archive pages, and preserve the skill part in `.skills` instead of page content.
- Add an AI verification skill that checks commit-prep folders, file metadata properties (`created`, `modified`, `accepted`), and preparation completeness.
- Preserve every intermediate Python scripts code file created during planning and implementation.
- Create an AI agent instruction file for AI guidance and reproducible task execution.
- Preserve AI planning notes and AI-generated implementation code as archive artifacts.

### Phase 4: File & Folder Planning

- Research static site generation and archive deployment strategies.
- Research repository snapshot and migration workflows.
- Build a local archive site that can be inspected, deployed, and run offline.
- Generate a sitemap for archive discovery.
- Add schema metadata, authorship markup, and search preview metadata.
- Add social sharing compatibility support and sharing metadata.
- Track archive versions with clear tags and release notes.
- Define URL routing, redirects, and canonical links for archived pages.
- Establish Git backup, tagging, and release workflow.


### Phase 5: v1 Migration

- Fix progressive index pages encoding and filtering for all prep commits.

- Create deployment checklists for local preview and production publishing.
- Use AI tools to assist implementation, with clear human review steps.
- Add AI transparency logging for generated code, decisions, and prompts.
- Adopt open-source-friendly workflows and document licensing.
- Integrate tooling and automation to speed implementation while tracking changes.
- Define git migration preparation folders under `src-preps/`, with subfolders for each commit (`commit0`, `commit1`, ...), including files added or changed per commit.
- Create `commit0` prep containing README and a CC licence file that allows non-commercial sharing with attribution.
- Identify the initial blog post and align the initial commit date for `src` files, referenced non-blog pages, images, never-referenced `src` pages, and blog archive links to the date of the initial blog post.
- Read `src-prep-last` folder to verify final content version and compare with commit preparations.
- Plan commit sequence for blog posts, starting with initial blog archive content and then adding subsequent posts plus newly referenced non-blog files and assets.
- Ensure all blog posts have publishing dates and that each commit includes the blog post content, updated blog archive file, and any newly referenced assets.


### Phase 6: Execution

- Update archive to HTML5 doctype and modern markup standards.
- Introduce PHP template includes for shared header and footer to deduplicate HTML across pages.
- Create page-type templates: one for static pages, one for blog posts.
- Add per-page template details support (page background image, sidebar image assets, etc.).
- Preserve original table structure and HTML layout in rendered output.
- Update contact page to remove original author email and add archive contact link.
- Remove `a_pscouk.gif` asset and all references from content and scripts.
- Rebuild prep folders with updated `src-content/` structure and encoding fixes.

- Create developer guidance for rebuilding and migrating the archive.
- Create user guidance for navigating and using the archived site.
- Document repository structure, naming conventions, and content ownership.
- Document known issues, omissions, and archive completeness.
- Add license, copyright, terms, privacy, and attribution documentation.

## Documentation

Developer guides (`.docs/dev-guides/`) cover consultation, migration, task management, and technical decisions. Browsing guides (`.docs/archive-guides/`) cover visitor-facing archive usage.

## Repository Structure

This project is organized as two separate public archives:

- **Blog columns archive** — Peter Soul's motoring and physics columns (2002–2019)
- **Family tree archive** — Compiled family trees by Brendan Soul and Peter Soul, to be migrated to a dedicated repository

Each archive has its own repository, task tracking, and documentation.

## Version History

### v1.0.0 — Original Backup
- First commit with README, LICENSE, and `.version` file
- All content committed with backdated Git timestamps
- File paths restructured to `content/` and `content/columns/`
- Links rewritten to relative paths for viewability
- Author text and encoding preserved exactly as published
- HTML files annotated with `<!-- Latest Updated on: YYYY-MM-DD -->`
- Browser search function (Ctrl+F or Cmd+F) available for finding names, dates, or topics within any page

### v1.1.0 — Compatibility update
- Doctype update and code consolidation
- All original content, encoding, grammar, and wording intact
- Only file paths and links updated for viewability
- No visible changes to content or layout

### v1.5.0 — Template Modernization
- HTML5 doctype and modern markup standards
- PHP template includes for shared header and footer
- Page-type templates for static pages and blog posts
- Contact page updated with archive contact link
- Original email asset removed

### v2.0.0 — Modernization
- Built on extensive v1 preparation: consultation, GitHub setup, VS setup, tools, AI setup, and interactions
- Internal markup and assets modernized
- User-facing view and style remain identical to v1.1.0
- Some visible changes to content or layout to adapt for the viewers screen sizes and easier navigation.

### v2.1.0 — Archive Separation & Privacy
- Family trees separated into `commit0-familytree` with per-tree folders and shared `credits.html`
- All plaintext email addresses removed from HTML; contact pages use obfuscated format `name [at] something [dot] com`
- Living individuals' data marked private; details stored separately and only released to verified family members or serious research requests
- `notes.html` removed from archive
- Google search forms removed as external dependency
- Family tree index links updated to trailing-slash URLs (`branch/xxx/`)
- All prep commit file and directory meta dates set to corresponding blog post creation dates
- Columns index pages progressively list posts available at each commit date

### v2.2.0 — Index Preparation
- Progressive index pages created for all prep commits
- Each commit's `content/columns/index.html` and `content/index.html` list only posts available at that commit date
- Restored Windows-1252 byte encoding while preserving ISO-8859-1 charset declarations
- Fixed year header filtering to remove orphaned year sections with no posts
- Script: `.dev-scripts/scripts/fix_index_pages.py`

## Folder Structure

```
src-preps/
├── commit0/
│   ├── README.md
│   ├── LICENSE
│   └── .version
├── commit1/
│   └── src-content/
│       ├── content/
│       │   ├── info.html
│       │   └── ...
│       ├── content/columns/
│       │   ├── index.html
│       │   └── july_2002.html
│       ├── assets/
│       └── .htaccess
├── commit2/
│   └── src-content/
│       └── content/columns/
│           └── september_2002.html
...
```

## Commit Dates

- Blog posts: `YYYY-MM-01 13:00:00` from filename
- Two posts in one month: day 1 and day 15 at 13:00
- Individual pages: batch upload date, overridden by mtime if newer

### Metadata Date Backdating

All files and folders inside each `src-preps/commitN` folder are backdated to the blog post date contained in that commit, including the `assets/` folder and all inner folders such as `assets/images/autogen/`. This ensures consistent archival timestamps across the entire commit.

**Three timestamps set:**
- **Date created** (creation time)
- **Date modified** (modification time)
- **Date accessed** (access time)

**Windows NTFS note:** On Windows, NTFS may reset the access time when files are read by system tools. To preserve the backdated access times for archival purposes, disable last-access updates system-wide before running the date update script:

```powershell
# Run PowerShell as Administrator
fsutil behavior set disablelastaccess 1
```

**Script:** `.dev-scripts/scripts/update_commit_dates.py` sets all three timestamps using the Windows API (`SetFileTime`) on Windows, and `os.utime()` on other platforms.

## Output

- Git history spanning 2002–2026
- Backdated commits matching original publish dates
- HTML files annotated with latest update dates
