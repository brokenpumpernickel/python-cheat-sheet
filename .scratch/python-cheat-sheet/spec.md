Status: ready-for-agent

# Spec: Python Cheat Sheet for the stats lab

## Problem Statement

Students in the statistics & probability lab finished an introductory programming course, but while working in Jupyter they keep forgetting the basics: how to slice a list, how a dictionary lookup fails, how to format a p-value in an f-string. Existing references are either too long (official docs, tutorials) or too flat (a single scrolling page that turns into a wall of text as more libraries are added). Students need a quick, good-looking refresher they can keep open in a side tab, find things in within seconds, read in English or Polish, and trust: every example must really run and show what it really prints.

The Author (the teacher, often working through AI agents) needs to grow the cheat sheet over time, with NumPy, pandas, Matplotlib and SciPy stats to come, without hand-editing layout, hand-copying outputs or managing plot images, and without agents being able to break the site or publish wrong outputs.

## Solution

A single-page static website, hosted on GitHub Pages, that works like a map:

- The **Overview** shows every **Area** and its **Topics** at a glance, in one of two arrangements the Student can switch between: the **Map** (default; one round island per Area with Topic bubbles on it) or the **Trail** (a winding path through the Topics in **Topic order**, numbered, one stretch per Area).
- Clicking a Topic plays a short **semantic zoom** into that Topic's page (ADR 0001). The Topic page shows its **Entries** as two-column cards. Each card has a title, a short explanation, a self-contained code example, its **Output**, an optional **Pitfall**, and See-also links. The page ends with "Previous stop / Next stop".
- Inside a Topic, the Overview shrinks into a side rail that acts as the **Index**. It shows mini islands (in Map mode) or a mini-trail (in Trail mode), marks "you are here", and expands the current Topic's Entries, highlighting the one being read.
- Search (Ctrl+K or `/`) covers titles, explanations and code in both Languages and zooms straight to the chosen Entry. Every Topic and Entry has a stable shareable link, the browser's Back button and Esc zoom out, and everything is usable by keyboard.
- An **EN | PL** switch changes the **Language** of all prose. Code and Outputs are shared by both Languages (ADR 0005).
- Outputs and figures are never typed by hand: the build runs every example in a Jupyter kernel with pinned library versions and captures what it prints or plots (ADR 0002). A broken example, a missing translation or a malformed Entry fails the build.

The UI direction was chosen through prototyping: variant **C4** ("Islands: map + trail") plus the Language switch. See Further Notes.

## User Stories

### Finding things

1. As a Student, I want to see every Area and Topic on one screen, so that I can orient myself without reading a table of contents.
2. As a Student, I want the Map to show each Area as an island with its Topics as labelled bubbles with a recognisable glyph (`[ ]`, `{k:v}`, `def`…), so that I can spot the Topic I need visually.
3. As a Student, I want to switch the Overview to a Trail that shows the Topics in a numbered learning order, so that I can revise in a sensible sequence.
4. As a Student, I want the site to remember whether I prefer the Map or the Trail, so that I don't have to switch every visit.
5. As a Student, I want the Map to be what I see the first time, so that I start from the at-a-glance picture.
6. As a Student, I want clicking a Topic to zoom smoothly into its page, so that I keep a sense of where I am on the map.
7. As a Student, I want a search box I can open with Ctrl+K or `/`, so that I can find "slicing" or "KeyError" without knowing which Topic it's in.
8. As a Student, I want search to match words inside code examples too (e.g. `.get(`), so that I can find an Entry by the function I half-remember.
9. As a Student, I want search to find matches in both English and Polish whichever Language is active, so that typing "słownik" or "dictionary" both work.
10. As a Student, I want to pick a search result with the arrow keys and Enter, so that I never have to reach for the mouse.
11. As a Student, I want choosing a search result to take me straight to that Entry, highlighted briefly, so that I see immediately which part answers my question.
12. As a Student, I want an Index rail beside the Topic page that shows all Areas and Topics and marks where I am, so that I can jump sideways without going back to the Overview.
13. As a Student, I want the rail to list the current Topic's Entries and highlight the one I'm reading as I scroll, so that I can jump within a long Topic.
14. As a Student, I want chips at the top of a Topic page listing its Entries, so that I can jump to one even on a phone, where the rail is reduced.
15. As a Student, I want "Previous stop / Next stop" at the end of every Topic page, so that I can keep revising in Topic order without going back to the Overview.
16. As a Student, I want See-also links between related Entries (e.g. Sorting → lambda), so that I can follow a concept across Topics.

