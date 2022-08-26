import streamlit as st


def app():
    st.title("Drought Monitoring")

    # import the necessary libraries
    import ee, geemap
    import geemap.foliumap as geemap
    import gc
    import numpy as np
    from dataset import GetIndices
    from args import get_main_args
    args = get_main_args()
    
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
    
    st.subheader('Define ROI')
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
    st.subheader(args.season)
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
    
    image_idx = st.slider("Image", 0, VCI.size().getInfo(), 0)                          # display month and year
    args.idx = image_idx
    VCI_image = ee.Image(listOfVCIImages.get(args.idx))
    TCI_image = ee.Image(listOfTCIImages.get(args.idx))
    PCI_image = ee.Image(listOfPCIImages.get(args.idx))
    ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
    SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))
    
    
    input_indcies = (
        "VCI",
        "TCI",
        "PCI",
        "ETCI",
        "SMCI"
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

            
    ## PCA
#     st.subheader('Compute CMDI')
    
#     gc.collect()
#     Image = ee.Image.cat([VCI_image.clip(roi), 
#                           TCI_image.clip(roi),
#                           PCI_image.clip(roi),
#                           ETCI_image.clip(roi),
#                           SMCI_image.clip(roi)]) 
    
#     # Get the PCs at the specified scale and in the specified region
#     pcImage, eigenVectors = getPrincipalComponents(Image, args.scale, roi, args.bandNames)    
#     eigenVectors_np = np.array(eigenVectors.getInfo())[0]
#     contrib_coeff = eigenVectors_np**2
#     weights = [math.ceil(i*100)/100 for i in contrib_coeff]
#     display_weights = st.button('Weights')
#     st.subheader(f"Contribution coefficient of:\n VCI {weights[0]} \n TCI {weights[1]} \n PCI {weights[2]} \n ETCI {weights[3]} \n SMCI {weights[4]}")
                    

    # compute CMDI
#     country = st.button("Compute CMDI", countries)
#     CMDI_image = compute_CMDI(VCI_image, TCI_image, PCI_image, ETCI_image, SMCI_image, weights, roi)
    
