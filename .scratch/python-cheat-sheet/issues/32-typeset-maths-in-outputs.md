# 32: Typeset maths in Outputs (SymPy setup)

**What to build:** The SymPy Area (tickets 33–37) shows symbolic results. In Jupyter, `display(expr)` shows them as typeset maths, but the build keeps only printed text, figures and widgets. This ticket installs SymPy and makes the build keep displayed maths, in order with printed text. The site then typesets it with KaTeX at build time. It writes no SymPy content: ticket 33 does that.

Decided with the Author (every recommendation accepted):

- **Setup:**
  - `uv add sympy`, and add it to `EXAMPLE_LIBRARIES` in `cheatsheet/build.py` so the footer shows its version. Commit `uv.lock`, and update the guide's *Libraries* line.
- **How SymPy examples show results** (the convention for tickets 33–37):
  - Every SymPy example starts with `import sympy as sp`, then `sp.init_printing()`, shown, as in the Author's lab notebook.
  - Without `init_printing`, Jupyter typesets a single expression but shows a list (`solve`'s), a dict (`eigenvals`') or a tuple as plain text. With it, all of them come out as LaTeX. This was checked in a real kernel with SymPy 1.14.
  - `display(x)` shows a result as maths. `display` is built into Jupyter, so it needs no import. `print(x)` still gives SymPy's one-line text, for plain values or where the text form is the point.
  - Examples keep "prints explicitly": a bare expression on the last line still shows nothing.
- **The build:**
  - Keep a `display_data` message's `text/latex`, which is SymPy's `$\displaystyle …$`, as maths.
    - Keep the existing rules first: SVG is a figure, and a widget view is a widget.
    - A `display_data` with only `text/plain` (e.g. `display(3)` without `init_printing`) shows as text, as Jupyter does.
    - Ignore `image/png`.
  - **Order:** printed text and displayed maths appear in the Output in the order the code produced them. Today stdout is joined into one string, so the Output data needs a shape that keeps this order. Choose it, update `generated/content.json`'s readers in the site, and keep text-only Outputs looking exactly as they do now.
  - The error line of `raises=` still ends the Output.
  - **Speed:** in a kernel, `sp.init_printing()` also makes a PNG of every result through Matplotlib's mathtext. The first display took about 25 seconds in a test, against the 60-second limit. Stop the kernel from making PNGs without changing the shown code, e.g. leave `image/png` out of the display formatter's active types in `_KERNEL_CONFIG`. Figures are already SVG. Then check that an example with several `display` calls runs in about a second.
- **The site:**
  - Typeset the LaTeX with KaTeX at build time (`katex` from npm, `renderToString`, display mode, output `htmlAndMathml`), so screen readers get MathML. No client-side maths library, and no CDN: bundle KaTeX's CSS and fonts with the site.
  - **Look:**
    - Each displayed result is its own block, left-aligned, in the Output's text colour.
    - It reads well in both themes.
    - A formula wider than the card scrolls inside the Output, as long text does now.
  - **Failure:** if KaTeX can't typeset SymPy's LaTeX, fail the build, naming the Entry and the LaTeX, instead of showing broken maths. Add the message to the guide's Validation rules.
  - **Search:** check what search indexes from Outputs, if anything, and make sure maths doesn't put raw LaTeX or KaTeX markup into it.
- **Docs:**
  - **ADR 0007:** displayed maths is typeset at build time with KaTeX. It records why: the Outputs match what Students see in Jupyter, there is no client-side script, and screen readers get MathML.
  - **The guide:** a *Maths* section under Code example or Output, covering the convention above (when to `display` and when to `print`, and `sp.init_printing()`), with a short example. Add GLOSSARY terms only if a new one is needed.
- **Tests:**
  - A content-build fixture interleaving `print` and `display`: text, then maths, text, maths. Check the order and the LaTeX.
  - A `display` with only `text/plain`.
  - The KaTeX failure, if it can be triggered from a fixture.
  - Site tests:
    - The maths is typeset (MathML present).
    - A wide formula scrolls inside its Output and not the page.
    - axe passes in both themes, like the existing accessibility tests.

**Blocked by:** none.

**Status:** resolved

- [x] SymPy is installed, in `EXAMPLE_LIBRARIES` and the guide's Libraries line, with `uv.lock` committed.
- [x] `display(expr)` after `sp.init_printing()` shows typeset maths in the Output, in order with printed text, and lists, dicts and tuples typeset too.
- [x] Kernels make no PNGs of SymPy results, and a multi-`display` example runs in about a second.
- [x] KaTeX is bundled; the maths has MathML, works in both themes, and wide formulas scroll inside the Output.
- [x] LaTeX that KaTeX can't typeset fails the build with a message in the guide.
- [x] ADR 0007 and the guide's Maths section are written.
- [x] `uv run cheatsheet build` and `uv run pytest` pass, and the existing content's Outputs look unchanged.
- [x] One session and one PR.

