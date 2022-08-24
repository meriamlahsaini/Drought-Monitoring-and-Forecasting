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

    with st.expander("Where to find your Earth Engine token?"):
        st.markdown(
            """
            - **Windows:** `C:/Users/USERNAME/.config/earthengine/credentials`
            - **Linux:** `/home/USERNAME/.config/earthengine/credentials`
            - **macOS:** `/Users/USERNAME/.config/earthengine/credentials`
            """
        )

    st.header("Example")
    with st.expander("See Source Code"):
        st.code(
            """        
# Import libraries
import ee
ee.Initialize()
import geemap.foliumap as geemap
from dataset import GetIndices
from args import get_main_args


args = get_main_args()
    
roi = ee.FeatureCollection(args.roi_dir)

TCI = GetIndices(args, roi, index='TCI', sum=False).get_scaled_index()
VCI = GetIndices(args, roi, index='VCI', sum=False).get_scaled_index()
ETCI = GetIndices(args, roi, index='ETCI', sum=True).get_scaled_index()
PCI  = GetIndices(args, roi, index='PCI', sum=True).get_scaled_index()
SMCI = GetIndices(args, roi, index='SMCI', sum=False).get_scaled_index()

        """
        )
     # Import libraries
    import ee
    import geemap.foliumap as geemap
    from dataset import GetIndices
    from args import get_main_args
    from google.oauth2.credentials import Credentials
    
    #set up credentials
    credentials = Credentials(
        None,
        refresh_token="1//0dcJrJefrRht5CgYIARAAGA0SNwF-L9Irmei5_CU3CUT5BKPZqpqs-GptW0snXkm1pX0TvpwvIuPsY_aeXmUMCMmHbKomlCrUg4Y",
        token_uri=ee.oauth.TOKEN_URI,
        client_id=ee.oauth.CLIENT_ID,
        client_secret=ee.oauth.CLIENT_SECRET,
        scopes=ee.oauth.SCOPES)
    ee.Initialize(credentials=credentials)
    
    args = get_main_args()
    
    roi = ee.FeatureCollection(args.roi_dir)

    TCI = GetIndices(args, roi, index='TCI', sum=False).get_scaled_index()
    VCI = GetIndices(args, roi, index='VCI', sum=False).get_scaled_index()
    ETCI = GetIndices(args, roi, index='ETCI', sum=True).get_scaled_index()
    PCI  = GetIndices(args, roi, index='PCI', sum=True).get_scaled_index()
    SMCI = GetIndices(args, roi, index='SMCI', sum=False).get_scaled_index()

   
