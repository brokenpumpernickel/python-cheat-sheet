# 03: Full content validation, expected errors and figures

**What to build:** The content build becomes the safety net that lets agents write content (ADR 0002, ADR 0005). Every rule under "Validation" in the spec is enforced, and every failure stops the build with a message naming the Area, Topic and Entry. Examples marked as expected to raise show only the final error line as their Output. Pitfall examples run and are captured like Entry examples. Matplotlib figures are captured as SVG (non-interactive backend, every figure open at `plt.show()` or at the end). Planned Areas and Topics pass with no Entries.

**Blocked by:** 01 (Tracer bullet).

**Status:** ready-for-agent

- [ ] Expected error of the right type → Output is that final line (e.g. `KeyError: 'sd'`); wrong type, an unmarked error, or a marked example that completes normally each fail the build.
- [ ] A Matplotlib example produces an SVG figure in the data; a fixture covers this even though the MVP has no Matplotlib content.
- [ ] The build fails on: missing required field, more than one code example in an Entry, duplicate Entry ids, any missing Polish counterpart, See-also to a non-existent Entry, Topic order naming an unknown Topic, a Topic file absent from every Topic order.
- [ ] Each rule above has a content-build test with a small fixture folder.
- [ ] Error messages are short and point at the exact place, so an agent can fix the content from the message alone.
