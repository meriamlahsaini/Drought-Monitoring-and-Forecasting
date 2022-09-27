import streamlit as st
import ee, geemap
geemap.ee_initialize()
#     import geemap.foliumap as geemap: don't use it, it messes up with the API initialization
import time
import gc
import math
import datetime as dt
import pandas as pd
import numpy as np
from drought_monitoring import dataset, pca, CMDI
# from dataset import GetIndices
# from pca import getPrincipalComponents
# from CMDI import compute_CMDI
from args import get_main_args


def app():
    st.title("Drought Monitoring")
    
    ## ROI
    countries = (
        "Afghanistan",
        "Burkina Faso",
        "Ethiopia",
        "Ghana",
        "Kenya",
        "Senegal",
        "Zambia"
    )
    
    # import the necessary libraries
    args = get_main_args()
    
    st.subheader("Define ROI")
    start_time = time.time()
#     roi_bar = st.progress(0)
    
    country = st.selectbox("Country", countries, label_visibility="collapsed")
    if country == "Afghanistan":
        roi = ee.FeatureCollection(args.afghanistan_dir)
    elif country == "Burkina Faso":
        roi = ee.FeatureCollection(args.burkina_faso_dir)
    elif country == "Ethiopia":
        roi = ee.FeatureCollection(args.ethiopia_dir)
    elif country == "Ghana":
        roi = ee.FeatureCollection(args.ghana_dir) 
    elif country == "Kenya":
        roi = ee.FeatureCollection(args.kenya_dir) 
    elif country == "Senegal":
        roi = ee.FeatureCollection(args.senegal_dir)      
    elif country == "Zambia":
        roi = ee.FeatureCollection(args.zambia_dir)
    
    display_boundary_map = st.button('Display Boundary Map')
    if display_boundary_map: 
        with st.spinner('Wait for it...'):
            Map = geemap.Map(plugin_Draw=True, Draw_export=False)
            Map.centerObject(roi, 6)
            Map.addLayer(roi, {}, country +'Boundary Map') 
            Map.to_streamlit()
    
        
    ## INPUT INDICES: VCI, TCI, PCI, ETCI, SMCI
    st.subheader('Compute Input Indices')
    season = st.radio('choose season', ('Growing Season', 'Sowing Season'), horizontal=True, label_visibility="collapsed")
    if season == 'Growing Season':
        st.write('The growing season spans January to April from 2016 to 2022. Please select one of these dates')
        st.write({'Month': ['January', 'February', 'March', 'April'],
                  'Year': ['2016', '2017', '2018', '2019', '2020', '2021', '2022']})       

    else:
        st.write('The sowing season spans Novermber to December from 2016 to 2021. Please select one of these dates')
        st.write({'Month': ['November', 'December'],
                  'Year': ['2016', '2017', '2018', '2019', '2020', '2021']})  

    
    args.season = season
    TCI = dataset.GetIndices(args, roi, index='TCI', sum=False).get_scaled_index()
    VCI = dataset.GetIndices(args, roi, index='VCI', sum=False).get_scaled_index()
    ETCI = dataset.GetIndices(args, roi, index='ETCI', sum=True).get_scaled_index()
    PCI  = dataset.GetIndices(args, roi, index='PCI', sum=True).get_scaled_index()
    SMCI = dataset.GetIndices(args, roi, index='SMCI', sum=False).get_scaled_index()

    listOfVCIImages = VCI.toList(VCI.size())
    listOfTCIImages = TCI.toList(TCI.size())
    listOfPCIImages = PCI.toList(PCI.size())
    listOfETCIImages = ETCI.toList(ETCI.size())
    listOfSMCIImages = SMCI.toList(SMCI.size())

    if args.season == 'Growing Season':
        month = ['January', 'February', 'March', 'April']
        year = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
        d = st.date_input(
            "Select a month and a year",
            value=dt.date(2016, 1, 1), min_value=dt.date(2016, 1, 1),max_value=dt.date(2022, 4, 30), label_visibility="collapsed")
    else:
        month = ['November', 'December']
        year = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
        d = st.date_input(
            "Select a month and a year",
                value=dt.date(2016, 11, 1), min_value=dt.date(2016, 11, 1), max_value=dt.date(2022, 12, 31), label_visibility="collapsed")
        
    dates = [i+' '+j for j in year for i in month]
    if d.strftime("%B %Y") not in dates:
        st.warning('Please select one of the recommended dates', icon="⚠️")
        st.write(dates)
    else:
        args.idx =  tuple(dates).index(d.strftime("%B %Y"))

    VCI_image = ee.Image(listOfVCIImages.get(args.idx))
    TCI_image = ee.Image(listOfTCIImages.get(args.idx))
    PCI_image = ee.Image(listOfPCIImages.get(args.idx))
    ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
    SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))
   

            
    ## PCA
    gc.collect()
    image = ee.Image.cat([VCI_image.clip(roi), 
                          TCI_image.clip(roi),
                          PCI_image.clip(roi),
                          ETCI_image.clip(roi),
                          SMCI_image.clip(roi)]) 
    
    st.subheader('Compute CMDI')
    # Get the PCs at the specified scale and in the specified region
    pcImage, eigenVectors = pca.getPrincipalComponents(image, args.scale, roi, args.bandNames)    
    eigenVectors_np = np.array(eigenVectors.getInfo())[0]
    contrib_coeff = eigenVectors_np**2
    weights = [math.ceil(i*100)/100 for i in contrib_coeff]
    display_weights = st.button('Weights')
    if display_weights:
        st.write(pd.DataFrame({
            'Input Indices': ['VCI', 'TCI', 'PCI', 'ETCI', 'ETCI'],
            'Contribution Weights': list(map(lambda x: "%.2f" % x, weights)), 
        }))

                    
    input_indcies = (
        "CMDI",
        "ETCI",
        "PCI",
        "SMCI",
        "TCI",
        "VCI"
    )
    input_index = st.radio('choose index', input_indcies, horizontal=True, label_visibility="collapsed")
