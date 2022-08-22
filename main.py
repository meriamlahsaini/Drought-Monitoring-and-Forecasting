from args import *
from dataset import *
ee.Initialize()


if __name__ == "__main__":
    args = get_main_args()
    callbacks = []

    compute_TCI = GetIndices(args, index='TCI', sum=False).get_scaled_index()
    print('TCI dataset:'+ str(compute_TCI.size().getInfo()))

    compute_VCI = GetIndices(args, index='VCI', sum=False).get_scaled_index()
    print('VCI dataset:'+ str(compute_VCI.size().getInfo()))

    compute_ETCI = GetIndices(args, index='ETCI', sum=True).get_scaled_index()
    print('ETCI dataset:'+ str(compute_ETCI.size().getInfo()))

    compute_PCI  = GetIndices(args, index='PCI', sum=True).get_scaled_index()
    print('PCI dataset:'+ str(compute_PCI.size().getInfo()))

    compute_SMCI = GetIndices(args, index='SMCI', sum=False).get_scaled_index()
    print('SMCI dataset:'+ str(compute_SMCI.size().getInfo()))

    