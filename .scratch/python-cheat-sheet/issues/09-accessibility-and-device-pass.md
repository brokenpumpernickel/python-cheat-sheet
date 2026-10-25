# 09: Accessibility and device pass

**What to build:** A final pass over the finished interface, checking that a Student can use everything by keyboard and screen reader, with reduced motion and in both themes, on a laptop and a phone. Problems found are fixed here. This verifies the per-ticket criteria together; it doesn't replace them.

**Blocked by:** 08 (Language switch).

**Status:** resolved

- [x] An automated accessibility check (e.g. axe via Playwright) passes on the Overview (both arrangements), a Topic page and the open search pop-up, in both themes and both Languages.
- [x] A keyboard-only walkthrough covers Overview → Topic → Entry chip → See-also → Next stop → search → Esc back out, with visible focus throughout; it is recorded as a browser test.
- [x] Colour contrast meets WCAG AA for text in both themes, including Outputs, error lines and Pitfall callouts.
- [x] Reduced motion: no animations anywhere; state changes still complete.
- [x] Phone width (375 px): no horizontal page scroll; the rail strip, chips, cards and search are usable.

## Comments

**Resolved.** Tests: `tests/test_accessibility.py`. axe-core is a pinned npm dev dependency of `site/` (CI's `npm ci` installs it) and is injected into the page by Playwright.

- **Audit:** axe (WCAG 2.2 A/AA plus best practices) over the Map, the Trail, a Topic page in each rail arrangement and the open search pop-up, in both themes and both Languages, plus the figure Topic. axe leaves text over a gradient (the sea, the Trail's stretches, the sticky chips and strip) "for review", so the audit runs colour contrast twice more with every gradient flattened to its first and then its last colour, and fails on anything still undecided. A control test checks that it catches faint text on the sea. The only violations it found were contrast.
- **Contrast, for any hue:** the Author picks Area hues freely, so a second site (generated content, an Area every 30°, each with code, Output, an error line, a Pitfall, See also and a planned Topic, plus a planned Area) is audited in both themes; the palette was also checked offline every 2°. Changes in `theme.css`: light `--ink-2` #475569, `--ink-3` #586779, `--err` #b71c1c, `--deep-l` 25 % (was 30 %, too light on yellow and green), `--tk-num` #bf360c, `--tk-com`/`--tk-op` follow the inks; dark `--ink-2` #c8d3e0, `--ink-3` #8d9db3, `--err` #ffaaa3, and the Pitfall's yellow tint is a variable (`--pitfall-tint`, `--pitfall-output-tint`), lighter in dark so error lines read on it. The toggles and search prompt pass with the new `--ink-3`. Rule of thumb now: `--ink-3` only on neutral surfaces (sea, cards, code); text on an Area's colour uses `--ink-2` or darker.
- **Planned Topics:** no longer faded with `opacity`. They stay muted by their dashed outline, no fill and smaller type, in `--ink-2` on an island's colour and `--ink-3` on the sea of a planned Area. The rail now says "(coming soon)" to screen readers for them, as the Overview does.
- **Keyboard:** the walkthrough test tabs Overview → Numbers → the Addition chip → See also (Joining) → Next stop → Ctrl K, "powers", Enter → "/" then Esc (closes search, focus back on the Entry) → Esc (Overview, focus on the tile), checking at every Tab stop that the focused element is `:focus-visible` with a ring. Fixes: a Topic page that takes focus on zoom-in shows the ring on its header; an Entry jumped to keeps its ring when focus is visible (the flash still marks it after a click). A deep link counts as visible focus in Chrome, so the landed-on Entry shows the ring too. The selected search result is outlined in the focus colour instead of `--line`, since focus stays in the input.
- **Reduced motion:** one rule in `theme.css` turns off every CSS animation, transition and smooth scroll; the per-component rules it replaces are gone (the Entry flash keeps its still ring). The test walks zoom, hover, copy button, flash, Next stop, the toggle, Esc, an Area dot and search, checking `document.getAnimations()` and every element's computed durations, and that each change completes.
- **Phones (320 and 375 px):** in both Languages, the Map, a Topic page, the figure page, the Trail and open search have no sideways page scroll and no text cut off at the edges outside the strips meant to scroll (the rail strip, chips, code). The last chip and the last strip pin can be scrolled to and opened. A 15-Topic island at 375 px keeps every name inside its bubble. The top bar fits at 320 px (wraps the switches to a second row, as 08 left it).
- **The 08 notes:** the segments no longer show the default for a moment: an inline script right after them in `TopBar.astro` checks the choices the head script applied (tested with the client modules blocked). The radios stay "EN" / "PL": that is their visible text, so the name matches what voice-control users say, each carries its own `lang` so it's pronounced in its Language, and the group is named "Language" / "Język". A switch during the 1.5 s "Copied!" still leaves that one confirmation in the old Language; not worth the code.
- **Screen readers:** no screen reader was run. The accessibility tree of the Map, Trail, both rails, the top bar and a Topic page was reviewed through Playwright: landmarks, headings, list structure and link names read sensibly (Trail stones read as "1 Numbers Arithmetic.").

**Follow-ups:**
- **For the Author:** figures are `role="img"` with the generic label "Figure drawn by the code above". Real alt text needs an optional figure-description field (EN and PL) in the content format, written per figure.
- A manual pass with NVDA or VoiceOver over the rail, the Trail and search would confirm the tree review.
- Printed Output that is wider than its card scrolls but isn't a Tab stop. Chrome and Firefox make such scrollers keyboard-focusable themselves; Safari doesn't. Code blocks are Tab stops already (Shiki adds `tabindex="0"`).
