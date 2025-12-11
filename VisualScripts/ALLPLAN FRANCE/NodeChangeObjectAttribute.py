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

    def normalize_to_adapter_list(self,
                                  objects: ElementAdapter.BaseElementAdapterList | ElementAdapter.BaseElementAdapter | list
                                  )-> ElementAdapter.BaseElementAdapterList:
        """ Will always return BaseElementAdapterList from:
        - BaseElementAdapterList
        - single BaseElementAdapter
        - list/tuple of BaseElementAdapter

        Returns:
            objects as BaseElementAdapterList
        """
        if isinstance(objects, ElementAdapter.BaseElementAdapterList):
            return objects

        if isinstance(objects, ElementAdapter.BaseElementAdapter):
            adapter_list = ElementAdapter.BaseElementAdapterList()
            adapter_list.append(objects)
            return adapter_list

        if isinstance(objects, (list, tuple)):
            if not objects:
                self.error = "The list of objects cannot be empty."

            if not all(isinstance(obj, ElementAdapter.BaseElementAdapter) for obj in objects):
                self.error = "All items in the objects list must be BaseElementAdapter instances."

            return ElementAdapter.BaseElementAdapterList(objects)

        # Unsupported type
        self.error = f"Unsupported type for objects: {type(objects).__name__}."


    def _create_output(self) -> None:
        """ Change or add an attribute
        """
        self._set_init_node_output(self.build_ele.ModifiedObjects)

        raw_objects = self.build_ele.Objects.value
        attr_id = self.build_ele.AttributeID.value
        values = self.build_ele.NewValue.value

        objects = self.normalize_to_adapter_list(raw_objects)

        if not attr_id or (attr_name := BaseElements.AttributeService.GetAttributeName(self.document, attr_id)) == '???':
            self.error = f"Attribute ID {attr_id} does not exist in this project"

        if not values or values == []:
            self.error = "NewValue cannot be empty"

        if isinstance(values, str):
            values = [values]

        for idx, obj in enumerate(objects):
            element_adapters = ElementAdapter.BaseElementAdapterList()
            element_adapters.append(obj)
            new_value = values[idx] if idx < len(values) else values[-1]
            BaseElements.ElementsAttributeService.ChangeAttribute(attr_id, new_value, element_adapters)

        self.build_ele.ModifiedObjects.value = NodeObjectUtil.create_base_element_adpter_list(objects)
