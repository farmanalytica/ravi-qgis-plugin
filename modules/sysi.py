import zipfile
import geopandas as gpd
import ee


def load_aoi(self, sentinel2_collection=None):

    #collection size
    print(sentinel2_collection.size().getInfo())
