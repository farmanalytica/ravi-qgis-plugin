# RAVI - Remote Analysis of Vegetation Indices

RAVI is a QGIS plugin designed to seamlessly integrate with Google Earth Engine (GEE), enabling efficient processing and visualization of geospatial data. Utilizing the Sentinel-2 [harmonized surface reflectance catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED), the plugin supports vegetation index calculations and easy download of multispectral imagery. These features make it viable tool for students, researchers, farmers, and GIS professionals working in agriculture, land monitoring, or environmental management.

## Key Features

### 1. Earth Engine Integration
- **Easy Authentication**: Authenticate with Google Earth Engine to enable plugin functionality.
- **Direct Processing**: Access, process, and analyze Sentinel-2 imagery without leaving QGIS.
- **On-the-Fly Visualization**: Visualize processed data as raster layers or interactive plots.

### 2. Vegetation Index Calculations
- **Supported Indices**: Compute indices such as NDVI, EVI, SAVI and GNDVI.
- **Customizable Metrics**: Aggregate data using mean, max, min, median, amplitude, or standard deviation.

### 3. Advanced Time Series Analysis
- Generate time series for vegetation indices over a defined Area of Interest (AOI).
- Integrate precipitation data from NASA POWER for cross-variable comparisons.
- Smooth data with Savitzky-Golay filters for enhanced trend analysis.

### 4. AOI Selection
- **AOI Management**: Load areas of interest from shapefiles or GeoJSON files.

### 5. Interactive Visualization
- **Charts**: Create interactive time series plots using Plotly.
- **Raster Styling**: Apply predefined color ramps (e.g., RdYlGn) for visual clarity.
- **Export Options**: Export processed data as GeoTIFFs, CSVs, or styled rasters.

### 6. Comprehensive Imagery Management
- **Date Filtering**: Filter individual images by acquisition date.
- **Cloud Filtering**: Exclude or mask cloudy pixels while preserving usable data.
- **Composite Creation**: Generate composite images based on user-defined metrics.

## Installation

To install RAVI:

1. Open QGIS and navigate to the **Plugins** menu.
2. Select **Manage and Install Plugins**.
3. In the plugin repository settings, enable **Show also experimental plugins**.
  ![Show also experimental plugins](media/experimental.png)
4. In the "All" tab, search for "RAVI", select it, and click **Install**.
5. Ensure that RAVI is checked in the installed plugins list.
6. Restart QGIS.

## Usage

### Step 1: Authentication
![Step 1](media/step1.png)
- Open the plugin dialog.
- Authenticate with Google Earth Engine using your credentials.

### Step 2: Select output folder
![Step 2](media/step2.png)
- Choose the folder where you want to save the output files.

### Step 3: Load and select the area of interest (AOI)
![Step 3](media/step3.png)
- Select an AOI by loading a shapefile or GeoJSON file.
- Ensure the geometry is valid (Polygon or MultiPolygon only).
- Add a Google Maps layer to the QGIS canvas for better visualization and context.
- Use the **Build AOI from Canvas Extent** button to automatically generate a new AOI based on the current canvas extent.

### Step 4: Define time range for imagery search
![Step 4](media/step4.png)
- Set a custom time range or select a suggested one.

### Step 5: Select vegetation index for time series analysis
![Step 5](media/step5.png)
- Choose the vegetation index you want to analyze from the dropdown menu.

### Step 6: Imagegery Overlap filter and AOI Buffer filter options
![Step 6](media/step6.png)
- Set the specified filter according to your analysis requirements.

### Step 7: AOI Buffer
![Step 7](media/step7.png)
- Use AOI Buffer filter to reduce the AOI boundary for analysis.

### Step 8: Cloud pixel percentage filter
![Step 8](media/step8.png)
- Set the specified filter according to your analysis requirements.

### Step 9: Valid pixel percentage filter
![Step 9](media/step9.png)
- Set the specified filter according to your analysis requirements.

### Results Page

