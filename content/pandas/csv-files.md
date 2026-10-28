---
title: Reading and writing CSV
glyph: ".csv"
summary: "CSV files as DataFrames: reading, semicolons and decimal commas, reading from a URL, and writing with to_csv."
pl:
  title: Odczyt i zapis CSV
  summary: "Pliki CSV jako ramki danych (DataFrames): odczyt, średniki i przecinki dziesiętne, odczyt z adresu URL oraz zapis przez to_csv."
---

## Reading a CSV file

PL: Odczyt pliku CSV

`pd.read_csv("scores.csv")` reads a CSV file into a DataFrame: the first line gives the column names, and each column gets its type from its values. Here `scores.csv` has the header `name,group,score` and three students; pandas reads files as UTF-8, so `Łucja` comes through.

PL: `pd.read_csv("scores.csv")` wczytuje plik CSV do ramki danych (DataFrame): pierwszy wiersz daje nazwy kolumn, a każda kolumna dostaje typ na podstawie swoich wartości. Tutaj `scores.csv` ma nagłówek `name,group,score` i trzech studentów; pandas czyta pliki jako UTF-8, więc `Łucja` wczytuje się poprawnie.

```python
with open("scores.csv", "w", encoding="utf-8") as f: f.write("name,group,score\nAla,A,72\nJan,B,85\nŁucja,A,90\n")  #| hide
import pandas as pd

df = pd.read_csv("scores.csv")
print(df)
print(df.dtypes)
```

### See also

- files/csv-files-with-the-csv-module
- array-files/csv-files
- dates/dates-from-a-csv-file

## Semicolons and decimal commas

PL: Średniki i przecinki dziesiętne

A CSV file saved by a Polish Excel separates the values with `;` and writes `165,5` for 165.5, so pass `sep=";"` and `decimal=","`. Here `heights.csv` has the header `name;height;score` and three rows like `Ala;165,5;72`.

PL: Plik CSV zapisany przez polskiego Excela rozdziela wartości znakiem `;` i zapisuje 165.5 jako `165,5`, więc podaj separator (delimiter) `sep=";"` i `decimal=","`. Tutaj `heights.csv` ma nagłówek `name;height;score` i trzy wiersze w rodzaju `Ala;165,5;72`.

```python
with open("heights.csv", "w", encoding="utf-8") as f: f.write("name;height;score\nAla;165,5;72\nJan;180,0;85\nEwa;172,5;90\n")  #| hide
import pandas as pd

df = pd.read_csv(
    "heights.csv", sep=";", decimal=",")
print(df)
print(df.dtypes)
```

### Pitfall

Without `sep=";"` pandas looks for commas, so each line lands in one column, named after the whole header, and `df.shape` shows a single column. Without `decimal=","` the heights stay text.

PL: Bez `sep=";"` pandas szuka przecinków, więc każdy wiersz trafia do jednej kolumny, nazwanej całym nagłówkiem, a `df.shape` pokazuje tylko jedną kolumnę. Bez `decimal=","` wzrosty zostają tekstem.

```python
with open("heights.csv", "w", encoding="utf-8") as f: f.write("name;height;score\nAla;165,5;72\nJan;180,0;85\nEwa;172,5;90\n")  #| hide
import pandas as pd

df = pd.read_csv("heights.csv")
print(df.shape)
print(df.columns)
```

### See also

- dates/text-to-dates

## Reading from a URL

PL: Odczyt z adresu URL

`pd.read_csv(url)` downloads a CSV file from the web and reads it as it would a local file, with no separate download step. Give it the address of the file itself, not of a web page that shows the file.

PL: `pd.read_csv(url)` pobiera plik CSV z sieci i czyta go tak jak plik lokalny, bez osobnego pobierania. Podaj adres (URL) samego pliku, a nie strony internetowej, która go wyświetla.

```python
with open("scores.csv", "w", encoding="utf-8") as f: f.write("name,group,score\nAla,A,72\nJan,B,85\nEwa,A,90\n")  #| hide
import pandas as pd

url = "https://example.org/scores.csv"
df = pd.read_csv("scores.csv")  #| show: df = pd.read_csv(url)
print(df)
```

## Writing with to_csv

PL: Zapis przez to_csv

`df.to_csv("out.csv", index=False)` writes the table to a CSV file with a header line, and `pd.read_csv` reads it back. `index=False` leaves out the row numbers, which you rarely want in the file.

PL: `df.to_csv("out.csv", index=False)` zapisuje tabelę do pliku CSV z wierszem nagłówka, a `pd.read_csv` odczytuje ją z powrotem. `index=False` pomija numery wierszy, czyli indeks (index), który rzadko jest potrzebny w pliku.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [72, 85, 90],
})
df.to_csv("out.csv", index=False)
print(pd.read_csv("out.csv"))
```

### Pitfall

Without `index=False` the row numbers are written as an unnamed first column, so reading the file back gives an extra `Unnamed: 0` column.

PL: Bez `index=False` numery wierszy zapisują się jako pierwsza kolumna bez nazwy, więc po ponownym odczycie pliku pojawia się dodatkowa kolumna `Unnamed: 0`.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ala", "Jan", "Ewa"],
    "score": [72, 85, 90],
})
df.to_csv("out.csv")
print(pd.read_csv("out.csv"))
```

### See also

- files/writing-a-text-file
- array-files/text-files-with-savetxt-and-loadtxt
