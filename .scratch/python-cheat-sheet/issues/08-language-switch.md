# 08: EN | PL Language switch

**What to build:** An EN | PL switch in the top bar changes the Language of all prose and interface labels (ADR 0005). English is the default. The choice is remembered per visitor, and a `?lang=pl` or `?lang=en` parameter overrides it and stays in the URL while switching. Switching re-renders in place, keeping the route and scroll position. Links are identical in both Languages. The document's `lang` attribute follows the Language. Agreed Polish labels: Wynik (Output), Pułapka (Pitfall), Mapa (Map), Szlak (Trail).

**Blocked by:** 04 (Map Overview), 05 (Topic page), 06 (Search), 07 (Index rail and Trail).

**Status:** resolved

- [x] Every visible string in every view (Overview in both arrangements, Topic page, rail, search pop-up, copy button, hints, footer) switches; no English remains in Polish mode.
- [x] Switching inside a Topic keeps the Topic, the highlighted Entry and roughly the scroll position.
- [x] `?lang=pl` opens in Polish on first visit; toggling updates the parameter.
- [x] Search results display in the active Language while still matching both.
- [x] Browser tests cover switching on the Overview and inside a Topic, persistence across reloads, and `?lang=pl`.

## Comments

**Resolved.** The page holds both Languages, and CSS shows one. `components/Text.astro` renders a label (by key) or a content twin (`en` and `pl`) as `<span data-lang="en">…</span><span data-lang="pl">…</span>`. One rule in `theme.css` hides the spans that don't match `<html lang>`. The spans have no styles of their own, so they take the look of whatever element holds them. Attributes that CSS can't switch (`aria-label`, `placeholder`) are rendered with `labelAttributes()` from `labels.ts`, which also marks them (`data-label-attributes="aria-label=index"`). `client/language.ts` rewrites them, along with `document.title`, at start and on every switch.

- **Why not re-render on the client:** a switch changes nothing but `lang` and a few attributes. The rail's "you are here", the scroll spy, focus, the flash and the arrangement are left alone. Links are the same by construction. The cost is that prose is in the page twice. Code, Outputs and figures make up most of the page, and those appear once. For Lists, the page grows from about 28 KB to 34 KB, or from 4.5 KB to 5.5 KB gzipped. Client-side re-rendering would need a second copy of the prose in the bundle anyway.
- **The switch:** a second radio group in `TopBar.astro`, beside Map | Trail. The two groups sit together in `.switches`, which wraps to a second row, on the right, when it doesn't fit beside the logo and pill. That happens at 320 px; at 375 px everything fits on one row in both Languages. On phones the segments are narrower (`padding: 6px 12px`). The radios read EN and PL in both Languages, each marked with its own `lang`; the group is "Language" / "Język".
- **Choice and `?lang=`:** the choice is stored in `localStorage["cheatsheet.language"]`, wrapped in try/catch. `?lang=en|pl` wins over the stored choice but isn't stored itself, so a link with `?lang=pl` in lab instructions doesn't change a Student's own setting. Switching stores the choice and, if the URL has `lang`, replaces it with `replaceState`, keeping the hash. No parameter is added when there wasn't one. The inline head script (`pages/index.astro`) applies the parameter or the stored choice, and the title, before the first paint, next to the arrangement. An unknown `?lang=` falls back to the stored choice.
- **In place:** `startLanguage(around)` lets `views.keepPlace(change)` wrap each switch. It keeps one element at the same place on screen: the Entry the rail highlights or, failing that, the first Entry, island or stretch of the Trail in view. It then holds the rail highlight (`rail.jumped`, new `rail.current()`) until the Student scrolls. At the top of a page it stays at the top. `search.languageSwitched()` re-renders open results (the dialog is modal, so this is a safety net); results reopen in the current Language anyway. After "Copied!", the copy button restores its own two-Language label (`copy.ts`), so it keeps following the switch.
- **Tests:** `tests/test_language.py`. The "nothing left over" check collects the rendered text nodes (outside code, Outputs, figures and key caps), the title, and every `aria-label` and `placeholder`. It then looks for whole-word matches of the other Language's labels (from `labels.ts`) and prose (the hidden `data-lang` twins). It runs in both directions, over the Map, the Trail, two Topic pages, the Trail rail and open search results, with a positive control. The `labels` fixture moved to `conftest.py`. Existing tests that compared `textContent` now use `use_inner_text=True` (or `filter(visible=True)`), because `textContent` includes the hidden twin.

- **For 09:**
  - The top bar isn't sticky, so a mouse or keyboard user reaches the switch near the top of the page, and focusing it scrolls there anyway. Keeping the place matters only if the bar becomes sticky (the tests click the radio without scrolling to check it).
  - Hidden twins are `display: none`, so they stay out of the accessibility tree. Run axe in both Languages. Only the radio labels carry their own `lang`; everything else inherits `<html lang>`.
  - Consider whether the radios should be read as "English" / "Polski" rather than "EN" / "PL" (keep the visible text in the name).
  - Like Map | Trail, the radios are rendered checked for the default until `client/language.ts` runs, so the wrong segment can show for a moment before the script loads. The text itself is already right before the first paint.
  - A switch during the 1.5 s "Copied!" leaves that one confirmation in the old Language until it resets.
  - The switch uses the same `.toggle` styles as Map | Trail, in both themes. Check its contrast along with the toggle's.
