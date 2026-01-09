""" Script for NodeGetObjectAttribute
"""

from __future__ import annotations

import NemAll_Python_BaseElements as BaseElements

from NodeUtil.NodeBase     import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('GetObjectAttribute')


def create_node(init_data: NodeInitData) -> NodeGetObjectAttribute:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of GetObjectAttribute
    """

    return NodeGetObjectAttribute(init_data)


class NodeGetObjectAttribute(NodeBase):
    """ Definition of class GetObjectAttribute
    """

    def _create_output(self) -> None:
        """ Get an attribute
        """
        self._set_init_node_output(self.build_ele.Result)

        ele_list = self.build_ele.Objects.value
        attr_id = self.build_ele.AttributeID.value

        if not attr_id or (attr_name := BaseElements.AttributeService.GetAttributeName(self.document, attr_id)) == '???':
            self.error = f"Attribute ID {attr_id} does not exist in this project"
            return

        attr_list = []

        for ele in ele_list:
            attrs = ele.GetAttributes(BaseElements.eAttibuteReadState.ReadAllAndComputable)
            attr = next((val for id, val in attrs if id == attr_id), None)

            attr_list.append(attr)

        self.build_ele.Result.value = attr_list
