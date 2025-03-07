    def load_index(self, temporary=False):
        """
        Calculates a vegetation index, downloads the GeoTIFF, and adds it to
        the QGIS project as a styled raster layer, ensuring unique names for
        each layer.
        """
        """
        Calcula um índice de vegetação, baixa o GeoTIFF e o adiciona ao projeto
        QGIS como uma camada raster estilizada, garantindo nomes exclusivos
        para cada camada.
        """
        try:
            print("First index clicked")
            QApplication.setOverrideCursor(
                Qt.WaitCursor
            )  # Set wait cursor for user feedback

            # Retrieve vegetation index and date inputs / Recupera o índice de
            # vegetação e as entradas de data
            vegetation_index = self.imagem_unica_indice.currentText()
            date = [self.dataunica.currentText()]

            first_image = self.sentinel2.filter(
                ee.Filter.inList("date", date)
            ).first()

            # Clip image to AOI / Recorta a imagem para a AOI
            first_image = first_image.clip(self.aoi)

            # Calculate the selected vegetation index / Calcula o índice de
            # vegetação selecionado
            if vegetation_index == "NDVI":
                index_image = first_image.normalizedDifference(["B8", "B4"]).rename(
                    "NDVI"
                )
            elif vegetation_index == "GNDVI":
                index_image = first_image.normalizedDifference(["B8", "B3"]).rename(
                    "GNDVI"
                )
            elif vegetation_index == "MSAVI":
                index_image = first_image.expression(
                    "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
                    {
                        "NIR": first_image.select("B8"),
                        "RED": first_image.select("B4"),
                    },
                ).rename("MSAVI")
            elif vegetation_index == "EVI":
                index_image = first_image.expression(
                    "2.5 * ((NIR / 10000 - RED / 10000) / (NIR / 10000 + 6 * RED / 10000 - 7.5 * BLUE / 10000 + 1))",
                    {
                        "NIR": first_image.select("B8"),
                        "RED": first_image.select("B4"),
                        "BLUE": first_image.select("B2"),
                    },
                ).rename("EVI")
            elif vegetation_index == "SAVI":
                L = 0.5  # Soil brightness correction factor
                index_image = first_image.expression(
                    "(1 + L) * ((NIR / 10000) - (RED / 10000)) / ((NIR / 10000) + (RED / 10000) + L)",
                    {
                        "NIR": first_image.select("B8"),
                        "RED": first_image.select("B4"),
                        "L": L,
                    },
                ).rename("SAVI")
            elif vegetation_index == "SFDVI":
                index_image = first_image.expression(
                    "(NIR - SWIR) / (NIR + SWIR)",
                    {
                        "NIR": first_image.select("B8"),
                        "SWIR": first_image.select("B11"),
                    },
                ).rename("SFDVI")
            elif vegetation_index == "CIgreen":
                index_image = first_image.expression(
                    "(NIR / GREEN) - 1",
                    {
                        "NIR": first_image.select("B8"),
                        "GREEN": first_image.select("B3"),
                    },
                ).rename("CIgreen")
            elif vegetation_index == "NDRE":
                index_image = first_image.normalizedDifference(["B8", "B5"]).rename("NDRE")
            else:
                raise ValueError(f"Invalid vegetation index: {vegetation_index}")

            

            # Prepare download URL and output filename / Prepara o URL de
            # download e o nome do arquivo de saída
            url = index_image.getDownloadUrl(
                {
                    "scale": 10,
                    "region": self.aoi.geometry().bounds().getInfo(),
                    "format": "GeoTIFF",
                }
            )
            base_output_file = f"{vegetation_index}_{date[0]}.tiff"
            output_file = self.get_unique_filename(base_output_file, temporary)

            # Download the image / Baixa a imagem
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                print(f"{vegetation_index} image downloaded as {output_file}")
            else:
                print(f"Failed to download image. HTTP Status: {response.status_code}")
                return

            # Prepare unique layer name / Prepara o nome exclusivo da camada
            layer_name = f"{vegetation_index} {date[0]}"
            base_name = layer_name
            i = 1
            while QgsProject.instance().mapLayersByName(layer_name):
                layer_name = f"{base_name}_{i}"
                i += 1
            print(f"Layer name adjusted to '{layer_name}' to ensure uniqueness.")

            # Add raster layer with styling / Adiciona a camada raster com
            # estilo
            map_tools.load_raster_layer_colorful(
                output_file, layer_name, vegetation_index, None
            )

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            QApplication.restoreOverrideCursor()  # Restore the default cursor

    def composite(self, temporary):
        print("Composição de índices vegetativos")
        indice_vegetacao = self.indice_composicao.currentText()
        metrica = self.metrica.currentText()

        # Função para calcular o índice vegetal desejado e preservar a data
        def calculate_index(image):
            if indice_vegetacao == "NDVI":
                return (
                    image.normalizedDifference(["B8", "B4"])
                    .rename("NDVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif indice_vegetacao == "EVI":
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
            elif indice_vegetacao == "SAVI":
                return (
                    image.expression(
                        "(1 + L) * ((NIR/10000 - RED/10000) / (NIR/10000 + RED/10000 + L))",
                        {"NIR": image.select("B8"), "RED": image.select("B4"), "L": 0.5},
                    )
                    .rename("SAVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif indice_vegetacao == "MSAVI":
                index_image = image.expression(
                    "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
                    {
                        "NIR": image.select("B8"),
                        "RED": image.select("B4"),
                    },
                ).rename("MSAVI")
            elif indice_vegetacao == "GNDVI":
                return (
                    image.normalizedDifference(["B8", "B3"])
                    .rename("GNDVI")
                    .copyProperties(image, ["system:time_start"])
                )
            elif indice_vegetacao == "SFDVI":
                index_image = image.expression(
                    "(NIR - SWIR) / (NIR + SWIR)",
                    {
                        "NIR": image.select("B8"),
                        "SWIR": image.select("B11"),
                    },
                ).rename("SFDVI")
            elif indice_vegetacao == "CIgreen":
                index_image = image.expression(
                    "(NIR / GREEN) - 1",
                    {
                        "NIR": image.select("B8"),
                        "GREEN": image.select("B3"),
                    },
                ).rename("CIgreen")
            elif indice_vegetacao == "NDRE":
                index_image = image.normalizedDifference(["B8", "B5"]).rename("NDRE")
            else:
                raise ValueError(f"Invalid indice_vegetacao: {indice_vegetacao}")
            

        # Aplica o cálculo do índice à coleção filtrada
        index_collection = self.sentinel2_selected_dates.map(calculate_index)

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

            # Define a data inicial; certifique-se de que self.inicio esteja no formato "YYYY-MM-DD"
            start_date = ee.Date(self.inicio)
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
        final_image = final_image.clip(self.aoi.geometry())

        # Gera a URL de download para a imagem final (GeoTIFF, escala de 10)
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

    def calculate_timeseries(self):
        """Calculates the time series of the selected vegetation index for the
        AOI."""
        """Calcula a série temporal do índice de vegetação selecionado para a
        AOI."""
        vegetation_index = self.series_indice.currentText()

        # Buffer the AOI geometry inward by 10 meters (adjust distance as
        # needed)
        buffer_distance = self.horizontalSlider_buffer.value()
        if buffer_distance != 0:
            print(f"Buffer distance: {buffer_distance} meters")
            aoi = self.aoi.map(lambda feature: feature.buffer(buffer_distance))
        else:
            print("No buffer applied")
            aoi = self.aoi

        # Define the vegetation index calculation in a function
        def calculate_index(image):
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
            elif vegetation_index == "MSAVI":
                index_image = image.expression(
                    "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
                    {
                        "NIR": image.select("B8"),
                        "RED": image.select("B4"),
                    },
                ).rename("index")
            elif vegetation_index == "SFDVI":
                index_image = image.expression(
                    "(NIR - SWIR) / (NIR + SWIR)",
                    {
                        "NIR": image.select("B8"),
                        "SWIR": image.select("B11"),
                    },
                ).rename("index")
            elif vegetation_index == "CIgreen":
                index_image = image.expression(
                    "(NIR / GREEN) - 1",
                    {
                        "NIR": image.select("B8"),
                        "GREEN": image.select("B3"),
                    },
                ).rename("index")
            elif vegetation_index == "NDRE":
                index_image = image.normalizedDifference(["B8", "B5"]).rename("index")
            else:
                raise ValueError(f"Unsupported vegetation index: {vegetation_index}")

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = self.sentinel2.map(calculate_index)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()
        image_ids = result.aggregate_array("system:index").getInfo()

        # Combine the dates, mean indices, and image IDs into a DataFrame
        df = pd.DataFrame(
            {"date": dates, "AOI_average": mean_indices, "image_id": image_ids}
        )

        # Optional: Smoothing or further processing
        self.df = df.copy()
        self.df_aux = df.copy()
        self.load_dates()
        self.plot_timeseries()

    def feature_calculate_timeseries(self, name):
        """Calculates the time series of the selected vegetation index for a
        specific feature."""
        """Calcula a série temporal do índice de vegetação selecionado para uma
        feição específica."""
        vegetation_index = self.series_indice.currentText()

        # Buffer the AOI geometry inward by 10 meters (adjust distance as
        # needed)
        buffer_distance = self.horizontalSlider_buffer.value()
        if buffer_distance != 0:
            print(f"Buffer distance: {buffer_distance} meters")
            aoi = self.aoi_feature.map(lambda feature: feature.buffer(buffer_distance))
        else:
            print("No buffer applied")
            aoi = self.aoi_feature

        # Define the vegetation index calculation in a function
        def calculate_index(image):
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
            elif vegetation_index == "MSAVI":
                index_image = image.expression(
                    "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
                    {
                        "NIR": image.select("B8"),
                        "RED": image.select("B4"),
                    },
                ).rename("index")
            elif vegetation_index == "SFDVI":
                index_image = image.expression(
                    "(NIR - SWIR) / (NIR + SWIR)",
                    {
                        "NIR": image.select("B8"),
                        "SWIR": image.select("B11"),
                    },
                ).rename("index")
            elif vegetation_index == "CIgreen":
                index_image = image.expression(
                    "(NIR / GREEN) - 1",
                    {
                        "NIR": image.select("B8"),
                        "GREEN": image.select("B3"),
                    },
                ).rename("index")
            elif vegetation_index == "NDRE":
                index_image = image.normalizedDifference(["B8", "B5"]).rename("index")
            else:
                raise ValueError(f"Unsupported vegetation index: {vegetation_index}")

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = self.sentinel2_selected_dates.map(calculate_index)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()

        # Combine the dates, mean indices
        print(f"Creating DataFrame for {name}")
        return pd.DataFrame({"date": dates, name: mean_indices})

    def point_calculate_timeseries(self, aoi, name):
        """Calculates the time series of the selected vegetation index for a
        specific point."""
        """Calcula a série temporal do índice de vegetação selecionado para um
        ponto específico."""
        vegetation_index = self.series_indice.currentText()

        # Define the vegetation index calculation in a function
        def calculate_index(image):
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
            elif vegetation_index == "MSAVI":
                index_image = image.expression(
                    "((2 * NIR + 1) - sqrt((2 * NIR + 1) ** 2 - 8 * (NIR - RED))) / 2",
                    {
                        "NIR": image.select("B8"),
                        "RED": image.select("B4"),
                    },
                ).rename("index")
            elif vegetation_index == "SFDVI":
                index_image = image.expression(
                    "(NIR - SWIR) / (NIR + SWIR)",
                    {
                        "NIR": image.select("B8"),
                        "SWIR": image.select("B11"),
                    },
                ).rename("index")
            elif vegetation_index == "CIgreen":
                index_image = image.expression(
                    "(NIR / GREEN) - 1",
                    {
                        "NIR": image.select("B8"),
                        "GREEN": image.select("B3"),
                    },
                ).rename("index")
            elif vegetation_index == "NDRE":
                index_image = image.normalizedDifference(["B8", "B5"]).rename("index")
            else:
                raise ValueError(f"Unsupported vegetation index: {vegetation_index}")

            # Calculate mean value for the index over AOI
            mean_index = (
                index_image.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=aoi, scale=10, bestEffort=True
                )
                .get("index")
            )

            return image.set({"mean_index": mean_index})

        # Map the calculation function over the collection and get results
        result = self.sentinel2_selected_dates.map(calculate_index)
        result = result.filter(ee.Filter.notNull(["mean_index"]))

        # Retrieve dates and mean index values separately using aggregate_array
        dates = result.aggregate_array("date").getInfo()
        mean_indices = result.aggregate_array("mean_index").getInfo()

        # Combine the dates, mean indices
        print(f"Creating DataFrame for {name}")
        return pd.DataFrame({"date": dates, name: mean_indices})