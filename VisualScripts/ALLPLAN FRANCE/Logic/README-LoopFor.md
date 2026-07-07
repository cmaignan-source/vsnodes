# LOOPFOR & LOOPOPERATION - VS NODES FOR ALLPLAN

## Overview
These nodes provide iterative and mathematical operations for parameterized scripting in ALLPLAN VisualScripting.
The **LoopFor** node runs a for-loop over a specified range. One or several **LoopOperation** subnodes can be attached inside the loop to perform mathematical or object-based procedures on each iteration.

Results or actions can be associated with single values, lists of values, and a default option when no match occurs.

---

## 1. Inputs / Outputs

**LoopFor Inputs:**
- `Repeat` → defines the number of loop iterations (range)
- `Function` → takes one or more **LoopOperation** node outputs

**LoopFor Outputs:**
- `Result`
  - if one operation is connected, returns a single list of results
  - if multiple operations are connected, returns a list of lists — one for each connected operation (you can use the standard **ListItem** node to access specific result lists)

**LoopOperation Inputs:**
- `InitValue` → initial value or object for the operation
- `Operand` → numeric value used in the operation (ignored if `InitValue` is an geometrical object)
- `Operation` → mathematical operator (+, -, *, /) (ignored if `InitValue` is an geometrical object)

**LoopOperation Outputs:**
- `Result` → result of the mathematical expression for each iteration or the duplicated object if no operand is set

---

## 2. Mathematical Operations

Supports **basic arithmetic** and **trigonometric functions**.

- **Operators**: `+  -  *  /  %  **`
- **Math functions**:
  - `abs(x)` — absolute value (float)
  - `sqrt(x)` — square root
  - `pow(x, y)` — power
  - `rad(deg)` — convert degrees to radians
  - `deg(rad)` — convert radians to degrees
  - `sin(x)`, `cos(x)`, `tan(x)` — trigonometry (in radians)
  - `asin(x)`, `acos(x)`, `atan(x)` — inverse trig (returns radians)
  - `log(x)`, `log10(x)`, `exp(x)`

Please note that for instantaneous mathematical functions (e.g., `sqrt`, `sin`, `log`), the `Operand`, **not** the `InitValue`.
The result will be identical in each iteration.

---

## 3. Examples

Numeric loop: Arithmetic progression

- `Repeat`=10
- `Function`:
  - **LoopOperation** ➔ `InitValue`=0, `Operand`=1, `Operation`='+'
- `Result`:
  - ➔ `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`


Numeric loop: Multiplication by π

- `Repeat`=3
- `Function`:
  - **LoopOperation** → `InitValue`=1, `Operand`='pi', `Operation`='*'
- `Result`:
  - ➔ `[3.14159, 9.86960, 31.00628]`


Multiple functions loop (parallel operations)

- `Repeat`=3
`Function`:
  - **LoopOperation** ➔ `InitValue`=0, `Operand`=1, `Operation`='+'
  - **LoopOperation** ➔ `InitValue`=2, `Operand`=2, `Operation`='*'
- `Result`:
- ➔ `[[1, 2, 3], [4, 8, 16]]`


Geometry duplication

- `Repeat`=5
- `Function`:
  - **LoopOperation** ➔ `InitValue`=**Box**, `Operand`=0.0, `Operation`=''
- `Result`:
  - ➔ `[Polyhedron3D, Polyhedron3D, Polyhedron3D, Polyhedron3D, Polyhedron3D]`


Geometry loop: Point3D + Vector3D

- `Repeat`=3
- `Function`:
  - **LoopOperation** ➔ `InitValue`=Geometry.Point3D(1, 2, 3), `Operand`=Geometry.Vector3D(10, 20, 30), `Operation`='+'
- `Result`:
  - ➔ `[Point3D(11, 22, 33), Point3D(21, 42, 63), Point3D(31, 62, 93)]`


Geometry loop: Point3D * Scalar

- `Repeat`=3
- `Function`:
  - **LoopOperation** ➔ `InitValue` = Geometry.Point3D(2, 3, 4), `Operand`=2, `Operation`='*'
- `Result`:
  - ➔ `[Point3D(4, 6, 8), Point3D(8, 12, 16), Point3D(16, 24, 32)]`
