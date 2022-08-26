/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the MODIS data based on user inputs
and performes the scaled NDVI (VCI) computation.

USES:
    - seasonal_filter.js
    - monthly_composites.js

Note: Load the ROI, here it uses "Zambia" as a featureCollection.
*/

// MODULES DECLARATION -----------------------------------------------------------
//seasonal filter
var seasonalFilter = require("users/Plottings/drought_dataset:dataset/seasonal_filter.js")
//monthly composites
var monthlyComposites = require('users/Plottings/drought_dataset:dataset/monthly_composites.js')
//


// Filter image collection by roi and date --------------------------------------------------------------
var terra_NDVI = ee.ImageCollection ("MODIS/006/MOD13Q1") 
var aqua_NDVI = ee.ImageCollection("MODIS/006/MYD13Q1")   

// Combine Terra and Aqua MODIS NDVI Image Collections
var modis_NDVI = terra_NDVI.merge(aqua_NDVI) 
                       .filterBounds(Zambia) 
                       .select('NDVI')           // 960
var Col =  seasonalFilter.Season(modis_NDVI)     //79 images

// Display the image collection from January 2016
var ndviVis = {min: 0.0, max: 8000.0, 
               palette: ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', 
                         '99B718', '74A901','66A000', '529400', '3E8601', 
                         '207401', '056201', '004C00', '023B01','012E01', 
                         '011D01', '011301']}
Map.centerObject(Zambia, 6)
Map.addLayer(Col.first().clip(Zambia), ndviVis, 'Jan, 2016');


// Compute monthly avg, min, and max -------------------------------------------------------------------
var monthly_avg =  monthlyComposites.monthly_Avg(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_avg) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_avg)

// Display sum, min, and max ET images from 2016
Map.addLayer(monthly_avg.first().clip(Zambia), ndviVis, 'Jan_avg, 2016');
Map.addLayer(monthly_min.first().clip(Zambia), ndviVis, 'Jan_min, 2016');
Map.addLayer(monthly_max.first().clip(Zambia), ndviVis, 'Jan_max, 2016');


// Compute VCI -------------------------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

var VCI = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_avg.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
                                    
    var avgNDVI = ee.Image(filtered.first())
    var minNDVI = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                      .first())
    var maxNDVI = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                      .first())
                            
    var image = ee.Image.cat([avgNDVI, minNDVI, maxNDVI])
                        .rename(['avgNDVI', 'minNDVI', 'maxNDVI'])
    // VCI = (NDVI - min) / (max - min)
    return image.expression('(avgNDVI - minNDVI) / (maxNDVI - minNDVI)',
    {'avgNDVI': image.select('avgNDVI'),
    'minNDVI': image.select('minNDVI'),
    'maxNDVI': image.select('maxNDVI')
      
    }).rename('VCI')
      .set({'month': month, 'year': year});
  });
}).flatten());


// Display VCI index from January 2016
var vciPalette = ['#a50026','#d73027','#f46d43','#fdae61',
                  '#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837'];
var vciVisParams = {min: 0, max: 1, palette: vciPalette}
Map.addLayer(VCI.first().clip(Zambia), vciVisParams, 'VCI: Jan, 2016');


// Export the data ----------------------------------------------------------------------
var listOfImages = VCI.toList(VCI.size());
var firstImage = ee.Image(listOfImages.get(0));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'VCI',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
