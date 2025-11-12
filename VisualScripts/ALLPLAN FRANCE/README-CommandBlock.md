# COMMANDBLOCK - VS NODE FOR ALLPLAN

## Overview
This node for Allplan VisualScripting processes **one-line string instructions** and produces **four outputs**:

- **AsInteger** → Integer value (if applicable)
- **AsDouble** → Floating–point value (if applicable)
- **AsString** → Text value (if applicable)
- **AsList** → List representation of the result (consistent with the other output)

It acts as a **multi-purpose interpreter** that can:
- Parse and store single values (numbers or strings)
- Perform basic and trigonometric calculations
- Parse and generate ordered sequences
- Generate lists from manual input or random values

---

## 1. Input / Outputs

**Input:**
A single–line string containing an instruction.

**Outputs:**
- `AsInteger`
- `AsDouble`
- `AsString`
- `AsList`

The script detects the type of result and fills the relevant outputs accordingly, leaving the others `None`.

---

## 2. Single Value Handling

If the input is a **single value** without special syntax:

- **Integer**
  - `AsInteger` = integer value
  - `AsDouble` = same value as float
  - `AsList` = list with a single integer
- **Decimal**
  - `AsDouble` = float value
  - `AsList` = list with a single float
- **Text**
  - `AsString` = string value
  - `AsList` = list with a single string

**Examples:**
- "42" → AsInteger=42, AsDouble=42.0, AsList=[42]
- "3.14" → AsDouble=3.14, AsList=[3.14]
- "hello" → AsString="hello", AsList=["hello"]

---

## 3. Mathematical Operations

Supports **basic arithmetic**, **trigonometric functions**, and **mathematical constants**.

- **Operators**: `+  -  *  /  %  **  ( )`
- **Math constants**: `pi`
- **Math functions**:
  - `abs(x)` — absolute value (float)
  - `sqrt(x)` — square root
  - `pow(x, y)` — power
  - `rad(deg)` — convert degrees to radians
  - `deg(rad)` — convert radians to degrees
  - `sin(x)`, `cos(x)`, `tan(x)` — trigonometry (in radians)
  - `asin(x)`, `acos(x)`, `atan(x)` — inverse trig (returns radians)
  - `log(x)`, `log10(x)`, `exp(x)`

**Examples:**
- "5+5" → AsInteger=10, AsDouble=10.0, AsList=[10]
- "sqrt(9)" → AsInteger=3, AsDouble=3.0, AsList=[3]
- "cos(pi)" → AsInteger=-1, AsDouble=-1.0, AsList=[-1]
- "cos(rad(60))" → AsDouble=0.5, AsList=[0.5]
- "deg(acos(0.5))" → AsDouble=60.0, AsList=[60.0]

---

## 4. Manual List Creation

Using the **`|`** separator, you can manually create a list with detection of element types:
- All integers → list of `int`
- All floats   → list of `float`
- Mixed / text → list of `str`

**Examples:**
- "toto|tata|titi" → AsList=["toto", "tata", "titi"]

---

## 5. Complex Sequence Generation

Using `..` notation, the script supports several formats:

- `start..end` — step=1 implicit
- `start..end..step`
- `start..end..@count`
- `start..@count..end`

**Features:**
- Works with **numbers** and **letters**
- Supports ascending and descending sequences

**Examples:**
- "1..5" → AsList=[1,2,3,4,5]
- "10..0..2" → AsList=[10,8,6,4,2,0]
- "A..E" → AsList=["A", "B", "C", "D", "E"]
- "A..Z..@6" → AsList=["A", "F", "K", "P", "U", "Z"]

---

## 6. Random Value Generation

Two syntaxes are supported:

- **Unique random integers**:
rand(min, max, count[, 'raw'])

Generates `count` unique integers in `[min, max]` inclusive, sorted ascending.

- **Unique random floats**:
randf(min, max, count[, precision, 'raw'])

Generates `count` unique floats in `[min, max]` inclusive, sorted ascending.
Precision defaults to **3 decimals** if not specified.
With `raw` as last argument, the list will **not** be sorted.

**Examples:**
- "rand(1,10,5)" → AsList=[1,2,3,7,10]
- "rand(1,10,3,raw)" → AsList=[8,3,4]
- "randf(0,1,5,2)" → AsList=[0.53,0.70,0.75,0.79,0.84]
