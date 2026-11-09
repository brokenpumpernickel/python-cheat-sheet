# 34: SymPy Substituting and evaluating, and Plotting with SymPy

**What to build:** Two planned SymPy Topics, written:
- **Substituting and evaluating:** putting numbers into an expression and getting decimals or a NumPy function out.
- **Plotting with SymPy:** `sp.plot`, and the usual alternative of `lambdify` plus `plt`.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Substituting and evaluating** (`evaluating`). The Entries, with these English titles:
  - **Substituting values:**
    - `expr.subs(a, 10)`, then several at once with a dict, `expr.subs({a: 10, x: 3})`.
    - **Pitfall:** `subs` returns a new expression and leaves `expr` unchanged. Show `expr` printed after a `subs` whose result wasn't kept.
  - **Substituting an expression:** `expr.subs(x, x**2)` or `expr.subs(x, y + 1)` puts an expression in place of a symbol.
  - **Decimal values:**
    - `.evalf()`, `.evalf(30)` and `sp.N(expr, 30)` after `subs`.
    - The notebook's `res.subs({a: 10, x: 3}).evalf(30)` for a 10th derivative is a good model; take the derivative as given, since Derivatives is ticket 35.
  - **Functions for NumPy:**
    - `f = sp.lambdify(x, expr)` makes a Python function that takes a NumPy array, e.g. `f(np.linspace(0, 1, 5))`.
    - With several symbols, `sp.lambdify((x, a), expr)`.
- **Plotting with SymPy** (`sympy-plots`). The Entries, with these English titles:
  - **A plot with sp.plot:**
    - `sp.plot(expr, (x, -3, 3))` draws an expression straight from SymPy.
    - Check how its figure reaches the Output and its size. Use `size=(6, 3.5)` if `sp.plot` takes it, so it matches the figure rules. Check that the build captures it as an SVG, and that the axis labels it adds are language-neutral (`x`, `f(x)`).
  - **Several curves:** `sp.plot(e1, e2, (x, a, b))`, and `show=False` with `.extend` or `.append` only if it is short.
  - **Plotting with lambdify:**
    - `lambdify` then `plt.plot(xs, f(xs))` on a `np.linspace` grid, as the notebook ends.
    - Say that this is the usual way when the plot needs Matplotlib's options, data points beside the curve, or subplots.
- **Figures** follow the guide's figure rules: one figure per Entry, `figsize=(6, 3.5)` or `sp.plot`'s equivalent, `plt.show()` where it applies, language-neutral text, and a figure description in both Languages.
- **Conventions** are ticket 33's: `import sympy as sp` and `sp.init_printing()` at the top, `display(...)` for symbolic results, `print(...)` for plain values. Read `symbols.md` and `expressions.md` and match them.
- **Links:**
  - Between the two Topics: *Functions for NumPy* ↔ *Plotting with lambdify*.
  - Matplotlib's *A line plot*, and NumPy *Arrays* (`linspace`).
  - At most three per Entry.

**Running in parallel** with tickets 35, 36 and 37. Each runs in its own session and PR.
- Edit only `evaluating.md` and `sympy-plots.md`, plus at most two back-links elsewhere, not in the files the other tickets edit (`derivatives.md`, `integrals.md`, `equations.md`, `matrices.md`, `differential-equations.md`, `probability.md`).
- Don't touch `_area.md`.
- The other tickets' Topics are still planned, so don't link to them. List any link you'd add under **Links to add later** in the Comments.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "podstawienie (substitution)".

**Blocked by:** 33 (the SymPy Area and its conventions).

**Status:** resolved

- [x] Both Topics are written (no longer planned), with summaries in both Languages and the decided Entries with their Polish, including the `subs` Pitfall.
- [x] Every figure follows the figure rules, with a figure description in both Languages.
- [x] Every example runs alone in a fresh kernel with no warnings, apart from the expected non-interactive one for figures.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages.
- [x] The Comments list every Entry with its Polish title, any decisions made on the way, and any Links to add later.
- [x] One session and one PR.

## Comments

- Resolved by PR (link to follow).
- **Topics** (English / Polish, glyph unchanged):
  - `evaluating`: *Substituting and evaluating* / *Podstawianie i obliczanie*, `subs`. Summary: "Putting values into SymPy expressions: substituting numbers and expressions, decimal values, and NumPy functions with lambdify." / "Podstawianie (substitution) wartości do wyrażeń SymPy: liczby i wyrażenia w miejsce symboli, wartości dziesiętne i funkcje dla NumPy z lambdify."
  - `sympy-plots`: *Plotting with SymPy* / *Wykresy w SymPy*, `plot`. Summary: "Plots of SymPy expressions: sp.plot for a quick curve, several curves at once, and lambdify with plt for everything Matplotlib can do." / "Wykresy (plots) wyrażeń SymPy: sp.plot do szybkiej krzywej, kilka krzywych naraz oraz lambdify z plt, gdy potrzebujesz wszystkiego, co daje Matplotlib."
