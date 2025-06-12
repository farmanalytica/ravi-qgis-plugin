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

Softwares focados em processar, analisar e visualizar dados geográficos, conhecidos como Sistema de Informações Geográficas (SIG) podem fazem parte do fluxo de trabalho de acadêmicos e profissionais que aplicam AP. Entre esses softwares, o QGIS destaca-se por ser um software gratuito, com diversas ferramentas inclusas, além de permitir a ampliação de suas funcionalidades por meio de complementos, que funcionam como aplicativos internos da plataforma. Os complementos para QGIS são desenvolvidos em linguagem de programação Python e podem, por meio da API Python PyQGIS, controlar os recursos do QGIS, além de acessar o terminal Python integrado, com possibilidade de importar bibliotecas externas e executar algoritmos customizados.

Diante da constatação dos gargalos para a adoção de dados Sentinel-2 na AP, principalmente devido à curva de aprendizado em programação, e da disponibilidade de ferramentas que viabilizam a integração dos recursos de acesso e processamento de dados por computação em nuvem (a API Python do GEE e a capacidade de implementá-la no QGIS via complemento), este trabalho foi proposto, com foco no desenvolvimento de um complemento para o QGIS que integra as rotinas GEE comumente usadas no acesso e processamento de dados Sentinel-2 para as finalidades de AP, a uma interface gráfica. Assim, usuários da ferramenta poderão aplicar as rotinas desenvolvidas por meio de uma interface gráfica, agilizando o fluxo de trabalho necessário para obter esses resultados.
 

### 1.1	JUSTIFICATIVA

A crescente demanda por sustentabilidade e eficiência na produção agrícola impulsiona a adoção da Agricultura de Precisão (AP), que se beneficia da análise de dados geoespaciais de sensoriamento remoto orbital, como os fornecidos pelos satélites Sentinel-2. No entanto, o acesso e o processamento desses dados, especialmente por meio de plataformas como o Google Earth Engine (GEE), exigem proficiência em programação e conhecimentos técnicos avançados, criando uma barreira para sua ampla utilização por agrônomos, pesquisadores e produtores rurais. Diante desse cenário, a ausência de ferramentas que facilitem o uso de sensoriamento remoto orbital em ambientes SIG familiares, como o QGIS, sem a necessidade de codificação, justifica o desenvolvimento deste trabalho como uma solução prática para impulsionar a utilização desse tipo de dado para finalidades como monitoramento agrícola e Agricultura de Precisão.

### 1.2	OBJETIVOS

O objetivo deste trabalho é desenvolver e disponibilizar publicamente um complemento para o software QGIS, denominado RAVI (Análise Remota de Índices de Vegetação). Por meio deste complemento, os recursos de acesso e processamento de imagens da missão Copernicus Sentinel-2 na plataforma em nuvem Google Earth Engine (GEE) poderão ser utilizados sem a necessidade de conhecimentos em programação ou manipulação de código. Serão oferecidas funcionalidades como seleção de área de interesse, filtragem de nuvens, geração de séries temporais de índices de vegetação, bem como a visualização e o download de imagens em cor natural e de índices para datas selecionadas ou em composições sintéticas

## 2. REVISÃO BIBLIOGRÁFICA

### 2.1	Agricultura de Precisão (AP)

A Agricultura de Precisão (AP) pode ser definida como estratégia de gestão agrícola que visa otimizar o uso de recursos e elevar a produtividade, reconhecendo e gerenciando a variabilidade espacial e temporal das lavouras. Diferentemente de abordagens tradicionais que aplicam insumos de forma homogênea, a AP baseia-se na premissa de que as condições do solo e as demandas nutricionais das culturas variam dentro de uma mesma propriedade ou mesmo talhão. Ao longo da história, o manejo agrícola buscou aprimorar a eficiência, mas foi com o advento das tecnologias de posicionamento global (GNSS), técnicas de sensoriamento e ferramentas computacionais que a AP se consolidou como uma disciplina capaz de fornecer subsídios para a tomada de decisões localizadas, permitindo, por exemplo, a aplicação de fertilizantes e defensivos em taxa variada, apenas onde e quando necessário.

