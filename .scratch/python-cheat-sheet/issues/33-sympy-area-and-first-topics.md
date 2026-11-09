# 33: SymPy Area: the Topic order, Symbols and numbers, Simplifying expressions

**What to build:** A new Area, **SymPy**, for symbolic maths. The Author shows Students a SymPy notebook that covers:
- symbols, and exact and high-precision numbers;
- `diff`, `integrate`, `subs` and `evalf`;
- `solve`, matrices with eigenvalues, `dsolve`;
- plotting through `sp.plot` and `lambdify`.

This ticket adds the Area and lays out its 10 Topics, most as planned Topics. It writes the first two, which set the conventions for tickets 34–37, which then run in parallel.

Decided with the Author (every recommendation accepted). The English titles are decided; the Polish titles are the agent's.

- **The Area:**
  - `content/sympy/_area.md`, title **SymPy**, last in `content/areas.yaml` (after `scipy-stats`).
  - Hue 55 (yellow). That is the widest gap between the existing hues, and far from SciPy stats' 320, its neighbour.
  - A blurb in both Languages covering the 10 Topics.
- **The Topic order** (10), with these ids and English titles. Choose distinct glyphs per the guide; the suggestions are in brackets.
  1. `symbols`: **Symbols and numbers** (`Symbol`). Written here.
  2. `expressions`: **Simplifying expressions** (`expand`). Written here.
  3. `evaluating`: **Substituting and evaluating** (`subs`). Ticket 34.
  4. `derivatives`: **Derivatives and limits** (`diff`). Ticket 35.
  5. `integrals`: **Integrals and sums** (`∫`). Ticket 35.
  6. `equations`: **Equations** (`Eq`). Ticket 36.
  7. `matrices`: **Matrices** (`Matrix`). Ticket 36.
  8. `differential-equations`: **Differential equations** (`dsolve`). Ticket 36.
  9. `sympy-plots`: **Plotting with SymPy** (`sp.plot`). Ticket 34.
  10. `probability`: **Probability with SymPy** (`E(X)`). Ticket 37.

  Topics 3–10 are planned Topic files with a title, glyph and `pl.title`.
- **Conventions** (ticket 32 and its guide section *Maths*):
  - `import sympy as sp` and `sp.init_printing()` at the top of every example.
  - `display(...)` for symbolic results, which the site typesets.
  - `print(...)` for plain values, or where the one-line text form is the point.
  - Name symbols as Students do: `x = sp.Symbol("x")`, or `a, b = sp.symbols("a b")`.
- **Symbols and numbers** (`symbols`). The Entries, with these English titles:
  - **Symbols:** `sp.Symbol("x")` and `sp.symbols("a b c")`. A name like `"x_1"` or `"omega"` typesets as x₁ or ω. The Python variable and the symbol's name are separate things.
  - **Assumptions:** `sp.Symbol("n", integer=True)` makes `sp.sin(sp.pi * n)` give `0`, and `positive=True` makes `sp.sqrt(a**2)` give `a`. Show each with and without the assumption.
  - **Exact numbers:**
    - `sp.Rational(10, 3)` and `sp.Integer(358)**987`, which stays exact.
    - **Pitfall:** `1/3 * x` gives `0.333333333333333*x`, because Python divides first. Write `x / 3` or `sp.Rational(1, 3) * x`.
  - **Decimals to many digits:**
    - `.evalf(30)` or `sp.N(r, 30)` on a Rational, and `sp.pi.evalf(50)`.
    - `sp.Float("0.3", 30)` from text.
    - **Pitfall:** `sp.Float(0.3, 30)` keeps the binary error of the Python float 0.3 (`0.299999999999999988897769753748`).
  - **Constants:** `sp.pi`, `sp.E`, `sp.I` and `sp.oo`, which stay exact in expressions (`sp.exp(sp.I * sp.pi)` gives `-1`).
- **Simplifying expressions** (`expressions`). The Entries, with these English titles:
  - **Building expressions:**
    - Arithmetic on symbols, e.g. `3*x**2 + 2*x + 1`, and SymPy's functions `sp.sin`, `sp.exp`, `sp.sqrt` and `sp.log`.
    - **Pitfall:** `np.sin(x)` or `math.sin(x)` on a Symbol raises `TypeError` (`raises=TypeError`). Check the exact type in SymPy 1.14 and NumPy 2.
  - **Expanding and factoring:** `sp.expand((x + 1)**3)`, and `sp.factor(x**2 - 5*x + 6)` back.
  - **simplify:** `sp.simplify(sp.sin(x)**2 + sp.cos(x)**2)` and a fraction that cancels. Say that `simplify` tries many rules and can be slow, and that `expand` or `factor` say exactly what you want.
  - **Collecting terms:** `sp.collect(expr, x)` by powers of `x`, and `sp.apart` for partial fractions.