### Reading an Entry

17. As a Student, I want every Entry to have a short explanation of one to three sentences, so that I get the idea without reading a tutorial.
18. As a Student, I want every code example to include its own imports and setup, so that I can paste it into a Jupyter cell and it just runs (ADR 0003).
19. As a Student, I want to see the real Output under each example, so that I know what to expect when I run it.
20. As a Student, I want plots to appear as the actual figure the code produces, so that I can recognise what I'm aiming for.
21. As a Student, I want Pitfalls highlighted as a "Watch out!" callout, sometimes with a small example showing the mistake and its real error, so that I learn the mistakes I'm likely to make.
22. As a Student, I want examples that demonstrate an error to show the error line (e.g. `KeyError: 'sd'`), so that I recognise it when it happens to me.
23. As a Student, I want a copy button on every code block, so that I can move an example into my notebook in one click.
24. As a Student, I want syntax-highlighted code in a monospaced font, so that it reads like it does in my editor.
25. As a Student, I want to see which Python and library versions the examples were run with, so that I understand differences on my machine.

### Language

26. As a Student, I want an EN | PL switch in the top bar, so that I can read explanations in the language I'm most comfortable with.
27. As a Student, I want the switch to change the text in place, keeping my Topic and scroll position, so that switching never loses my place.
28. As a Student, I want my Language choice remembered, so that the site opens in Polish next time if that's what I chose.
29. As a Student, I want Polish text to name Python concepts in Polish with the English term in parentheses at the first mention (e.g. "krotka (tuple)"), so that I can connect them to the English I see in errors and documentation.
30. As a Student, I want every page to be fully translated whenever I choose Polish, so that I never land on a half-English page.
31. As an Author, I want to share a link that opens in Polish (`?lang=pl`), so that I can put it in lab instructions for Polish-speaking groups.
32. As a Student, I want links to be the same in both Languages, so that a link from a classmate works regardless of their setting.

### Links, keyboard, accessibility, devices

33. As an Author, I want every Topic and every Entry to have a stable link (e.g. `#lists/slicing`), so that I can reference exactly the right Entry in lab instructions.
34. As a Student, I want opening such a link to land directly on the Entry without a zoom animation, so that a shared link is instant.
35. As a Student, I want the browser's Back button and Esc to zoom back out, so that navigation behaves the way I expect.
36. As a Student, I want to Tab through Topics, press Enter to zoom in and Esc to zoom out, so that I can use the site without a mouse.
37. As a Student who has reduced motion turned on, I want zoom animations replaced by instant transitions, so that the site doesn't make me uncomfortable.
38. As a Student, I want the site to follow my system's light or dark mode, so that it matches my editor and isn't blinding at night.
39. As a Student, I want the site to be comfortable on a laptop next to Jupyter, and usable on my phone, so that I can check something on the go.
40. As a Student, I want the site to load fast and work without an account, so that it's quicker than searching the web.

### Authoring and maintenance

