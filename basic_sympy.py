"""Module for Sympy practices"""

from sympy import *

x, y = symbols('x y')

# basic expression
expr = x + 2 * y
expr += y
print(expr)

# derivative
expr1 = sin(x) * exp(x)
print(diff(expr1, x))

# floating division and rational
print(1 / 3)
print(Rational(1, 3))

# trigonometric expansion
expr2 = sin(2 * x) + cos(2 * x)
print(expand_trig(expr2))

# Physics Vectors and Reference Frame
from sympy.physics.vector import *
N = ReferenceFrame('N')
