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

`interact_manual` adds a button that the site can't draw.

PL: `interact_manual` dodaje przycisk, którego strona nie umie narysować.

```python
from ipywidgets import interact_manual

def show(x=5):
    print(x)


interact_manual(show, x=(0, 10))
```
