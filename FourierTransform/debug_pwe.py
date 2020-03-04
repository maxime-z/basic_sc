"""Module to debug pwe 2d for 1d problem"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fftn, fftshift

a = np.array([1] * 10 + [1] * 5 + [1] * 10)

a = np.ones((5,5))
a[2,:] = 5

fa = fftshift(fftn(a)) / np.prod(a.shape)

fig, ax = plt.subplots(nrows=1, ncols=3)
ax[0].imshow(a)
ax[1].imshow(np.real(fa))
ax[2].imshow(np.imag(fa))
plt.show()
