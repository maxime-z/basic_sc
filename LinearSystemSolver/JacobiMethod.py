"""A demo of Jacobi Method to solve linear system iteratively"""
import numpy as np


def solve_jacobi(A, b, it_limit: int):
    """Solve iteratively the linear system Ax = b
    - Variations: start point choice & stop criteria
    """
    A_diag = np.diag(A)
    x = b / A_diag
    for i in range(it_limit):
        x = (b - (A @ x - x * A_diag)) / A_diag

    return x


if __name__ == '__main__':
    A = np.array([[2, -1, 0],
                  [-1, 2, -1],
                  [0, -1, 2]])
    b = np.array([0, 1, 2])

    x = solve_jacobi(A, b, 100)

    print(x)

    print(A @ x)
