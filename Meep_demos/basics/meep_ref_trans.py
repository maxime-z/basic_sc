"""FDTD simulation for reflectance/transmittance spectrum"""

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 10

sx = 16
sy = 32
cell = mp.Vector3(sx, sy, 0)

dpml = 1.0
pml_layers = [mp.PML(dpml)]

pad = 4
w = 1

wvg_xcen = 0.5 * (sx - w - 2 * pad)
wvg_ycen = -0.5 * (sy - w - 2 * pad)

geometry = [mp.Block(size=mp.Vector3(mp.inf, w, mp.inf),
                     center=mp.Vector3(0, wvg_ycen, 0),
                     material=mp.Medium(epsilon=12))]

fcen = 0.15
df = 0.1

sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df),
                     component=mp.Ez,
                     center=mp.Vector3(-0.5 * sx + dpml, wvg_ycen, 0),
                     size=mp.Vector3(0, w, 0))]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)
nfreq = 100

# reflected flux
refl_fr = mp.FluxRegion(center=mp.Vector3(-0.5 * sx + dpml + 0.5, wvg_ycen, 0),
                        size=mp.Vector3(0, 2 * w, 0))

refl = sim.add_flux(fcen, df, nfreq, refl_fr)

# transmitted flux
tran_fr = mp.FluxRegion(center=mp.Vector3(0.5 * sx - dpml, wvg_ycen, 0),
                        size=mp.Vector3(0, 2 * w, 0))
tran = sim.add_flux(fcen, df, nfreq, tran_fr)

pt = mp.Vector3(0.5 * sx - dpml - 0.5, wvg_ycen)

sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, pt, 1e-3))

# for normalization run, save flux fields data for reflection plane
straight_refl_data = sim.get_flux_data(refl)

# save incident power for transmission plane
straight_tran_flux = mp.get_fluxes(tran)

"""Normal Run"""
sim.reset_meep()

geometry = [
    mp.Block(mp.Vector3(sx - pad, w, mp.inf), center=mp.Vector3(-0.5 * pad, wvg_ycen), material=mp.Medium(epsilon=12)),
    mp.Block(mp.Vector3(w, sy - pad, mp.inf), center=mp.Vector3(wvg_xcen, 0.5 * pad), material=mp.Medium(epsilon=12))]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

# reflected flux
refl = sim.add_flux(fcen, df, nfreq, refl_fr)

tran_fr = mp.FluxRegion(center=mp.Vector3(wvg_xcen, 0.5 * sy - dpml - 0.5, 0), size=mp.Vector3(2 * w, 0, 0))
tran = sim.add_flux(fcen, df, nfreq, tran_fr)

# for normal run, load negated fields to subtract incident from refl. fields
sim.load_minus_flux_data(refl, straight_refl_data)

pt = mp.Vector3(wvg_xcen, 0.5 * sy - dpml - 0.5)

sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, pt, 1e-3))

bend_refl_flux = mp.get_fluxes(refl)
bend_tran_flux = mp.get_fluxes(tran)

flux_freqs = mp.get_flux_freqs(refl)

wl = []
Rs = []
Ts = []
for i in range(nfreq):
    wl = np.append(wl, 1 / flux_freqs[i])
    Rs = np.append(Rs, -bend_refl_flux[i] / straight_tran_flux[i])
    Ts = np.append(Ts, bend_tran_flux[i] / straight_tran_flux[i])

if mp.am_master():
    plt.figure()
    plt.plot(wl, Rs, 'bo-', label='reflectance')
    plt.plot(wl, Ts, 'ro-', label='transmittance')
    plt.plot(wl, 1 - Rs - Ts, 'go-', label='loss')
    plt.axis([5.0, 10.0, 0, 1])
    plt.xlabel("wavelength (μm)")
    plt.legend(loc="upper right")


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

"""
CONVERGENCE TEST:
We should also check whether our data is converged. 
We can do this by increasing the resolution and cell size and seeing by how much the numbers change. 
sx=32
xy=62
"""
