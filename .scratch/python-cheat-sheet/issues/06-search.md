# 06: Search

**What to build:** A search pop-up opened with Ctrl/Cmd+K, with `/` when not typing in a field, or from the search pill in the top bar. It searches a build-time index of Topic titles and summaries, and Entry titles, explanations and code, in both Languages whichever one is active. Every query word must match. Ranking: title prefix > title contains > Topic name > body. Results show the title and the Area › Topic path. Arrow keys move, Enter opens, Esc closes. Choosing a result navigates to the Entry and highlights it.

**Blocked by:** 01 (Tracer bullet).

**Status:** ready-for-agent

- [ ] The index is produced at build time and loads without slowing the first view.
- [ ] Finds an Entry by an English word, a Polish word (e.g. "słownik") and a code fragment (e.g. `.get(`).
- [ ] Shows a clear "no matches" state; planned Topics never appear.
- [ ] Fully keyboard-operable; focus returns sensibly when closed.
- [ ] Browser tests cover the three kinds of query, keyboard selection and navigation to the Entry.
