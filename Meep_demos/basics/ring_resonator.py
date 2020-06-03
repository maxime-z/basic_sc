"""Modes of a ring resonator"""

"""In this example, the Harminv tool will be used to analyze the frequencies, lifetime or Q-factor
 of a signal. 
 
 Harminv is a free program (and accompanying library) to solve the problem of "harmonic inversion." 
 Given a discrete, finite-length signal that consists of a sum of finitely-many sinusoids (possibly 
 exponentially decaying), it determines the frequencies, decay constants, amplitudes, and phases of 
 those sinusoids.
 """

import meep as mp

n = 3.4
w = 1
r = 1
pad = 4
dpml = 2

sxy = 2 * (r + w + pad + dpml)

c1 = mp.Cylinder(radius=r + w, material=mp.Medium(index=n))
c2 = mp.Cylinder(radius=r)

# Solicit the ring with random frequency source
fcen = 0.15
df = 0.1
src = mp.Source(mp.GaussianSource(fcen, fwidth=df),
                component=mp.Ez,
                center=mp.Vector3(r + 0.1, 0, 0))

sim = mp.Simulation(cell_size=mp.Vector3(sxy, sxy),
                    geometry=[c1, c2],
                    sources=[src],
                    resolution=10,
                    boundary_layers=[mp.PML(dpml)])

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.after_sources(mp.Harminv(mp.Ez, mp.Vector3(r + 0.1), fcen, df)),
        until_after_sources=300)

# sim.run(mp.at_beginning(mp.output_epsilon))


res_harminv = mp.Harminv(mp.Ez, mp.Vector3(r + 0.1), fcen, df)

print('end')



