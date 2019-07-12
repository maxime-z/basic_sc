import numpy as np

from LinearSystemSolver.DetLaplace import detLaplace


def cramer(A, b):
    """CRAMER solves a linear system with Cramer's rule
    x = Cramer(A,b): A, b should be in type of numpy.ndarray
    The determinants are computed using the Laplace expansion"""

    if not isinstance(b, np.ndarray):
        raise TypeError('parameter b should be of type ndarray')

    n = b.size
    x = np.zeros(n)
    detA = detLaplace(A)
    for i in range(0, n):
        AI = np.hstack((A[:, 0:i], b.reshape(n, 1), A[:, i + 1:n]))
        x[i] = detLaplace(AI) / detA

    return x


def cramer_demo():
    A = np.array([[1, 0], [0, -2]])
    b = np.array([1, 1])
    print(cramer(A, b))


cramer_demo()
