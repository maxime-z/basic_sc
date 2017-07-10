# CHOLESKY compute the Cholesky decomposition of a matrix
#  R =  cholesky(A) computes the decomposed matrix R that A = R'R

# For symmetric positive definite matrix, it is possible to decompose it into
# the product of a upper triangular matrix with it's transposed counterpart
#    A =  R^T * R

import numpy
import unittest


def cholesky(A):
    if not (isinstance(A, numpy.ndarray)):
        raise TypeError('Parameter A should be of type numpy.ndarray')
    elif A.ndim != 2:
        raise ValueError('Parameter A shoud be 2 dimensional')

    n = A.shape[0]
    R = A * 0.0
    for j in range(0, n):
        v = A[j, j:n]
        if j > 0:
            v = v - numpy.matmul(numpy.transpose(R[:j, j]), R[:j, j:n])
        if v[0] <= 0:
            raise ValueError('Matrix A is not positive definite')
        else:
            h = 1.0 / numpy.sqrt(v[0])
        R[j, j:n] = v * h

    return R


class TestCholesky(unittest.TestCase):
    def testElimnation(self):
        A = numpy.array([[16, -120, 240, -140],
                         [-120, 1200, -2700, 1680],
                         [240, -2700, 6480, -4200],
                         [-140, 1680, -4200, 2800]]).astype('float')
        R = numpy.array([[4., -30., 60., -35., ],
                         [-0., 17.32050808, -51.96152423, 36.37306696],
                         [0., -0., 13.41640786, -15.65247584],
                         [-0., 0., -0., 2.64575131]])

        self.assertTrue(numpy.allclose(cholesky(A), R))
