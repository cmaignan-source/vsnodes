""" Script for NodeChangeObjectAttribute
"""

from __future__ import annotations

import NemAll_Python_BaseElements       as BaseElements
import NemAll_Python_IFW_ElementAdapter as ElementAdapter

from NodeUtil.NodeBase       import NodeBase
from NodeUtil.NodeInitData   import NodeInitData
from NodeUtil.NodeObjectUtil import  NodeObjectUtil


NodeBase.trace_node_name('ChangeObjectAttribute')


def create_node(init_data: NodeInitData) -> NodeChangeObjectAttribute:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of ChangeObjectAttribute
    """

    return NodeChangeObjectAttribute(init_data)


class NodeChangeObjectAttribute(NodeBase):
    """ Definition of class ChangeObjectAttribute
    """

    def _create_output(self) -> None:
        """ Change or add an attribute
        """
        self._set_init_node_output(self.build_ele.ModifiedObjects)

        objects = self.build_ele.Objects.value
        attr_id = self.build_ele.AttributeID.value
        values = self.build_ele.NewValue.value

        if not attr_id or (attr_name := BaseElements.AttributeService.GetAttributeName(self.document, attr_id)) == '???':
            self.error = f"Attribute ID {attr_id} does not exist in this project"
            return

        if not values:
            self.build_ele.ModifiedObjects.value = self.build_ele.Objects.value
            return

        if isinstance(values, str):
            values = [values]

        modified_objects = []

        for idx, obj in enumerate(objects):
            if not isinstance(obj, ElementAdapter.BaseElementAdapter):
                self.error = f"Each object must be a BaseElementAdapter, found {type(obj).__name__}"
                continue
            element_adapters = ElementAdapter.BaseElementAdapterList()
            element_adapters.append(obj)
            new_value = values[idx] if idx < len(values) else values[-1]
            BaseElements.ElementsAttributeService.ChangeAttribute(attr_id, new_value, element_adapters)
            modified_objects.append(obj)

        self.build_ele.ModifiedObjects.value = NodeObjectUtil.create_base_element_adpter_list(modified_objects)
