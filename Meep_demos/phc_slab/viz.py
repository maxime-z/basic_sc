
import matplotlib.pyplot as plt
import numpy as np

def plot_slice(data, cmap='copper'):
    """Plot slices in 3-directions"""
    inds = np.array(data.shape) // 2
    inds[2] = data.shape[2] // 2
    fig, axs = plt.subplots(nrows=1, ncols=3)

    min, max = np.min(data), np.max(data)

    plane_x = axs[0].imshow(data[:, :, inds[2]].T, vmin=min, vmax=max, cmap=cmap)
    axs[0].set_title('xy plan at z=0')
    # fig.colorbar(plane_x, ax=axs[0])
    plane_y = axs[1].imshow(data[:, inds[1], :].T, vmin=min, vmax=max, cmap=cmap)
    axs[1].set_title('xz plan at y=0')

    plane_z = axs[2].imshow(data[inds[0], :, :].T, vmin=min, vmax=max, cmap=cmap)
    axs[2].set_title('yz plan at x=0')


def npy_to_png(filename):
    data = np.load(filename)
    n = data.shape[0]

    vmax = np.max(np.real(data))
    vmin = np.max(np.imag(data))
    for i in range(n):
        plt.imshow(np.real(data[i]), vmax=vmax, vmin=vmin, cmap='coolwarm')
        plt.savefig('%d.png'%i)


if __name__ == '__main__':
    npy_to_png('ex_leaky.npy')