#     input_index = st.selectbox("Input Indices", input_indcies)
    display_input_index = st.button('Display '+ input_index)

    
    # compute CMDI
    CMDI_image = CMDI.compute_CMDI(VCI_image, TCI_image, PCI_image, ETCI_image, SMCI_image, weights, roi)
    
    if display_input_index:
        if input_index == 'VCI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, ' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="VCI, " + d.strftime("%B %Y"))
                Map.to_streamlit()
    
        elif input_index == 'TCI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, ' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.tciVis, label="TCI", orientation="vertical", layer_name="TCI, " + d.strftime("%B %Y"))
                Map.to_streamlit()

        elif input_index == 'PCI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, ' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.vciVis, label="PCI", orientation="vertical", layer_name="PCI, " + d.strftime("%B %Y"))
                Map.to_streamlit()

        elif input_index == 'ETCI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI,' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.etciVis, label="ETCI", orientation="vertical", layer_name="ETCI, " + d.strftime("%B %Y"))
                Map.to_streamlit()
            
        elif input_index == 'SMCI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, ' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.smciVis, label="SMCI", orientation="vertical", layer_name="SMCI, " + d.strftime("%B %Y"))
                Map.to_streamlit()
                   

        elif input_index == 'CMDI':
            with st.spinner('Wait for it...'):
                Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
                Map.centerObject(roi, 6)
                Map.addLayer(CMDI_image.clip(roi), args.cdmiVis, 'CMDI,' + d.strftime("%B %Y")) 
                Map.add_colorbar(args.cdmiVis, label="CMDI", orientation="vertical", layer_name="CMDI, " + d.strftime("%B %Y"))
                Map.to_streamlit()
    end_time = time.time()
    execution_time = end_time - start_time
    st.success('Execution Time'+str(round("%.2f" % execution_time))+' seconds', icon="✅")
