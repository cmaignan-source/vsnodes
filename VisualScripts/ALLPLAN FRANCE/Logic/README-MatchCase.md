# MATCHCASE & CASE - VS NODES FOR ALLPLAN

## Overview
These nodes provide flexible multi-condition selection ("switch" or "pattern matching") for ALLPLAN VisualScripting.
The **MatchCase** node compares an input value against one or multiple conditions, each defined by its own **Case** node.

Results or actions can be associated with single values, lists of values, and a default option when no match occurs.

---

## 1. Inputs / Outputs

**MatchCase Inputs:**
- `Value` → the value to be tested
- `Cases` → list of **Case** node outputs, each representing a condition and its associated result
- `Default` → result or action used if no `Cases` are matched

**MatchCase Outputs:**
- `Result` → the matched result or the `Default` if no match

**Case Inputs:**
- `MatchValue` → single value or list of values to match
- `Function` → result or action to return if this `Case` matches

**Case Outputs:**
- `Result` → case structure for use in the `Cases` list

---

## 2. How it works
- Each **Case** node defines a possible condition (single value or list) and the action/result if matched.
- The **MatchCase** node compares the input value in order against each **Case**. As soon as a match is found, the associated result is returned and no further cases are checked.
- If a **Case’s** MatchValue is a list (e.g., [0,5,7]), the input value is checked for membership in that list.
- If no **Case** matches, the `Default` value or action is returned.

---

## 3. Example
Color update from a **Box** dimensions

- `Value`=Length
- `Cases`:
  - **Case**(`MatchValue`=500, `Function`=**ColorInput 4**)
  - **Case**(`MatchValue`=1000, `Function`=**ColorInput 5**)
  - **Case**(`MatchValue`=[750, ..., 800], `Function`=**ColorInput 7**)
- `Default`=**ColorInput 8**

-  `Result`:
  - If the Length is set to 500, the cube will be in green.
  - If it's 1000, the cube will be in pink.
  - In any value between 750 and 800 (inclusive) it will be blue.
  - For all the others cases, the cube will be orange.
