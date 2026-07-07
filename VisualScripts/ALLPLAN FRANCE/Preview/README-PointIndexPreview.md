# POINT INDEX PREVIEW - VS NODE FOR ALLPLAN

## Overview
This node allows you to preview the index of the points of supported 3D geometry objects directly in Allplan. It is useful for inspecting vertex order and debugging geometry used in Visual Scripting or PythonPart workflows.

---

## 1. Inputs / Output

**Inputs:**
- `TextHeight` → height of the displayed point indices, as a `Double`; optional, default value: `50`
- `Objects` → list of supported 3D geometry objects: `Line3D`, `Polyline3D`, `Polygon3D`, `Spline3D`, `BSpline3D`, `Polyhedron3D`, `BRep3D`

**Output:**
- No explicit data output

---

## 2. How it works
- The node converts the input into a geometry object list.
- For each object, it extracts the vertices according to its geometry type: line endpoints, `.Points` collections, `Polyhedron3D` vertices, or `BRep3D` vertices via `GetVertex(i)`.
- The indices are displayed in ALLPLAN, centered on each point, starting at `0`.

---

## 3. Typical use cases
- Check the order of points before using the geometry in another node or PythonPart script.
- Verify the vertex sequence of a `Polygon3D`, `Polyline3D`, `Polyhedron3D` or `BRep3D`.
- Debug generated geometry when the resulting shape does not match the expected point order.

---

## 4. Example

- `Objects` = `Polyline3D` with 4 points
- `TextHeight` = `50`
- `Result`:
  - The numbers **0, 1, 2, 3** are displayed at each vertex position in preview mode, centered on the point.

---

## 5. Notes
- This node is preview-only and does not create permanent geometry in the drawing.
- Indices always start at `0`.
- The preview reference position is `CENTER_CENTER`.
