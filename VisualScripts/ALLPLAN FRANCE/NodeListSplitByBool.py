""" Script for NodeListSplitByBool
"""

from __future__ import annotations

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeListSplitByBool')


def create_node(init_data: NodeInitData)  -> NodeListSplitByBool:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of ListSplitByBool
    """

    return NodeListSplitByBool(init_data)


class NodeListSplitByBool(NodeBase):
    """ Definition of class NodeListSplitByBool
    """

    def _create_output(self) -> None:
        """ Split list by bool mask
        """
        self._set_init_node_output(self.build_ele.ListIfTrue)
        self._set_init_node_output(self.build_ele.ListIfFalse)

        list_to_split = self.build_ele.ListToSplit.value
        boolmask = self.build_ele.BoolMask.value

        if list_to_split == []:
            self.warning = "List is empty"
            return

        if boolmask:
            boolmask = self.normalize_boolmask(boolmask)
            if len(boolmask) < len(list_to_split):
                boolmask += [False] * (len(list_to_split) - len(boolmask))
            self.build_ele.ListIfTrue.value = [item for idx, item in enumerate(list_to_split) if boolmask[idx]]
            self.build_ele.ListIfFalse.value = [item for idx, item in enumerate(list_to_split) if not boolmask[idx]]
        else:
            self.build_ele.ListIfTrue.value = []
            self.build_ele.ListIfFalse.value = list_to_split


    def normalize_boolmask(self, boolmask: list) -> list:
        """ Ensures all entries are bool (True/False)
        Args:
            boolmask: list to be validate

        Returns:
            list with correct values
        """
        normalized = []
        for val in boolmask:
            if isinstance(val, bool):
                normalized.append(val)
            elif val == 1:
                normalized.append(True)
            elif val == 0:
                normalized.append(False)
            else:
                raise ValueError(f"Invalid mask value: {val}. Only bool, 0, 1 allowed.")

        return normalized
