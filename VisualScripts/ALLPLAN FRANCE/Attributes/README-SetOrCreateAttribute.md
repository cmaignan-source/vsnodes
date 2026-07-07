# SETORCREATEATTRIBUTE - VS NODE FOR ALLPLAN

## Overview
This node enables you to **set** or **create** an attribute on a new PythonPart object in your ALLPLAN project.
It supports all main ALLPLAN attribute types: `string`, `integer`, `double`, `date` and `enum`.

---

## 1. Inputs / Outputs

**Inputs:**
- `AttributeName` → name of the attribute to set or create
- `AttributeValue` → value to assign

**Outputs:**
- `AttributeID` → ID of the attribute (as an integer)

---

## 2. How it works
- The node checks if the attribute already exists on the current ALLPLAN project.
- If so: updates the attribute value.
- If not: creates the attribute with the specified value.

---

## 3. Examples

- `AttributeName`='TEST_STRING' (not exists)
- `AttributeValue`='TEST_VALUE'
- `Result`:
  - Create a new attribute 'TEST_STRING' as **Text** (type of the value)
  - Set this new attribute to the PythonPart object with 'TEST_VALUE' as value

- `AttributeName`='TEST_LIST' (existing **ListBox** as `VALUE_0|VALUE_1|VALUE_2`)
- `AttributeValue`=1
- `Result`:
  - Set this attribute to the PythonPart object with 'VALUE_1' as value
