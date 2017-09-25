import numpy
import pynufft.pynufft as pnft
import pkg_resources
import scipy.misc
import matplotlib.cm as cm
import matplotlib.colors
import matplotlib.pyplot as pyplot

NufftObj = pnft.NUFFT()

# load the data folder
## find the relative path of data folder
# DATA_PATH = pkg_resources.resource_filename('pynufft', 'data/')
## now load the om locations
# om = numpy.load(DATA_PATH + 'om2D.npz')['arr_0']

om1 = numpy.random.randn(122880)
om2 = numpy.random.randn(122880)
om = numpy.vstack((om1,om2)).transpose()


# om is an Mx2 numpy.ndarray
print(om.shape)

# display om
pyplot.figure(0)
pyplot.plot(om[:, 0], om[:, 1], 'o')
pyplot.title('2D trajectory of M points')
pyplot.xlabel('X')
pyplot.ylabel('Y')
pyplot.axis('equal')


Nd = (256, 256)  # image dimension
Kd = (512, 512)  # k-spectrum dimension
Jd = (6, 6)  # interpolator size

NufftObj.plan(om, Nd, Kd, Jd)

# load image from scipy.misc.face()


image = scipy.misc.face(gray=True)
image = scipy.misc.imresize(image, (256, 256))
image = image.astype(numpy.float) / numpy.max(image[...])
pyplot.figure(1)
pyplot.imshow(image, cmap=cm.gray)

# Forward NUFFT transform
y = NufftObj.forward(image)

# Regular spectrum % pre-normalized spectrum
k = NufftObj.y2k(y)
k_show = numpy.fft.fftshift(k)
pyplot.figure(2)
pyplot.imshow(numpy.abs(k_show), cmap=cm.gray, norm=matplotlib.colors.Normalize(0, 1e+3))

# Adjoint transform
x2 = NufftObj.adjoint(y)
pyplot.figure(3)
pyplot.imshow(x2.real,cmap=cm.gray)

# Inverse transform using density compensation inverse_DC()
x3 = NufftObj.inverse_DC(y)
x3_display = x3 * 1.0 / numpy.max(x3[...].real)
pyplot.figure(4)
pyplot.imshow(x3_display.real, cmap=cm.gray)
pyplot.show()
