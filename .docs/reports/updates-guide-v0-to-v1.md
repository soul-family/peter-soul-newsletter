# Updates Guide v0 to v1

## Overview

Version 1.0.0 is the original website backup committed to GitHub with backdated Git timestamps. File paths are restructured to `content/` and `content/columns/` for viewability, but author text and encoding are preserved exactly as published, including the design.

## Archive Purpose and Boundaries

The archive purpose, audience, and success criteria define during the consulting phase. The archive preserves the original website published by the author between 2002 and 2019. Preservation boundaries validate and document: original author intent respects, and the archive maintains through the author's family.

## GitHub Organisation

A GitHub organisation was setup for the Soul Family with separate repositories for the family tree and the website archive. This provides a structured home for each archive and related materials.

## Preparation for v2

The v1.0.0 backup is not just a simple copy. It involves extensive preparation for the v2 migration:

- **Consultation**: Define archive purpose, audience, and success criteria
- **GitHub setup**: Create organisation, repositories, and access controls
- **VS setup**: Configure development environment and workflows
- **Tools setup**: Establish Python scripts, date mappers, and verification tools
- **AI setup**: Configure AI agent instructions, transparency logging, and skill files
- **AI interactions**: Document planning decisions, generate code, and implementation artifacts
- **Task tracking**: Create todo lists, phase plans, and verification checklists
- **Date backdating**: Set all file and folder meta dates to blog post creation dates
- **Privacy and cleanup**: Remove plaintext emails, add obfuscated contact info, separate family trees
- **Index preparation**: Create progressive column index pages for each commit

All of these tasks track with T-numbers and document in the migration guide.

## What Is Preserved

- Original HTML pages as published, with encoding recover from cp1252/latin-1 where needed
- Images and assets in restructured folder layout
- Author text and design intent — grammar and wording untouched
- Original links rewrite to relative paths for GitHub viewability
- File names and paths map to new structure (`html/` → `content/`, `html/` → `content/columns/`)

## What Changed

- Folder structure: `html/` → `content/` (non-blog) and `content/columns/` (blog posts)
- `links.html` renamed to `content/columns/index.html`
- `index.html` moved from root to `content/index.html`
- All internal links update to relative paths
- HTML files annotate with `<!-- Latest Updated on: YYYY-MM-DD -->`

## Known Limitations

- Filesystem dates were reset by archive extraction; Git history provides accurate chronology
- Original design targeted older screen sizes; modern responsive behavior is planned for v2

## Usage

This backup is tagged `v1.0.0` in Git. To inspect:

```bash
git show v1.0.0:content/columns/july_2002.html
```

Or check out the tag:

```bash
git checkout v1.0.0
```

## License

See licence details in the documentation. 
