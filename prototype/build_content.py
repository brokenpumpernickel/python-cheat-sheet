"""PROTOTYPE - throwaway. Sample content for the UI mockups in prototype/index.html.

Runs every example for real (ADR 0002) and writes prototype/content.js.
Usage: uv run prototype/build_content.py
"""

import json
import os
import re
import subprocess
import sys
import textwrap
from importlib.metadata import version
from pathlib import Path

HERE = Path(__file__).parent
PYTHON = sys.argv[1] if len(sys.argv) > 1 else sys.executable


def entry(title, explain, code, raises=None, pitfall=None, see=None):
    return {
        "title": title,
        "explain": explain,
        "code": textwrap.dedent(code).strip("\n"),
        "raises": raises,
        "pitfall": pitfall,
        "see": see or [],
    }


def pit(text, code=None, raises=None):
    return {"text": text, "code": textwrap.dedent(code).strip("\n") if code else None, "raises": raises}


AREAS = [
    {
        "id": "python-basics",
        "title": "Python Basics",
        "blurb": "The core language: names, control flow, functions and built-in collections.",
        "topics": [
            {
                "id": "variables",
                "title": "Variables",
                "glyph": "x =",
                "summary": "Naming values, basic types, converting between them.",
                "entries": [
                    entry(
                        "Assigning values",
                        "A variable is a name bound to a value with `=`. Python works out the type from the value; `type()` tells you what it is.",
                        """
                        n = 30
                        mean = 4.2
                        label = "trial A"
                        is_valid = True
                        print(n, mean, label, is_valid)
                        print(type(n), type(mean))
                        """,
                        pitfall=pit("`=` assigns a value, `==` compares two values. `if x = 3:` is a syntax error."),
                    ),
                    entry(
                        "Updating a variable",
                        "Augmented operators like `+=` and `*=` update a variable using its current value.",
                        """
                        total = 0
                        total += 5
                        total *= 2
                        print(total)
                        """,
                    ),
                    entry(
                        "Converting types",
                        "`int()`, `float()` and `str()` convert between types. Data read from files usually arrives as text and needs converting.",
                        """
                        print(int("42") + 1)
                        print(float("3.5") * 2)
                        print(str(7) + " samples")
                        print(round(2.71828, 2))
                        """,
                    ),
                ],
            },
            {
                "id": "strings",
                "title": "Strings",
                "glyph": "\"Aa\"",
                "summary": "Text, f-strings and formatting numbers.",
                "entries": [
                    entry(
                        "f-strings",
                        "Put an `f` before the quotes and write expressions in `{}`. After a colon you can format numbers: `.3f` for 3 decimals, `.1%` for a percentage.",
                        """
                        p = 0.04567
                        n = 120
                        print(f"n = {n}, p = {p:.3f}")
                        print(f"success rate: {0.8731:.1%}")
                        """,
                        pitfall=pit(
                            "You can't add a number to a string with `+`. Use an f-string or convert with `str()`.",
                            code='print("n = " + 120)',
                            raises="TypeError",
                        ),
                    ),
                    entry(
                        "Cleaning and splitting",
                        "`.strip()` removes surrounding whitespace and `.split(sep)` breaks a string into a list of pieces.",
                        """
                        line = "  12,15,9 \\n"
                        parts = line.strip().split(",")
                        print(parts)
                        print([int(p) for p in parts])
                        """,
                        see=["lists/list-comprehensions"],
                    ),
                ],
            },
            {
                "id": "conditionals",
                "title": "Conditionals",
                "glyph": "if",
                "summary": "Choosing what runs with if / elif / else.",
                "entries": [
                    entry(
                        "if / elif / else",
                        "Python checks each condition from the top and runs the first block whose condition is true. Blocks are defined by indentation.",
                        """
                        p = 0.03
                        if p < 0.01:
                            print("very strong evidence")
                        elif p < 0.05:
                            print("significant")
                        else:
                            print("not significant")
                        """,
                    ),
                    entry(
                        "Combining conditions",
                        "Combine conditions with `and`, `or` and `not`. Comparisons can be chained: `0 <= x <= 1`.",
                        """
                        x = 0.7
                        print(0 <= x <= 1)
                        print(x > 0.5 and x < 0.9)
                        print(not x > 0.5)
                        """,
                        pitfall=pit(
                            "`if x == 1 or 2:` is always true, because `2` on its own counts as true. Write `x == 1 or x == 2`, or `x in (1, 2)`.",
                        ),
                    ),
                ],
            },
            {
                "id": "loops",
                "title": "Loops",
                "glyph": "for",
                "summary": "Repeating work with for, range, enumerate and while.",
                "entries": [
                    entry(
                        "for over a collection",
                        "A `for` loop runs its block once for each item in a list, string or other collection.",
                        """
                        scores = [72, 85, 90]
                        for s in scores:
                            print(s - 70)
                        """,
                    ),
                    entry(
                        "range",
                        "`range(stop)` counts from 0 up to, but not including, `stop`. `range(start, stop, step)` gives more control.",
                        """
                        for i in range(3):
                            print(i)
                        print(list(range(2, 11, 4)))
                        """,
                        pitfall=pit("`range(5)` gives 0, 1, 2, 3, 4. It stops *before* 5."),
                    ),
                    entry(
                        "enumerate",
                        "`enumerate()` gives you the position and the item together, so you don't need a separate counter.",
                        """
                        for i, name in enumerate(["A", "B", "C"]):
                            print(i, name)
                        """,
                        see=["tuples/unpacking"],
                    ),
                ],
            },
            {
                "id": "functions",
                "title": "Functions",
                "glyph": "def",
                "summary": "Defining reusable code, arguments, return values.",
                "entries": [
                    entry(
                        "Defining and calling",
                        "`def` creates a function. `return` sends a value back to the caller. Call the function by writing its name with arguments in parentheses.",
                        """
                        def mean(values):
                            return sum(values) / len(values)

                        print(mean([2, 4, 9]))
                        """,
                        pitfall=pit(
                            "A function without `return` gives back `None`. Printing inside a function is not the same as returning.",
                            code="""
                            def mean(values):
                                print(sum(values) / len(values))

                            m = mean([2, 4, 9])
                            print(m)
                            """,
                        ),
                    ),
                    entry(
                        "Default arguments",
                        "Parameters can have default values, which are used when the caller leaves them out. Arguments can also be passed by name.",
                        """
                        def describe(x, digits=2):
                            return f"{x:.{digits}f}"

                        print(describe(3.14159))
                        print(describe(3.14159, digits=4))
                        """,
                    ),
                    entry(
                        "Returning several values",
                        "Return several values separated by commas; they come back as a tuple you can unpack into separate names.",
                        """
                        def spread(values):
                            return min(values), max(values)

                        low, high = spread([4, 8, 1, 6])
                        print(low, high)
                        """,
                        see=["tuples/unpacking"],
                    ),
                    entry(
                        "lambda",
                        "`lambda` makes a small one-line function without a name. It's most often used as the `key` when sorting.",
                        """
                        people = [("Ola", 23), ("Jan", 19), ("Ewa", 31)]
                        print(sorted(people, key=lambda p: p[1]))
                        """,
                        see=["lists/sorting"],
                    ),
                ],
            },
            {
                "id": "lists",
                "title": "Lists",
                "glyph": "[ ]",
                "summary": "Ordered, changeable sequences: indexing, slicing, sorting.",
                "entries": [
                    entry(
                        "Creating and indexing",
                        "A list holds items in order inside `[]`. Indexing starts at 0, and negative indexes count from the end.",
                        """
                        data = [3, 1, 4, 1, 5]
                        print(data[0])
                        print(data[-1])
                        print(len(data))
                        """,
                    ),
                    entry(
                        "Slicing",
                        "`data[start:stop]` takes a part of a list; `stop` is not included. Leave either one out to go to the start or end; add `:step` to skip items.",
                        """
                        data = [10, 20, 30, 40, 50]
                        print(data[1:3])
                        print(data[:2])
                        print(data[::2])
                        """,
                    ),
                    entry(
                        "Adding and removing",
                        "`.append()` adds one item at the end, `.extend()` adds several, and `.pop()` removes and returns an item (the last one by default).",
                        """
                        data = [1, 2]
                        data.append(3)
                        data.extend([4, 5])
                        last = data.pop()
                        print(data, last)
                        """,
                    ),
                    entry(
                        "Sorting",
                        "`sorted(x)` returns a new sorted list; `x.sort()` sorts the list in place and returns `None`.",
                        """
                        data = [3, 1, 2]
                        print(sorted(data, reverse=True))
                        data.sort()
                        print(data)
                        """,
                        pitfall=pit(
                            "`data = data.sort()` replaces your list with `None`.",
                            code="""
                            data = [3, 1, 2]
                            data = data.sort()
                            print(data)
                            """,
                        ),
                        see=["functions/lambda"],
                    ),
                    entry(
                        "List comprehensions",
                        "`[expression for item in collection]` builds a new list in one line. Add `if condition` at the end to keep only some items.",
                        """
                        data = [1, 2, 3, 4, 5, 6]
                        print([x ** 2 for x in data])
                        print([x for x in data if x % 2 == 0])
                        """,
                    ),
                    entry(
                        "Summaries",
                        "`len`, `sum`, `min` and `max` work on any list of numbers. Together they give quick descriptive statistics.",
                        """
                        data = [4, 8, 15, 16, 23, 42]
                        print(len(data), sum(data), min(data), max(data))
                        print(sum(data) / len(data))
                        """,
                    ),
                ],
            },
            {
                "id": "tuples",
                "title": "Tuples",
                "glyph": "( )",
                "summary": "Fixed, unchangeable groups of values and unpacking.",
                "entries": [
                    entry(
                        "Unpacking",
                        "A tuple is a fixed group of values in `()`. You can unpack it straight into separate names.",
                        """
                        point = (2.5, -1.0)
                        x, y = point
                        print(x, y)
                        """,
                        pitfall=pit(
                            "Tuples can't be changed after they are created. Use a list if you need to change the items.",
                            code="""
                            point = (2.5, -1.0)
                            point[0] = 3
                            """,
                            raises="TypeError",
                        ),
                    ),
                    entry(
                        "zip",
                        "`zip()` pairs up items from several lists by position, giving one tuple per position.",
                        """
                        xs = [1, 2, 3]
                        ys = [2.1, 3.9, 6.2]
                        for x, y in zip(xs, ys):
                            print(x, y)
                        """,
                    ),
                ],
            },
            {
                "id": "dictionaries",
                "title": "Dictionaries",
                "glyph": "{k:v}",
                "summary": "Looking values up by key: access, updating, looping, counting.",
                "entries": [
                    entry(
                        "Creating and accessing",
                        "A dictionary maps keys to values. Look a value up with `d[key]`.",
                        """
                        sample = {"mean": 4.2, "sd": 1.1, "n": 30}
                        print(sample["mean"])
                        print(len(sample))
                        """,
                    ),
                    entry(
                        "Missing keys",
                        "`d[key]` raises a `KeyError` if the key isn't there. `.get(key, default)` returns the default instead.",
                        """
                        sample = {"mean": 4.2}
                        print(sample.get("sd", 0.0))
                        print(sample["sd"])
                        """,
                        raises="KeyError",
                    ),
                    entry(
                        "Adding and updating",
                        "Assigning to a key adds it if it's new and replaces its value if it already exists.",
                        """
                        sample = {"n": 30}
                        sample["mean"] = 4.2
                        sample["n"] = 31
                        print(sample)
                        """,
                    ),
                    entry(
                        "Looping over items",
                        "`.items()` gives each key together with its value. `.keys()` and `.values()` give just one side.",
                        """
                        sample = {"mean": 4.2, "sd": 1.1}
                        for key, value in sample.items():
                            print(key, "->", value)
                        """,
                    ),
                    entry(
                        "Counting occurrences",
                        "A dictionary is a natural way to count how often each value appears, for example the outcomes of die rolls.",
                        """
                        rolls = [3, 6, 3, 1, 6, 6]
                        counts = {}
                        for r in rolls:
                            counts[r] = counts.get(r, 0) + 1
                        print(counts)
                        """,
                        see=["dictionaries/missing-keys"],
                    ),
                ],
            },
            {
                "id": "sets",
                "title": "Sets",
                "glyph": "{ }",
                "summary": "Unique values and set operations: union, intersection, difference.",
                "entries": [
                    entry(
                        "Unique values",
                        "A set keeps each value only once and has no order. `set(list)` is a quick way to remove duplicates.",
                        """
                        rolls = [3, 6, 3, 1, 6, 6]
                        print(set(rolls))
                        print(len(set(rolls)))
                        """,
                        pitfall=pit("`{}` is an empty **dictionary**. For an empty set, write `set()`."),
                    ),
                    entry(
                        "Set operations",
                        "`|` (union), `&` (intersection) and `-` (difference) work just like operations on events in probability.",
                        """
                        A = {1, 2, 3, 4}
                        B = {3, 4, 5}
                        print(A | B)
                        print(A & B)
                        print(A - B)
                        """,
                    ),
                ],
            },
        ],
    },
    {
        "id": "numpy",
        "title": "NumPy",
        "blurb": "Fast arrays and vectorised maths.",
        "placeholder": True,
        "topics": [{"id": t.lower().replace(" ", "-"), "title": t, "glyph": g, "placeholder": True}
                   for t, g in [("Arrays", "[[ ]]"), ("Indexing", "a[i]"), ("Random", "rng"), ("Aggregates", "Σ")]],
    },
    {
        "id": "pandas",
        "title": "pandas",
        "blurb": "Tables of data: DataFrames, filtering, grouping.",
        "placeholder": True,
        "topics": [{"id": t.lower().replace(" ", "-"), "title": t, "glyph": g, "placeholder": True}
                   for t, g in [("DataFrames", "df"), ("Selecting", "loc"), ("Grouping", "grp")]],
    },
    {
        "id": "matplotlib",
        "title": "Matplotlib",
        "blurb": "Plots for exploring and presenting data.",
        "topics": [
            {
                "id": "plotting-basics",
                "title": "Plotting basics",
                "glyph": "∿",
                "summary": "Line plots and histograms with labelled axes.",
                "entries": [
                    entry(
                        "Line plot",
                        "`plt.plot(x, y)` draws a line through the points. Always label the axes; `plt.show()` displays the figure.",
                        """
                        import numpy as np
                        import matplotlib.pyplot as plt

                        x = np.linspace(-4, 4, 200)
                        y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
                        plt.figure(figsize=(6, 3.2))
                        plt.plot(x, y)
                        plt.xlabel("x")
                        plt.ylabel("density")
                        plt.title("Standard normal PDF")
                        plt.show()
                        """,
                    ),
                    entry(
                        "Histogram",
                        "`plt.hist(data, bins=...)` shows how often values fall into each range. `density=True` scales the bars so their total area is 1.",
                        """
                        import numpy as np
                        import matplotlib.pyplot as plt

                        rng = np.random.default_rng(42)
                        sample = rng.normal(loc=0, scale=1, size=1000)
                        plt.figure(figsize=(6, 3.2))
                        plt.hist(sample, bins=30, density=True, edgecolor="white")
                        plt.xlabel("value")
                        plt.ylabel("density")
                        plt.title("1000 draws from N(0, 1)")
                        plt.show()
                        """,
                        see=["plotting-basics/line-plot"],
                    ),
                ],
            },
            {"id": "scatter", "title": "Scatter plots", "glyph": "⁘", "placeholder": True},
            {"id": "subplots", "title": "Subplots", "glyph": "▦", "placeholder": True},
        ],
    },
    {
        "id": "scipy-stats",
        "title": "SciPy stats",
        "blurb": "Distributions and statistical tests.",
        "placeholder": True,
        "topics": [{"id": t.lower().replace(" ", "-"), "title": t, "glyph": g, "placeholder": True}
                   for t, g in [("Distributions", "pdf"), ("t-tests", "t"), ("Correlation", "ρ")]],
    },
]