###  2.2	Sensoriamento Remoto (SR)

O Sensoriamento Remoto (SR) compreende o conjunto de técnicas e tecnologias que permitem a aquisição de informações sobre a superfície terrestre e seus fenômenos sem contato físico direto. Na agricultura, o sensoriamento remoto orbital tornou-se uma ferramenta para o monitoramento de culturas em diferentes escalas. Esses dados, coletados por sensores embarcados em satélites orbitais –, capturam a refletância da luz solar ou a emissão de energia em distintas faixas do espectro eletromagnético. A análise dessas respostas espectrais pode possibilitar a inferências sobre atributos biofísicos da vegetação, como estresse hídrico, deficiências nutricionais e o estágio de desenvolvimento das plantas, e pode fornecer subsídios para o manejo localizado e a gestão das lavouras. 

###  2.3	Missão Copernicus Sentinel-2

Os satélites de observação da Terra embarcam tecnologia de sensoriamento remoto aplicada a diversas áreas, incluindo a agricultura e o monitoramento ambiental. Ao longo das últimas décadas, missões como Landsat e MODIS estabeleceram a base para o fornecimento contínuo de dados de larga escala. No contexto da Agricultura de Precisão, a missão Copernicus Sentinel-2 da Agência Espacial Europeia (ESA) destaca-se como uma fonte de dados de resolução espacial (até 10 m) e temporal (até 5 dias de tempo de retorno), superando aspectos e capacidades de missões anteriores para aplicações de monitoramento agrícola e Agricultura de Precisão. Composta por dois satélites idênticos (Sentinel-2A e Sentinel-2B) que orbitam em sincronia, seus sensores capturam 13 bandas espectrais. 

###  2.3	Índices de Vegetação (IVs)

Índices de Vegetação (IVs) são transformações matemáticas que combinam valores de reflectância de duas ou mais bandas espectrais para gerar uma única métrica que realça uma propriedade da vegetação. A base física para a maioria dos IVs é o comportamento espectral da vegetação saudável, que, devido à clorofila, absorve fortemente a radiação na faixa do vermelho (VIS) e, por sua estrutura celular, reflete intensamente na faixa do infravermelho próximo (NIR). Ao quantificar esse contraste, o valor do índice correlaciona-se com parâmetros biofísicos como densidade de biomassa, índice de área foliar (IAF) e atividade fotossintética. A existência de múltiplos índices, como o tradicional NDVI (Índice de Vegetação por Diferença Normalizada) e o EVI (Índice de Vegetação Aprimorado), deve-se à necessidade de mitigar interferências que podem distorcer a medição, como o brilho do solo e a dispersão atmosférica, sendo o EVI, por exemplo, otimizado para oferecer maior sensibilidade em áreas de vegetação densa. Dessa forma, os IVs fornecem uma base quantitativa para o monitoramento da dinâmica da vegetação em aplicações agrícolas e ambientais. 

###  2.4	Plataformas de Processamento de Dados Geoespaciais em Nuvem

A explosão no volume de dados geoespaciais gerados por satélites e outras fontes, juntamente com a crescente demanda por análises em larga escala, tem impulsionado o desenvolvimento e a adoção de plataformas de processamento em nuvem. Essas plataformas revolucionaram a forma como os dados de sensoriamento remoto são armazenados, acessados e analisados, eliminando a necessidade de infraestrutura de hardware local robusta e permitindo a execução de algoritmos complexos em ambientes distribuídos. Entre as soluções disponíveis, o Google Earth Engine (GEE) se destaca como um exemplo proeminente, oferecendo um catálogo de dados geospaciais multi-petabyte e uma capacidade de computação em nuvem sem precedentes. No entanto, o pleno aproveitamento de seus recursos frequentemente demanda habilidades em programação, o que pode representar uma barreira de entrada para muitos profissionais e pesquisadores da área de Agricultura de Precisão.

###  2.5 Sistemas de Informações Geográficas (SIG) e Desenvolvimento de Complementos

