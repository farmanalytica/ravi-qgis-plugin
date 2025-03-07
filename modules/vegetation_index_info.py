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
            The Structurally Focused Difference Vegetation Index (SFDVI) is designed to 
            better capture structural variations in vegetation canopies by combining 
            spectral information from multiple bands. It evaluates not only chlorophyll 
            content but also canopy structure and biomass.
        </p>
        <p>
            SFDVI is particularly effective for:
            <ul>
                <li>Monitoring crop canopy development</li>
                <li>Assessing forest structure and biomass</li>
                <li>Distinguishing between different vegetation types</li>
                <li>Tracking vegetation structural changes over time</li>
            </ul>
        </p>
        <p>
            The SFDVI formula is calculated as:
        </p>
        <pre>
SFDVI = (NIR - RED - BLUE) / (NIR + RED + BLUE)
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
            By incorporating blue reflectance, SFDVI provides enhanced sensitivity to 
            structural components of vegetation while maintaining robustness to atmospheric 
            effects and background noise.
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
        <h3>Índice de Vegetação por Diferença Focada na Estrutura (SFDVI)</h3>
        <p>
            O Índice de Vegetação por Diferença Focada na Estrutura (SFDVI) é projetado para 
            capturar melhor as variações estruturais nos dosséis da vegetação, combinando 
            informações espectrais de múltiplas bandas. Ele avalia não apenas o conteúdo de 
            clorofila, mas também a estrutura do dossel e a biomassa.
        </p>
        <p>
            O SFDVI é particularmente eficaz para:
            <ul>
                <li>Monitorar o desenvolvimento do dossel das culturas</li>
                <li>Avaliar a estrutura e biomassa florestal</li>
                <li>Distinguir entre diferentes tipos de vegetação</li>
                <li>Acompanhar mudanças estruturais na vegetação ao longo do tempo</li>
            </ul>
        </p>
        <p>
            A fórmula do SFDVI é calculada como:
        </p>
        <pre>
SFDVI = (NIR - RED - BLUE) / (NIR + RED + BLUE)
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
            Ao incorporar a reflectância do azul, o SFDVI proporciona maior sensibilidade aos 
            componentes estruturais da vegetação, mantendo a robustez aos efeitos atmosféricos 
            e ao ruído de fundo.
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
                <li><b>REDEDGE</b>: Reflectância na banda da borda do vermelho (tipicamente 720-740 nm)</li>
            </ul>
        </p>
        <p>
            Os valores do NDRE geralmente variam de -1 a 1, com valores mais altos indicando vegetação 
            mais saudável. O NDRE oferece vantagens significativas sobre o NDVI em vegetação densa onde 
            o NDVI tende a saturar, tornando-o especialmente útil para agricultura de precisão e 
            aplicações avançadas de monitoramento de vegetação.
        </p>
    """
}