# Topic order = learning order (Trail, "Next stop"). Loops come after the collections they iterate over.
BASICS_ORDER = ["variables", "strings", "conditionals", "lists", "tuples", "dictionaries", "sets", "loops", "functions"]
AREAS[0]["topics"].sort(key=lambda t: BASICS_ORDER.index(t["id"]))

# These Entries use a loop before the Loops Topic (Topic order is a suggestion, not a prerequisite chain).
for e_title in ["Cleaning and splitting", "List comprehensions", "Looping over items", "Counting occurrences"]:
    for t in AREAS[0]["topics"]:
        for e in t.get("entries", []):
            if e["title"] == e_title:
                e["see"].append("loops/for-over-a-collection")

# ---------- Polish (ADR 0005). Prototype shortcut: one table here instead of next to each Entry. ----------
PL_AREAS = {
    "python-basics": ("Podstawy Pythona", "Rdzeń języka: nazwy, sterowanie przepływem, funkcje i wbudowane kolekcje."),
    "numpy": ("NumPy", "Szybkie tablice i obliczenia wektorowe."),
    "pandas": ("pandas", "Dane w tabelach: ramki danych (DataFrame), filtrowanie, grupowanie."),
    "matplotlib": ("Matplotlib", "Wykresy do eksploracji i prezentacji danych."),
    "scipy-stats": ("SciPy stats", "Rozkłady i testy statystyczne."),
}
PL_TOPICS = {
    "variables": ("Zmienne", "Zmienne (variables): nazywanie wartości, podstawowe typy i konwersja między nimi."),
    "strings": ("Napisy", "Napisy (strings): tekst, f-stringi i formatowanie liczb."),
    "conditionals": ("Warunki", "Instrukcje warunkowe (conditionals): wybór kodu do wykonania za pomocą if / elif / else."),
    "lists": ("Listy", "Listy (lists): uporządkowane, modyfikowalne sekwencje — indeksowanie, wycinanie, sortowanie."),
    "tuples": ("Krotki", "Krotki (tuples): stałe, niezmienne grupy wartości i ich rozpakowywanie."),
    "dictionaries": ("Słowniki", "Słowniki (dictionaries): wartości wyszukiwane po kluczu — odczyt, aktualizacja, iterowanie, zliczanie."),
    "sets": ("Zbiory", "Zbiory (sets): unikalne wartości i operacje na zbiorach — suma, iloczyn, różnica."),
    "loops": ("Pętle", "Pętle (loops): powtarzanie pracy z for, range, enumerate i while."),
    "functions": ("Funkcje", "Funkcje (functions): kod wielokrotnego użytku, argumenty, zwracane wartości."),
    "plotting-basics": ("Podstawy wykresów", "Wykresy liniowe i histogramy z opisanymi osiami."),
    "arrays": ("Tablice", None), "indexing": ("Indeksowanie", None), "random": ("Losowanie", None), "aggregates": ("Agregacje", None),
    "dataframes": ("Ramki danych", None), "selecting": ("Wybieranie", None), "grouping": ("Grupowanie", None),
    "scatter": ("Wykresy punktowe", None), "subplots": ("Podwykresy", None),
    "distributions": ("Rozkłady", None), "t-tests": ("Testy t", None), "correlation": ("Korelacja", None),
}
# "topic/entry": (title, explanation, pitfall-or-None)
PL_ENTRIES = {
    "variables/assigning-values": ("Przypisywanie wartości", "Zmienna to nazwa powiązana z wartością za pomocą `=`. Python sam ustala typ na podstawie wartości; `type()` pokazuje, jaki to typ.",
                                   "`=` przypisuje wartość, `==` porównuje dwie wartości. `if x = 3:` to błąd składni."),
    "variables/updating-a-variable": ("Aktualizowanie zmiennej", "Operatory złożone, takie jak `+=` i `*=`, zmieniają zmienną na podstawie jej bieżącej wartości.", None),
    "variables/converting-types": ("Konwersja typów", "`int()`, `float()` i `str()` zamieniają wartości między typami. Dane wczytane z plików zwykle są tekstem i trzeba je przekonwertować.", None),
    "strings/f-strings": ("f-stringi", "Postaw `f` przed cudzysłowem i wpisuj wyrażenia w `{}`. Po dwukropku możesz sformatować liczbę: `.3f` to 3 miejsca po przecinku, `.1%` to procent.",
                          "Nie da się dodać liczby do napisu za pomocą `+`. Użyj f-stringa albo zamień liczbę funkcją `str()`."),
    "strings/cleaning-and-splitting": ("Czyszczenie i dzielenie", "`.strip()` usuwa białe znaki z początku i końca, a `.split(sep)` dzieli napis na listę kawałków.", None),
    "conditionals/if-elif-else": ("if / elif / else", "Python sprawdza warunki od góry i wykonuje pierwszy blok, którego warunek jest prawdziwy. Bloki wyznacza wcięcie.", None),
    "conditionals/combining-conditions": ("Łączenie warunków", "Warunki łączy się za pomocą `and`, `or` i `not`. Porównania można łączyć w łańcuch: `0 <= x <= 1`.",
                                          "`if x == 1 or 2:` jest zawsze prawdziwe, bo samo `2` liczy się jako prawda. Napisz `x == 1 or x == 2` albo `x in (1, 2)`."),
    "lists/creating-and-indexing": ("Tworzenie i indeksowanie", "Lista przechowuje elementy po kolei w `[]`. Indeksy zaczynają się od 0, a ujemne liczą od końca.", None),
    "lists/slicing": ("Wycinanie (slicing)", "`data[start:stop]` wybiera fragment listy; `stop` nie wchodzi do wyniku. Pomiń jedno z nich, aby sięgnąć do początku lub końca; dodaj `:step`, aby przeskakiwać elementy.", None),
    "lists/adding-and-removing": ("Dodawanie i usuwanie", "`.append()` dodaje jeden element na końcu, `.extend()` dodaje kilka, a `.pop()` usuwa i zwraca element (domyślnie ostatni).", None),
    "lists/sorting": ("Sortowanie", "`sorted(x)` zwraca nową posortowaną listę; `x.sort()` sortuje listę w miejscu i zwraca `None`.",
                      "`data = data.sort()` zastępuje Twoją listę wartością `None`."),
    "lists/list-comprehensions": ("Wyrażenia listowe (list comprehensions)", "`[wyrażenie for element in kolekcja]` buduje nową listę w jednej linii. Dodaj na końcu `if warunek`, aby zostawić tylko niektóre elementy.", None),
    "lists/summaries": ("Podsumowania", "`len`, `sum`, `min` i `max` działają na każdej liście liczb. Razem dają szybkie statystyki opisowe.", None),
    "tuples/unpacking": ("Rozpakowywanie", "Krotka to stała grupa wartości w `()`. Można ją od razu rozpakować do osobnych nazw.",
                         "Krotek nie można zmieniać po utworzeniu. Jeśli chcesz zmieniać elementy, użyj listy."),
    "tuples/zip": ("zip", "`zip()` łączy w pary elementy z kilku list według pozycji, dając jedną krotkę na każdą pozycję.", None),
    "dictionaries/creating-and-accessing": ("Tworzenie i odczyt", "Słownik przypisuje wartości do kluczy. Wartość odczytuje się przez `d[klucz]`.", None),
    "dictionaries/missing-keys": ("Brakujące klucze", "`d[klucz]` zgłasza `KeyError`, jeśli klucza nie ma. `.get(klucz, domyślna)` zwraca wtedy wartość domyślną.", None),
    "dictionaries/adding-and-updating": ("Dodawanie i aktualizacja", "Przypisanie do klucza dodaje go, jeśli jest nowy, i zastępuje jego wartość, jeśli już istnieje.", None),
    "dictionaries/looping-over-items": ("Iterowanie po elementach", "`.items()` daje każdy klucz razem z wartością. `.keys()` i `.values()` dają tylko jedną stronę.", None),
    "dictionaries/counting-occurrences": ("Zliczanie wystąpień", "Słownik to naturalny sposób na policzenie, ile razy pojawia się każda wartość, np. wyniki rzutów kostką.", None),
    "sets/unique-values": ("Unikalne wartości", "Zbiór przechowuje każdą wartość tylko raz i nie ma kolejności. `set(lista)` to szybki sposób na usunięcie duplikatów.",
                           "`{}` to pusty **słownik**. Pusty zbiór zapisuje się jako `set()`."),
    "sets/set-operations": ("Operacje na zbiorach", "`|` (suma), `&` (iloczyn) i `-` (różnica) działają dokładnie jak działania na zdarzeniach w rachunku prawdopodobieństwa.", None),
    "loops/for-over-a-collection": ("for po kolekcji", "Pętla `for` wykonuje swój blok raz dla każdego elementu listy, napisu lub innej kolekcji.", None),
    "loops/range": ("range", "`range(stop)` liczy od 0 do `stop`, ale bez niego. `range(start, stop, step)` daje większą kontrolę.",
                    "`range(5)` daje 0, 1, 2, 3, 4. Kończy się *przed* 5."),
    "loops/enumerate": ("enumerate", "`enumerate()` daje jednocześnie pozycję i element, więc nie potrzebujesz osobnego licznika.", None),
    "functions/defining-and-calling": ("Definiowanie i wywoływanie", "`def` tworzy funkcję. `return` odsyła wartość do miejsca wywołania. Funkcję wywołuje się, pisząc jej nazwę z argumentami w nawiasach.",
                                       "Funkcja bez `return` zwraca `None`. Wypisanie wyniku wewnątrz funkcji to nie to samo, co jego zwrócenie."),
    "functions/default-arguments": ("Argumenty domyślne", "Parametry mogą mieć wartości domyślne, używane, gdy wywołujący ich nie poda. Argumenty można też przekazywać po nazwie.", None),
    "functions/returning-several-values": ("Zwracanie kilku wartości", "Zwróć kilka wartości oddzielonych przecinkami; wrócą jako krotka, którą można rozpakować do osobnych nazw.", None),
    "functions/lambda": ("lambda", "`lambda` tworzy małą, jednolinijkową funkcję bez nazwy. Najczęściej używa się jej jako `key` przy sortowaniu.", None),
    "plotting-basics/line-plot": ("Wykres liniowy", "`plt.plot(x, y)` rysuje linię przez punkty. Zawsze opisuj osie; `plt.show()` wyświetla wykres.", None),
    "plotting-basics/histogram": ("Histogram", "`plt.hist(data, bins=...)` pokazuje, jak często wartości wpadają do kolejnych przedziałów. `density=True` skaluje słupki tak, by ich łączne pole wynosiło 1.", None),
}

