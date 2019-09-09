import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import numpy as np


def example_case():
    num_bands = 3
    resolution = 32
    k_point = [mp.Vector3(),
               mp.Vector3(0.5),
               mp.Vector3(0.5, 0.5),
               mp.Vector3()]
    k_points = mp.interpolate(40, k_point)

    geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]
    geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1))
    ms = mpb.ModeSolver(num_bands=num_bands,
                        k_points=k_points,
                        geometry=geometry,
                        geometry_lattice=geometry_lattice,
                        resolution=resolution)
    ms.run_te()
    return ms


def data_visualization(modal_solver: mpb.ModeSolver):
    """Plot lattice structure and band diagram(Dispersion relation)"""
    plt.figure()
    ax1 = plt.subplot(121)
    md = mpb.MPBData(rectify=True, periods=3, resolution=64)
    eps = modal_solver.get_epsilon()
    converted_eps = md.convert(eps)
    ax1.imshow(converted_eps.T)
    ax1.axis('off')
    ax1.set_title('Relative Permittivity')

    ax2 = plt.subplot(122)
    mu = modal_solver.get_mu()
    couverted_mu = md.convert(mu)
    ax2.imshow(couverted_mu.T)
    ax2.set_title('Relative Permittivity')
    ax2.axis('off')



if __name__ == '__main__':
    modal_solver = example_case()
    data_visualization(modal_solver)
    plt.show()
