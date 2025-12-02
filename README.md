## RAVI - Remote Analysis of Vegetation Indices

This repository contains the source code for the **RAVI** plugin for QGIS, which integrates with Google Earth Engine (GEE) Python API to process and visualize geospatial data using the Copernicus mission Sentinel-2 harmonized surface reflectance catalog. RAVI is a tool for students, researchers, farmers, and professionals working in agriculture, land monitoring, or environmental management.

## Tutorial
An usage guide is available via GitHub Pages here:  
[https://caioarantes.github.io/ravi-qgis-plugin/](https://caioarantes.github.io/ravi-qgis-plugin/)  

## Reporting Issues
If you encounter any issues or have suggestions for improvements, please open an issue in the [GitHub Issues](https://github.com/caioarantes/ravi-qgis-plugin/issues) section or contact me directly [caio.arantes@farmanalytica.com.br](mailto:caio.arantes@farmanalytica.com.br).


## RAVI - Remote Analysis of Vegetation Indices

Este repositório contém o código-fonte do complemento **RAVI** para QGIS, que integra a API Python do Google Earth Engine (GEE) para processar e visualizar dados geoespaciais utilizando o catálogo de reflectância de superfície harmonizada da missão Copernicus Sentinel-2. O RAVI é uma ferramenta para estudantes, pesquisadores, produtores rurais e profissionais que atuam em agricultura, monitoramento territorial ou gestão ambiental.

## Tutorial
Um guia de uso está disponível via GitHub Pages em:  
[https://raviqgis.org/](https://raviqgis.org/)  

## Relato de Problemas
Se você encontrar algum problema ou tiver sugestões de melhorias, abra uma issue na seção [GitHub Issues](https://github.com/caioarantes/ravi-qgis-plugin/issues) ou entre em contato direto, envie um e-mail para [caio.arantes@farmanalytica.com.br](mailto:caio.arantes@farmanalytica.com.br).

## 1. Autenticação (Passo 1)

Para utilizar o complemento, é necessário que o usuário possua uma conta na plataforma Google Cloud, com os serviços do GEE habilitados. Cabe ao usuário a responsabilidade de cumprir os termos de serviço da plataforma, que atualmente estabelecem regras que permitem o uso gratuito da plataforma para fins não comerciais e de pesquisa. 

A primeira etapa da interface do complemento RAVI é dedicada ao processo de autenticação do usuário e à configuração de seu ID de projeto no Google Cloud. O ID de projeto é um identificador exigido pelo GEE e tem como finalidade monitorar o uso de recursos, definir limites e gerenciar potenciais custos (Google Cloud, 2025).

![Tela de autenticação do RAVI — Passo 1: Autenticação e inserção do ID de projeto](medias/medias_pt/step0.png)

Figura 1 — Interface de autenticação do complemento RAVI. Insira o ID do projeto do Google Cloud e clique em "Autenticar" para iniciar o fluxo de autorização. Consulte a documentação do GEE caso precise criar ou localizar o ID do projeto.

## 2. Pasta de Saída (Passo 2)

Esta etapa foi implementada para atender ao requisito técnico da funcionalidade de download de imagens em arquivos locais, uma vez que é necessário definir o destino dos dados obtidos via GEE para, posteriormente, carregá-los no QGIS e visualizá-los. O usuário deve especificar a pasta (diretório) onde os resultados das imagens serão salvos para avançar para a próxima etapa da interface. 

![Tela de configuração da Pasta de Saída — Passo 2: Seleção do diretório para salvar resultados](medias/medias_pt/step2.png)

Figura 2 — Interface do Passo 2 do complemento RAVI. Selecione a pasta onde os GeoTIFFs gerados (visualização temporária ou downloads permanentes) serão salvos. Use o botão "Selecionar pasta" para navegar até o diretório desejado; o complemento verifica permissões de escrita e pode criar automaticamente uma subpasta (por exemplo, "ravi-exports"). Recomenda-se escolher uma pasta local com espaço suficiente (evitar unidades de rede instáveis) e confirmar o caminho antes de prosseguir para o Passo 3.

## 3. Seleção da Área de Interesse (Passo 3)


A área da AOI que pode ser utilizada foi limitada a 120 km², se refere ao contorno exato da AOI selecionada (e não a um retângulo que a envolve), para atender a uma limitação técnica do método de download de imagens, que impõe um limite de 32 MB por imagem (ee.Image.getDownloadURL). 
Para facilitar a compreensão do usuário, a AOI selecionada e o limite estabelecido são exibidos para comparação e, caso a AOI selecionada exceda esse limite, é exibido um aviso.
Ainda nessa etapa, o botão "Carregar imagem mais recente disponível" foi adicionado para agilizar o monitoramento da AOI. Ao acioná-lo, o restante dos parâmetros de configuração é definido com valores padrão e a busca de imagens é executada. Em seguida, a imagem multiespectral mais recente disponível, com composição em cor verdadeira, e sua respectiva imagem NDVI são carregadas automaticamente.
Adicionalmente, nesta etapa, foi implementada a funcionalidade de obter Modelos Digitais de Elevação (MDE), de múltiplos fonte de dados disponibilizados no catálogo do GEE, permitindo o download do arquivo de altimetria com resolução espacial de até 30 metros recortado para os limites da AOI.

![Tela de seleção da AOI — Passo 3: Seleção da Área de Interesse e verificação do limite de 120 km²](medias/medias_pt/step3.png)

Figura 3 — Interface do Passo 3 do complemento RAVI. Exibe o contorno da AOI com indicação do limite máximo permitido (120 km²) e aviso caso seja excedido; inclui o botão "Carregar imagem mais recente disponível" para preenchimento automático dos parâmetros e busca imediata da cena multiespectral e do NDVI, além das opções de obtenção de Modelos Digitais de Elevação (MDE) a partir de múltiplas fontes do catálogo do GEE.

## 4. Seleção do Intervalo de Tempo (Passo 4)

A definição do período para a busca de imagens Sentinel-2 atende a um requisito do GEE e facilita o uso pelo usuário, oferecendo opções com intervalos predefinidos (últimos 3, 6, 12 meses, etc.) e uma caixa de seleção para inserir as datas exatas de início e fim. A seleção padrão corresponde ao intervalo dos últimos 3 meses, mantendo o tempo de processamento reduzido. Selecionar apenas o período de interesse pode, ainda, reduzir o tempo de espera na busca e no processamento das imagens. No entanto, é importante notar que a geração global sistemática e operacional de produtos de Nível 2A, utilizada neste trabalho, está em andamento desde 13 de dezembro de 2018 (ESA, 2025).

![Tela de seleção do Intervalo de Tempo — Passo 4: Seleção do período para busca de imagens](medias/medias_pt/step4.png)

Figura 4 — Interface do Passo 4 do complemento RAVI. Apresenta intervalos predefinidos (ex.: últimos 3, 6, 12 meses), campos para inserir datas de início e fim, e seleção padrão para os últimos 3 meses, permitindo ao usuário reduzir o tempo de busca e processamento ao restringir o período de interesse.

## 5. Seleção do Índice de Vegetação (Passo 5)

A interface de seleção de IV inclui uma gama de índices predefinidos (Tabela 1), acompanhados de um breve texto explicativo para cada. Essas explicações, que incluem a fórmula matemática de cada IV e a descrição de suas principais aplicações, foram desenvolvidas em Linguagem de Marcação de Hipertexto (HTML). Além dos índices predefinidos, é possível criar índices personalizados com a construção de expressões matemáticas entre as bandas espectrais disponíveis e um conjunto de operadores e funções. A documentação adicional disponível dentro do complemento pode ser consultada para mais detalhes sobre como desenvolver os índices personalizados. O índice selecionado será utilizado para o cálculo do perfil temporal da AOI, e os resultados serão exibidos graficamente em “Painel A”.

![Tela de seleção do Índice de Vegetação — Passo 5: Escolha de índices e criação de índices personalizados](medias/medias_pt/step5.png)

Figura 5 — Interface do Passo 5 do complemento RAVI. Permite selecionar índices predefinidos, consultar a descrição e a fórmula em HTML, além de criar índices personalizados por meio de expressões entre bandas; o índice selecionado é utilizado no cálculo do perfil temporal (Painel A).
 
### Tabela 1 – Índices de vegetação implementados no complemento RAVI
| Nome | Sigla | Fórmula | Citação Original (Autor, Ano) |
|------|-------|---------:|----------------------------------|
| Normalized Difference Vegetation Index | NDVI | (NIR - RED) / (NIR + RED) | Rouse et al. (1974) |
| Green Normalized Difference Vegetation Index | GNDVI | (NIR - GREEN) / (NIR + GREEN) | Gitelson et al. (1996) |
| Enhanced Vegetation Index | EVI | 2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1)) | Huete et al. (1999) |
| Enhanced Vegetation Index 2 | EVI2 | 2.5 * ((NIR - RED) / (NIR + RED + 1)) | Jiang et al. (2008) |
| Soil-Adjusted Vegetation Index | SAVI | (1 + L) * ((NIR - RED) / (NIR + RED + L)) | Huete (1988) |
| Modified Soil-Adjusted Vegetation Index | MSAVI | (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - RED))) / 2 | Qi et al. (1994) |
| Structurally Focused Difference Vegetation Index | SFDVI | ((NIR + GREEN) - (RED + REDEDGE)) / 2 | Baptista (2015) |
| Chlorophyll Index Green | CIgreen | NIR / GREEN - 1 | Gitelson et al. (2003) |
| Normalized Difference Red Edge | NDRE | (NIR - REDEDGE) / (NIR + REDEDGE) | Gitelson & Merzlyak (1994) |
| Atmospherically Resistant Vegetation Index | ARVI | (NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE)) | Kaufman & Tanré (1992) |
| Normalized Difference Moisture Index | NDMI | (NIR - SWIR) / (NIR + SWIR) | Gao (1996) |
| Normalized Burn Ratio | NBR | (NIR - SWIR) / (NIR + SWIR) | Key & Benson (1999) |
| Structure Insensitive Pigment Index | SIPI | (NIR - BLUE) / (NIR - RED) | Peñuelas et al. (1995) |
| Normalized Difference Water Index | NDWI | (GREEN - NIR) / (GREEN + NIR) | McFeeters (1996) |
| Red Edge Chlorophyll Index | ReCI | NIR / REDEDGE - 1 | Gitelson et al. (2003) |
| MERIS Terrestrial Chlorophyll Index | MTCI | (NIR - REDEDGE) / (REDEDGE - RED) | Dash & Curran (2004) |
| Modified Chlorophyll Absorption Ratio Index | MCARI | ((REDEDGE - RED) - 0.2 * (REDEDGE - GREEN)) * (REDEDGE / RED) | Daughtry et al. (2000) |
| Visible Atmospherically Resistant Index | VARI | (GREEN - RED) / (GREEN + RED - BLUE) | Gitelson et al. (2002) |
| Triangular Vegetation Index | TVI | 0.5 * (120 * (NIR - GREEN) - 200 * (RED - GREEN)) | Broge & Leblanc (2001) |

