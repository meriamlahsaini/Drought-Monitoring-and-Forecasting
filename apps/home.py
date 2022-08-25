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

VCI_image = ee.Image(listOfVCIImages.get(args.idx))
TCI_image = ee.Image(listOfTCIImages.get(args.idx))
PCI_image = ee.Image(listOfPCIImages.get(args.idx))
ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))


if args.visualize:
    Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6, plugin_Draw=True, Draw_export=False)
    Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, Jan 2012')
    Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, Jan 2012')
    Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, Jan 2012')
    Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI, Jan 2012')
    Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, Jan 2012')
    Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="PCI, Jan 2012")
    Map.to_streamlit()
      
    else:
        print('Processing ended')

        """
        )
     # Import libraries
    import ee
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
    
    
    listOfVCIImages = VCI.toList(VCI.size())
    listOfTCIImages = TCI.toList(TCI.size())
    listOfPCIImages = PCI.toList(PCI.size())
    listOfETCIImages = ETCI.toList(ETCI.size())
    listOfSMCIImages = SMCI.toList(SMCI.size())

    VCI_image = ee.Image(listOfVCIImages.get(args.idx))
    TCI_image = ee.Image(listOfTCIImages.get(args.idx))
    PCI_image = ee.Image(listOfPCIImages.get(args.idx))
    ETCI_image = ee.Image(listOfETCIImages.get(args.idx))
    SMCI_image = ee.Image(listOfSMCIImages.get(args.idx))
    if args.visualize:
        Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6, plugin_Draw=True, Draw_export=False)
        Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, Jan 2012')
        Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, Jan 2012')
        Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, Jan 2012')
        Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI, Jan 2012')
        Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, Jan 2012')
        Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="PCI, Jan 2012")
        Map.to_streamlit()

    else:
        print('Processing ended')
    
#     Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6, plugin_Draw=True, Draw_export=False)
#     Map.addLayer(roi, {}, 'Boundary Map') 
#     Map.to_streamlit()


   
