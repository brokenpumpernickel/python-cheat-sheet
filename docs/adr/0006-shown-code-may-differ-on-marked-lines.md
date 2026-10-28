# Shown code may differ from run code, on marked lines only

This refines ADR 0002 and ADR 0003. Students in the lab call `default_rng()` and `rvs` without a seed and get new numbers on every run, and showing `default_rng(7)` or `random_state=rng` in every example confused them. The build still needs a seed, or the Outputs would change from build to build. Later Entries will also want to show a web download while the build, which has no network, reads a local copy. So an example's code may now run in one form and be shown in another, but only line by line: `code  #| show: <shown code>` runs `code` and shows `<shown code>` in its place, and `code  #| hide` runs `code` and isn't shown. Unmarked lines run exactly as shown, and the page, Copy and search all use the shown code. The markers are for seeds and data sources only, never for changing what an example does. The build can't check that a shown line means the same as its run line; the Author has to.

## Considered Options

- **A hidden second code block that runs instead of the shown one**: rejected. The Output could quietly drift from the code beside it, and every change would have to be made twice.
- **Patching NumPy and SciPy in the kernel** so that unseeded calls are seeded: rejected. It is invisible in the content, couples the build to library internals that change between versions, and doesn't help with data sources.
- **Keeping the seeds visible**: rejected; it is not how the lab works, and the seed stays visible where it is the point (NumPy's *Setting a seed*, SciPy's *Reproducible samples*).

## Note: the np.random functions (ticket 21)

Generator objects confused Students as much as visible seeds did, and the lab calls the `np.random.*` functions directly (`np.random.normal(...)`, `np.random.randint(...)`). So the examples do too, seeded by a hidden `np.random.seed(<n>)  #| hide` line. SciPy's `rvs` without `random_state` draws from the same global generator, so that line seeds it as well and the `random_state=rng` markers are gone. A generator from `np.random.default_rng` is mentioned only in NumPy's *Setting a seed*, as the style newer code uses.