## 6. Filtro de Sobreposição de Imagens (Passo 6)

As imagens Sentinel-2 Nível 2A são disponibilizadas em cenas de 10.000 km² (100 km x 100 km) e podem não cobrir completamente a AOI, inviabilizando certas análises. Como a função de busca do GEE não realiza filtragem que mensura a proporção da AOI coberta pela cena, implementou-se, portanto, um filtro adicional. Esse filtro calcula a porcentagem de sobreposição por meio da razão entre a área em comum e a área total da AOI, assegurando que cada cena cubra adequadamente a AOI. 

O cálculo da sobreposição é realizado por funções específicas da API do GEE, que determinam a área comum entre o contorno da AOI e a extensão espacial de cada imagem candidata. Dessa forma, apenas imagens cuja porcentagem de sobreposição seja igual ou superior ao limiar definido são mantidas. Definiu-se um limiar padrão de 90% para recomendar que análises iniciais apresentem alto grau de sobreposição com a AOI. No entanto, é importante mencionar que AOIs grandes ou irregulares podem dificultar a busca por imagens que atinjam um limiar elevado, uma vez que a cobertura integral de áreas extensas ou complexas é incomum. Dessa forma, o valor de sobreposição ajustável oferece ao usuário um mecanismo para equilibrar a qualidade dos dados e a disponibilidade de cenas, otimizando a seleção conforme o tamanho e o formato da AOI.



