# 19: Matplotlib Interactive plots: ipywidgets and interact

**What to build:** A new Matplotlib Topic on driving plots with Jupyter widgets: `interact`, the controls it makes from values, the `@interact` decorator, sliders made explicitly, and `fixed`. With ticket 18, each example's Output shows the figure at the starting values, with the controls drawn above it as a static picture.

Decided with the Author (every recommendation accepted, plus the static controls from ticket 18):

- **Where:** a new Topic, `interactive-plots`, **Interactive plots** (*Wykresy interaktywne*), last in the Matplotlib Topic order, after Subplots. Choose its glyph per the authoring guide.
- **Entries** (6), with these English titles; the Polish titles are the agent's:
  - A slider with interact:
    - `interact(plot, mu=(-3.0, 3.0))` on a normal curve, with `def plot(mu=0.0):`. The function's default sets where the slider starts; without one, it starts in the middle of the range.
    - **Pitfall, with code:** whole numbers make a whole-number slider, so `p=(0, 1)` gives only 0 or 1. Write `(0.0, 1.0)`, or give a step: `(0, 1, 0.05)`.
  - Several sliders:
    - `mu` and `sigma`. The function fixes the axes with `plt.xlim` / `plt.ylim`.
    - **Pitfall, without code:** without fixed limits, the axes rescale on every move, and the curve seems not to change.
  - Dropdowns and checkboxes: a list gives a dropdown, `True` / `False` a checkbox, and a string a text box. For example, choose `bins` from `[10, 20, 50]` and toggle `density` on a histogram.
  - The @interact decorator: `@interact(n=(10, 1000, 10))` written above the function. Here it is a growing sample's histogram, the law of large numbers.
  - Sliders made explicitly:
    - `widgets.FloatSlider(min=..., max=..., step=..., value=..., description="σ")` passed to `interact`, for full control.
    - `continuous_update=False`, so a slow plot redraws only when the slider is released.
  - Holding a value fixed: `fixed(data)` passes a sample in without making a control for it.
- **Plotting inside the function:** every function starts with `plt.figure(figsize=(6, 3.5))` and ends with `plt.show()`, like the other Matplotlib examples. With the default inline backend that redraws cleanly on each move. `%matplotlib widget` (ipympl) is not covered.
- **NumPy only:** formulas are written with NumPy, as in the existing Matplotlib Entries, because the SciPy stats Area comes after Matplotlib. See-also links point to SciPy stats Entries such as *Comparing parameters*, and to Matplotlib and NumPy Entries where natural.
- **Imports:** `from ipywidgets import interact`, plus `fixed` and `import ipywidgets as widgets` where used.
- **Text in figures** stays language-neutral. Control descriptions are code names or symbols (`mu`, `σ`, `n`), which are language-neutral too.
- **Figure descriptions** describe the plot at the starting values; the controls have their own screen-reader text (ticket 18).

Conventions from tickets 12–17 apply: one figure per example at `figsize=(6, 3.5)`, the default style, seeded `default_rng`, a blank line after compound blocks so examples paste into the REPL, and "Polish term (English term)" at first mention, e.g. "suwak (slider)", "kontrolka (widget)".

**Blocked by:** 18 (Widgets in Outputs).

**Status:** ready-for-agent

- [ ] The Topic exists last in the Matplotlib Topic order, with its Polish title and a distinct glyph, and the six Entries with the decided English titles, each with Polish, including both Pitfalls.
- [ ] Every example's Output shows its figure at the starting values with the controls drawn above it, and every figure has a description in both Languages.
- [ ] Examples use NumPy only, the agreed imports and the plotting pattern; random data is seeded.
- [ ] See-also links connect the Entries with SciPy stats, Matplotlib and NumPy Entries where natural.
- [ ] Every example runs alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, with no warnings, and pastes into the REPL.
- [ ] `uv run cheatsheet build` and `uv run pytest` pass; the Topic was looked at in both Languages and both themes in `uv run cheatsheet serve`.
- [ ] The Comments list every Entry with its Polish title and figure description.
- [ ] One session and one PR.

## Comments
