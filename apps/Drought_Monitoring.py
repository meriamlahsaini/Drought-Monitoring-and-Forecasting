import streamlit as st
import ee, geemap
geemap.ee_initialize()
#     import geemap.foliumap as geemap: don't use it, it messes up with the API initialization
import time
import gc
import math
import datetime as dt
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
#     roi_st = time.time()
#     roi_bar = st.progress(0)
    
    country = st.selectbox("Country", countries)
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
        Map = geemap.Map(plugin_Draw=True, Draw_export=False)
        Map.centerObject(roi, 6)
        Map.addLayer(roi, {}, country +'Boundary Map') 
        Map.to_streamlit()

#     roi_et = time.time()
#     roi_time = roi_et - roi_st
#     for t in roi_time:
#         time.sleep(0.1)
#         roi_bar = st.progress(t)

        
        
    ## INPUT INDICES: VCI, TCI, PCI, ETCI, SMCI
    st.subheader('Compute Input Indices')
    
    season = st.radio('choose season', ('Growing Season', 'Sowing Season'), horizontal=True, label_visibility="collapsed")
    if season == 'Growing Season':
        st.write('The growing season spans January to April from 2016 to 2022, Please select one of these dates')
    else:
        st.write('The growing season spans Novermber to December from 2016 to 2021, Please select one of these dates')
        
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
        d = st.date_input(
            "Select a month and a year",
            value=dt.date(2016, 1, 1), min_value=dt.date(2016, 1, 1), max_value=dt.date(2022, 4, 30), label_visibility="collapsed")
        st.write(d.strftime("%B%Y"))
        
        
        
        
        
        month = ['January', 'February', 'March', 'April']
        year = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
    else:
        d = st.date_input(
            "Select a month and a year",
            value=dt.date(2016, 11, 1), min_value=dt.date(2016, 11, 1), max_value=dt.date(2022, 12, 31), label_visibility="collapsed")
        
        month = ['November', 'December']
        year = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
        
#     d = st.date_input(
#         "Select a month and a year",
#         datetime.date(2016, 1, 1))
        
#     dates = [i+' '+j for j in year for i in month]
#     date = st.selectbox("Date", tuple(dates))
    

#     args.idx =  tuple(dates).index(date)
#     VCI_image = ee.Image(listOfVCIImages.get(args.idx))
#     TCI_image = ee.Image(listOfTCIImages.get(args.idx))
#     PCI_image = ee.Image(listOfPCIImages.get(args.idx))
#     ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
#     SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))
   

            
#     ## PCA
#     st.subheader('Compute CMDI')
    
#     gc.collect()
    
#     image = ee.Image.cat([VCI_image.clip(roi), 
#                           TCI_image.clip(roi),
#                           PCI_image.clip(roi),
#                           ETCI_image.clip(roi),
#                           SMCI_image.clip(roi)]) 
    
#     # Get the PCs at the specified scale and in the specified region
#     pcImage, eigenVectors = pca.getPrincipalComponents(image, args.scale, roi, args.bandNames)    
#     eigenVectors_np = np.array(eigenVectors.getInfo())[0]
#     contrib_coeff = eigenVectors_np**2
#     weights = [math.ceil(i*100)/100 for i in contrib_coeff]
#     display_weights = st.button('Weights')

# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40],
# }))



#     if display_weights:
#         st.subheader(f"Contribution coefficient of:\n VCI: {weights[0]} \n TCI: {weights[1]} \n PCI: {weights[2]} \n ETCI: {weights[3]} \n SMCI: {weights[4]}")
                    
#     input_indcies = (
#         "CMDI",
#         "ETCI",
#         "PCI",
#         "SMCI",
#         "TCI",
#         "VCI"
#     )
    
#     input_index = st.selectbox("Input Indices", input_indcies)
#     display_input_index = st.button('Display '+input_index)
    
#     # compute CMDI
#     CMDI_image = CMDI.compute_CMDI(VCI_image, TCI_image, PCI_image, ETCI_image, SMCI_image, weights, roi)
    
#     if display_input_index:
#         if input_index == 'VCI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, '+date) 
#             Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="VCI, "+date)
#             Map.to_streamlit()
    
#         elif input_index == 'TCI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, '+date) 
#             Map.add_colorbar(args.tciVis, label="TCI", orientation="vertical", layer_name="TCI, "+date)
#             Map.to_streamlit()

#         elif input_index == 'PCI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, '+date) 
#             Map.add_colorbar(args.vciVis, label="PCI", orientation="vertical", layer_name="PCI, "+date)
#             Map.to_streamlit()
    
#         elif input_index == 'ETCI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI,'+date) 
#             Map.add_colorbar(args.etciVis, label="ETCI", orientation="vertical", layer_name="ETCI, "+date)
#             Map.to_streamlit()
            
#         elif input_index == 'SMCI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, '+date) 
#             Map.add_colorbar(args.smciVis, label="SMCI", orientation="vertical", layer_name="SMCI, "+date)
#             Map.to_streamlit()
        
#         elif input_index == 'CMDI':
#             Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
#             Map.centerObject(roi, 6)
#             Map.addLayer(CMDI_image.clip(roi), args.cdmiVis, 'CMDI,'+date) 
#             Map.add_colorbar(args.cdmiVis, label="CMDI", orientation="vertical", layer_name="CMDI, "+date)
#             Map.to_streamlit()
