import ee
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def get_main_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    arg = parser.add_argument


    arg("--roi_dir", type=str, default="users/Plottings/Zambia", help="Roi Directory")
    arg("--terra_LST", type=str, default=ee.ImageCollection("MODIS/061/MOD11A1"), help="Terra LST Image Collection")
    arg("--aqua_LST", type=str, default=ee.ImageCollection("MODIS/061/MYD11A1"), help="Aqua LST Image Collection")
    arg("--terra_NDVI", type=str, default=ee.ImageCollection("MODIS/061/MOD13Q1"), help="Terra NDVI Image Collection")
    arg("--aqua_NDVI", type=str, default=ee.ImageCollection("MODIS/061/MYD13Q1"), help="Aqua NDVI Image Collection")
    arg("--modis_ET", type=str, default=ee.ImageCollection("MODIS/006/MOD16A2"), help="ET Image Collection")
    arg("--precip", type=str, default=ee.ImageCollection("NASA/GPM_L3/IMERG_V06"), help="Precip Image Collection")
    arg("--sm", type=str, default=ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H"), help="SM Image Collection")

    arg("--years", type=list, default=[2012+i for i in range(11)], help="Study Period Range-years")
    arg("--months", type=list, default=[1, 2, 3, 4], help="Study Period Range-months")
    arg("--season", type=str, default='growing', help="Study Period Season")

    return parser.parse_args(args=[])

