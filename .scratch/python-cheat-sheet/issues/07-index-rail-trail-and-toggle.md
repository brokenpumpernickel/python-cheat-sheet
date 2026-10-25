# 07: Index rail, Trail and the Map | Trail toggle

**What to build:** The two arrangements of the Overview and the Index that follows them (prototype C4).

- **Trail:** one stretch per Area, Topics as numbered stepping stones swaying along a dotted path with their title and summary beside them, plus dots at the left edge that jump to each Area and show which one is in view.
- **Toggle:** a Map | Trail switch in the top bar. Map is the default, and the choice is remembered per visitor.
- **Index rail:** inside a Topic, the Overview shrinks into a side rail that slides in. In Map mode it shows mini islands with Topic pins; in Trail mode, a numbered mini-trail. The current Topic is marked "you are here" and expands its Entries, and the Entry in view is highlighted as the Student scrolls.
- **Phone width:** the rail becomes a horizontally scrolling strip centred on the current Topic, without the Entry list.

**Blocked by:** 04 (Map Overview and semantic zoom), 05 (Topic page).

**Status:** ready-for-agent

- [ ] Switching the toggle on the Overview swaps the arrangement; inside a Topic it swaps only the rail.
- [ ] Zooming in and out works from the Trail as from the Map, returning to the Topic's stone.
- [ ] Rail pins navigate between Topics with a crossfade; the expanded Entry links jump within the page.
- [ ] Scroll spy highlights the Entry in view; a deep link highlights its Entry.
- [ ] The toggle is an accessible radio group; the rail is labelled as the Index.
- [ ] Browser tests cover toggle persistence across reloads, both rails, "you are here" and Entry expansion.