The results page includes the following features:

### 1. Time Series Plot
![1](/media/results1.png)
- Visualize the time series of the selected vegetation index over the defined AOI.
- Hover over the plot to see specific values and dates for detailed analysis.

### 2. Load RGB Layer (Focus on a Day)
![2](/media/results2.png)
- Load and display an RGB layer for a specific date to analyze the visual appearance of the area. All spectral bands are downloaded, and the band numbers correspond to the Sentinel-2 bands as listed in the table below:

| Sentinel-2 Band Name         | QGIS Band Number | Wavelength (nm) | Spatial Resolution (m) |
|------------------------------|------------------|-----------------|------------------------|
| Band 1 (Coastal aerosol)     | 1                | 443             | 60                     |
| Band 2 (Blue)                | 2                | 490             | 10                     |
| Band 3 (Green)               | 3                | 560             | 10                     |
| Band 4 (Red)                 | 4                | 665             | 10                     |
| Band 5 (Vegetation Red Edge) | 5                | 705             | 20                     |
| Band 6 (Vegetation Red Edge) | 6                | 740             | 20                     |
| Band 7 (Vegetation Red Edge) | 7                | 783             | 20                     |
| Band 8 (NIR)                 | 8                | 842             | 10                     |
| Band 8A (Vegetation Red Edge)| 9                | 865             | 20                     |
| Band 9 (Water Vapour)        | 10               | 945             | 60                     |
| Band 10 (SWIR - Cirrus)      | 11               | 1375            | 60                     |
| Band 11 (SWIR)               | 12               | 1610            | 20                     |
| Band 12 (SWIR)               | 13               | 2190            | 20                     |


### 3. Load Index Layer (Focus on a Day)
![3](/media/results3.png)
- Load and display a vegetation index layer for a specific date.

### 4. Load Index Layer (Composite Image)
![4](/media/results4.png)
- Generate and display a composite image based on the selected vegetation index and the user-defined metric.
- The composite image will include all images within the current date selection. Use the date selection tool to filter out specific dates.

### 5. Date Selection Tool
![5](/media/results5.png)
- Use the date selection tool to filter and select specific dates for analysis.
- The date selection tool updates the time series plot
- Composite images are based on all selected dates.

### 6. Savitzky-Golay Filter
![6](/media/results6.png)
- Apply the Savitzky-Golay filter to smooth the time series data for enhanced trend analysis.
- The parameters for the Savitzky-Golay algorithm, such as the order of the polynomial and the window length, can be adjusted as needed to fine-tune the smoothing process.

### 7. Save Options
![7](/media/results7.png)
![71](/media/results71.png)
- Save the time series data in spreasheet format (CSV).
- To save the time series as image, open it in the browser to enable the download option.

### 8. NASA POWER Precipitation
![8](/media/results8.png)
- Add monthly precipitation data from NASA POWER for cross-variable comparisons.
- Save the precipitation data in spreasheet format (CSV).

### 9. Quickly Reload Time Series
![9](/media/results9.png)
- Quickly reload a new time series analysis by changing the Area of Interest (AOI), Vegetation Index, or time range.

### 10. Clear All Loaded Layers
![10](/media/results10.png)
- Clear all loaded layers from the layer panel to start a new analysis or to declutter the workspace.

## Troubleshooting
- **Earth Engine Authentication Failed**: Ensure you have the necessary requirements as explained in the authentication tab.
- **AOI Errors**: Verify the AOI file is valid and has a valid CRS (EPSG:4326 preferred).

## Reporting Issues
If you encounter any issues or have suggestions for improvements, please open an issue in the [GitHub Issues](https://github.com/caioarantes/ravi-qgis-plugin/issues) section.

## Contribute to the Project
Contributions are welcome! Please visit the [GitHub repository](https://github.com/caioarantes/ravi-qgis-plugin) to get started.

## License
RAVI is licensed under the GNU General Public License v2.0 or later. Refer to the LICENSE file for details.