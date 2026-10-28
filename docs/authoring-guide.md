# Authoring guide

How to add or edit content in `content/` so it builds and reads well the first time. It is written for AI agents working on the Author's behalf, and for the Author. Read it whole before your first content task; after that, the [validation rules](#validation-rules) and the [example Topic](#complete-example-topic) are the parts to come back to.

The content build (`cheatsheet/content.py`, then `cheatsheet/build.py`) is the only reader of these files. It checks everything in this guide that can be checked and runs every example. What it can't check (length, tone, Topic order, Polish quality) is up to you.

## Contents

- [Vocabulary](#vocabulary)
- [Folder layout](#folder-layout)
- [Area description](#area-description-_areamd)
- [Topic file](#topic-file-topic-idmd)
- [Entry](#entry): [title](#title), [explanation](#explanation), [code example](#code-example), [shown and run code](#shown-and-run-code), [Output](#output), [expected error](#expected-error), [figures](#figures), [figure description](#figure-description), [widgets](#widgets), [Pitfall](#pitfall), [See also](#see-also)
- [Topic order](#topic-order)
- [Polish](#polish)
- [New Areas: hue and glyphs](#new-areas-hue-and-glyphs)
- [Workflow](#workflow)
- [Validation rules](#validation-rules)
- [Complete example Topic](#complete-example-topic)
- [Before you finish](#before-you-finish)

## Vocabulary

Use the terms in `GLOSSARY.md` and avoid the synonyms it lists, in content, tickets, commit messages and code comments alike. The ones you need most:

| Term | Means | Not |
| --- | --- | --- |
| **Area** | A group of Topics, usually one library (Python Basics, NumPy) | section, category, chapter |
| **Topic** | One bubble on the Map with its own page (Lists, Functions) | section, page, card |
| **Entry** | One concept in a Topic: title, explanation, code example, Output | snippet, item, card, example |
| **Output** | What the code example produces when the build runs it | result, expected output |
| **Pitfall** | An optional callout about a common mistake | gotcha, warning, tip |
| **Topic order** | The learning order of Topics in an Area | sequence, curriculum |
| **Student** | The reader | user, learner |
| **Author** | Whoever writes the content: the teacher, or you | admin, editor |

The **Student** finished an intro programming course, works in a statistics and probability lab, and keeps the cheat sheet open in a side tab while working in Jupyter. They come to look something up, not to read a tutorial.

## Folder layout

```
content/
  areas.yaml              # Area order: a YAML list of Area ids
  python-basics/          # one folder per Area; the folder name is the Area id
    _area.md              # the Area description
    lists.md              # one file per Topic; the file name is the Topic id
```

Ids are lowercase letters and digits joined by `-`. Topic ids are unique across all Areas, because links are `#topic` and `#topic/entry`; if two libraries both want `indexing`, name one `numpy-indexing`. Every Area folder is listed in `areas.yaml`, and every Topic file is listed in its Area's Topic order.

Files are UTF-8. Write frontmatter values in double quotes when they contain `: ` or ` #`, or start with `[`, `{`, `"`, `'`, `*`, `&`, `!` or `%`. In double quotes a backslash is doubled (`"/\\"`); a value that contains `"` goes in single quotes (`'"Aa"'`).

## Area description (`_area.md`)

Frontmatter only, no body:

```yaml
---
title: Python Basics
blurb: "The core language: names, control flow, functions and built-in collections."
hue: 160                  # 0–360, the Area's colour; see "New Areas"
planned: false            # optional, default false; a planned Area lists only planned Topics
topics:                   # the Topic order, including planned Topics
  - lists
  - tuples
pl:
  title: Podstawy Pythona
  blurb: "Rdzeń języka: nazwy, sterowanie przepływem, funkcje i wbudowane kolekcje."
---
```

The blurb is one plain-text sentence (no Markdown) shown on the Overview.

## Topic file (`<topic-id>.md`)

Frontmatter, then the Entries in reading order:

```yaml
---
title: Lists
glyph: "[ ]"              # short symbol on the Topic's bubble; see "New Areas"
summary: "Ordered, changeable sequences: indexing, slicing, sorting."
pl:
  title: Listy
  summary: "Listy (lists): uporządkowane, modyfikowalne sekwencje — indeksowanie, wycinanie, sortowanie."
---
```

- **title**: the Topic's name, one to three words, title case in English.
- **summary**: one plain-text line (no Markdown) shown under the title: what the Topic is, then what its Entries cover. There's no fixed punctuation; the colon and dash in the examples are just one way to write it.
- A **planned** Topic (`planned: true`) shows Students what's coming. It has a title, a glyph and `pl.title`, no Entries and no body; `summary` and `pl.summary` may be left out. It can't be clicked and can't be linked to (see [See also](#see-also)). When you write its Entries, remove `planned: true` and add both summaries.

## Entry

Every Entry is a `##` section. **Pair rule:** every piece of English prose (the `##` title, the explanation, the Pitfall text, a figure description) is immediately followed by its Polish counterpart, a paragraph that starts with `PL:`.

````markdown
## Sorting

PL: Sortowanie

`sorted(x)` returns a new sorted list; `x.sort()` sorts the list in place and returns `None`.

PL: `sorted(x)` zwraca nową posortowaną listę; `x.sort()` sortuje listę w miejscu i zwraca `None`.

```python
data = [3, 1, 2]
print(sorted(data, reverse=True))
data.sort()
print(data)
```

### Pitfall

`data = data.sort()` replaces your list with `None`.

PL: `data = data.sort()` zastępuje twoją listę wartością `None`.

```python
data = [3, 1, 2]
data = data.sort()
print(data)
```

### See also

- functions/lambda
````

Inside a Topic file there is nothing but Entries, and inside an Entry nothing but what is shown above, in that order: title, `PL:` title, explanation, `PL:` explanation, one code block, then `### Figure` if that code draws a figure (see [Figure description](#figure-description)), then optionally `### Pitfall` (followed by a `### Figure` of its own if its code draws one) and `### See also`. No other headings, lists, quotes, tables, images or indented code.

### Title

- One to four words, sentence case, plain text: no backticks or other Markdown. `Sorting`, `List comprehensions`, `Missing keys`, `if / elif / else`.
- The **Entry id** is the English title slugified: `List comprehensions` → `list-comprehensions`, `if / elif / else` → `if-elif-else`. Links use it, so renaming an Entry breaks every See-also link to it (the build tells you which).
- When your task lists the Entry titles (the MVP's were decided by the Author), use them exactly and don't add, drop or rename Entries. Otherwise choose them yourself.
- The title names the concept or task the Student would look for, not the function alone: `Sorting`, not `sorted()`.

### Explanation

- **One paragraph of 1–3 sentences**, aim for under 50 words. The paragraph says what the thing does and the one detail people forget; the example shows the rest. It may state a side fact the example doesn't run ("so `t[0] = 1` raises `TypeError`"), but whatever is the Entry's main point is shown by the example.
- Lead with the syntax in backticks, then what it does: "`sorted(x)` returns a new sorted list; …".
- Inline Markdown only: `` `code` ``, `*emphasis*`, `**bold**`. Put every name, value and piece of syntax in backticks.
- Plain, direct and present tense. Address the Student as "you". No "simply", "just", "easy", no history and no comparisons with other languages.
- It describes this Entry's code, using the same names as the code where it helps.

### Code example

Exactly one ` ```python ` block per Entry, always with `python` as the language (not `py`, and never a bare ```` ``` ````).

- **Self-contained (ADR 0003).** Every example runs in its own fresh kernel, so it includes all its own imports and data and never uses a variable from another Entry. Repeating `import numpy as np` in every Entry is deliberate; don't factor it out. A Student must be able to paste the block into an empty Jupyter cell and run it.
- **Prints explicitly.** Show every value with `print(...)`. A bare expression on the last line prints nothing here: the build captures only what is printed (and figures), so `x + 1` as the last line gives an empty Output without any error. The exception is a figure Entry, whose Output is the figure.
- **Short and focused:** about 3–8 lines that show this Entry's concept and nothing else. Small, readable data with a statistics flavour (scores, measurements, dice rolls) beats `foo` and `bar`.
- **Pastes into the `python` prompt too.** Leave a blank line after a compound block (`for`, `while`, `if`, `def`) when an unindented line follows it. Jupyter doesn't need it, but pasted into the plain `python` prompt the next line is a `SyntaxError` without it.
- **Code is the same in both Languages.** Write names, strings and comments in English, and print values rather than sentences: `print(mean)` or `print("mean", mean)`, not `print(f"The mean is {mean}")`, since a Polish reader sees the same Output.
- **NumPy numbers are printed on their own.** Print a single NumPy number (`data.mean()`, `a[0]`) by itself, beside other values in one `print(x, y)`, or in an f-string, rounding long decimals where needed (`f"{x:.3f}"`). Never print it inside a list, tuple or dict: NumPy 2 then shows its type, `[np.float64(18.0)]`. Arrays print fine as they are.
- **Same Output on every build, no seed on the page.** The build seeds all randomness, but Students don't: in the lab they call `default_rng()` and `rvs` without a seed. So seed in the run code and show the unseeded form with a [`#| show:` marker](#shown-and-run-code): `rng = np.random.default_rng(7)  #| show: rng = np.random.default_rng()`. In SciPy, pass that generator as `random_state=rng` and show the call without it; hide the line that makes `rng` with `#| hide`, and `import numpy as np` too if nothing shown uses it. In NumPy always use a generator from `default_rng`, never the legacy `np.random.seed`; for the standard library, `random.seed(1)  #| hide`. Show the seed only where it is the point (NumPy's *A generator with a seed*, SciPy's *Reproducible samples*). Where the numbers matter to the explanation, say that the Student's will differ, because the Output comes from one run. Avoid the current date and time, memory addresses and anything else that changes between runs.
- **No outside world.** The kernel starts in an empty temporary folder with no input: an example that reads a file must write it first, and `input()` fails. Don't use the network; to show a download, read a local copy in the run code and show the download with `#| show:`. Each example has 60 seconds.
- **Libraries:** only what `pyproject.toml` installs (now NumPy, Matplotlib, SciPy and ipywidgets). To add one, run `uv add pandas` and add it to `EXAMPLE_LIBRARIES` in `cheatsheet/build.py`, so the footer shows the version the Outputs came from. Commit `uv.lock` with it.

### Shown and run code

The build runs the code block as written, and the page shows it with its marked lines changed (ADR 0006). A marker is a comment at the end of a line of code, after two or more spaces:

```python
rng = np.random.default_rng(7)  #| show: rng = np.random.default_rng()
sample = d.rvs(size=1000, random_state=rng)  #| show: sample = d.rvs(size=1000)
open("scores.csv", "w").write("72,45,88\n")  #| hide
data = np.loadtxt("scores.csv", delimiter=",")  #| show: data = np.loadtxt("https://example.org/scores.csv", delimiter=",")
```

- `code  #| show: <shown code>` runs `code` and shows `<shown code>` in its place, with the line's indentation kept.
- `code  #| hide` runs `code` and leaves the line out of what is shown. Blank lines left at the top of the shown code are dropped.
- Unmarked lines run exactly as shown. The marker is the last `#| ` on the line that follows two or more spaces; those spaces belong to neither the run code nor the shown code.
- The page, the Copy button, syntax highlighting and search all use the shown code. Entry and Pitfall code take markers alike.
- **Only for seeds and data sources.** The build can't check that a shown line means the same as its run line, so never use a marker to change what the example does or to hide a step the Output depends on. A Student who pastes the shown code must get the same kind of Output, only with other random numbers or the real data.

### Output

The Output is never written by hand (ADR 0002). The build runs the code and keeps what it prints, its figures and, for an expected error, the error's final line. Don't paste an Output into the file, and don't describe a specific printed value in the explanation in a way that would go stale if a library changed it.

The build ignores stderr, so a library warning doesn't fail it and doesn't show up anywhere. Run an example on its own with `uv run python example.py` (in a scratch folder) when you want to see its warnings, and change the code so it has none.

### Expected error

Add `raises=<ExceptionType>` to the code block's info string: ` ```python raises=KeyError `. The Output then shows what was printed before the error, then the error's final line (`KeyError: 'sd'`).

- **When:** the error *is* the point, because the Entry is about it (Missing keys), or a Pitfall's code shows a mistake that raises. Never mark an error to get a broken example past the build.
- Put the line that raises **last**: execution stops there, so nothing after it runs or prints. Print the working alternative before it.
- Use the exact class name from the error's final line: `KeyError`, not `LookupError` or `Exception`. For library errors use the bare class name (`LinAlgError`, not `numpy.linalg.LinAlgError`).
- The build fails if the example raises a different type, raises without the marker, or runs without an error despite it.

### Figures

Matplotlib draws with a non-interactive backend. Every figure open at `plt.show()` or at the end of the example becomes an SVG in the Output; a figure closed with `plt.close()` does not. Every example that draws a figure needs a [figure description](#figure-description).

- **One figure per Entry, one size.** Start it with `plt.figure(figsize=(6, 3.5))`, or pass `figsize=(6, 3.5)` to `plt.subplots`, keep Matplotlib's default style, and end the example with `plt.show()`, as Students do in Jupyter. Draw with the `plt` functions (`plt.plot`, `plt.xlabel`); use `ax.` methods only on the plots `plt.subplots` returns.
- **Text in figures is language-neutral,** because both Languages share the Output: symbols and maths (`x`, `f(x)`, `N(0, 1)`, `n = 30`, `σ = 2`), variable names (`a`, `r`), group letters (`A`, `B`) and numbers, or no text at all. No English words and no sentence-like titles: `plt.xlabel("height")` or `plt.title("Exam scores")` would stay English on the Polish page. Say in the explanation, in both Languages, what the axes show.
- **Random data** comes from a `default_rng` seeded in the run code and shown unseeded (`rng = np.random.default_rng(1)  #| show: rng = np.random.default_rng()`), as in any other example. The figure description describes the figure on the page, which comes from the seeded run.
- **Checking warnings:** a plain `uv run python example.py` opens a window at `plt.show()`. Run it with `MPLBACKEND=Agg` instead; then `plt.show()` warns that `FigureCanvasAgg is non-interactive`, which is expected, and any other warning needs a fix.

### Figure description

A Student using a screen reader can't see a figure, so every figure has a short description in both Languages, read out as the figure's name in the Language the Student chose. It goes in a `### Figure` section right after the code that draws the figure: one English paragraph and its `PL:` twin, nothing else.

````markdown
```python
import matplotlib.pyplot as plt

counts = {"A": 7, "B": 3}
plt.figure(figsize=(6, 3.5))
plt.bar(list(counts.keys()), list(counts.values()))
plt.show()
```

### Figure

Two bars, A and B; the A bar is more than twice as tall.

PL: Dwa słupki, A i B; słupek A jest ponad dwa razy wyższy.
````

- **When:** exactly when the code draws a figure. The build runs the example and fails if it drew a figure without a description, or if a description sits on an example that drew none.
- **A Pitfall's figure** gets its own `### Figure` after the Pitfall's code, below `### Pitfall`. A `### Figure` describes the code above it: before `### Pitfall` the Entry's, after it the Pitfall's.
- **One per example:** if the code draws several figures, one description covers them all, in the order they appear.
- **What to write:** one or two sentences saying what the plot shows and its notable shape, as a sighted Student would take it in at a glance: the kind of plot, what is on it, and the pattern that matters (a bell-shaped peak around 0, a line rising ever faster, the second bar tallest). Give a number only when the plot makes it stand out. Don't repeat the explanation, don't describe colours unless they carry meaning, and don't start with "Image of", "Figure showing" or "Wykres przedstawiający": the screen reader already says it's an image.
- **Plain text:** no Markdown, not even backticks, since it is read out, not shown. Write a name plainly (x, A) and describe the plot, not the code: "two bars", not "the Output of `plt.bar`".
- **Polish:** the same facts in natural Polish, under the usual [Polish](#polish) rules.

### Widgets

An example that calls `interact` (ipywidgets) shows controls above its plot in Jupyter. The build can't move them, so the Output is the figure at the starting values, with the controls drawn above it as a picture, captioned "Controls in Jupyter" so nobody tries to drag them.

- **Starting values** come from the function's defaults: `def plot(mu=0.0):` starts the `mu` slider at 0. Without a default, a slider starts in the middle of its range, a dropdown at its first option.
- **Supported controls:** sliders (`IntSlider`, `FloatSlider`, from `(min, max)` or `(min, max, step)`), dropdowns (`Dropdown`, from a list), checkboxes (`Checkbox`, from `True` / `False`) and text boxes (`Text`, from a string), made by `interact` or explicitly, also inside `VBox` / `HBox`. `fixed(...)` makes no control. Anything else, such as the button `interact_manual` adds, a `FloatLogSlider` or `RadioButtons`, fails the build (see [Running the examples](#running-the-examples)).
- **Descriptions and values are code** and are shown as they are in both Languages, so use code names or symbols (`mu`, `σ`, `n`), as for [text in figures](#figures).
- **The figure description** describes the plot at the starting values. The controls get their own screen-reader text in both Languages ("mu: slider from -3.00 to 3.00, at 0.00"), so don't list them in it.

### Pitfall

An optional `### Pitfall` section with one English paragraph, one `PL:` paragraph and optionally one ` ```python ` block (which may also carry `raises=`). Its code runs and is captured like the Entry's, in its own fresh kernel.

- **When:** a mistake Students really make with this concept, which gives a wrong result without complaint or an error that's hard to read: `data = data.sort()`, `counts[x] += 1` on a new key, `range(1, 10)` stopping at 9. Not a general tip, a style preference or a second concept. At most one per Entry, and most Entries have none.
- **Text:** one or two sentences naming the mistake and its effect. The interface already labels it ("Pitfall" / "Pułapka", with a "Watch out!" sticker), so don't start with "Pitfall:" or "Watch out".
- **With code** when running the mistake shows it: the Output is the surprising value, or the error marked with `raises=`. The code shows the mistake, not the fix (the Entry's own example is the fix).
- **Without code** when the mistake fits in the sentence and running it adds nothing: "`in` checks the keys only: `4.2 in stats` is `False`."

### See also

An optional `### See also` section with a bullet list of `topic-id/entry-id` references:

```markdown
### See also

- loops/for-over-a-collection
- functions/lambda
```

- **When:** the Entry uses a concept explained in another Entry (especially in a later Topic; see [Topic order](#topic-order)), or another Entry is the natural next step or contrast (`sorted(key=...)` → `functions/lambda`). One to three links; none is fine.
- Each reference must name an existing Entry. A link into a planned Topic fails the build until that Topic has Entries, so note it in the ticket and add it when the Entry exists.
- Links within the same Topic are allowed but rarely needed: the chips at the top of the page already list its Entries.

## Topic order

The `topics:` list in `_area.md` is the Topic order. It numbers the Trail and decides the Previous and Next stop on a Topic page.

- A Topic comes after the Topics its examples rely on: Loops after the collections they loop over, Functions last. A NumPy Topic may rely on any Python Basics Topic, since Python Basics comes first in `areas.yaml`.
- When an Entry needs a concept from a later Topic (Counting occurrences in Dictionaries uses a `for` loop, and Loops comes after Dictionaries), keep the order: use the concept as plainly as you can and add a See-also link to the later Entry that explains it. Don't move Topics around to fix one Entry.
- Entries in a Topic are in reading order too: the basic form first, variations and special cases after. A later Entry may rely on what an earlier one *explained*, never on its variables.
- The Python Basics Topic order is fixed by the spec (Variables, Strings, Conditionals, Lists, Tuples, Dictionaries, Sets, Loops, Functions). Changing an Area's Topic order is the Author's call.
- A new Topic goes at its place in that order among the Topics that already exist (Tuples right after Lists while Strings doesn't exist yet). Don't add the missing Topics as planned ones unless your task asks for it.

## Polish

Polish is required everywhere (ADR 0005), and the build fails without it: Area title and blurb, Topic title and summary (a planned Topic needs only its title), and every Entry's title, explanation, Pitfall text and figure description. Code and Outputs exist once and are shared.

- **Terminology rule:** name a Python concept in Polish with the English term in parentheses at its first mention, e.g. "krotka (tuple)", "Wycinanie (slicing)", "Wyrażenia listowe (list comprehensions)". Students meet the English term in error messages and documentation. "First mention" is per Entry, since Students land on single Entries from search: the first time the term appears in the Entry's Polish title, explanation or Pitfall text, whichever comes first. After that, write the Polish term alone; repeating the parentheses isn't an error, just noise. The Topic's Polish summary gets it once too. Ordinary words that aren't Python terms don't get it: "Sortowanie", "Podsumowania".
- Keep code as code: keywords, names, values and exception types stay in backticks and in English (`None`, `True`, `KeyError`, `.append()`).
- Write natural Polish that says the same as the English, with the same facts and the same inline code; don't translate word for word. Address the Student as "ty", with imperatives ("Użyj", "Dodaj", "Pomiń"), and write "twój", "twoja" in lowercase, since this is a reference, not a letter.
- **Agreed labels** (from `GLOSSARY.md`), for whenever Polish prose names a part of the interface: Output = **Wynik**, Pitfall = **Pułapka**, Map = **Mapa**, Trail = **Szlak**. The interface (`site/src/labels.ts`) also calls an Area "obszar", a Topic "temat" and an Entry "hasło".

## New Areas: hue and glyphs

To add an Area:

1. Create `content/<area-id>/_area.md` and add the id to `content/areas.yaml` where it belongs; libraries come after Python Basics.
2. For an Area that isn't written yet, set `planned: true` and give it only planned Topic files, each with a title, glyph and `pl.title`.
3. If its examples need a library that isn't installed, add it as described under [Code example](#code-example).

**Hue** is the hue of an HSL colour, a whole number from 0 to 360: 0 red, 30 orange, 55 yellow, 120 green, 160 sea green (Python Basics), 200 sky blue, 230 blue, 270 violet, 320 pink. It colours the island, the Topic page header and links to the Area's Entries.

- Contrast doesn't limit the choice. The palette is audited at every hue in both themes (ticket 09), so text on an Area's colour stays readable whatever you pick.
- Pick for distinctness: at least about 40° from every other Area's hue, and further from the Areas next to it in `areas.yaml`. List the hues in use with `grep -H "^hue" content/*/_area.md`.
- Changing the site's colours in `site/src/theme.css` is not a content task. If you have to, keep its rule of thumb: `--ink-3` text only on neutral surfaces (the sea, cards, code), and `--ink-2` or darker on an Area's colour. Then run `uv run pytest tests/test_accessibility.py`.

**Glyph** is the short monospaced symbol on a Topic's bubble, in the Index and on the Topic page header.

- One to five characters that look like the Topic's Python syntax: `[ ]` Lists, `( )` Tuples, `{k:v}` Dictionaries, `"Aa"` Strings, `for` Loops, `def` Functions, `if` Conditionals. For a library Topic, a short piece of what Students type for it: `rng` for random numbers, `df[ ]` for selecting, `.sum` for aggregates.
- Distinct within the Area, so Topics can be told apart at a glance.
- Always quote it, since glyphs often start with a character YAML treats specially.

## Workflow

1. **Read the task** and the files you'll touch: the Area's `_area.md` and the Topics before and after yours in Topic order. Match their tone, but where existing content disagrees with this guide (the Lists sample predates it), follow the guide.
2. **Write** the files. A new Topic is one file plus one line in its Area's `topics:`.
3. **Build:**

   ```bash
   uv run cheatsheet build
   ```

   The content build parses and validates everything, runs every example (each in a fresh kernel, up to 8 at a time), writes `generated/content.json`, then builds the site into `site/dist/` with Astro (installing the site's Node packages first if `site/node_modules` is missing). A good build logs a `ran <file> (topic-id/entry-id)` line per example, then Astro's log, and ends with `Built the site in …site/dist`. `generated/` and `site/dist/` are build output, ignored by git: never commit them.

4. **Read failures.** A content problem stops the build before Astro with `Content error:` and a message that starts with the place to fix: the file, often its line, and the Entry as `topic-id/entry-id`, e.g.

   ```
   Content error: python-basics/lists.md:56 (lists/sorting) See also: 'lists/sortng' names no Entry of Topic 'lists'; its Entries are: ...
   ```

   Parsing stops at the first problem, so fix it and build again; several parse problems take several builds. Examples run only when everything parses, and then every failing example is listed, one per line. Look the message up in [Validation rules](#validation-rules). A Python traceback instead of `Content error:` means the build itself broke, not the content; report it rather than working around it.

5. **Check the Outputs.** A clean build doesn't mean a good Output: an empty Output means a missing `print`, and an Output that doesn't show what the explanation promises means the example needs work. Look on the page (step 6), or list every Output from `generated/content.json`, one line per example (the Pitfall's on the line after its Entry's), in a POSIX shell such as Git Bash:

   ```bash
   uv run python -X utf8 -c "import json; d=json.load(open('generated/content.json',encoding='utf-8')); [print(f\"{t['id']}/{e['id']}\", repr(o['text']), o['error'] or '', f\"{len(o['figures'])} figure(s)\" if o['figures'] else '') for a in d['areas'] for t in a['topics'] for e in t['entries'] for o in [e['output']] + ([e['pitfall']['output']] if e['pitfall'] and e['pitfall']['output'] else [])]"
   ```

   In that file an Entry's Output is `output` (`text`, `error`, `figures`, `widgets`), and its Pitfall's is `pitfall.output` (`null` when the Pitfall has no code).
6. **Preview:**

   ```bash
   uv run cheatsheet serve
   ```

   Open http://127.0.0.1:4321/, find the Topic on the Map, open it and read every Entry. Check the Polish with the EN | PL switch or http://127.0.0.1:4321/?lang=pl. Stop the server with Ctrl+C.

7. **Test:**

   ```bash
   uv run pytest
   ```

   The tests use their own fixtures, not `content/`, so content changes rarely break them, but run them before a pull request anyway. The first time, install Chromium with `uv run playwright install chromium`. CI runs the tests and the same build (with `--base /python-cheat-sheet/`) on every pull request, so a failing example fails the check.

Manage Python only with uv: `uv run`, `uv add`. Don't use `pip` or a system Python.

## Validation rules

Every rule below stops the build with `Content error:`. The message starts with the place (left out in the table): a file such as `python-basics/lists.md`, often `:line`, and for an Entry `(topic-id/entry-id)`, followed by ` Pitfall`, ` Figure`, ` Pitfall Figure` or ` See also` when the problem is there. `<…>` stands for the part that varies.

### Areas and the Area order

| Message | Cause | Fix |
| --- | --- | --- |
| `areas.yaml: file not found in <folder>` | `content/areas.yaml` is missing | Create it: a YAML list of Area ids. |
| `areas.yaml: expected a list of Area ids` | It isn't a list of plain words | One `- area-id` line per Area. |
| `areas.yaml: Area '<id>' is listed twice` | Duplicate line | Remove one. |
| `<id>/: Area folder is not listed in areas.yaml` | A folder in `content/` isn't in the list | Add its id to `areas.yaml`, or remove the folder. |
| `areas.yaml: Area '<id>' has no <id>/_area.md` | Listed, but the folder or its `_area.md` is missing | Create `content/<id>/_area.md`, or remove the line. |
| `<id>/_area.md: an Area description has frontmatter only, no body` | Text after the closing `---` | Delete it; the description is the `blurb`. |
| `'topics' must be a list of Topic ids (the Topic order)` | `topics:` missing or not a list | Add `topics:` with one `- topic-id` per Topic. |
| `Topic order lists '<id>' twice` | Duplicate in `topics:` | Remove one. |
| `Topic order names '<id>', but there is no <area>/<id>.md` | Listed Topic has no file | Create the file (planned, if it isn't written yet), or fix the id. |
| `<area>/<id>.md: Topic is not listed in the Topic order of <area>/_area.md` | A Topic file isn't in `topics:` | Add it to `topics:` at its place in the Topic order. |
| `'hue' must be a whole number from 0 to 360` | `hue` missing, quoted, decimal or out of range | `hue: 210`, unquoted. |
| `<area>/<id>.md: a planned Area lists only planned Topics; add 'planned: true'` | A written Topic in a planned Area | Add `planned: true` to the Topic, or remove `planned: true` from the Area. |
| `<area>/<id>.md: Topic id '<id>' is also used in Area '<other>'` | Same file name in two Areas | Rename one file (e.g. `numpy-indexing.md`) and its line in `topics:`. |

### Frontmatter (Areas and Topics)

| Message | Cause | Fix |
| --- | --- | --- |
| `the file must start with YAML frontmatter between '---' lines` | No `---` on the first line, or no closing `---` | Start the file with `---`, the fields, then `---` on its own line. |
| `invalid YAML (<details>); quote values that contain ': '` | Usually an unquoted value with `: `, or one starting with `[`, `{`, `"` | Put the value in double quotes (see [Folder layout](#folder-layout)). |
| `the frontmatter must be a set of 'key: value' lines` | The frontmatter is a list or plain text | Write `key: value` lines. |
| `'<field>' is required and must be text` | `title`, `blurb`, `summary` or `glyph` missing or empty | Add it. A message starting `<file> pl:` means the Polish one under `pl:`. |
| `'pl' is required and must hold the Polish fields` | No `pl:` block | Add `pl:` with indented `title:` and `blurb:` (Area) or `title:` and `summary:` (Topic). |
| `'planned' must be true or false` | e.g. `planned: yes please` or `"true"` | `planned: true`, unquoted, or leave it out. |
| `'<id>' is not a valid id (lowercase letters, digits and '-')` | Area folder or Topic file name with capitals, `_` or spaces | Rename to e.g. `list-comprehensions.md`, and update `topics:` or `areas.yaml`. |

### Topics and Entries

| Message | Cause | Fix |
| --- | --- | --- |
| `a planned Topic has no Entries` | A planned Topic has a body | Delete the body, or remove `planned: true` and finish the Topic. |
| `a Topic needs at least one Entry (a '## ' section) unless it is planned` | Empty body | Write an Entry, or add `planned: true`. |
| `expected an Entry ('## Title') before any other content` | Text, or a `#` heading, before the first `##` | Delete it; the Topic's intro is its `summary`. |
| `two Entries have the id '<id>'; ids come from the titles, so change one title` | Two titles slugify alike (`Sorting` / `sorting!`) | Rename one. |
| `an Entry title needs letters or digits, since the Entry id is made from it` | Title like `## ???` | Use a word title. |
| `unexpected heading '<text>'; inside an Entry only '### Figure', '### Pitfall' and '### See also' are allowed` | Any other heading level or text, e.g. `### Example`, `#### Note`, `### Pitfalls` | Remove it, or spell it exactly `### Figure` / `### Pitfall` / `### See also`. |
| `'### <section>' appears twice` | Two Pitfalls, two See-also sections, or two figure descriptions for the same code | Keep one; an Entry has at most one Pitfall, and one description covers all the figures of an example. |
| `the heading must be followed by a 'PL: <Polish title>' paragraph` | No `PL:` line right after `##`, or it's in the wrong place | Add `PL: <Polish title>` as the next paragraph. |
| `the 'PL:' paragraph after the heading is empty; write the Polish title` | `PL:` with nothing after it | Write the Polish title. |
| `expected one English paragraph, found <n>` | Explanation (or Pitfall text) split into paragraphs, or missing | Join it into one paragraph of 1–3 sentences, or write it. |
| `expected one 'PL:' paragraph with the Polish text, found <n>` | Polish explanation (or Pitfall text) missing or split | One `PL:` paragraph after the English one. |
| `the 'PL:' paragraph at line <n> is empty; write the Polish text` | `PL:` with nothing after it | Write the Polish text. |
| `unexpected <kind> at line <n>; use paragraphs and ```python blocks only` | A bullet or ordered list, quote, rule or indented code in the explanation or Pitfall | Rewrite as one sentence-paragraph; code goes in the ` ```python ` block. |
| `an Entry needs exactly one ```python code block, found <n>` | No code block, or more than one | Keep exactly one; merge them or split the Entry. |
| `Pitfall: at most one ```python code block, found <n>` | Two blocks in the Pitfall | Keep one. |
| `the code block at line <n> has no language; fence examples as ```python` | A bare ```` ``` ```` fence | Write ` ```python `. |
| `code blocks must be ```python, not ```<lang> (line <n>)` | ` ```py `, ` ```pycon `, ` ```text `… | Use ` ```python `. Output isn't written in the file at all. |
| `unknown code block option '<option>'; the only option is raises=<ExceptionType>` | e.g. `raises KeyError`, `raises=KeyError,ValueError`, `title=…` | Write `raises=KeyError` with no spaces, one type. |
| `the code block at line <n> is empty` | ` ```python ` with nothing inside | Write the example. |
| `unknown marker '<marker>' at line <n>; the only markers are '#\| show: <code>' and '#\| hide', two spaces after the code` | A `#\|` comment that isn't a [marker](#shown-and-run-code): `#\| hidden`, `#\|show:x`, one space before it, or no code before it | Write `code  #\| show: <shown code>` or `code  #\| hide`. |
| `'#\| show:' at line <n> has no code after it; write the code to show, or use '#\| hide'` | `#\| show:` with nothing after it | Write the code to show, or use `#\| hide` to leave the line out. |
| `every line of the code block at line <n> is hidden; show at least one` | Every line has `#\| hide` | Show at least one line; an example the page can't show doesn't belong on it. |

### Figure descriptions

The place ends in ` Figure` for the Entry's description and ` Pitfall Figure` for the Pitfall's. The pair-rule messages above apply here too, e.g. `Figure: expected one 'PL:' paragraph with the Polish text, found 0` when the Polish is missing.

| Message | Cause | Fix |
| --- | --- | --- |
| `a figure description has no code block; it describes the figures of the code above it` | A ` ```python ` block inside `### Figure` | Move the code above `### Figure`; the section holds the two paragraphs only. |
| ``a figure description is plain text, read out as the figure's name; remove the Markdown (`code`, *emphasis*)`` | Backticks, `*`, a link or other Markdown in the description | Write it as plain text (see [Figure description](#figure-description)). |
| `the Pitfall has no code, so it draws no figure; remove the '### Figure' description` | A `### Figure` after a Pitfall without code | Remove it, or move it above `### Pitfall` if it describes the Entry's figure. |

### See also

| Message | Cause | Fix |
| --- | --- | --- |
| `See also: expected one bullet list of topic-id/entry-id references` | Not a bullet list, or text besides it | One list, one `- topic-id/entry-id` per line, nothing else. |
| `See also: '<item>' is not a topic-id/entry-id reference` | A title, a link, `#topic/entry`, backticks or an Entry id alone | Write `lists/sorting`: the ids, lowercase, no `#`. |
| `See also: '<ref>' names Topic '<id>', which does not exist` | Wrong Topic id | Use the Topic's file name, without `.md`. |
| `See also: '<ref>' points into planned Topic '<id>', which has no Entries yet` | Link to a planned Topic | Remove it for now; add it when that Topic has Entries. |
| `See also: '<ref>' names no Entry of Topic '<id>'; its Entries are: <ids>` | Wrong Entry id, or the Entry was renamed | Pick one from the list in the message. |

### Running the examples

These are checked only after everything parses, and all failures are listed at once. The place is `<file> (topic-id/entry-id)`, plus ` Pitfall` for the Pitfall's code; the two figure checks also give the Entry's line, `<file>:<line> (topic-id/entry-id)`.

| Message | Cause | Fix |
| --- | --- | --- |
| `the example failed with <Error>: <message>` | The code raises and isn't marked | Fix the code; it must run in a fresh kernel on its own (missing import, a variable from another Entry, a typo). If the error is the point, add `raises=<Error>`. |
| `the example failed with <Error>: <message> (marked raises=<Other>)` | It raises a different type than marked | Mark the exact type from the message, or fix the code so it raises the one you meant. |
| `marked raises=<Error>, but the example ran without an error` | Marked, but nothing raised | Make the line that should raise actually raise, or remove the marker. |
| `the example timed out after 60 s` | It was still running after 60 seconds: an endless loop, a long `sleep`, or too much data | Make it smaller; an example should finish in about a second. |
| `the example draws a figure but has no description; add a '### Figure' section after its code` (or `draws <n> figures`) | The code drew a figure, and no `### Figure` follows it | Add a [figure description](#figure-description) right after the code block (after the Pitfall's code when the place ends in ` Pitfall`). |
| `Figure: the example draws no figure; remove the '### Figure' description` | A description on code that drew nothing: no plotting, or every figure closed with `plt.close()` | Remove the section, or fix the code if it should draw. |
| `the example displays a <Model> widget, which the site can't draw yet` (e.g. `ButtonModel`) | The example shows a widget the site can't draw: `interact_manual`'s button, `FloatLogSlider`, `RadioButtons`… | Use a [supported control](#widgets) (`interact` instead of `interact_manual`, a `FloatSlider`, a dropdown). |

**Not caught by the build** (check them yourself): an empty Output from a missing `print`, warnings (stderr is ignored), Output that changes between builds, a `#| show:` line that doesn't mean the same as its run line, length, tone, Topic order and the quality of the Polish.

## Complete example Topic

A Dictionaries Topic that uses every Entry feature, with the Area description and a planned Topic it needs. It builds as shown. The notes after it explain each choice.

`content/python-basics/_area.md`:

```yaml
---
title: Python Basics
blurb: "The core language: names, control flow, functions and built-in collections."
hue: 160
topics:
  - lists
  - dictionaries                 # (1) listed in the Topic order
  - loops                        # (2) a planned Topic still has a file and a place in the order
pl:
  title: Podstawy Pythona
  blurb: "Rdzeń języka: nazwy, sterowanie przepływem, funkcje i wbudowane kolekcje."
---
```

`content/python-basics/loops.md` (2):

```yaml
---
title: Loops
glyph: "for"
planned: true
pl:
  title: Pętle
---
```

`content/python-basics/dictionaries.md`:

````markdown
---
title: Dictionaries
glyph: "{k:v}"
summary: "Values looked up by key: creating, missing keys, counting."
pl:
  title: Słowniki
  summary: "Słowniki (dictionaries): wartości wyszukiwane po kluczu — tworzenie, brakujące klucze, zliczanie."
---

## Creating and accessing

PL: Tworzenie i odczyt

A dictionary maps keys to values inside `{}`. Read a value with `d[key]`; `d[key] = value` adds a new key or changes an existing one.

PL: Słownik (dictionary) przypisuje kluczom (keys) wartości (values) w `{}`. Wartość odczytasz przez `d[key]`; `d[key] = value` dodaje nowy klucz albo zmienia istniejący.

```python
scores = {"Ala": 4.5, "Bartek": 3.0}
scores["Celina"] = 5.0
print(scores["Ala"])
print(scores)
```

### See also

- lists/creating-and-indexing

## Missing keys

PL: Brakujące klucze

Reading a key that is not in the dictionary raises `KeyError`. `d.get(key, default)` returns `default` instead.

PL: Odczyt klucza, którego nie ma w słowniku, zgłasza wyjątek `KeyError`. `d.get(key, default)` zwraca wtedy `default`.

```python raises=KeyError
stats = {"mean": 4.2, "n": 30}
print(stats.get("sd", 0.0))
print(stats["sd"])
```

### Pitfall

`in` checks the keys only: `"mean" in stats` is `True`, but `4.2 in stats` is `False`.

PL: `in` sprawdza tylko klucze: `"mean" in stats` daje `True`, ale `4.2 in stats` daje `False`.

## Counting occurrences

PL: Zliczanie wystąpień

`counts[x] = counts.get(x, 0) + 1` counts how often each value appears, starting from 0 the first time a value is seen.

PL: `counts[x] = counts.get(x, 0) + 1` zlicza, ile razy pojawia się każda wartość, zaczynając od 0, gdy wartość pojawia się pierwszy raz.

```python
rolls = [3, 6, 3, 1, 6, 3]
counts = {}
for roll in rolls:
    counts[roll] = counts.get(roll, 0) + 1
print(counts)
```

### Pitfall

`counts[x] += 1` fails the first time `x` is seen, because there is no count to add to yet.

PL: `counts[x] += 1` zawodzi, gdy `x` pojawia się pierwszy raz, bo nie ma jeszcze licznika, do którego można dodać 1.

```python raises=KeyError
counts = {}
counts["heads"] += 1
print(counts)
```

## Plotting counts

PL: Wykres zliczeń

`plt.bar(keys, values)` draws one bar per key. The figure open at `plt.show()` becomes the Output.

PL: `plt.bar(keys, values)` rysuje jeden słupek na klucz. Wykres otwarty w chwili `plt.show()` staje się Wynikiem.

```python
import matplotlib.pyplot as plt

counts = {"A": 7, "B": 3}
plt.figure(figsize=(6, 3.5))
plt.bar(list(counts.keys()), list(counts.values()))
plt.show()
```

### Figure

Two bars, A and B; the A bar is more than twice as tall.

PL: Dwa słupki, A i B; słupek A jest ponad dwa razy wyższy.
````

What it shows:

1. **The Topic is registered** in `topics:`, after Lists because its examples use lists. The file name `dictionaries.md` is the Topic id. The glyph is quoted because it starts with `{`; the summary is quoted because it contains `: `. The Polish summary names the concept with its English term: "Słowniki (dictionaries)".
2. **A planned Topic** (`loops.md`) has a title, glyph, `planned: true` and a Polish title, no summary and no body. It shows on the Map as a dashed bubble and can't be linked to yet.
3. **Creating and accessing** is a plain Entry with a **See-also link**. Its id is `creating-and-accessing`. The explanation is two sentences with the syntax in backticks; the Polish one gives "słownik (dictionary)", "klucz (key)" and "wartość (value)" at their first mention. The example prints both a single value and the whole dictionary, so the Output shows both things the explanation mentions.
4. **Missing keys** has an **expected error** and a **Pitfall without code**. The working alternative (`.get`) is printed first, and the line that raises comes last, so the Output is `0.0` and then `KeyError: 'sd'`. The Pitfall's point fits in one sentence, so it has no code.
5. **Counting occurrences** has a **Pitfall with code that raises**: it shows the mistake, not the fix, and is marked `raises=KeyError`, so its Output is `KeyError: 'heads'`. The Entry uses a `for` loop although Loops comes later. That is fine under the [Topic order](#topic-order) rule, and once Loops has Entries this Entry gets `- loops/for-over-a-collection` under `### See also`. Adding that link now would fail the build, because Loops is planned.
6. **Plotting counts** has a **figure**: no `print`, the bar chart is the Output, and it has no title or labels to translate. Its **figure description** says what a Student would see at a glance, two bars with A clearly taller, in plain text and in both Languages. (In the real content figures belong in the Matplotlib Area; this one is here so the example covers every feature.)

## Before you finish

- [ ] Every Entry: a title of one to four words, an explanation of 1–3 sentences in one paragraph, one self-contained ` ```python ` example that prints what it shows.
- [ ] Every Output comes from the build, is not empty, and shows what the explanation promises; no warnings.
- [ ] Expected errors only where the error is the point, with the raising line last.
- [ ] No seed or `random_state` on the page unless the seed is the point: seeds run hidden behind `#| show:` and `#| hide`, and markers are used for nothing but seeds and data sources.
- [ ] Every example that draws a figure has a `### Figure` description in both Languages: what the plot shows and its shape, in plain text.
- [ ] Pitfalls only for real, common mistakes; See-also links where an Entry relies on another.
- [ ] Polish for every title, summary, blurb, explanation, Pitfall and figure description, with "polski termin (English term)" at first mention.
- [ ] The Topic is in its Area's `topics:`, after the Topics its examples rely on.
- [ ] `uv run cheatsheet build` passes, you've looked at the Topic in `uv run cheatsheet serve` in both Languages, and `uv run pytest` passes.
