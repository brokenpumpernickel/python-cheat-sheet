# 06: Search

**What to build:** A search pop-up opened with Ctrl/Cmd+K, with `/` when not typing in a field, or from the search pill in the top bar. It searches a build-time index of Topic titles and summaries, and Entry titles, explanations and code, in both Languages whichever one is active. Every query word must match. Ranking: title prefix > title contains > Topic name > body. Results show the title and the Area › Topic path. Arrow keys move, Enter opens, Esc closes. Choosing a result navigates to the Entry and highlights it.

**Blocked by:** 01 (Tracer bullet).

**Status:** resolved

- [x] The index is produced at build time and loads without slowing the first view.
- [x] Finds an Entry by an English word, a Polish word (e.g. "słownik") and a code fragment (e.g. `.get(`).
- [x] Shows a clear "no matches" state; planned Topics never appear.
- [x] Fully keyboard-operable; focus returns sensibly when closed.
- [x] Browser tests cover the three kinds of query, keyboard selection and navigation to the Entry.

## Comments

**Resolved.** The index is built by `site/src/search/build.ts` and written by the static endpoint `site/src/pages/search.json.ts` as `search.json` next to the page. It holds one document per non-planned Topic and Entry: titles (EN and PL), the Area › Topic path, and a plain-text body. For a Topic the body is its summary; for an Entry it is the explanations (tag-stripped), code, Pitfall text and code, and expected errors. It is about 3.5 KB for Lists. The page fetches it the first time search opens, or when the pointer reaches the pill, so the first view doesn't load it. Matching and ranking are in `site/src/search/match.ts`, which has no runtime imports, so Node can test it. Matching ignores case and diacritics ("slownik" finds "słownik"). Each query word scores by the best field it matches (title prefix 8, title contains 4, Topic name 2, body 1); ties keep Topic order; at most 20 results. The pop-up is a modal `<dialog>` in `components/Search.astro`, with the input as a combobox over a listbox, run by `client/search.ts`. The pill is in `TopBar.astro`. Tests: `tests/test_search.py`.

- **Focus:** opening a result calls `goTo()` in `client/router.ts`, which sets the hash, or re-renders when the hash is already the same. `views.ts` now focuses the Entry it scrolls to (Entry cards have `tabindex="-1"`), so chips, See also and deep links move focus too. Esc and a backdrop click return focus to where it was before opening. Enter pressed while the index is still loading opens the top result once it arrives.
- **For 07:** the pill sits after the logo with `margin-left: auto`; put the Map | Trail toggle after it. The pill is now the first Tab stop, before the Map's bubbles (`test_zoom.py` tabs past it). If the top bar becomes sticky, the search dialog is unaffected (it's in the top layer), but `scrollTo` must subtract the bar's height as well.
- **For 08:** result titles and paths come from the index's `en`/`pl` pairs and use `pageLanguage()` (new `client/language.ts`, shared with copy) when they render, so they follow `<html lang>`. Results already on screen re-render on the next keystroke, or call `render()` after a switch. The dialog's static labels (`search*` keys, plus `hintSearch`) are rendered at build time like every other label, so switch them the same way as the rest. The `Ctrl K` key caps (`[data-shortcut]`) become `⌘ K` on Apple platforms.
- **For 09:** the input shows focus with a coloured bottom border, not an outline. On `(hover: none)` screens the key hints are hidden, and below 640 px the pill shows only its icon (its prompt stays as the accessible name). Results have no visible focus ring because they aren't focusable: the input keeps focus, and `aria-activedescendant` with a filled selected row shows the selection.
