from qgis.core import QgsProject, QgsRasterLayer, QgsCoordinateReferenceSystem
from qgis.utils import iface
from qgis.core import QgsRasterLayer, QgsLayerTreeLayer, QgsColorRampShader, QgsStyle, QgsRasterShader, QgsSingleBandPseudoColorRenderer

print("Loading map_tools.py...")

def hybrid_function():
    """Adds a Google Hybrid XYZ tile layer to the QGIS project if it is not already present."""
    existing_layers = QgsProject.instance().mapLayers().values()
    layer_names = [layer.name() for layer in existing_layers]
    if "Google Hybrid" in layer_names:
        print("Google Hybrid layer already added.")
        return

    google_hybrid_url = "type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Dy%26x%3D{x}%26y%3D{y}%26z%3D{z}"
    layer_name = "Google Hybrid"
    provider_type = "wms"

    try:
        # Create the XYZ tile layer
        google_hybrid_layer = QgsRasterLayer(google_hybrid_url, layer_name, provider_type)

        if google_hybrid_layer.isValid():
            # Add the layer to the project
            QgsProject.instance().addMapLayer(google_hybrid_layer, False)

            # Set the project CRS to EPSG:4326 (WGS 84)
            crs_4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            QgsProject.instance().setCrs(crs_4326)

            # Adjust visibility and add to the layer tree
            google_hybrid_layer.setOpacity(1)
            root = QgsProject.instance().layerTreeRoot()
            root.addLayer(google_hybrid_layer)

            # Refresh the canvas and zoom to extent
            iface.mapCanvas().refresh()
            iface.mapCanvas().zoomToFullExtent()
            print(f"{layer_name} layer added successfully in EPSG:4326.")
        else:
            print(f"Failed to load {layer_name}. Invalid layer.")
    except Exception as e:
        print(f"Error loading {layer_name}: {e}")

def load_raster_layer_colorful(raster_file_path, layer_name, index, metrica):
    print(f"Loading raster layer color: {index}")

    # Load the raster layer
    raster_layer = QgsRasterLayer(raster_file_path, layer_name)
    if not raster_layer.isValid():
        print("Failed to load raster layer!")
        return
    
    # Get min and max values from the raster
    min_val = raster_layer.dataProvider().bandStatistics(1).minimumValue
    max_val = raster_layer.dataProvider().bandStatistics(1).maximumValue
    
    # # For NDVI that's not AUC, use 0-1 range instead
    # use_ndvi_range = (index == 'NDVI' and metrica != 'Area Under Curve (AUC)')
    
    # # If it's NDVI (not AUC), override the min/max values
    # if use_ndvi_range:
    #     display_min = 0
    #     display_max = 1
    #     print('Using NDVI range 0-1')
    # else:
    #     display_min = min_val
    #     display_max = max_val
    #     print(f'Using data range {min_val} to {max_val}')


    display_min = min_val
    display_max = max_val

    QgsProject.instance().addMapLayer(raster_layer, False)
    root = QgsProject.instance().layerTreeRoot()
    root.insertChildNode(0, QgsLayerTreeLayer(raster_layer))
    print("Raster layer loaded successfully!")

    # Create a color ramp shader
    color_ramp_shader = QgsColorRampShader()
    color_ramp_shader.setColorRampType(QgsColorRampShader.Interpolated)

    # Load the predefined color ramp (e.g., RdYlGn) from the QGIS style manager
    style = QgsStyle().defaultStyle()
    color_ramp = style.colorRamp('RdYlGn')

    # Check if the color ramp is successfully loaded
    if color_ramp:
        # Define the number of color stops
        num_stops = 5
        step = (display_max - display_min) / (num_stops - 1)

        # Create color ramp items using the display range
        color_ramp_items = []
        for i in range(num_stops):
            value = display_min + i * step
            color = color_ramp.color(i / (num_stops - 1))  # Interpolates color along the ramp
            color_ramp_items.append(QgsColorRampShader.ColorRampItem(value, color))

        # Set the color ramp items to the color ramp shader
        color_ramp_shader.setColorRampItemList(color_ramp_items)
    else:
        print("Color ramp 'RdYlGn' not found in the QGIS style library.")

    # Create a raster shader and set it to use the color ramp shader
    raster_shader = QgsRasterShader()
    raster_shader.setRasterShaderFunction(color_ramp_shader)

    # Apply the raster shader to the raster layer renderer
    renderer = QgsSingleBandPseudoColorRenderer(raster_layer.dataProvider(), 1, raster_shader)
    
    # Set the classification range to match the display range
    renderer.setClassificationMin(display_min)
    renderer.setClassificationMax(display_max)
    
    raster_layer.setRenderer(renderer)

    # Refresh the layer to update the visualization
    raster_layer.triggerRepaint()
    iface.mapCanvas().refresh()
