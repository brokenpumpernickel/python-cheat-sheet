# 04: Map Overview and semantic zoom

**What to build:** The Overview becomes the Map from the prototype (C4). Each Area is a round island in its hue, and its Topics are bubbles with glyph and title, placed on rings: the first Topic in the centre once there are five or more, the rest clockwise from the top, and a second ring beyond about thirteen. Islands flow and wrap automatically. Planned Areas and Topics render faded and can't be clicked. Clicking a Topic plays the semantic zoom into its page (ADR 0001), and Back or Esc zooms back out to the tile. Visual style: the soft "Islands" look, with self-hosted fonts and light and dark themes that follow the system setting.

**Blocked by:** 01 (Tracer bullet).

**Status:** resolved

- [x] Islands are sized from their ring layout so every bubble fits inside its island, for any number of Topics (verified with fixture Areas of 1, 3, 9 and 15 Topics).
- [x] Zoom-in scales the Overview toward the tile and fades in the Topic page; zoom-out reverses and returns focus to the tile.
- [x] Opening a deep link plays no animation; reduced motion turns all animations off; every animation has a timeout fallback, so navigation completes in a background tab.
- [x] Topics are real links, reachable with Tab and opened with Enter; Esc zooms out unless typing in a field.
- [x] A route to a planned or unknown Topic shows the Overview.
- [x] Browser tests cover click and keyboard zoom in/out, Back, deep link and reduced motion.
- [x] Interface labels come from one label table with English and Polish entries (the switch itself is ticket 08).

## Comments

**Resolved.** The page is split into `site/src/components/` (TopBar, Overview, MapView, Island, TopicView, TopicPage, Footer) and client modules in `site/src/client/` (`router`, `motion`, `views`, `keys`, wired in `main`). Labels: `site/src/labels.ts`. Ring layout: `site/src/map/rings.ts`, computed at build time. Tests: `tests/test_zoom.py`, `tests/test_map.py` (generated content data with Areas of 1, 3, 9 and 15 Topics, no kernels), `tests/test_labels.py`; shared site fixtures in `tests/conftest.py`.

- **For 05 (Topic page):** replace `TopicPage.astro`; keep `data-topic`, `tabindex="-1"` and the `data-home` back link. Entry targets are found by `data-entry="topic/entry"`. Switching Topics already crossfades (`views.ts`); add the Entry flash where `views.ts` scrolls to the Entry.
- **For 06 (search):** use `isTyping()` from `client/keys.ts` for `/`. The Esc handler skips events with `defaultPrevented`, so call `preventDefault()` when Esc closes the pop-up. Add the pill to `TopBar.astro`.
- **For 07 (Trail, rail, toggle):** put the Trail as a second arrangement inside `Overview.astro`, beside `MapView`, with `data-tile` on each stone: the zoom uses the tile in the visible arrangement. Put the rail inside `[data-topic-view]` in `TopicView.astro`. Add the rail slide to `motion.ts`, so it goes through `play()` and gets the timeout fallback. The toggle goes in `TopBar.astro`.
- **For 08:** every label is in `labels.ts`, with `label(key, language)`. The page renders English only for now.
- **For 09:** on narrow screens the whole Map scales down so its widest island fits (`--u` in `MapView.astro`). Bubble text keeps a minimum size, so it gets tight in a 15-Topic island at 375 px.
- **Build:** Astro 7 now emits the self-hosted fonts as asset files and moves them into the output folder by renaming them. That fails across drives on Windows, so `build_site` builds into `site/.astro/out` and copies the result to the output folder.
- **Esc** adds an Overview history entry (no `#` left in the URL), so Back after Esc returns to the Topic.
