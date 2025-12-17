""" Script for NodeSortObjectsByAttribute
"""

from __future__ import annotations

import NemAll_Python_BaseElements       as BaseElements

from NodeUtil.NodeBase       import NodeBase
from NodeUtil.NodeInitData   import NodeInitData


NodeBase.trace_node_name('SortObjectsByAttribute')


def create_node(init_data: NodeInitData) -> NodeSortObjectsByAttribute:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeSortObjectsByAttribute
    """

    return NodeSortObjectsByAttribute(init_data)


class NodeSortObjectsByAttribute(NodeBase):
    """ Definition of class NodeSortObjectsByAttribute
    """

    def _create_output(self) -> None:
        """ Sort the list of objects
        """
        self._set_init_node_output(self.build_ele.ObjectsWithAttribute)
        self._set_init_node_output(self.build_ele.ObjectsWithoutAttribute)

        objects = self.build_ele.Objects.value
        attr_id = self.build_ele.AttributeID.value

        if not attr_id or (attr_name := BaseElements.AttributeService.GetAttributeName(self.document, attr_id)) == '???':
            self.error = f"Attribute ID {attr_id} does not exist in this project"
            return

        readstate = BaseElements.eAttibuteReadState.ReadAllAndComputable

        tmp_list = []

        for obj in objects:
            atts = dict(BaseElements.ElementsAttributeService.GetAttributes(obj, readstate))
            val = atts.get(attr_id, None)
            tmp_list.append((val, obj))

        # List of objects with specified attribute
        with_attr = [(val, obj) for val, obj in tmp_list if val is not None]
        with_attr_sorted = sorted(with_attr, key=lambda t: t[0])
        sorted_obj_with_attr = [obj for _, obj in with_attr_sorted]

        # List of objects without specified attribute
        obj_without_attr = [obj for val, obj in tmp_list if val is None]

        self.build_ele.ObjectsWithAttribute.value = sorted_obj_with_attr
        self.build_ele.ObjectsWithoutAttribute.value = obj_without_attr
