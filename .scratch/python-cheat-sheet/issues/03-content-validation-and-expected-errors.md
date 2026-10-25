# 03: Full content validation, expected errors and figures

**What to build:** The content build becomes the safety net that lets agents write content (ADR 0002, ADR 0005). Every rule under "Validation" in the spec is enforced, and every failure stops the build with a message naming the Area, Topic and Entry. Examples marked as expected to raise show only the final error line as their Output. Pitfall examples run and are captured like Entry examples. Matplotlib figures are captured as SVG (non-interactive backend, every figure open at `plt.show()` or at the end). Planned Areas and Topics pass with no Entries.

**Blocked by:** 01 (Tracer bullet).

**Status:** resolved

- [x] Expected error of the right type → Output is that final line (e.g. `KeyError: 'sd'`); wrong type, an unmarked error, or a marked example that completes normally each fail the build.
- [x] A Matplotlib example produces an SVG figure in the data; a fixture covers this even though the MVP has no Matplotlib content.
- [x] The build fails on: missing required field, more than one code example in an Entry, duplicate Entry ids, any missing Polish counterpart, See-also to a non-existent Entry, Topic order naming an unknown Topic, a Topic file absent from every Topic order.
- [x] Each rule above has a content-build test with a small fixture folder.
- [x] Error messages are short and point at the exact place, so an agent can fix the content from the message alone.

## Comments

**Resolved.** Every rule fails with a `ContentError` whose message starts with the place to fix (file, usually line, and `topic-id/entry-id`). Tests: `tests/test_content_build.py`, one folder per rule in `tests/fixtures/invalid/`, and `tests/fixtures/figures/` for Matplotlib. Rules added beyond the ticket's list: an Area folder missing from `areas.yaml`, an Area or Topic listed twice, a planned Area with a non-planned Topic, an empty `PL:` paragraph or code block. Examples now run in parallel (up to 8 kernels, each still fresh), and every failing example is reported at once, one per line. The real Lists Topic builds in about 2.5 s instead of about 8 s.

- **For 05:** each figure is a complete `<svg>` string in `output.figures`, without the XML prolog, so it can be inlined. Sizes are in pt from Matplotlib's default figure size, and the background is Matplotlib's default white. Inline SVGs share the page's id namespace; Matplotlib's ids are content hashes, so different figures don't collide. If that ever bites, render them as `<img src="data:image/svg+xml,...">` instead. Pitfall `output` is `null` when the Pitfall has no code. A Pitfall can also have figures.
- **For 10:** the rules are in `docs/content-format.md`, including a new "When the build fails" section. A See-also link must name an existing Entry, so links to a planned Topic wait until it has Entries. Parse errors stop at the first problem. Execution errors are all listed. The Matplotlib backend is non-interactive (inline, SVG); figures open at `plt.show()` or at the end are captured, and `plt.close()` drops one.
- **For 12:** add the See-also links left out in 01 (Sorting → `functions/lambda`, List comprehensions → `loops/for-over-a-collection`) only once those Entries exist, or the build fails. Planned Areas may list only planned Topics. The build ignores stderr, so library warnings don't fail it; check examples for warnings by hand if "no warnings" matters.
