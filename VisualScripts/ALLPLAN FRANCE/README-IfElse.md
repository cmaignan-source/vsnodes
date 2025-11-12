# IFELSE - VS NODE FOR ALLPLAN

## Overview
This node for Allplan VisualScripting allows you to select between two values or objects depending on a condition.

---

## 1. Inputs / Outputs

**Inputs:**
- `Condition` → the condition to test (boolean, integer 0|1, or a list of conditions)
- `OnTrue` → result if condition is **True**
- `OnFalse` → result if condition is **False**

**Outputs:**
- `Result`

---

## 2. Condition as Single Value

If the input is a **single value** (boolean or integer 0|1), the result will be exactly the provided **OnTrue** or **OnFalse** input.

**Example:**
Selection between a cube or cylinder according to the condition’s value.

---

## 3. Condition as List

If the input is a **list**, the result is a list where each entry is either the corresponding **OnTrue** or **OnFalse** value.
If the lists are not the same length, the shorter lists are automatically extended by repeating their last element until they match the largest size.

**Example:**
- `Condition` → [False, False, False, False, True, False, ...]
- `OnTrue` → ['A', 'B', ... 'Z']
- `OnFalse` → [0, 1, 2, 3, 4, ..., 10]

-  `Result` → [0, 1, 2, 3, 4, 'F', 6, 7, 8, 9, 10, 10, 10, 10, ...]
