# GETOBJECTATTRIBUTE - VS NODE FOR ALLPLAN

## Overview
This node enables you to **get** the value of a specific attribute for one or more objects in your ALLPLAN project.

---

## 1. Inputs / Outputs

**Inputs:**
- `Objects` → list of objects to read (BaseElementAdapter or BaseElementAdapterList)
- `AttributeID` → ID of the attribute (as an integer)

**Outputs:**
- `Result` → list of values of the specified attribute

---

## 2. Example

- `Objects`=BaseElementAdapterList(...)
- `AttributeID`=507
- `Result`:
  - List of values of the attribute **Name**
