---
title: Loops
glyph: "for"
summary: "Repeating work with for, range, enumerate, zip and while."
pl:
  title: Pętle
  summary: "Pętle (loops): powtarzanie pracy z for, range, enumerate, zip i while."
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

### See also

- loops/looping-with-zip

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

## Looping with zip

PL: Pętla z zip

`for x, y in zip(xs, ys):` loops over several collections at once. `zip` pairs up their items by position, giving one tuple per position that you unpack into names.

PL: `for x, y in zip(xs, ys):` przechodzi pętlą (loop) po kilku kolekcjach naraz. `zip` łączy w pary ich elementy według pozycji i daje na każdą pozycję jedną krotkę (tuple), którą rozpakowujesz do nazw.

```python
xs = [1, 2, 3]
ys = [2.1, 3.9, 6.2]
for x, y in zip(xs, ys):
    print(x, y)

print(list(zip(xs, ys)))
```

### Pitfall

When the collections have different lengths, `zip` stops at the end of the shortest without an error, so the extra items are silently dropped. `zip(xs, ys, strict=True)` raises `ValueError` instead.

PL: Gdy kolekcje mają różne długości, `zip` kończy się wraz z najkrótszą bez żadnego błędu, więc nadmiarowe elementy po cichu znikają. `zip(xs, ys, strict=True)` zgłasza wtedy `ValueError`.

### See also

- tuples/unpacking

## while loops

PL: Pętla while

`while condition:` repeats its block as long as `condition` is `True`, checking it before each pass. Use it when you don't know in advance how many passes you need.

PL: Pętla (loop) `while condition:` powtarza swój blok, dopóki `condition` jest `True`, i sprawdza warunek przed każdym przebiegiem. Użyj jej, gdy nie wiesz z góry, ilu przebiegów potrzebujesz.

```python
error = 1.0
steps = 0
while error >= 0.01:
    error = error / 2
    steps += 1

print(steps, error)
```

### Pitfall

If the block never changes what the condition tests, for example you forget `error = error / 2`, the condition stays `True` and the loop never ends. Stop it with the stop button in Jupyter (Kernel → Interrupt Kernel), or Ctrl+C in a terminal.

PL: Jeśli blok nigdy nie zmienia tego, co sprawdza warunek, na przykład zapomnisz o `error = error / 2`, warunek pozostaje `True` i pętla nigdy się nie kończy. Zatrzymaj ją przyciskiem stop w Jupyterze (Kernel → Interrupt Kernel) albo Ctrl+C w terminalu.
