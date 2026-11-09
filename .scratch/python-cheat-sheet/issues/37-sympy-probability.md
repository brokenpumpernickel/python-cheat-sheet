# 37: SymPy Probability with SymPy (pdfs, moments, moment generating functions, sympy.stats)

**What to build:** The last planned SymPy Topic, **Probability with SymPy**. It does the lab's probability by hand with SymPy, then with `sympy.stats`:
- normalising a pdf;
- mean and variance with integrals, or sums for a discrete distribution;
- moment generating functions.

Decided with the Author (every recommendation accepted, plus the Author's request to cover moment generating functions). The English titles are decided; the Polish titles are the agent's.

- **Probability with SymPy** (`probability`). The Entries, with these English titles:
  - **Normalising a pdf:**
    - Find `c` so that `c * x * sp.exp(-x)` (or `c*(1 - x**2)` on [-1, 1]) integrates to 1.
    - `sp.solve(sp.integrate(f, (x, 0, sp.oo)) - 1, c)`.
  - **Mean and variance:**
    - E[X] = ∫ x f(x) dx and Var(X) = E[X²] − E[X]², for an exponential pdf `lam*sp.exp(-lam*x)` with `lam` positive, giving `1/lam` and `1/lam**2`.
  - **Discrete distributions:**
    - The same with `sp.Sum(...).doit()`, e.g. the mean of a geometric or Poisson pmf over k = 0 … ∞.
    - Check what `doit()` returns, and use `sp.simplify` if it is a `Piecewise`.
  - **Moment generating functions:**
    - M(t) = E[e^{tX}] by hand: `sp.integrate(sp.exp(t*x) * f, (x, 0, sp.oo))` for the exponential, with `conds="none"` or a `t < lam` assumption, whichever is clearer.
    - Then the moments as derivatives at 0: `M.diff(t, n).subs(t, 0)`.
    - Show that the first two give the mean and variance of *Mean and variance*.
  - **Distributions in sympy.stats:**
    - `from sympy.stats import Normal, Exponential, E, variance, P, density`.
    - `X = Normal("X", mu, sigma)`, then `E(X)`, `variance(X)`, `density(X)(x)` and `P(X > mu)`.
    - With numbers, `P(X > 1).evalf()`.
  - **Moment generating functions in sympy.stats:**
    - `moment_generating_function(X)` for `Normal` and `Exponential`, matching the hand-made one.
    - `sp.stats.moment(X, n)`, or `E(X**n)`, for a moment directly.
  - **Pitfall:** in `P(X > 1)`, `X > 1` must involve the random variable `X`. A plain Symbol `x` there is the usual mix-up. Show what happens, and use `raises=` if it raises. Check what SymPy 1.14 does, and keep the Pitfall only if the result is confusing.
- **Conventions** are ticket 33's: `import sympy as sp` and `sp.init_printing()` at the top, `display(...)` for symbolic results, `print(...)` for plain values. Read `symbols.md` and `expressions.md` and match them. Use `positive=True` on parameters so results don't come back as `Piecewise`, and say so once.
- **Links:**
  - Symbols and numbers' *Assumptions*.
  - SciPy stats' *A distribution object* and *Mean, spread and intervals*: the numeric counterpart of `sympy.stats`.
  - Plotting distributions' *Probability as an area*.
  - At most three per Entry.

**Running in parallel** with tickets 34, 35 and 36. Each runs in its own session and PR.
- Edit only `probability.md`, plus at most two back-links elsewhere, not in the files the other tickets edit (`evaluating.md`, `sympy-plots.md`, `derivatives.md`, `integrals.md`, `equations.md`, `matrices.md`, `differential-equations.md`). A back-link from SciPy stats is fine.
- Don't touch `_area.md`.
- The other tickets' Topics are still planned, so don't link to them. List under **Links to add later** in the Comments:
  - Integrals and sums' *Integrals to infinity* and *Sums*;
  - Derivatives and limits' *Higher derivatives*, for the moments;
  - Equations' *Solving expr = 0*, for normalising.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "gęstość (pdf)", "wartość oczekiwana (expected value)", "wariancja (variance)", "funkcja tworząca momenty (moment generating function)", "zmienna losowa (random variable)".

**Blocked by:** 33 (the SymPy Area and its conventions).

**Status:** resolved

- [x] Probability with SymPy is written (no longer planned), with a summary in both Languages and the decided Entries with their Polish, including both moment generating function Entries.
- [x] Every example runs alone in a fresh kernel with no warnings.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. The page was looked at in both Languages, with typeset maths and no code box scrolling sideways.
- [x] The Comments list every Entry with its Polish title, any decisions made on the way, and any Links to add later.
- [x] One session and one PR.

## Comments

- Resolved by PR (link below once opened).
- **The Topic:** `content/sympy/probability.md`, *Probability with SymPy* / *Prawdopodobieństwo w SymPy*, `E(X)`, no longer planned. Summary: "Probability by hand and with sympy.stats: normalising a pdf, mean and variance, discrete distributions, moment generating functions and random variables." / "Prawdopodobieństwo ręcznie i z sympy.stats: normowanie gęstości (pdf), wartość oczekiwana i wariancja, rozkłady dyskretne, funkcje tworzące momenty (moment generating functions) i zmienne losowe (random variables)."
- **Entries** (English / Polish), checked against SymPy 1.14.0:
  - *Normalising a pdf* / *Normowanie gęstości (pdf)*: `c*(1 - x**2)` on [-1, 1] integrates to 4c/3, `sp.solve(total - 1, c)[0]` gives 3/4 and the normalised pdf 3/4 − 3x²/4; then `c*x*sp.exp(-2*x)` on [0, ∞) gives `[4]`. See also: plotting-distributions/probability-as-an-area.
  - *Mean and variance* / *Wartość oczekiwana i wariancja*: exponential pdf with `lam = sp.Symbol("lambda", positive=True)`: E[X] = 1/λ, E[X²] = 2/λ², Var = 1/λ². This is where `positive=True` is explained once (a plain `lam` gives a `Piecewise` with the condition |arg λ| < π/2). See also: symbols/assumptions, distributions/mean-spread-and-intervals.
  - *Discrete distributions* / *Rozkłady dyskretne*: Poisson pmf with `k` `integer=True, nonnegative=True` and `mu` positive: `sp.Sum(k*pmf, ...).doit()` is μ; E[k²] comes back as μ(μ + 1), so the variance needs `sp.simplify` to reach μ. Then a geometric pmf with `p = sp.Rational(1, 4)` gives 3. See also: discrete-distributions/poisson-distribution, symbols/assumptions.
  - *Moment generating functions* / *Funkcje tworzące momenty*: `sp.integrate(sp.exp(t*x) * f, (x, 0, sp.oo), conds="none")`, then `sp.simplify` gives λ/(λ − t); `M.diff(t).subs(t, 0)` is 1/λ and `m2 - m1**2` is 1/λ², matching *Mean and variance*.
  - *Distributions in sympy.stats* / *Rozkłady w sympy.stats*: `X = Normal("X", mu, sigma)`: `E(X)` μ, `variance(X)` σ², `density(X)(x)`, `P(X > mu)` 1/2; `Z = Normal("Z", 0, 1)` and `print(P(Z > 1).evalf())` 0.158655253931457. Pitfall (`raises=ValueError`): with a plain Symbol `x`, `E(x**2)` quietly returns x², and `P(x > 1)` raises `ValueError: Expression containing Random Variable expected, not x > 1`. See also: distributions/a-distribution-object, distributions/mean-spread-and-intervals.
  - *Moment generating functions in sympy.stats* / *Funkcje tworzące momenty w sympy.stats*: `moment_generating_function(X)(t)` for `Normal` (e^(μt + σ²t²/2)) and `Exponential("Y", lam)` (λ/(λ − t), the hand-made one), `moment(Y, 3)` 6/λ³ and `E(Y**2)` 2/λ².
- **Decisions:**
  - *Normalising a pdf* uses `c*(1 - x**2)` first, since `c*x*sp.exp(-x)` already integrates to `c` (c = 1 shows nothing); the infinite-range case is `c*x*sp.exp(-2*x)` (c = 4).
  - *Discrete distributions* uses the Poisson pmf for the symbolic mean and variance: its `doit()` comes back clean, while a geometric pmf with a symbol `p` (even `positive=True`) gives a `Piecewise` with `|p - 1| < 1` that `sp.simplify` does not remove. The explanation says so, and the geometric sum uses `p = 1/4`.
  - *Moment generating functions*: `conds="none"` rather than a `t < lam` assumption (SymPy can't express t < λ as an assumption; `t` `negative=True` works but is misleading). Without `sp.simplify` the result is −λ/(t(1 − λ/t)), and `subs(t, 0)` on its derivatives gives `nan`, which the explanation names.
  - The Pitfall is kept, because `E(x**2)` with a plain Symbol fails silently; the `P` error is readable, but together they show the mix-up. `raises=ValueError`, with `P(...)` last.
  - `sympy.stats` names are imported with `from sympy.stats import (...)` after `import sympy as sp` and before `sp.init_printing()`. `moment_generating_function` is used under its full name, without an alias, so Students can look it up.
  - One back-link: SciPy stats' *Mean, spread and intervals* → `probability/distributions-in-sympy-stats`.
  - Code box width: at 1280 px the box's client width is 396 px, which fits about 43.6 characters of JetBrains Mono at 14 px, so every 44-character line on the site (e.g. in pandas' *Grouping*) scrolls by 6 px in the in-app browser. This Topic's longest line is 43 characters, so it doesn't scroll. The site-wide 44-character limit may need a look.
- **Links to add later** (their Topics are still planned):
  - *Normalising a pdf* → Equations' *Solving expr = 0*, and integrals' *Integrals to infinity*.
  - *Mean and variance* → integrals' *Integrals to infinity*.
  - *Discrete distributions* → integrals' *Sums*.
  - *Moment generating functions* → derivatives' *Higher derivatives*, and integrals' *Integrals to infinity*.
  - Keep at most three per Entry.
