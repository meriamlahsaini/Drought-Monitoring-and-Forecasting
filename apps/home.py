import streamlit as st


def app():
    st.title("Home")

    st.header("Introduction")
    st.markdown(
        """
    This site demostrates how to build a multi-page [Earth Engine](https://earthengine.google.com) App using [streamlit](https://streamlit.io) and [geemap](https://geemap.org).
    You can deploy the app on various cloud platforms, such as [share.streamlit.io](https://share.streamlit.io) or [Heroku](https://heroku.com).
    Make sure you set `EARTHENGINE_TOKEN='your-token'` as an environment variable (secret) on the cloud platform.
    - **Web App:** <https://gishub.org/geemap-apps>
    - **Github:** <https://github.com/Rim-chan/geemap-apps>
    """
    )


    st.header("Example")
    with st.expander("See Source Code"):
        st.code(
            """        
# Import libraries
import ee
import geemap.foliumap as geemap
from dataset import GetIndices
from args import get_main_args


args = get_main_args()
roi = ee.FeatureCollection(args.roi_dir)

Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6, plugin_Draw=True, Draw_export=False)
Map.addLayer(roi, {}, 'Boundary Map') 
Map.to_streamlit()

        """
        )
     # Import libraries
    import ee
    import geemap.foliumap as geemap
    from dataset import GetIndices
    from args import get_main_args

    
    args = get_main_args()
    roi = ee.FeatureCollection(args.roi_dir)
    
    Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6, plugin_Draw=True, Draw_export=False)
    Map.addLayer(roi, {}, 'Boundary Map') 
    Map.to_streamlit()


   
