/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the MODIS data based on user inputs
and performes the GPP monthly computation.

USES:
    - seasonal_filter.js
    - monthly_composites.js

Note: Load the ROI, here it uses "Zambia" as a featureCollection.
*/

// MODULES DECLARATION --------------------------------------------------------------------------
//seasonal filter
var seasonalFilter = require("users/Plottings/drought_dataset:dataset/seasonal_filter.js")
//monthly composites
var monthlyComposites = require('users/Plottings/drought_dataset:dataset/monthly_composites.js')
//

// Import and combine Terra and Aqua MODIS GPP Image Collections and filter by roi and date -----
var terra_GPP = ee.ImageCollection("MODIS/006/MOD17A2H")
var aqua_GPP = ee.ImageCollection("MODIS/006/MYD17A2H") 
var modis_GPP = terra_GPP.merge(aqua_GPP) 
                           .filterBounds(Zambia) 
                           .select('Gpp')       
var Col =  seasonalFilter.Season(modis_GPP)     

// Display the image collection from January 2016
var gppVis = {min: 0.0,max: 600.0, palette: ['#a50026','#d73027','#f46d43','#fdae61',
                                             '#fee08b','#ffffbf','#d9ef8b','#a6d96a',
                                             '#66bd63','#1a9850','#006837']};

Map.centerObject(Zambia, 6)
Map.addLayer(Col.first().clip(Zambia), gppVis, 'Jan, 2016');

// compute monthly avg, min, and max ------------------------------------------------------------
var monthly_avg =  monthlyComposites.monthly_Avg(Col) 
var monthly_min =  monthlyComposites.monthly_Min(monthly_avg) 
var monthly_max =  monthlyComposites.monthly_Max(monthly_avg)

// compute scaled GPP --------------------------------------------------------------------------
var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

var scaledGPP = ee.ImageCollection.fromImages(years.map(function(year) {
  return months.map(function (month) {
    var filtered = monthly_avg.filter(ee.Filter.eq('year', year))
                              .filter(ee.Filter.eq('month', month))
                                    
    var avgGPP = ee.Image(filtered.first())
    var minGPP = ee.Image(monthly_min.filter(ee.Filter.eq('month', month))
                                      .first())
    var maxGPP = ee.Image(monthly_max.filter(ee.Filter.eq('month', month))
                                      .first())
                            
    var image = ee.Image.cat([avgGPP, minGPP, maxGPP])
                        .rename(['avgGPP', 'minGPP', 'maxGPP'])
    // GPPCI = (GPP - min) / (max - min)
    return image.expression('(avgGPP - minGPP) / (maxGPP - minGPP)',
    {'avgGPP': image.select('avgGPP'),
    'minGPP': image.select('minGPP'),
    'maxGPP': image.select('maxGPP')
      
    }).rename('scaledGPP')
      .set({'month': month, 'year': year});
  });
}).flatten());


// Display monthly GPP from January 2016
Map.addLayer(scaledGPP.first().clip(Zambia), gppVis, 'GPP: Jan, 2016');
 

// Export the data ----------------------------------------------------------------------
var listOfImages = scaledGPP.toList(scaledGPP.size());
var firstImage = ee.Image(listOfImages.get(27));
Export.image.toDrive({
  image: firstImage.clip(Zambia),
  description: 'GPP',
  scale: 250,
  region: Zambia,
  maxPixels:1e13,
  fileFormat: 'GeoTIFF',
});
