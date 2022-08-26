/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the NASA-USDA soil moisture data based on user inputs
and performes the monthly computation of ssm.

This dataset is available from 2015 only. 

USES:
    - seasonal_filter.js
    - monthly_composites.js

Note: Load the ROI, here it uses "Zambia" as a featureCollection.
*/

// MODULES DECLARATION ---------------------------------------------------------------------------------
//seasonal filter
var seasonalFilter = require("users/Plottings/drought_dataset:dataset/seasonal_filter.js")
//monthly composites
var monthlyComposites = require('users/Plottings/drought_dataset:dataset/monthly_composites.js')
//


// Filter image collection by roi, and date ------------------------------------------------------------
var soilMoisture = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture')
                .filterBounds(Zambia)
                .select('ssm');
var Col = seasonalFilter.Season(soilMoisture);    


// Display the image collection from 2016
Map.centerObject(Zambia, 6)
var smVis = {min: 0.0, max: 28.0, palette: ['0300ff', '418504','efff07', 'efff07', 'ff0303']};
Map.addLayer(Col.first().clip(Zambia), smVis, 'Jan, 2016');


// Compute monthly sums, min, and max -------------------------------------------------------------------
var monthly_avg =  monthlyComposites.monthly_Avg(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_avg) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_avg)

// Display sum, min, and max ET images from 2016
Map.addLayer(monthly_avg.first().clip(Zambia), smVis, 'Jan_avg, 2016');
Map.addLayer(monthly_min.first().clip(Zambia), smVis, 'Jan_min, 2016');
Map.addLayer(monthly_max.first().clip(Zambia), smVis, 'Jan_max, 2016');

// Compute the SMCI --------------------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);
var SMCI = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_avg.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
                                    
    var avgSM = ee.Image(filtered.first())
    var minSM = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                    .first())
    var maxSM = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                    .first())
                            
    var image = ee.Image.cat([avgSM, minSM, maxSM])
                        .rename(['avgSM', 'minSM', 'maxSM'])
    // SMCI = (SM - min) / (max - min)
    return image.expression('(avgSM - minSM) / (maxSM - minSM)',
    {'avgSM': image.select('avgSM'),
    'minSM': image.select('minSM'),
    'maxSM': image.select('maxSM')
      
    }).rename('SMCI')
      .set({'month': month, 'year': year});
  });
}).flatten());

// Display the SMCI index from January 2016
var smciVisParams = {min: 0, max: 1, palette: ['0300ff', '418504','efff07', 'efff07', 'ff0303']}
Map.addLayer(SMCI.first().clip(Zambia), smciVisParams,'SMCI Jan 2016');

// Export the data -------------------------------------------------------------------------------------
var listOfImages = SMCI.toList(SMCI.size());
var firstImage = ee.Image(listOfImages.get(0));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'SMCI',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
