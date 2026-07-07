""" Script for NodePointIndexPreview
"""
from __future__ import annotations

from typing import Any

import NemAll_Python_Geometry as Geometry

import GeometryValidate

from Utils import TextReferencePointPosition

from NodeUtil import NodeBase
from NodeUtil import NodePreviewUtil
from NodeUtil import NodeObjectUtil
from NodeUtil.NodeInitData import NodeInitData

NodeBase.trace_node_name('NodePointIndexPreview')


def create_node(init_data: NodeInitData) -> NodePointIndexPreview:
    """ Create the node

    Args:
        init_data: data for the node initialization

    Returns:
        instance of NodePointIndexPreview
    """
    return NodePointIndexPreview(init_data)


class NodePointIndexPreview(NodeBase):
    """ Definition of class NodePointIndexPreview
    """

    def __init__(self, init_data) -> None:
        """ Initialization of class NodePointIndexPreview

        Args:
            init_data:  data for the node initialization
        """
        super().__init__(init_data)


    def _create_output(self) -> None:
        """ Create output
        """
        if self.build_ele.Objects.value == []:
            self.error = "Object is empty"
            return

        geo_object_list = NodeObjectUtil.create_objects_list(self.build_ele.Objects.value)

        for geo_object in geo_object_list:

            points = self.get_vertices(geo_object)

            if not points:
                continue

            NodePreviewUtil.number_points(
                points= points,
                build_ele= self.build_ele,
                preview_com_prop= self.preview_com_prop,
                ref_pnt_pos= TextReferencePointPosition.CENTER_CENTER,
                height= self.build_ele.TextHeight.value,
                angle= Geometry.Angle(),
                number_prefix= "",
                start_index= 0,
                force_preview= True
                )


    def get_vertices(self,
                     geo_object: Any) -> list[Geometry.Point3D]:
        """ Get vertices of the geometry object

        Args:
            geo_object: geometry object

        Returns:
            list of vertices
        """
        if isinstance(geo_object, Geometry.Line3D):
            return [geo_object.StartPoint, geo_object.EndPoint]

        if isinstance(geo_object, (Geometry.Polyline3D, Geometry.Polygon3D, Geometry.Spline3D, Geometry.BSpline3D)):
            return list(geo_object.Points)

        if isinstance(geo_object, Geometry.Polyhedron3D):
            return [geo_object[i] for i in range(geo_object.GetVerticesCount())]

        # BRep3D
        vertices = []

        for i in range(geo_object.GetVertexCount()):
            err, vertex = geo_object.GetVertex(i)

            if GeometryValidate.element_method(err):
                vertices.append(vertex)

        return vertices
