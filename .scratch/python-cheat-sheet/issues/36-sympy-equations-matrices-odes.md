# 36: SymPy Equations, Matrices, and Differential equations

**What to build:** Three planned SymPy Topics, written, following the Author's notebook:
- **Equations:** `Eq`, `solve`, systems;
- **Matrices:** with determinants and eigenvalues;
- **Differential equations:** `Function`, `dsolve`, initial conditions.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Equations** (`equations`). The Entries, with these English titles:
  - **Equations with Eq:**
    - `eq = sp.Eq(a*x**2 + b*x + c, 0)` and `sp.solve(eq, x)` give the quadratic formula's two roots.
    - **Pitfall:** `a*x**2 + b*x + c == 0` is `False`, because `==` compares the expressions themselves. Use `sp.Eq`.
  - **Solving expr = 0:** `sp.solve(expr, x)` treats a bare expression as equal to 0.
  - **Systems of equations:** `sp.solve([2*x + y, 3*x + 4*y + 1], [x, y])` gives a dict.
  - **Solving for one symbol:** solve a formula for one of its symbols, e.g. a normal quantile, `z = (x - mu)/sigma` for `x`.
  - **Numeric solutions:** `sp.nsolve(sp.cos(x) - x, x, 1)` when `solve` finds no closed form.
- **Matrices** (`matrices`). The Entries, with these English titles:
  - **Making a matrix:**
    - `sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])`, a matrix times a symbol as in the notebook (`V0 * sp.Matrix(...)`), and `sp.eye(3)`.
    - `.shape`, and one element `M[0, 1]`.
  - **Matrix arithmetic:**
    - `M * N` is the matrix product, `M.T` the transpose, and `M.inv()` the inverse.
    - **Pitfall:** for a NumPy array, `*` multiplies element by element, but for a SymPy Matrix it is the matrix product. Show both on the same numbers.
  - **Determinants:** `M.det()` on a symbolic matrix.
  - **Eigenvalues and eigenvectors:**
    - `M.eigenvals()` gives a dict of value → multiplicity.
    - `M.eigenvects()` gives (value, multiplicity, vectors) triples.
    - Use the notebook's 3×3 with `V_0`.
- **Differential equations** (`differential-equations`). The Entries, with these English titles:
  - **Functions and their derivatives:** `x = sp.Function("x")`, then `x(t)` and `x(t).diff(t, t)`.
  - **Solving an ODE:**
    - `sp.dsolve(sp.Eq(x(t).diff(t, t), -w**2 * x(t)), x(t))`, the harmonic oscillator from the notebook, with constants `C1`, `C2`.
    - Give `w` `positive=True` so the result has sin and cos.
  - **Initial conditions:**
    - `ics={x(0): x0, x(t).diff(t).subs(t, 0): v0}`.
    - The derivative at 0 is written with `.subs(t, 0)`; say so.
  - **Using the solution:**
    - `res.rhs` is the solution's formula.
    - Substitute numbers with `subs`, and turn it into a NumPy function with `lambdify`.
    - Keep this short: those Entries are in ticket 34's Substituting and evaluating, which is planned, so add the link later.
- **Conventions** are ticket 33's: `import sympy as sp` and `sp.init_printing()` at the top, `display(...)` for symbolic results, `print(...)` for plain values. Read `symbols.md` and `expressions.md` and match them.
- **Links:**
  - Symbols and numbers' *Assumptions*.
  - NumPy's *Matrix multiplication* or *Linear algebra* Entries, where they exist, for the `*` Pitfall.
  - Between the three Topics.
  - At most three per Entry.

**Running in parallel** with tickets 34, 35 and 37. Each runs in its own session and PR.
- Edit only `equations.md`, `matrices.md` and `differential-equations.md`, plus at most two back-links elsewhere, not in the files the other tickets edit (`evaluating.md`, `sympy-plots.md`, `derivatives.md`, `integrals.md`, `probability.md`).
- Don't touch `_area.md`.
- The other tickets' Topics are still planned, so don't link to them. List any link you'd add under **Links to add later** in the Comments.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "równanie (equation)", "układ równań (system of equations)", "macierz (matrix)", "wartości własne (eigenvalues)", "równanie różniczkowe (differential equation)", "warunki początkowe (initial conditions)".

**Blocked by:** 33 (the SymPy Area and its conventions).

**Status:** resolved

