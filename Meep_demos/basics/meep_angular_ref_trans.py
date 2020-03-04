"""Tutorial basics: Angular Reflectance Spectrum of a Planar Interface"""

import meep as mp
import argparse
import math

# TODO; plot the reflectance spectrum and Brewster's angle.
def main(resolution, theta):
    """Simulation"""
    # resolution = args.res

    dpml = 1.0
    sz = 10 + 2 * dpml
    # 1d cell size
    cell_size = mp.Vector3(0, 0, sz)
    pml_layers = [mp.PML(dpml)]

    wvl_min = 0.4
    wvl_max = 0.8

    fmin = 1 / wvl_max
    fmax = 1 / wvl_min
    fcen = 0.5 * (fmin + fmax)

    df = fmax - fmin
    nfreq = 100

    # rotation angle
    theta_r = math.radians(theta)

    # rotation along y direction
    """
    Here we scale the Bloch wave vector with respect ot fmin:
    Because in MEEP unit systems, a bloch wave vector is always in unit 2*PI/a (a is length unit).
    And so, k = f*(2*PI/a), has correct value and unit.
    """

    k = mp.Vector3(math.sin(theta_r), 0, math.cos(theta_r)).scale(fmin)

    # if normal incidence, force number of dimensions to be 1
    if theta_r == 0:
        dimensions = 1
    else:
        dimensions = 3

    sources = [mp.Source(mp.GaussianSource(fcen, fwidth=df),
                         component=mp.Ex,
                         center=mp.Vector3(0, 0, -0.5 * sz + dpml))]

    sim = mp.Simulation(cell_size=cell_size,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k,
                        dimensions=dimensions,
                        resolution=resolution)

    refl_fr = mp.FluxRegion(center=mp.Vector3(0, 0, -0.25 * sz))
    refl = sim.add_flux(fcen, df, nfreq, refl_fr)

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(0, 0, -0.5 * sz + dpml), 1e-9))

    empty_flux = mp.get_fluxes(refl)
    empty_data = sim.get_flux_data(refl)

    """Normal run"""
    sim.reset_meep()

    geometry = [mp.Block(mp.Vector3(mp.inf, mp.inf, 0.5 * sz),
                         center=mp.Vector3(0, 0, 0.25 * sz),
                         material=mp.Medium(index=3.5))]

    sim = mp.Simulation(cell_size=cell_size,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k,
                        dimensions=dimensions,
                        resolution=resolution)

    refl = sim.add_flux(fcen, df, nfreq, refl_fr)
    sim.load_minus_flux_data(refl, empty_data)

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(0, 0, -0.5 * sz + dpml), 1e-9))

    refl_flux = mp.get_fluxes(refl)
    freqs = mp.get_flux_freqs(refl)

    for i in range(nfreq):
        print("refl:, {}, {}, {}, {}".format(k.x,
                                             1 / freqs[i],
                                             math.degrees(math.asin(k.x / freqs[i])),
                                             -refl_flux[i] / empty_flux[i]))




if __name__ == "__main__":
    main(200, 0)