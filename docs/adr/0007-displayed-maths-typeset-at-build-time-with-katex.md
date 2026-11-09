# Displayed maths is typeset at build time with KaTeX

This extends ADR 0002 and ADR 0004 for the SymPy Area. In Jupyter, `display(expr)` after `sp.init_printing()` shows a SymPy result as typeset maths, and Students read it that way in the lab. So the build keeps the LaTeX of each displayed result (the `text/latex` of a `display_data` message), in order with the printed text, and the Astro build typesets it with KaTeX's `renderToString`, in display mode with `htmlAndMathml` output. The page then shows what Students see in Jupyter, needs no maths script, and gives screen readers MathML. KaTeX's CSS and fonts are bundled with the site from npm. LaTeX that KaTeX can't typeset fails the build, naming the Entry, so a page never shows broken maths.

## Considered Options

- **Plain text** (`print(expr)`, or the `text/plain` of a display): rejected as the only form. `x**2 + 2*x + 1` is not how Students see results in Jupyter, and fractions, roots, matrices and integrals read badly as text. `print` stays for plain values and where the text form is the point.
- **MathJax or KaTeX in the browser**: rejected. It adds a script to a page that otherwise only shows, hides and animates what the build rendered, the maths would pop in after the page loads, and the Outputs would depend on the client.
- **The PNG that SymPy's `init_printing` makes**: rejected. It is an image (no MathML, no text colour in the dark theme), and drawing it with Matplotlib's mathtext took seconds per result, so kernels don't make PNGs at all.
- **MathJax at build time**: KaTeX is smaller, faster, and covers the LaTeX SymPy prints; if it ever can't, the build says so.

## The Output data

An Output's printed text and displayed maths are one ordered list of parts, `{"text": ...}` or `{"maths": <LaTeX>}`, replacing the single `text` string. Neighbouring text is joined into one part, so an Output with text only is one part and looks as before. A `display_data` with only `text/plain` (`display(3)` without `init_printing`) is text, as Jupyter shows it. Figures, widgets and the error line keep their places.