Os Sistemas de Informações Geográficas (SIG) são ferramentas computacionais que permitem a captura, armazenamento, manipulação, análise e visualização de dados referenciados espacialmente. No contexto da Agricultura de Precisão, os SIG desempenham um papel central, sendo utilizados para integrar informações de diversas fontes – como mapas de solo, dados de produtividade, informações de sensoriamento remoto e pontos de amostragem – auxiliando no planejamento, execução e avaliação das práticas de manejo. Dentre as opções de software SIG, o QGIS (Quantum GIS) consolidou-se como uma escolha preferencial para muitos profissionais e acadêmicos, devido à sua natureza de código aberto, gratuidade e uma vasta gama de ferramentas nativas. Além disso, a arquitetura extensível do QGIS, que permite o desenvolvimento de complementos (complementos) em Python (através da biblioteca PyQGIS), oferece uma oportunidade única para personalizar funcionalidades e integrar recursos externos, como APIs de processamento em nuvem, diretamente no ambiente do usuário.

###  2.6 Lacunas da Literatura e a Contribuição do Presente Trabalho

Apesar do avanço significativo nas tecnologias de sensoriamento remoto e nas plataformas de processamento geoespacial em nuvem, como o Google Earth Engine, uma lacuna persistente na literatura e na prática da Agricultura de Precisão reside na acessibilidade e facilidade de uso dessas ferramentas para usuários que não possuem proficiência em linguagens de programação. Embora o GEE ofereça capacidade computacional e um catálogo de dados amplo, sua interface de programação exige conhecimentos específicos que demandam tempo e dedicação para serem adquiridos. Paralelamente, os Sistemas de Informações Geográficas, notadamente o QGIS, são amplamente utilizados por agrônomos e pesquisadores e representam o ambiente de trabalho preferencial para a análise espacial. Contudo, a integração fluida entre o ambiente SIG e o poder de processamento em nuvem do GEE ainda é subexplorada de forma simplificada. Diante dessa constatação, o presente trabalho se propõe a contribuir para a área ao desenvolver o complemento RAVI para o QGIS, preenchendo essa lacuna ao oferecer uma interface gráfica para o acesso, processamento e visualização de dados Sentinel-2 via GEE, eliminando a barreira da programação e facilitando a incorporação de análises de sensoriamento remoto avançadas no dia a dia da Agricultura de Precisão.

## 3. METODOLOGIA

### 3.1 Base tecnológica

Para auxiliar no processo de desenvolvimento, foram utilizados os complementos Plugin Builder e Plugin Reloader. O Plugin Builder facilitou a criação da estrutura básica do complemento, gerando automaticamente os arquivos e pastas necessários, além de fornecer um modelo para a interface gráfica (arquivo .ui). O Plugin Reloader permitiu a atualização automática do complemento no QGIS após cada modificação no código, agilizando o processo de testes e depuração. 

A interface gráfica do complemento foi criada com o framework Qt Designer, que oferece um ambiente visual para a criação de interfaces personalizadas. Os elementos da interface (botões, caixas de texto, menus, comboboxes, sliders, checkboxes, visualizadores de texto e web) foram organizados em um fluxo de trabalho passo a passo, facilitado por um sistema de abas para guiar o usuário através das funcionalidades do complemento. 

O desenvolvimento do complemento também fez uso extensivo do pacote `pandas` para manipulação e análise de dados tabulares, além de diversas bibliotecas Python relacionadas à manipulação de arquivos locais (como `os`, `shutil` e `pathlib`) e ao envio de requisições web (como `requests`). Essas bibliotecas foram fundamentais para o processamento eficiente dos dados, integração com APIs externas e gerenciamento dos arquivos gerados e baixados durante o uso do complemento.

A comunicação com o Google Earth Engine (GEE) foi realizada por meio da API Python do GEE, que permite o acesso aos dados e o processamento em nuvem, dependendo da autenticação do usuário.

### 3.2	Desenvolvimento de software

