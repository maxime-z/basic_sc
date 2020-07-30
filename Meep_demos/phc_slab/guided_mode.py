"""Verify the guided and leaky mode computed by GWE"""

import sys

# sys.path.append('./')
sys.path.append('/home/lei/devs/github/basic_sc')
# print(sys.path)

import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from Meep_demos.phc_slab.viz import plot_slice
from Meep_demos.phc_slab import res_dir

f_inf = 0.20
f_sup = 0.28

f = 0.5*(f_inf+f_sup)
df = f_sup-f_inf
wvl = 1 / f

"""Materials"""
n_ej232 = 1.58
n_bgo = 2.15
n_lyso = 1.82
n_cdse = 2.61
eps1_cdse = n_cdse ** 2
eps2_cdse = 0.5
# eps2_cdse = 0.5
# FIXME:
cdse = mp.Medium(epsilon=eps1_cdse, D_conductivity=f * eps2_cdse / eps1_cdse)
print(cdse.epsilon(0.28)[0,0])
"""Dimensions"""
a = 1
thickness = 1 * a
radius = 0.1 * a

"""build the geometry for meep"""
r1 = np.array([0.5, -np.sqrt(3) / 2]) * a
r2 = np.array([0.5, np.sqrt(3) / 2]) * a

vec1 = mp.Vector3(*r1)
vec2 = mp.Vector3(*r2)
cell_size = mp.Vector3(a, np.sqrt(3), 10 * a)

pml_layers = mp.PML(0.5 * wvl, direction=mp.Z)

# resolution = np.ceil((1 / (wvl / 100)))
resolution = 15

geom = [mp.Block(center=mp.Vector3(z=0.25 * cell_size.z),
                 size=mp.Vector3(mp.inf, mp.inf, 0.5 * cell_size.z),
                 material=mp.Medium(index=n_ej232)),
        mp.Block(center=mp.Vector3(z=-0.25 * cell_size.z),
                 size=mp.Vector3(mp.inf, mp.inf, 0.5 * cell_size.z),
                 material=mp.Medium(index=n_lyso)),
        mp.Block(size=mp.Vector3(mp.inf, mp.inf, thickness),
                 material=cdse),
        mp.Cylinder(radius=radius,
                    height=thickness,
                    material=mp.Medium(index=n_ej232)),
        mp.Cylinder(radius=radius,
                    center=vec1,
                    height=thickness,
                    material=mp.Medium(index=n_ej232)),
        mp.Cylinder(radius=radius,
                    center=vec2,
                    height=thickness,
                    material=mp.Medium(index=n_ej232)),
        mp.Cylinder(radius=radius,
                    center=vec1 * -1,
                    height=thickness,
                    material=mp.Medium(index=n_ej232)),
        mp.Cylinder(radius=radius,
                    center=vec2 * -1,
                    height=thickness,
                    material=mp.Medium(index=n_ej232))]

source = mp.Source(src=mp.GaussianSource(f, fwidth=df),
                   center=mp.Vector3(),
                   component=mp.Ex)

sim = mp.Simulation(sources=[source],
                    boundary_layers=[pml_layers],
                    cell_size=cell_size,
                    geometry=geom,
                    resolution=resolution)

# TODO:Periodic boundary condition with given bloch vector

sim.k_point = mp.Vector3(x=4 / 3 * 0.8)

"""Guided or Leaky mode field"""

res = []


def slice_step(sim):
    ex = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Ex)
    center_index = np.array(ex.shape) // 2
    res.append(ex[center_index[0], center_index[1], center_index[2]])


"""Configure harminv"""
h = mp.simulation.Harminv(source.component, source.center, f, df)
h.Q_thresh = 10

"""Coupling simulation & Spectral analysis"""
sim.run(
    # mp.at_beginning(mp.output_epsilon),
    mp.at_every(1 / 10, slice_step),
    mp.after_sources_and_time(50, h),
    until_after_sources=150)
np.save(res_dir / ('ex_f_%0.2f_ImEPS_%0.1f' % (f, eps2_cdse)), np.asarray(res))

"""Visualization"""
eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
plot_slice(np.sqrt(eps_data))
plt.show()
