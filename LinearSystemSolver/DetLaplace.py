import numpy

def detLaplace(A):
# DETLAPLACE : compute the determinant using Laplace expansion
# A: square matrix represented in the type of 2D numpy.array
# using the Laplace expansion for the first row

    if not isinstance(A, numpy.ndarray):
        raise TypeError('parameter should be of type numpy.ndarray!')
    elif A.ndim != 2:
        raise TypeError("parameter's dimension is not 2!")

    n = A.shape[0]
    if n == 1:
        return A[0,0]
    else:
        d = 0.0
        for i in range(0,n):
            a = (-1)**(1+i+1)
            d += A[0,i]*a*detLaplace(numpy.hstack((A[1:n, 0:i], A[1:n, i + 1:n])))
        return d

def testDetLaplace():
    a = numpy.array([[1, 2], [3, 4]])
    print(detLaplace(numpy.array([1, 2])))
