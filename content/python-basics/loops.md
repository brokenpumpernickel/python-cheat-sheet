---
title: Loops
glyph: "for"
summary: "Repeating work with for, range and enumerate."
pl:
  title: Pętle
  summary: "Pętle (loops): powtarzanie pracy z for, range i enumerate."
---

## for over a collection

PL: for po kolekcji

`for item in collection:` runs its block once for each item of a list, string or other collection, with `item` set to that item.

PL: Pętla (loop) `for item in collection:` wykonuje swój blok raz dla każdego elementu listy, napisu lub innej kolekcji (collection), a `item` jest wtedy tym elementem.

```python
scores = [72, 85, 90]
for s in scores:
    print(s - 70)
```

## range

PL: range

`range(stop)` counts from 0 up to, but not including, `stop`. `range(start, stop, step)` also sets where to start and how far to step.

PL: `range(stop)` liczy od 0 do `stop`, ale bez niego. `range(start, stop, step)` ustala też, od czego zacząć i o ile przeskakiwać.

```python
for i in range(3):
    print(i)

print(list(range(2, 11, 4)))
```

### Pitfall

`range(1, 10)` gives 1 to 9, because it stops *before* `stop`. For 1 to 10, write `range(1, 11)`.

PL: `range(1, 10)` daje liczby od 1 do 9, bo kończy się *przed* `stop`. Dla liczb od 1 do 10 napisz `range(1, 11)`.

## enumerate

PL: enumerate

`enumerate(data)` gives each item together with its position, counting from 0, so you don't need a separate counter.

PL: `enumerate(data)` daje każdy element razem z jego pozycją, licząc od 0, więc nie potrzebujesz osobnego licznika w pętli (loop).

```python
scores = [72, 85, 90]
for i, s in enumerate(scores):
    print(i, s)
```

### See also

- tuples/unpacking
