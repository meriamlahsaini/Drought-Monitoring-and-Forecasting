/* Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This function filters image collections by dates and creates a collection
for the specified growing season (January, February, March, April).

to call these functions use:

var seasonalFilter = require('users/Plottings/Drought-Dataset/seasonal_filter.js')
var seasonalData  = seasonalFilter.Season(ImageCollection)

INPUTS:
        - collection: <ee.ImageCollection>
                image collection for which dates are filtered 
OUTPUTS:
        - <ee.ImageCollection>
                seasonally filtered image collection

*/

// filters image collection
exports.Season = function (collection) {
    return collection.filter(ee.Filter.calendarRange(2016, 2022, 'year'))
                     .filter(ee.Filter.calendarRange(1, 4, 'month'))
};