- **Style:**
  - Small symbolic examples with a physics or statistics flavour where natural (the notebook's `sp.exp(-a*x**2)`, a quadratic `a*x**2 + b*x + c`).
  - Outputs are typeset maths from `display` or values from `print`, never English sentences.
- **Links:**
  - NumPy's *Maths functions* (for the `np.sin` Pitfall) and Python Basics' Variables, where they help.
  - At most three per Entry.
  - Don't link to the planned Topics. List such links under **Links to add later**.

Conventions from tickets 12–24 apply:
- A blank line follows a compound block.
- "Polish term (English term)" at first mention, e.g. "symbol (symbol)", "założenia (assumptions)", "liczba wymierna (Rational)", "rozwinięcie (expand)".

**Blocked by:** 32 (typeset maths in Outputs, and SymPy installed).

**Status:** resolved

- [x] The SymPy Area is in `areas.yaml` with hue 55, a blurb in both Languages, and the 10 Topics in order, 3–10 as planned Topics with glyphs and Polish titles.
- [x] Symbols and numbers and Simplifying expressions are written with the decided Entries, Pitfalls and Polish.
- [x] Every example starts with `import sympy as sp` and `sp.init_printing()`, and runs alone in a fresh kernel with no warnings.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both pages were looked at in both Languages, with typeset maths in the Outputs and no code box scrolling sideways.
- [x] The Comments list every Entry with its Polish title, any decisions made on the way, and any Links to add later.
- [x] One session and one PR.

## Comments

- Resolved by the PR on branch `claude/sympy-area-f0b752` (link added after it is opened).
- **The Area:** `content/sympy/_area.md`, last in `areas.yaml`, hue 55. Blurb: "Symbolic maths with SymPy: symbols, exact numbers and simplifying, substituting, derivatives, integrals, equations, matrices, differential equations, plots and probability." / "Matematyka symboliczna w SymPy: symbole, liczby dokładne i upraszczanie, podstawianie, pochodne, całki, równania, macierze, równania różniczkowe, wykresy i prawdopodobieństwo."
- **Topics** (English / Polish, glyph), in the Topic order:
  1. `symbols`: *Symbols and numbers* / *Symbole i liczby*, `Sym`. Summary: "Symbols and exact numbers in SymPy: making symbols, assumptions, exact fractions, decimals to many digits and constants." / "Symbole (symbols) i liczby dokładne w SymPy: tworzenie symboli, założenia, dokładne ułamki, liczby dziesiętne z wieloma cyframi i stałe."
  2. `expressions`: *Simplifying expressions* / *Upraszczanie wyrażeń*, `(x+1)`. Summary: "Building and reshaping SymPy expressions: functions, expanding and factoring, simplify, collecting terms and partial fractions." / "Budowanie i przekształcanie wyrażeń (expressions) SymPy: funkcje, rozwijanie i rozkład na czynniki, simplify, grupowanie wyrazów i ułamki proste."
  3. `evaluating`: *Substituting and evaluating* / *Podstawianie i obliczanie*, `subs` (planned)
  4. `derivatives`: *Derivatives and limits* / *Pochodne i granice*, `diff` (planned)
  5. `integrals`: *Integrals and sums* / *Całki i sumy*, `∫` (planned)
  6. `equations`: *Equations* / *Równania*, `Eq` (planned)
  7. `matrices`: *Matrices* / *Macierze*, `Mat` (planned)
  8. `differential-equations`: *Differential equations* / *Równania różniczkowe*, `y''` (planned)
  9. `sympy-plots`: *Plotting with SymPy* / *Wykresy w SymPy*, `plot` (planned)
  10. `probability`: *Probability with SymPy* / *Prawdopodobieństwo w SymPy*, `E(X)` (planned)
- **Entries** (English / Polish):
  - Symbols and numbers:
    - *Symbols* / *Symbole (symbols)*: `a*x**2 + b*x + c`, then `w = sp.Symbol("omega")` and `x1 = sp.Symbol("x_1")` displayed (ω x₁) and printed (`omega*x_1`), which shows the variable/name split.
    - *Assumptions* / *Założenia (assumptions)*: plain `n` and `a` beside `n_int = sp.Symbol("n", integer=True)` and `a_pos = sp.Symbol("a", positive=True)`, so the Output pairs sin(πn) / 0 and √(a²) / a.
    - *Exact numbers* / *Liczby dokładne*: `print(10 / 3)` beside `sp.Rational(10, 3)` and `r + sp.Rational(1, 6)` (7/2); `sp.Integer(358)**987` printed as its digit count, 2521. Pitfall: `display(1/3 * x)` gives 0.333333333333333x.
    - *Decimals to many digits* / *Liczby dziesiętne z wieloma cyframi*: `r.evalf(30)`, `sp.N(r, 30)`, `sp.pi.evalf(40)`, `sp.Float("0.3", 30)`, all printed. Pitfall: `sp.Float(0.3, 30)` prints `0.299999999999999988897769753748`.
    - *Constants* / *Stałe*: e^{iπ} = −1, cos(π/6) = √3/2, √−4 = 2i, log(e³) = 3, ∞ + 1 = ∞.
  - Simplifying expressions:
    - *Building expressions* / *Budowanie wyrażeń (expressions)*: `3*x**2 + 2*x + 1`, `sp.exp(-a*x**2)`, `sp.sin(x) / sp.sqrt(x)`, `sp.log(x**2 + 1)`. Pitfall: `np.sin(x)`, `raises=TypeError`; in SymPy 1.14 / NumPy 2.5 the final line is `TypeError: loop of ufunc does not support argument 0 of type Symbol which has no callable sin method` (`math.sin(x)` raises `TypeError: Cannot convert expression to float`, named in the Pitfall text).
    - *Expanding and factoring* / *Rozwinięcie (expand) i rozkład na czynniki (factor)*: `sp.expand((x + 1)**3)`, `sp.factor(x**2 - 5*x + 6)`, `sp.factor(a**2 - b**2)`.
    - *simplify* / *Upraszczanie (simplify)*: sin²x + cos²x → 1, and (x² − 1)/(x − 1) displayed before and after → x + 1.
    - *Collecting terms* / *Grupowanie wyrazów (collect)*: `sp.collect(a*x**2 + b*x + 2*x**2 + 3*x, x)` and `sp.apart(1 / (x * (x + 1)))`.
- **Links:** *Symbols* → Variables' *Assigning values*; *Building expressions* → NumPy Array maths' *Maths functions* (for the `np.sin` Pitfall).
- **Links to add later:**
  - *Decimals to many digits* → Substituting and evaluating (ticket 34), the Entry on `evalf` / `subs`, once written.
  - *Building expressions* → Plotting with SymPy's `lambdify` Entry (ticket 34): it is the way to get a NumPy function from an expression, the fix the `np.sin` Pitfall points towards.
  - *Exact numbers* or *Symbols* → Equations (ticket 36), where `Rational` coefficients and symbol assumptions change what `solve` returns, if those Entries rely on them.
- **Conventions for tickets 34–37** (as used here):
  - Every example (Entry and Pitfall) starts `import sympy as sp`, `sp.init_printing()`, blank line.
  - `display(...)` for every symbolic result; `print(...)` for plain numbers, decimals from `evalf`, counts, and the one-line text form when it is the point (*Symbols* prints `omega*x_1`).
  - Symbols named as Students do: `x = sp.Symbol("x")`, `a, b = sp.symbols("a b")`; a symbol with an assumption gets its own Python name (`n_int`, `a_pos`) when it sits beside a plain one.
  - Printed text in an Output is not wrapped: it scrolls sideways past about 46 characters at 1280 px. Typeset maths that fits a 1280 px card is anything up to about the width of x²(a + 2) + x(b + 3).
- **Decisions:**
  - **Glyphs at most five characters**, as the guide says, so the suggestions that were longer changed: `Symbol` → `Sym`, `expand` → `(x+1)` (an expression, which is the Topic), `Matrix` → `Mat`, `dsolve` → `y''` (the unknown's second derivative, as in the harmonic oscillator), `sp.plot` → `plot`. `subs`, `diff`, `∫`, `Eq` and `E(X)` kept.
  - **π to 40 digits, not 50:** `sp.pi.evalf(50)` prints 52 characters, which made the Output scroll sideways at 1280 px; 40 digits (42 characters) fits.
  - **`sp.Integer(358)**987` is shown by its digit count** (2521), not displayed: its 2521 digits would be one long scrolling line.
  - **Constants** has no Pitfall (none was decided); the `math.pi` float mistake is one sentence of its explanation instead: `sp.sin(math.pi)` gives a tiny number, not 0.
  - **Polish titles carry the English term** where it is a SymPy/Python term (*Symbole (symbols)*, *Założenia (assumptions)*, *Budowanie wyrażeń (expressions)*, *Rozwinięcie (expand) i rozkład na czynniki (factor)*, *Upraszczanie (simplify)*, *Grupowanie wyrazów (collect)*), as Python Basics does (*Wycinanie (slicing)*). `Rational` and `Float` get theirs in the explanations.
  - **Checks:** every example ran alone in IPython with `-W default` and printed no warnings; `uv run cheatsheet build` passed, then `uv run pytest` (266 passed). Playwright screenshots at 1280 px of both Topics in EN and PL: all maths typeset, and no code box, Output or maths box scrolls sideways.
  - **Seen on the Map:** the planned *Prawdopodobieństwo w SymPy* bubble's long word runs slightly past its small dashed circle in Polish. It goes away when ticket 37 writes the Topic (written bubbles are larger); not changed here.
