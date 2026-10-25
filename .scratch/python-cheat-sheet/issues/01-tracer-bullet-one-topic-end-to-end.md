# 01: Tracer bullet: one Topic from Markdown to a rendered page

**What to build:** The thinnest complete path through both build stages (ADR 0004). An Author writes one Topic file and one Area description in the content folder. A single local command runs the Python content build, which parses the files, runs each Entry's example in a fresh Jupyter kernel and captures its Output, then writes the generated content data. Astro then renders a bare single page: an Overview listing the Area and its Topic, and that Topic's page with its Entries (title, explanation, code, Output). Hash links (`#topic`, `#topic/entry`) open the Topic page and scroll to the Entry, and Back returns to the Overview. Styling, zoom and other polish come later. This ticket fixes the Markdown syntax for the whole content model, including the Polish text, Pitfall, expected-error marker and See-also, even though most fields are only parsed here, not yet fully checked.

See the spec (`.scratch/python-cheat-sheet/spec.md`): "Content model", "Execution of examples", "Testing Decisions". The look and behaviour reference is the `prototype/ui-mockups` branch, variant C4.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] The Markdown syntax for Area descriptions, Topic files and Entries (both Languages, Pitfall with optional code, expected-error marker, See-also, glyph, planned flag) is decided and written down briefly; the full authoring guide comes in ticket 10.
- [ ] One command (run through uv) builds content and site; a second serves the built site locally.
- [ ] Each Entry's example runs in its own fresh Jupyter kernel; stdout is captured as its Output, and Entries cannot see each other's variables.
- [ ] The generated content data matches the shape in the spec and is loaded by Astro through a typed schema.
- [ ] Footer shows the real Python and library versions from the uv environment.
- [ ] Test infrastructure for both seams exists and runs with one `uv run pytest`: a content-build test (fixture folder in, data out) and a browser test (Playwright) that opens the built fixture site, follows a Topic link and a deep Entry link, and uses Back.
- [ ] The real content folder contains one sample Topic (e.g. Lists, taken from the prototype) so the page is demoable.
