from args import *
from dataset import *
ee.Initialize()


if __name__ == "__main__":
    args = get_main_args()
    callbacks = []

    compute_TCI = GetIndices(args, index='TCI', sum=False).get_scaled_index()
    compute_VCI = GetIndices(args, index='VCI', sum=False).get_scaled_index()
    compute_ETCI = GetIndices(args, index='ETCI', sum=True).get_scaled_index()
    compute_PCI  = GetIndices(args, index='PCI', sum=True).get_scaled_index()
    compute_SMCI = GetIndices(args, index='SMCI', sum=False).get_scaled_index()

    