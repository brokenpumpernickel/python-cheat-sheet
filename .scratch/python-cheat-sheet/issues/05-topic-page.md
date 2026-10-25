# 05: Topic page

**What to build:** The full Topic page from the prototype (C4). It has a coloured header in the Area's hue (glyph, Area, title, summary), sticky Entry chips that jump to Entries, and Entry cards in two columns on wide screens and one on narrow ones. Each card shows its title, explanation (with inline code and emphasis), syntax-highlighted code with a copy button, and its Output: text, the error line, or the figure on a white card. A Pitfall shows a "Watch out!" sticker and a callout, with its own code and Output when it has them. See-also chips link to other Entries. The page ends with Previous stop / Next stop, following Topic order across all non-planned Topics, Area by Area. A deep link to an Entry briefly highlights it.

**Blocked by:** 01 (Tracer bullet).

**Status:** ready-for-agent

- [ ] All Entry parts render for text Output, expected-error Output, figure Output, Pitfall with and without code, and See-also.
- [ ] Copy puts the exact example code on the clipboard and confirms briefly.
- [ ] Previous/Next stop follow Topic order and skip planned Topics; the first and last Topics show only one of the two.
- [ ] Layout is comfortable at laptop width beside Jupyter and usable at phone width without horizontal page scroll (code blocks may scroll on their own).
- [ ] Browser tests cover Next stop order, See-also navigation, Entry highlight on deep link and copy.
- [ ] All labels ("Output", "Pitfall", "Watch out!", "See also", "Next stop", …) come from the bilingual label table.
