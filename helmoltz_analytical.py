"""Module to compute an analytical solution for Electromagnetic wave equation


Reference:
    [1] Convergence analysis of Finite Element Methods for H(curl)-elliptic interface problems

"""

from sympy.physics.vector import ReferenceFrame, curl

R = ReferenceFrame('R')
# 3 coordinate variables
x, y, z = R[0], R[1], R[2]
# 3 basis vectors
e_x, e_y, e_z = R.x, R.y, R.z


def e_field(r, n):
    """The exact solution of the problem"""
    e = (x - n * (r - x ** 2 - y ** 2) * y + n * (r - x ** 2 - y ** 2) * z) * e_x + \
        (-n * (r - x ** 2 - y ** 2) * x + y - n * (r - x ** 2 - y ** 2) * z) * e_y + \
        (n * (r - x ** 2 - y ** 2) * x - n * (r - x ** 2 - y ** 2) * y + z) * e_z
    return e


def source_function(field, khi, beta):
    """Compute the source function using given field"""
    return khi * curl(curl(field, R), R) + beta * field


if __name__ == '__main__':
    field = e_field(1, 1)

    # TODO: How to transform the symbolic expression into function.
    source = source_function(field, 1, 1)

    source_x = source & e_x
    print(source_x)
    source_y = source & e_y
    print(source_y)
    source_z = source & e_z
    print(source_x)

    # Dirichlet Boundary condtion
    r = x**2+y**2
    n = 1
    print(e_field(r, n))