import zipfile
import geopandas as gpd
import ee


def load_aoi(self, shapefile_path):
    """
    Loads the vector layer from the selected file path, reprojects it to
    EPSG:4326, dissolves multiple features if necessary, and converts it
    into an Earth Engine FeatureCollection representing the AOI.
    """
    """
    Carrega a camada vetorial do caminho do arquivo selecionado, a
    reprojeta para EPSG:4326, dissolve várias feições, se necessário, e a
    converte em um Earth Engine FeatureCollection representando a AOI.
    """
    if shapefile_path is None:
        shapefile_path = self.selected_aio_layer_path

    try:
        # Load the shapefile, handling both .zip archives and regular files.
        if shapefile_path.endswith(".zip"):
            with zipfile.ZipFile(shapefile_path, "r") as zip_ref:
                shapefile_found = False
                for file in zip_ref.namelist():
                    if file.endswith(".shp"):
                        shapefile_found = True
                        shapefile_within_zip = file
                        break
                if not shapefile_found:
                    print("No .shp file found inside the zip archive.")
                    return

                # Read shapefile directly from the zip archive.
                aoi = gpd.read_file(
                    f"zip://{shapefile_path}/{shapefile_within_zip}"
                )
        else:
            aoi = gpd.read_file(shapefile_path)

        # Reproject the GeoDataFrame to EPSG:4326 to ensure correct
        # coordinates for Earth Engine.
        aoi = aoi.to_crs(epsg=4326)

        if aoi.empty:
            print("The shapefile does not contain any geometries.")
            return

        # Dissolve multiple features into a single geometry if necessary.
        if len(aoi) > 1:
            aoi = aoi.dissolve()

        # Extract the first geometry.
        geometry = aoi.geometry.iloc[0]

        # Convert the geometry to GeoJSON format.
        geojson = geometry.__geo_interface__

        # Remove any third dimension from the coordinates.
        if geojson["type"] == "Polygon":
            geojson["coordinates"] = [
                list(map(lambda coord: coord[:2], ring)) for ring in geojson["coordinates"]
            ]
        elif geojson["type"] == "MultiPolygon":
            geojson["coordinates"] = [
                [list(map(lambda coord: coord[:2], ring)) for ring in polygon]
                for polygon in geojson["coordinates"]
            ]

        # Create an Earth Engine geometry object.
        ee_geometry = ee.Geometry(geojson)
        feature = ee.Feature(ee_geometry)
        aoi = ee.FeatureCollection([feature])

        print("AOI defined successfully.")

        return aoi