- [x] All three Topics are written (no longer planned), with summaries in both Languages and the decided Entries with their Polish, including the `==` and `*` Pitfalls.
- [x] Every example runs alone in a fresh kernel with no warnings.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. All three pages were looked at in both Languages, with typeset maths and no code box scrolling sideways.
- [x] The Comments list every Entry with its Polish title, any decisions made on the way, and any Links to add later.
- [x] One session and one PR.

## Comments

- **Topics** (English / Polish, glyph kept from ticket 33):
  - `equations`: *Equations* / *Równania*, `Eq`. Summary: "Equations in SymPy: Eq and solve, solving an expression equal to 0, systems of equations, solving a formula for one symbol and numeric solutions." / "Równania (equations) w SymPy: Eq i solve, rozwiązywanie wyrażenia równego 0, układy równań, wyznaczanie jednego symbolu ze wzoru i rozwiązania numeryczne."
  - `matrices`: *Matrices* / *Macierze*, `Mat`. Summary: "Exact, symbolic matrices in SymPy: making a matrix, the matrix product, transpose and inverse, determinants, eigenvalues and eigenvectors." / "Dokładne, symboliczne macierze (matrices) w SymPy: tworzenie macierzy, iloczyn macierzy, transpozycja i odwrotność, wyznaczniki, wartości i wektory własne."
  - `differential-equations`: *Differential equations* / *Równania różniczkowe*, `y''`. Summary: "Ordinary differential equations in SymPy: unknown functions and their derivatives, dsolve, initial conditions and using the solution." / "Równania różniczkowe zwyczajne (ordinary differential equations) w SymPy: funkcje niewiadome i ich pochodne, dsolve, warunki początkowe i korzystanie z rozwiązania."
- **Entries** (English / Polish):
  - Equations:
    - *Equations with Eq* / *Równania (equations) z Eq*: `sp.Eq(a*x**2 + b*x + c, 0)` displayed, then `sp.solve(eq, x)`, the two quadratic-formula roots. Pitfall: `print(a*x**2 + b*x + c == 0)` prints `False`.
    - *Solving expr = 0* / *Rozwiązywanie expr = 0*: `x**2 - 5*x + 6` → [2, 3], `x**2 - 2` → [−√2, √2], `x**2 + 1` → [−i, i]; the explanation says complex roots are included unless `x` is `real=True`.
    - *Systems of equations* / *Układy równań (systems of equations)*: `sp.solve([2*x + y, 3*x + 4*y + 1], [x, y])` → {x: 1/5, y: −2/5}, then `sol[x]`.
    - *Solving for one symbol* / *Wyznaczanie jednego symbolu*: `sp.Eq(z, (x - mu) / sigma)` solved for `x` → [μ + σz], with `sigma` `positive=True`; then `.subs({z: 2, mu: 100, sigma: 15})` prints `130`.
    - *Numeric solutions* / *Rozwiązania numeryczne*: `sp.nsolve(sp.cos(x) - x, x, 1)` prints `0.739085133215161`, and `sp.cos(r) - r` prints `0` as a check. The explanation names the `NotImplementedError` that `sp.solve` raises on the same equation.
  - Matrices:
    - *Making a matrix* / *Tworzenie macierzy (matrix)*: the notebook's `V0 * sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])` (`V_0` shows as V₀), `M.shape` printed, `M[0, 1]`, `sp.eye(3)`.
    - *Matrix arithmetic* / *Działania na macierzach*: `M * N`, `M.T`, `M.inv()` on 2×2 matrices (the inverse shows 3/2 and −1/2). Pitfall: `a * a` for `np.array([[1, 2], [3, 4]])` prints `[[ 1  4] [ 9 16]]`, while `M * M` for the same `sp.Matrix` is [[7, 10], [15, 22]]; the text names `a @ a`.
    - *Determinants* / *Wyznaczniki (determinants)*: `sp.Matrix([[a, b], [c, d]]).det()` → ad − bc, and a symbolic 3×3 tridiagonal matrix → 1 − 2x².
    - *Eigenvalues and eigenvectors* / *Wartości i wektory własne (eigenvalues, eigenvectors)*: the notebook's 3×3 with `V_0`: `M.eigenvals()` → {0: 1, −√2V₀: 1, √2V₀: 1}, then each triple of `M.eigenvects()` displayed on its own line.
  - Differential equations:
    - *Functions and their derivatives* / *Funkcje i ich pochodne (derivatives)*: `x = sp.Function("x")`, `x(t)`, `x(t).diff(t)`, `x(t).diff(t, t)`.
    - *Solving an ODE* / *Rozwiązywanie równania różniczkowego (ODE)*: the harmonic oscillator `sp.Eq(x(t).diff(t, t), -w**2 * x(t))` with `w = sp.Symbol("omega", positive=True)`, displayed, then `sp.dsolve` → x(t) = C₁ sin(ωt) + C₂ cos(ωt).
    - *Initial conditions* / *Warunki początkowe (initial conditions)*: `ics = {x(0): x0, x(t).diff(t).subs(t, 0): v0}` → x(t) = x₀ cos(ωt) + v₀ sin(ωt)/ω. The explanation says x′(0) is written with `.subs(t, 0)`: the derivative first, then `t = 0`.
    - *Using the solution* / *Korzystanie z rozwiązania*: with x(0) = 2 and x′(0) = 0, `display(res)` and `display(res.rhs)` (2 cos(ωt)), then `sp.lambdify(t, res.rhs.subs(w, sp.pi))` on `np.array([0, 1, 2])` prints `[ 2. -2.  2.]`. Kept short, as decided.
