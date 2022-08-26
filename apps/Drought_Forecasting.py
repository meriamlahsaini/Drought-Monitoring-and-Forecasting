import streamlit as st


def app():
    st.title("Drought Forecasting")

    # import the necessary libraries
    import ee
    import geemap.foliumap as geemap
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