## 7. Opções de Buffer (Passo 7)

Este recurso foi implementado para permitir que o usuário redefina os contornos de sua AOI, especificando uma distância, em metros, para expandir (positivo) ou contrair (negativo) os contornos da área. Um buffer negativo reduz a área e, assim, os efeitos de borda, como a presença de carreadores, enquanto que um positivo expande para capturar o contexto e pode permitir ajustes futuros por parte do usuário no próprio QGIS. 

A nova geometria é empregada em todas as funcionalidades, como nas funções de perfil temporal e de download de imagem, assegurando que as análises e os dados gerados considerem a AOI modificada. Por padrão, nenhum buffer é aplicado; a decisão de usá-lo cabe ao usuário. Essa redefinição ocorre em cópia dos contornos em memória do GEE e não afeta os arquivos originais.

## 8. Filtro de Nuvem na Cena (Passo 8)

A presença de nuvens é uma causa significativa de ruído em cenas Sentinel-2. Para reduzir esse ruído e proporcionar ao usuário controle sobre os resultados obtidos pelo complemento, este filtro foi implementado para permitir que ele defina um limite percentual máximo de cobertura de nuvens mais adequado às suas análises. 

Essa filtragem é realizada por meio de um indicativo de qualidade já presente no metadado de cada imagem da coleção (CLOUDY_PIXEL_PERCENTAGE), que representa uma estimativa da cobertura percentual de nuvens em toda a extensão da cena, de 10.000 km². Dessa forma, apenas as cenas cuja porcentagem de cobertura por nuvens em toda a cena seja igual ou inferior ao limite definido pelo usuário são mantidas na coleção para as etapas subsequentes do processamento. Dessa forma, o filtro será mais rigoroso quando definido em 0%, restringindo a coleção a imagens completamente livres de nuvens, e menos rigoroso em 100%, caso a cobertura de nuvens não seja avaliada. O valor padrão foi definido em 40%.