FIG_PREAMBLE = """
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as _plt
def _show(*a, **k):
    import io
    for n in _plt.get_fignums():
        buf = io.StringIO()
        _plt.figure(n).savefig(buf, format="svg", bbox_inches="tight")
        print("@@FIG@@" + buf.getvalue().replace("\\n", " ") + "@@END@@")
    _plt.close("all")
_plt.show = _show
"""


def run(code, raises, where):
    src = (FIG_PREAMBLE if "matplotlib" in code else "") + code
    proc = subprocess.run([PYTHON, "-I", "-X", "utf8", "-c", src], capture_output=True, text=True, encoding="utf-8",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    text, figures = [], []
    for line in proc.stdout.splitlines():
        if line.startswith("@@FIG@@"):
            figures.append(line[len("@@FIG@@"):-len("@@END@@")])
        else:
            text.append(line)
    error = None
    if proc.returncode != 0:
        last = proc.stderr.strip().splitlines()[-1]
        if not raises or not last.startswith(raises):
            sys.exit(f"{where}: unexpected error\n{proc.stderr}")
        error = last
    elif raises:
        sys.exit(f"{where}: expected {raises} but code ran fine")
    return {"text": "\n".join(text), "error": error, "figures": figures}


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


missing = []
for area in AREAS:
    area["pl"] = dict(zip(("title", "blurb"), PL_AREAS.get(area["id"], (None, None))))
    missing += [area["id"]] if not area["pl"]["title"] else []
    for topic in area["topics"]:
        title, summary = PL_TOPICS.get(topic["id"], (None, None))
        topic["pl"] = {"title": title, "summary": summary}
        missing += [topic["id"]] if not title or (not topic.get("placeholder") and not summary) else []
        for e in topic.get("entries", []):
            e["id"] = slug(e["title"])
            where = f"{topic['id']}/{e['id']}"
            pl = PL_ENTRIES.get(where)
            if not pl or bool(pl[2]) != bool(e["pitfall"]):
                missing.append(where)
            else:
                e["pl"] = {"title": pl[0], "explain": pl[1], "pitfall": pl[2]}
            e["output"] = run(e["code"], e["raises"], where)
            if e["pitfall"] and e["pitfall"]["code"]:
                e["pitfall"]["output"] = run(e["pitfall"]["code"], e["pitfall"]["raises"], where + " (pitfall)")
            print("ok", where)
if missing:
    sys.exit("Missing Polish for: " + ", ".join(missing))

v = sys.version_info
meta = {"versions": f"Python {v.major}.{v.minor} · NumPy {version('numpy')} · Matplotlib {version('matplotlib')}"}
(HERE / "content.js").write_text(
    "// PROTOTYPE - generated by build_content.py, do not edit\nwindow.CONTENT = "
    + json.dumps({"areas": AREAS, "meta": meta}, ensure_ascii=False)
    + ";\n",
    encoding="utf-8",
)
print("wrote content.js")
