/* Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

These functions compute optical remote sensing indices that can be used for drought indices validation.
It uses MODIS Terra and Aqua SR data.


to call these functions use:

var valIndices = require('users/Plottings/drought_dataset:dataset/compute_indices.js')
var ImagewithNDMI = valIndices.addNDMI(image)
var ImagewithMNDWI= valIndices.addMNDWI(image)
var ImagewithNMDI = valIndices.addNMDI(image)
var ImagewithSWCI = valIndices.addSWCI(image)
var ImagewithVSDI = valIndices.addVSDI(image)
or
var collectionwithNDMI = ImageCollection.map(valIndices.addNDMI)
var collectionwithMNDWI= ImageCollection.map(valIndices.addMNDWI)
var collectionwithNMDI = ImageCollection.map(valIndices.addNMDI)
var collectionwithSWCI = ImageCollection.map(valIndices.addSWCI)
var collectionwithVSDI = ImageCollection.map(valIndices.addVSDI)


INPUTS:
        - image: <ee.Image>
                image for which to calculate the index
OUTPUTS:
        - <ee.Image>
          the input image with 1 new band: 
          'NDMI' : normalized difference moisture index
          'MNDWI': modified normalized difference water index
          'NMDI' : normalized multi-band drought index
          'SWCI' : surface water content index
          'VSDI' : visible and shortwave drought index
          
*/


exports.addNDMI = function(image) {
    //NDMI = (NIR - SWIR) / (NIR + SWIR)
    var ndmi = image.normalizedDifference(['sur_refl_b02', 'sur_refl_b06'])
                    .rename('NDMI')
                    .copyProperties(image, ["system:time_start"]);
    return image.addBands(ndmi);
  };
  
  
  exports.addMNDWI = function(image) {
    //MNDWI = (Green – SWIR) / (Green + SWIR)
    var mndwi = image.normalizedDifference(['sur_refl_b04', 'sur_refl_b06'])
                     .rename('MNDWI')
                     .copyProperties(image, ["system:time_start"]);
    return image.addBands(mndwi);
  };
  
  
  exports.addNMDI = function(image) {
    //  [0, 1]
    var nmdi = image.expression('(B5- (B6-B7)) / (B5 + (B6-B7))',
      {'B5': image.select('sur_refl_b02'),
       'B6': image.select('sur_refl_b06'),
       'B7': image.select('sur_refl_b07')
      }).rename('NMDI')
        .copyProperties(image, ["system:time_start"]);
    return image.addBands(nmdi);
  };
  
  
  exports.addSWCI = function(image) {
    //  [-1, 1]
    var swci = image.expression('(B6-B7) / (B6+B7)',
      { 'B6': image.select('sur_refl_b06'),
        'B7': image.select('sur_refl_b07')
      }).rename('SWCI')
        .copyProperties(image, ["system:time_start"]);
    return image.addBands(swci);
  };
  
  
  exports.addVSDI = function(image) {
    // [0, 1]
    var vsdi = image.expression('1  -((B7-B3) / (B1+B3))',
      { 'B1': image.select('sur_refl_b01'),
        'B3': image.select('sur_refl_b03'),
        'B7': image.select('sur_refl_b07')
      }).rename('VSDI')
        .copyProperties(image, ["system:time_start"]);
    return image.addBands(vsdi);
  };
