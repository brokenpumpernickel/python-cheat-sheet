# Polish as a toggleable second Language, sharing code and Outputs

We originally chose English only, then added Polish because Students are Polish speakers. English stays the default; each visitor can switch to Polish (remembered per visitor, or forced with `?lang=pl`), and links are identical in both Languages. Only prose is translated: titles, explanations, Pitfalls and interface labels. Code and Outputs exist once and are shared, so examples are still executed once (ADR 0002). Both Languages live side by side in the same Topic file, and the build fails if any Topic or Entry lacks Polish, so a Student who switches never lands on a half-English page. Polish text names a Python concept in Polish with the English term in parentheses at its first mention, e.g. "krotka (tuple)", because the English term is what Students meet in error messages and documentation.

## Considered Options

- **Separate file per Language**: rejected; agents would have to keep two files in sync and code would be duplicated.
- **Optional Polish with English fallback**: rejected; mixed-language pages are worse than a build that refuses to ship them, and agents make translating cheap.
