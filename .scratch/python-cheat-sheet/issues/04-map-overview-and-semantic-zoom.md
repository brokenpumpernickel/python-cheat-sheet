# 04: Map Overview and semantic zoom

**What to build:** The Overview becomes the Map from the prototype (C4). Each Area is a round island in its hue, and its Topics are bubbles with glyph and title, placed on rings: the first Topic in the centre once there are five or more, the rest clockwise from the top, and a second ring beyond about thirteen. Islands flow and wrap automatically. Planned Areas and Topics render faded and can't be clicked. Clicking a Topic plays the semantic zoom into its page (ADR 0001), and Back or Esc zooms back out to the tile. Visual style: the soft "Islands" look, with self-hosted fonts and light and dark themes that follow the system setting.

**Blocked by:** 01 (Tracer bullet).

**Status:** ready-for-agent

- [ ] Islands are sized from their ring layout so every bubble fits inside its island, for any number of Topics (verified with fixture Areas of 1, 3, 9 and 15 Topics).
- [ ] Zoom-in scales the Overview toward the tile and fades in the Topic page; zoom-out reverses and returns focus to the tile.
- [ ] Opening a deep link plays no animation; reduced motion turns all animations off; every animation has a timeout fallback, so navigation completes in a background tab.
- [ ] Topics are real links, reachable with Tab and opened with Enter; Esc zooms out unless typing in a field.
- [ ] A route to a planned or unknown Topic shows the Overview.
- [ ] Browser tests cover click and keyboard zoom in/out, Back, deep link and reduced motion.
- [ ] Interface labels come from one label table with English and Polish entries (the switch itself is ticket 08).