## Comments

Resolved in PR PRLINK. SymPy 1.14.0 is installed and listed in the footer, and KaTeX 0.19.1 comes from npm. No SymPy content was written: ticket 33 does that.

Decisions made on the way:

- **The Output data shape:** an Output's `text` string is now `parts`, an ordered list of `{"text": ...}` and `{"maths": <LaTeX>}`. Neighbouring text is joined into one part, each text part loses its last line break, and empty text is dropped. So an Output with text only is one part, and renders as the same single `<pre>` as before. `error`, `figures` and `widgets` are unchanged, and the error line still ends the Output.
- **The LaTeX kept** is SymPy's `text/latex` without the `$` around it, e.g. `\displaystyle x^{2} + 2 x + 1`. `\displaystyle` is kept; KaTeX's display mode makes it a no-op.
- **Which display is what:** SVG is a figure, then a widget view is a widget, then `text/latex` is maths. A `display_data` whose only formats are `text/plain` (and `image/png`) is text. Anything else, such as `display(df)`'s HTML, is still dropped, as before. The guide says not to `display` tables.
- **No PNGs:** `c.PNGFormatter.enabled = False` in `_KERNEL_CONFIG`. Figures were already SVG, so nothing else used PNGs. A test checks that a SymPy result is formatted as `text/latex` and `text/plain` only. An example with five `display` calls went from 10.4 s to 1.5 s, kernel start included.
- **The KaTeX check** runs where KaTeX is, in the Astro build. `loadContent` typesets every maths part once, before anything renders, and collects the failures. Each starts with `Content error: <file> (topic/entry)[ Pitfall]: KaTeX can't typeset the displayed maths <LaTeX> (<KaTeX's reason>)`. `build_site` now keeps Astro's stderr. When the build fails with such lines, it raises a `ContentError` listing them, so `uv run cheatsheet build` ends with `Content error:` like every other content problem. Any other failure is shown as before. The test builds content data with two bad formulas (an Entry's and a Pitfall's), without running kernels.
- **Look:** each maths part is its own left-aligned block in the Output's text colour, 16 px (KaTeX's 1.21 em of 13.25 px), with KaTeX's centring and margins removed. The block has `overflow-x: auto`, like the printed text.
- **Keyboard access to wide Outputs:** axe flagged the wide formula's scroll box (`scrollable-region-focusable`). A small client module (`site/src/client/scrollers.ts`) watches the Output's text and maths blocks with a `ResizeObserver`. It gives `tabindex="0"` to the blocks that actually scroll, and only to those. This covers long printed text too, which had the same latent problem. It is not a maths script: the maths is all rendered at build time.
- **axe and KaTeX:** KaTeX draws maths as single glyphs positioned over each other, so axe left their contrast for review. The shared audit now excludes `.katex-html`, which is `aria-hidden`; screen readers read its MathML twin. A test checks that the maths has the same colour as the Output's text, whose contrast axe does judge.
- **Search** indexes no Outputs at all (titles, explanations, code, Pitfall text and exception names only), so maths adds nothing to it. A test checks that `search.json` has no LaTeX or KaTeX markup.
- **npm packages after a pull:** `build_site` used to run `npm ci` only when `site/node_modules` was missing. A checkout that already had it would then fail on the new `katex` import. It now also runs it when `node_modules/.package-lock.json` is older than `site/package-lock.json`, and the README says so.
- **GLOSSARY:** no new term. The Output's definition now says "text, typeset maths or a figure".

**One existing Output changed, on purpose:** the Pitfall of `pandas-plots/a-histogram-of-a-column` now shows `<Figure size 600x350 with 0 Axes>` above its histograms. The empty figure that `plt.figure(...)` leaves before `df.hist()` has no SVG, so Jupyter shows its `text/plain`. Under this ticket's rule, the build now does too, and the Pitfall's own text says that Jupyter shows exactly this line. The other 256 Outputs were compared with a build of `main`. Their `content.json` data matches once `text` is read as one part, and their rendered HTML is identical apart from the new `data-scrolls` attribute and Astro's scoping attributes.

Checks:

- `uv run cheatsheet build` passed, then `uv run pytest`: 266 tests, of which 264 passed on the full run. The other two, the phone rail strip and re-opening the shown Entry from search, are Playwright tests in areas this ticket doesn't touch, and they passed when rerun on their own.
- The fixture Topic was looked at in Playwright screenshots in both themes: interleaved text and maths, collections, a fraction above an error line, and a wide formula scrolling inside its Output.
