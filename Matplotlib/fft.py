import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(0, 1.8, 10)

X, Y = np.meshgrid(a, a)
V = np.cos(2.*np.pi*(X + Y))

f = np.fft.fft2(V)
fvec = np.array(list(map(np.linalg.norm,f)))
print(np.where(fvec> 0.0001))


print(f)
print(f[2,2])
print(np.linalg.norm(f[2,2]))
print(np.linalg.norm(f))
