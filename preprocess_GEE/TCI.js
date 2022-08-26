/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the MODIS data based on user inputs
and performes the scaled LST (TCI) computation.

USES:
    - seasonal_filter.js
    - monthly_composites.js

Note: Load the ROI, here it uses "Zambia" as a featureCollection.
*/

// MODULES DECLARATION ---------------------------------------------------------------------------
//seasonal filter
var seasonalFilter = require("users/Plottings/drought_dataset:dataset/seasonal_filter.js")
//monthly composites
var monthlyComposites = require('users/Plottings/drought_dataset:dataset/monthly_composites.js')
//


// Import Terra and Aqua MODIS LST Image Collections----------------------------------------------
var terra_LST = ee.ImageCollection("MODIS/006/MOD11A1")
var aqua_LST = ee.ImageCollection("MODIS/006/MYD11A1") 

// Combine Terra and Aqua MODIS LST Image Collections
var modis_LST = terra_LST.merge(aqua_LST) 
                       .filterBounds(Zambia) 
                       .select('LST_Day_1km') // 15197
                       
var Col =  seasonalFilter.Season(modis_LST)   //1225               
                       
// Display the image collection from 2016
var lstVis = {min: 13000.0, max: 16500.0, palette: [
    '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
    'ff0000', 'de0101', 'c21301', 'a71001', '911003'
  ],
};

Map.centerObject(Zambia, 6)
Map.addLayer(Col.first().clip(Zambia), lstVis, 'LST')

// Compute monthly sums, min, and max -------------------------------------------------------------------
var monthly_avg =  monthlyComposites.monthly_Avg(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_avg) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_avg)

// Display sum, min, and max ET images from January 2016
Map.addLayer(monthly_avg.first().clip(Zambia), lstVis, 'Jan_avg, 2016');
Map.addLayer(monthly_min.first().clip(Zambia), lstVis, 'Jan_min, 2016');
Map.addLayer(monthly_max.first().clip(Zambia), lstVis, 'Jan_max, 2016');


// Compute the TCI ----------------------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

var TCI = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_avg.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
    var avgLST = ee.Image(filtered.first())
    var minLST = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                     .first())
    var maxLST = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                     .first())

    var image = ee.Image.cat([avgLST, minLST, maxLST])
                        .rename(['avgLST', 'minLST', 'maxLST'])
    // TCI = (max - avgLST) / (max - min)
    return image.expression('(maxLST - avgLST) / (maxLST - minLST)',
    {'avgLST': image.select('avgLST'),
    'minLST': image.select('minLST'),
    'maxLST': image.select('maxLST')
      
    }).rename('TCI')
      .set('month', month).set('year', year);
  });
}).flatten());


// Display TCI index from January 2016
var tciVis = {min: 0.0, max: 1.0, palette: [
    '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
    'ff0000', 'de0101', 'c21301', 'a71001', '911003'
  ],
};

Map.addLayer(TCI.first().clip(Zambia), tciVis, 'TCI: Jan, 2016');


// Export the data ---------------------------------------------------------------------------------------
var listOfImages = TCI.toList(TCI.size());
var firstImage = ee.Image(listOfImages.get(0));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'TCI',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
