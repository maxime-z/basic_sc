"""An example of stiff problem and ODE method stability"""
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, Function, Eq
from sympy.solvers.ode import dsolve


# A typical scalar stiff problem is : x' = -ax, with initial condition x(0) = 1 and known a>0.

### First let's try to define the equation and solve it analytical using Sympy


def analytical_solution():
    t, a = symbols('t a')
    x = Function('x')(t)
    dx = -a * x

    ode_eq = Eq(x.diff(t), dx)

    # Try to solve it using Sympy's ode solver
    sol = dsolve(ode_eq)
    return sol


### Secondly, let's try to solve the problem using Euler explicit

def explicit_euler_solution(dx, x0, dt, n_step):
    # Initial condition and first order derivative
    x0 = 1
    dx = lambda x: -a * x

    t = np.arange(0, n_step) * dt
    x_num = np.zeros(n_step)
    x_num[0] = x0
    for i in range(1, n_step):
        x_num[i] = x_num[i - 1] + dt * dx(x_num[i - 1])

    return t, x_num


def implicit_euler_solution(a, dt, n_step):
    pass


if __name__ == '__main__':
    a = 10

    dt = 0.12
    n_step = 10
    plt.plot(*explicit_euler_solution(a, dt, n_step))
    plt.show()
