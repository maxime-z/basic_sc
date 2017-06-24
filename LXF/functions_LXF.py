# -*- coding = utf-8 -*-
import math

def my_abs(a):
    if not isinstance(a,(int,float)):
        raise TypeError("parameter is neither int nor float")
    if a >= 0:
        return a
    else:
        return -a


def quadratic_roots(a, b, c):
    if not isinstance(a,(int,float)):
        raise TypeError("parameter is neither int nor float")
    determinant = b**2 - 4*a*c
    if determinant < 0:
        return "no real root"
    elif determinant == 0:
        return -b/(2*a)
    else:
        sqrt_det = math.sqrt(determinant)
        return (-b+sqrt_det)/(2*a), (-b-sqrt_det)/(2*a)

def hanoi(n, A ,B ,C):
    if n == 1:
        print(A + "->" + C)
    else:
        hanoi(n-1, A,C,B)
        print(A + "->" + C)
        hanoi(n-1, B,A,C)



print(my_abs(-100))
#print(my_abs("abc"))

print(quadratic_roots(1,1,1))

hanoi(5, 'A', 'B' ,'C')