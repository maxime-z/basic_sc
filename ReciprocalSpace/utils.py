"""Module for computing reciprocal space """
import numpy as np
from meep import geom

def reciprocal_lattice_vector(lattice_basis: np.ndarray):
    """Compute reciprocal lattice vector

    2D lattice vector:
        [[a1x, a1y],
        [a2x, a2y]]

    """
    dim = lattice_basis.shape[0]

    if dim is 2:
        assert lattice_basis.shape == (2, 2), "2D lattice basis input should be of shape (2,2)!"
        reciprocal_basis_transposed = 2 * np.pi * np.linalg.inv(lattice_basis.T)
        return reciprocal_basis_transposed
    elif dim is 3:
        pass
    else:
        raise Exception("lattice basis dimension should be 2 or 3!")

def cartesian_to_lattice(x, lattice_basis):
    """Cartesian to lattice basis conversion.
    Args:
        x(np.ndarray): coordinates in cartesian system
        lattice_basis(np.ndarray):
            [[a1x, a1y],
            [a2x, a2y]]
        """
    return np.linalg.inv(lattice_basis.T) @ x



def honeycombe_lattice_and_reciprocal_basis():
    """Computer honeycombe lattice """
    sqrt3 = np.sqrt(3)
    honeycombe_lat_basis = np.array([[0.5, sqrt3 / 2],
                                     [0.5, -sqrt3 / 2]])
    honeycombe_recip_basis = reciprocal_lattice_vector(honeycombe_lat_basis)


    m_carte = np.array([0,1])
    m_recip = cartesian_to_lattice(m_carte, honeycombe_recip_basis/2/np.pi
                                   )

    return honeycombe_lat_basis, honeycombe_recip_basis


def triangular_lattice_and_reciprocal_basis():
    sqrt3 = np.sqrt(3)
    tri_lat_basis = np.array([[sqrt3 / 2, 0.5],
                              [sqrt3 / 2, -0.5]])

    tri_recip_basis = 2 * np.pi * np.array([[1 / sqrt3, 1],
                                            [1 / sqrt3, -1]])
    print(reciprocal_lattice_vector(tri_lat_basis))

    print(reciprocal_lattice_vector(tri_lat_basis) - tri_recip_basis)


if __name__ == "__main__":
    res = honeycombe_lattice_and_reciprocal_basis()
    print(res[0])
    print(res[1])
