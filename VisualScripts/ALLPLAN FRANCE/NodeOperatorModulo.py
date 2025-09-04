""" Script for NodeOperatorModulo
"""

from __future__ import annotations

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('OperatorModulo')


def create_node(init_data: NodeInitData) -> NodeOperatorModulo:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of OperatorModulo
    """

    return NodeOperatorModulo(init_data)


class NodeOperatorModulo(NodeBase):
    """ Definition of class OperatorModulo
    """

    def _create_output(self) -> None:
        """ Calculate the modulo
        """

        x = self.build_ele.X.value
        y = self.build_ele.Y.value

        if x == []:
            self.warning = "X is empty"
            return

        if y == []:
            self.error = "Y is empty"
            return

        if y == 0:
            self.error = "Can't divide by zero"
            return

        self.build_ele.Result.value = [item % y for item in x]
