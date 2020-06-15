"""Module to show the relation between time-width and frequency-width
https://meep.readthedocs.io/en/latest/Python_User_Interface/#gaussiansource
"""
import numpy as np
import matplotlib.pyplot as plt

"""The width w used in the Gaussian. No default value. You can instead specify fwidth=x, 
which is a synonym for width=1/x (i.e. the frequency width is proportional to the inverse of the temporal width)."""


def gaussian_source_in_time(t: float, t0, w: float, f: float):
    """Amplitude in function of time
    Args:
        t(float): time
        t0(float): center
        width(float): width
        f(float): center frequency

    Return:
        (float) amplitude
    """
    return np.exp(-2j * np.pi * f * t - (t - t0) ** 2 / (2 * w * w))


t0 = 30
width = 2
f = 2

# time sampling point
t = np.linspace(0, 100, 200)

amplitude = gaussian_source_in_time(t, t0, width, f)
sp = np.fft.fft(amplitude)
freq = np.fft.fftfreq(sp.shape[-1])

fig, axs = plt.subplots(ncols=2)
axs[0].plot(t, amplitude)
axs[0].plot(t, np.abs(amplitude), 'r-.')
axs[0].set_title('Time Domain')

axs[1].plot(freq, sp.real, 'b', freq, sp.imag, 'r')
axs[1].set_title('Frequency Domain')

plt.show()