O desenvolvimento de software do projeto adotou uma metodologia de desenvolvimento de software com duas frentes complementares (iterativa e incremental). Essa abordagem foi escolhida por sua flexibilidade e eficiência, permitindo que o projeto evoluísse de forma controlada e adaptativa.

A metodologia pode ser compreendida da seguinte forma:

Incremental: O desenvolvimento foi dividido em partes funcionais e autônomas, chamadas de "incrementos". Em vez de tentar construir todo o complemento de uma só vez, o foco foi entregar funcionalidades utilizáveis em etapas. Por exemplo, o primeiro incremento focou exclusivamente na autenticação com o Google Earth Engine. Uma vez validado, o ciclo seguinte adicionou a funcionalidade de seleção de área de interesse, e um ciclo posterior a geração do gráfico de série temporal. Cada incremento adicionava ao objetivo do projeto.

Iterativa: O processo foi organizado em ciclos de desenvolvimento curtos e repetidos, ou "iterações". Ao final de cada ciclo, uma nova versão do complemento era gerada, não apenas incorporando novas funcionalidades (o incremento), mas também permitindo a revisão e o aprimoramento das funcionalidades já existentes com base em testes e feedback. Se um teste revelasse uma falha na interface do usuário desenvolvida no ciclo anterior, a correção seria planejada para o ciclo seguinte.

A combinação dessas duas abordagens permitiu a adaptação contínua do complemento. A figura 1 ilustra o fluxo de desenvolvido,  nota que o cliclo fechado do fluxo indica o processo iterativo mencionaado.

![Figura1](.\medias\tcc\figura1.png)
Figura 1: Fluxograma de desenvolvimento

### 3.3	Viabilidade técnica e levantamento de requisitos 

Foi desenvolvido um complemento protótipo denominado IndiceVerde (Figura 2) para testar a viabilidade técnica na fase preliminar do projeto. Nesta fasse foi validado a viabilide da autenticação dor serviões do GEE para sua API Python dentro do ambiente QGIS e seleção de área de interesse com base em arquivo local, como shapefiles (.shp) 

![Figura2](.\medias\tcc\prototipo.png)
Figura 2: Fluxograma de desenvolvimento

Os blocos ilustrados dividem a interface em etapas de uso:

A – Autenticação: para acesso ao GEE, é preciso uma conta google. 1 - Ao clicar uma em Autenticar, abre- se uma janela no navegador padrão para autenticação da conta. 2 -Verificação se autenticação foi bem sucedida. A autenticação fica armazenada na máquina local mesmo após reiniciação da máquina, por isso foi incluído um botão para limpar a autenticação caso seja necessário trocar de usuário.

B – Parâmetros de filtragem e opções, como o período de coleção de imagens, índice vegetativo de escolha e camada vetorial escolhia (área de interesse).

C – Processamento internos, exportação de dados e resultados. Diversos botões foram criados com a
finalidade de dividir etapas do processamento interno do complemento e facilitar o desenvolvimento, e não
representaram a interface gráfica final. Inclui: botão para carregar a primeira imagem do índice
selecionado do período selecionado sob área de interesse; botão para carregar a imagem sintética de
média de índice vegetativo que abrange todo o período sob área de interesse.

O levantamento de requisitos, termo frequentemento utilizado no desenvolvimento de projetos de sofware, busca listar as funcionalidades essenciais do complemento deve entregar, e foram definidas como:

•	Seleção de Área de Interesse (AOI) por arquivos locais.
•	Filtragem de imagens Sentinel-2 por periodo e nuvem.
•	Cálculo e download de imagens multiespectrais e de índices de vegetação.
•	Gerar de séries temporais de índice de vegetação para a AOI.


### 3.3 Validação da Arquitetura

A execução deste trabalho envolve desafios técnicos, incluindo a gestão de interfaces gráficas, o tratamento de requisições assíncronas e a manipulação de dados geoespaciais. A fim de consolidar as competências necessárias, a metodologia incluiu uma fase de desenvolvimento preliminar. Nesta fase, foi desenvolvido outro complemento paralelo, denominado EasyDEM, focado em acessar e processar dados de Modelos Digitais de Elevação (MDE) de catálogos disponiveis no GEE. Este projeto serviu como um ambiente controlado para dominar a API do QGIS (PyQGIS), a construção de interfaces com a biblioteca Qt e a lógica de interação dos serviços GEE via sua API Python.

