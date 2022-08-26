/* Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function creates monthly composites: monthly sums, monthly avrages, monthly min, and monthly max.

to call these functions use:

var monthlyComposites = require('users/Plottings/Drought-Dataset/monthly_composites.js')
var monthly_avg =  monthlyComposites.monthly_Avg(Col)
var monthly_sum =  monthlyComposites.monthly_Sum(Col) 
var monthly_min =  monthlyComposites.monthly_Min(Col) 
var monthly_max =  monthlyComposites.monthly_Max(Col)

INPUTS:
        - image: <ee.Image>
                image for which monthly aggregates are performed 
OUTPUTS:
        - <ee.Image>
                monthly aggregated images
*/


var years = ee.List.sequence(2016, 2022);
var months = ee.List.sequence(1, 4);

// Map over the years and create a monthly average (NDVI, LST, and SM),
// and monthly sums (For Precipitation and Evapotranspiration) collection
// for the specified season------------------------------------------------------
exports.monthly_Avg = function (Col){
  return ee.ImageCollection.fromImages(
    years.map(function(year) {
      return months.map(function(month) {
        return Col
        .filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .mean()
        .set({'month': month, 'year': year});
  });
}).flatten())}

exports.monthly_Sum = function (Col){
  return ee.ImageCollection.fromImages(
    years.map(function(year) {
      return months.map(function(month) {
        return Col
        .filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .sum()
        .set({'month': month, 'year': year});
  });
}).flatten())}



// Compute Minimum for each month across all years ---------------------------------------
exports.monthly_Min = function (Col){
  return ee.ImageCollection.fromImages(
    months.map(function(month) {
      return Col
      .filter(ee.Filter.eq('month', month))
      .min()
      .abs()
      .set('month', month);
}))};


// Compute Maximum for each month across all years ---------------------------------------
exports.monthly_Max = function (Col){
  return ee.ImageCollection.fromImages(
    months.map(function(month) {
      return Col
      .filter(ee.Filter.eq('month', month))
      .max()
      .abs()
      .set('month', month);
}))};
