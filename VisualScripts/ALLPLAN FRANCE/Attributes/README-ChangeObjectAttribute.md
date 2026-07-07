# CHANGEOBJECTATTRIBUTE - VS NODE FOR ALLPLAN

## Overview
This node enables you to **set** or **add** an attribute on a existing object in your ALLPLAN project.

---

## 1. Inputs / Outputs

**Inputs:**
- `Objects` → list of the objects to be modify (BaseElementAdapter or BaseElementAdapterList)
- `AttributeID` → ID of the attribute (as an integer)
- `NewValue` → new value for the attribute (single string or list of strings)

**Outputs:**
- `ModifiedObjects` → modified objects as a BaseElementAdapterList

---

## 2. How it works
- The node checks if the attribute already exists on the ALLPLAN elements.
- If it does, the attribute value is updated.
- If not: adds the attribute with the specified value.
- If `NewValue` is a list, each element receives a value according to the order of the list; if there are more objects than values, the last value is reused for the remaining objects.

---

## 3. Example

- `Objects`=BaseElementAdapterList(...)
- `AttributeID`=507
- `NewValue`='Hello'
- `Result`:
  - Sets the attribute **Name** to 'Hello'