Devido à sua utilidade prática, o EasyDEM foi publicado  nos canais oficiais do QGIS e, desde então, adquiriu uma base de usuários, sendo mantido pelo autor como um projeto pessoal paralelo. É importante ressaltar que, embora sua criação tenha sido um passo metodológico para este TCC, a descrição detalhada de sua arquitetura e funcionalidades foge ao escopo do presente trabalho. O conhecimento prático consolidado nesta etapa foi diretamente aplicado no desenvolvimento do complemento RAVI, objeto principal deste trabalho, garantindo uma implementação mais robusta e eficiente.

### 3.4	 Entrada de dados e configuações de usuário

A entrada de dados foi dividida por etapas em uma interface com abas, ilustrada na Figura 3. Cada aba corresponde a uma fase do fluxo de trabalho, guiando o usuário desde a autenticação inicial até a configuração dos parâmetros de análise, seleção da área de interesse, definição do período temporal, escolha do índice de vegetação, aplicação de filtros e, por fim, a a visualização e exportação dos resultados (Apresentados em Resultados E Discussões). Esse formato sequencial facilita o uso do complemento, tornando o processo mais didático e reduzindo a possibilidade de erros durante a configuração das análises.


![](.\medias\tcc\figura2.png)
Figura 3: Fluxograma de funcionamento geral


#### 3.4.1	 Autenticação

A Figura 3 apresenta a primeira etapa da interface gráfica do complemento RAVI, dedicada ao processo de autenticação do usuário. Nessa tela, o usuário realiza a autenticação com os serviços do Google Earth Engine (GEE), etapa necessária para habilitar as funcionalidades do complemento. Para isso, é necessário possuir uma conta GEE vinculada a um projeto no Google Cloud e uma ID do projeto. Isso se deve aos seguintes motivos:

- **Autenticação e Permissões:** O GEE exige autenticação para garantir que apenas usuários autorizados possam acessar seus recursos e dados. A conta vinculada ao Google Cloud permite esse controle de acesso.
- **Gerenciamento de Recursos:** O Google Cloud fornece a infraestrutura necessária para o processamento e armazenamento dos dados geoespaciais. Ter um projeto no Google Cloud possibilita monitorar o uso de recursos, definir limites e gerenciar custos.
- **APIs e Serviços:** Diversas funcionalidades do GEE dependem de APIs do Google Cloud, como autenticação OAuth2, armazenamento em nuvem (Google Drive, Cloud Storage) e processamento distribuído.
- **Segurança:** O uso de contas e projetos separados aumenta a segurança, permitindo isolar dados e permissões conforme a necessidade do usuário ou da organização.


![](.\medias\tcc\step1.png)
Figura 3:  Autenticação  


#### 3.4.1	 Pasta de saída  

A figura 4 aprensa a interface de definição do diretório de saída. Aqui, o usuário especifica a pasta local onde os resultados do processamento, como gráficos, imagens e dados tabulares, serão salvos.

![](.\medias\tcc\step2.png)
Figura 4:  Pasta de saída

#### 3.4.2	 Seleção da Área de Interesse

A figura 5 demonstra as diversas opções para delimitar a Área de Interesse (AOI) dentro do complemento RAVI. O usuário pode desenhar geometrias diretamente no mapa do QGIS ou selecionar camadas vetoriais já carregadas.

![](.\medias\tcc\step3.png)
Figura 5:  Seleção da Área de Interesse  
 
 
#### 3.4.3	 Seleção do intervalo de tempo

A quarta etapa da interface, apresentada na figura 6, permite ao usuário definir o período de tempo para a análise das imagens Sentinel-2. Estão disponíveis opções para seleção manual de datas ou atalhos para intervalos predefinidos (últimos 3, 6, 12 meses, etc.).

![](.\medias\tcc\step4.png)
Figura 6:  Seleção do intervalo de tempo
 