## 9. Filtro de Classificação de Cena (Passo 9)

O filtro implementado no Passo 9 representa uma tentativa de aprimorar a filtragem de imagens com presença de nuvens, de forma mais contextualizada em relação à AOI, por meio de dados da camada SCL. Dessa forma, a acurácia dessa funcionalidade depende inteiramente da confiabilidade da camada SCL original fornecida pela ESA, o que sabidamente apresenta limitações.
O algoritmo opera sobre a coleção de imagens de entrada, utilizando a seleção das classes de pixel, para definir a lista de identificadores SCL considerados "inválidos”. O processo é executado para cada imagem da coleção: uma máscara booleana é gerada para a AOI, identificando os pixels como válidos ou inválidos. Em seguida, o sistema contabiliza o número total de pixels válidos (pela soma dos valores da máscara) e o número total de pixels contidos na AOI. A razão percentual de pixels válidos (válidos/total) é então calculada e anexada a cada imagem como nova propriedade. Por fim, aplica-se à coleção a retenção apenas das imagens cuja nova propriedade seja maior ou igual ao limiar definido pelo usuário, resultando em uma nova coleção filtrada.
Opcionalmente, é possível ativar a opção "Aplicar máscara SCL para remover pixels". Quando habilitada, essa função utiliza a máscara booleana para definir como nulos (NoData) todos os pixels classificados como "inválidos". Essa operação de mascaramento é propagada para todos os processamentos subsequentes.
A interface do filtro permite ao usuário definir quais classes SCL devem ser consideradas para retirada da cena (inválidas), por exemplo, nuvens e sombras de nuvens, e estabelecer um limiar de aceitação em percentual total. Esse limiar define a proporção mínima de pixels "válidos" que uma imagem deve conter na AOI para ser mantida na coleção.
Dessa forma, a filtragem é mais rigorosa quando ajustada em 100% e sem efeito quando ajustada em 0%. O valor padrão deste filtro é de 80%, o que implica o descarte de imagens com mais de 20% de pixels inválidos na AOI. Este valor, combinado com o valor padrão do filtro de nuvens em cena descrito no item anterior, apresenta desempenho médio na eliminação de ruído por nuvens e será discutido em maior detalhe em uma seção posterior. Recomenda-se que os usuários explorem alternativas de configuração de acordo com suas necessidades.

