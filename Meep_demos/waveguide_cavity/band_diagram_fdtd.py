"""Analyze Dispersion curves via FDTD method"""

import numpy as np
import meep as mp
import matplotlib.pyplot as plt

eps = 13
w = 1.2
r = 0.36

# cell dimensions
sy = 12
dpml = 1
# here the periodicity equals to 1
cell = mp.Vector3(1, sy)

b = mp.Block(size=mp.Vector3(mp.inf, w, mp.inf), material=mp.Medium(epsilon=eps))
c = mp.Cylinder(radius=r, material=mp.Medium(index=1))

resolution = 50

pml_layers = mp.PML(dpml, direction=mp.Y)

fcen = 0.8838
df = 0.1



# TODO:  why a Hz-polarized odd-symmetry modes (recalling the pseudovector subtlety discussed above) ???
sym = mp.Mirror(direction=mp.Y, phase=-1)

s = mp.Source(src=mp.GaussianSource(fcen, fwidth=df),
              size=mp.Vector3(1, 0, 0),
              component=mp.Hz,
              center=mp.Vector3(0.123, 0.0))
sim = mp.Simulation(sources=[s],
                    boundary_layers=[pml_layers],
                    cell_size=cell,
                    geometry=[b,c],
                    resolution=resolution)

kx = 0.3
sim.k_point = mp.Vector3(kx)



"""Harminv mode analysis"""
# sim.run(mp.after_sources(mp.Harminv(mp.Hz, mp.Vector3(0.1234), fcen, df)),
#         until_after_sources=300)
# k_interp = 11
# sim.run_k_points(300, mp.interpolate(k_interp, [mp.Vector3(0), mp.Vector3(0.5)]))

"""Coupling simulation"""
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("hz", mp.at_every(1/fcen/10, mp.output_hfield_z)),
        until_after_sources=5/fcen)

"""Viusalize epsilon"""
# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
#
# plt.imshow(eps_data.transpose())
# plt.show()
