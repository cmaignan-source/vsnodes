""" Script for NodeMatchCase
"""
from __future__ import annotations

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeMatchCase')


CASE_LIST_MARKER = "__MATCH_CASE_CASELIST__"


def create_node(init_data: NodeInitData) -> NodeMatchCase:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeMatchCase
    """

    return NodeMatchCase(init_data)


class NodeMatchCase(NodeBase):
    """ Definition of class NodeMatchCase
    """

    def _create_output(self) -> None:
        """ Match/Case statement
        """
        self._set_init_node_output(self.build_ele.Result)

        value = self.build_ele.Value.value
        cases = self.build_ele.Cases.value
        default = self.build_ele.Default.value

        cases = cases if isinstance(cases, list) else []

        result = None

        if len(cases) == 3 and cases[0] == CASE_LIST_MARKER:
            cases = [cases]

        # Check if only one type of operations
        types_set = set(type(case[2]) for case in cases if len(case) == 3 and case[0] == CASE_LIST_MARKER)
        if len(types_set) > 1:
            for typ in types_set:
                if typ.__module__ != "NemAll_Python_Geometry":
                    self.error = "All operations/functions in cases must be of the same type."
                    return

        for case in cases:
            if len(case) == 3 and case[0] == CASE_LIST_MARKER:
                match_value = case[1]
                operation = case[2]

                if isinstance(match_value, list):
                    if value in match_value:
                        result = operation
                        break
                else:
                    if value == match_value:
                        result = operation
                        break

        if result is None and default is not None:
            result = default

        self.build_ele.Result.value = result