## 10. Filtro de Imagem Única

O filtro de imagem única foi implementado para eliminar redundâncias decorrentes de múltiplas cenas quase idênticas adquiridas pela constelação Sentinel‑2 em um mesmo instante orbital, com diferença de frações de segundos entre si, que não agregam informação adicional, mas aumentam o volume de dados e o tempo de processamento. 
O complemento identifica e agrupa essas imagens equivalentes, mantendo apenas uma cena representativa por data de aquisição, selecionada com base em critérios hierárquicos: primeiramente, conserva-se a imagem com maior percentual de cobertura da Área de Interesse (AOI), calculado conforme o filtro de sobreposição de imagens (Passo 6); caso haja igualdade nessa métrica, a imagem mais recente é priorizada. Esse procedimento é executado automaticamente sem necessidade de configuração pelo usuário, garantindo que a coleção final retenha apenas uma imagem por data efetiva, o que reduz redundâncias, otimiza o desempenho do complemento e assegura maior coerência temporal às análises subsequentes.

## 11 Visão Geral

Esta aba da interface foi desenvolvida para oferecer um resumo das opções de entrada de dados e configurações do RAVI, consolidando as abas anteriores em uma única janela, que permite revisar o conjunto de configurações possíveis. Usuários recorrentes podem utilizar o botão “Pular Etapas”, localizado no Passo 3, para acessar diretamente a visão geral e realizar as configurações diretamente nela.

### 2 FUNCIONALIDADES ACESSÍVEIS NA ABA PAINEL 

Após a inserção dos dados e das configurações, ao clicar em “Executar análises” na aba “Visão Geral”, inicia-se o processamento no GEE e, após o retorno dos resultados ao QGIS, a aba “Painel” é habilitada. As opções disponíveis na aba “Painel” foram categorizadas de “A” a “H” (Figura 6) para fins de identificação e descrição nos próximos itens. 

Figura 6:  Interface da aba 'Painel' do complemento RAVI, com a localização das principais funcionalidades de análise e exportação
 
A aba 'Painel' atua como um centro de controle interativo por meio de interações do tipo “apontar e clicar” do usuário com o complemento e instrui um fluxo de envio de requisições para processamento em nuvem no GEE, o retorno dos resultados para visualização no QGIS e/ou armazenamento no sistema local (Figura 7). Os itens a seguir detalham cada uma dessas funcionalidades.

Figura 7:  Diagrama de fluxo das funcionalidades da aba 'Painel', ilustrando a interação entre o QGIS, o GEE e o sistema do usuário
 
## 2.1 Perfil Temporal de IV (Painel A)

O perfil temporal de IV decorre da coleção resultante da busca por imagens. O IV desejado é calculado por pixel, por meio de operações aritméticas mapeadas à coleção (com a função map() do GEE, usada para aplicar operações a cada imagem de uma ee.ImageCollection, aproveitando o processamento paralelo em nuvem). Em seguida, para cada imagem, o valor médio do IV para a AOI é calculado por um redutor de média (no GEE, um redutor (ee.Reducer) é uma classe usada para agregar dados em várias dimensões, incluindo tempo, espaço, bandas dentro de uma imagem ou atributos dentro de uma ee.FeatureCollection).
Esses valores calculados são agregados à coleção como propriedades associadas a cada imagem. A extração desses dados ocorre por meio de requisições assíncronas, que retornam os valores em listas estruturadas. Posteriormente, essas listas são convertidas em formato de dataframe, uma estrutura de dados tabular da biblioteca Pandas, empregada para facilitar a manipulação das informações.
Uma vez estruturados, os dados são processados e preparados para exibição gráfica por meio de recursos da biblioteca Plotly, que possibilita a criação de visualizações interativas e dinâmicas. A renderização dessas visualizações é realizada com o uso do widget QWebView, componente do Qt Design que emula um navegador de internet integrado ao próprio complemento.

