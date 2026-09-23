# Markdown Links and GitHub Pages

## The `.md` Link Convention

All internal links in the markdown source files use `.md` extensions in their paths. For example:

```markdown
[Title](./2002/07/eyes-in-the-dark.md)
```

**Do NOT** convert these to directory-style URLs (e.g., `./2002/07/eyes-in-the-dark/`) in the source files. The public website handles the conversion automatically.

## How Links Work on the Public Site

1. Jekyll builds the site with `permalink: pretty`, generating each page at `/path/to/page/index.html`
2. The GitHub Actions workflow (`.github/workflows/pages.yml`) runs a post-processing step that converts `.md` links in the generated HTML to directory URLs with trailing slashes:
   - `.md"` → `/"`  (double-quoted href attributes)
   - `.md'` → `/'`  (single-quoted href attributes)
3. This turns `href="./2002/07/eyes-in-the-dark.md"` into `href="./2002/07/eyes-in-the-dark/"`, which correctly resolves to the generated `index.html`

## External Links

External links (e.g., `https://creativecommons.org/licenses/by-nc-sa/4.0/`) must keep their original URL format. The sed post-processing only converts `.md` followed by a quote character (`"` or `'`), so external URLs ending in `/` or other characters are unaffected.

## Navigation Files

The sidebar navigation is controlled by `_includes/sidebar.md`, which uses root-relative URLs.