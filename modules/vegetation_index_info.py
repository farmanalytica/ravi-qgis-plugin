print("Loading vegetation_index_info.py...")

# Information about vegetation indices
vegetation_indices = {
    "NDVI": """
        <h3>Normalized Difference Vegetation Index (NDVI)</h3>
        <p>
            The Normalized Difference Vegetation Index (NDVI) is a widely used and well-established 
            indicator of vegetation health and vigor. It exploits the contrasting spectral 
            reflectance properties of plant pigments, particularly chlorophyll. 
            Healthy vegetation strongly absorbs visible red light for photosynthesis while 
            reflecting a significant portion of near-infrared (NIR) radiation. 
            Conversely, non-vegetated areas like soil and water tend to reflect both red and 
            NIR light more equally. 
        </p>
        <p>
            The NDVI formula is calculated as follows:
        </p>
        <pre>
NDVI = (NIR - RED) / (NIR + RED)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
            </ul>
            By calculating the difference between NIR and red reflectance and normalizing it 
            by their sum, NDVI effectively enhances the vegetation signal while minimizing 
            the influence of factors like variations in illumination and atmospheric conditions. 
            NDVI values typically range from -1 to 1. 
            Higher values (closer to 1) generally indicate denser, healthier vegetation with 
            higher leaf area and chlorophyll content. 
            Lower values (closer to -1) often correspond to bare soil, water, or senescent 
            (dying) vegetation.
        </p>
    """,
    "GNDVI": """
        <h3>Green Normalized Difference Vegetation Index (GNDVI)</h3>
        <p>
            The Green Normalized Difference Vegetation Index (GNDVI) is a modification of NDVI 
            that utilizes the green band of the electromagnetic spectrum instead of the red band. 
            Chlorophyll, the primary pigment involved in photosynthesis, strongly absorbs 
            blue and red light while reflecting green light. 
            Therefore, GNDVI is particularly sensitive to variations in chlorophyll content 
            within plant canopies.
        </p>
        <p>
            The GNDVI formula is calculated as:
        </p>
        <pre>
GNDVI = (NIR - GREEN) / (NIR + GREEN)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>GREEN</b>: Reflectance in the green band</li>
            </ul>
            This sensitivity makes GNDVI a valuable tool for:
            <ul>
                <li>Monitoring plant stress and nutrient deficiencies</li>
                <li>Detecting early signs of disease or pest infestations</li>
                <li>Assessing crop vigor and yield potential</li>
                <li>Studying the impact of environmental factors on plant growth</li>
            </ul>
        </p>
    """,
    "EVI": """
        <h3>Enhanced Vegetation Index (EVI)</h3>
        <p>
            The Enhanced Vegetation Index (EVI) was developed to address some of the limitations 
            of NDVI, particularly in areas of high biomass or atmospheric interference. 
            EVI incorporates a blue band in its calculation, which helps to minimize the 
            influence of atmospheric aerosols and soil background noise. 
            Additionally, EVI uses a canopy background adjustment term to improve sensitivity 
            in areas of high biomass and to better discriminate vegetation from non-vegetated 
            surfaces.
        </p>
        <p>
            The EVI formula is calculated as:
        </p>
        <pre>
EVI = 2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>BLUE</b>: Reflectance in the blue band</li>
            </ul>
            EVI has proven to be highly effective in:
            <ul>
                <li>Monitoring vegetation dynamics in diverse ecosystems</li>
                <li>Estimating biomass and productivity</li>
                <li>Assessing the impact of climate change on vegetation</li>
                <li>Mapping vegetation cover and land use/land cover change</li>
            </ul>
        </p>
    """,
    "EVI2": """
        <h3>Enhanced Vegetation Index 2 (EVI2)</h3>
        <p>
            The Enhanced Vegetation Index 2 (EVI2) is a simplified version of the Enhanced Vegetation Index (EVI) 
            that does not require the blue band. This makes it particularly useful for sensors that lack a blue band 
            or in cases where the blue band data is unreliable.
        </p>
        <p>
            The EVI2 formula is calculated as:
        </p>
        <pre>
    EVI2 = 2.5 * ((NIR - RED) / (NIR + RED + 1))
        </pre>
        <p>
            where:
            <ul>
            <li><b>NIR</b>: Reflectance in the near-infrared band</li>
            <li><b>RED</b>: Reflectance in the red band</li>
            </ul>
        </p>
        <p>
            EVI2 retains many of the advantages of EVI, such as improved sensitivity in areas of high biomass, 
            while being computationally simpler and more broadly applicable.
        </p>
        """,
    "SAVI": """
        <h3>Soil-Adjusted Vegetation Index (SAVI)</h3>
        <p>
            The Soil-Adjusted Vegetation Index (SAVI) is specifically designed to minimize 
            the influence of soil background reflectance, particularly in areas with sparse 
            vegetation cover. 
            In such areas, soil reflectance can significantly impact the accuracy of 
            vegetation indices like NDVI.
        </p>
        <p>
            SAVI incorporates a soil brightness correction factor (L) into its calculation. 
            This factor adjusts the sensitivity of the index to soil background, 
            allowing for more accurate assessment of vegetation in areas with varying 
            soil conditions. SAVI is particularly useful in:
            <ul>
                <li>Arid and semi-arid regions</li>
                <li>Agricultural areas with low plant cover</li>
                <li>Disturbed or degraded ecosystems</li>
            </ul>
        </p>
        <p>
            The SAVI formula is calculated as:
        </p>
        <pre>
SAVI = (1 + L) * ((NIR - RED) / (NIR + RED + L))
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>L</b>: Soil brightness correction factor (typically set to 0.5)</li>
            </ul>
        </p>
        <p><b>Note:</b> For this plugin, the soil brightness correction factor (L) is set to 0.5.</p>
    """,
    "MSAVI": """
        <h3>Modified Soil-Adjusted Vegetation Index (MSAVI)</h3>
        <p>
            The Modified Soil-Adjusted Vegetation Index (MSAVI) is an enhancement of the SAVI 
            designed to further minimize soil background effects on vegetation monitoring. 
            Unlike SAVI, which uses a constant soil adjustment factor (L), MSAVI dynamically 
            adjusts this factor based on vegetation density, making it more responsive to 
            variations in vegetative cover.
        </p>
        <p>
            MSAVI is particularly valuable in areas with mixed vegetation densities and varying 
            soil backgrounds, as it reduces the need for prior knowledge of vegetation cover. 
            This makes it ideal for:
            <ul>
                <li>Agricultural monitoring across different growth stages</li>
                <li>Ecological studies in heterogeneous landscapes</li>
                <li>Land degradation assessment</li>
                <li>Monitoring vegetation recovery after disturbances</li>
            </ul>
        </p>
        <p>
            The MSAVI formula is calculated as:
        </p>
        <pre>
MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)² - 8 * (NIR - RED))) / 2
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
            </ul>
        </p>
        <p>
            The self-adjusting nature of MSAVI provides more consistent measurements across 
            diverse landscapes and vegetation conditions compared to NDVI and SAVI.
        </p>
    """,
    "SFDVI": """
        <h3>Structurally Focused Difference Vegetation Index (SFDVI)</h3>
        <p>
            The Spectral Feature Depth Vegetation Index (SFDVI) integrates the Red Edge band 
            with the red band to investigate vegetation behavior by means of the spectral 
            feature depth.  SFDVI shows more gradations in dense vegetation than NDVI and RENDVI.
        </p>
        <p>
            SFDVI is effective for:
            <ul>
                <li>Analyzing vegetation using spectral feature depth.</li>
                <li>Showing gradations in dense vegetation.</li>
            </ul>
        </p>
        <p>
            The SFDVI formula is calculated as:
        </p>
        <pre>
SFDVI = ((NIR + GREEN)/2 - (RED + REDEDGE)/2)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>GREEN</b>: Reflectance in the green band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>REDEDGE</b>: Reflectance in the red edge band</li>
            </ul>
        </p>
    """,
    "CIgreen": """
        <h3>Chlorophyll Index Green (CIgreen)</h3>
        <p>
            The Chlorophyll Index Green (CIgreen) is specifically designed to estimate 
            chlorophyll content in plant leaves and canopies. Unlike normalized difference 
            indices, CIgreen uses a ratio-based approach that has shown strong correlation 
            with actual chlorophyll concentrations in various vegetation types.
        </p>
        <p>
            This index is particularly sensitive to subtle changes in chlorophyll levels, 
            making it valuable for:
            <ul>
                <li>Early detection of plant stress</li>
                <li>Monitoring crop nitrogen status</li>
                <li>Assessing photosynthetic capacity</li>
                <li>Tracking seasonal changes in vegetation health</li>
            </ul>
        </p>
        <p>
            The CIgreen formula is calculated as:
        </p>
        <pre>
CIgreen = (NIR / GREEN) - 1
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>GREEN</b>: Reflectance in the green band</li>
            </ul>
        </p>
        <p>
            Higher CIgreen values generally indicate greater chlorophyll content and 
            healthier vegetation. The index's simple formulation makes it computationally 
            efficient while still providing valuable insights into plant physiological status.
        </p>
    """,
    "NDRE": """
        <h3>Normalized Difference Red Edge (NDRE)</h3>
        <p>
            The Normalized Difference Red Edge (NDRE) is an advanced vegetation index that 
            utilizes the red edge portion of the electromagnetic spectrum. The red edge 
            represents the rapid change in reflectance between the red and near-infrared 
            regions (approximately 680-730 nm) and is highly sensitive to chlorophyll 
            content and vegetation health.
        </p>
        <p>
            NDRE is particularly valuable in:
            <ul>
                <li>Detecting early signs of crop stress before visible symptoms appear</li>
                <li>Monitoring nitrogen status in crops with high precision</li>
                <li>Assessing vegetation health in dense canopies where NDVI may saturate</li>
                <li>Distinguishing between subtle variations in vegetation condition</li>
            </ul>
        </p>
        <p>
            The NDRE formula is calculated as:
        </p>
        <pre>
NDRE = (NIR - REDEDGE) / (NIR + REDEDGE)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>REDEDGE</b>: Reflectance in the red edge band (typically 720-740 nm)</li>
            </ul>
        </p>
        <p>
            NDRE values typically range from -1 to 1, with higher values indicating healthier 
            vegetation. NDRE offers significant advantages over NDVI in dense vegetation where 
            NDVI tends to saturate, making it especially useful for precision agriculture and 
            advanced vegetation monitoring applications.
        </p>
    """,
    "ARVI": """
        <h3>Atmospherically Resistant Vegetation Index (ARVI)</h3>
        <p>
            The Atmospherically Resistant Vegetation Index (ARVI) is designed to be less sensitive 
            to atmospheric effects (such as aerosols) compared to NDVI. It incorporates a correction 
            factor using the blue band to compensate for atmospheric scattering.
        </p>
        <p>
            The ARVI formula is calculated as:
        </p>
        <pre>
ARVI = (NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>BLUE</b>: Reflectance in the blue band</li>
            </ul>
        </p>
        <p>
            ARVI is useful in regions with significant atmospheric aerosol presence, providing a 
            more accurate assessment of vegetation cover.
        </p>
    """,
    "NDMI": """
        <h3>Normalized Difference Moisture Index (NDMI)</h3>
        <p>
            The Normalized Difference Moisture Index (NDMI) is used to monitor vegetation moisture content. 
            It is sensitive to changes in the water content of plant canopies.
        </p>
        <p>
            The NDMI formula is calculated as:
        </p>
        <pre>
NDMI = (NIR - SWIR) / (NIR + SWIR)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>SWIR</b>: Reflectance in the shortwave infrared band</li>
            </ul>
        </p>
        <p>
            NDMI is valuable in drought monitoring, irrigation management, and assessing vegetation stress 
            related to water availability.
        </p>
    """,
    "NBR": """
        <h3>Normalized Burn Ratio (NBR)</h3>
        <p>
            The Normalized Burn Ratio (NBR) is designed to identify burned areas and assess burn severity. 
            It uses the difference between near-infrared and shortwave infrared reflectance.
        </p>
        <p>
            The NBR formula is calculated as:
        </p>
        <pre>
NBR = (NIR - SWIR) / (NIR + SWIR)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>SWIR</b>: Reflectance in the shortwave infrared band</li>
            </ul>
        </p>
        <p>
            NBR is used extensively in post-fire assessment to map burned areas and monitor vegetation recovery.
        </p>
    """,
    "SIPI": """
        <h3>Structure Insensitive Pigment Index (SIPI)</h3>
        <p>
            The Structure Insensitive Pigment Index (SIPI) is used to assess vegetation canopy stress.
        </p>
        <p>
            The SIPI formula is calculated as:
        </p>
        <pre>
SIPI = (NIR - BLUE) / (NIR - RED)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>BLUE</b>: Reflectance in the blue band</li>
            </ul>
        </p>
        <p>
            SIPI is useful for minimizing canopy structure effects.
        </p>
    """,
    "NDWI": """
        <h3>Normalized Difference Water Index (NDWI)</h3>
        <p>
            The Normalized Difference Water Index (NDWI) is used to monitor changes in water content in
            vegetation.
        </p>
        <p>
            The NDWI formula is calculated as:
        </p>
        <pre>
NDWI = (GREEN - NIR) / (GREEN + NIR)
        </pre>
        <p>
            where:
            <ul>
                <li><b>GREEN</b>: Reflectance in the green band</li>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
            </ul>
        </p>
        <p>
            NDWI is sensitive to changes in liquid water content of vegetation canopies.
        </p>
    """,
    "ReCI": """
        <h3>Red Edge Chlorophyll Index (ReCI)</h3>
        <p>
            The Red Edge Chlorophyll Index (ReCI) is designed to estimate chlorophyll content in
            vegetation using the red edge band.
        </p>
        <p>
            The ReCI formula is calculated as:
        </p>
        <pre>
ReCI = (NIR / REDEDGE) - 1
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>REDEDGE</b>: Reflectance in the red edge band</li>
            </ul>
        </p>
        <p>
            ReCI is particularly useful in precision agriculture for monitoring crop health and
            nitrogen status.
        </p>
    """,
    "MTCI": """
        <h3>MERIS Terrestrial Chlorophyll Index (MTCI)</h3>
        <p>
            The MERIS Terrestrial Chlorophyll Index (MTCI) is sensitive to chlorophyll content in
            vegetation.
        </p>
        <p>
            The MTCI formula is calculated as:
        </p>
        <pre>
MTCI = (NIR - REDEDGE) / (REDEDGE - RED)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>REDEDGE</b>: Reflectance in the red edge band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
            </ul>
        </p>
        <p>
            MTCI is useful for estimating chlorophyll content and monitoring vegetation health.
        </p>
    """,
    "MCARI": """
        <h3>Modified Chlorophyll Absorption Ratio Index (MCARI)</h3>
        <p>
            The Modified Chlorophyll Absorption Ratio Index (MCARI) is designed to be sensitive to
            chlorophyll concentration.
        </p>
        <p>
            The MCARI formula is calculated as:
        </p>
        <pre>
MCARI = ((REDEDGE - RED) - 0.2 * (REDEDGE - GREEN)) * (REDEDGE / RED)
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band (used as REDEDGE)</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>GREEN</b>: Reflectance in the green band</li>
            </ul>
        </p>
        <p>
            MCARI can be used to assess vegetation stress.
        </p>
    """,
    "VARI": """
        <h3>Visible Atmospherically Resistant Index (VARI)</h3>
        <p>
            The Visible Atmospherically Resistant Index (VARI) minimizes atmospheric effects and
            enhances the vegetation signal in the visible part of the spectrum.
        </p>
        <p>
            The VARI formula is calculated as:
        </p>
        <pre>
VARI = (GREEN - RED) / (GREEN + RED - BLUE)
        </pre>
        <p>
            where:
            <ul>
                <li><b>GREEN</b>: Reflectance in the green band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>BLUE</b>: Reflectance in the blue band</li>
            </ul>
        </p>
        <p>
            VARI is useful when atmospheric correction is challenging.
        </p>
    """,
    "TVI": """
        <h3>Triangular Vegetation Index (TVI)</h3>
        <p>
            The Triangular Vegetation Index (TVI) is a transformation of the NDVI index.
        </p>
        <p>
            The TVI formula is calculated as:
        </p>
        <pre>
TVI = 0.5 * (120 * (NIR - GREEN) - 200 * (RED - GREEN))
        </pre>
        <p>
            where:
            <ul>
                <li><b>NIR</b>: Reflectance in the near-infrared band</li>
                <li><b>RED</b>: Reflectance in the red band</li>
                <li><b>GREEN</b>: Reflectance in the green band</li>
            </ul>
        </p>
    """,
}

