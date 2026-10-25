# 13: Content review batch: the Author's notes on the MVP

**What to build:** One batch update from the Author's review of the live MVP content, with each note settled by a decision:

- **Strings:** a new Entry with a table of useful number formats (decimal places, significant digits, width, zero padding, thousands separator, percent, scientific). The content format has no tables, so the example loops over format specs and prints each beside its formatted result, which makes the table a generated Output (ADR 0002). It uses a `for` loop before Loops, so it links to `loops/for-over-a-collection`.
- **Dictionaries:** a new Entry *Keys and values* for `.keys()` and `.values()`; *Looping over items* stays focused on `.items()`. A new `defaultdict` Entry.
- **Standard library:** a new Area (Polish *Biblioteka standardowa*) after Python Basics in the Area order, with a hue spaced from the others. A `collections` Topic holds `Counter` and is kept small; it links to the `defaultdict` Entry rather than repeating it. `itertools` is a planned Topic. *Counting occurrences* keeps its manual example and links to the `Counter` Entry.
- **Loops:** a new `while` Entry whose example halves a value until it drops below a threshold, with a Pitfall about loops that never end. No infinite loop runs. The `zip` Entry moves from Tuples into Loops under a looping title; *for over a collection* and Tuples' *Unpacking* link to it. This amends ticket 11's Entry list.
- **Authoring guide:** a line under "Code example" saying a compound block needs a blank line after it so the example also pastes into the plain `python` prompt (found in ticket 12).

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] Strings has a number-format Entry whose Output is the table, with a See-also link to `loops/for-over-a-collection`.
- [x] Dictionaries has *Keys and values* and a `defaultdict` Entry; *Looping over items* covers `.items()` only.
- [x] The Standard library Area exists after Python Basics, with a spaced hue, a `collections` Topic with `Counter`, and a planned `itertools` Topic; *Counting occurrences* links to `Counter`.
- [x] Loops has a `while` Entry with a Pitfall about loops that never end, and none of its code loops forever.
- [x] The `zip` Entry is in Loops, linked from *for over a collection* and *Unpacking*; ticket 11's Comments note the change.
- [x] The authoring guide has the blank-line rule under "Code example".
- [x] Every new or changed example runs alone with `uv run python` in an empty folder, its stdout matches the Output, it has no warnings and it pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass, and the changed Topics and the new Area were looked at in both Languages.

## Comments

**Resolved.** All of the Author's notes are in one PR. Python Basics now has 33 Entries (29 + 5 new − 1 moved out of Tuples), and the new Standard library Area has 2.

New and moved Entries, for the Author to skim (English / Polish, `topic-id/entry-id`):

- **Strings:** *Number formats* / *Formaty liczb* (`strings/number-formats`), new, after f-strings. The example loops over seven specs (`.2f`, `.3g`, `10.2f`, `010.2f`, `,.2f`, `.1%`, `.2e`) and prints each spec beside a large value and a small one, so the Output is an aligned three-column table. It uses `format(x, spec)`, which the explanation ties to `f"{x:spec}"`. See also: `loops/for-over-a-collection`.
- **Dictionaries:**
  - *Keys and values* / *Klucze i wartości* (`dictionaries/keys-and-values`), new, before *Looping over items*. It has a prose Pitfall: `in` checks only the keys, so use `7 in counts.values()`.
  - *Grouping with defaultdict* / *Grupowanie z defaultdict* (`dictionaries/grouping-with-defaultdict`), new and last. It groups measurements with `defaultdict(list)` and mentions `defaultdict(int)` for counting. Its Pitfall has code: reading a missing key quietly adds it.
  - *Looping over items* now covers `.items()` only. *Counting occurrences* keeps its manual example and links to `collections/counting-with-counter`.
- **Loops:**
  - *Looping with zip* / *Pętla z zip* (`loops/looping-with-zip`), moved from Tuples' *zip* and placed after *enumerate*. A prose Pitfall was added: `zip` silently drops the extra items of a longer collection, and `strict=True` raises `ValueError` instead. *for over a collection* and Tuples' *Unpacking* link to it.
  - *while loops* / *Pętla while* (`loops/while-loops`), new and last. It halves `error` from `1.0` until it drops below `0.01`, then prints the number of steps and the final value. The Pitfall about a loop that never ends is prose only: nothing runs forever. It says how to stop one (Kernel → Interrupt Kernel in Jupyter, Ctrl+C in a terminal).
- **Standard library** / *Biblioteka standardowa* (new Area, after Python Basics, hue 90):
  - Topic *collections* (glyph `Ctr`): *Counting with Counter* / *Zliczanie z Counter* (`collections/counting-with-counter`), which links to *Counting occurrences* and *Grouping with defaultdict*; and *Most common values* / *Najczęstsze wartości* (`collections/most-common-values`), with `.most_common(n)` and `.total()`. No more than that, to keep it small. `defaultdict` stays in Dictionaries.
  - Topic *itertools* (glyph `iter`), planned.

Other changes:

- **Summaries:** the Tuples, Dictionaries and Loops summaries list their new Entries (EN and PL).
- **Ticket 11:** its Comments note the move of `zip`.
- **Authoring guide:** a "Pastes into the `python` prompt too" bullet under "Code example" (the blank line after a compound block).
- **Hue:** 90 sits between Matplotlib 25 and Python Basics 160, at 65° and 70°, and 120° from NumPy, its other neighbour in `areas.yaml`.
- **Checked:** every new or changed example (11 Entries, 2 Pitfalls with code) ran alone with `uv run python` in an empty folder. Stdout matched the Output and stderr was empty, apart from the expected `TypeError` in *Unpacking*'s Pitfall. Each was also fed line by line to `code.InteractiveConsole` like a REPL paste: no `SyntaxError`, same output. `uv run cheatsheet build` and `uv run pytest` pass. The changed Topics and the new Area were looked at in `uv run cheatsheet serve` in both Languages.

For the Author to check:

- The Polish.
- The glyphs `Ctr` and `iter`, and hue 90.
- The Topic titles: `collections` and `itertools` are written as the module names, lowercase in both Languages, the way the pandas Area is.
- The two Pitfalls added beyond the notes: *Keys and values* (`in` checks keys) and *Looping with zip* (silent truncation).
- `.total()` in *Most common values* needs Python 3.10 or later.
