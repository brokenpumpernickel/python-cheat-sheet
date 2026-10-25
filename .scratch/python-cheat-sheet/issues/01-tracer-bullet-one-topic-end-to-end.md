# 01: Tracer bullet: one Topic from Markdown to a rendered page

**What to build:** The thinnest complete path through both build stages (ADR 0004). An Author writes one Topic file and one Area description in the content folder. A single local command runs the Python content build, which parses the files, runs each Entry's example in a fresh Jupyter kernel and captures its Output, then writes the generated content data. Astro then renders a bare single page: an Overview listing the Area and its Topic, and that Topic's page with its Entries (title, explanation, code, Output). Hash links (`#topic`, `#topic/entry`) open the Topic page and scroll to the Entry, and Back returns to the Overview. Styling, zoom and other polish come later. This ticket fixes the Markdown syntax for the whole content model, including the Polish text, Pitfall, expected-error marker and See-also, even though most fields are only parsed here, not yet fully checked.

See the spec (`.scratch/python-cheat-sheet/spec.md`): "Content model", "Execution of examples", "Testing Decisions". The look and behaviour reference is the `prototype/ui-mockups` branch, variant C4.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] The Markdown syntax for Area descriptions, Topic files and Entries (both Languages, Pitfall with optional code, expected-error marker, See-also, glyph, planned flag) is decided and written down briefly; the full authoring guide comes in ticket 10.
- [x] One command (run through uv) builds content and site; a second serves the built site locally.
- [x] Each Entry's example runs in its own fresh Jupyter kernel; stdout is captured as its Output, and Entries cannot see each other's variables.
- [x] The generated content data matches the shape in the spec and is loaded by Astro through a typed schema.
- [x] Footer shows the real Python and library versions from the uv environment.
- [x] Test infrastructure for both seams exists and runs with one `uv run pytest`: a content-build test (fixture folder in, data out) and a browser test (Playwright) that opens the built fixture site, follows a Topic link and a deep Entry link, and uses Back.
- [x] The real content folder contains one sample Topic (e.g. Lists, taken from the prototype) so the page is demoable.

## Comments

**Resolved by the tracer bullet.** Notes for the tickets that build on it:

- **Syntax** is in `docs/content-format.md` (Area order in `content/areas.yaml`, one folder per Area with `_area.md`, one file per Topic; the `PL:` pair rule; ` ```python raises=X `; `### Pitfall`; `### See also`; `glyph` and `planned` in frontmatter). Ticket 10 grows it into the authoring guide.
- **Commands:** `uv run cheatsheet build` (content build into `generated/content.json`, then Astro into `site/dist/`; runs `npm ci` first if `site/node_modules` is missing) and `uv run cheatsheet serve`. Tests: `uv run pytest` (needs `uv run playwright install chromium` once).
- **Prose fields** (`explain`, Pitfall `text` and their Polish counterparts) are stored as inline HTML rendered by the content build, so Astro never parses Markdown. Titles, summaries and blurbs are plain text. Search (06) will need a tag-stripped copy.
- **For 03:** the parser already rejects many malformed inputs with a file:line location (missing frontmatter fields or Polish, more than one code block, duplicate Entry ids, a Topic order naming a missing file, a Topic file missing from the Topic order, unknown headings or blocks), and the build already checks `raises=` against what the example does. Only the unmarked-error case has a test. Still missing: dangling See-also references, figure capture (`figures` is always `[]`), and one test per rule. Execution is sequential, about 1.2 s per kernel; running examples in parallel would speed up the MVP content.
- **For 02:** set the Pages base path with `uv run cheatsheet build --base /python-cheat-sheet/`. Node dependencies are locked in `site/package-lock.json`. CI needs `uv run playwright install --with-deps chromium`.
- **For 12:** the Lists sample leaves out the prototype's See-also links to Topics that don't exist yet. Add them back once those Topics land: Sorting → `functions/lambda`, List comprehensions → `loops/for-over-a-collection`.
