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
    - name: Caio Arantes
      orcid: 0009-0006-6926-9368
      affiliation: 1
affiliations:
    - name: Universidade Estadual de Campinas (UNICAMP)
      index: 1
date: 2025-08-31
bibliography: paper.bib
---

# Resumo

O `ravi-qgis-plugin` (RAVI) é um plugin para QGIS que integra, em uma interface gráfica unificada, (i) cálculo de índices de vegetação amplamente utilizados (ex.: NDVI, EVI) [@rouse1974; @huete2002], (ii) consulta a séries temporais via Google Earth Engine (GEE) [@gorelick2017], (iii) aquisição de dados meteorológicos da API NASA POWER [@nasapower2023], (iv) captura e gestão de coordenadas para comparações de séries temporais, e (v) utilidades de exportação e organização de resultados. O objetivo é reduzir a complexidade das análises ambientais reprodutíveis, fornecendo fluxos de trabalho simplificados e documentação acessível. O projeto é distribuído sob licença livre e visa apoiar pesquisas em monitoramento ambiental, agricultura de precisão e ecologia da vegetação.

# Declaração de Necessidade

Análises de vegetação com imagens Sentinel-2 frequentemente utilizam o Google Earth Engine Code Editor, exigindo rotinas de processamento complexas para definir áreas de interesse, obter e visualizar índices espectrais e suas séries temporais. O Code Editor representa uma barreira para pesquisadores não programadores. Embora existam plugins que cobrem partes dessas tarefas, falta uma solução que agregue: (a) geração de séries temporais de índices de vegetação, (b) integração com dados climáticos, e (c) interface gráfica para acessar recursos do GEE. O RAVI supre essa lacuna ao encapsular tarefas comuns de tratamento de dados Sentinel-2 dentro do ecossistema consolidado do QGIS [@qgis2024].

# Estado da Arte e Diferenciais

Ferramentas existentes geralmente focam em: (1) acesso ao GEE (ex.: interfaces que expõem coleções sem pós-processamento integrado), (2) cálculo de índices isolados, ou (3) download de variáveis meteorológicas. O RAVI diferencia-se por: (i) orquestrar essas etapas em uma sequência coerente; (ii) fornecer validações de parâmetros (intervalos espectrais, escala espacial, CRS) antes da execução; (iii) permitir extensão modular via arquitetura de submódulos Python; e (iv) incorporar descrições de índices diretamente na interface, auxiliando usuários na escolha de métricas apropriadas. A integração simultânea de dados de reflectância e variáveis climáticas facilita análises ecofisiológicas sem alternância entre aplicações.

# Funcionalidades Principais

- Definição de área de interesse com camada vetorial no projeto QGIS.
- Consulta a coleções GEE com filtros personalizáveis por data e cobertura de nuvens.
- Cálculo e visualização de séries temporais de índices vegetativos (NDVI, EVI, SAVI, NDWI, entre outros) diretamente no QGIS.
- Exportação de resultados em formato CSV.
- Geração de gráficos comparativos entre diferentes áreas ou coordenadas.
- Download direto de imagens multiespectrais ou camadas de índice para datas selecionadas, recortadas na área de interesse e adicionadas ao projeto QGIS como camada raster.

# Exemplos de Uso

1. Monitoramento agrícola: detecção de falhas de plantio e estresses em culturas (por motivos diversos, como déficit hídrico, pragas ou manejo inadequado) por meio da análise integrada de séries temporais de NDVI, comparação entre áreas e avaliação de imagens recentes, permitindo identificar rapidamente alterações e padrões espaciais de vigor das plantas.
2. Avaliação do impacto de eventos climáticos extremos (ex.: seca ou geada) sobre áreas de vegetação nativa utilizando séries históricas de NDVI e dados meteorológicos.
3. Mapeamento de áreas com potencial para restauração ecológica, combinando índices de vegetação e variáveis climáticas para priorização espacial.
4. Suporte à tomada de decisão em manejo agrícola, identificando períodos ótimos para irrigação ou aplicação de insumos com base em tendências espectrais e dados climáticos.
5. Monitoramento de áreas protegidas, detectando alterações anômalas na vegetação por meio de séries temporais de índices.

# Impacto Potencial

Ao simplificar o acesso a dados processados e permitir a execução de rotinas complexas com poucos cliques, o RAVI apoia estudos em monitoramento agrícola e conservação. A integração simultânea de clima e reflectância encoraja abordagens eco-hidrológicas integradas. Além disso, ao oferecer uma interface acessível e fluxos de trabalho simplificados, o plugin pode servir como porta de entrada para novos usuários interessados em explorar dados da coleção de refletância de superfície harmonizada Sentinel-2.

# Disponibilidade do Código

- Repositório: https://github.com/caioarantes/ravi-qgis-plugin
- Licença: GNU GPL
- Linguagem principal: Python

# Agradecimentos

Agradece-se à comunidade QGIS, aos mantenedores de bibliotecas científicas Python, aos provedores de dados abertos, a aos usuários que deram feedback e incentivaram este projeto.