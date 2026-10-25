# 10: Authoring guide for agents

**What to build:** A written guide that lets an agent, or the Author, add or edit content correctly the first time, linked from the project's agent instructions. It covers:

- **Structure:** the Area and Topic file format; the Entry anatomy, with an explanation of 1–3 sentences, exactly one self-contained example that prints explicitly (ADR 0003), the Output never written by hand (ADR 0002), when to add a Pitfall, and when to mark an expected error.
- **Topic order:** a Topic comes after the Topics its examples rely on, and See-also links to a later Topic are preferred over reordering.
- **Polish:** Polish is required, with the Polish term plus the English one in parentheses at the first mention, and the agreed labels (ADR 0005).
- **Vocabulary:** use the glossary's terms.
- **Workflow:** how to build, read failures and preview locally.

**Blocked by:** 03 (Full content validation), since the guide documents the final rules.

**Status:** ready-for-agent

- [ ] The guide includes one complete annotated example Topic covering every Entry feature.
- [ ] Every validation rule from ticket 03 is listed with the error it produces and how to fix it.
- [ ] The project's agent instructions point to the guide for any content task.
- [ ] Verified by having a fresh agent add a small throwaway Topic using only the guide; it builds on the first or second try (then removed).
