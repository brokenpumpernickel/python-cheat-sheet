# 09: Accessibility and device pass

**What to build:** A final pass over the finished interface, checking that a Student can use everything by keyboard and screen reader, with reduced motion and in both themes, on a laptop and a phone. Problems found are fixed here. This verifies the per-ticket criteria together; it doesn't replace them.

**Blocked by:** 08 (Language switch).

**Status:** ready-for-agent

- [ ] An automated accessibility check (e.g. axe via Playwright) passes on the Overview (both arrangements), a Topic page and the open search pop-up, in both themes and both Languages.
- [ ] A keyboard-only walkthrough covers Overview → Topic → Entry chip → See-also → Next stop → search → Esc back out, with visible focus throughout; it is recorded as a browser test.
- [ ] Colour contrast meets WCAG AA for text in both themes, including Outputs, error lines and Pitfall callouts.
- [ ] Reduced motion: no animations anywhere; state changes still complete.
- [ ] Phone width (375 px): no horizontal page scroll; the rail strip, chips, cards and search are usable.
