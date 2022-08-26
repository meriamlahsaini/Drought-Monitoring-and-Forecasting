import streamlit as st




def app():
    st.title("Drought Forecasting")
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
    import ee
    import geemap.foliumap as geemap
    from args import get_main_args
    args = get_main_args()
    

    roi = ee.FeatureCollection(args.afghanistan_dir)

        

    Map = geemap.Map(plugin_Draw=True, Draw_export=False)
    Map.centerObject(roi, 6)
    Map.addLayer(roi, {}, country +'Boundary Map') 
    Map.to_streamlit()
