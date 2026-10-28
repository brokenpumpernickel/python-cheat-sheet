# 23: Reading and writing files: a Python Basics Files Topic and a NumPy Saving and loading Topic

**What to build:** Students need to read data from files and save results, both in plain Python and with NumPy. Two new Topics cover it: **Files** in Python Basics (text files, lines, numbers, CSV, paths) and **Saving and loading** in NumPy (text and CSV with `loadtxt`/`savetxt`/`genfromtxt`, binary `.npy` and `.npz`).

Decided with the Author (every recommendation accepted):

- **Python Basics: Files** (`files`, *Pliki*). It goes last in the Python Basics Topic order, after Functions; its examples rely on Strings, Lists and Loops. Choose a glyph per the authoring guide, e.g. `open`. The Entries (6), with these English titles; the Polish titles are the agent's:
  - **Writing a text file:** `with open("notes.txt", "w", encoding="utf-8") as f:` and `f.write(...)`; `with` closes the file. **Pitfall:** `"w"` erases what was in the file, and `"a"` adds to the end instead.
  - **Reading a whole file:** `f.read()`, and `.splitlines()` for a list of lines.
  - **Reading line by line:** `for line in f:`. **Pitfall:** every line keeps its `"\n"`; use `line.strip()`.
  - **Reading numbers from a file:** one value per line, `float(line.strip())`, then a sum or mean.
  - **CSV files with the csv module:** `csv.reader` for reading, and `csv.writer` with `newline=""` when writing. Rows come back as lists of strings, so convert numbers.
  - **Where Python looks for files:** a relative path starts from the working folder, which in Jupyter is the notebook's folder; `os.getcwd()` shows it. A missing file raises `FileNotFoundError`, an expected error (`raises=FileNotFoundError`).
  - **Encoding:** every `open` passes `encoding="utf-8"`. Say why once, in *Writing a text file* or *Reading a whole file*: on Windows the default encoding garbles Polish letters. Show a Polish word, e.g. `"źdźbło"`, round-tripping.
- **NumPy: Saving and loading** (`array-files`, since `files` is taken; *Zapis i odczyt*). It goes last in the NumPy Topic order, after Random. Choose a glyph, e.g. `.npy`. The Entries (6), with these English titles; the Polish titles are the agent's:
  - **Text files with savetxt and loadtxt:** `np.savetxt("data.txt", a, fmt="%.2f")` and `np.loadtxt("data.txt")`, for 1-D and 2-D arrays.
  - **CSV files:** `delimiter=","`, `skiprows=1` to skip a header line, and `usecols=` to pick columns.
  - **Columns as separate arrays:** `x, y = np.loadtxt(..., delimiter=",", unpack=True)`.
  - **Missing values with genfromtxt:** empty fields become `nan`. **Pitfall:** `np.loadtxt` raises `ValueError` on the same file (`raises=ValueError`).
  - **Binary files with save and load:** `np.save("a.npy", a)` / `np.load("a.npy")` keep the exact values and the dtype, and are fast. Mention that `np.save` adds `.npy` itself if it's missing.
  - **Several arrays in an npz file:** `np.savez("data.npz", x=x, y=y)`, then `d = np.load("data.npz")`, `d["x"]` and `d.files`. Mention `np.savez_compressed` for large arrays.
