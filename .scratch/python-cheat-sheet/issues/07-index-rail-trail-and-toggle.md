# 07: Index rail, Trail and the Map | Trail toggle

**What to build:** The two arrangements of the Overview and the Index that follows them (prototype C4).

- **Trail:** one stretch per Area, Topics as numbered stepping stones swaying along a dotted path with their title and summary beside them, plus dots at the left edge that jump to each Area and show which one is in view.
- **Toggle:** a Map | Trail switch in the top bar. Map is the default, and the choice is remembered per visitor.
- **Index rail:** inside a Topic, the Overview shrinks into a side rail that slides in. In Map mode it shows mini islands with Topic pins; in Trail mode, a numbered mini-trail. The current Topic is marked "you are here" and expands its Entries, and the Entry in view is highlighted as the Student scrolls.
- **Phone width:** the rail becomes a horizontally scrolling strip centred on the current Topic, without the Entry list.

**Blocked by:** 04 (Map Overview and semantic zoom), 05 (Topic page).

**Status:** resolved

- [x] Switching the toggle on the Overview swaps the arrangement; inside a Topic it swaps only the rail.
- [x] Zooming in and out works from the Trail as from the Map, returning to the Topic's stone.
- [x] Rail pins navigate between Topics with a crossfade; the expanded Entry links jump within the page.
- [x] Scroll spy highlights the Entry in view; a deep link highlights its Entry.
- [x] The toggle is an accessible radio group; the rail is labelled as the Index.
- [x] Browser tests cover toggle persistence across reloads, both rails, "you are here" and Entry expansion.

## Comments

**Resolved.** The Trail is `TrailView.astro` (the Area dots and "Start here") with one `TrailLand.astro` per Area, laid out by `site/src/map/trail.ts` at build time: stones sway at x = 50 ± 30 % of the stretch, 132 px apart, numbered per Area by `stopNumbers()` (the Area's stops, as Previous / Next walks them). The toggle is two native radio inputs in a `role="radiogroup"` in `TopBar.astro`, run by `client/arrangement.ts`. The choice is `<html data-arrangement>`; one rule in `theme.css` hides whatever is marked for the other arrangement (`data-arrangement="map"|"trail"` on the Map, the Trail, the rail's two halves and the hero's back-link text). An inline script in the page head applies the stored choice (`localStorage["cheatsheet.arrangement"]`) before the first paint. The rail is `IndexRail.astro` (with `RailEntries.astro`) inside `[data-topic-view]`; `client/rail.ts` marks the current Topic's pins `aria-current="page"` (CSS then shows "you are here" and expands its Entries) and runs the scroll spy. The rail slides in and out through `slideRail()` in `motion.ts`, alongside the page fade. `client/trail.ts` runs the Area dots. Tests: `tests/test_index.py`; `test_zoom.py` now expects the rail's slide and tabs past the toggle.

- **Found on the way:** `isTyping()` in `client/keys.ts` treated every `<input>` as a text field, so Esc did nothing while focus sat on the toggle. Radio buttons and checkboxes no longer count.
- **Scroll spy:** the Entry being read is the one that most recently scrolled up to the sticky chips (the highest one, with two columns), or the first one before any has. After a jump (chip, rail, search, deep link), the jumped-to Entry stays highlighted until the Student scrolls, because the page may end before a late Entry can reach the chips.
- **Phone (≤ 860 px):** the rail is a sticky strip 56 px tall (`--strip` in `TopicView.astro`). The chips stick below it through `--sticky-top`, and `scrollTo` in `views.ts` now subtracts the chips' computed `top` plus their height. The strip hides Area titles (the Trail keeps each Area's dot as a separator), planned Topics and the Entry lists. It is scrolled so that the current Topic is centred.
- **Test locators:** the rail repeats Topic and Entry titles (twice in the DOM, once per arrangement), so scope link lookups to the chips, the page or the rail. `get_by_text` matches hidden copies too, so use `.filter(visible=True)`. Text checks on rail links should use the accessible name, because `textContent` includes the glyph and the hidden "you are here".
- **For 08 (Language):** new labels: `trail`, `arrangement`, `index`, `youAreHere`, `areas`, `hintStone`, `startHere`. All are rendered at build time, as are the Area titles and blurbs, Topic titles and summaries, and Entry titles in the Trail and the rail. These need their `pl` twins on a switch. Re-rendering in place keeps the route, and the arrangement lives on `<html>`, so it survives a re-render. After swapping the rail's contents, call `show(currentPage)` on the rail (`startRail` returns it; `views.ts` owns it) so that "you are here", the expanded Entries and the spy highlight are reapplied. Astro strips whitespace between elements, so keep the explicit `{" "}` spaces in stone and step names. Without them, screen readers read "1Numbers".
- **For 09 (accessibility, devices):**
  - Each arrangement shows only one copy of the rail; the hidden copy is `display: none`, so it never reaches assistive technology.
  - The toggle's focus ring is on the visible segment (`input:focus-visible + span`).
  - The Area dots are buttons with `aria-current`. Their names show only on hover, focus or when current, and they are hidden below 860 px.
  - The "you are here" text is `aria-hidden`, because `aria-current="page"` already says it.
  - In the top bar below 640 px, the site title is visually hidden (the badge stays). Check that the logo, search icon and toggle (and 08's EN | PL) fit at 320 px.
  - Long Topic titles in a Trail label wrap at 210 px (110 px on phones).
  - The rail and the Trail have not been checked with a screen reader.
