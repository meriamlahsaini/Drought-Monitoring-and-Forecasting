import streamlit as st


def app():
    st.title("Drought Forecasting")

    countries = (
        "Zambia",
        "Ethiopia"
    )

    country = st.selectbox("Country", countries)
   


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
