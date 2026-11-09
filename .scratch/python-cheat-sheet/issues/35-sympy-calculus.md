# 35: SymPy Derivatives and limits, and Integrals and sums

**What to build:** Two planned SymPy Topics, written, for the calculus Students do in the lab:
- **Derivatives and limits**;
- **Integrals and sums**, including the improper integrals and infinite sums that probability needs.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **Derivatives and limits** (`derivatives`). The Entries, with these English titles:
  - **Derivatives:** `expr.diff(x)` and `sp.diff(expr, x)` on the notebook's `sp.exp(-a*x**2)`.
  - **Higher derivatives:** `expr.diff(x, x)` and `expr.diff(x, 10)`.
  - **Partial derivatives:** `f.diff(x)` and `f.diff(x, y)` for a function of two symbols.
  - **Limits:**
    - `sp.limit(sp.sin(x)/x, x, 0)` and a limit at `sp.oo`.
    - One-sided with `dir="+"`, e.g. `1/x` at 0.
  - **Taylor series:** `sp.series(sp.exp(x), x, 0, 5)`, and `.removeO()` to drop the O(x⁵) term.
- **Integrals and sums** (`integrals`). The Entries, with these English titles:
  - **Indefinite integrals:**
    - `sp.integrate(expr, x)`.
    - Say that SymPy adds no constant.
    - A result with `erf` is fine; say what it is in one clause.
  - **Definite integrals:** `sp.integrate(expr, (x, -1, 1))`.
  - **Integrals to infinity:**
    - `sp.integrate(sp.exp(-a*x**2), (x, -sp.oo, sp.oo))` with `a` positive gives `sqrt(pi)/sqrt(a)`.
    - **Pitfall:** without `positive=True` on `a`, the result is a `Piecewise` with conditions. Show it.
  - **Unevaluated integrals:** `sp.Integral(...)` shows the integral itself; `.doit()` computes it. This is handy to display the question beside the answer.
  - **Sums:**
    - `sp.Sum(k**2, (k, 1, n)).doit()`.
    - An infinite geometric series, `sp.Sum(p**k, (k, 0, sp.oo))`, and its condition on `p`.
    - Also `sp.summation`.
- **Conventions** are ticket 33's: `import sympy as sp` and `sp.init_printing()` at the top, `display(...)` for symbolic results, `print(...)` for plain values. Read `symbols.md` and `expressions.md` and match them. Assumptions on symbols are explained in Symbols and numbers' *Assumptions*; link there.
- **Links:**
  - Symbols and numbers' *Assumptions* and *Constants*.
  - Between the two Topics.
  - At most three per Entry.

**Running in parallel** with tickets 34, 36 and 37. Each runs in its own session and PR.
- Edit only `derivatives.md` and `integrals.md`, plus at most two back-links elsewhere, not in the files the other tickets edit (`evaluating.md`, `sympy-plots.md`, `equations.md`, `matrices.md`, `differential-equations.md`, `probability.md`).
- Don't touch `_area.md`.
- The other tickets' Topics are still planned, so don't link to them. List any link you'd add under **Links to add later** in the Comments. Ticket 37 (Probability) will want to link to your *Integrals to infinity*, *Sums* and *Higher derivatives*, so keep those titles.
- If `main` moves and your PR conflicts, bring your branch up to date with `main` and resolve it. Check that the PR is still OPEN before every push.

Conventions from tickets 12–24 apply:
- Outputs show values, not English sentences.
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "pochodna (derivative)", "granica (limit)", "całka oznaczona (definite integral)", "szereg Taylora (Taylor series)".

**Blocked by:** 33 (the SymPy Area and its conventions).

**Status:** resolved

- [x] Both Topics are written (no longer planned), with summaries in both Languages and the decided Entries with their Polish, including the `Piecewise` Pitfall.
- [x] Every example runs alone in a fresh kernel with no warnings.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages, with typeset maths and no code box scrolling sideways.
- [x] The Comments list every Entry with its Polish title, any decisions made on the way, and any Links to add later.
- [x] One session and one PR.

## Comments

- Resolved by PR #56: https://github.com/brokenpumpernickel/python-cheat-sheet/pull/56.
- **Topics** (English / Polish, glyph unchanged):
  - `derivatives`: *Derivatives and limits* / *Pochodne i granice*, `diff`. Summary: "Derivatives and limits of SymPy expressions: diff, higher and partial derivatives, one-sided limits and Taylor series." / "Pochodne (derivatives) i granice (limits) wyrażeń SymPy: diff, pochodne wyższych rzędów i cząstkowe, granice jednostronne i szereg Taylora."
  - `integrals`: *Integrals and sums* / *Całki i sumy*, `∫`. Summary: "Integrals and sums in SymPy: indefinite and definite integrals, integrals to infinity, unevaluated integrals and finite and infinite sums." / "Całki (integrals) i sumy w SymPy: całki nieoznaczone i oznaczone, całki do nieskończoności, całki nieobliczone oraz sumy skończone i nieskończone."
