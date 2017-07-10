from sympy import *
from sympy.plotting import *

xi = Symbol("xi")
eta = Symbol("eta")

#Shape functions in reference element
def Ni(xi,eta,i):
    references_vertices = {1:[-1,-1],2:[1,-1],3:[1,1],4:[-1,1]}
    xiv = references_vertices[i][0]
    etav = references_vertices[i][1]
    return Rational(1,4)*(1+xiv*xi)*(1+etav*eta)

#Give a specific element in physical space with an angle >= 180 degree
physical_vertices = {1:[-1,-1],2:[1,-1],3:[1,1],4:[0,0]}

#Interpolation for (x,y) in terms of (xi,eta)
def mapping(xi,eta,vertices):
    x = 0
    y = 0
    for i in vertices:
        xv = vertices[i][0]
        yv = vertices[i][1]
        x += Ni(xi,eta,i)*xv
        y += Ni(xi,eta,i)*yv
    return [x,y]

#mapping (xi, eta) -> (x, y)
xy = mapping(xi,eta,physical_vertices)
print("x and y")
print(factor(xy[0]))
print(factor(xy[1]))

#Jacobian
jac = []
jac.append([xy[0].diff(xi),xy[0].diff(eta)])
jac.append([xy[1].diff(xi),xy[1].diff(eta)])

print("Jacobian Matrix")
print(factor(jac))

#The determinant of Jacobian
det_jac = jac[0][0]*jac[1][1]-jac[0][1]*jac[1][0]
print(factor(det_jac))

#Plot
plot3d_parametric_surface(xy[0], xy[1], det_jac,(xi,-1,1),(eta,-1,1))
det_jac.subs([(xi,1),(eta,-1)])


