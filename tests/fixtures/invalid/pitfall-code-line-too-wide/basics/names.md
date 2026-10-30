---
title: Names
glyph: "x ="
summary: Binding names.
pl:
  title: Nazwy
  summary: Wiązanie nazw.
---

## Binding

PL: Wiązanie

`=` binds a name to a value.

PL: `=` wiąże nazwę z wartością.

```python
x = 1
print(x)
```

### Pitfall

`x == 1` compares; it does not bind.

PL: `x == 1` porównuje; nie wiąże.

```python
x = 1
print(x == 1, x == 2, x == 3, x == 4000)
print(x == 1, x == 2, x == 3, x == 40000)
```
