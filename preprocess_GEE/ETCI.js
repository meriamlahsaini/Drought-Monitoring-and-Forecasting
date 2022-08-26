/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the MODIS data based on user inputs
and performes the scaled ET computation.

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


// Filter image collection by roi, date then apply cloud masks -------------------------------------------
var MODIS_data = ee.ImageCollection('MODIS/006/MOD16A2')
                .filterBounds(Zambia)
                .select('ET'); 
var Col = seasonalFilter.Season(MODIS_data);    

// Display the image collection from 2016
Map.centerObject(Zambia, 6)
var ETVis = {min: 0.0, max: 300.0, palette: ['ffffff', 'fcd163', '99b718',
                                             '66a000', '3e8601', '207401',
                                             '056201', '004c00', '011301']};
Map.addLayer(Col.first().clip(Zambia), ETVis, 'Feb, 2016');


// Compute monthly sums, min, and max ---------------------------------------------------------------------
var monthly_sum =  monthlyComposites.monthly_Sum(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_sum) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_sum)

// Display sum, min, and max ET images from 2016
Map.addLayer(monthly_sum.first().clip(Zambia), ETVis, 'Jan_sum, 2016');
Map.addLayer(monthly_min.first().clip(Zambia), ETVis, 'Jan_min, 2016');
Map.addLayer(monthly_max.first().clip(Zambia), ETVis, 'Jan_max, 2016');

// Compute the ETCI ---------------------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

var ETCI = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_sum.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
                                    
    var sumET = ee.Image(filtered.first())
    var minET = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                    .first())
    var maxET = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                    .first())
                            
    var image = ee.Image.cat([sumET, minET, maxET])
                        .rename(['sumET', 'minET', 'maxET'])
    // ETCI = (Pre - min) / (max - min)
    return image.expression('(sumET - minET) / (maxET - minET)',
    {'sumET': image.select('sumET'),
    'minET': image.select('minET'),
    'maxET': image.select('maxET')
      
    }).rename('ETCI')
      .set({'month': month, 'year': year});
  });
}).flatten());

// Display the ETCI index from January 2016
var ETVisParams = {min: 0, max: 1, palette: ['blue', 'orange', 'red']}
Map.addLayer(ETCI.first().clip(Zambia), ETVisParams,'ETCI Jan 2016');

// Export the data -----------------------------------------------------------------------------------------
var listOfImages = ETCI.toList(ETCI.size());
var firstImage = ee.Image(listOfImages.get(0));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'ETCI',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
