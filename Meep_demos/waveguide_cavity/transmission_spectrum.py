import meep as mp
import argparse
from Meep_demos.meep_visualization import visualize
import numpy as np
import matplotlib.pyplot as plt


def simulate(N, sy, fcen, df):
    """Simulate transmission spectrum """
    resolution = 20
    eps = 13

    # width of waveguide
    w = 1.2

    # radius of holes
    r = 0.36

    # deflect spacing(ordinary spacing=1)
    d = 1.4

    # number of holes on either side of defect
    # N = args.N

    # size of cell in the y direction
    # sy = args.sv

    # padding between last hole and PML layers
    pad = 2
    dpml = 1

    sx = 2 * (pad + dpml + N) + d - 1
    cell = mp.Vector3(sx, sy, 0)

    blk = mp.Block(size=mp.Vector3(mp.inf, w, mp.inf), material=mp.Medium(epsilon=eps))

    geometry = [blk]

    for i in range(N):
        geometry.append(mp.Cylinder(r, center=mp.Vector3(d / 2 + i)))
        geometry.append(mp.Cylinder(r, center=mp.Vector3(-(d / 2 + i))))

    pml_layers = [mp.PML(1.0)]

    # pulse center frequency
    # fcen = args.fcen
    # df = args.df

    src = [mp.Source(mp.GaussianSource(fcen, fwidth=df),
                     component=mp.Ey,
                     center=mp.Vector3(-0.5 * sx + dpml, 0, 0),
                     size=mp.Vector3(0, w, 0))]
    # TODO: why it's odd mirror symmetry through the Y-axis
    sym = [mp.Mirror(mp.Y, phase=-1)]

    sim = mp.Simulation(cell_size=cell,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        sources=src,
                        symmetries=sym,
                        resolution=resolution)

    # transmission flux region
    freg = mp.FluxRegion(center=mp.Vector3(0.5 * sx - dpml - 0.5),
                         size=mp.Vector3(0, 2 * w))

    nfreq = 500

    trans = sim.add_flux(fcen, df, nfreq, freg)

    vol = mp.Volume(mp.Vector3(0), size=mp.Vector3(sx))

    # sim.run(mp.at_beginning(mp.output_epsilon),
    #         mp.during_sources(mp.in_volume(vol, mp.to_appended("hz-slice", mp.at_every(0.4, mp.output_efield_y)))),
    #         until_after_sources=mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(0.5 * sx - dpml - 0.5), 1e-3))

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(0.5 * sx - dpml - 0.5), 1e-3))

    sim.display_fluxes(trans)  # print out the flux spectrum

    eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)

    plt.imshow(eps_data)
    # visualize(eps_data.transpose())
    return np.stack((mp.get_flux_freqs(trans), mp.get_fluxes(trans)), axis=0)


if __name__ == '__main__':
    N = 3
    sy = 6
    fcen = 0.25
    df = 0.2

    # without holes
    flux0 = simulate(0, sy, fcen, df)

    # with holes
    flux = simulate(N, sy, fcen, df)

    transmittance = flux[1] / flux0[1]
    plt.figure()
    plt.plot(flux[0], transmittance, '-o')
    plt.show()