vegetation_indices_pt = {
    "NDVI": """
        <h3>Índice de Vegetação por Diferença Normalizada (NDVI)</h3>
        <p>
            O Índice de Vegetação por Diferença Normalizada (NDVI) é um indicador amplamente utilizado e bem estabelecido da saúde e vigor da vegetação. Ele explora as propriedades de reflectância espectral contrastantes dos pigmentos das plantas, particularmente a clorofila. A vegetação saudável absorve fortemente a luz vermelha visível para a fotossíntese enquanto reflete uma parte significativa da radiação do infravermelho próximo (NIR). Por outro lado, áreas não vegetadas, como solo e água, tendem a refletir a luz vermelha e NIR de forma mais equilibrada.
        </p>
        <p>
            A fórmula do NDVI é calculada da seguinte forma:
        </p>
        <pre>
NDVI = (NIR - RED) / (NIR + RED)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
            </ul>
            Ao calcular a diferença entre a reflectância do NIR e da luz vermelha e normalizando-a pela soma dos dois, o NDVI realça efetivamente o sinal da vegetação enquanto minimiza a influência de fatores como variações na iluminação e condições atmosféricas. Os valores do NDVI geralmente variam de -1 a 1. Valores mais altos (próximos de 1) indicam, em geral, vegetação mais densa e saudável, com maior área foliar e teor de clorofila. Valores mais baixos (próximos de -1) frequentemente correspondem a solo exposto, água ou vegetação senescente (em declínio).
        </p>
    """,
    "GNDVI": """
        <h3>Índice de Vegetação por Diferença Normalizada Verde (GNDVI)</h3>
        <p>
            O Índice de Vegetação por Diferença Normalizada Verde (GNDVI) é uma modificação do NDVI que utiliza a banda verde do espectro eletromagnético em vez da banda vermelha. A clorofila, o pigmento primário envolvido na fotossíntese, absorve fortemente a luz azul e vermelha, enquanto reflete a luz verde. Portanto, o GNDVI é particularmente sensível às variações no conteúdo de clorofila dentro dos dosséis das plantas.
        </p>
        <p>
            A fórmula do GNDVI é calculada como:
        </p>
        <pre>
GNDVI = (NIR - GREEN) / (NIR + GREEN)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
            </ul>
            Essa sensibilidade torna o GNDVI uma ferramenta valiosa para:
            <ul>
                <li>Monitorar o estresse das plantas e deficiências nutricionais</li>
                <li>Detectar sinais precoces de doenças ou infestações por pragas</li>
                <li>Avaliar o vigor das culturas e o potencial de rendimento</li>
                <li>Estudar o impacto de fatores ambientais no crescimento das plantas</li>
            </ul>
        </p>
    """,
    "EVI": """
        <h3>Índice de Vegetação Aprimorado (EVI)</h3>
        <p>
            O Índice de Vegetação Aprimorado (EVI) foi desenvolvido para superar algumas das limitações do NDVI, particularmente em áreas com alta biomassa ou interferência atmosférica. O EVI incorpora uma banda azul em seu cálculo, o que ajuda a minimizar a influência de aerossóis atmosféricos e o ruído do fundo do solo. Além disso, o EVI utiliza um termo de ajuste do fundo do dossel para melhorar a sensibilidade em áreas de alta biomassa e para discriminar melhor a vegetação de superfícies não vegetadas.
        </p>
        <p>
            A fórmula do EVI é calculada como:
        </p>
        <pre>
EVI = 2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>BLUE</b>: Reflectância na banda azul</li>
            </ul>
            O EVI tem se mostrado altamente eficaz em:
            <ul>
                <li>Monitorar a dinâmica da vegetação em diversos ecossistemas</li>
                <li>Estimar a biomassa e a produtividade</li>
                <li>Avaliar o impacto das mudanças climáticas na vegetação</li>
                <li>Mapear a cobertura vegetal e as mudanças no uso/ocupação do solo</li>
            </ul>
        </p>
    """,
    "EVI2": """
        <h3>Índice de Vegetação Aprimorado 2 (EVI2)</h3>
        <p>
            O Índice de Vegetação Aprimorado 2 (EVI2) é uma versão simplificada do Índice de Vegetação Aprimorado (EVI) 
            que não requer a banda azul. Isso o torna particularmente útil para sensores que não possuem uma banda azul 
            ou em casos onde os dados da banda azul são pouco confiáveis.
        </p>
        <p>
            A fórmula do EVI2 é calculada como:
        </p>
        <pre>
    EVI2 = 2.5 * ((NIR - RED) / (NIR + RED + 1))
        </pre>
        <p>
            onde:
            <ul>
            <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
            <li><b>RED</b>: Reflectância na banda vermelha</li>
            </ul>
        </p>
        <p>
            O EVI2 mantém muitas das vantagens do EVI, como maior sensibilidade em áreas de alta biomassa, 
            enquanto é computacionalmente mais simples e amplamente aplicável.
        </p>
        """,
    "SAVI": """
        <h3>Índice de Vegetação Ajustado ao Solo (SAVI)</h3>
        <p>
            O Índice de Vegetação Ajustado ao Solo (SAVI) foi desenvolvido especificamente para minimizar a influência da reflectância do solo, especialmente em áreas com cobertura vegetal 
esparsa. Em tais áreas, a reflectância do solo pode impactar significativamente a precisão de índices de vegetação como o NDVI.
        </p>
        <p>
            O SAVI incorpora um fator de correção do brilho do solo (L) em seu cálculo. Esse fator ajusta a sensibilidade do índice ao fundo do solo, permitindo uma avaliação mais precisa da vegetação em áreas com condições de solo variadas. O SAVI é particularmente útil em:
            <ul>
                <li>Regiões áridas e semiáridas</li>
                <li>Áreas agrícolas com baixa cobertura de vegetação</li>
                <li>Ecossistemas perturbados ou degradados</li>
            </ul>
        </p>
        <p>
            A fórmula do SAVI é calculada como:
        </p>
        <pre>
SAVI = (1 + L) * ((NIR - RED) / (NIR + RED + L))
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>L</b>: Fator de correção do brilho do solo (geralmente definido como 0.5)</li>
            </ul>
        </p>
        <p><b>Nota:</b> Para este plugin, o fator de correção do brilho do solo (L) está definido como 0.5.</p>
    """,
    "MSAVI": """
        <h3>Índice de Vegetação Ajustado ao Solo Modificado (MSAVI)</h3>
        <p>
            O Índice de Vegetação Ajustado ao Solo Modificado (MSAVI) é um aprimoramento do SAVI 
            projetado para minimizar ainda mais os efeitos do solo no monitoramento da vegetação. 
            Diferente do SAVI, que usa um fator de ajuste do solo constante (L), o MSAVI ajusta 
            este fator dinamicamente com base na densidade da vegetação, tornando-o mais responsivo 
            às variações na cobertura vegetativa.
        </p>
        <p>
            O MSAVI é particularmente valioso em áreas com densidades de vegetação mistas e diferentes 
            fundos de solo, pois reduz a necessidade de conhecimento prévio sobre a cobertura vegetal. 
            Isso o torna ideal para:
            <ul>
                <li>Monitoramento agrícola em diferentes estágios de crescimento</li>
                <li>Estudos ecológicos em paisagens heterogêneas</li>
                <li>Avaliação de degradação do solo</li>
                <li>Monitoramento da recuperação da vegetação após distúrbios</li>
            </ul>
        </p>
        <p>
            A fórmula do MSAVI é calculada como:
        </p>
        <pre>
MSAVI = (2 * NIR + 1 - sqrt((2 * NIR + 1)² - 8 * (NIR - RED))) / 2
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
            </ul>
        </p>
        <p>
            A natureza auto-ajustável do MSAVI proporciona medições mais consistentes em paisagens 
            diversas e condições de vegetação variadas em comparação com o NDVI e o SAVI.
        </p>
    """,
    "SFDVI": """
        <h3>Spectral Feature Depth Vegetation Index (SFDVI)</h3>
        <p>
            O Spectral Feature Depth Vegetation Index (SFDVI) integra a banda Red Edge 
            com a banda vermelha para investigar o comportamento da vegetação por meio 
            da profundidade da feição espectral. SFDVI mostra mais gradações em vegetação 
            densa do que NDVI e RENDVI.
        </p>
        <p>
            SFDVI é eficaz para:
            <ul>
                <li>Analisar a vegetação usando a profundidade da feição espectral.</li>
                <li>Mostrar gradações em vegetação densa.</li>
            </ul>
        </p>
        <p>
            A fórmula do SFDVI é calculada como:
        </p>
        <pre>
SFDVI = ((NIR + GREEN)/2 - (RED + REDEDGE)/2)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>REDEDGE</b>: Reflectância na banda da borda vermelha</li>
            </ul>
        </p>
    """,
    "CIgreen": """
        <h3>Índice de Clorofila Verde (CIgreen)</h3>
        <p>
            O Índice de Clorofila Verde (CIgreen) é especificamente projetado para estimar 
            o conteúdo de clorofila em folhas e dosséis de plantas. Diferente dos índices de 
            diferença normalizada, o CIgreen usa uma abordagem baseada em razão que tem mostrado 
            forte correlação com as concentrações reais de clorofila em vários tipos de vegetação.
        </p>
        <p>
            Este índice é particularmente sensível a mudanças sutis nos níveis de clorofila, 
            tornando-o valioso para:
            <ul>
                <li>Detecção precoce de estresse em plantas</li>
                <li>Monitoramento do status de nitrogênio em culturas</li>
                <li>Avaliação da capacidade fotossintética</li>
                <li>Acompanhamento de mudanças sazonais na saúde da vegetação</li>
            </ul>
        </p>
        <p>
            A fórmula do CIgreen é calculada como:
        </p>
        <pre>
CIgreen = (NIR / GREEN) - 1
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
            </ul>
        </p>
        <p>
            Valores mais altos de CIgreen geralmente indicam maior conteúdo de clorofila e 
            vegetação mais saudável. A formulação simples do índice o torna computacionalmente 
            eficiente, enquanto ainda fornece informações valiosas sobre o status fisiológico das plantas.
        </p>
    """,
    "NDRE": """
        <h3>Diferença Normalizada da Borda do Vermelho (NDRE)</h3>
        <p>
            A Diferença Normalizada da Borda do Vermelho (NDRE) é um índice de vegetação avançado 
            que utiliza a porção da borda do vermelho do espectro eletromagnético. A borda do vermelho 
            representa a mudança rápida na reflectância entre as regiões vermelha e infravermelho 
            próximo (aproximadamente 680-730 nm) e é altamente sensível ao conteúdo de clorofila 
            e à saúde da vegetação.
        </p>
        <p>
            O NDRE é particularmente valioso para:
            <ul>
                <li>Detectar sinais precoces de estresse nas culturas antes que os sintomas visíveis apareçam</li>
                <li>Monitorar o status de nitrogênio nas culturas com alta precisão</li>
                <li>Avaliar a saúde da vegetação em dosséis densos onde o NDVI pode saturar</li>
                <li>Distinguir entre variações sutis na condição da vegetação</li>
            </ul>
        </p>
        <p>
            A fórmula do NDRE é calculada como:
        </p>
        <pre>
NDRE = (NIR - REDEDGE) / (NIR + REDEDGE)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>REDEDGE</b>: Reflectância na banda da borda vermelha (tipicamente 720-740 nm)</li>
            </ul>
        </p>
        <p>
            Os valores do NDRE geralmente variam de -1 a 1, com valores mais altos indicando vegetação 
            mais saudável. O NDRE oferece vantagens significativas sobre o NDVI em vegetação densa onde 
            o NDVI tende a saturar, tornando-o especialmente útil para agricultura de precisão e 
            aplicações avançadas de monitoramento de vegetação.
        </p>
    """,
    "ARVI": """
        <h3>Índice de Vegetação Resistente à Atmosfera (ARVI)</h3>
        <p>
            O Índice de Vegetação Resistente à Atmosfera (ARVI) é projetado para ser menos sensível 
            aos efeitos atmosféricos (como aerossóis) em comparação com o NDVI. Ele incorpora um 
            fator de correção usando a banda azul para compensar a dispersão atmosférica.
        </p>
        <p>
            A fórmula do ARVI é calculada como:
        </p>
        <pre>
ARVI = (NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>BLUE</b>: Reflectância na banda azul</li>
            </ul>
        </p>
        <p>
            O ARVI é útil em regiões com presença significativa de aerossóis atmosféricos, fornecendo 
            uma avaliação mais precisa da cobertura vegetal.
        </p>
    """,
    "NDMI": """
        <h3>Índice de Umidade por Diferença Normalizada (NDMI)</h3>
        <p>
            O Índice de Umidade por Diferença Normalizada (NDMI) é usado para monitorar o conteúdo de 
            umidade da vegetação. Ele é sensível a mudanças no conteúdo de água dos dosséis das plantas.
        </p>
        <p>
            A fórmula do NDMI é calculada como:
        </p>
        <pre>
NDMI = (NIR - SWIR) / (NIR + SWIR)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>SWIR</b>: Reflectância na banda do infravermelho de ondas curtas</li>
            </ul>
        </p>
        <p>
            O NDMI é valioso no monitoramento da seca, no gerenciamento da irrigação e na avaliação 
            do estresse da vegetação relacionado à disponibilidade de água.
        </p>
    """,
    "NBR": """
        <h3>Índice de Queimada Normalizada (NBR)</h3>
        <p>
            O Índice de Queimada Normalizada (NBR) é projetado para identificar áreas queimadas e avaliar 
            a severidade da queimada. Ele usa a diferença entre a reflectância do infravermelho próximo e 
            do infravermelho de ondas curtas.
        </p>
        <p>
            A fórmula do NBR é calculada como:
        </p>
        <pre>
NBR = (NIR - SWIR) / (NIR + SWIR)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>SWIR</b>: Reflectância na banda do infravermelho de ondas curtas</li>
            </ul>
        </p>
        <p>
            O NBR é usado extensivamente na avaliação pós-incêndio para mapear áreas queimadas e 
            monitorar a recuperação da vegetação.
        </p>
    """,
    "SIPI": """
        <h3>Índice de Pigmentos Insensível à Estrutura (SIPI)</h3>
        <p>
            O Índice de Pigmentos Insensível à Estrutura (SIPI) é usado para avaliar o estresse do dossel 
            da vegetação.
        </p>
        <p>
            A fórmula do SIPI é calculada como:
        </p>
        <pre>
SIPI = (NIR - BLUE) / (NIR - RED)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>BLUE</b>: Reflectância na banda azul</li>
            </ul>
        </p>
        <p>
            SIPI é útil para minimizar os efeitos da estrutura do dossel.
        </p>
    """,
    "NDWI": """
        <h3>Índice de Água por Diferença Normalizada (NDWI)</h3>
        <p>
            O Índice de Água por Diferença Normalizada (NDWI) é usado para monitorar mudanças no conteúdo 
            de água na vegetação.
        </p>
        <p>
            A fórmula do NDWI é calculada como:
        </p>
        <pre>
NDWI = (GREEN - NIR) / (GREEN + NIR)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
            </ul>
        </p>
        <p>
            NDWI é sensível a mudanças no conteúdo de água líquida dos dosséis de vegetação.
        </p>
    """,
    "ReCI": """
        <h3>Índice de Clorofila da Borda Vermelha (ReCI)</h3>
        <p>
            O Índice de Clorofila da Borda Vermelha (ReCI) é projetado para estimar o conteúdo de 
            clorofila na vegetação usando a banda da borda vermelha.
        </p>
        <p>
            A fórmula do ReCI é calculada como:
        </p>
        <pre>
ReCI = (NIR / REDEDGE) - 1
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>REDEDGE</b>: Reflectância na banda da borda vermelha</li>
            </ul>
        </p>
        <p>
            ReCI é particularmente útil na agricultura de precisão para monitorar a saúde das culturas 
            e o status de nitrogênio.
        </p>
    """,
    "MTCI": """
        <h3>Índice de Clorofila Terrestre MERIS (MTCI)</h3>
        <p>
            O Índice de Clorofila Terrestre MERIS (MTCI) é sensível ao conteúdo de clorofila na vegetação.
        </p>
        <p>
            A fórmula do MTCI é calculada como:
        </p>
        <pre>
MTCI = (NIR - REDEDGE) / (REDEDGE - RED)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>REDEDGE</b>: Reflectância na banda da borda vermelha</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
            </ul>
        </p>
        <p>
            MTCI é útil para estimar o conteúdo de clorofila e monitorar a saúde da vegetação.
        </p>
    """,
    "MCARI": """
        <h3>Índice de Razão de Absorção de Clorofila Modificado (MCARI)</h3>
        <p>
            O Índice de Razão de Absorção de Clorofila Modificado (MCARI) é projetado para ser sensível 
            à concentração de clorofila.
        </p>
        <p>
            A fórmula do MCARI é calculada como:
        </p>
        <pre>
MCARI = ((REDEDGE - RED) - 0.2 * (REDEDGE - GREEN)) * (REDEDGE / RED)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo (usado como REDEDGE)</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
            </ul>
        </p>
        <p>
            MCARI pode ser usado para avaliar o estresse da vegetação.
        </p>
    """,
    "VARI": """
        <h3>Índice Visível Resistente à Atmosfera (VARI)</h3>
        <p>
            O Índice Visível Resistente à Atmosfera (VARI) minimiza os efeitos atmosféricos e realça o 
            sinal da vegetação na parte visível do espectro.
        </p>
        <p>
            A fórmula do VARI é calculada como:
        </p>
        <pre>
VARI = (GREEN - RED) / (GREEN + RED - BLUE)
        </pre>
        <p>
            onde:
            <ul>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>BLUE</b>: Reflectância na banda azul</li>
            </ul>
        </p>
        <p>
            VARI é útil quando a correção atmosférica é desafiadora.
        </p>
    """,
    "TVI": """
        <h3>Índice de Vegetação Triangular (TVI)</h3>
        <p>
            A fórmula do TVI é calculada como:
        </p>
        <pre>
TVI = 0.5 * (120 * (NIR - GREEN) - 200 * (RED - GREEN))
        </pre>
        <p>
            onde:
            <ul>
                <li><b>NIR</b>: Reflectância na banda do infravermelho próximo</li>
                <li><b>RED</b>: Reflectância na banda vermelha</li>
                <li><b>GREEN</b>: Reflectância na banda verde</li>
            </ul>
        </p>
    """,
}