41. As an Author, I want each Topic to be a single plain-text Markdown file, with English and Polish side by side, so that I (or an agent) can review and edit it easily.
42. As an Author, I want to add a new Topic by creating one file and listing it in its Area's Topic order, so that extending the sheet needs no layout work.
43. As an Author, I want to add a new Area (e.g. NumPy) by creating an Area description with its title, blurb, colour and Topic order, so that the Map and Trail lay it out automatically.
44. As an Author, I want to mark Areas or Topics as planned, so that Students can see what's coming without dead links.
45. As an Author, I want the build to run every example and capture its Output and figures, so that I never type an Output or manage an image file.
46. As an Author, I want to mark an example as expected to raise a specific error, so that I can show mistakes on purpose, while any other error still fails the build.
47. As an Author, I want the build to fail with a clear message naming the Topic and Entry when an example breaks, a translation is missing, a See-also link points nowhere or an Entry is malformed, so that agents can't publish broken content.
48. As an Author, I want a written authoring guide that agents follow (Entry anatomy, tone, length, Pitfalls, the Polish terminology rule, Topic order rule), so that agent-written content is consistent.
49. As an Author, I want library versions pinned with uv and shown on the site, so that Outputs don't silently change between builds.
50. As an Author, I want pushing to the main branch to rebuild and publish the site automatically, so that publishing is one step.
51. As an Author, I want a single local command that builds the site and a preview server to look at it, so that I can check content before publishing.
52. As an Author, I want to review a title-only list of Entries per Topic before full content is written, so that I control what goes in.

## Implementation Decisions

### Architecture (ADR 0002, ADR 0004)

- Two stages, one build command:
  1. **Content build (Python, run with uv)**: reads the content folder (Area descriptions and Topic files), parses and validates it, executes every code example, and writes one generated content data document plus figure files. This stage is the only parser of the Markdown content. Nothing else reads the raw files.
  2. **Site build (Astro)**: loads the generated content data through a typed schema (a second safety net), renders the single static page, and adds a small client-side layer for zoom, routing, Index, search and Language.
- The site is fully static, with no server, database or accounts. It is deployed to GitHub Pages by a GitHub Actions workflow that installs uv and Node, runs both stages, and publishes. Setting up the GitHub repository and enabling Pages is a human step.
- Python, its version and all libraries examples use (NumPy, Matplotlib now; pandas and SciPy later) are pinned in the uv project. The footer shows the actual versions, read from the installed packages at build time.

### Content model

- **Area description** (one per Area): id, title and blurb in English and Polish, a hue for its colour, its **Topic order** (an ordered list of Topic ids, including planned Topics), and whether the whole Area is planned. Areas themselves are ordered in one top-level list.
- **Topic file** (one Markdown file per Topic): id (from the file name), title, summary and glyph, plus Polish title and summary, followed by its Entries in reading order.
- **Entry** (a level-2 section in a Topic file): English title and explanation, Polish title and explanation, exactly one Python code example, an optional expected-error marker naming the exception type, an optional Pitfall (English and Polish text, optional code example with its own optional expected-error marker), and optional See-also references (`topic-id/entry-id`). Entry ids come from slugified English titles and must be unique within a Topic.
- **Planned** Areas and Topics have a title (both Languages) and glyph but no Entries. They render faded and aren't clickable.
- The exact Markdown syntax (frontmatter keys, how the Polish text, the Pitfall and the expected-error marker are written) is fixed in the first content-pipeline ticket and documented in the authoring guide. The validator enforces it.
- Shape of the generated content data, from the prototype, trimmed to the decision-rich parts:

  ```
  Area   { id, title, blurb, hue, planned, pl: { title, blurb }, topics: Topic[] }        // topics in Topic order
  Topic  { id, title, summary, glyph, planned, pl: { title, summary }, entries: Entry[] }
  Entry  { id, title, explain, code, raises?, see: ["topic/entry"],
           pitfall?: { text, code?, raises?, output? },
           output: { text, error?, figures: [svg] },
           pl: { title, explain, pitfall? } }
  meta   { versions }
  ```

### Execution of examples

- Every Entry's code (and every Pitfall's code) runs in a **fresh Jupyter kernel**, so Entries can't depend on each other (ADR 0003).
- Captured: stdout as text, figures as SVG (Matplotlib is used non-interactively, and every figure open at `plt.show()` or at the end is captured), and, for an expected error, only the final error line (e.g. `KeyError: 'sd'`).
- The build fails if an example raises when it isn't marked, raises a different exception type than marked, or completes normally despite being marked.
- Examples print explicitly with `print(...)`; the build doesn't rely on Jupyter's display of the last expression, so the code also works as a plain script.

### Validation (all failures stop the build and name the Area/Topic/Entry)

