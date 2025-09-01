---
title: "ravi-qgis-plugin: Ferramentas integradas de sensoriamento remoto e dados ambientais para o QGIS"
tags:
    - QGIS
    - SIG
    - sensoriamento remoto
    - índices de vegetação
    - Google Earth Engine
    - NASA POWER
    - Python
    - Sentinel-2
authors:
    - name: Caio Simplicio Arantes
      orcid: 0009-0006-6926-9368
      affiliation: 1
    - name: Lucas Rios do Amaral
      orcid: 0000-0001-8071-4449
      affiliation: 1
    - name: Isabella Alves Cunha
      orcid: 0000-0002-4004-3406
      affiliation: 1
    - name: Bruna da Silva Brito Ribeiro
      orcid: 0000-0002-4453-793X
      affiliation: 1
affiliations:
    - name: Universidade Estadual de Campinas (UNICAMP)
      index: 1
date: 2025-08-31
bibliography: paper.bib
---

RAVI é um plugin para QGIS que integra, em uma interface gráfica unificada, (i) cálculo de índices de vegetação amplamente utilizados (ex.: NDVI, EVI) [@rouse1974; @huete2002], (ii) consulta a séries temporais via Google Earth Engine (GEE), aproveitando recursos de computação em nuvem [@gorelick2017], (iii) aquisição de dados meteorológicos da API NASA POWER [@nasapower2023], (iv) captura e gestão de coordenadas para comparações de séries temporais, e (v) utilidades de exportação e organização de resultados. O foco principal do plugin é o catálogo de refletância de superfície harmonizada Sentinel-2 [@esa_sentinel2] , facilitando o acesso e processamento desses dados para análises ambientais. O objetivo é reduzir a complexidade das análises ambientais reprodutíveis, fornecendo fluxos de trabalho simplificados e documentação acessível. O projeto é distribuído sob licença livre e visa apoiar pesquisas em monitoramento ambiental, agricultura de precisão e ecologia da vegetação.

# Declaração de Necessidade

A análise de imagens Sentinel-2 frequentemente depende do uso do Google Earth Engine Code Editor, que exige conhecimento em programação e familiaridade com a API JavaScript do GEE. Essa abordagem, embora robusta, pode ser um desafio para pesquisadores sem experiência em programação. Apesar da existência de plugins que abordam aspectos específicos desse fluxo, ainda falta uma solução integrada que ofereça: (a) geração automatizada de séries temporais de índices de vegetação, (b) download e visualização local dos resultados, e (c) interface gráfica intuitiva para acesso aos recursos do GEE. O RAVI atende a essa demanda ao reunir funcionalidades essenciais para o processamento de dados Sentinel-2 diretamente no ambiente QGIS [@qgis2024], tornando certos tipos de análises mais acessíveis.

# Funcionalidades Principais

- Definição de área de interesse com camada vetorial no projeto QGIS.
- Consulta a coleções GEE com filtros personalizáveis por data e cobertura de nuvens.
- Cálculo e visualização de séries temporais de índices vegetativos (NDVI, EVI, SAVI, NDWI, entre outros) diretamente no QGIS.
- Exportação de resultados em formato CSV.
- Geração de gráficos comparativos entre diferentes áreas ou coordenadas.
- Download direto de imagens multiespectrais ou camadas de índice para datas selecionadas, recortadas na área de interesse e adicionadas ao projeto QGIS como camada raster.
- Geração de imagens compostas geradas a partir da combinação de múltiplas imagens de diferentes datas.

# Exemplos de Uso

1. Monitoramento agrícola: detecção de falhas de plantio e estresses em culturas (por motivos diversos, como déficit hídrico, pragas ou manejo inadequado) por meio da análise integrada de séries temporais de NDVI, comparação entre áreas e avaliação de imagens recentes, permitindo identificar rapidamente alterações e padrões espaciais de vigor das plantas.
2. Avaliação do impacto de eventos climáticos extremos (ex.: seca ou geada) sobre áreas de vegetação nativa utilizando séries históricas de NDVI e dados meteorológicos.
3. Mapeamento de áreas com potencial para restauração ecológica, combinando índices de vegetação e variáveis climáticas para priorização espacial.
4. Suporte à tomada de decisão em manejo agrícola, identificando períodos ótimos para irrigação ou aplicação de insumos com base em tendências espectrais e dados climáticos.
5. Monitoramento de áreas protegidas, detectando alterações anômalas na vegetação por meio de séries temporais de índices.

# Impacto Potencial

Ao simplificar o acesso a dados processados e permitir a execução de rotinas complexas com poucos cliques, o RAVI apoia estudos em monitoramento agrícola e conservação. A integração simultânea de clima e reflectância encoraja abordagens eco-hidrológicas integradas. Além disso, ao oferecer uma interface gráfica, o plugin pode servir como porta de entrada para novos usuários interessados em explorar dados da coleção de refletância de superfície harmonizada Sentinel-2 [@esa_sentinel2].

# Disponibilidade do Código

- Repositório: https://github.com/caioarantes/ravi-qgis-plugin
- Licença: GNU GPL
- Linguagem principal: Python

# Agradecimentos

Agradece-se à comunidade QGIS, aos mantenedores de bibliotecas científicas Python, aos provedores de dados abertos, a aos usuários que deram feedback e incentivaram este projeto.

# Referências
