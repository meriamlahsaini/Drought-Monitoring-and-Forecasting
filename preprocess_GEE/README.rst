======
Drought Dataset
======

**Content**

- `Introduction`_
- `Data Preprocessing`_
- `CDMI Construction`_
- `CDMI Validation`_
- `Experimental Setup`_
- `Folder Structure`_




Introduction
------------
In this study, I propose the construction of an integrated drought monitoring index (CDMI) that takes into account precipitation, temperature, and vegetation as explanatory variables to monitor drought in the countries of interest. These countries are poorly instrumented areas (e.g., Zambia) of the world and lack good quality ground truth data. Therefore, datasets from remote sensing were used to calculate drought indices. The specification of these datasets are presented in the following table:


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
    
    
    
CDMI Construction
------------------
Principal Component Analysis (PCA) is performed here to determine the weights for the drought factors. This produces a different weight value per year and per month for each input variable as shown in the equation below. When the CDMI is calculated for February, the weights will be different to when the CDMI is calculated for April, etc. The main steps of this technique include: (1) Standardization of the data (2) Calculation of the covariance matrix. (3) Computing the eigenvectors and eigenvalues of the co-variance matrix (4) Solving the principal components, generally only considering the principal components with eigenvalues exceeding 1. (5) Calculation of the contribution rate.

In this last step, the aim is to determine the weights of the input variables. These weights are derived from the loadings of the eigenvector that corresponds to the principal component that holds most of the variance in the dataset. In this study we considered a cumulative contribution rate exceeding 85\% that corresponds with an eigenvalue exceeding 1.

:raw-math:`$$  CDMI_{y,m}  = W_{VCI,y,m}* VCI_{y,m}+ W_{TCI,y,m}*TCI_{y,m}+ W_{PCI,y,m}*PCI_{y,m}+W_{ETCI,y,m}*ETCI_{y,m}+W_{SMCI,y,m}*SMCI_{y,m} $$`


CDMI Validation
----------------
SPI-3, SPI-6, SPI-9, SPI-12, and GPP data derived from IMERG and MODIS respectively were used to validate the resulting monthly CDMI data.  



Experimental Setup
------------------
As for the experimental setup I used `Google Earth Engine (GEE) <https://earthengine.google.com/>`__ . A cloud computing platform which was launched by Google, in 2010.
GEE provides free access to numerous remotely sensed datasets as well as computing power, facilitating big geo data processing and analysis .
In addition `geemap <https://geemap.org/>`__ -a Python package for interactive mapping with Google Earth Engine and Google Collaboratory were also used for the calculation of the construction of the drought index.  `climate-indices <https://pypi.org/project/climate-indices/>`__  -python package is used for SPI claculations.

Folder Structure
----------------
In this folder you will find:

* `preprocess_GEE <https://github.com/surajitghoshiwmi/Rim/tree/main/dataset/preprocess_GEE>`__ contains GEE Java Scripts to generate the drought indices and the validation indices.
* `preprocess.py <https://github.com/surajitghoshiwmi/Rim/blob/main/dataset/preprocess.py>`__ contains geemap based python code to generate the drought indices and the validation indices. 
* `PCA_CDMI_[Zambia].ipynb <https://github.com/surajitghoshiwmi/Rim/blob/main/dataset/PCA_CDMI_[Zambia].ipynb>`__ Google Colab notebook to generate the drought indices and the validation indices. 
* `SPI_based_on_IMERG_HalfHourlyData_[Zambia].ipynb <https://github.com/surajitghoshiwmi/Rim/blob/main/dataset/SPI_based_on_IMERG_HalfHourlyData_[Zambia].ipynb>`__ Google Colab notebook to generate SPI at different time scales using half hourly IMERG data.
* `SPI_based_on_IMERG_DailyData_[Zambia].ipynb <https://github.com/surajitghoshiwmi/Rim/blob/main/dataset/SPI_based_on_IMERG_DailyData_[Zambia].ipynb>`__ Google Colab notebook to generate SPI at different time scales using daily IMERG data.




Instructions for Data Preprocessing and Generation
--------------------------------------------------

This section provides instructions for the Data preprocessing and generation phase.

- To use the Java Script in GEE:
 `GEE Repo <https://code.earthengine.google.com/?accept_repo=users/Plottings/drought_dataset>`__

- To use the python code:

**Prepare environment**

.. code:: python
 
  # Install geemap package
  import subprocess

  try:
      import geemap
  except ImportError:
      print('Installing geemap ...')
      subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])
      
.. code:: python

  # git clone source
  !git clone https://Rim-chan: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@github.com/Rim-chan/IWMI-Drought-Monitoring.git
   
**Data Preprocessing**

.. code:: python

  !python ./IWMI-Drought-Monitoring/dataset/preprocess.py
  
  
- To run the full python code using Google Colab:
For SPI Calculation suing daily IMERG data:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/surajitghoshiwmi/Rim/blob/main/dataset/SPI_based_on_IMERG_DailyData_[Zambia].ipynb

For SPI Calculation suing half hourly IMERG data:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/surajitghoshiwmi/Rim/blob/main/dataset/SPI_based_on_IMERG_HalfHourlyData_[Zambia].ipynb
 
For PCA-CDMI Calculation:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/surajitghoshiwmi/Rim/blob/main/dataset/PCA_CDMI_[Zambia].ipynb
        
        
    
