==========================
PCA-ConvLSTM Network: A Machine Learning Approach for Drought Monitoring and Forecasting – Case study of Zambia
==========================
 .. image:: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
         :target: https://rim-chan-drought-monitoring-and-forecasting-app-qjoet8.streamlitapp.com/


**Content**

- `Introduction`_
- `Experimental Setup`_
- `Project Structure`_
- `Instructions for Data Preprocessing and Generation`_


Introduction
-------------
Drought is a climate-related disaster that negatively impacts a variety of sectors and poses challenges for millions of people in Zambia. The occurrence and the increase in drought severity result in significant losses to the farming community. As an agrarian economy, establishing drought monitoring and early warning systems can help decision-makers better act in response to drought. The overarching objective of this study is to address this problem through the development of a drought monitoring and forecasting system, leveraging the synergistic use of Principal Component Analysis (PCA) and convolutional long short term memory (ConvLSTM) over Zambia. The main objectives are:

* Derive a new composite drought index (CMDI) that encapsulates the effects of different drivers (climate- precipitation and temperature, Agriculture- vegetation, evapotranspiration, soil moisture). 
* Implement ConvLSTM for Spatio-temporal prediction of CMDI. 
* Demonstrate that online platforms such as Google Earth Engine - a cloud-based geospatial analysis, as well as Google Colab and Kaggle which offer free yet limited GPU usage, are effective tools for carrying out the analysis of global geospatial big data at scale. Therefore, leveraging them can help bypass the need for expensive and limited datasets and hardware. 
* Compare the spatial-temporal distribution of CMDI with multi-time scale SPI (3-month to 12-month) and Gross Primary production (GPP).


.. figure:: https://github.com/Rim-chan/DM/blob/main/images/Drought%20Monitoring%20and%20Forecasting%20Workflow.jpg
    :align: center



Experimental Setup
-------------------
For data preprocessing and CDMI construction using Principal Componnent Analysis (PCA). I used `Google Earth Engine (GEE) <https://earthengine.google.com/>`__ . A cloud computing platform which was launched by Google, in 2010. GEE provides free access to numerous remotely sensed datasets as well as computing power, facilitating big geo data processing and analysis. In addition `geemap <https://geemap.org/>`__ -a Python package for interactive mapping with Google Earth Engine and Google Collaboratory were also used for the calculation of the construction of the drought index.  `climate-indices <https://pypi.org/project/climate-indices/>`__  -python package was used for SPI claculations. ConvLSTM implementation was conducted using `Kaggle <https://www.kaggle.com/>`__ .


Project Structure
------------------
In this folder you will find:

* `preprocess_GEE <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/tree/main/preprocess_GEE>`__ contains GEE Java Scripts to generate the drought indices and the validation indices;
* `requirements.txt <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/requirements.txt>`__ contains all the necessary libraries;
* `args.py <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/args.py>`__ contains all the arguments used in this project;
* `drought monitoring <https://github.com/surajitghoshiwmi/Rim/tree/main/dought%20monitoring>`__ contains geemap based python code to generate the drought indices and the validation indices;
* `drought forecasting <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/tree/main/drought_forecasting>`__ contains jupyter notebook for PCA based CMDI forecasting using ConvLSTM;
* `SPI <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/tree/main/SPI>`__ contains jupyter notebooks for to generate SPI at different time scales using daily IMERG data and  half hourly IMERG data;
* `apps <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/tree/main/apps>`__,  `app.py <https://github.com/Rim-chan/DM/blob/main/app.py>`__, and, `multiapp.py <https://github.com/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/multiapp.py>`__,  A streamlit multipage app for geospatial applications. It can be deployed ;



Instructions for Data Preprocessing and Generation
--------------------------------------------------

This section provides instructions for the Data preprocessing and generation phase.

- To use the Java Script in GEE:
 `GEE Repo <https://code.earthengine.google.com/?accept_repo=users/Plottings/drought_dataset>`__
 
- To use the streamlit app:
 
 .. image:: https://static.streamlit.io/badges/streamlit_badge_black_white.svg
         :target: https://rim-chan-drought-monitoring-and-forecasting-app-qjoet8.streamlitapp.com/

- To run the full python code using Google Colab:
For SPI Calculation suing daily IMERG data:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/SPI/SPI_based_on_IMERG_DailyData_[Zambia].ipynb
         

- For SPI Calculation suing half hourly IMERG data:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/SPI/SPI_based_on_IMERG_HalfHourlyData_[Zambia].ipynb
 
- For PCA-CDMI Calculation:
  
 .. image:: https://colab.research.google.com/assets/colab-badge.svg
         :target: https://colab.research.google.com/github/Rim-chan/Drought-Monitoring-and-Forecasting/blob/main/drought_monitoring/CMDI_[PCA][2016_22].ipynb
         
