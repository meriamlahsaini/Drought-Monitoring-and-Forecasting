from args import *
from dataset import *
import ee, geemap
ee.Initialize()


if __name__ == "__main__":
    args = get_main_args()
    callbacks = []
    
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

    VCI_image = ee.Image(listOfVCIImages.get(args.index))
    TCI_image = ee.Image(listOfTCIImages.get(args.index))
    PCI_image = ee.Image(listOfPCIImages.get(args.index))
    ETCI_image = ee.Image(listOfETCIImages.get(args.index))
    SMCI_image = ee.Image(listOfSMCIImages.get(args.index))


    if args.visualize == True:
        Map = geemap.Map(center=[-13.4751, 28.6304], zoom = 6) 
        Map.addLayer(VCI_image.clip(roi), args.vciVis, 'VCI, Jan 2012')
        Map.addLayer(TCI_image.clip(roi), args.tciVis, 'TCI, Jan 2012')
        Map.addLayer(PCI_image.clip(roi), args.pciVis, 'PCI, Jan 2012')
        Map.addLayer(ETCI_image.clip(roi), args.etciVis, 'ETCI, Jan 2012')
        Map.addLayer(SMCI_image.clip(roi), args.smciVis, 'SMCI, Jan 2012')
        Map.add_colorbar(args.vciVis, label="VCI", orientation="vertical", layer_name="PCI, Jan 2012")
        # Map

        Map.addLayerControl()
        Map