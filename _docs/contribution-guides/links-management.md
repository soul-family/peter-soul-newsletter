# Markdown Links and GitHub Pages

## The `.md` Link Convention

All internal links in the markdown source files use `.md` extensions in their paths. For example, a link from one column article to another is written as:

```markdown
[Title](../../../../src-content/columns/2002/07/eyes-in-the-dark.md)
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

The build workflow also adds `target="_blank" rel="noopener noreferrer"` to external links so they open in a new tab. The visible external-link marker is drawn by CSS rather than markup, so no marker character is needed in the source files.

### Keeping External Links Working

Websites move, reorganise, and close. When adding or reviewing a link:

1. Check that the destination still serves the information the column relies on, not just that it returns a successful response.
2. Prefer a replacement that carries the same subject matter, such as the relevant reference article, an official successor site, or the current guidance page.
3. Encode characters that break markdown link syntax, for example `(` and `)` as `%28` and `%29`, so the whole address stays inside the link.
4. Record the destination and its subject in `.ai-activity/ai-logs/sources.md`.
5. List the destination in `src-content/links.md` so readers have a single place to find the references used by the columns.

## Navigation Files

The sidebar navigation is controlled by `_includes/navigation.html`. Most links use the `.md` convention (e.g., `columns.md`, `advanced-driving.md`, `links.md`), which the GitHub Action converts to directory URLs with trailing slashes (`columns/`, `advanced-driving/`, `links/`).

**Exception:** The Home link uses `{{ site.baseurl }}/` (which resolves to `/`) instead of `index.md`, because with `permalink: pretty` the homepage is served at `/` not `/index/`.