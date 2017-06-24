# -*- coding = utf-8 -*-
from copy import deepcopy

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
#        print(b)
        yield b
        a, b = b, a + b
        n += 1
    return 'done'

for b in fib(10):
    print(b)

#杨辉三角
def triangles(max):
    n, a, b = 0,  [0], [1]
    while n < max:
        yield b
        a = deepcopy(b)
        len_a = len(a)
        if len_a == 1:
            b.insert(len_a, 1)
        else:
            b.insert(-1, 1)
            for i in range(0,len_a-1):
                b[i+1]=a[i]+a[i+1]

        n += 1
    return 'done'

#the best implementation !?
def yanghui_triangle(max):
    L=[1]
    n = 0
    while n < max:
        n += 1
        yield L
        L = [1] + [ L[x-1] + L[x] for x in range(1,len(L)) ] + [1]
    return 'done'

for list in triangles(6):
    print(list)

for list in yanghui_triangle(6):
    print(list)
