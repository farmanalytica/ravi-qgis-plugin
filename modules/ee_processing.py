# ee_processing.py
import ee
import pandas as pd
from scipy.signal import savgol_filter
import requests
from datetime import datetime
from .modules import nasa_power


class EEProcessor:
    def __init__(self, parent):
        self.parent = parent

    def authenticate_ee(self, project_id):
        """Authenticates Earth Engine and initializes the API."""
        """Autentica o Earth Engine e inicializa a API."""
        try:
            ee.Authenticate()
            ee.Initialize(project=project_id)
            return True
        except Exception as e:
            print(f"Earth Engine authentication failed: {e}")
            return False

    def open_nasapower(self, lat, lon, start_date, end_date):
        """Opens NASA POWER data for a given latitude, longitude, and date range."""
        """Abre os dados do NASA POWER para uma determinada latitude, longitude e
        intervalo de datas."""
        df_nasa, daily_precipitation = nasa_power.open_nasapower(
            lat, lon, start_date, end_date
        )
        return df_nasa, daily_precipitation

    def calculate_index(self, image, vegetation_index):
        """Calculates the specified vegetation index for an image."""
        """Calcula o índice de vegetação especificado para uma imagem."""
        if vegetation_index == "NDVI":
            index_image = image.normalizedDifference(["B8", "B4"]).rename("index")
        elif vegetation_index == "EVI":
            index_image = image.expression(
                "2.5 * ((NIR / 10000 - RED / 10000) / (NIR / 10000 + 6 * RED / 10000 - 7.5 * BLUE / 10000 + 1))",
                {
                    "NIR": image.select("B8"),
                    "RED": image.select("B4"),
                    "BLUE": image.select("B2"),
                },
            ).rename("index")
        elif vegetation_index == "SAVI":
            L = 0.5
            index_image = image.expression(
                "(1 + L) * ((NIR / 10000) - (RED / 10000)) / ((NIR / 10000) + (RED / 10000) + L)",
                {
                    "NIR": image.select("B8"),
                    "RED": image.select("B4"),
                    "L": L,
                },
            ).rename("index")
        elif vegetation_index == "GCI":
            index_image = image.expression(
                "NIR / GREEN - 1",
                {"NIR": image.select("B8"), "GREEN": image.select("B3")},
            ).rename("index")
        elif vegetation_index == "GNDVI":
            index_image = image.normalizedDifference(["B8", "B3"]).rename("index")
        else:
            raise ValueError(f"Unsupported vegetation index: {vegetation_index}")
        return index_image

    def calculate_timeseries(self, sentinel2, aoi, vegetation_index, buffer_distance):
        """Calculates the time series of the selected vegetation index for the AOI."""
        """Calcula a série temporal do índice de vegetação selecionado para a
        AOI."""

        # Buffer the AOI geometry inward by 10 meters (adjust distance as
        # needed)
        if buffer_distance != 0:
            print(f"Buffer distance: {buffer_distance} meters")
            aoi = aoi.map(lambda feature: feature.buffer(buffer_distance))
        else:
            print("No buffer applied")
            aoi = aoi

        # Define the vegetation index calculation in a function
        def calculate_index_wrapper(image):
            index_image = self.calculate_index(image, vegetation_index)

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = sentinel2.map(calculate_index_wrapper)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()
        image_ids = result.aggregate_array("system:index").getInfo()

        # Combine the dates, mean indices, and image IDs into a DataFrame
        df = pd.DataFrame(
            {"date": dates, "AOI_average": mean_indices, "image_id": image_ids}
        )

        return df

    def point_calculate_timeseries(self, sentinel2, aoi, vegetation_index, name):
        """Calculates the time series of the selected vegetation index for a
        specific point."""
        """Calcula a série temporal do índice de vegetação selecionado para um
        ponto específico."""

        # Define the vegetation index calculation in a function
        def calculate_index_wrapper(image):
            index_image = self.calculate_index(image, vegetation_index)

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = sentinel2.map(calculate_index_wrapper)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()

        # Combine the dates, mean indices
        print(f"Creating DataFrame for {name}")
        return pd.DataFrame({"date": dates, name: mean_indices})

    def feature_calculate_timeseries(self, sentinel2, aoi, vegetation_index, name, buffer_distance):
        """Calculates the time series of the selected vegetation index for a
        specific feature."""
        """Calcula a série temporal do índice de vegetação selecionado para uma
        feição específica."""

        # Buffer the AOI geometry inward by 10 meters (adjust distance as
        # needed)
        if buffer_distance != 0:
            print(f"Buffer distance: {buffer_distance} meters")
            aoi = aoi.map(lambda feature: feature.buffer(buffer_distance))
        else:
            print("No buffer applied")
            aoi = aoi

        # Define the vegetation index calculation in a function
        def calculate_index_wrapper(image):
            index_image = self.calculate_index(image, vegetation_index)

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = sentinel2.map(calculate_index_wrapper)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()

        # Combine the dates, mean indices
        print(f"Creating DataFrame for {name}")
        return pd.DataFrame({"date": dates, name: mean_indices})

    def apply_savitzky_golay_filter(self, df, window_length, polyorder):
        """Applies the Savitzky-Golay filter to smooth the time series data."""
        """Aplica o filtro Savitzky-Golay para suavizar os dados da série
        temporal."""
        try:
            if window_length > len(df):
                window_length = len(df)
                print(f"Window length too large. Using maximum value: {window_length}")

            # Apply Savitzky-Golay filter to smooth the time series
            df["savitzky_golay_filtered"] = savgol_filter(
                df["AOI_average"], window_length=window_length, polyorder=polyorder
            )
            return df
        except Exception as e:
            print(
                f"Error applying Savitzky-Golay filter: {e}"
            )  # Log the error for debugging
            return None

    def ee_load_collection(self, inicio, final, nuvem, aoi, coverage_threshold, local_pixel_limit, mask, scl_classes_behavior):
        """Loads the Earth Engine image collection based on user-defined
        criteria."""
        """Carrega a coleção de imagens do Earth Engine com base nos critérios
        definidos pelo usuário."""

        # Define the Sentinel-2 image collection with filtering by date, bounds,
        # and cloud percentage
        sentinel2 = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterDate(inicio, final)
            .filterBounds(aoi)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", nuvem))
            .map(lambda image: image.set("date", image.date().format("YYYY-MM-dd")))
        )

        # Check if the collection is empty
        if sentinel2.size().getInfo() == 0:
            return None, "No images found for the selected criteria. Please select a larger date range or less strick filtering and try again."

        # Apply AOI coverage filter to the image collection
        if coverage_threshold > 0:
            sentinel2, message = self.AOI_coverage_filter(sentinel2, aoi, coverage_threshold)
            if sentinel2 is None:
                return None, message

        if local_pixel_limit > 0:
            # Apply local pixel limit filter to the image collection
            sentinel2, message = self.filter_within_AOI(sentinel2, aoi, local_pixel_limit, scl_classes_behavior)
            if sentinel2 is None:
                return None, message

        # Apply cloud and shadow mask if the checkbox is checked
        if mask:
            sentinel2 = self.SCL_filter(sentinel2, aoi, scl_classes_behavior)
            if sentinel2.size().getInfo() == 0:
                return None, "No images found for the selected criteria. Please select a larger date range or less strick filtering and try again."

        sentinel2 = self.uniqueday_collection(sentinel2)

        return sentinel2, None

    def uniqueday_collection(self, sentinel2):
        """Filters the image collection to include only one image per day."""
        """Filtra a coleção de imagens para incluir apenas uma imagem por dia."""
        print("Filtering to unique days...")
        print("Original collection size:", sentinel2.size().getInfo())
        # Step 1: Aggregate timestamps from the ImageCollection
        original_timestamps = sentinel2.aggregate_array("system:time_start").getInfo()

        # Step 2: Convert timestamps to formatted dates
        formatted_dates = [
            datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")
            for ts in original_timestamps
        ]

        # Step 3: Identify unique dates and map them back to the original
        # timestamps
        df = pd.DataFrame(
            list(zip(original_timestamps, formatted_dates)),
            columns=["timestamp", "date"],
        )
        first_timestamps_per_date = df.groupby("date")["timestamp"].min().tolist()

        print(f"Number of unique dates: {len(first_timestamps_per_date)}")

        # Step 4: Filter the collection to include only the first image for each
        # unique date
        return sentinel2.filter(
            ee.Filter.inList("system:time_start", ee.List(first_timestamps_per_date))
        )

    def AOI_coverage_filter(self, sentinel2, aoi, coverage_threshold):
        """Filters the image collection based on the coverage of the Area of
        Interest (AOI)."""
        """Filtra a coleção de imagens com base na cobertura da Área de
        Interesse (AOI)."""
        if coverage_threshold == 1:
            coverage_threshold = 0.9999  # Avoid floating-point comparison issues

        # Coverage Ratio Function
        aoi_geometry = aoi.first().geometry()
        aoi_area = aoi_geometry.area()

        def calculate_coverage_ratio(image):
            """
            Calculates the ratio of the AOI area covered by the image.

            Args:
                image (ee.Image): The Sentinel-2 image.

            Returns:
                ee.Image: The original image with an added 'coverage_ratio'
                    property.
            """
            # Compute the intersection geometry between AOI and image footprint
            intersection = aoi_geometry.intersection(image.geometry(), ee.ErrorMargin(1))

            # Calculate the area of the intersection
            intersection_area = intersection.area()

            # Calculate the coverage ratio (intersection area / AOI area)
            coverage_ratio = intersection_area.divide(aoi_area)

            # Set the coverage ratio as a property of the image
            return image.set("coverage_ratio", coverage_ratio)

        # -------------------------------
        # Step 6: Apply Coverage Ratio Calculation
        # -------------------------------

        # Map the coverage ratio function over the Sentinel-2 collection
        sentinel2_with_ratio = sentinel2.map(calculate_coverage_ratio)

        # -------------------------------
        # Step 7: Filter Based on Coverage Ratio
        # -------------------------------

        # Define a filter to keep images with coverage_ratio >=
        # coverage_threshold
        coverage_filter = ee.Filter.gte("coverage_ratio", coverage_threshold)

        # Apply the filter to get the final collection
        covering_colection = sentinel2_with_ratio.filter(coverage_filter)

        # Get the number of images before filtering
        initial_count = sentinel2.size().getInfo()

        # Get the number of images after coverage filtering
        filtered_count = covering_colection.size().getInfo()

        print(f"Number of images before coverage filtering: {initial_count}")
        print(
            f"Number of images with >= {coverage_threshold*100}% AOI coverage: {filtered_count}"
        )

        if covering_colection.size().getInfo() == 0:
            return None, "No images found for the selected criteria. Please select a larger date range or less strick filtering and try again."

        return covering_colection, None

    def filter_within_AOI(self, sentinel2, aoi, valid_pixel_threshold, scl_classes_behavior):
        """Filters the image collection based on the percentage of valid pixels
        within the AOI."""
        """Filtra a coleção de imagens com base na porcentagem de pixels
        válidos dentro da AOI."""

        def mask_cloud_and_shadows(image):
            scl = image.select("SCL")
            # Start with an all-inclusive mask
            mask = ee.Image.constant(1)
            # Apply exclusions
            for class_value, include in scl_classes_behavior.items():
                if include:
                    mask = mask.And(scl.neq(class_value))

            masked_image = image.updateMask(mask)

            # Calculate the percentage of valid pixels
            total_pixels = (
                image.select(0)
                .reduceRegion(reducer=ee.Reducer.count(), geometry=aoi, scale=10)
                .get("B1")
            )

            valid_pixels = (
                masked_image.select(0)
                .reduceRegion(reducer=ee.Reducer.count(), geometry=aoi, scale=10)
                .get("B1")
            )

            percentage_valid = (
                ee.Number(valid_pixels).divide(total_pixels).multiply(100)
            )

            # Add the percentage of valid pixels as a property
            return masked_image.set("percentage_valid_pixels", percentage_valid)

            # Apply the cloud and shadow mask function

        # Apply the cloud and shadow mask function to the image collection
        sentinel2_masked = sentinel2.map(mask_cloud_and_shadows)

        # Filter the collection based on the valid pixel threshold
        filtered_collection = sentinel2_masked.filter(
            ee.Filter.gte("percentage_valid_pixels", valid_pixel_threshold)
        )

        # Get the number of images in the filtered collection
        filtered_count = filtered_collection.size().getInfo()

        masked_timestamps = filtered_collection.aggregate_array("system:time_start").getInfo()

        if filtered_collection.size().getInfo() == 0:
            return None, "No images found for the selected criteria. Please select a larger date range or less strick filtering and try again."

        return sentinel2.filter(
            ee.Filter.inList("system:time_start", ee.List(masked_timestamps))
        ), None

    def SCL_filter(self, sentinel2, aoi, scl_classes_behavior):
        """Applies a Scene Classification Layer (SCL) filter to the image
        collection."""
        """Aplica um filtro de Camada de Classificação de Cena (SCL) à coleção
        de imagens."""

        def mask_cloud_and_shadows(image):
            scl = image.select("SCL")
            # Start with an all-inclusive mask
            mask = ee.Image.constant(1)
            # Apply exclusions
            for class_value, include in scl_classes_behavior.items():
                if include:
                    mask = mask.And(scl.neq(class_value))

            return image.updateMask(mask)

            # Apply the cloud and shadow mask function to the image collection

        return sentinel2.map(mask_cloud_and_shadows)

    def composite(self, sentinel2_selected_dates, aoi, vegetation_index, metrica, inicio):
        """Composição de índices vegetativos"""

        # Função para calcular o índice vegetal desejado e preservar a data
        def calculate_index(image):
            if vegetation_index == "NDVI":
                return (
                    image.normalizedDifference(["B8", "B4"])
                    .rename("NDVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif vegetation_index == "EVI":
                return (
                    image.expression(
                        "2.5 * ((NIR/10000 - RED/10000) / (NIR/10000 + 6*RED/10000 - 7.5*BLUE/10000 + 1))",
                        {
                            "NIR": image.select("B8"),
                            "RED": image.select("B4"),
                            "BLUE": image.select("B2"),
                        },
                    )
                    .rename("EVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif vegetation_index == "SAVI":
                return (
                    image.expression(
                        "(1 + L) * ((NIR/10000 - RED/10000) / (NIR/10000 + RED/10000 + L))",
                        {"NIR": image.select("B8"), "RED": image.select("B4"), "L": 0.5},
                    )
                    .rename("SAVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif vegetation_index == "GNDVI":
                return (
                    image.normalizedDifference(["B8", "B3"])
                    .rename("GNDVI")
                    .copyProperties(image, ["system:time_start"])
                )
            else:
                raise ValueError(f"Invalid indice_vegetacao: {vegetation_index}")

        # Aplica o cálculo do índice à coleção filtrada
        index_collection = sentinel2_selected_dates.map(calculate_index)

        # Seleção da métrica de agregação
        if metrica in ["Mean", "Média"]:
            final_image = index_collection.mean()
        elif metrica in ["Max", "Máximo"]:
            final_image = index_collection.max()
        elif metrica in ["Min", "Mínimo"]:
            final_image = index_collection.min()
        elif metrica in ["Median", "Mediana"]:
            final_image = index_collection.median()
        elif metrica in ["Amplitude"]:
            final_image = index_collection.max().subtract(index_collection.min())
        elif metrica in ["Standard Deviation", "Desvio Padrão"]:
            final_image = index_collection.reduce(ee.Reducer.stdDev())
        elif metrica in ["Sum", "Soma"]:
            final_image = index_collection.sum()
        elif metrica in ["Area Under Curve (AUC)"]:
            # --- Cálculo da AUC por pixel via método de array ---
            count = index_collection.size().getInfo()
            if count < 2:
                raise ValueError("Número insuficiente de imagens para calcular a AUC.")

            # Cria uma "pilha" dos índices (cada imagem vira uma banda)
            indexStack = index_collection.toBands()
            # Define uma máscara válida (mínimo valor da máscara de todas as bandas)
            validMask = indexStack.mask().reduce(ee.Reducer.min())

            # Obtém os nomes das bandas (cada banda corresponde a uma data)
            bands = indexStack.bandNames()

            # Define a data inicial; certifique-se de que inicio esteja no formato "YYYY-MM-DD"
            start_date = ee.Date(inicio)
            # Cria uma lista de timestamps em dias relativos à data inicial
            timestamps = index_collection.aggregate_array("system:time_start").map(
                lambda date: ee.Number(ee.Date(date).difference(start_date, "day"))
            )

            # Alinha os timestamps com o número de bandas
            alignedTimestamps = ee.List(timestamps.slice(0, bands.size()))
            # Cria uma imagem com constantes baseadas nos timestamps e renomeia para os nomes das bandas
            timeImage = ee.Image.constant(alignedTimestamps).rename(bands).toArray()

            # Converte a pilha de índices para um array
            ndviArray = indexStack.toArray()

            # Calcula as diferenças entre timestamps consecutivos
            diffs = timeImage.arraySlice(0, 1).subtract(timeImage.arraySlice(0, 0, -1))
            # Soma os valores de NDVI de imagens consecutivas
            sums = ndviArray.arraySlice(0, 1).add(ndviArray.arraySlice(0, 0, -1))
            # Aplica a regra do trapézio: (diferença * soma) / 2 e reduz o array pela soma dos intervalos
            auc = diffs.multiply(sums).divide(2).arrayReduce(ee.Reducer.sum(), [0])
            # Extrai o resultado final, aplica a máscara e define como imagem final
            final_image = ee.Image(auc.arrayGet([0])).updateMask(validMask)
        else:
            raise ValueError(f"Invalid metric: {metrica}")

        # Recorta a imagem final à área de interesse (AOI)
        final_image = final_image.clip(aoi.geometry())

        return final_image

    def download_ee_image(self, final_image, aoi, scale=10, format="GeoTIFF"):
        """Gera a URL de download para a imagem final (GeoTIFF, escala de 10)"""
        url = final_image.getDownloadUrl(
            {
                "scale": scale,
                "region": aoi.geometry().bounds().getInfo(),
                "format": format,
            }
        )
        return url
