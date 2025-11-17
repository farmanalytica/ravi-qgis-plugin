from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsWkbTypes,
    QgsGeometry,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsPointXY,
)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsVertexMarker
import random


class CoordinateCaptureTool_2(QgsMapToolEmitPoint):
    """
    A map tool for capturing coordinates from the map canvas and processing
    them using a provided dialog. It displays a colored dot at each captured
    coordinate.
    """

    WGS84_EPSG = "EPSG:4326"  # Constant for WGS84 CRS

    # Note: previous implementation used colored dots. Now we use a fixed red 'X' marker.
    # keep DOT_COLORS for compatibility with calling code that clears it
    DOT_COLORS = []

    def __init__(self, canvas, ravi_dialog):
        """
        Initializes the CoordinateCaptureTool.

        Args:
            canvas: The QgsMapCanvas to interact with.
            ravi_dialog: A dialog object with a method to process coordinates.
        """
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.canvas = canvas
        self.ravi_dialog = ravi_dialog
        self.rubber_bands = []  # store markers/rubberbands
        self.latitude = None
        self.longitude = None
        self.wgs84_crs = QgsCoordinateReferenceSystem(
            self.WGS84_EPSG
        )  # Store CRS object

    # removed color generation: markers are fixed red 'X'

    def canvasReleaseEvent(self, event):
        """
        Handles the canvas release event (mouse click). Transforms the clicked
        point to WGS84, displays a dot, and processes the coordinates.

        Args:
            event: The QgsMapMouseEvent.
        """
        # Get the clicked point in map coordinates (project CRS)
        point_project = self.toMapCoordinates(event.pos())

        self.process_and_display(point_project)

    def process_and_display(self, point_project):
        """
        Transforms the point to WGS84, displays a dot on the canvas, and
        processes the coordinates using the ravi_dialog.

        Args:
            point_project: The point in the project's CRS.
        """
        # Transform to WGS84 (EPSG:4326)
        point_wgs84 = self.transform_to_wgs84(point_project)

        # Store WGS84 coordinates
        self.latitude = point_wgs84.y()
        self.longitude = point_wgs84.x()

        # Display dot in project CRS
        self.display_dot(point_project)

        # Call the Earth Engine function with WGS84 coordinates
        if self.latitude is not None and self.longitude is not None:
            self.ravi_dialog.process_coordinates_2(self.longitude, self.latitude)

    def transform_to_wgs84(self, point_project):
        """
        Transforms a point from the project CRS to WGS84.

        Args:
            point_project: The point in the project's CRS.

        Returns:
            The transformed point in WGS84.
        """
        project_crs = self.canvas.mapSettings().destinationCrs()
        transformer = QgsCoordinateTransform(
            project_crs, self.wgs84_crs, QgsProject.instance()
        )
        return transformer.transform(point_project)

    def display_dot(self, point):
        """
        Displays a colored dot on the map canvas at the given point.
        Clears any previous markers before adding the new one.

        Args:
            point: The point (QgsPointXY) in the project's CRS where the dot
                should be displayed.
        """
        # Clear previous markers
        self.clear_markers()
        
        # Use a fixed red 'X' marker instead of colored dot
        marker = QgsVertexMarker(self.canvas)
        try:
            marker.setCenter(point)
        except Exception:
            # older API name
            marker.setCenter(QgsPointXY(point.x(), point.y()))
        marker.setColor(QColor(255, 0, 0))
        # ICON_X draws a cross
        try:
            marker.setIconType(QgsVertexMarker.ICON_X)
        except Exception:
            # some bindings provide constants differently; ignore if unavailable
            pass
        marker.setIconSize(12)
        marker.setPenWidth(2)
        self.rubber_bands.append(marker)

    def add_dot_from_coordinates(self, longitude, latitude):
        """
        Adds a colored dot to the map canvas based on provided WGS84 coordinates.

        Args:
            longitude: The longitude of the point in WGS84.
            latitude: The latitude of the point in WGS84.
        """
        # Create a QgsPointXY object from WGS84 coordinates
        point_wgs84 = QgsPointXY(longitude, latitude)

        # Transform the point from WGS84 to the project's CRS
        project_crs = self.canvas.mapSettings().destinationCrs()
        transformer = QgsCoordinateTransform(
            self.wgs84_crs, project_crs, QgsProject.instance()
        )
        point_project = transformer.transform(point_wgs84)

        # Display the dot on the canvas
        self.display_dot(point_project)

    def clear_markers(self):
        """
        Removes all markers from the canvas and clears the rubber_bands list.
        """
        for marker in self.rubber_bands:
            try:
                self.canvas.scene().removeItem(marker)
            except Exception:
                try:
                    marker.hide()
                except Exception:
                    pass
        self.rubber_bands.clear()
        self.canvas.refresh()

    def deactivate(self):
        """
        Deactivates the tool, clearing the stored coordinates. It does NOT
        remove the dots from the canvas.
        """
        self.latitude = None
        self.longitude = None