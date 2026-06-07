# -*- coding: utf-8 -*-
"""
AOI service layer.

Extract and convert uploaded AOI geometries to EE objects.
"""

import json
import ee

from qgis.core import (
    QgsProject,
    QgsMapLayer,
    QgsWkbTypes,
    QgsGeometry,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
)


def _remove_z_dimension(coords):

    if isinstance(coords[0], (int, float)):
        return coords[:2]
    return [_remove_z_dimension(c) for c in coords]


class AOIService:
    """Service for extracting and converting AOI geometries to Earth Engine objects."""

    @staticmethod
    def _validate_vector_polygon_layer(layer):

        if not layer or layer.type() != QgsMapLayer.VectorLayer:
            raise ValueError("Layer must be a valid vector layer.")

        if layer.geometryType() != QgsWkbTypes.PolygonGeometry:
            raise ValueError("Layer must be polygon or multipolygon.")

    @staticmethod
    def _get_layer_by_id(layer_id):

        layer = QgsProject.instance().mapLayer(layer_id)
        AOIService._validate_vector_polygon_layer(layer)

        return layer

    @staticmethod
    def _get_dissolved_geometry(layer, use_selected_features=True):

        features = (
            layer.selectedFeatures()
            if use_selected_features and layer.selectedFeatureCount() > 0
            else list(layer.getFeatures())
        )
        geometries = [f.geometry() for f in features]

        if not geometries:
            raise ValueError("Layer has no geometries.")

        return QgsGeometry.unaryUnion(geometries)

    @staticmethod
    def _layer_to_ee_feature_collection(layer, use_selected_features=True):
        """
        Convert a QGIS layer's to an Earth Engine FeatureCollection, assuring
        compatibility (2D and EPSG:4326)

        Returns a tuple of FeatureCollection and Bounding Box [min_x, min_y, max_x, max_y]
        """
        geometry = AOIService._get_dissolved_geometry(layer, use_selected_features)

        if geometry.isEmpty():
            raise ValueError("Empty geometry.")

        if not geometry.isGeosValid():
            geometry = geometry.makeValid()

        if layer.crs().authid() != "EPSG:4326":
            transform = QgsCoordinateTransform(
                layer.crs(),
                QgsCoordinateReferenceSystem("EPSG:4326"),
                QgsProject.instance(),
            )
            geometry.transform(transform)

        rectangle = geometry.boundingBox()
        bbox = (
            rectangle.xMinimum(),
            rectangle.yMinimum(),
            rectangle.xMaximum(),
            rectangle.yMaximum(),
        )

        geojson_str = geometry.asJson()
        if not geojson_str:
            raise ValueError(
                f"Could not export geometry to GeoJSON. "
                f"Geometry type: {geometry.type()}, WKB type: {geometry.wkbType()}"
            )

        geojson = json.loads(geojson_str)
        geojson["coordinates"] = _remove_z_dimension(geojson["coordinates"])

        ee_geometry = ee.Geometry(geojson)
        return ee.FeatureCollection([ee.Feature(ee_geometry)]), bbox

    @staticmethod
    def get_ee_feature_colection_from_layer(layer, use_selected_features=True):

        AOIService._validate_vector_polygon_layer(layer)
        return AOIService._layer_to_ee_feature_collection(layer, use_selected_features)

    @staticmethod
    def get_ee_feature_colection_from_layer_id(layer_id, use_selected_features=True):
        layer = AOIService._get_layer_by_id(layer_id)
        return AOIService._layer_to_ee_feature_collection(layer, use_selected_features)
