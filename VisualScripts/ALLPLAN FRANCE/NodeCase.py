""" Script for NodeCase
"""
from __future__ import annotations

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeCase')


CASE_LIST_MARKER = "__MATCH_CASE_CASELIST__"


def create_node(init_data: NodeInitData) -> NodeCase:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeCase
    """

    return NodeCase(init_data)


class NodeCase(NodeBase):
    """ Definition of class NodeCase
    """

    def _create_output(self) -> None:
        """ Case definition
        """
        self._set_init_node_output(self.build_ele.Result)

        match_value = self.build_ele.MatchValue.value
        operation = self.build_ele.Function.value

        if match_value is None or match_value == '':
            self.error = "MatchValue can not be empty"
            return

        result = []
        result.append(CASE_LIST_MARKER)
        result.append(match_value)
        result.append(operation)

        self.build_ele.Result.value = result
