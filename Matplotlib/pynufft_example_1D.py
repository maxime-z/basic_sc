import pynufft.pynufft as pnft
import numpy
import matplotlib.pyplot as pyplot

NufftObj = pnft.NUFFT()

om = numpy.random.randn(1512, 1)
# om is an M x 1 ndarray: locations of M points. *om* is normalized between [-pi, pi]
# Here M = 1512
Nd = (256,)
Kd = (512,)
Jd = (6,)
NufftObj.plan(om, Nd, Kd, Jd)

# generate a time series of a pulse signal
time_data = numpy.zeros(256, )
time_data[96:128 + 32] = 1.0
pyplot.plot(time_data)
pyplot.ylim(-1, 2)

# forward Fourier Transform
y = NufftObj.forward(time_data)
pyplot.figure()
pyplot.plot(om, y.real, '.', label='real')
pyplot.plot(om, y.imag, 'r.', label='imag')
pyplot.legend()

# adjoint transform
x2 = NufftObj.adjoint(y)
pyplot.figure()
pyplot.plot(x2.real, 'b.-', label='real')
pyplot.plot(x2.imag, 'r.-', label='imag')
pyplot.plot(time_data, 'k', label='original signal')
# pyplot.ylim(-1, 2)
pyplot.legend()

# Inverse transform through density compensation
x3 = NufftObj.inverse_DC(y)
pyplot.figure()
pyplot.plot(x3.real, 'b.-', label='real')
pyplot.plot(x3.imag, 'r.-', label='imag')
pyplot.plot(time_data, 'k', label='original signal')
pyplot.ylim(-1, 2)
pyplot.legend()


pyplot.show()
