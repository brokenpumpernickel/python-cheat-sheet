---
title: Files
glyph: "open"
summary: "Text files: writing, reading whole files and lines, numbers, CSV, and where Python looks for them."
pl:
  title: Pliki
  summary: "Pliki (files) tekstowe: zapis, odczyt całych plików i wierszy, liczby, CSV oraz miejsce, w którym Python ich szuka."
---

## Writing a text file

PL: Zapis pliku tekstowego

`with open("notes.txt", "w", encoding="utf-8") as f:` opens a file for writing, `f.write(text)` writes a string to it, and `with` closes the file when the block ends. Always pass `encoding="utf-8"`: on Windows the default encoding garbles Polish letters such as `ź`.

PL: `with open("notes.txt", "w", encoding="utf-8") as f:` otwiera plik (file) do zapisu, `f.write(text)` zapisuje w nim napis (string), a `with` zamyka plik po zakończeniu bloku. Zawsze podawaj `encoding="utf-8"`: w Windowsie domyślne kodowanie (encoding) psuje polskie litery, takie jak `ź`.

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("źdźbło\n")
    f.write("n = 30\n")

with open("notes.txt", encoding="utf-8") as f:
    print(f.read())
```

### Pitfall

`"w"` empties the file before writing, so opening it with `"w"` a second time erases what was there. Open it with `"a"` (append) to add to the end instead.

PL: `"w"` opróżnia plik przed zapisem, więc ponowne otwarcie z `"w"` kasuje to, co w nim było. Aby dopisać na końcu, otwórz plik z `"a"` (append).

```python
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("run 1\n")

with open("log.txt", "w", encoding="utf-8") as f:
    f.write("run 2\n")

with open("log.txt", encoding="utf-8") as f:
    print(f.read())
```

## Reading a whole file

PL: Odczyt całego pliku

`f.read()` returns the whole file as one string, and `.splitlines()` splits that string into a list of lines without their `"\n"`. Here `cities.txt` holds three city names, one per line.

PL: `f.read()` zwraca cały plik (file) jako jeden napis (string), a `.splitlines()` dzieli ten napis na listę wierszy bez ich `"\n"`. Tutaj `cities.txt` zawiera trzy nazwy miast, po jednej w wierszu.

```python
with open("cities.txt", "w", encoding="utf-8") as f: f.write("Łódź\nKraków\nGdańsk\n")  #| hide
with open("cities.txt", encoding="utf-8") as f:
    text = f.read()

print(repr(text))
print(text.splitlines())
```

### See also

- strings/cleaning-and-splitting

## Reading line by line

PL: Odczyt wiersz po wierszu

`for line in f:` reads the file one line at a time, so even a large file never has to fit in memory at once. Here `names.txt` holds three names, one per line.

PL: `for line in f:` czyta plik (file) po jednym wierszu, więc nawet duży plik nie musi naraz zmieścić się w pamięci. Tutaj `names.txt` zawiera trzy imiona, po jednym w wierszu.

```python
with open("names.txt", "w", encoding="utf-8") as f: f.write("Ala\nJan\nEwa\n")  #| hide
names = []
with open("names.txt", encoding="utf-8") as f:
    for line in f:
        names.append(line.strip())

print(names)
print("Jan" in names)
```

### Pitfall

Every `line` keeps its `"\n"` at the end, so without `line.strip()` the list holds `"Jan\n"` and `"Jan" in names` is `False`.

PL: Każdy `line` zachowuje na końcu swoje `"\n"`, więc bez `line.strip()` lista zawiera `"Jan\n"`, a `"Jan" in names` daje `False`.

```python
with open("names.txt", "w", encoding="utf-8") as f: f.write("Ala\nJan\nEwa\n")  #| hide
names = []
with open("names.txt", encoding="utf-8") as f:
    for line in f:
        names.append(line)

print(names)
print("Jan" in names)
```

### See also

- loops/for-over-a-collection
- strings/cleaning-and-splitting

## Reading numbers from a file

PL: Odczyt liczb z pliku

A line read from a file is always a string, so convert it with `float(line.strip())` before doing maths with it. Here `heights.txt` holds three heights in centimetres, one per line.

PL: Wiersz odczytany z pliku (file) jest zawsze napisem (string), więc zamień go przez `float(line.strip())`, zanim zaczniesz na nim liczyć. Tutaj `heights.txt` zawiera trzy wzrosty w centymetrach, po jednym w wierszu.

```python
with open("heights.txt", "w", encoding="utf-8") as f: f.write("168.5\n175.0\n181.5\n")  #| hide
heights = []
with open("heights.txt", encoding="utf-8") as f:
    for line in f:
        heights.append(float(line.strip()))

print(heights)
print(sum(heights) / len(heights))
```

### See also

- array-files/text-files-with-savetxt-and-loadtxt
- loops/for-over-a-collection

## CSV files with the csv module

PL: Pliki CSV z modułem csv

`csv.writer(f).writerows(rows)` writes one comma-separated line per row, and `csv.reader(f)` reads them back as lists of strings, so convert the numbers yourself. Open CSV files with `newline=""`, or on Windows every row is followed by an empty line.

PL: Z modułu (module) `csv` funkcja `csv.writer(f).writerows(rows)` zapisuje każdy wiersz jako linię wartości rozdzielonych przecinkami, a `csv.reader(f)` odczytuje je z powrotem jako listy napisów (strings), więc liczby trzeba zamienić samodzielnie. Pliki CSV otwieraj z `newline=""`, bo inaczej w Windowsie po każdym wierszu pojawia się pusty wiersz.

```python
import csv

rows = [["name", "score"], ["Ala", 72], ["Jan", 85]]
with open("scores.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

with open("scores.csv", newline="", encoding="utf-8") as f:
    back = list(csv.reader(f))

print(back)
print([int(r[1]) for r in back[1:]])
```

### See also

- array-files/csv-files
- lists/list-comprehensions
- csv-files/reading-a-csv-file

## Where Python looks for files

PL: Gdzie Python szuka plików

A relative path such as `"scores.txt"` starts from the working directory, which in Jupyter is the notebook's folder; `os.getcwd()` shows its full path and `os.listdir()` the files in it. Opening a file that isn't there raises `FileNotFoundError`; here the folder holds only `scores.txt`.

PL: Ścieżka (path) względna, taka jak `"scores.txt"`, zaczyna się w katalogu roboczym (working directory), którym w Jupyterze jest folder notatnika; `os.getcwd()` pokazuje jego pełną ścieżkę, a `os.listdir()` pliki w nim. Otwarcie pliku (file), którego tam nie ma, zgłasza `FileNotFoundError`; tutaj w folderze jest tylko `scores.txt`.

```python raises=FileNotFoundError
with open("scores.txt", "w", encoding="utf-8") as f: f.write("72\n85\n")  #| hide
import os

print(os.listdir())
print(os.path.exists("scores.txt"))
open("score.txt", encoding="utf-8")
```
