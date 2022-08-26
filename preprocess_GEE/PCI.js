/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the CHIRPS precipitation data based on user inputs
and performes the precipitation condition index (PCI) computation

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

// Filter image collection by roi, and date ------------------------------------------------------------
var precipitation = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD")
                      .filterBounds(Zambia)
                      .select('precipitation');
var Col = seasonalFilter.Season(precipitation);     

// Display the image collection from January 2016 
Map.centerObject(Zambia, 6)
var precipitationVis = {min: 0.0, max: 112.0, palette: ['d7191c','fdae61','ffffbf','abdda4','2b83ba']};
Map.addLayer(Col.first().clip(Zambia), precipitationVis, 'Jan, 2016');


// Compute monthly sums, min, and max --------------------------------------------------------------------
var monthly_sum =  monthlyComposites.monthly_Sum(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_sum) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_sum)

// Display sum, min, and max ET images from January 2016
var monthlyVis = {min: 0.0, max: 500.0, palette: ['d7191c','fdae61','ffffbf','abdda4','2b83ba']};
Map.addLayer(monthly_sum.first().clip(Zambia), monthlyVis, 'Jan_sum, 2016');
Map.addLayer(monthly_min.first().clip(Zambia), monthlyVis, 'Jan_min, 2016');
Map.addLayer(monthly_max.first().clip(Zambia), monthlyVis, 'Jan_max, 2016');

// Compute PCI --------------------------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

var PCI = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_sum.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
                                    
    var sumPre = ee.Image(filtered.first())
    var minPre = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                     .first())
    var maxPre = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                     .first())
                            
    var image = ee.Image.cat([sumPre, minPre, maxPre])
                        .rename(['sumPre', 'minPre', 'maxPre'])
    // PCI = (Pre - min) / (max - min)
    return image.expression('(sumPre - minPre) / (maxPre - minPre)',
    {'sumPre': image.select('sumPre'),
    'minPre': image.select('minPre'),
    'maxPre': image.select('maxPre')
      
    }).rename('PCI')
      .set({'month': month, 'year': year});
  });
}).flatten());

// Display the PCI index from January 2016
var pciVis = {min: 0.0, max: 1.0, palette: ['d7191c','fdae61','ffffbf','abdda4','2b83ba']};
Map.addLayer(PCI.first().clip(Zambia), pciVis, 'PCI: Jan, 2016');

// Export the data ----------------------------------------------------------------------------------------
var listOfImages = PCI.toList(PCI.size());
var firstImage = ee.Image(listOfImages.get(0));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'PCI',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
