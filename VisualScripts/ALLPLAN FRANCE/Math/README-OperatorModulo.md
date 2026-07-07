# OPERATORMODULO - VS NODE FOR ALLPLAN

## Overview
This node for Allplan VisualScripting performs the **modulo operation** between two numeric inputs.

---

## Inputs / Output

**Inputs:**
- `X` → dividend (list of numeric values)
- `Y` → divisor (single value)

Please note that **Y** can not be zero.

**Output:**
- `Result` → result of the modulo operation in a list

**Example:**
- Test if a number is even or odd :
`[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] % 2 → [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]`
