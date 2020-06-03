import meep as mp
import cmath
import numpy as np
import matplotlib.pyplot as plt

cell_size = mp.Vector3(10, 10, 10)
resolution = 10
dpml = 1
pml_layers = [mp.PML(thickness=dpml)]

wavelength = 1
fcen = 1 / wavelength

k = mp.Vector3(0, 0, 1).scale(fcen)

sigma = 1.5


def gaussian_beam(sigma, k, x0):
    def _gaussian_beam(x):
        return cmath.exp(1j * 2 * np.pi * k.dot(x - x0) - (x - x0).dot(x - x0) / (2 * sigma ** 2))

    return _gaussian_beam


src_center = mp.Vector3(0, 0, 0.5 * cell_size.z - 2 * dpml)

sources = [mp.Source(src=mp.ContinuousSource(fcen, fwidth=0.2 * fcen, start_time=10, end_time=15),
                     component=mp.Ez,
                     center=src_center,
                     size=mp.Vector3(cell_size.x, cell_size.y),
                     amp_func=gaussian_beam(sigma, k, src_center))]

sim = mp.Simulation(cell_size=cell_size,
                    sources=sources,
                    boundary_layers=pml_layers,
                    resolution=resolution)

sim.run(
    until=20)

x_plane = mp.Volume(center=mp.Vector3(0, 0, 0), size=mp.Vector3(0, cell_size.y, cell_size.x))
ez_x = sim.get_array(vol=x_plane, component=mp.Ez)
print(sim.get_array(mp.Ez).max())

plt.figure()
plt.imshow(np.flipud(np.transpose(np.real(ez_x))), interpolation='spline36', cmap='RdBu')
plt.axis('off')
plt.show()
