# LISTSPLIBYBOOL - VS NODE FOR ALLPLAN

## Overview
This node for Allplan VisualScripting splits a source list into two sublists, based on a matching boolmask.

---

## Inputs / Outputs

**Inputs:**
- `ListToSplit` → list of elements to split
- `BooleanMask` → boolean mask list

Please note:
- if `BooleanMask` is not set, all values will be treated as **False**
- if the mask is shorter than the main list, extra items will be assigned **False**

**Outputs:**
- `ListIfTrue` → items where corresponding boolean is **True**
- `ListIfFalse` → items where corresponding boolean is **False**
