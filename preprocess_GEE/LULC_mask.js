/*  Author: Rim Sleimi (rim.sleimi@etudiant-fst.utm.tn)

This script extracts the agricultural mask of Zambia from 2019.
Note: Load the ROI, here it uses "Zambia" as a featureCollection.
*/

// Filter image collection by roi --------------------------------------------------                           
var Zambia_LULC = ee.Image("COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019")
                  .select('discrete_classification')
                  .clip(Zambia);


// Display the LULC from 2019
Map.addLayer(Zambia_LULC.clip(Zambia), {}, "Land Cover");                  

var properties = Zambia_LULC.propertyNames();
print('Metadata properties:', properties);
var names = ee.List(Zambia_LULC.get("discrete_classification_class_names"))
var values = ee.List(Zambia_LULC.get("discrete_classification_class_values"))
var palette = ee.List(Zambia_LULC.get("discrete_classification_class_palette"))

// lulc index : value : name
// 0:0: Unknown. No or not enough satellite data available.
// 1:20: Shrubs. Woody perennial plants with persistent and woody stems and without any defined main stem being less than 5 m tall. The shrub foliage can be either evergreen or deciduous.
// 2:30: Herbaceous vegetation. Plants without persistent stem or shoots above ground and lacking definite firm structure. Tree and shrub cover is less than 10 %.
// 3:40: Cultivated and managed vegetation / agriculture. Lands covered with temporary crops followed by harvest and a bare soil period (e.g., single and multiple cropping systems). Note that perennial woody crops will be classified as the appropriate forest or shrub land cover type.
// 4:50: Urban / built up. Land covered by buildings and other man-made structures.
// 5:60: Bare / sparse vegetation. Lands with exposed soil, sand, or rocks and never has more than 10 % vegetated cover during any time of the year.
// 6:70: Snow and ice. Lands under snow or ice cover throughout the year.
// 7:80: Permanent water bodies. Lakes, reservoirs, and rivers. Can be either fresh or salt-water bodies.
// 8:90: Herbaceous wetland. Lands with a permanent mixture of water and herbaceous or woody vegetation. The vegetation can be present in either salt, brackish, or fresh water.
// 9:100: Moss and lichen.
// 10:111: Closed forest, evergreen needle leaf. Tree canopy >70 %, almost all needle leaf trees remain green all year. Canopy is never without green foliage.
// 11:112: Closed forest, evergreen broad leaf. Tree canopy >70 %, almost all broadleaf trees remain green year round. Canopy is never without green foliage.
// 12:113: Closed forest, deciduous needle leaf. Tree canopy >70 %, consists of seasonal needle leaf tree communities with an annual cycle of leaf-on and leaf-off periods.
// 13:114: Closed forest, deciduous broad leaf. Tree canopy >70 %, consists of seasonal broadleaf tree communities with an annual cycle of leaf-on and leaf-off periods.
// 14:115: Closed forest, mixed.
// 15:116: Closed forest, not matching any of the other definitions.
// 16:121: Open forest, evergreen needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and grassland, almost all needle leaf trees remain green all year. Canopy is never without green foliage.
// 17:122: Open forest, evergreen broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and grassland, almost all broadleaf trees remain green year round. Canopy is never without green foliage.
// 18:123: Open forest, deciduous needle leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and grassland, consists of seasonal needle leaf tree communities with an annual cycle of leaf-on and leaf-off periods.
// 19:124: Open forest, deciduous broad leaf. Top layer- trees 15-70 % and second layer- mixed of shrubs and grassland, consists of seasonal broadleaf tree communities with an annual cycle of leaf-on and leaf-off periods.
// 20:125: Open forest, mixed.
// 21:126: Open forest, not matching any of the other definitions.
// 22:200: Oceans, seas. Can be either fresh or salt-water bodies.


// Reclassify the land cover data and create a mask of agricultural areas
var agricultureMask = Zambia_LULC.where(Zambia_LULC.gt(40), 0)
                                 .where(Zambia_LULC.lt(40), 0)
                                 .where(Zambia_LULC.eq(40), 1);

Map.addLayer(agricultureMask, {min: 0, max:1}, 'agriculture only');

//Export the agricultural mask------------------------------------------------

Export.image.toAsset({
  image: agricultureMask,
  description : "agriculture Mask_250m",
  region : Zambia, 
  scale :250, 
  maxPixels : 1e12});
