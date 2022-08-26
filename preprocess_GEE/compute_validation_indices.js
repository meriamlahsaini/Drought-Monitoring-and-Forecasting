/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function selects the MODIS data based on user inputs
and performes the scaled ET computation.


USES:
    - seasonal_filter.js
    - monthly_composites.js
    - validation_indices.js

*/

// MODULES DECLARATION -----------------------------------------------------------
//seasonal filter
var seasonalFilter = require("users/Plottings/drought_dataset:dataset/seasonal_filter.js")
//monthly composites
var monthlyComposites = require('users/Plottings/drought_dataset:dataset/monthly_composites.js')
//validation indices
var valIndices = require('users/Plottings/drought_dataset:dataset/validation_indices.js')
//


// Filter image collection by roi, date and compute monthly averages ------------------------------------
var terra_SR = ee.ImageCollection ("MODIS/061/MOD09A1"); 
var aqua_SR = ee.ImageCollection("MODIS/061/MYD09A1");   

// Combine Terra and Aqua MODIS SR Image Collections
var modis_SR = terra_SR.merge(aqua_SR) 
                          .filterBounds(Zambia) 
                          .select(['sur_refl_b01','sur_refl_b02', 'sur_refl_b03',
                                   'sur_refl_b04','sur_refl_b06', 'sur_refl_b07']);       // 960

var Col =  seasonalFilter.Season(modis_SR);           //213
var monthly_avg = monthlyComposites.monthly_Avg(Col); //28

// Compute Indices -------------------------------------------------------------------------------------
var newCol = monthly_avg.map(valIndices.addNDMI)
                        .map(valIndices.addMNDWI)
                        .map(valIndices.addNMDI)
                        .map(valIndices.addSWCI)
                        .map(valIndices.addVSDI)



// NDMI
var ndmiCol = newCol.select('NDMI')
var ndmiList = ndmiCol.toList(ndmiCol.size());
var ndmiImage = ee.Image(ndmiList.get(3));

// MNDWI
var mndwiCol = newCol.select('MNDWI')
var mndwiList = mndwiCol.toList(mndwiCol.size());
var mndwiImage = ee.Image(mndwiList.get(3));

// NMDI
var nmdiCol = newCol.select('NMDI')
var nmdiList = nmdiCol.toList(nmdiCol.size());
var nmdiImage = ee.Image(nmdiList.get(3));

// SWCI
var swciCol = newCol.select('SWCI')
var swciList = swciCol.toList(swciCol.size());
var swciImage = ee.Image(swciList.get(3));

// VSDI
var vsdiCol = newCol.select('VSDI')
var vsdiList = vsdiCol.toList(vsdiCol.size());
var vsdiImage = ee.Image(vsdiList.get(3));


//Display some indices -----------------------------------------------------------------------------------
Map.centerObject(Zambia, 6)
var droughtPalette = ['#a50026','#d73027','#f46d43','#fdae61','#fee08b',
                      '#ffffbf','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837'];
                  
var droughtParams = {min: 0, max: 1, palette: droughtPalette}
Map.addLayer(vsdiImage.clip(Zambia), droughtParams, 'VSDI: April, 2016');
