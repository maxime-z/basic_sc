import numpy
import unittest

# BACKSUBSTITUTION solves a linear system by back substitution
# x = backSubstitution(U,b) solves Ux = b, U is supposed to be upper triangular matrix
# the parameters should be of type numpy.ndarray

# ATTENTION!!! the diagonal term of U should be non-zero(in the meaning of finite precision arithmetic)
def backSubstitutions(U, b):
    parameterCheck(U,b)
    n = b.size
    x = b.copy()
    for i in range(n-1,-1,-1):
        for j in range(i+1,n):
            x[i] -= U[i,j]*x[j]
        x[i] /= U[i,i]
    return x


#BACKSUBSTITUTIONSAXPY is the SAXPY variant of BACKSUBSTITUTIONS
#SAXPY which stands for "scalar a.x plus y", is a basic linear algebra operation that
#  overwrites a vector y with the result of ax+y, where a is a scalar.This operation is
#  implemented efficiently in several libraries that can be tuned to the machine on which
#  the code is executed.

def backSubstitutionsSAXPY(U,b):
    parameterCheck(U,b)
    n = b.size
    x = b.copy()
    for i in range(n-1,-1,-1):
        x[i] /= U[i,i]
        x[:i] = x[:i]-U[:i,i]*x[i]
    return x

# check the parameters types and dimensions
def parameterCheck(U,b):
    if not (isinstance(U,numpy.ndarray) and isinstance(b,numpy.ndarray)):
        raise TypeError('Parameters both should be of type numpy.ndarray')
    if not (U.ndim == 2 and b.ndim == 1):
        raise TypeError('Dimension error found for U or b')

#unit test
class TestBackSubstitution(unittest.TestCase):

    def testBackSubstituations(self):
        U = numpy.array([[3, 5, -1],[0,2,-7],[0,0,-4]])
        b = numpy.array([2,-16,-8])
        x = backSubstitutions(U, b)
        self.assertEqual(x.all(),(numpy.array([3,-1,2])).all())

    def testBackSubstituationsSAXPY(self):
        U = numpy.array([[3, 5, -1], [0, 2, -7], [0, 0, -4]])
        b = numpy.array([2, -16, -8])
        x = backSubstitutionsSAXPY(U, b)
        self.assertEqual(x.all(), (numpy.array([3, -1, 20])).all())


