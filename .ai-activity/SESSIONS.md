# AI Activity Log

## Sessions

### Session: Project review and inconsistency audit

**Task:** Review project state, update AI transparency logs, and identify inconsistencies across todo files, guides, skills, and documentation.

**Outcome:** All checks pass. Identified T-number, phase, path, encoding, email, and version inconsistencies across project files. Fixes planned and executed.

---

### Session: commit0-familytree folder structure and file copy

**Task:** Create the commit0-familytree folder structure, copy all family tree HTML files from src-prep-last/html/ to src-preps/commit0-familytree/src-content/familytrees/[name]/index.html, create credits.html, and update internal links.

**Files Modified/Created:**

| File | Action | Details |
|------|--------|---------|
| src-preps/commit0-familytree/src-content/familytrees/index.html | Created | Copied from src-prep-last/html/familytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/bailey/index.html | Created | Copied from baileyfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/clark_unwin/index.html | Created | Copied from clark_unwinfamilytrees.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/cockin/index.html | Created | Copied from cockinfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/coles/index.html | Created | Copied from colesfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/fletcher/index.html | Created | Copied from fletcherfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/giles/index.html | Created | Copied from gilesfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/handley/index.html | Created | Copied from handleyfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/hankin/index.html | Created | Copied from hankinfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/holt/index.html | Created | Copied from holtfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/hone/index.html | Created | Copied from honefamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/jacobsohn_cohen/index.html | Created | Copied from jacobsohn_cohenfamilytrees.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/letters/index.html | Created | Copied from lettersfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/roberts/index.html | Created | Copied from robertsfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/simmonds/index.html | Created | Copied from simmondsfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/smith/index.html | Created | Copied from smithfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/soul/index.html | Created | Copied from soulfamilytree.html; links updated; credits link manually added (source uses lowercase </body>) |
| src-preps/commit0-familytree/src-content/familytrees/wilson/index.html | Created | Copied from wilsonfamilytree.html; links updated |
| src-preps/commit0-familytree/src-content/familytrees/credits.html | Created | New file with credits content, contact info, and back-to-index link |

**Decisions/Notes:**

- All `../html/[filename]` links in family tree HTML files replace with `../[subfolder]/index.html` according to the mapping provided.
- `../html/familytree.html` replaces with `../index.html` (both in subdirectory files and the index file itself).
- The `../html/letters.html` link in index.html remains unchanged as it is not a family tree file (not in scope).
- Credits link `<p><a href="../credits.html">Credits</a></p>` adds before `</BODY>`/`</body>` in each family tree file.

**Sources Consulted:**

| Source | Type | Reliability |
|--------|------|-------------|
| src-prep-last/html/*.html | Local source files | High |
