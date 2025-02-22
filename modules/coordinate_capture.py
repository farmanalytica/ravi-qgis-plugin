from PyQt5.QtGui import QColor
from qgis.core import QgsWkbTypes, QgsGeometry, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
import random

# Define a class for our custom map tool
class CoordinateCaptureTool(QgsMapToolEmitPoint):
    def __init__(self, canvas, ravi_dialog):
        QgsMapToolEmitPoint.__init__(self, canvas)
        self.canvas = canvas
        self.ravi_dialog = ravi_dialog  # Reference to the main dialog
        self.rubberBands = []  # Store rubber bands for persistence
        self.latitude = None
        self.longitude = None
        self.dot_color = self.generate_bright_color()
        self.transform = QgsCoordinateTransform(self.canvas.mapSettings().destinationCrs(), QgsCoordinateReferenceSystem(4326), QgsProject.instance())
        print("CoordinateCaptureTool initialized")  # Debugging
        print(f"self.rubberBands: {self.rubberBands}")  # Debugging

    def generate_bright_color(self):
        # Generate a bright, random color
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return QColor(r, g, b, 200)  # Semi-transparent

    def canvasReleaseEvent(self, event):
        # Get the clicked point in map coordinates
        point = self.toMapCoordinates(event.pos())
        point = self.transform.transform(point)  # Transform to EPSG:4326
        self.latitude = point.y()
        self.longitude = point.x()

        # Display a dot on the canvas
        self.display_dot(point)

        # Call the Earth Engine function in the main dialog
        if self.latitude is not None and self.longitude is not None:
            self.ravi_dialog.process_coordinates(self.longitude, self.latitude)

    def display_dot(self, point):
        # Create a new rubber band (a circle)
        rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
        rubberBand.setColor(self.dot_color)
        rubberBand.setWidth(5)  # Dot size

        # Set the geometry of the rubber band to the clicked point
        rubberBand.setToGeometry(QgsGeometry.fromPointXY(point), None)
        rubberBand.show()

        # Store the rubber band for later removal
        self.rubberBands.append(rubberBand)
        print("Rubber band added to self.rubberBands")  # Debugging
        print(f"self.rubberBands: {self.rubberBands}")  # Debugging

        # Generate a new color for the next dot
        self.dot_color = self.generate_bright_color()

    def deactivate(self):
        # Clean up when the tool is deactivated
        # self.remove_all_dots()  # REMOVE THIS LINE!
        self.latitude = None  # Reset coordinates
        self.longitude = None
        print("CoordinateCaptureTool deactivated")  # Debugging

    # No remove_all_dots method here!  It's in RAVIDialog
