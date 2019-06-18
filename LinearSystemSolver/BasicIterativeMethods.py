"""A demo of Basic Iterative Method for linear system resolving

- Jacobi Iteration
- Gauss-Seidal Iteration
- SOR - Successive Over Relaxation
"""

import matplotlib.pyplot as plt
import numpy as np


def solve_jacobi(A, b, iter_limit: int):
    """Solve iteratively the linear system Ax = b through Jacobi Iteration
    - Variations: start point choice & stop criteria
    """
    a_diag = np.diag(A)
    x = b / a_diag
    residu = np.zeros(iter_limit)
    for i in range(iter_limit):
        x = (b - (A - np.diag(a_diag)) @ x) / a_diag
        residu[i] = np.linalg.norm(A @ x - b)
    return x, residu


def solve_gauss_seidal(A, b, iter_limit: int):
    """Solve iteratively linear system Ax = b through Gauss-Seidel Iteration"""
    a_diag = np.diag(A)
    x = b / a_diag
    residu = np.zeros(iter_limit)
    for n in range(iter_limit):
        for i in range(b.size):
            x[i] = (b[i] - (A[i, :] @ x - x[i] * a_diag[i])) / a_diag[i]
        residu[n] = np.linalg.norm(A @ x - b)
    return x, residu


def solve_sor(A, b, iter_limit: int, w=1.2):
    """Solve iteratively linear system Ax = b through Successive Over Relaxation(SOR)
    - This demo implemented Gauss-Seidal's iteration.
    """
    assert 1 < w < 2, "Relaxation coefficient should be chosen in (1, 2)!"

    a_diag = np.diag(A)
    x = b / a_diag
    residu = np.zeros(iter_limit)
    for n in range(iter_limit):
        for i in range(b.size):
            x[i] = (1 - w) * x[i] + w * (b[i] - (A[i, :] @ x - x[i] * a_diag[i])) / a_diag[i]
        residu[n] = np.linalg.norm(A @ x - b)
    return x, residu


def plot_residual(iter_num, residus, name):
    """Visualization the residual with repect to iterations"""
    plt.plot(np.arange(1, iter_num + 1), residus, label=name)
    plt.ylabel('|Ax-b|')
    plt.xlabel('Iteration Number')
    plt.grid(True)


if __name__ == '__main__':
    A = np.array([[2, -1, 0],
                  [-1, 2, -1],
                  [0, -1, 2]])
    b = np.array([0, 1, 2])

    iter_num = 40
    # Solve with Jacobi Iteration
    x_jac, res_jac = solve_jacobi(A, b, iter_num)
    print(x_jac)
    print(A @ x_jac)
    plot_residual(iter_num, res_jac, 'Jacobi')

    # Solve with Gauss-Seidel Iteration
    x_gs, res_gs = solve_gauss_seidal(A, b, iter_num)
    print(x_gs)
    print(A @ x_gs)
    plot_residual(iter_num, res_gs, 'Gauss-Seidal')

    # Solve with Successive Over Relaxation Iteration
    x_sor, res_sor = solve_sor(A, b, iter_num, w=1.2)
    print(x_sor)
    print(A @ x_sor)
    plot_residual(iter_num, res_sor, 'SOR')

    # Show residual plots
    plt.legend()
    plt.show()
