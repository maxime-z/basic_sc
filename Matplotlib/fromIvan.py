import numpy as np
import matplotlib.pyplot as plt
import time

import scipy.optimize as opt
print("")

def fx2D(x,y):
    """text."""
    return (np.exp(np.cos(y*x))*(x+1)/(0.3*y+2)/3 + \
           np.exp(np.cos(0.7*x)*np.cos(4*y))*(0.2*y+0.1))

# descreet space creation
x_lim0 = [7,7]
x_lim1 = [9,9]
nx, ny = 100, 100
hx = (x_lim1[0]-x_lim0[0])/nx
hy = (x_lim1[1]-x_lim0[1])/ny
X, Y = np.meshgrid(np.linspace(x_lim0[1], x_lim1[1], ny),np.linspace(x_lim0[0], x_lim1[0], nx))

f_vals = fx2D(X,Y)

fig1 = plt.figure()
plt.imshow(f_vals, origin='lower',
           extent=[x_lim0[0],x_lim1[0],x_lim0[1],x_lim1[1]])
plt.xlim(x_lim0[0],x_lim1[0])
plt.ylim(x_lim0[1],x_lim1[1])
plt.xlabel('first parameter')
plt.ylabel('second parameter')
plt.title('Filter reflectance')
plt.colorbar()
# plt.savefig('results/solution1.png',bbox_inches='tight')

################################################################
# FFT Games     #
################################################################

fft_freqs = np.fft.fftshift(np.fft.fft2(f_vals)) / (nx*ny)
fft_freqs_plot = 20*np.log(np.abs(fft_freqs))

NQ, NP = 20, 20
fft_trunc = fft_freqs[int(nx/2)-int(NQ/2):int(nx/2)-int(NQ/2)+NQ,
                      int(ny/2)-int(NP/2):int(ny/2)-int(NP/2)+NP]

# calculate grating vector expansion
pa = np.linspace(-NQ/2,NQ/2,NQ+1)
qa = np.linspace(-NP/2,NP/2,NP+1)

size_a = x_lim1[0] - x_lim0[0]
size_b = x_lim1[1] - x_lim0[1]
KX = 2 * np.pi * pa / size_a
KY = 2 * np.pi * qa / size_b
KX, KY = np.meshgrid(KX, KY)

fig2 = plt.figure()
plt.imshow(fft_freqs_plot, origin='lower')
plt.colorbar()
# plt.savefig('results/fft_frequencies.png',bbox_inches='tight')

fig3 = plt.figure()
plt.imshow(20*np.log(np.abs(fft_trunc)), origin='lower')
plt.colorbar()
# plt.savefig('results/fft_truncated.png',bbox_inches='tight')

UTC = np.zeros((nx,ny), dtype=complex)

for i in range(NQ):
    for j in range(NP):
        plane_wave = np.exp(1j*(KX[i,j]*X + KY[i,j]*Y))
        UTC += fft_trunc[i,j] * plane_wave

fig3 = plt.figure()
plt.imshow(np.fft.fftshift(np.real(UTC)), origin='lower',
                   extent=[x_lim0[0],x_lim1[0],x_lim0[1],x_lim1[1]])
plt.xlim(x_lim0[0],x_lim1[0])
plt.ylim(x_lim0[1],x_lim1[1])
plt.colorbar()
# plt.savefig('results/resulting_image.png',bbox_inches='tight')

plt.show()
