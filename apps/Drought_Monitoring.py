import streamlit as st
import ee, geemap
geemap.ee_initialize()
import gc
import math
import numpy as np
from dataset import GetIndices
from pca import getPrincipalComponents
from CMDI import compute_CMDI
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
    #     import geemap.foliumap as geemap: don't use it, it messes up with the API initialization
    
    
#     st.subheader('Define ROI')
    st.write("""####Define ROI""")
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

        
    ## INPUT INDICES: VCI, TCI, PCI, ETCI, SMCI
    st.subheader('Compute Input Indices')
    
    seasons = (
        "Sowing",
        "Growing",
    )
        
    season = st.selectbox("Season", seasons)
    
    args.season = season
   
    TCI = GetIndices(args, roi, index='TCI', sum=False).get_scaled_index()
    VCI = GetIndices(args, roi, index='VCI', sum=False).get_scaled_index()
    ETCI = GetIndices(args, roi, index='ETCI', sum=True).get_scaled_index()
    PCI  = GetIndices(args, roi, index='PCI', sum=True).get_scaled_index()
    SMCI = GetIndices(args, roi, index='SMCI', sum=False).get_scaled_index()
    
    listOfVCIImages = VCI.toList(VCI.size())
    listOfTCIImages = TCI.toList(TCI.size())
    listOfPCIImages = PCI.toList(PCI.size())
    listOfETCIImages = ETCI.toList(ETCI.size())
    listOfSMCIImages = SMCI.toList(SMCI.size())
    
    
    month = ['January', 'February', 'March', 'April']
    year = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
    dates = [i+' '+j for j in year for i in month]
    date = st.selectbox("Date", tuple(dates))
    
#     image_idx = st.slider("Image", 0, VCI.size().getInfo(), 0)                          # display month and year
#     args.idx = image_idx
    args.idx =  tuple(dates).index(date)
    VCI_image = ee.Image(listOfVCIImages.get(args.idx))
    TCI_image = ee.Image(listOfTCIImages.get(args.idx))
    PCI_image = ee.Image(listOfPCIImages.get(args.idx))
    ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
    SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))
   

            
    ## PCA
    st.subheader('Compute CMDI')
    
    gc.collect()
    
    image = ee.Image.cat([VCI_image.clip(roi), 
                          TCI_image.clip(roi),
                          PCI_image.clip(roi),
                          ETCI_image.clip(roi),
                          SMCI_image.clip(roi)]) 
    
    # Get the PCs at the specified scale and in the specified region
    pcImage, eigenVectors = getPrincipalComponents(image, args.scale, roi, args.bandNames)    
    eigenVectors_np = np.array(eigenVectors.getInfo())[0]
    contrib_coeff = eigenVectors_np**2
    weights = [math.ceil(i*100)/100 for i in contrib_coeff]
    display_weights = st.button('Weights')
    if display_weights:
        st.subheader(f"Contribution coefficient of:\n VCI: {weights[0]} \n TCI: {weights[1]} \n PCI: {weights[2]} \n ETCI: {weights[3]} \n SMCI: {weights[4]}")
                    

    # compute CMDI
    CMDI_image = compute_CMDI(VCI_image, TCI_image, PCI_image, ETCI_image, SMCI_image, weights, roi)
    
     input_indcies = (
        "VCI",
        "TCI",
        "PCI",
        "ETCI",
        "SMCI",
        "CMDI"
    )
    
    input_index = st.selectbox("Input Indices", input_indcies)
    display_input_index = st.button('Display '+input_index)
    
    if display_boundary_map:
        Map = geemap.Map(zoom = 6, plugin_Draw=True, Draw_export=False)
        Map.centerObject(roi, 6)
        
        if input_index == 'VCI':
            Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, Jan 2012') 
            Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="VCI, Jan 2012")
            Map.to_streamlit()
    
        elif input_index == 'TCI':
            Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, Jan 2012') 
            Map.add_colorbar(args.tciVis, label="TCI", orientation="vertical", layer_name="TCI, Jan 2012")
            Map.to_streamlit()

        elif input_index == 'PCI':
            Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, Jan 2012') 
            Map.add_colorbar(args.vciVis, label="PCI", orientation="vertical", layer_name="PCI, Jan 2012")
            Map.to_streamlit()
    
        elif input_index == 'ETCI':
            Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI, Jan 2012') 
            Map.add_colorbar(args.etciVis, label="ETCI", orientation="vertical", layer_name="ETCI, Jan 2012")
            Map.to_streamlit()
            
        elif input_index == 'SMCI':
            Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, Jan 2012') 
            Map.add_colorbar(args.smciVis, label="SMCI", orientation="vertical", layer_name="SMCI, Jan 2012")
            Map.to_streamlit()
        
        elif input_index == 'CMDI':
            Map.addLayer(CMDI_image.clip(roi), args.cdmiVis, 'CMDI, Jan 2012') 
            Map.add_colorbar(args.cdmiVis, label="CMDI", orientation="vertical", layer_name="CMDI, Jan 2012")
            Map.to_streamlit()