- Missing or empty required fields; more than one code example in an Entry; duplicate Entry ids.
- A missing Polish counterpart for any title, summary, blurb, explanation or Pitfall (ADR 0005).
- See-also references to non-existent Entries; Topic order referencing unknown Topics; Topic files not listed in any Area's Topic order.
- Example execution failures, as above.

### Client behaviour

- **Routing**: hash routes (`#topic` and `#topic/entry`) on a single page. Back/forward follows the hash. Esc goes to the Overview. A route to a planned or unknown Topic shows the Overview.
- **Semantic zoom** (ADR 0001): from the Overview, zooming in scales the Overview toward the clicked tile and fades in the Topic page with the rail sliding in. Zooming out reverses this and returns focus to the tile. Switching between Topics inside the Topic view crossfades. On first load of a deep link there's no animation. With reduced motion there are no animations. Every animation has a timeout fallback, so navigation completes even when the browser isn't painting (background tab). This was a real bug found in the prototype.
- **Map layout**: islands flow and wrap automatically (no hand-placed coordinates). Each island is round, and its bubbles are placed on rings: the first Topic in the centre once an Area has five or more, the rest clockwise from the top, with a second ring beyond about thirteen. The island is sized from the ring radius, so every bubble always fits.
- **Trail layout**: one stretch per Area, Topics as numbered stepping stones swaying left and right along a dotted path, with labels and summaries beside them, plus dots at the left edge that jump to each Area and show which is in view.
- **Overview arrangement**: Map by default. The Map | Trail choice is remembered per visitor and applies both to the Overview and to the rail inside a Topic.
- **Topic page**: coloured header (glyph, Area, title, summary), sticky Entry chips, Entry cards in two columns on wide screens, Pitfall sticker and callout, See-also chips, then Previous/Next stop. These follow Topic order across all non-planned Topics, Area by Area.
- **Index rail**: shown only in the Topic view. Map mode lists Areas as mini islands with Topic pins, Trail mode as a numbered mini-trail. The current Topic is marked "you are here" and expands its Entries, and the Entry in view is highlighted (scroll spy). On narrow screens the rail becomes a horizontally scrolling strip and the Entry list is hidden there.
- **Search**: a pop-up opened by Ctrl/Cmd+K or `/` (unless typing in a field). It searches a build-time index of Topic titles and summaries and Entry titles, explanations and code in both Languages. Every query word must match. Ranking: title prefix > title contains > Topic name > body. Results show the title and the Area › Topic path in the active Language, and choosing one navigates to the Entry and flashes it.
- **Language** (ADR 0005): English by default. The choice is remembered per visitor, and a `?lang=` parameter overrides it and stays in the URL when switching. Switching re-renders in place, keeping the route and scroll position. All interface labels exist in both Languages, and the agreed Polish labels are Wynik (Output), Pułapka (Pitfall), Mapa (Map) and Szlak (Trail). The document's `lang` attribute follows the Language.
- **Look**: the soft "Islands" style from the prototype: pastel sea background, one hue per Area, rounded display headings (Fredoka), readable body text (Nunito), JetBrains Mono for code. Fonts are self-hosted. Light and dark themes follow the system setting. Figures sit on a white card in both themes.
- **Accessibility**: tiles and pins are real links, the toggles are radio groups, visible focus rings everywhere, and focus moves to the Topic page on zoom-in and back to the tile on zoom-out. Copy buttons are labelled in the active Language.

### Authoring

