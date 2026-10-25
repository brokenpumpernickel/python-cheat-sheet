# 08: EN | PL Language switch

**What to build:** An EN | PL switch in the top bar changes the Language of all prose and interface labels (ADR 0005). English is the default. The choice is remembered per visitor, and a `?lang=pl` or `?lang=en` parameter overrides it and stays in the URL while switching. Switching re-renders in place, keeping the route and scroll position. Links are identical in both Languages. The document's `lang` attribute follows the Language. Agreed Polish labels: Wynik (Output), Pułapka (Pitfall), Mapa (Map), Szlak (Trail).

**Blocked by:** 04 (Map Overview), 05 (Topic page), 06 (Search), 07 (Index rail and Trail).

**Status:** ready-for-agent

- [ ] Every visible string in every view (Overview in both arrangements, Topic page, rail, search pop-up, copy button, hints, footer) switches; no English remains in Polish mode.
- [ ] Switching inside a Topic keeps the Topic, the highlighted Entry and roughly the scroll position.
- [ ] `?lang=pl` opens in Polish on first visit; toggling updates the parameter.
- [ ] Search results display in the active Language while still matching both.
- [ ] Browser tests cover switching on the Overview and inside a Topic, persistence across reloads, and `?lang=pl`.