- **Files that reading examples need** (ticket 20's markers):
  - Reading examples create their file in hidden `#| hide` lines, so the shown code is only the reading. The explanation says what the file contains, and the Output shows it as read.
  - Writing examples write and then read back in plain sight, so the Output shows what was written.
  - Examples run in an empty temporary folder, so no file is left anywhere that matters.
  - No `#| show:` paths to the web: that's for a later ticket.
- **Printing:** NumPy numbers are printed on their own, or whole arrays printed, as the guide says. For text read back, print it with `print(...)` or `repr(...)` when the `"\n"` is the point (the line-by-line Pitfall).
- **Links:** two-way See-also links between the matching Entries in the two Topics, e.g. *CSV files with the csv module* ↔ *CSV files*, and *Reading numbers from a file* ↔ *Text files with savetxt and loadtxt*. Add links to Strings' *Cleaning and splitting* and Loops' *for over a collection* where natural, and to NumPy Aggregates' *Along an axis* for column statistics. At most three per Entry. pandas `read_csv` stays for the planned pandas Area.

Conventions from tickets 12–22 apply: Outputs show values, not English sentences; a blank line follows a compound block so examples paste into the `python` REPL; "Polish term (English term)" at first mention, e.g. "plik (file)", "kodowanie (encoding)", "ścieżka (path)", "katalog roboczy (working directory)"; seeds, if any randomness is needed, in hidden `np.random.seed` lines.

**Blocked by:** none.

**Status:** resolved

- [x] Python Basics has the Files Topic last in its Topic order, and NumPy has Saving and loading last in its order, each with its Polish title and a distinct glyph.
- [x] The 12 Entries exist with the decided English titles, each with Polish, including the Pitfalls (`"w"` erases, lines keep `"\n"`, `loadtxt` on missing values) and the expected `FileNotFoundError`.
- [x] Every `open` passes `encoding="utf-8"`, and one Entry says why, with a Polish word round-tripping.
- [x] Reading examples create their files in hidden lines, and each explanation says what the file contains; writing examples read back visibly.
- [x] Two-way See-also links connect the two Topics, plus the other links above.
- [x] Every example runs alone with `uv run python` in an empty folder (with its hidden lines), with no warnings, and pastes into the REPL.
- [x] `uv run cheatsheet build` and `uv run pytest` pass. Both Topics were looked at on the Map, the Trail and their pages in both Languages in `uv run cheatsheet serve`.
- [x] The Comments list every Entry with its Polish title.
- [x] One session and one PR, which also adds this ticket file.

## Comments

- Resolved by the PR for branch `claude/ticket-23-reading-and-writing-files-a4bf67` (link added below once it is open).
- **Topics:**
  - `content/python-basics/files.md`: *Files* / *Pliki*, glyph `open`, last in the Python Basics Topic order (after Functions). Summary: "Text files: writing, reading whole files and lines, numbers, CSV, and where Python looks for them." / "Pliki (files) tekstowe: zapis, odczyt całych plików i wierszy, liczby, CSV oraz miejsce, w którym Python ich szuka."
  - `content/numpy/array-files.md`: *Saving and loading* / *Zapis i odczyt*, glyph `.npy`, last in the NumPy Topic order (after Random). Summary: "Arrays in files: text and CSV with savetxt, loadtxt and genfromtxt, binary .npy and .npz files." / "Tablice (arrays) w plikach: tekst i CSV przez savetxt, loadtxt i genfromtxt, binarne pliki .npy i .npz."
- **Entries** (English / Polish):
  - Files:
    - *Writing a text file* / *Zapis pliku tekstowego*, with the `"w"` erases / `"a"` appends Pitfall; says why `encoding="utf-8"` and round-trips `"źdźbło"`
    - *Reading a whole file* / *Odczyt całego pliku*
    - *Reading line by line* / *Odczyt wiersz po wierszu*, with the `"\n"` Pitfall (`"Jan" in names` is `False`)
    - *Reading numbers from a file* / *Odczyt liczb z pliku*
    - *CSV files with the csv module* / *Pliki CSV z modułem csv*
    - *Where Python looks for files* / *Gdzie Python szuka plików*, `raises=FileNotFoundError`
  - Saving and loading:
    - *Text files with savetxt and loadtxt* / *Pliki tekstowe z savetxt i loadtxt*
    - *CSV files* / *Pliki CSV*
    - *Columns as separate arrays* / *Kolumny jako osobne tablice*
    - *Missing values with genfromtxt* / *Brakujące wartości z genfromtxt*, with the `np.loadtxt` Pitfall (`raises=ValueError`)
    - *Binary files with save and load* / *Pliki binarne z save i load*
    - *Several arrays in an npz file* / *Kilka tablic w pliku npz*
- **Links:** *Reading numbers from a file* ↔ *Text files with savetxt and loadtxt*; *CSV files with the csv module* ↔ *CSV files*. Also: *Reading a whole file* → Strings' *Cleaning and splitting*; *Reading line by line* → Loops' *for over a collection* and *Cleaning and splitting*; *Reading numbers from a file* → *for over a collection*; *CSV files with the csv module* → Lists' *List comprehensions*; *CSV files* → Aggregates' *Along an axis*; *Text files with savetxt and loadtxt* → Arrays' *Two-dimensional arrays*; *Columns as separate arrays* → Tuples' *Unpacking* and Scatter plots' *A scatter plot*; *Missing values with genfromtxt* → Indexing's *Changing values through a mask*; *Binary files with save and load* → Arrays' *Shape and dtype*. At most three per Entry.
- Decisions:
  - **NumPy needs `encoding="utf-8"` too.** On Windows, `np.loadtxt` and `np.genfromtxt` open a file in the locale encoding (cp1252), so a UTF-8 file whose header has a Polish letter such as `Ł` raises `UnicodeDecodeError`, even when `skiprows` / `skip_header` skips that header (checked with NumPy 2.5.4). So every NumPy example that reads a file with a header passes `encoding="utf-8"`, and *CSV files* says why in one sentence. *Text files with savetxt and loadtxt* (numbers only, no header) keeps the decided `np.loadtxt("data.txt")`.
  - **`os.getcwd()` is named, not printed.** Its Output would be the build's random temporary folder, different on every build. *Where Python looks for files* prints `os.listdir()` and `os.path.exists(...)` instead, and its explanation says what `os.getcwd()` shows. The missing file is a typo, `"score.txt"` for `"scores.txt"`.
  - **Hidden file creation:** each reading example creates its file in one hidden line, `with open(..., "w", encoding="utf-8") as f: f.write(...)  #| hide`, so it is closed at once and also passes the encoding. *CSV files with the csv module* both writes and reads, so it needs no hidden line.
  - **Line length:** the long NumPy calls are wrapped with a hanging indent, so they stay within 43 characters except `with open("data.txt", encoding="utf-8") as f:` (45). The Files lines with `encoding="utf-8"` are longer (up to 66 characters, the CSV `open` with `newline=""`), like other Python Basics lines.
  - The Python Basics blurb ("…functions and built-in collections") was left as it is.
- All 15 examples (12 Entries and 3 Pitfalls) were run alone with `uv run python -W default` in their own empty folders, with their hidden lines: no warnings, and the build's Outputs match those runs. Each was also pasted, line by line, into `code.InteractiveConsole` after its hidden lines: no `SyntaxError`.
- `uv run cheatsheet build` and `uv run pytest` (237 tests) pass, run one after the other. In `uv run cheatsheet serve`, the `open` bubble shows on the Python Basics island and `.npy` on the NumPy island. On the Trail, Files is stop 10 and Saving and loading stop 6. Both pages were read in English and Polish: the hidden lines aren't shown, the See-also links work, and the Previous and Next stops are Functions → collections and Random → Plotting basics.