- An authoring guide for agents (linked from the project's agent instructions) covers:
  - the Entry anatomy and length (explanation 1–3 sentences)
  - self-contained examples that print explicitly
  - when to write a Pitfall and when to mark an expected error
  - choosing Topic order (a Topic comes after the Topics its examples rely on, and uses See-also links rather than reordering when an Entry needs a later concept)
  - the Polish terminology rule
  - the glossary vocabulary
- MVP content: the Python Basics Area with nine Topics in this Topic order: Variables, Strings, Conditionals, Lists, Tuples, Dictionaries, Sets, Loops, Functions. The prototype's 29 sample Python Basics Entries (with Polish) are the starting draft. A title-only Entry list per Topic is reviewed by the Author before final content is written.
- The MVP also ships four **planned** Areas, so Students see what's coming and the Map isn't a single island on day one. Each lists planned Topics only:
  - NumPy (Arrays, Indexing, Random, Aggregates)
  - pandas (DataFrames, Selecting, Grouping)
  - Matplotlib (Plotting basics, Scatter plots, Subplots)
  - SciPy stats (Distributions, t-tests, Correlation)

  Their titles need Polish too. The prototype has them: Tablice, Indeksowanie, Losowanie, Agregacje; Ramki danych, Wybieranie, Grupowanie; Podstawy wykresów, Wykresy punktowe, Podwykresy; Rozkłady, Testy t, Korelacja. The Matplotlib figure examples from the prototype are kept out of the MVP and come back with the Matplotlib spec. Figure capture is still covered by the content-build tests.

## Testing Decisions

- Good tests check behaviour that the Author or a Student can observe, never internal functions or markup details. A test should still pass after any refactor that keeps the behaviour.
- **Seam 1: the content build.** Input is a folder of Area descriptions and Topic files. Output is either the generated content data (plus figures) or a list of errors naming their location. Tests use small fixture content folders and check, for example:
  - a valid Topic produces the expected data, with real captured Output
  - a Matplotlib example yields a figure
  - an expected error is captured as its final line
  - an unmarked error, a wrong exception type, or a marked example that doesn't raise each fail
  - missing Polish fails
  - a dangling See-also fails
  - a Topic missing from the Topic order fails
  - Entries can't see each other's variables
  - planned Topics pass with no Entries
- **Seam 2: the built site in a real browser.** The site is built from a small fixture content set and driven through Playwright. Tests check, for example:
  - the Overview shows Areas and Topics
  - the Map/Trail toggle is remembered
  - clicking and keyboard (Tab, Enter, Esc) zoom in and out
  - Back zooms out
  - a deep link lands on the right Entry
  - search finds an Entry by an English word, a Polish word and a code fragment, and navigates to it
  - switching to PL keeps the route and translates the page
  - `?lang=pl` opens in Polish
  - "Next stop" follows Topic order
  - the rail marks the current Topic and expands its Entries
  - with reduced motion emulated, no animations run
- Both seams run under one command with pytest (Playwright's pytest plugin for Seam 2), all managed by uv. CI runs them before publishing.
- There's no prior art in this repository yet. The prototype on the `prototype/ui-mockups` branch is the behavioural reference for Seam 2.

## Out of Scope

- Runnable or editable examples in the browser (e.g. Pyodide).
- A printable or PDF version.
- The glossary of Python **Terms** (definitions such as *iterable* that link to Entries): a later addition.
- Content for NumPy, pandas, Matplotlib and SciPy stats. The MVP shows them only as planned Areas, and their Entries come in later specs.
- Languages other than English and Polish, and a manual light/dark toggle.
- Accounts, analytics, comments, a CMS or any server-side component.
- Offline/installable (PWA) support.
- Setting up the GitHub repository, Pages and any custom domain (a human step, described in the README).

## Further Notes

- **Prototype**: the UI was decided by building throwaway mockups, kept on the `prototype/ui-mockups` branch (`prototype/`, served with `python -m http.server -d prototype`; variant switcher at the bottom, `?variant=C4`). Explored: A "Atlas" (editorial), B "Workbench" (IDE), C "Islands" (literal map), C2 (self-arranging islands + mini-map rail), C3 (Trail), C4 (C2 + Trail toggle). **Verdict: C4**, with ring-laid-out round islands, "Next stop" in both modes, Topic order with Loops after the collections, an EN | PL switch, and the rail expanding the current Topic's Entries. The prototype's code is a reference for behaviour and look, not code to promote. It was written without tests or error handling.
- **Decisions recorded as ADRs**: 0001 semantic zoom instead of a free canvas, 0002 Outputs generated at build time, 0003 self-contained Entries, 0004 Astro plus a Python execution step, 0005 Polish as a second Language.
- **Lessons from the prototype**: links must never be nested (a tile that contains other links breaks the page), and miniature or decorative copies of content must not be focusable.
