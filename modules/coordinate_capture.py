from PyQt5.QtGui import QColor
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
    def __init__(self, canvas, ravi_dialog):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.canvas = canvas
        self.ravi_dialog = ravi_dialog
        self.rubberBands = []
        self.latitude = None
        self.longitude = None
        self.dot_color = self.generate_bright_color()

    def generate_bright_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return QColor(r, g, b, 200)

    def canvasReleaseEvent(self, event):
        # Get the clicked point in map coordinates (project CRS)
        point_project = self.toMapCoordinates(event.pos())

        # Create coordinate transformer for the current project CRS
        project_crs = self.canvas.mapSettings().destinationCrs()
        wgs84_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        transformer = QgsCoordinateTransform(project_crs, wgs84_crs, QgsProject.instance())

        # Transform to WGS84 (EPSG:4326)
        point_wgs84 = transformer.transform(point_project)

        # Store WGS84 coordinates
        self.latitude = point_wgs84.y()
        self.longitude = point_wgs84.x()

        # Display dot in project CRS
        self.display_dot(point_project)

        # Call the Earth Engine function with WGS84 coordinates
        if self.latitude is not None and self.longitude is not None:
            self.ravi_dialog.process_coordinates(self.longitude, self.latitude)

    def display_dot(self, point):
        rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        rubberBand.setColor(self.dot_color)
        rubberBand.setWidth(5)

        # Create geometry in project CRS
        rubberBand.setToGeometry(QgsGeometry.fromPointXY(point), None)
        rubberBand.show()

        self.rubberBands.append(rubberBand)
        self.dot_color = self.generate_bright_color()

    def deactivate(self):
        self.latitude = None
        self.longitude = None
