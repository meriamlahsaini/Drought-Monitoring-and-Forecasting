======
Drought Dataset
======

**Content**

- `Introduction`_
- `Data Preprocessing`_
- `CMDI Construction`_
- `CMDI Validation`_




Introduction
------------
In this study, I propose the construction of an integrated drought monitoring index (CMDI) that takes into account precipitation, temperature, and vegetation as explanatory variables to monitor drought in the countries of interest. These countries are poorly instrumented areas (e.g., Zambia) of the world and lack good quality ground truth data. Therefore, datasets from remote sensing were used to calculate drought indices. The specification of these datasets are presented in the following table:


.. figure:: https://github.com/surajitghoshiwmi/Rim/blob/main/images/data%20specs.png
    :align: center

    
Data Preprocessing
------------------
As seen in the data summary Table above, the raw data is available in varying resolutions and quality and therefore needs to be filtered and homogenized before use. For computational reasons we restricted the study period to the growing season (January-February-March-April) from 2016 until 2022. All datasets are aggregated as monthly datasets: summation in the case of precipitation and evapotranspiration and average for the case of LST, SM and NDVI.

As input parameters for the construction of the drought index in the study areas, I selected the variables related to agricultural and meteorological drought conditions. The precipitation factor greatly influences meteorological drought which can be calculated using precipitation condition index (PCI). Crop growth is hindered by high surface temperature, which can be measured in this study using the temperature condition index (TCI). Vegetation shows its response to a state of low precipitation and deficit soil moisture. This situation can be measured using the VCI and SMCI, drought indices. Additional RS indices such as ETCI can be used for drought characterization as well.

**Precipitation condition index (PCI):**

.. role:: raw-math(raw)
    :format: latex html

:raw-math:`$$  PCI = \frac{P-P_{min}}{P_{max}-P_{min}} $$`

   
**Vegetation condition index (VCI):**

:raw-math:`$$  VCI = \frac{NDVI_j-NDVI_{min}}{NDVI_{max}-NDVI_{min}} $$`


**Temperature Condition Index (TCI):**

:raw-math:`$$  TCI = \frac{LST_{max}-LST_{i}}{LST_{max}-LST_{min}} $$`


**Evapotranspiration Condition Index (ETCI):**

:raw-math:`$$  ETCI = \frac{ET_i-ET_{min}}{ET_{max}-ET_{min}} $$`


**Soil Moisture Condition Index (SMCI):**

:raw-math:`$$  SMCI = \frac{SM_i-SM_{min}}{SM_{max}-SM_{min}} $$`



.. figure:: https://github.com/surajitghoshiwmi/Rim/blob/main/images/indices.png
    :align: center
    
    
    
CMDI Construction
------------------
Principal Component Analysis (PCA) is performed here to determine the weights for the drought factors. This produces a different weight value per year and per month for each input variable as shown in the equation below. When the CDMI is calculated for February, the weights will be different to when the CDMI is calculated for April, etc. The main steps of this technique include: (1) Standardization of the data (2) Calculation of the covariance matrix. (3) Computing the eigenvectors and eigenvalues of the co-variance matrix (4) Solving the principal components, generally only considering the principal components with eigenvalues exceeding 1. (5) Calculation of the contribution rate.

In this last step, the aim is to determine the weights of the input variables. These weights are derived from the loadings of the eigenvector that corresponds to the principal component that holds most of the variance in the dataset. In this study we considered a cumulative contribution rate exceeding 85\% that corresponds with an eigenvalue exceeding 1.

:raw-math:`$$  CDMI_{y,m}  = W_{VCI,y,m}* VCI_{y,m}+ W_{TCI,y,m}*TCI_{y,m}+ W_{PCI,y,m}*PCI_{y,m}+W_{ETCI,y,m}*ETCI_{y,m}+W_{SMCI,y,m}*SMCI_{y,m} $$`


CMDI Validation
----------------
SPI-3, SPI-6, SPI-9, SPI-12, and GPP data derived from IMERG and MODIS respectively were used to validate the resulting monthly CMDI data.  
