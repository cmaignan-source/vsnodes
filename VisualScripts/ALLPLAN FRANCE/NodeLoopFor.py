""" Script for NodeLoopFor
"""
from __future__ import annotations

from typing import Any

import operator
import math

import NemAll_Python_Geometry as Geometry

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeLoopFor')


LOOP_LIST_MARKER = "__LOOP_RETURN__"

# Authorized operators

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "**": operator.pow,
    }

MATH_FUNCS = {
    "abs": math.fabs,
    "sqrt": math.sqrt,
    "pow": math.pow,

    "rad": math.radians,   # degrees -> radians
    "deg": math.degrees,   # radians -> degrees

    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,

    "log": math.log,       # log(x) = ln(x)
    "log10": math.log10,   # log base 10
    "exp": math.exp,       # e**x
    }


def create_node(init_data: NodeInitData) -> NodeLoopFor:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeLoopFor
    """

    return NodeLoopFor(init_data)


class NodeLoopFor(NodeBase):
    """ Definition of class NodeLoopFor
    """

    def _create_output(self) -> None:
        """ Loop statement
        """
        self._set_init_node_output(self.build_ele.Result)
        all_results = []

        repeat = self.build_ele.Repeat.value
        functions = self.build_ele.Function.value

        if len(functions) == 4 and functions[0] == LOOP_LIST_MARKER:
            functions = [functions]

        for idx, f in enumerate(functions):
            if f[0] != LOOP_LIST_MARKER:
                self.error = "Invalid node, please use LoopOperation."
                return
            else:
                if len(f) == 4:
                    marker, initvalue, operation, operand = f
                    result = []
                    duplicate = (
                        hasattr(initvalue, '__module__') and
                        initvalue.__module__ == "NemAll_Python_Geometry" and
                        (operand is None or operand == 0)
                        )
                    is_operand_list = isinstance(operand, (list, tuple))

                    # Check list homogeneity
                    if is_operand_list and operand:
                        types_set = set(type(item) for item in operand)
                        if len(types_set) != 1:
                            self.error = f"All operands in the list must be of the same type (found: {list(types_set)})."
                            return

                    if duplicate:
                        for i in range(repeat):
                            try:
                                geo_type = type(initvalue)
                                geo_copied = geo_type(initvalue)
                                result.append(geo_copied)
                            except Exception:
                                result.append(initvalue)
                        all_results.append(result)
                    else:
                        current_value = initvalue
                        for i in range(repeat):
                            if is_operand_list:
                                current_operand = operand[i] if i < len(operand) else operand[-1]
                            else:
                                current_operand = operand
                            new_func = [current_value, operation, current_operand]
                            if hasattr(initvalue, '__module__') and initvalue.__module__ == "NemAll_Python_Geometry":
                                current_operand = float(current_operand) if isinstance(current_operand, int) else current_operand
                                res = self.operate_geom(current_value, operation, current_operand)
                            else:
                                res = self.calculate_operation(new_func)
                            result.append(res)
                            current_value = res
                        all_results.append(result)

        if len(functions) > 1:
            self.build_ele.Result.value = all_results
        else:
            self.build_ele.Result.value = all_results[0] if all_results else []


    def calculate_operation(self,
                            function: list) -> int | float:
        """ Calculate the operation

        Args:
            list: list from LoopOperation node

        Returns:
            result of calculation
        """
        initvalue, operation, operand = function

        if operation in ["/", "%"]:
            if operand == 0:
                self.error = "Division by zero is not allowed."
                return
            res = OPS[operation](initvalue, operand)
        elif operation in OPS:
            res = OPS[operation](initvalue, operand)
        elif operation in MATH_FUNCS:
            if operand is not None:
                res = MATH_FUNCS[operation](operand)
            else:
                res = MATH_FUNCS[operation](initvalue)
        else:
            self.error = f"Unsupported operation: {operation}"
            return

        return res


    def operate_geom(self,
                    value:     Any,
                    operation: str,
                    operand:   Any) -> Any:
        """ Geometric operations when using Point3D, Vector3D or Matrix3D

        Args:
            initvalue: initial object
            operation: symbol of the operation (+, -, *, /)
            operand:   operand for the operation (list or object)

        Returns:
            result of the geometric operation
        """
        op_func = OPS.get(operation)

        if op_func is None:
            self.error = f"Operator {operation} not supported"

        match (type(value), type(operand), operation):
            # Point3D / Point3D : addition/subtraction
            case (Geometry.Point3D, Geometry.Point3D, "+" | "-"):
                return op_func(value, operand)
            # Point3D / Vector3D : translation
            case (Geometry.Point3D, Geometry.Vector3D, "+" | "-"):
                return op_func(value, operand)
            # Vector3D / Vector3D : addition/subtraction
            case (Geometry.Vector3D, Geometry.Vector3D, "+" | "-"):
                return op_func(value, operand)
            # Point3D multiplication
            case (Geometry.Point3D, float, "*"):
                return op_func(value, operand)
            # Point3D division
            case (Geometry.Point3D, float, "/"):
                return op_func(value, operand)
            # Vector3D multiplication
            case (Geometry.Vector3D, float, "*"):
                return op_func(value, operand)
            # Vector3D division
            case (Geometry.Vector3D, float, "/"):
                return op_func(value, operand)
            # Matrix transformation
            case ((Geometry.Point3D, Geometry.Vector3D), Geometry.Matrix3D, "*"):
                return op_func(value, operand)
            # Operand as list
            case (_, list, _):
                types_set = set(type(item) for item in operand)
                if len(types_set) == 1:
                    # Point3D & Vector3D list
                    if isinstance(value, Geometry.Point3D) and operand and all(isinstance(item, Geometry.Vector3D) for item in operand) and operation in ["+", "-"]:
                        return [op_func(value, item) for item in operand]
                    # Operand list same type as initvalue
                    if operand and all(type(item) == type(value) for item in operand):
                        return [op_func(value, item) for item in operand]
                    # Scalar list (scaling)
                    if operand and all(isinstance(item, (float, int)) for item in operand) and operation in ["*", "/"]:
                        return [op_func(value, item) for item in operand]
                else:
                    self.error = f"All operands in the list must be of the same type (found: {list(types_set)})."
                    return
            case _:
                self.error = f"Operand types incompatible for this operation."
