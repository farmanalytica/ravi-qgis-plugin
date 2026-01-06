//Original SYSI code by Gabriel Capucci


// Alteração no ndvi -> melhor pois diminuiu a perda 
//#var shape = ee.FeatureCollection('...');
var aoi2 = shape.geometry().bounds();  // Definindo a variável aoi2
Map.centerObject(aoi2, 14);  // Centraliza o mapa com a área de interesse (aoi2)

/*------------------------- Mascara QA_PIXEL para o Sentinel-2  -----------------------*/

function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask);
}

var s2_names = ['B2', 'B3', 'B4', 'B6', 'B8','B11','B12','QA60'];
var b_names = ['blue', 'green', 'red','rededge', 'nir', 'swir1', 'swir2', 'QA60'];


/*------------------- Dataset of Sentinel 2 -------------------*/

var dataset_s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    //.filterDate('2006-08-01', '2006-10-01') // To get all images this filter wont be used
    .filterBounds(aoi2)  // Usando aoi2 para filtrar as imagens
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',10)) // Get less pixels of Cloud
    .filter(ee.Filter.lt('WATER_PERCENTAGE',2)) // Get less pixels of Water
//    .filter(ee.Filter.lt('VEGETATION_PERCENTAGE',30)) // Get less pixels of Vegetation
    .map(maskS2clouds)
    .map(function(image){return image.clip(aoi2)})  // Recorta para a área de interesse (aoi2)
    .select(s2_names, b_names);
    
print("Coleção de imagens do sentinel 2:", dataset_s2);

/*------------------- GEOS3 indexes  ---------------- */

var add_indexes = function(img){
  var ndvi = img.normalizedDifference(['nir', 'red']); // Normalized Difference vegetation index
  var nbr2 = img.normalizedDifference(['swir1', 'swir2']); // Normalized Difference Burn Ratio 2
  var grbl = img.select('green').subtract(img.select('blue')); // Difference between green and blue
  var regr = img.select('red').subtract(img.select('green')); // Difference between red and green
  
  img = img.addBands(ndvi.rename('ndvi')).addBands(nbr2.rename('nbr2')).addBands(grbl.rename('grbl')).addBands(regr.rename('regr'));
 
  return img ;
};

var s2_indexes = dataset_s2.map(add_indexes);

print('Dataset S2 com os indices: ',s2_indexes);


/*------------------- Applying scale factors ---------------- */

function applyScaleFactors(image) {
  var opticalBands = image.select(b_names).divide(10000);
  return image.addBands(opticalBands, null, true);
}

s2_indexes = s2_indexes.map(applyScaleFactors);

var sent_collection = s2_indexes;


/*------------------- Applying the temporal filter (months) ------------------*/

var sent_collection_maio_a_setembro = sent_collection.filter(ee.Filter.calendarRange(1, 12, 'month'));

print('Dataset unidos (entre maio e setembro): ', sent_collection_maio_a_setembro)


/*------------------- Aplicação da mascara GEOS3 ---------------- */

var addGEOS3Mask = function(img, options) {
 var rescale_flag = options.rescale_flag || 0;
 var ndvi_thres = options.ndvi_thres || [-0.25, 0.25];
 var nbr_thres = options.nbr_thres || [-0.3, 0.1];
 var vnsir_thres = options.vnsir_thres || 0.9;

 if (rescale_flag === 1) {
    img = img.divide(10000); // rescale to [0,1] reflectance to sentinel
 }

 // Visible-toshortwave-infrared tendency index - NÃO ESTA NO ARTIGO
 var vnsir = ee.Image(1)
              .subtract(ee.Image(2).multiply(img.select('red'))
                                             .subtract(img.select('green')).subtract(img.select('blue'))
              .add(ee.Image(3).multiply(img.select('nir').subtract(img.select('red')))));
              
 // GEOS3 "equation"
 var geos3 = img.select('ndvi').gte(ndvi_thres[0]).and(img.select('ndvi').lte(ndvi_thres[1]))            // NDVI conditions
              .and(img.select('nbr2').gte(nbr_thres[0]).and(img.select('nbr2').lte(nbr_thres[1])))       // NBR conditions
              .and(vnsir.lte(vnsir_thres))                                                               // VISNIR condition
              .and(img.select('grbl').gt(0)).and(img.select('regr').gt(0));                              // Bands difference conditions
              
 img = img.addBands(geos3.rename('GEOS3'));            
  
 return img; // Return the image where the band 'GEOS3' is the bare soil pixel stack
 };
 
