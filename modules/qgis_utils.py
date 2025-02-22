# -*- coding: utf-8 -*-
"""QGIS related utility functions."""

from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsFeatureRequest,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsMultiBandColorRenderer,
    QgsContrastEnhancement,
    QgsProcessingFeedback,
    QgsRectangle,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsSingleBandPseudoColorRenderer,
    QgsRasterShader,
    QgsColorRampShader,
    QgsStyle,
    QgsMapLayer,
    QgsColorRamp,
    QgsLayerTreeLayer,
)
from qgis.utils import iface
import qgis
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import Qt
import processing
import os

def load_vector_layer(path, name):
    """Loads a vector layer from the given path."""
    layer = QgsVectorLayer(path, name, "ogr")
    if not layer.isValid():
        print(f"Failed to load vector layer: {path}")
        return None
    return layer

def add_vector_layer(layer):
    """Adds a vector layer to the current QGIS project."""
    QgsProject.instance().addMapLayer(layer)

def load_raster_layer(path, name):
    """Loads a raster layer from the given path."""
    layer = QgsRasterLayer(path, name)
    if not layer.isValid():
        print(f"Failed to load raster layer: {path}")
        return None
    return layer

def add_raster_layer(layer):
    """Adds a raster layer to the current QGIS project."""
    QgsProject.instance().addMapLayer(layer)

def zoom_to_layer(layer_name, margin_ratio=0.1):
    """
    Zoom to the specified layer with an optional margin.

    :param layer_name: Name of the layer to zoom to.
    :param margin_ratio: Fraction of the extent to add as margin (default is 0.1, or 10%).
    """
    project = QgsProject.instance()
    layers = project.mapLayersByName(layer_name)  # Get layers matching the name

    if not layers:
        print(f"Layer '{layer_name}' not found.")
        return

    layer = layers[0]  # Use the first matching layer
    iface = qgis.utils.iface  # Access the QGIS interface
    canvas = iface.mapCanvas()  # Get the active map canvas

    # Ensure the canvas CRS matches the layer CRS
    canvas.setDestinationCrs(layer.crs())

    # Get the layer's extent and add a margin
    layer_extent = layer.extent()
    x_margin = layer_extent.width() * margin_ratio
    y_margin = layer_extent.height() * margin_ratio

    expanded_extent = QgsRectangle(
        layer_extent.xMinimum() - x_margin,
        layer_extent.yMinimum() - y_margin,
        layer_extent.xMaximum() + x_margin,
        layer_extent.yMaximum() + y_margin,
    )

    # Set the expanded extent to the canvas
    canvas.setExtent(expanded_extent)
    canvas.refresh()

    print(f"Zoomed to layer extent with margin: {expanded_extent.toString()}")

def clip_raster_by_vector(raster_path, shapefile_path, output_path):
    """Clips a raster layer by a vector layer."""
    result = processing.run(
        "gdal:cliprasterbymasklayer",
        {
            "INPUT": raster_path,
            "MASK": shapefile_path,
            "NODATA": -9999,  # Change to appropriate NoData value if needed
            "CROP_TO_CUTLINE": True,
            "KEEP_RESOLUTION": True,
            "OUTPUT": output_path,
        },
        feedback=QgsProcessingFeedback(),
    )
    return result

def create_memory_layer(geometry_type, crs):
    """Creates a memory layer with the specified geometry type and CRS."""
    uri = f"{geometry_type}?crs={crs}"
    layer = QgsVectorLayer(uri, "memory_layer", "memory")
    return layer

def write_vector_layer(layer, output_path, driver_name="ESRI Shapefile"):
    """Writes a vector layer to the specified output path."""
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = driver_name
    error, message = QgsVectorFileWriter.writeAsVectorFormat(
        layer, output_path, "UTF-8", layer.crs(), options
    )
    if error != QgsVectorFileWriter.NoError:
        print(f"Error writing vector layer: {message}")
        return False
    return True

def add_field_to_layer(layer, field_name, field_type):
    """Adds a field to the specified vector layer."""
    layer.startEditing()
    layer.addAttribute(QgsField(field_name, field_type))
    layer.updateFields()
    layer.commitChanges()

def add_feature_to_layer(layer, geometry, attributes):
    """Adds a feature to the specified vector layer."""
    feature = QgsFeature()
    feature.setGeometry(geometry)
    feature.setAttributes(attributes)
    layer.dataProvider().addFeatures([feature])

