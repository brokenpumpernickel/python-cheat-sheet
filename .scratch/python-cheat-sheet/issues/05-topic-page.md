# 05: Topic page

**What to build:** The full Topic page from the prototype (C4). It has a coloured header in the Area's hue (glyph, Area, title, summary), sticky Entry chips that jump to Entries, and Entry cards in two columns on wide screens and one on narrow ones. Each card shows its title, explanation (with inline code and emphasis), syntax-highlighted code with a copy button, and its Output: text, the error line, or the figure on a white card. A Pitfall shows a "Watch out!" sticker and a callout, with its own code and Output when it has them. See-also chips link to other Entries. The page ends with Previous stop / Next stop, following Topic order across all non-planned Topics, Area by Area. A deep link to an Entry briefly highlights it.

**Blocked by:** 01 (Tracer bullet).

**Status:** resolved

- [x] All Entry parts render for text Output, expected-error Output, figure Output, Pitfall with and without code, and See-also.
- [x] Copy puts the exact example code on the clipboard and confirms briefly.
- [x] Previous/Next stop follow Topic order and skip planned Topics; the first and last Topics show only one of the two.
- [x] Layout is comfortable at laptop width beside Jupyter and usable at phone width without horizontal page scroll (code blocks may scroll on their own).
- [x] Browser tests cover Next stop order, See-also navigation, Entry highlight on deep link and copy.
- [x] All labels ("Output", "Pitfall", "Watch out!", "See also", "Next stop", …) come from the bilingual label table.

## Comments

**Resolved.** The page is `TopicPage.astro` (header, sticky Entry chips, cards, Previous/Next stop), built from `EntryCard`, `CodeBlock` and `OutputBlock`. `TopicView.astro` works out the Topic order (`stops`: non-planned Topics, Area by Area) and the See-also lookup. Code is highlighted at build time by Astro's own `<Code>` (Shiki, so no new dependency). The theme in `site/src/code/theme.ts` maps grammar scopes to the `--tk-*` colours in `theme.css`. Client: `client/copy.ts` handles copy, and `flash()` in `client/motion.ts` flashes the Entry, called from `scrollTo` in `views.ts`. Tests: `tests/test_topic_page.py`. `tests/fixtures/site` now has a second Area (Plots › Charts, with a figure), an expected error, Pitfalls with and without code, and See-also links in both directions.

- **For 06 (search):** to open a result, set `location.hash = "#topic/entry"`. The page then scrolls the Entry in below the chips and flashes it. If the result is the Entry already in the hash, no `hashchange` fires, so call `flash()` yourself. `entry.code` is plain text; `explain` and the Pitfall `text` are HTML.
- **For 07 (rail, scroll spy):** Entry cards are `[data-entry]` sections. The chips are `[data-chips]`, sticky at `top: 0`, and `scrollTo` subtracts their height. If the top bar or the rail strip becomes sticky above them, change both. The Trail can number Topics with the same `stops` order as Previous/Next.
- **For 08 (Language):** every label is rendered with `label()` at build time, including the `aria-label`s (Entries, See also, Pitfall, Topic order, figure). The copy confirmation reads `<html lang>` at click time, so it already follows a switch. The copy text sits in the button's `[aria-live]` span. Content that needs its Polish twin: the header, chip and card titles, explanations, Pitfall text, See-also chip titles (the target Entry's `pl.title`), and the Previous/Next Topic titles.
- **For 09 (accessibility, devices):**
  - Copy buttons hide until hover only on `(hover: hover)` devices; on touch screens they always show.
  - Without the Clipboard API, copy falls back to `execCommand`.
  - Code blocks scroll on their own and are focusable (Shiki adds `tabindex="0"`).
  - Error lines wrap; printed text keeps its layout and scrolls.
  - Below 600 px, the chips become one row that scrolls sideways.
  - With reduced motion, the flash is a still ring.
  - The sticker is `aria-hidden`, because the Pitfall `aside` is labelled.
  - Figures are `role="img"` with a generic label; real alt text would need a content field.
- **Clipboard on Windows:** the clipboard stores line breaks as CRLF, so the copy test normalises them before comparing.
