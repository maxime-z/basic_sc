"""Module for the Fabry-Perot etalon"""

import numpy as np
from numpy import pi
from scipy.constants import c
import matplotlib.pyplot as plt

a = 1
eps = 12
w = 2 * pi * c / a * np.linspace(0.25, 0.6, 200)

kx = 0.2*2*pi/a

# Incidence Region
k_air = w/c
inc_ang = np.arcsin(kx/k_air)

# Transmission Region
k_dielectric = w/(c/np.sqrt(eps))
trans_ang = np.arcsin(kx/k_dielectric)

# plot
fig, axs = plt.subplots(ncols=2, nrows=1)
axs[0].plot(w/(2*pi*c/a), np.rad2deg(inc_ang))
axs[0].set_title("Incidence Angle")
axs[0].grid()


axs[1].plot(w/(2*pi*c/a), np.rad2deg(trans_ang))
axs[1].set_title("Transmission Angle")
axs[1].grid()

plt.show()