def clear_all_raster_layers():
    """Removes all raster layers from the current QGIS project."""
    # Get the current project instance
    project = QgsProject.instance()

    # Create a copy of the layer list to avoid issues with removing during iteration
    layers_to_remove = list(project.mapLayers().values())

    # Iterate over the copied list
    for layer in layers_to_remove:
        if (
            layer.type() == QgsMapLayer.RasterLayer
            and layer.name() != "Google Hybrid"
        ):
            layer_name = layer.name()  # Store the layer name before removing it
            project.removeMapLayer(layer.id())  # Use layer.id() for removal
            print(f"Removed raster layer: {layer_name}")
            iface.mapCanvas().refresh()

def load_raster_layer_colorful(raster_file_path, layer_name):
    """Loads a raster layer with a colorful style."""
    # Load the raster layer
    raster_layer = QgsRasterLayer(raster_file_path, layer_name)
    if not raster_layer.isValid():
        print("Failed to load raster layer!")
    else:
        QgsProject.instance().addMapLayer(raster_layer, False)
        root = QgsProject.instance().layerTreeRoot()
        root.insertChildNode(0, QgsLayerTreeLayer(raster_layer))
        print("Raster layer loaded successfully!")

        # Create a color ramp shader
        color_ramp_shader = QgsColorRampShader()
        color_ramp_shader.setColorRampType(QgsColorRampShader.Interpolated)

        # Load the predefined color ramp (e.g., RdYlGn) from the QGIS style manager
        style = QgsStyle().defaultStyle()
        color_ramp = style.colorRamp("RdYlGn")

        # Check if the color ramp is successfully loaded
        if color_ramp:
            # Define the number of color stops
            num_stops = 5
            min_val = raster_layer.dataProvider().bandStatistics(1).minimumValue
            max_val = raster_layer.dataProvider().bandStatistics(1).maximumValue
            step = (max_val - min_val) / (num_stops - 1)

            # Create color ramp items by interpolating the color ramp
            color_ramp_items = []
            for i in range(num_stops):
                value = min_val + i * step
                color = color_ramp.color(
                    i / (num_stops - 1)
                )  # Interpolates color along the ramp
                color_ramp_items.append(
                    QgsColorRampShader.ColorRampItem(value, color)
                )

            # Set the color ramp items to the color ramp shader
            color_ramp_shader.setColorRampItemList(color_ramp_items)
        else:
            print("Color ramp 'RdYlGn' not found in the QGIS style library.")

        # Create a raster shader and set it to use the color ramp shader
        raster_shader = QgsRasterShader()
        raster_shader.setRasterShaderFunction(color_ramp_shader)

        # Apply the raster shader to the raster layer renderer
        renderer = QgsSingleBandPseudoColorRenderer(
            raster_layer.dataProvider(), 1, raster_shader
        )
        raster_layer.setRenderer(renderer)

        # Refresh the layer to update the visualization
        raster_layer.triggerRepaint()

def pop_aviso(aviso):
    """
    Displays a warning message box with the given message and Ok/Cancel buttons.
    Args:
        aviso (str): The warning message to display in the message box.
    Returns:
        bool: True if the Ok button is clicked, False if the Cancel button is clicked.
    Note:
        This method restores the override cursor before displaying the message box.
    """
    QApplication.restoreOverrideCursor()
    msg = QMessageBox(None)
    msg.setWindowTitle("Warning!")
    msg.setIcon(QMessageBox.Warning)
    msg.setText(aviso)

    # Set buttons with Ok on the right and Cancel on the left
    msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)

    # Access the buttons to set custom text
    cancel_button = msg.button(QMessageBox.Cancel)
    ok_button = msg.button(QMessageBox.Ok)
    cancel_button.setText("Cancel")
    ok_button.setText("Ok")

    ret = msg.exec_()  # Display the message box

    if ret == QMessageBox.Ok:
        print("Ok button clicked")
        return True
    elif ret == QMessageBox.Cancel:
        print("Cancel button clicked")
        return False

def pop_aviso_auth(aviso):
    """
    Displays a warning message box with the given message and Ok button.
    Args:
        aviso (str): The warning message to display in the message box.
    Returns:
        None
    Note:
        This method restores the override cursor before displaying the message box.
    """
    QApplication.restoreOverrideCursor()
    msg = QMessageBox(None)
    msg.setWindowTitle("Warning!")
    msg.setIcon(QMessageBox.Warning)
    msg.setText(aviso)

    # Set buttons with Ok on the right
    msg.setStandardButtons(QMessageBox.Ok)

    # Access the buttons to set custom text
    ok_button = msg.button(QMessageBox.Ok)
    ok_button.setText("Ok")

    msg.exec_()
