import h5py as h5
import numpy as np



def write2h5file():
    filename = 'h5_test'

    a1 = np.random.randn(10,2)
    a2 = np.arange(3, 222, 12)

    with h5.File(filename, 'w') as f:
        dset1 = f.create_dataset('a1', data=a1)
        dset2 = f.create_dataset('a2', data=a2)


def readh5_to_np(filename):

    f = h5.File(filename, 'r')
    #
    print(f.keys())

    # read dataset to numpy array
    name = 'a1'
    if name in f:
        a1 = f[name][()]
        print(a1)


if __name__ =='__main__':
    readh5_to_np('h5_test')