- **Entries** (English / Polish):
  - Derivatives and limits:
    - *Derivatives* / *Pochodne (derivatives)*: `f.diff(x)` and `sp.diff(f, x)` on `sp.exp(-a*x**2)`, both −2ax·e^(−ax²), plus `sp.diff(x**3 + 2*x, x)`.
    - *Higher derivatives* / *Pochodne wyższych rzędów (higher derivatives)*: `f.diff(x, x)` and `f.diff(x, 2)` on the same `f`, and `sp.sin(2*x).diff(x, 10)` = −1024 sin(2x).
    - *Partial derivatives* / *Pochodne cząstkowe (partial derivatives)*: `f = x**2 * y + sp.sin(x*y)`, then `f.diff(x)`, `f.diff(y)`, `f.diff(x, y)`.
    - *Limits* / *Granice (limits)*: sin(x)/x at 0 → 1, (1 + 1/x)^x at `sp.oo` → e, `1/x` at 0 with `dir="+"` → ∞ and `dir="-"` → −∞. Pitfall: `sp.limit(1/x, x, 0)` without `dir` gives ∞, because the default direction is from the right.
    - *Taylor series* / *Szereg Taylora (Taylor series)*: `sp.series(sp.exp(x), x, 0, 5)` with its O(x⁵), `.removeO()`, and `sp.series(sp.cos(x), x, 0, 6)`.
  - Integrals and sums:
    - *Indefinite integrals* / *Całki nieoznaczone (indefinite integrals)*: x² + cos x → x³/3 + sin x (no constant added), and e^(−x²) → √π·erf(x)/2, with `erf` named as the error function the normal CDF is built from.
    - *Definite integrals* / *Całki oznaczone (definite integrals)*: x² over (−1, 1) → 2/3; e^(−x²) over (−1, 1) → √π·erf(1), then `area.evalf()` printed (1.49364826562485).
    - *Integrals to infinity* / *Całki do nieskończoności*: with `a = sp.Symbol("a", positive=True)`, e^(−ax²) over (−∞, ∞) → √π/√a; 1/x² from 1 → 1 (converges); 1/x from 1 → ∞ (diverges). Pitfall: with a plain `a`, the same integral is a `Piecewise`: √π/√a for |arg(a)| ≤ π/2, the unevaluated integral otherwise.
    - *Unevaluated integrals* / *Całki nieobliczone (Integral)*: `q = sp.Integral(x * sp.exp(-x), (x, 0, sp.oo))` displayed, `q.doit()` → 1, and `sp.Eq(q, q.doit())` for the question beside its answer.
    - *Sums* / *Sumy (Sum)*: `sp.Sum(k**2, (k, 1, n))` displayed and `.doit()` → n³/3 + n²/2 + n/6; `sp.Sum(p**k, (k, 0, sp.oo)).doit()` → a `Piecewise` with 1/(1 − p) for |p| < 1; `sp.summation(1/k**2, (k, 1, sp.oo))` → π²/6.
- **Links:**
  - In these Topics: *Derivatives* → Simplifying expressions' *Building expressions*; *Limits* → *Constants*; *Indefinite integrals* → *Derivatives*; *Definite integrals* → *Decimals to many digits*; *Integrals to infinity* → *Assumptions* and *Constants*; *Sums* → *Constants*.
  - Back-links (two): Symbols and numbers' *Assumptions* → *Integrals to infinity*; Simplifying expressions' *Building expressions* → *Derivatives*.
- **Links to add later** (those Topics are planned now):
  - *Derivatives* → Substituting and evaluating (ticket 34), the `subs` Entry, for a derivative's value at a point.
  - *Definite integrals* → Substituting and evaluating (ticket 34), the `evalf` / numeric Entry.
  - *Unevaluated integrals* → Equations (ticket 36), the `sp.Eq` Entry, since it uses `sp.Eq` to show the question beside the answer.
  - *Higher derivatives* or *Partial derivatives* → Differential equations (ticket 36), the Entry on `sp.Function` and `x(t).diff(t, t)`.
  - *Higher derivatives*, *Integrals to infinity* and *Sums* → Probability with SymPy (ticket 37): moments from the moment generating function, mean and variance as integrals, and sums for a discrete distribution. Ticket 37 links the other way.
- **Decisions:**
  - **A second Pitfall, on *Limits*:** SymPy's `limit` defaults to `dir="+"`, so `sp.limit(1/x, x, 0)` gives ∞ although the two-sided limit doesn't exist. It is a real, silent mistake, so it is a Pitfall. (`dir="+-"` returns `zoo` here in SymPy 1.14, not an error, so the Pitfall doesn't show it.)
  - **10th derivative of `sp.sin(2*x)`, not of `sp.exp(-a*x**2)`:** the 10th derivative of the Gaussian is a long polynomial that would scroll; −1024 sin(2x) shows the point in one short line. `f.diff(x, 2)` beside `f.diff(x, x)` shows the two spellings agree.
  - **Indefinite integral of `sp.exp(-x**2)`, not `sp.exp(-a*x**2)`:** with a plain `a`, SymPy returns a `Piecewise` on `Ne(a, 0)`, which belongs to the *Integrals to infinity* Pitfall, not here.
  - **Convergent and divergent beside the Gaussian:** *Integrals to infinity* adds 1/x² (→ 1) and 1/x (→ ∞) from 1, so the Student sees what a divergent integral returns.
  - **`sp.Eq(q, q.doit())`** is used for "the question beside the answer", ahead of Equations; the explanation says what it does.
  - **Code width:** every shown line is at most 44 characters (40 in Pitfalls); long calls were shortened with a named `f`, and `sp.Integral(...)` is wrapped inside its brackets.
  - **Checks:** every example ran alone in IPython with `PYTHONWARNINGS=default` and printed no warnings. `uv run cheatsheet build` passed, then `uv run pytest`: 264 passed, 2 Playwright language tests failed and passed when rerun alone (flaky). Both Topics were checked in the browser in EN and PL: all maths typeset (no KaTeX errors), the widest maths 376 px, and no code box, Output or maths scrolls sideways at a 1280 px layout.
  - **Seen on the way (not changed):** in the app's browser pane, Windows draws a 15 px scrollbar, so a 1280 px window lays out at 1265 px and any 44-character code line (also existing ones, such as Plotting basics' `plt.fill_between(...)`) overflows its box by 6 px. At a 1280 px layout it fits. The 44-character limit may be one character too generous for browsers with classic scrollbars.