- **Links:**
  - *Equations with Eq* → *Symbols*; *Solving expr = 0* and *Solving for one symbol* → *Assumptions*; *Numeric solutions* → *Decimals to many digits*.
  - *Making a matrix* → NumPy's *Two-dimensional arrays*; *Matrix arithmetic* (for the `*` Pitfall) → NumPy's *Element-wise arithmetic* and *Two-dimensional arrays*. NumPy has no matrix multiplication or linear algebra Entry.
  - *Solving an ODE* → *Assumptions* and *Equations with Eq*; *Using the solution* → NumPy's *Maths functions*.
  - **Back-links (two):** Symbols and numbers' *Assumptions* → *Solving an ODE*, where `positive=True` turns the answer from exponentials into sin and cos; NumPy's *Element-wise arithmetic* → *Matrix arithmetic*, for the `*` contrast.
- **Links to add later** (their Topics are planned while tickets 34, 35 and 37 run):
  - *Functions and their derivatives* → Derivatives and limits' `diff` Entry (ticket 35).
  - *Using the solution* → Substituting and evaluating's `subs` and `lambdify` Entries (ticket 34).
  - *Solving for one symbol* → Substituting and evaluating's `subs` Entry (ticket 34), for its `.subs({...})` line.
  - *Numeric solutions* → Substituting and evaluating's `evalf` Entry (ticket 34).
  - *Using the solution* → Plotting with SymPy, to plot the solution, once it is written.
  - Ticket 33's pending link, *Exact numbers* or *Symbols* → Equations, was not added: no Equations Entry relies on `Rational`.
- **Decisions:**
  - **Eigenvectors one triple per line:** `display(M.eigenvects())` as one list is about three times wider than the card and would scroll, so the example loops `for triple in M.eigenvects(): display(triple)`. Each line keeps the (value, multiplicity, [vector]) form.
  - **The quadratic's roots stay one list:** at 1280 px the two fractions fit the card, so `sp.solve` shows as Students see it in Jupyter.
  - **No raised `NotImplementedError`:** *Numeric solutions* names it in the explanation rather than running it, because the error is not the Entry's point; the example prints `cos(r) - r` as a check instead.
  - **Determinants uses a 3×3 with `x`, not the notebook's matrix,** whose determinant is 0 and shows nothing. The notebook's matrix is in *Making a matrix* and *Eigenvalues and eigenvectors*.
  - **Solving for one symbol** substitutes z = 2, μ = 100, σ = 15 (printing `130`) rather than z = 1.96, which prints the Float `129.400000000000`.
  - **Using the solution** takes ω = π, so the NumPy values at t = 0, 1, 2 are exactly 2, −2, 2, with no rounding noise.
  - **Polish titles carry the English term** where Students meet it in documentation: *Równania (equations) z Eq*, *Układy równań (systems of equations)*, *Tworzenie macierzy (matrix)*, *Wyznaczniki (determinants)*, *Wartości i wektory własne (eigenvalues, eigenvectors)*, *Funkcje i ich pochodne (derivatives)*, *Rozwiązywanie równania różniczkowego (ODE)*, *Warunki początkowe (initial conditions)*. The explanations add `Function`, matrix product, transpose, inverse, dict and right-hand side.
  - **Checks:** all 15 examples (Entries and Pitfalls) ran alone in IPython with `-W default` and wrote nothing to stderr. `uv run cheatsheet build` passed. Then `uv run pytest`: 265 passed and 1 failed (`test_language`, `PL-en-charts (trail rail)`, a Playwright timeout), which passed when rerun alone. All three pages were checked at 1280 px in EN and PL: 29 typeset results, no KaTeX errors, and no code box, Output or maths box scrolls sideways.
