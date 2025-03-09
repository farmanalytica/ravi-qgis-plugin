    def calculate_vegetation_index(self, image, index_name):
        """
        Calculates the specified vegetation index for the given image using
        dictionary-based expressions.

        Args:
            image (ee.Image): The input Earth Engine image.
            index_name (str): The name of the vegetation index to calculate
                (e.g., "NDVI", "EVI").

        Returns:
            ee.Image: The image containing the calculated vegetation index, renamed
                to "index".

        Raises:
            ValueError: If an unsupported vegetation index is specified.
        """
        index_expressions = {
            "NDVI": 'image.normalizedDifference(["B8", "B4"]).rename("index")',
            "EVI": (
                "image.expression("
                "2.5 * ((NIR / 10000 - RED / 10000) / (NIR / 10000 + 6 * RED / 10000 - 7.5 * BLUE / 10000 + 1))",
                "{"
                '"NIR": image.select("B8"),'
                '"RED": image.select("B4"),'
                '"BLUE": image.select("B2"),'
                "})"
                '.rename("index")'
            ),
            "SAVI": (
                "image.expression("
                "(1 + L) * ((NIR / 10000) - (RED / 10000)) / ((NIR / 10000) + (RED / 10000) + L)",
                '{"NIR": image.select("B8"), "RED": image.select("B4"), "L": 0.5}',
                ')'
                '.rename("index")'
            ),
            "GNDVI": 'image.normalizedDifference(["B8", "B3"]).rename("index")',
            "MSAVI": (
                "image.expression("
                '((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2',
                '{"NIR": image.select("B8"), "RED": image.select("B4")}',
                ')'
                '.rename("index")'
            ),
            "SFDVI": (
                "image.expression("
                '(NIR - SWIR) / (NIR + SWIR)',
                '{"NIR": image.select("B8"), "SWIR": image.select("B11")}',
                ')'
                '.rename("index")'
            ),
            "CIgreen": (
                "image.expression("
                '(NIR / GREEN) - 1',
                '{"NIR": image.select("B8"), "GREEN": image.select("B3")}',
                ')'
                '.rename("index")'
            ),
            "NDRE": 'image.normalizedDifference(["B8", "B5"]).rename("index")',
        }

        if index_name in index_expressions:
            expression = index_expressions[index_name]
            # Execute the expression using eval()
            index_image = eval(expression)
            return index_image
        else:
            raise ValueError(f"Unsupported vegetation index: {index_name}")
        

    def composite(self, temporary):
        """Calculates a composite of the selected vegetation index over the selected dates."""
        print("Composição de índices vegetativos")
        
        # Get the selected vegetation index and metric for aggregation
        indice_vegetacao = self.indice_composicao.currentText()
        metrica = self.metrica.currentText()

        # Function to calculate the desired vegetation index and preserve the date
        def calculate_index(image):
            # Calculate the vegetation index using the existing method
            index_image = self.calculate_vegetation_index(image, indice_vegetacao)
            # Preserve the original image's time property
            return index_image.copyProperties(image, ["system:time_start"])

        # Apply the index calculation to the filtered collection
        index_collection = self.sentinel2_selected_dates.map(calculate_index)

        # Aggregate the index collection based on the selected metric
        final_image = self.aggregate_index_collection(index_collection, metrica)

        # Optional: Further processing of final_image can be added here
        # For example, you might want to download the final image or add it to the QGIS project

        # Prepare download URL and output filename for the final image
        url = final_image.getDownloadUrl(
            {
                "scale": 10,
                "region": self.aoi.geometry().bounds().getInfo(),
                "format": "GeoTIFF",
            }
        )

        base_output_file = f"{metrica}_{indice_vegetacao}.tiff"
        output_file = self.get_unique_filename(base_output_file, True)
        response = requests.get(url)
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"{indice_vegetacao} image downloaded as {output_file}")

        # Recorta a imagem raster usando a camada vetorial (normalmente a AOI)
        layer_name = f"{indice_vegetacao} {metrica}"
        base_output_file = f"{metrica}_{indice_vegetacao}_clipped.tiff"
        output_file_clipped = self.get_unique_filename(base_output_file, temporary)
        self.clip_raster_by_vector(
            output_file, self.selected_aio_layer_path, output_file_clipped, layer_name
        )

        # Carrega a camada raster com estilo colorido no QGIS
        map_tools.load_raster_layer_colorful(
            output_file_clipped, layer_name, indice_vegetacao, self.metrica.currentText()
        )


    def clip_raster_by_vector(
        self, raster_path, shapefile_path, output_path, layer_name
    ):
        print(
            f"Clipping raster {raster_path} by vector {shapefile_path} to {output_path}"
        )
        # Load layers
        shapefile_layer = QgsVectorLayer(shapefile_path, "Clip Layer", "ogr")
        raster_layer = QgsRasterLayer(raster_path, "Raster Layer")

        # Check if layers loaded successfully
        if not shapefile_layer.isValid():
            print("Failed to load shapefile.")
        if not raster_layer.isValid():
            print("Failed to load raster.")

        # Clip raster using the shapefile
        result = processing.run(
            "gdal:cliprasterbymasklayer",
            {
                "INPUT": raster_layer,
                "MASK": shapefile_layer,
                "NODATA": -9999,  # Change to appropriate NoData value if needed
                "CROP_TO_CUTLINE": True,
                "KEEP_RESOLUTION": True,
                "OUTPUT": output_path,
            },
            feedback=QgsProcessingFeedback(),
        )

        print(f"Clipping result: {result}")