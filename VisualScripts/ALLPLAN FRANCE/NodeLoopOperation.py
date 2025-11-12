""" Script for NodeLoopOperation
"""
from __future__ import annotations

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeLoopOperation')


LOOP_LIST_MARKER = "__LOOP_RETURN__"


def create_node(init_data: NodeInitData) -> NodeLoopOperation:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeLoopOperation
    """

    return NodeLoopOperation(init_data)


class NodeLoopOperation(NodeBase):
    """ Definition of class NodeLoopOperation
    """

    def _create_output(self) -> None:
        """ Match/Case statement
        """
        self._set_init_node_output(self.build_ele.Result)

        init_value = self.build_ele.InitValue.value
        operation = self.build_ele.Operation.value
        operand = self.build_ele.Operand.value

        result = []
        result.append(LOOP_LIST_MARKER)
        result.append(init_value)
        result.append(operation)
        result.append(operand)

        self.build_ele.Result.value = result
