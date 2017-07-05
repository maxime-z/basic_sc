from sympy import *
from sympy.plotting import*
from sympy.functions import exp
import math

x = Symbol('x')
y = Symbol('y')

## load distribution function
# A : load amplitude
# sig : the "width" of distribution
# center: load center
def load(A, sig, center, x, y):
    x0 = center[0]
    y0 = center[1]
    exponent = -1/2*(((x-x0)/sig)**2+((y-y0)/sig)**2)
    coef = A/(2*math.pi*sig)
    return coef*exp(exponent)

A = 1
sig = 0.5
center = (0, 0)

p = load(A,sig,center,x,y)

#Plot
plot3d_parametric_surface(x, y, p,(x,-1,1),(y,-1,1))
