## RAVI - Remote Analysis of Vegetation Indices

Este repositório contém o código-fonte do complemento **RAVI** para QGIS, que integra a API Python do Google Earth Engine (GEE) para processar e visualizar dados geoespaciais utilizando o catálogo de reflectância de superfície harmonizada da missão Copernicus Sentinel-2. O RAVI é uma ferramenta para estudantes, pesquisadores, produtores rurais e profissionais que atuam em agricultura, monitoramento territorial ou gestão ambiental.

## Tutorial
Um guia de uso está disponível via GitHub Pages em:  
[https://caioarantes.github.io/ravi-qgis-plugin/](https://caioarantes.github.io/ravi-qgis-plugin/)  

## Relato de Problemas
Se você encontrar algum problema ou tiver sugestões de melhorias, abra uma issue na seção [GitHub Issues](https://github.com/caioarantes/ravi-qgis-plugin/issues) ou entre em contato diretamente.

## Licença
O RAVI está licenciado sob a GNU General Public License v2.0 ou posterior. Consulte o arquivo [LICENSE](https://github.com/caioarantes/ravi-qgis-plugin/blob/main/LICENSE) para mais detalhes.

---

## RAVI - Remote Analysis of Vegetation Indices

This repository contains the source code for the **RAVI** plugin for QGIS, which integrates with Google Earth Engine (GEE) Python API to process and visualize geospatial data using the Copernicus mission Sentinel-2 harmonized surface reflectance catalog. RAVI is a tool for students, researchers, farmers, and professionals working in agriculture, land monitoring, or environmental management.

## Tutorial
An usage guide is available via GitHub Pages here:  
[https://caioarantes.github.io/ravi-qgis-plugin/](https://caioarantes.github.io/ravi-qgis-plugin/)  

## Reporting Issues
If you encounter any issues or have suggestions for improvements, please open an issue in the [GitHub Issues](https://github.com/caioarantes/ravi-qgis-plugin/issues) section or contact me directly.

## License
RAVI is licensed under the GNU General Public License v2.0 or later. Refer to the [LICENSE](https://github.com/caioarantes/ravi-qgis-plugin/blob/main/LICENSE) file for details.


## TEXTO DO TCC
## (VERSÃO PRELIMINAR - NÃO REVISADA POR ORIENTADORES)

### RESUMO:

O complemento RAVI (Remote Analysis of Vegetation Indices), desenvolvido para a plataforma QGIS, disponibilizado publicamente, e foco deste trabalho, é uma ferramenta para Agricultura de Precisão (AP), monitoramento ambiental e pesquisa acadêmica. Seu objetivo é fornecer uma interface gráfica e de fácil acesso para acessar, processar e visualizar imagens da missão Copernicus Sentinel-2 utilizando recursos do Google Earth Engine. Ele oferece um fluxo de trabalho passo a passo com opções para seleção de área de interesse, intervalo de tempo, filtragem e máscara de nuvem, visualização e exportação de dados. Como funcionalidade, o RAVI entrega a série temporal de índices de vegetação selecionado para a área de interesse, permite a criação de imagens sintéticas, visualização e download de imagens em cor natural ou índices de vegetação em data selecionada. O complemento foi publicado por meio oficial de distribuição e possui usuários ativos, o que demonstra seu potencial como ferramenta prática para as funcionalidades propostas, especialmente para usuários sem experiência em programação. Ao simplificar acesso e processamento de dados de sensoriamento remoto orbital, a ferramenta fortalece a integração da inovação tecnológica na gestão da vegetação e do solo, oferecendo mais um recurso para estudantes, pesquisadores e profissionais interessados em compreender e gerir a saúde da vegetação e do solo de forma baseada em dados.

Palavras chave: Índices vegetativos, Agricultura de Precisão, Sensoriamento Remoto, Sistema de Informações Geográficas.


### ABSTRACT:


The RAVI (Remote Analysis of Vegetation Indices) plugin, developed for the QGIS platform, publicly available, and the focus of this work, is a tool for Precision Agriculture (PA), environmental monitoring, and academic research. Its objective is to provide a user-friendly graphical interface for accessing, processing, and visualizing images from the Copernicus Sentinel-2 mission using Google Earth Engine resources. It offers a step-by-step workflow with options for selecting an area of interest, time range, cloud filtering and masking, visualization, and data export. As a functionality, RAVI delivers the time series of selected vegetation indices for the area of interest, allows for the creation of synthetic images, visualization and download of natural color images or vegetation indices on a selected date. The plugin was published through an official distribution channel and has active users, which demonstrates its potential as a practical tool for the proposed functionalities, especially for users without programming experience. By simplifying the access and processing of orbital remote sensing data, the tool strengthens the integration of technological innovation in vegetation and soil management, offering another resource for students, researchers, and professionals interested in understanding and managing vegetation and soil health in a data-driven manner.

Keywords: Vegetation Indices, Precision Agriculture, Remote Sensing, Geographic Information System.


## 1. INTRODUÇÃO

A Agricultura de Precisão (AP) é uma abordagem de gestão agrícola que visa considerar a variabilidade espacial das lavouras nas práticas de manejo, buscando otimizar o uso de recursos e elevar a produtividade sem a necessidade de expandir a área cultivada. Parte-se do princípio de que as condições do solo — tanto químicas quanto físicas — apresentam variabilidade ao longo da propriedade, o que influencia diretamente o desenvolvimento das culturas e as demandas locais por insumos, como fertilizantes e defensivos.

O Sensoriamento Remoto (SR) é um conjunto de técnicas voltadas a fornecer informações sobre a superfície da terra sem contato físico. O sensoriamento remoto orbital, com sensores multiespectrais embarcados em satélites que capturam a refletância da luz solar da superfície, pode gerar dados de suporte à AP. A refletância mensurada pelos sensores em diferentes espectros da luz, e a combinação desses dados com fórmulas matemáticas, conhecidas como Índice de Vegetação (IV), podem gerar dados relevantes para AP, como estimativas da atividade fotossintética e biomassa vegetal espacializada, que em sensores como Sentinel-2, pode chegar a 10 metros de resolução espacial e 5 dias de tempo de retorno (resolução temporal).

O acesso aos dados Sentinel-2 pode ser realizado em plataformas online como Copernicus Browser ou Google Earth Engine (GEE). Porém, o acesso aos dados pelo primeiro pode ser dispendioso em tempo, além de exigir processamento adicional dos dados em outras ferramentas para se tornarem úteis às finalidades de AP. No último, o acesso e processamento dos dados podem ser realizados online, por meio de uma interface de programação integrada (IDE) acessível pelo navegador de internet, denominada Code Editor. Além do Code Editor, é possível acessar os recursos de computação em nuvem do GEE por meio de sua API Python, que foi desenvolvida especificamente para a integração em aplicativos, segundo a própria empresa que a disponibiliza (Google).
O uso pleno dos recursos do GEE para finalidades de AP, porém, demanda conhecimentos técnicos em linguagem de programação JavaScript ou Python, de algoritmos e bibliotecas específicas de geoprocessamento, além de proficiência em manipular o código produzido, o que pode exigir dezenas de horas para aprendizado e proficiência.

Softwares focados em processar, analisar e visualizar dados geográficos, conhecidos como Sistema de Informações Geográficas (SIG) podem fazem parte do fluxo de trabalho de acadêmicos e profissionais que aplicam AP. Entre esses softwares, o QGIS destaca-se por ser um software gratuito, com diversas ferramentas inclusas, além de permitir a ampliação de suas funcionalidades por meio de complementos, que funcionam como aplicativos internos da plataforma.

Os complementos para QGIS são desenvolvidos em linguagem de programação Python e podem, por meio da API Python PyQGIS, controlar os recursos do QGIS, além de acessar o terminal Python integrado, com possibilidade de importar bibliotecas externas e executar algoritmos customizados.

Diante da constatação dos gargalos para a adoção de dados Sentinel-2 na AP, principalmente devido à curva de aprendizado em programação, e da disponibilidade de ferramentas que viabilizam a integração dos recursos de acesso e processamento de dados por computação em nuvem (a API Python do GEE e a capacidade de implementá-la no QGIS via complemento), este trabalho foi proposto, com foco no desenvolvimento de um complemento para o QGIS que integra as rotinas GEE comumente usadas no acesso e processamento de dados Sentinel-2 para as finalidades de AP, a uma interface gráfica. Assim, usuários da ferramenta poderão aplicar as rotinas desenvolvidas por meio de uma interface gráfica, agilizando o fluxo de trabalho necessário para obter esses resultados.
 

### 1.1	JUSTIFICATIVA

A crescente demanda por sustentabilidade e eficiência na produção agrícola impulsiona a adoção da Agricultura de Precisão (AP), que se beneficia da análise de dados geoespaciais de sensoriamento remoto orbital, como os fornecidos pelos satélites Sentinel-2. No entanto, o acesso e processamento desses dados, especialmente através de plataformas como o Google Earth Engine (GEE), exigem proficiência em programação e conhecimentos técnicos avançados, criando uma barreira para a sua ampla utilização por agrônomos, pesquisadores e produtores. Diante desse cenário, a ausência de ferramentas que facilitem o uso de SR orbital em ambientes SIG familiares como o QGIS sem a necessidade de codificação, justifica o desenvolvimento deste trabalho como uma solução prática para impulsionar a utilização deste tipo de dado.

### 1.2	OBJETIVOS

O objetivo deste trabalho é desenvolver e disponibilizar publicamente um complemento para o software QGIS, denominado RAVI (Análise Remota de Índices de Vegetação). Através deste complemento, capacidades de acesso e processamento de dados em nuvem do Google Earth Engine (GEE), de imagens da missão Copernicus Sentinel-2, serão disponibilizadas e poderão ser utilizadas sem necessidade de conhecimentos em programação e manipulação de linhas de código. Funcionalidades como seleção de área de interesse, filtragem de nuvens, geração de séries temporais de índices de vegetação, a visualização e download de imagens em cor natural e de índices para datas selecionadas ou em composições sintéticas serão oferecidas. 

## 2. REVISÃO BIBLIOGRÁFICA


## 3. METODOLOGIA


## 4. RESULTADOS E DISCUSSÃO


## 5. CONCLUSÕES


## REFERÊNCIAS
