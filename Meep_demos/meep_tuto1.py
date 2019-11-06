"""FDTD simulation to show the self-collimation phenomenon"""

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

"""Problem definition and execution"""

#  cell indicates the computational domain
cell = mp.Vector3(16, 8, 0)

geometry = [mp.Block(mp.Vector3(mp.inf, 1, mp.inf),
                     center=mp.Vector3(),
                     material=mp.Medium(epsilon=12))]

sources = [mp.Source(src=mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(-7, 0))]

# Absorbing material of thickness 1, placed inside the computational cell
pml_layers = [mp.PML(1.0)]

# Resolution indicates number of element(discretization) per unit length.
resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=200)

"""Post-processing"""
# plot the epsilon and mu values
eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
mu_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Permeability)

fig, axs = plt.subplots(2, 2)

axs[0, 0].imshow(eps_data.transpose(), cmap='binary')
axs[0, 1].imshow(mu_data.transpose(), cmap='binary')

# plot the z-component of electric field in the domain
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
hy_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Hy)
axs[1, 0].imshow(ez_data.transpose(), cmap='RdBu')
axs[1, 1].imshow(hy_data.transpose(), cmap='RdBu')

plt.show()
