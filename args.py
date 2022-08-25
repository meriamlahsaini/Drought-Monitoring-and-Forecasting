from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def get_main_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    arg = parser.add_argument
    arg("--roi_dir", type=str, default="users/Plottings/Zambia", help="Roi Directory")
    arg("--terra_LST_dir", type=str, default="MODIS/061/MOD11A1", help="Terra LST Image Collection")
    arg("--aqua_LST_dir", type=str, default="MODIS/061/MYD11A1", help="Aqua LST Image Collection")
    arg("--terra_NDVI_dir", type=str, default="MODIS/061/MOD13Q1", help="Terra NDVI Image Collection")
    arg("--aqua_NDVI_dir", type=str, default="MODIS/061/MYD13Q1", help="Aqua NDVI Image Collection")
    arg("--modis_ET_dir", type=str, default="MODIS/006/MOD16A2", help="ET Image Collection")
    arg("--precip_dir", type=str, default="NASA/GPM_L3/IMERG_V06", help="Precip Image Collection")
    arg("--sm_dir", type=str, default="NASA/GLDAS/V021/NOAH/G025/T3H", help="SM Image Collection")
    arg("--years", type=list, default=[2012+i for i in range(11)], help="Study Period Range-years")
    arg("--months", type=list, default=[1, 2, 3, 4], help="Study Period Range-months")
    arg("--season", type=str, default='growing', help="Study Period Season")
    arg("--visualize", type=bool, default=False, help="Option to Display Maps")
    arg("--idx", type=int, default=0, help="Index of Image to Display")
    arg("--vciVis", type=dict, default={'min':0.0, 'max': 1.0,
                                        'palette': ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', 
                                        '99B718', '74A901','66A000', '529400', '3E8601', 
                                        '207401', '056201', '004C00', '023B01','012E01', 
                                        '011D01', '011301']}, help="Visualization Parameters of VCI")
    arg("--tciVis", type=dict, default={'min':0.0, 'max': 1.0,
                                        'palette': ['040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
                                                    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
                                                    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
                                                    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
                                                    'ff0000', 'de0101', 'c21301', 'a71001', '911003']}, help="Visualization Parameters of TCI")
    arg("--pciVis", type=dict, default={'min':0.0, 'max': 1.0,
                                        'palette': ['d7191c','fdae61','ffffbf','abdda4','2b83ba']}, help="Visualization Parameters of PCI")
    arg("--etciVis", type=dict, default={'min':0.0, 'max': 1.0,
                                        'palette': ['blue', 'orange', 'red']}, help="Visualization Parameters of ETCI")
    arg("--smciVis", type=dict, default={'min':0.0, 'max': 1.0,
                                        'palette': ['0300ff', '418504','efff07', 'efff07', 'ff0303']}, help="Visualization Parameters of SMCI")    
    arg("--scale", type=int, default=250, help="Downsampling Scale")
    arg("--bandNames", type=list, default=['VCI', 'TCI', 'PCI', 'ETCI', 'SMCI'], help="Downsampling Scale")


    return parser.parse_args()
