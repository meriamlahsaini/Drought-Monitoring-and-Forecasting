import ee

class GetIndices():
  def __init__(self, args, roi, index, sum=False):
    
    self.args = args
    self.sum = sum
    self.index = index
    self.roi = roi

    self.raw_data = self.filter_data()
    self.seasonal_data = self.seasonal_filter()
    self.monthly_agg  = self.monthly_Data()
    self.monthly_min, self.monthly_max = self.monthly_Min_Max()


  def filter_data(self):
    if self.index == 'TCI':
      terra_lst = ee.ImageCollection(self.args.terra_LST_dir)
      aqua_lst = ee.ImageCollection(self.args.terra_LST_dir)
      MODIS_LST = terra_lst.merge(aqua_lst)\
                           .filterBounds(self.roi)\
                           .select('LST_Day_1km') 
      return MODIS_LST.map(lambda img: img.multiply(0.02)\
                                          .subtract(273.15)\
                                          .float()\
                                          .set("system:time_start", img.get("system:time_start")))


    elif self.index == 'VCI': 
      terra_ndvi = ee.ImageCollection(self.args.terra_NDVI_dir)
      aqua_ndvi = ee.ImageCollection(self.args.terra_NDVI_dir)
      MODIS_NDVI = terra_ndvi.merge(aqua_ndvi)\
                             .filterBounds(self.roi) \
                             .select('NDVI')  
      return MODIS_NDVI.map(lambda img: img.divide(10000)\
                                            .float()\
                                            .set("system:time_start", img.get("system:time_start")))
                  
      
    elif self.index == 'ETCI':
      modis_et = ee.ImageCollection(self.args.modis_ET_dir)
      MODIS_ET = modis_et.filterBounds(self.roi) \
                         .select('ET')
      return MODIS_ET.map(lambda img: img.multiply(0.1)\
                                         .float()\
                                         .set("system:time_start", img.get("system:time_start")))                      


    elif self.index == 'PCI':
      precip = ee.ImageCollection(self.args.precip_dir)
      return precip.filterBounds(self.roi)\
                   .select('precipitationCal')            
    
    elif self.index == 'SMCI':
      sm = ee.ImageCollection(self.args.sm_dir)
      return sm.filterBounds(self.roi) \
               .select('SoilMoi10_40cm_inst') 

  
  def seasonal_filter (self): 
    if self.args.season == 'sowing':
      return self.raw_data.filter(ee.Filter.calendarRange(2012, 2021, 'year')) \
                          .filter(ee.Filter.calendarRange(11, 12, 'month'))
    else:
      return self.raw_data.filter(ee.Filter.calendarRange(2012, 2022, 'year')) \
                          .filter(ee.Filter.calendarRange(1, 4, 'month'))
  
  ## Map over the years and create a monthly aggregates (sum or mean) 
  def monthly_Data (self):
    monthly_data = []
    for year in self.args.years:
      for month in self.args.months:
        Monthly_data = self.seasonal_data.filter(ee.Filter.calendarRange(year, year, 'year')) \
                                         .filter(ee.Filter.calendarRange(month, month, 'month')) \

        if self.sum == False:
          monthly_data.append (Monthly_data.mean() \
                                           .set({'month': month, 'year': year}))
        else:
          monthly_data.append (Monthly_data.sum() \
                                           .set({'month': month, 'year': year}))      
    return ee.ImageCollection.fromImages(monthly_data)


  ## compute Min and Max for each month across all years
  def monthly_Min_Max(self):
    min, max = [], []
    for month in self.args.months:
      Monthly_min = self.monthly_agg.filter(ee.Filter.eq('month', month)) \
                                    .min()\
                                    .set('month', month)

      Monthly_max = self.monthly_agg.filter(ee.Filter.eq('month', month)) \
                                    .max()\
                                    .set('month', month)
      min.append(Monthly_min)
      max.append(Monthly_max)
    return ee.ImageCollection.fromImages(min), ee.ImageCollection.fromImages(max)

  def Compute_Index (self, image):
    # TCI = (max - avg) / (max - min)
    # VCI, PCI, ETCI = (avg - min) / (max - min)
    if self.index =='TCI':
      expression = '(max - avg) / (max - min)'
    else: 
      expression = '(avg - min) / (max - min)'
    
    return image.expression(expression,
                            {'avg': image.select('avg'),
                            'min': image.select('min'),
                            'max': image.select('max')
                            }).rename(self.index) 
  
  def get_scaled_index(self):
    Index_img = []
    for year in self.args.years:
      for month in self.args.months:
        filtered =  self.monthly_agg.filter(ee.Filter.eq('year', year)) \
                                    .filter(ee.Filter.eq('month', month))
        avg = ee.Image(filtered.first())
        min = ee.Image(self.monthly_min.filter(ee.Filter.eq('month', month)).first())
        max = ee.Image(self.monthly_max.filter(ee.Filter.eq('month', month)).first())

        image = ee.Image.cat([avg, min, max]) \
                        .rename(['avg', 'min', 'max'])
        
        ScaledIndex = self.Compute_Index (image).set('month', month).set('year', year)
        Index_img.append (ScaledIndex)

    return ee.ImageCollection.fromImages(Index_img)
