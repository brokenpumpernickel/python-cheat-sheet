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

**Status:** resolved

- [x] The Topic exists last in the Matplotlib Topic order, with its Polish title and a distinct glyph, and the six Entries with the decided English titles, each with Polish, including both Pitfalls.
- [x] Every example's Output shows its figure at the starting values with the controls drawn above it, and every figure has a description in both Languages.
- [x] Examples use NumPy only, the agreed imports and the plotting pattern; random data is seeded.
- [x] See-also links connect the Entries with SciPy stats, Matplotlib and NumPy Entries where natural.
- [x] Every example runs alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass; the Topic was looked at in both Languages and both themes in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title and figure description.
- [x] One session and one PR.

## Comments

- Resolved by PR #29: https://github.com/brokenpumpernickel/python-cheat-sheet/pull/29.
- Entries, with their Polish titles and figure descriptions (the descriptions describe the plot at the starting values; the controls have their own screen-reader text):
  - **A slider with interact** — *Suwak (slider) z interact*. Control: `mu` slider from -3.00 to 3.00, at 0.00.
    - Figure: "A bell curve centred on x = 0, peaking at about 0.4, on an x-axis from −6 to 6." / "Krzywa dzwonowa o środku w x = 0, ze szczytem około 0,4, na osi x od −6 do 6."
    - Pitfall (with code, `def plot(p=0.5):` and `p=(0, 1)`; the slider runs 0 to 1 at 0). Figure: "One wide bar at 0 reaching the top of a y-axis from 0 to 1, and no bar at all at 1." / "Jeden szeroki słupek w 0 sięgający szczytu osi y od 0 do 1, a w 1 nie ma żadnego słupka."
  - **Several sliders** — *Kilka suwaków (sliders)*. Controls: `mu` and `sigma`.
    - Figure: "A bell curve centred on x = 0 on fixed axes, x from −6 to 6 and y from 0 to 0.85; its peak of about 0.4 reaches less than half the height." / "Krzywa dzwonowa o środku w x = 0 na ustalonych osiach, x od −6 do 6 i y od 0 do 0,85; jej szczyt, około 0,4, nie sięga nawet połowy wysokości."
    - Pitfall without code: the axes are fitted to every new curve, so the peak always touches the top and only the y-axis numbers change.
  - **Dropdowns and checkboxes** — *Listy rozwijane (dropdowns) i pola wyboru (checkboxes)*. Controls: `bins` dropdown (10, 20, 50) and `density` checkbox.
    - Figure: "Ten bars in a rough bell shape from about −2.3 to 2.6; the tallest, just right of 0, holds about 70 values." / "Dziesięć słupków w przybliżeniu w kształcie dzwonu, od około −2,3 do 2,6; najwyższy, tuż na prawo od 0, mieści około 70 wartości."
  - **The @interact decorator** — *Dekorator (decorator) @interact*. Control: `n` slider from 10 to 1000 in steps of 10, at 50.
    - Figure: "A smooth bell curve on an x-axis from −4 to 4 over a histogram of 50 values, all between −2 and 2; the bars are ragged, some well above the curve and some below it." / "Gładka krzywa dzwonowa na osi x od −4 do 4 nad histogramem 50 wartości, wszystkich między −2 a 2; słupki są nierówne, jedne wyraźnie powyżej krzywej, inne poniżej."
  - **Sliders made explicitly** — *Suwaki (sliders) tworzone jawnie*. Control: `σ` slider from 0.50 to 3.00, at 1.50.
    - Figure: "A wide, low bell curve centred on x = 0, peaking at about 0.27 on a y-axis from 0 to 0.85, and nearly flat at x = ±5." / "Szeroka, niska krzywa dzwonowa o środku w x = 0, ze szczytem około 0,27 na osi y od 0 do 0,85, prawie płaska przy x = ±5."
  - **Holding a value fixed** — *Ustalona wartość*. Control: `bins` slider from 5 to 50, at 20; `data=fixed(scores)` makes none.
    - Figure: "Twenty bars from about 30 to 105 in a rough bell shape around 65, with ragged tops." / "Dwadzieścia słupków od około 30 do 105, w przybliżeniu w kształcie dzwonu wokół 65, o nierównych wierzchołkach."
- Decisions:
  - **Glyph** `(0,1)`: the tuple Students type to get a slider, distinct in the Area.
  - **Topic summary** "Plots driven by Jupyter widgets with interact: …" / "Wykresy sterowane kontrolkami (widgets) Jupytera przez interact: …". The Matplotlib Area blurb now ends "…, grids of plots and interactive plots." / "…, siatki wykresów i wykresy interaktywne."
  - **`interact(...);`**: every `interact` call that ends a cell has a trailing `;`, so Jupyter doesn't also print `<function plot(...)>` under the controls (ticket 18's note). The first Entry says why in one sentence; the decorator Entry needs none.
  - **Pitfall 1** uses a function default of 0.5 with `p=(0, 1)`: the int slider turns it into 0, which the Output shows (slider at 0, all the probability on 0).
  - **Pitfall 2** is about the y-axis: the curve's x-range is fixed by `np.linspace`, so without `plt.ylim` the peak always touches the top and moving `sigma` seems not to change the height.
  - **Sliders made explicitly**: the slider's `value=1.5` is where it starts, so its function has no default. Checked in a kernel: an explicit widget's `value` wins over the function default.
  - **Holding a value fixed** says that, without `fixed`, `interact` turns the array into a dropdown of its values. That was checked in a kernel too.
  - **Polish terms**: "suwak (slider)", "lista rozwijana (dropdown)", "pole wyboru (checkbox)", "pole tekstowe (text box)", "kontrolka (widget)", "dekorator (decorator)", "argument nazwany (keyword argument)", "prawo wielkich liczb (law of large numbers)", at first mention per Entry, in the title when the title has it.
  - **See also**: SciPy stats' *A pdf curve*, *A histogram with the pdf* and *Comparing parameters*; Matplotlib's *Axis limits and a grid*, *Several lines and a legend*, *Choosing bins*, *Density with a PDF on top* and *A histogram*; NumPy's *Indexing and slicing* and *Normal samples*; Python Basics' *Default arguments*. One reverse link: *Comparing parameters* → *Several sliders*, its third.
- Checked: all 7 examples (6 Entries, 1 Pitfall with code) ran alone with `uv run python` in an empty folder with `MPLBACKEND=Agg`, each figure rendered to SVG, with no stderr besides Agg's notice. Each was also fed line by line to `code.InteractiveConsole` like a REPL paste. Code lines are at most 43 characters (39 in the Pitfall). Outside a kernel, `display` prints the widget's repr, `interactive(children=(FloatSlider(...), ...))`, which is plain Python's fallback and not a warning. In `generated/content.json` each Output has one figure and the controls listed above at their starting values.
- `uv run cheatsheet build` and `uv run pytest` (228 tests) pass, run one after the other. In `uv run cheatsheet serve` the Topic was looked at in English (dark theme) and Polish (light theme), and at 375 px with no sideways scrolling. In all 7 Outputs the drawn controls sit above the figure, and the hidden list reads each control in both Languages, e.g. "p: slider from 0 to 1, at 0" / "p: suwak od 0 do 1, ustawiony na 0".
