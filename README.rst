==========================
PCA-ConvLSTM Network: A Machine Learning Approach for Drought Monitoring and Forecasting – Case study of Zambia
==========================


**Content**

- `Introduction`_
- `Experimental Setup`_
- `Project Structure`_


Introduction
-------------
Drought is a climate-related disaster that negatively impacts a variety of sectors and poses challenges for millions of people in Zambia. The occurrence and the increase in drought severity result in significant losses to the farming community. As an agrarian economy, establishing drought monitoring and early warning systems can help decision-makers better act in response to drought. The overarching objective of this study is to address this problem through the development of a drought monitoring and forecasting system, leveraging the synergistic use of Principal Component Analysis (PCA) and convolutional long short term memory (ConvLSTM) over Zambia. The main objectives are:

* Derive a new composite drought index (CDMI) that encapsulates the effects of different drivers (climate- precipitation and temperature, Agriculture- vegetation, evapotranspiration, soil moisture). 
* Implement ConvLSTM for Spatio-temporal prediction of CDMI. 
* Demonstrate that online platforms such as Google Earth Engine - a cloud-based geospatial analysis, as well as Google Colab and Kaggle which offer free yet limited GPU usage, are effective tools for carrying out the analysis of global geospatial big data at scale. Therefore, leveraging them can help bypass the need for expensive and limited datasets and hardware. 
* Compare the spatial-temporal distribution of CDMI with multi-time scale SPI (3-month to 12-month) and Gross Primary production (GPP).


.. figure:: https://github.com/Rim-chan/DM/blob/main/images/Drought%20Monitoring%20and%20Forecasting%20Workflow.jpg
    :align: center



Experimental Setup
-------------------
For data preprocessing and CDMI construction using Principal Componnent Analysis (PCA). I used `Google Earth Engine (GEE) <https://earthengine.google.com/>`__ . A cloud computing platform which was launched by Google, in 2010. GEE provides free access to numerous remotely sensed datasets as well as computing power, facilitating big geo data processing and analysis. In addition `geemap <https://geemap.org/>`__ -a Python package for interactive mapping with Google Earth Engine and Google Collaboratory were also used for the calculation of the construction of the drought index.  `climate-indices <https://pypi.org/project/climate-indices/>`__  -python package was used for SPI claculations. ConvLSTM implementation was conducted using `Kaggle <https://www.kaggle.com/>`__ .


Project Structure
------------------
In this folder you will find:

* `dataset <https://github.com/surajitghoshiwmi/Rim/tree/main/dataset>`__ contains GEE Java Scripts and jupyter notebooks to generate the drought indices and the validation indices;
* `drought monitoring <https://github.com/surajitghoshiwmi/Rim/tree/main/dought%20monitoring>`__ contains jupyter notebooks for CDMI construction using LightGBM and WNet-Kmeans;
* `drought forecasting <https://github.com/surajitghoshiwmi/Rim/tree/main/drought%20forecasting>`__ contains jupyter notebook for PCA based CDMI forecasting using ConvLSTM;
* `requirements.txt <https://github.com/surajitghoshiwmi/Rim/blob/main/requirements.txt>`__ Contains all the necessary libraries.


