import meep as mp
from meep.materials import Al
import cmath
import random


def main(L):
    """Forward simulation
    Args:
        L(float): length of non-absorbing region of computational cell in X and Y.

    """
    resolution = 100
    # lenght unit: micron-meter
    lambda_min = 0.4
    lambda_max = 0.8
    fmin = 1 / lambda_max
    fmax = 1 / lambda_min
    fcen = 0.5 * (fmin + fmax)
    df = fmax - fmin

    # absorber / PML thickness
    tABS = lambda_max
    # thickness of <Glass, Indium tin oxide, >
    tGLS = 1.0
    tITO = 0.1
    tORG = 0.1
    tAL = 0.1

    sz = tABS + tGLS + tITO + tORG + tAL

    sxy = L+2*tABS
    cell_size = mp.Vector3(sxy, sxy, sz)

    # TODO: why the ABS side is on high side?
    boundary_layers = [mp.Absorber(tABS, direction=mp.X),
                       mp.Absorber(tABS, direction=mp.Y),
                       mp.PML(tABS, direction=mp.Z, side = mp.High)]

    ORG = mp.Medium(index=1.75)
    ITO = mp.Medium(index=1.80)
    GLS = mp.Medium(index=1.45)

    geometry = [mp.Block(material=GLS, size=mp.Vector3(mp.inf, mp.inf, tABS+tGLS),
                         center=mp.Vector3(0,0,0.5*sz-0.5*(tABS+tGLS))),
                mp.Block(material=ITO, size=mp.Vector3(mp.inf, mp.inf, tITO),
                         center=mp.Vector3(0,0,0.5*sz-tABS-tGLS-0.5*tITO))]
