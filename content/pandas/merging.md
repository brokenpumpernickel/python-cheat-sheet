---
title: Joining tables
glyph: "merge"
summary: "Two tables into one: merge on a shared column or on columns with different names, keeping unmatched rows, and stacking rows with concat."
pl:
  title: Łączenie tabel
  summary: "Dwie tabele w jedną: złączenie (join) przez merge po wspólnej kolumnie lub po kolumnach o różnych nazwach, zachowanie wierszy bez dopasowania i sklejanie wierszy przez concat."
---

## merge on a shared column

PL: merge po wspólnej kolumnie

`pd.merge(a, b, on="state")`, or `a.merge(b, on="state")`, joins two tables: each row of `a` gets the columns of the row of `b` with the same `state`. The order of the rows in `b` doesn't matter.

PL: `pd.merge(a, b, on="state")` albo `a.merge(b, on="state")` łączy dwie tabele, czyli robi złączenie (join): każdy wiersz `a` dostaje kolumny tego wiersza `b`, który ma ten sam `state`. Kolejność wierszy w `b` nie ma znaczenia.

```python
import pandas as pd

a = pd.DataFrame({
    "state": ["CA", "TX", "NY"],
    "sightings": [120, 85, 60],
})
b = pd.DataFrame({
    "state": ["NY", "CA", "TX"],
    "population": [20.2, 39.5, 29.1],
})
joined = pd.merge(a, b, on="state")
print(joined)
print(a.merge(b, on="state").equals(joined))
```

### See also

- grouping/the-group-as-an-index-or-as-a-column

## Different column names

PL: Różne nazwy kolumn

When the shared column has a different name in each table, `left_on="location_state", right_on="State"` names it in `a` and in `b`. Both columns stay in the result, so `.drop(columns="State")` removes the copy.

PL: Gdy wspólna kolumna ma w każdej tabeli inną nazwę, `left_on="location_state", right_on="State"` podaje ją w `a` i w `b`, po których robisz złączenie (join). W wyniku zostają obie kolumny, więc `.drop(columns="State")` usuwa kopię.

```python
import pandas as pd

a = pd.DataFrame({
    "location_state": ["CA", "TX", "NY"],
    "sightings": [120, 85, 60],
})
b = pd.DataFrame({
    "State": ["NY", "CA", "TX"],
    "population": [20.2, 39.5, 29.1],
})
joined = a.merge(b,
                 left_on="location_state",
                 right_on="State")
print(joined)
print(joined.drop(columns="State"))
```

## Keeping unmatched rows

PL: Zachowanie wierszy bez dopasowania

`a.merge(b, on="state", how="left")` keeps every row of `a`; where `b` has no matching row, its columns get `NaN`. Here the population table has no row for `AK`.

PL: `a.merge(b, on="state", how="left")` to złączenie lewostronne (left join): zachowuje każdy wiersz `a`, a tam, gdzie `b` nie ma pasującego wiersza, jego kolumny dostają `NaN`. Tutaj tabela z populacją nie ma wiersza dla `AK`.

```python
import pandas as pd

a = pd.DataFrame({
    "state": ["CA", "TX", "NY", "AK"],
    "sightings": [120, 85, 60, 15],
})
b = pd.DataFrame({
    "state": ["NY", "CA", "TX"],
    "population": [20.2, 39.5, 29.1],
})
print(a.merge(b, on="state", how="left"))
```

### Pitfall

Without `how`, `merge` makes an inner join, which quietly drops the rows that have no match in the other table. Compare `len` before and after the join.

PL: Bez `how` funkcja `merge` robi złączenie wewnętrzne (inner join), które po cichu usuwa wiersze bez dopasowania w drugiej tabeli. Porównaj `len` przed złączeniem i po nim.

```python
import pandas as pd

a = pd.DataFrame({
    "state": ["CA", "TX", "NY", "AK"],
    "sightings": [120, 85, 60, 15],
})
b = pd.DataFrame({
    "state": ["NY", "CA", "TX"],
    "population": [20.2, 39.5, 29.1],
})
joined = a.merge(b, on="state")
print(len(a), len(joined))
print(joined)
```

## Stacking rows with concat

PL: Sklejanie wierszy przez concat

`pd.concat([a, b])` puts the rows of `b` under the rows of `a`, matching the columns by name. The rows keep their old index, so labels repeat; `ignore_index=True` numbers them from 0 again.

PL: `pd.concat([a, b])` dokleja wiersze `b` pod wierszami `a`, dopasowując kolumny po nazwie; to sklejanie (concatenation) tabel. Wiersze zachowują swój dawny indeks (index), więc etykiety się powtarzają; `ignore_index=True` numeruje je znowu od 0.

```python
import pandas as pd

a = pd.DataFrame({"state": ["CA", "TX"],
                  "sightings": [120, 85]})
b = pd.DataFrame({"state": ["NY", "AK"],
                  "sightings": [60, 15]})
print(pd.concat([a, b]))
print(pd.concat([a, b], ignore_index=True))
```