## 2.2 Visualização e Download de Imagens em Data Específica (Painel B)

Cada ponto do perfil temporal do IV, exibido no “Painel A”, corresponde a uma data com imagem disponível na coleção resultante da busca. Essa funcionalidade tem como foco habilitar o download e a visualização das imagens multiespectrais (com composição de cor verdadeira) dos índices de vegetação selecionados, na data selecionada. Esse processo gera e transfere dados GeoTIFF, que podem ser armazenados opcionalmente na máquina dos usuários e visualizados no QGIS.
Para camadas multiespectrais, o complemento solicita ao GEE o download do arquivo já recortado ao contorno da AOI e, em seguida, o carrega no QGIS como camada do projeto para visualização. Um padrão predefinido é aplicado para mapear as bandas, com ajuste de contraste, em composição de cor verdadeira. 
No caso de camadas de IV, o complemento envia as instruções de cálculo ao GEE por meio de expressões aritméticas, exporta o arquivo e aplica a renderização de banda simples em falsa cor, utilizando a paleta de cores predefinida para otimizar a visualização. A seleção do índice para esse recurso não está limitada ao índice exibido no gráfico do perfil temporal, e pode ser alternada para qualquer IV disponível na caixa de seleção.
O complemento assegura que o GeoTIFF seja tratado como temporário, na opção de visualização, salvando os arquivos na pasta temporária do sistema operacional, ou, na opção de download, no diretório selecionado no Passo 2. O processo é acionado como descrito por imagem individual ou em lote, caso em que é aplicado a todas as imagens disponíveis automaticamente.

### 2.3 Opções de Imagem Sintética (Painel C)

A imagem sintética é gerada por meio da agregação pixel a pixel da coleção de imagens, do valor do IV ao longo do perfil temporal. A imagem resultante representa a métrica definida (média, máximo, etc.) calculada sobre a pilha de pixels em um mesmo local, em toda a AOI. O resultado é uma imagem composta (sintética) que derivada dos padrões temporais agregados, de acordo com a métrica selecionada, e é exportada localmente e visualizada, com renderização de banda simples em falsa cor, de forma análoga à funcionalidade do “Painel B”.

### 2.4 Opções de Remoção De Datas (Painel D)

A seleção de datas é realizada em uma interface interativa que permite escolher manualmente as observações temporais a serem incluídas em todas as outras análises que envolvem o conjunto de imagens da coleção. O usuário pode filtrar o perfil temporal removendo datas indesejadas ou selecionando períodos específicos por meio de caixas de seleção. Essas caixas são organizadas hierarquicamente por ano e mês, em que cada data disponível no perfil temporal possui uma caixa individual, e há caixas adicionais para seleção agregada nos níveis de mês e de ano. Essa seleção tem como objetivo filtrar as datas exibidas no “Painel A” e não altera a coleção do GEE, exceto quando novos cálculos sobre a coleção forem acionados pelos “Painel C” ou “H”.

### 2.5 Opções de Filtro Savitzky-Golay (Painel E)

O filtro Savitzky-Golay foi implementado para a reconstrução suavizada do perfil de IV da série temporal (Painel A), reduzindo alterações abruptas (ruído) enquanto preserva características relevantes, como picos e tendências. Ele é aplicado por meio da biblioteca SciPy, que ajusta polinômios locais aos dados em uma janela deslizante. A ordem do polinômio e o tamanho da janela são configuráveis da interface e controlam o grau de suavização resultante no perfil temporal exibido no “Painel A”, sobreposto ao perfil original, o que permite a comparação. A configuração padrão foi definida para que a suavização seja o mais tênue possível.

