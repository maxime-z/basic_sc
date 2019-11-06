"""Meep tutorial: A 90 degree bend"""

import meep as mp
import matplotlib.pyplot as plt

cell = mp.Vector3(16, 16, 0)

geometry = [mp.Block(mp.Vector3(12, 1, mp.inf),
                     center=mp.Vector3(-2.5, -3.5),
                     material=mp.Medium(epsilon=12)),
            mp.Block(mp.Vector3(1, 12, mp.inf),
                     center=mp.Vector3(3.5, 2),
                     material=mp.Medium(epsilon=12))]

pml_layers = [mp.PML(1.0)]

sources = [mp.Source(mp.ContinuousSource(wavelength=2 * (11 * 0.5), width=20),
                     component=mp.Ez,
                     center=mp.Vector3(-7, -3.5),
                     size=mp.Vector3(0, 1))]

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_beginning(mp.output_mu),
        mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
        until=200)


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