#### 3.4.4 Seleção do Índice de Vegetação

A figura 7 ilustra a etapa de seleção do índice de vegetação a ser calculado. O complemento RAVI oferece uma variedade de índices predefinidos (NDVI, EVI, SAVI, GNDVI, etc.), além da opção de definir um índice personalizado.

![](.\medias\tcc\step5.png)
Figura 7:  Seleção do índice de vegetação
 
#### 3.4.5 Filtro de sobreposição de imagens

Nesta etapa da interface, na figura 8, o usuário pode configurar filtros para otimizar a seleção de imagens, como definir uma porcentagem mínima de sobreposição desejada entre as imagens que cobrem a AOI.

![](.\medias\tcc\step6.png)
Figura 8:  Filtro de sobreposição de imagens

#### 3.4.6	 Opções de Buffer

A figura 9 apresenta a interface com as opções para aplicar um buffer ao redor da Área de Interesse selecionada. Essa funcionalidade pode ser útil para incluir ou excluir áreas adjacentes na análise, ou para mitigar efeitos de borda.

![](.\medias\tcc\step7.png)
Figura 9:  Opções de Buffer
 
 #### 3.4.7	 Filtro de nuvem


A oitava etapa da interface, figura 10, permite ao usuário definir um limiar máximo de cobertura de nuvens nas imagens Sentinel-2 a serem processadas, utilizando um controle deslizante (slider).

![](.\medias\tcc\step8.png)
Figura 10:  Filtro de nuvem

#### 3.4.8	 Filtro de Classificação de Cena

Esta figura demonstra as opções de filtragem baseadas na Classificação de Cena (SCL) das imagens Sentinel-2. O usuário pode selecionar as classes de pixels (nuvens, sombras, neve, etc.) que deseja mascarar ou remover da análise através de caixas de seleção (checkboxes).

![](.\medias\tcc\step9.png)
Figura 11:  Filtro de Classificação de Cena 
 
#### 3.4.9	 Visão geral

Esta figura oferece uma visão geral da interface principal do complemento RAVI, consolidando as diversas etapas e opções apresentadas nas figuras anteriores em um único painel para resumir o conjunto de confugurações .

![](.\medias\tcc\step10.png)
Figura 12:  Visão geral  

## 4. RESULTADOS E DISCUSSÃO

Para ilustrar os resultados obtidos, foi utilizado o cortorno da Fazenda São João localizada em Paulínia-SP.

Após o usuário definir os dados de entrada e configurações, o resultado da busca de imagens primeiro indica a quantidade total de imagens encontradas para a AOI, e a quantidade de imagens que premanece no conjunto de imagens após a aplicação de cada parametro de filtragem (figura 13), e após selecionano a opção de ir para próxima aba, outros resultados são exibidos.

![](.\medias\tcc\step11.png)
Figura 13:  Visão geral

### 4.1  Gráfico de Séries Temporais

A série temporal do índice de vegetação sobre a AOI definida pode ser visualizada em um gráfico interativo (figura 14). Valores e datas específicos para uma análise detalhada podem ser observados ao posicionar o cursor sobre o gráfico.

![](.\medias\tcc\results1.png)
Figura 14:  Séries Temporais

### 4.2 Carregar Camada Cor Natural  (Foco em um Dia)

A visualização da camada em cor natural (RGB) no QGIS é realizada ao se selecioar visualizar ou download para uma data específica (figura 14), permitindo que a aparência visual da área seja analisada. Todas as bandas espectrais são baixadas, sendo os números das bandas correspondentes às bandas do Sentinel-2, conforme listado abaixo:

| Nome da Banda Sentinel-2                | Número da Banda no QGIS | Comprimento de Onda (nm) | Resolução Espacial (m) |
|------------------------------------------|------------------------|--------------------------|------------------------|
| Banda 1 (Aerossol Costeiro)              | 1                      | 443                      | 60                     |
| Banda 2 (Azul)                           | 2                      | 490                      | 10                     |
| Banda 3 (Verde)                          | 3                      | 560                      | 10                     |
| Banda 4 (Vermelho)                       | 4                      | 665                      | 10                     |
| Banda 5 (Borda Vermelha da Vegetação)    | 5                      | 705                      | 20                     |
| Banda 6 (Borda Vermelha da Vegetação)    | 6                      | 740                      | 20                     |
| Banda 7 (Borda Vermelha da Vegetação)    | 7                      | 783                      | 20                     |
| Banda 8 (NIR)                            | 8                      | 842                      | 10                     |
| Banda 8A (Borda Vermelha da Vegetação)   | 9                      | 865                      | 20                     |
| Banda 9 (Vapor d'água)                   | 10                     | 945                      | 60                     |
| Banda 11 (SWIR)                          | 11                     | 1610                     | 20                     |
| Banda 12 (SWIR)                          | 12                     | 2190                     | 20                     |

Tabela 1: Informações das Bandas do Sentinel-2

Nota sobre a Banda 10: Observe que a Banda 10 (SWIR - Cirrus) não está disponível no catálogo de Reflectância de Superfície (SR) harmonizada do Sentinel-2. Esta banda é usada principalmente para detecção de nuvens cirrus e é excluída do conjunto de dados SR devido à sua aplicabilidade limitada na análise de superfície.

![](.\medias\tcc\results2.png)
Figura 15:  Carregar Camada Cor Natural (Foco em um Dia)

### 4.3 Carregar Camada de Índice (Foco em um Dia)

A camada de índice de vegetação é exibida no QGIS para uma data específica, sendo possível selecionar entre diversos índices disponíveis para visualização (figura 14).

![](.\medias\tcc\results3.png)
Figura 16:  Carregar Camada de Índice (Foco em um Dia)

### 4.4 Carregar Camada de Índice (Sintética)

A visualização da camada de índice de vegetação composta é realizada por meio da geração e exibição de uma imagem sintética baseada no índice de vegetação selecionado e na métrica definida pelo usuário. A imagem sintética é produzida a partir de todas as imagens que compõem a série temporal, sendo as imagens sobrepostas e cada pixel resultante representando a métrica definida para o índice de vegetação escolhido. Recomenda-se que a ferramenta de remoção de data seja utilizada para que datas indesejadas ou períodos específicos sejam filtrados antes da geração da imagem sintética.

![](.\medias\tcc\results4.png)
Figura 17: Carregar Camada de Índice (Sintética)

###  4.5 Ferramenta de Remoção de Data

A interface da ferramenta de seleção de data deve ser utilizada para que datas e períodos específicos sejam filtrados e selecionados para análise. O gráfico de séries temporais é atualizado automaticamente pela ferramenta. IMPORTANTE: As imagens sintéticas são geradas com base em todas as datas que estiverem selecionadas no momento.

![](.\medias\tcc\results5.png)
Figura 18: Ferramenta de Remoção de Data

###  4.6. Opções de exportaçao de dados

Opções de salvamento para download de imagem e planilha são disponibilizadas na interface. Os dados da série temporal podem ser salvos em formato CSV. Para que a série seja salva como imagem, recomenda-se que ela seja aberta no navegador, onde a opção de download será habilitada.

![](.\medias\tcc\results7.png)
Figura 19: Opções de exportaçao de dados

###  4.7 Análise de multifeição

A análise de séries temporais de multifeição pode ser realizada para avaliar o comportamento de índices de vegetação em diferentes áreas de interesse simultaneamente. Essa funcionalidade permite que múltiplos feiçõs (poligonos) sejam selecionados possibilitando a extração e comparação automática das séries temporais de cada área. Dessa forma, torna-se possível identificar padrões espaciais, comparar diferentes talhões ou regiões e obter insights sobre a variabilidade temporal da vegetação em múltiplas localidades, facilitando análises comparativas, por exemplo de diferentez zonas de manejo e compara o desempenho de diferentes trabamentos agronômicos.

![](.\medias\tcc\results12.png)
Figura 20: Análise de multifeição

### 4.4 Publicação e divulgação

Em dezembro de 2024, o complemento RAVI foi disponibilizado no repositório oficial de complementos experimentais do QGIS, possibilitando o acesso antecipado por usuários interessados em testar novas ferramentas. Essa liberação inicial teve como objetivo principal coletar feedback direto da comunidade, permitindo avaliar a usabilidade, identificar eventuais problemas e aprimorar as funcionalidades com base nas sugestões recebidas.

A versão estável 1.0 foi lançada em fevereiro de 2025 no repositório oficial do QGIS, tornando o complemento acessível a todos os usuários da plataforma. Desde então, o desenvolvimento seguiu um ciclo contínuo de melhorias, incorporando atualizações baseadas tanto em testes internos quanto no retorno dos usuários, com foco em estabilidade, desempenho, experiência do usuário e expansão das funcionalidades.

Além da publicação nos canais oficiais do QGIS, a divulgação do projeto em redes sociais e fóruns especializados contribuiu  para ampliar a base de usuários, promover o engajamento da comunidade e estimular o compartilhamento de experiências e casos de uso do complemento RAVI.

Sobre o uso do RAVI, já relatos privados e em redes sociais de estudantes de graduação que pretendem citar o complemento como ferramenta utilizada em suas iniciações científicas e trabalhos de conclusão de curso (TCC). Profissionais de diferentes áreas também têm adotado o complemento em seus fluxos de trabalho por razões profissionais, demonstrando a aplicabilidade prática e a aceitação da ferramenta por parte do meio acadêmico e profissional.

Foi criado um site oficial com tutoriais em vídeo para auxiliar os usuários na instalação e utilização do complemento RAVI. O site pode ser acessado em: [https://caioarantes.github.io/ravi-qgis-plugin/](https://caioarantes.github.io/ravi-qgis-plugin/). Os vídeos abordam desde a configuração inicial até exemplos práticos de uso das principais funcionalidades, facilitando o a introdução a novos usuários

![](.\medias\tcc\site.png)

Figura 21: site criado com infomações e tutoriais em vídeo

## 5. CONCLUSÕES

O complemento RAVI para a plataforma QGIS é uma ferramenta para o monitoramento agrícola, ambiental e a pesquisa científica. Sua compatibilidade com fluxos de trabalho existentes permite a integração com outras ferramentas de análise. Sua principal contribuição é a simplificação do acesso e processamento de daos sensoriamento remoto orbital, eliminando a necessidade de aprender linguagem de programação para utilizar o Google Earth Engine Code Editor (para as funcionalidades que o complemento oferece). Os resultados obtidos reforçam o potencial do complemento como uma ferramenta prática e eficiente para análise de índices de vegetação ao longo do tempo e acesso a imagens multiespectrais da Missão Copernicus Sentinel-2. A interface gráfica de usuário e as funcionalidades oferecidas atendem a uma base de usuários pouco atendida por outras ferramentas. Ao permitir que usuários sem experiência em programação acessem dados complexos, a ferramenta impulsiona o uso de geotecnologias e fortalece a integração entre inovação tecnológica e práticas agrícolas e de gerenciamento ambiental baseadas em dados. A capacidade da ferramenta em oferecer dados e insights visuais a tornam um recurso para estudantes, pesquisadores e profissionais interessados em compreender e gerir a saúde da vegetação e do solo de forma baseada em dados. A utilização do projeto por usurários indica que o objetivo de desevolver e disponibilizar uma ferrameta de suporte a AP foi satisfeito.

## REFERÊNCIAS

QGIS Development Team. (2025). QGIS Geographic Information System. QGIS Association. https://www.qgis.org Acesso em: 4 maio 2025.

PLUGIN BUILDER. QGIS Plugin Builder. Disponível em: https://g-sherman.github.io/Qgis-Plugin-Builder/. Acesso em: 4 maio 2025.

PLUGIN RELOADER. Plugin Reloader. Disponível em: https://github.com/borysiasty/plugin_reloader. Acesso em: 4 maio 2025.

QT DESIGNER. Qt Designer Manual. Disponível em: https://doc.qt.io/qt-6/qtdesigner-manual.html. Acesso em: 4 maio 2025.