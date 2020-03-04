import numpy
import unittest

from LinearSystemSolver.BackSubstitution import *


# ELIMINATION is a solver for linear system with Gaussian elimination method
# x = Elimination(A,b) solves the linear system Ax = b using Gaussian elimination
# with partial pivoting.

# The partial pivoting serves to guarantee a well-conditioned system.
# It means that before each elimination step,we look in the current column for the
# element with largest absolute value. This element will then be chosen as the pivot.
# If we cannot find a nonzero pivot element, this means that the corresponding unknown
# is absent fromthe remaining equations, so the linear system is singular. In finite precision
# arithmetic, we cannot expect in the singular case that all possible pivot elements will
# be exactly zero, since rounding errors will produce rather small (but nonzero) elements;
# these will have to be compared with the other matrix elements in order to decide if they
# should be treated as zeros. Therefore, we will consider in the following program a pivot
# element to be zero if it is smaller than 10^−14*norm(A), a reasonable size in practice.

def elimination(A, b):
    tol = 1e-14
    parameterCheck(A, b)
    n = b.size
    normaA = numpy.linalg.norm(A, ord=1)
    A = numpy.hstack((A, b.reshape(n, 1)))
    for i in range(0, n):
        absAi = numpy.absolute(A[i:, i])
        maximum = numpy.amax(absAi)
        kmax = numpy.argmax(absAi) + i
        if maximum < tol * normaA:
            raise ValueError('A is singular')
        if i != kmax:
            h = A[kmax, :].copy()
            A[kmax, :] = A[i, :]
            A[i, :] = h
        A[i + 1:, i] = A[i + 1:, i] / A[i, i]
        subDim = n - i - 1
        subMatrix = numpy.matmul(A[i + 1:, i].copy().reshape(subDim, 1),
                                 A[i, i + 1:n + 1].copy().reshape(1, subDim + 1))
        A[i + 1:, i + 1:n + 1] = A[i + 1:, i + 1:n + 1] - subMatrix

    x = backSubstitutionsSAXPY(A[:, :n], A[:, n])
    return x


class TestElimination(unittest.TestCase):
    def testElimnation(self):
        A = numpy.array([[16, -120, 240, -140],
                         [-120, 1200, -2700, 1680],
                         [240, -2700, 6480, -4200],
                         [-140, 1680, -4200, 2800]]).astype('float')
        b = numpy.array([-4, 60, -180, 140]).astype('float')
        sol = numpy.ones(4)
        print(numpy.dot(A, sol))
        x = elimination(A, b)

        # self.assertEqual(x.all(),sol.all())
        self.assertTrue(numpy.allclose(x, sol))
