from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsWkbTypes,
    QgsGeometry,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsPointXY,
)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
import random


class CoordinateCaptureTool(QgsMapToolEmitPoint):
    """
    A map tool for capturing coordinates from the map canvas and processing
    them using a provided dialog. It displays a colored dot at each captured
    coordinate.
    """

    WGS84_EPSG = "EPSG:4326"  # Constant for WGS84 CRS

    # Global variable to store colors
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
        self.rubber_bands = []  # Use snake_case for variable names
        self.latitude = None
        self.longitude = None
        self.dot_color = self.generate_bright_color()
        # Don't add the color here - will add it when actually used
        self.wgs84_crs = QgsCoordinateReferenceSystem(
            self.WGS84_EPSG
        )  # Store CRS object

    def generate_bright_color(self):
        """Generates a random bright color for the dot."""
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return QColor(r, g, b, 200)

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
            self.ravi_dialog.process_coordinates(self.longitude, self.latitude)

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

        Args:
            point: The point (QgsPointXY) in the project's CRS where the dot
                should be displayed.
        """
        rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        rubber_band.setColor(self.dot_color)
        rubber_band.setWidth(5)

        # Create geometry in project CRS
        rubber_band.setToGeometry(QgsGeometry.fromPointXY(point), None)
        rubber_band.show()

        # Add the current color to the list when it's actually used
        CoordinateCaptureTool.DOT_COLORS.append(self.dot_color)
        self.rubber_bands.append(rubber_band)
        
        # Generate a new color for the next dot
        self.dot_color = self.generate_bright_color()

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

    def deactivate(self):
        """
        Deactivates the tool, clearing the stored coordinates. It does NOT
        remove the dots from the canvas.
        """
        self.latitude = None
        self.longitude = None