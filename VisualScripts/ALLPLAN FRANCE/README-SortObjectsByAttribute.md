# SORTOBJECTSBYATTRIBUTE - VS NODE FOR ALLPLAN

## Overview
This node for Allplan VisualScripting sorts a list of model objects based on the value of a given Allplan **attribute**.

---

## Inputs / Output

**Inputs:**
- `Objects` → list of Allplan model objects to sort
- `AttributeID` → ID of the attribute used for sorting (for example `507` for `Name`)

**Outputs:**
- `ObjectsWithAttribute` → list of objects that have the specified attribute, sorted by the attribute value
- `ObjectsWithoutAttribute` → list of objects that do not have the specified attribute

**Example:**
- `Objects`= list of columns
- `AttributeID` = 507
- `ObjectsWithAttribute` = columns sorted by their name
- `ObjectsWithoutAttribute` = columns without a value for their name
