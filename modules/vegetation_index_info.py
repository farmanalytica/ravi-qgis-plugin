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
    """
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
    "SAVI": """
        <h3>Índice de Vegetação Ajustado ao Solo (SAVI)</h3>
        <p>
            O Índice de Vegetação Ajustado ao Solo (SAVI) foi desenvolvido especificamente para minimizar a influência da reflectância do solo, especialmente em áreas com cobertura vegetal esparsa. Em tais áreas, a reflectância do solo pode impactar significativamente a precisão de índices de vegetação como o NDVI.
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
    """
}