- **Entries** (English / Polish):
  - Substituting and evaluating:
    - *Substituting values* / *Podstawianie wartości (subs)*: `expr.subs(a, 10)` and `expr.subs({a: 10, x: 3})`, both displayed. Pitfall: a `subs` whose result isn't kept, then `display(expr)` shows `expr` unchanged.
    - *Substituting an expression* / *Podstawianie wyrażenia*: `expr.subs(x, y + 1)`, its `sp.expand`, and `expr.subs(x, x**2)`.
    - *Decimal values* / *Wartości dziesiętne*: `res = sp.diff(sp.sin(a*x), x, 10)`, then `res.subs({a: 10, x: 3})` and `.evalf()`, `.evalf(30)`, `sp.N(val, 30)`, printed.
    - *Functions for NumPy* / *Funkcje dla NumPy*: `sp.lambdify(x, sp.exp(-x**2 / 2))` and `sp.lambdify((x, a), a * sp.exp(-a*x))`, called on `xs = np.linspace(0, 2, 3)` (and `2` for `a`). Three points keep each printed array under the ~46 characters an Output shows at 1280 px without scrolling; five points made it 56.
  - Plotting with SymPy:
    - *A plot with sp.plot* / *Wykres z sp.plot*: `p = sp.plot(x**3 - 3*x, (x, -3, 3), size=(6, 3.5))`.
    - *Several curves* / *Kilka krzywych*: `sp.plot(sp.sin(x), sp.cos(x), (x, 0, 2*sp.pi), legend=True, size=(6, 3.5))`.
    - *Plotting with lambdify* / *Wykres z lambdify*: the normal density from `lambdify`, drawn with `plt.plot(xs, f(xs))` over `plt.hist` of 500 `np.random.normal` samples (seed hidden).
- **How `sp.plot` reaches the Output:** SymPy's Matplotlib backend makes its figure with `plt.figure(figsize=size)` and calls `plt.show()` itself, so the build's inline backend captures it as one SVG, like any `plt` figure. `size=(6, 3.5)` works and gives a 6 × 3.5 in figure (424.8 × 244.8 pt after `bbox_inches="tight"`). Its axis labels are mathtext `x` and `f(x)`, and its legend uses the expressions' text form (`sin(x)`), so the figure is language-neutral.
- **Decisions:**
  - **`p = sp.plot(...)`:** `sp.plot` returns a Plot object, and a bare `sp.plot(...)` as a cell's last line makes Jupyter (and the `python` prompt) print `<sympy.plotting...MatplotlibBackend object at 0x...>` under the figure. The build ignores that, but a Student would see it, so both `sp.plot` Entries assign the result, and *A plot with sp.plot* says why.
  - **Several curves uses `sin` and `cos`:** the legend labels each curve with its expression's text form, so `x**2` showed as `x**2`; `sin(x)` and `cos(x)` read the same in both forms.
  - **No `show=False` with `.extend`:** with a second plot, `extend` and `show()` it took the example to 8 shown lines and a second idea, so it is left out, as the ticket allowed.
  - **10th derivative of `sin(a*x)`** for *Decimal values*: it displays as a short `-a**10*sin(a*x)`, and `subs` leaves `-10000000000*sin(30)`, which shows why `evalf` is needed. `sp.diff` is used as given; the explanation names it only.
  - **Plotting with lambdify draws data beside the curve** (a histogram under the density), since that is one of the reasons the explanation gives for taking this route.
  - **Polish title *Podstawianie wartości (subs)*** gives the function name in brackets, like ticket 33's *Upraszczanie (simplify)*; the Topic's Polish summary carries "podstawianie (substitution)".
  - **Back-links (two):** *Building expressions* → `evaluating/functions-for-numpy` (the way to get a NumPy function, which its `np.sin` Pitfall points towards; ticket 33 named the `sympy-plots` lambdify Entry, but the `evaluating` one is the direct fix), and *Decimals to many digits* → `evaluating/decimal-values`.
  - Other links: *Functions for NumPy* ↔ *Plotting with lambdify*, `arrays/ranges` from both, `plotting-basics/a-line-plot` from *Plotting with lambdify*, `expressions/expanding-and-factoring` from *Substituting an expression*, `symbols/decimals-to-many-digits` from *Decimal values*.
- **Links to add later** (Topics of tickets 35–37, still planned while this ran; add them once those are merged):
  - *Decimal values* → Derivatives (ticket 35), its Entry on `sp.diff` with a count (higher derivatives), since the example takes the 10th derivative.
  - *Substituting values* or *Decimal values* ← Equations (ticket 36), if its Entries substitute a solution back with `subs` or turn one into a decimal with `evalf`.
  - *Plotting with lambdify* or *A plot with sp.plot* ← Differential equations (ticket 36), if it plots a solution of `dsolve`.
  - *Functions for NumPy* ← Probability (ticket 37), if it turns a density into a NumPy function.