### 2.6 Opções de dados NASA POWER (Painel F)

Esta funcionalidade foi implementada para integrar dados climáticos à análise de perfis temporais de IV. Quando acionada, uma requisição é enviada à API Python NASA POWER, utilizando a latitude e a longitude do centroide da AOI, além do intervalo de datas, como parâmetros. Os dados retornados incluem a precipitação e as temperaturas mínimas e máximas diárias, organizados em um dataframe. 
O complemento organiza os dados de precipitação em acumulados mensais e atualiza o “Painel A”, exibindo gráficos de barras sobrepostos para apresentar a precipitação sobreposta ao perfil temporal de IV. Embora apenas os dados de precipitação sejam exibidos graficamente, as temperaturas mínimas e máximas também constam nos dados tabulados disponíveis para exportação.

### 2.7 Opções para exportar dados tabulares (Painel G)

Os valores do gráfico do perfil temporal no “Painel A” podem ser exportados diretamente em formato tabular. A imagem do gráfico também pode ser salva, desde que seja aberta em um navegador de internet externo instalado no computador. Isso foi implementado porque o widget QWebView, embora simule um navegador integrado ao complemento, não possui todos os recursos necessários para realizar o download direto. No entanto, abrir o gráfico em um navegador pode ser vantajoso, pois permite ajustes manuais nas dimensões.

### 2.8 Opções para Alternar IV e Focar em Área (Painel H)

Esta funcionalidade foi desenvolvida para otimizar o processamento computacional em alguns fluxos de trabalho específicos, como a exploração dos diferentes IV disponíveis, ao evitar o reprocessamento dos filtros e preservando qualquer seleção de datas aplicada anteriormente. Exemplo de uso: Usuário obtém uma série temporal NDVI para uma AOI (fazenda) e após inspecionar algumas imagens decide removê-las da série temporal por conta de ruídos observados; em seguida gostaria de obter nova série temporal com outro índice, mantendo a seleção de imagem já aprimorada manualmente; para isso, faz uso desta funcionalidade. Além disso, é possível utilizá-la para obter um novo perfil temporal de uma subdivisão da AOI original (como um talhão), ao selecionar o contorno do talhão e executar o novo cálculo com a coleção de imagens existente (sem necessidade de nova busca de imagens e processamento de filtros), o que reduz tempo de espera pelos dados processados.


### 3 Análise Multifeição

As funcionalidades "Análise de Multifeição" e "Análise de Pontos" foram implementadas para possibilitar a análise comparativa de perfil temporal de diferentes regiões em múltiplas escalas. São recursos disponibilizados em abas individuais da interface, acessíveis após a disponibilização e operação do "Painel", e operam de forma análoga ao cálculo de perfis temporais em toda a AOI no "Painel A".

Na "Análise Multifeição", a AOI deve ser uma camada vetorial do tipo multipolígono, contendo um campo na tabela de atributos para identificação individual de cada polígono (feição). Ao executar essa análise, o complemento utiliza um recurso do QGIS para dividir as feições, armazenando-as individualmente em memória temporária, e processar cada uma como uma nova AOI, tendo seu perfil temporal calculado e exibido sobreposta, com legendas identificadoras.

### 4 Análise de Pontos

Para a "Análise de Pontos", foi implementado um recurso de captura de coordenadas, ativado ao clique do usuário no mapa do QGIS. Ao ser ativado, o recurso permite ao usuário clicar no mapa e o complemento captura a coordenada geográfica, adiciona um marcador com cor aleatória e define uma nova AOI circular cuja área contém um pixel. A cada clique, um novo perfil temporal é calculado para a nova AOI gerada e adicionado ao gráfico, em cor correspondente ao marco adicionado ao mapa e utilizando as coordenadas como identificador na legenda. O gráfico da AOI original também é exibido para comparação, e há um botão que permite reiniciar a análise e remover os marcadores.