// Appling the GEOS 3 mask for the collection 

sent_collection = sent_collection.map(function(img) {
 return addGEOS3Mask(img, {rescale_flag: 0, ndvi_thres: [-0.25, 0.25], nbr_thres: [-0.3, 0.100], vnsir_thres: 0.9});
});

function maskByGEOS3(image) {
 // Define a threshold for atmospheric opacity. Pixels with opacity greater than this value will be masked.
  
 // Create a mask that is true (1) for pixels with opacity equal to the threshold.
 var mask_geos3 = image.select('GEOS3').eq(1);
 
 // Create a mask that is true (1) for pixels with opacity equal to the threshold.
 var mask_swir = image.select('swir2').gte(0);// Removing black lines
 var mask_green = image.select('green').gte(0);// Removing black lines
 var mask_red = image.select('red').gte(0); // Removing black lines
 var mask_blue = image.select('blue').gte(0); // Removing black lines
 
 var mask = mask_geos3.and(mask_swir).and(mask_green).and(mask_red).and(mask_blue);

 // Apply the mask to the image.
 return image.updateMask(mask);
}

function maskByndvi(image) {
 // Define a threshold for atmospheric opacity. Pixels with opacity greater than this value will be masked.

 var mask_ndvi_v1 = image.select('ndvi').gte(0.00); // Removing white lines
 var mask_ndvi_v2 = image.select('ndvi').lte(0.20); // Removing ciliar forest
 
 var mask = mask_ndvi_v1.and(mask_ndvi_v2);

 // Apply the mask to the image.
 return image.updateMask(mask);
}


/*------------------- Get the pixel median -> TESS  ---------------- */

var tess_v1 = sent_collection.map(maskByGEOS3)

var ndvi = ui.Chart.image.series({
  imageCollection: tess_v1.select(['ndvi']),
  region: aoi2,  // Usando aoi2 para definir a região
  reducer: ee.Reducer.mean(),
  scale:10,
  xProperty: 'system:time_start'})
  .setOptions({
     title: 'NDVI ao longo do tempo (Pós mascara GEOS3)',
     vAxis: {title: 'NDVI'}});

print(ndvi)

tess_v1 = tess_v1.median()

var tess_v2 = maskByndvi(tess_v1)

/*------------------- Synthetic Soil Image (SYSI)  ---------------- */
//Is the TESS for the aoi

var visualization = {
  bands: ['red', 'green', 'blue'], // RGB
  min: 0.0,
  max: 0.3,
};

var visualization_f = {
  bands: ['swir1','nir','red'], // 6-5-4
  min: 0.0,
  max: 0.3,
};

var land_composite = sent_collection.median();
Map.addLayer(land_composite, visualization, 'Sentinel 2 - Composição de cor verdadeira',false);
Map.addLayer(tess_v1, visualization ,'Synthetic Soil Image (SYSI) - Version 1',false);
Map.addLayer(tess_v2, visualization_f ,'Synthetic Soil Image (SYSI) - Version 2');
Map.addLayer(tess_v1, visualization_f ,'Synthetic Soil Image (SYSI) - Version 1');
Map.addLayer(shape,{color:'Blue'},"Pontos de amostragem");

// Export generated composite results.
Export.image.toDrive({
  image: tess_v1.select(['blue','green','red','rededge','nir','swir1','swir2','ndvi']).toFloat(),
  description:'sentinel_geos3',
  fileNamePrefix: 'sentinel_geos3',
  folder:'Bare_soil',
  region: aoi2,  // Usando aoi2 para exportar
  crs: 'EPSG:4326',
  scale: 10,
  maxPixels:1e13
});

// Função para calcular a média das bandas NIR e Red para cada polígono
function calculateMean(image, region) {
  var mean = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: region,
    scale: 30,
    maxPixels: 1e8
  });
  return mean;
}

var regionOfInterest = aoi2;  // Usando aoi2 como região de interesse

var meanValues = calculateMean(tess_v1, regionOfInterest);
print('Mean values: ', meanValues);
