"""Modelling a uniform medium of an artifical dispersive material
https://meep.readthedocs.io/en/latest/Python_Tutorials/Material_Dispersion/
"""

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

"""Since this is a uniform medium, our computational cell can actually be of zero size (i.e. one pixel), 
where we will use Bloch-periodic boundary conditions to specify the wavevector k."""

cell = mp.Vector3()
resolution = 20

susceptibilities = [mp.LorentzianSusceptibility(frequency=1.1, gamma=1e-5, sigma=0.5),
                    mp.LorentzianSusceptibility(frequency=0.5, gamma=0.1, sigma=2e-5)]

default_material = mp.Medium(epsilon=2.25, E_susceptibilities=susceptibilities)
# default_material = mp.Medium(epsilon=2.25)

"""
In fact, there is a range of frequencies from 1.1 to 1.2161 where ε is negative. 
In this range, no propagating modes exist — it is actually a kind of electromagnetic band gap associated with 
<polariton resonances> in a material. 
"""

fcen = 1.0
df = 2.0

sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df), component=mp.Ez, center=mp.Vector3())]

kmin = 0.3
kmax = 2.2
k_interp = 10
kpts = mp.interpolate(k_interp, [mp.Vector3(kmin), mp.Vector3(kmax)])
sim = mp.Simulation(cell_size=cell,
                    geometry=[],
                    sources=sources,
                    default_material=default_material,
                    resolution=20)

all_freqs = sim.run_k_points(200, kpts)

# for fs, kx in zip(all_freqs, [v.x for v in kpts]):
#     for f in fs:
#         print("eps:, {.6f}, {.6f}, {.6f}".format(f.real, f.imag, (kx / f)**2))

kx = np.array([v.x for v in kpts])
freqs = np.array(all_freqs)

# plot frequency to kx
plt.figure()
for i in range(freqs.shape[1]):
    plt.plot(kx, np.real(freqs[:, i]))

# plot epsilon to frequency
epsilon = np.zeros(freqs.shape, dtype=complex)
for i, kx in enumerate(kx):
    epsilon[i] = (kx / freqs[i, :]) ** 2

fig, axs = plt.subplots(ncols=2)
for i in range(freqs.shape[1]):
    axs[0].scatter(np.real(freqs[:, i]), np.real(epsilon[:, i]))
    axs[1].scatter(np.real(freqs[:, i]), np.imag(epsilon[:, i]))

axs[0].set_ylim([-2, 6])
axs[0].grid(True)
axs[0].set_ylabel(r'Re $\epsilon$')

axs[1].set_ylim([0, 1.2e-4])
axs[1].grid(True)
axs[1].set_ylabel(r'Im $\epsilon$')
plt.show()
