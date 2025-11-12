""" Script for NodeSetOrCreateAttribute
"""
from __future__ import annotations

from typing import Any

import re

from enum            import Enum
from datetime        import datetime
from datetime        import date
from dateutil.parser import parse as dateutil_parse

import NemAll_Python_BaseElements as BaseElements
import NemAll_Python_Utility      as Utility

from BuildingElementAttributeList import BuildingElementAttributeList

from NodeUtil import NodeBase
from NodeUtil.NodeInitData import NodeInitData


NodeBase.trace_node_name('NodeSetOrCreateAttribute')


class AttrDataType(Enum):
    """ Dictionnary of attribute types
    """
    STRING = BaseElements.AttributeService.AttributeType.String
    INTEGER = BaseElements.AttributeService.AttributeType.Integer
    DOUBLE = BaseElements.AttributeService.AttributeType.Double
    DATE = BaseElements.AttributeService.AttributeType.Date
    ENUM = BaseElements.AttributeService.AttributeType.Enum


def create_node(init_data: NodeInitData) -> NodeSetOrCreateAttribute:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodeSetOrCreateAttribute
    """

    return NodeSetOrCreateAttribute(init_data)


class NodeSetOrCreateAttribute(NodeBase):
    """ Definition of class NodeSetOrCreateAttribute
    """

    def __init__(self, init_data) -> None:
        """ Initialization of class NodeSetOrCreateAttribute

        Args:
            init_data:  data for the node initialization
        """
        super().__init__(init_data)

        self.error = ""
        self.attr_id = 0


    def _create_output(self) -> None:
        """ Execute the node
        """
        self._set_init_node_output(self.build_ele.AttributeID)

        attr_name = self.build_ele.AttributeName.value
        attr_value = self.build_ele.AttributeValue.value

        if attr_value is None or attr_value == '':
            self.warning = "Empty value."
            return

        if isinstance(attr_value, list):
            attr_value = attr_value[0]

        # Try to get attribute id
        self.attr_id = BaseElements.AttributeService.GetAttributeID(self.document, attr_name)

        # Create new attribute
        if self.attr_id == -1:
            self.create_attr(attr_name, attr_value)
        # Set attribute
        else:
            attr_data_type = BaseElements.AttributeService.GetAttributeType(self.document, self.attr_id)
            self.check_and_assign_attr(attr_value, attr_data_type)

        self.build_ele.AttributeID.value = self.attr_id


    def create_attr(self,
                    attr_name: str,
                    value: Any) -> None:
        """ Create a new attribute

        Args:
            attr_name: name of the new attribute
            value:     input value
        """
        attr_data_type = self.guess_attr_type(value)

        if attr_data_type in [BaseElements.AttributeService.AttributeType.Double,
                              BaseElements.AttributeService.AttributeType.Integer]:
            min_value = -999999999
            max_value =  999999999
        else:
            min_value = max_value = 0

        self.attr_id = BaseElements.AttributeService.AddUserAttribute(
            doc= self.document,
            attributeType= attr_data_type,
            attributeName= attr_name,
            attributeDefaultValue= "",
            attributeMinValue= min_value,
            attributeMaxValue= max_value,
            attributeDimension= "",
            attributeCtrlType= BaseElements.AttributeService.AttributeControlType.Edit,
            attributeListValues= Utility.VecStringList()
            )


    def check_and_assign_attr(self,
                              value: Any,
                              data_type: BaseElements.AttributeService.AttributeType) -> None:
        """ Test if value and data_type are matching and assign it

        Args:
            value: input value
            data_type: type of attribute
        """
        try:
            if data_type == AttrDataType.STRING.value:
                self.build_ele.node_attribute_list.append(BaseElements.AttributeString(self.attr_id, str(value)))
                return
            elif data_type == AttrDataType.INTEGER.value:
                self.build_ele.node_attribute_list.append(BaseElements.AttributeInteger(self.attr_id, int(value)))
                return
            elif data_type == AttrDataType.DOUBLE.value:
                self.build_ele.node_attribute_list.append(BaseElements.AttributeDouble(self.attr_id, float(value)))
                return
            elif data_type == AttrDataType.DATE.value:
                day, month, year = self.convert_str_to_date(value)
                self.build_ele.node_attribute_list.append(BaseElements.AttributeDate(self.attr_id, day, month, year))
                return
            elif data_type == AttrDataType.ENUM.value:
                self.build_ele.node_attribute_list.append(BaseElements.AttributeEnum(self.attr_id, int(value)))
                return
        except Exception:
            self.error = f"Value type isn't in compliance with attribute type: {AttrDataType(data_type).name}."


    def convert_str_to_date(self,
                            text: str) -> tuple[int, int, int]:
        """ Convert a string to a date
        """
        text_str = str(text).strip()

        date_obj = re.sub(r"[- /]", ".", str(text_str))

        # Date from dd.mm.yyyy or dd.mm.yy
        for fmt in ("%d.%m.%Y", "%d.%m.%y"):
            try:
                date = datetime.strptime(date_obj, fmt).date()
                return (date.day, date.month, date.year)
            except Exception:
                pass

        # Date from yyyy-mm-dd
        date_iso = re.sub(r"[. /]", "-", str(text_str))
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                date = datetime.strptime(date_iso, fmt).date()
                return (date.day, date.month, date.year)
            except Exception:
                pass

        # Parse using dateutil
        try:
            date = dateutil_parse(text_str, dayfirst= True).date()
            return (date.day, date.month, date.year)
        except Exception:
            pass

        # Invalid date
        self.error = "Parameter value is not a valid date. Reset the value to current date."
        return (datetime.now().day, datetime.now().month, datetime.now().year)


    def guess_attr_type(self,
                        value: Any) -> BaseElements.AttributeService.AttributeType:
        """ Determine type of value to create a new attribute

        Args:
            value: input value

        Returns:
            type of value
        """
        if isinstance(value, (datetime, date)):
            return AttrDataType.DATE.value
        if isinstance(value, int):
            return AttrDataType.INTEGER.value
        if isinstance(value, float):
            return AttrDataType.DOUBLE.value
        return AttrDataType.STRING.value
