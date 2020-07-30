# import sys
#
# # added to run from terminal
# sys.path.append('/home/lei/devs/github/basic_sc')

import numpy as np
import meep as mp
import matplotlib.pyplot as plt


def energy_flux():
    """Source frequency interval"""

    f_inf = 0.20
    f_sup = 0.35

    f = 0.5 * (f_inf + f_sup)
    df = f_sup - f_inf

    wvl = 1 / f
    n_freq = 100
    source_component = mp.Ex

    """Materials"""
    n_ej232 = 1.58
    n_bgo = 2.15
    n_lyso = 1.82
    n_cdse = 2.61
    eps1_cdse = n_cdse ** 2
    eps2_cdse = 0
    # eps2_cdse = 0.5
    # fixme: here the sigma_d is different from MEEP's doc in function of freqeuency!
    cdse = mp.Medium(epsilon=eps1_cdse, D_conductivity=f * eps2_cdse / eps1_cdse)

    """Dimension"""
    a = 1.
    thickness = 1. * a
    radius = 0.1 * a
    dpml = 0.5 * wvl

    """Computational domain in Meep"""
    r1 = np.array([0.5, -np.sqrt(3) / 2]) * a
    r2 = np.array([0.5, np.sqrt(3) / 2]) * a

    vec1 = mp.Vector3(*r1)
    vec2 = mp.Vector3(*r2)

    height = thickness + 2 * (wvl + dpml)
    width = 2 * wvl + 2 * dpml

    cell_size = mp.Vector3(width, width, height)

    # resolution = np.ceil((1 / (wvl / 50)))
    resolution = 20

    # geometry
    geom = [mp.Block(center=mp.Vector3(z=0.25 * cell_size.z),
                     size=mp.Vector3(mp.inf, mp.inf, 0.5 * cell_size.z),
                     material=mp.Medium(index=n_ej232)),
            mp.Block(center=mp.Vector3(z=-0.25 * cell_size.z),
                     size=mp.Vector3(mp.inf, mp.inf, 0.5 * cell_size.z),
                     material=mp.Medium(index=n_lyso))]
    # periodic patterns
    diagonal = np.sqrt(cell_size.x ** 2 + cell_size.y ** 2)
    n1 = int(0.7 * diagonal / vec1.norm())
    n2 = int(0.7 * diagonal / vec2.norm())

    geom.append(mp.Block(center=mp.Vector3(),
                         size=mp.Vector3(mp.inf, mp.inf, thickness),
                         material=cdse))

    for i in range(-n1, n1 + 1):
        for j in range(-n2, n2 + 1):
            hole_center = i * vec1 + j * vec2
            if -0.5 * cell_size.x < hole_center.x < 0.5 * cell_size.x \
                    and -0.5 * cell_size.y < hole_center.y < 0.5 * cell_size.y:
                geom.append(mp.Cylinder(radius=radius,
                                        center=hole_center,
                                        height=thickness,
                                        material=mp.Medium(index=n_ej232)))

    source = mp.Source(src=mp.GaussianSource(f, fwidth=df),
                       center=mp.Vector3(),
                       component=mp.Ex)

    """Boundary conditions"""
    pml_layers = [mp.Absorber(dpml, direction=mp.X),
                  mp.Absorber(dpml, direction=mp.Y),
                  mp.PML(dpml, direction=mp.Z)]
    sim = mp.Simulation(sources=[source],
                        boundary_layers=pml_layers,
                        cell_size=cell_size,
                        geometry=geom,
                        resolution=resolution)

    """Energy flux region"""
    # source surrounding box
    srcbox_width = wvl / 4
    srcbox_top = sim.add_flux(f, df, n_freq,
                              mp.FluxRegion(center=mp.Vector3(0, 0, 0.5 * srcbox_width),
                                            size=mp.Vector3(srcbox_width, srcbox_width, 0),
                                            direction=mp.Z,
                                            weight=1))

    srcbox_bot = sim.add_flux(f, df, n_freq,
                              mp.FluxRegion(center=mp.Vector3(0, 0, -0.5 * srcbox_width),
                                            size=mp.Vector3(srcbox_width, srcbox_width, 0),
                                            direction=mp.Z,
                                            weight=-1))

    srcbox_yf = sim.add_flux(f, df, n_freq,
                             mp.FluxRegion(center=mp.Vector3(0, 0.5 * srcbox_width, 0),
                                           size=mp.Vector3(srcbox_width, 0, srcbox_width),
                                           direction=mp.Y,
                                           weight=1))

    srcbox_yb = sim.add_flux(f, df, n_freq,
                             mp.FluxRegion(center=mp.Vector3(0, -0.5 * srcbox_width, 0),
                                           size=mp.Vector3(srcbox_width, 0, srcbox_width),
                                           direction=mp.Y,
                                           weight=-1))

    srcbox_xf = sim.add_flux(f, df, n_freq,
                             mp.FluxRegion(center=mp.Vector3(0.5 * srcbox_width, 0, 0),
                                           size=mp.Vector3(0, srcbox_width, srcbox_width),
                                           direction=mp.X,
                                           weight=1))

    srcbox_xb = sim.add_flux(f, df, n_freq,
                             mp.FluxRegion(center=mp.Vector3(-0.5 * srcbox_width, 0, 0),
                                           size=mp.Vector3(0, srcbox_width, srcbox_width),
                                           direction=mp.X,
                                           weight=-1))

    srcbox_flux = [srcbox_top, srcbox_bot, srcbox_xf, srcbox_xb, srcbox_yf, srcbox_yb]

    # axial energy flux

    upper_axial = sim.add_flux(f, df, n_freq,
                               mp.FluxRegion(center=mp.Vector3(0, 0, 0.5 * height - dpml),
                                             size=mp.Vector3(cell_size[0] - 2 * dpml, cell_size[1] - 2 * dpml, 0),
                                             direction=mp.Z,
                                             weight=1))

    lower_axial = sim.add_flux(f, df, n_freq,
                               mp.FluxRegion(center=mp.Vector3(0, 0, -0.5 * height + dpml),
                                             size=mp.Vector3(cell_size[0] - 2 * dpml, cell_size[1] - 2 * dpml, 0),
                                             direction=mp.Z,
                                             weight=-1))

    # lateral energy flux
    lat_xz1_flux = sim.add_flux(f, df, n_freq,
                                mp.FluxRegion(center=mp.Vector3(0, 0.5 * cell_size[1] - dpml, 0),
                                              size=mp.Vector3(cell_size[0] - 2 * dpml, 0, cell_size[2] - 2 * dpml),
                                              direction=mp.Y))

    lat_xz2_flux = sim.add_flux(f, df, n_freq,
                                mp.FluxRegion(center=mp.Vector3(0, -0.5 * cell_size[1] + dpml, 0),
                                              size=mp.Vector3(cell_size[0] - 2 * dpml, 0, cell_size[2] - 2 * dpml),
                                              direction=mp.Y,
                                              weight=-1))

    lat_yz1_flux = sim.add_flux(f, df, n_freq,
                                mp.FluxRegion(center=mp.Vector3(0.5 * cell_size[0] - dpml, 0, 0),
                                              size=mp.Vector3(0, cell_size[1] - 2 * dpml, cell_size[2] - 2 * dpml),
                                              direction=mp.X))

    lat_yz2_flux = sim.add_flux(f, df, n_freq,
                                mp.FluxRegion(center=mp.Vector3(-0.5 * cell_size[0] + dpml, 0, 0),
                                              size=mp.Vector3(0, cell_size[1] - 2 * dpml, cell_size[2] - 2 * dpml),
                                              direction=mp.X,
                                              weight=-1))

    lateral_flux = [lat_xz1_flux, lat_xz2_flux, lat_yz1_flux, lat_yz2_flux]

    """Decay point for the stop criteria"""
    decay_point = mp.Vector3(0.5 * cell_size.x - 1.1 * dpml,
                             0.5 * cell_size.y - 1.1 * dpml,
                             0)

    # sim.run(until=2)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(1, source_component, decay_point, 1e-6))

    """Visualization"""
    # eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
    # plot_slice(np.sqrt(eps_data))
    # plt.show()

    """Post-processing"""

    freq = np.array(mp.get_flux_freqs(lower_axial))

    lateral_energy = np.zeros(freq.shape)

    for flux in lateral_flux:
        if np.min(mp.get_fluxes(flux)) < 0:
            raise ValueError("Energy flux negative for LATERAL")
        lateral_energy += np.array(mp.get_fluxes(flux))
        # print(np.min(np.array(mp.get_fluxes(flux))))

    source_energy = np.zeros(freq.shape)
    for flux in srcbox_flux:
        # if np.min(mp.get_fluxes(flux)) < 0:
        #     raise ValueError("Energy flux negative for SOURCE")
        source_energy += np.array(mp.get_fluxes(flux))

    lower_axial = np.array(mp.get_fluxes(lower_axial))

    upper_axial = np.array(mp.get_fluxes(upper_axial))

    """Post-processing"""
    eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
    index_data = np.sqrt(eps_data)

    return index_data, freq, source_energy, lateral_energy, lower_axial, upper_axial


def plot(file_name: str):
    """Plot energy flux results"""
    res = np.load(file_name)
    freq = res[0]
    plt.figure(file_name)
    plt.plot(freq, res[1], 'k', label='Source Box Total')
    plt.plot(freq, res[3] + res[4] + res[2], 'b', label='Domain Box Total')
    plt.plot(freq, res[2], 'r', label='Lateral')
    plt.legend()
    plt.grid(True)



if __name__ == "__main__":
    index_data, freq, source_energy, lateral_energy, lower_axial, upper_axial = energy_flux()
    flux_data = np.array([freq, source_energy, lateral_energy, lower_axial, upper_axial])
    np.save('ref_index', index_data)
    np.save('energy_flux', flux_data)

    # plot('energy_flux_im_0.5.npy')
    # plot('node_energy_flux.npy')
    # plt.show()