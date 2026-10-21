"""Equivalent circuit of the impedance flow cytometer (Q11-Q16).

The medium and the cell sit between the same two electrodes, so they form two
parallel branches:

    medium branch   R_m in parallel with C_m
    cell branch     C_mem in series with R_i

Part B adds the electrical double layer as one capacitance in series with the
whole network, because there is one 100 pF layer per electrode.
"""
from math import log, pi, sqrt, tanh

EPSILON_0 = 8.854187817e-12

# Parameters from table 1
CELL_RADIUS = 5e-6        # m
CHANNEL_HEIGHT = 40e-6    # m
ELECTRODE_WIDTH = 20e-6   # m
ELECTRODE_LENGTH = 40e-6  # m

MEDIUM_EPS_R = 80.0       # relative permittivity
MEDIUM_SIGMA = 0.1        # S/m
MEMBRANE_EPS_R = 8.0      # relative permittivity
INTERIOR_EPS_R = 60.0     # relative permittivity
INTERIOR_SIGMA = 0.6      # S/m
MEMBRANE_THICKNESS = 5e-9  # m

EDL_CAPACITANCE = 100e-12  # F, per electrode


def medium_eps():
    """Absolute permittivity of the medium."""
    return MEDIUM_EPS_R * EPSILON_0


def interior_eps():
    """Absolute permittivity of the cell interior."""
    return INTERIOR_EPS_R * EPSILON_0


def membrane_eps():
    """Absolute permittivity of the membrane."""
    return MEMBRANE_EPS_R * EPSILON_0


def kappa():
    """Cell constant correcting for the non-uniform field at the electrode edges.

    The assignment defines it as K(k)/K'(k) with k = tanh(pi w / 2h), where w is
    the electrode width and h the channel height. The elliptic ratio is
    evaluated with the Hilberg approximation.
    """
    k = tanh(pi * ELECTRODE_WIDTH / (2.0 * CHANNEL_HEIGHT))
    return (1.0 / pi) * log(4.0 * (1.0 + sqrt(k)) / (1.0 - sqrt(k)))


def volume_fraction():
    """Share of the sensing volume occupied by the cell."""
    cell_volume = 4.0 / 3.0 * pi * CELL_RADIUS**3
    sensed_volume = kappa() * ELECTRODE_WIDTH * CHANNEL_HEIGHT * ELECTRODE_LENGTH
    return cell_volume / sensed_volume


def epsilon_infinity(phi):
    """Permittivity of the cell-medium mixture at high frequency."""
    eps_m = medium_eps()
    eps_i = interior_eps()
    difference = eps_m - eps_i
    return eps_m * (2.0 * eps_m + eps_i - 2.0 * phi * difference) \
        / (2.0 * eps_m + eps_i + phi * difference)


def medium_resistance(phi, sigma_m=MEDIUM_SIGMA):
    """Resistance of the medium between the electrodes."""
    return 1.0 / (sigma_m * (1.0 - 1.5 * phi)
                  * ELECTRODE_LENGTH * kappa())


def medium_capacitance(phi):
    """Capacitance across the medium between the electrodes."""
    return epsilon_infinity(phi) * ELECTRODE_LENGTH * kappa()


def membrane_capacitance(phi, thickness=None, permittivity=None):
    """Capacitance of the cell membrane.

    Thickness and permittivity can be overridden to sweep them in Q13.
    """
    d = MEMBRANE_THICKNESS if thickness is None else thickness
    eps = membrane_eps() if permittivity is None else permittivity * EPSILON_0
    return (9.0 * phi * CELL_RADIUS / 4.0) * eps / d \
        * ELECTRODE_LENGTH * kappa()


def interior_resistance(phi, sigma_m=MEDIUM_SIGMA):
    """Resistance of the cell interior, including the medium inside the membrane."""
    conduction = 1.0 / (2.0 * sigma_m) + 1.0 / INTERIOR_SIGMA
    return 4.0 * conduction / (9.0 * phi * kappa() * ELECTRODE_LENGTH)


def medium_branch(omega, phi, sigma_m=MEDIUM_SIGMA):
    """Impedance of the medium branch, R_m in parallel with C_m."""
    r_m = medium_resistance(phi, sigma_m)
    z_c = 1.0 / (1j * omega * medium_capacitance(phi))
    return r_m * z_c / (r_m + z_c)


def cell_branch(omega, phi, sigma_m=MEDIUM_SIGMA, thickness=None, permittivity=None):
    """Impedance of the cell branch, C_mem in series with R_i."""
    z_c = 1.0 / (1j * omega * membrane_capacitance(phi, thickness, permittivity))
    return interior_resistance(phi, sigma_m) + z_c


def total_impedance(omega, phi, sigma_m=MEDIUM_SIGMA, thickness=None,
                    permittivity=None):
    """Total impedance of the two parallel branches."""
    z_medium = medium_branch(omega, phi, sigma_m)
    z_cell = cell_branch(omega, phi, sigma_m, thickness, permittivity)
    return z_medium * z_cell / (z_medium + z_cell)


def total_impedance_with_edl(omega, phi, sigma_m=MEDIUM_SIGMA):
    """Total impedance including the double layer capacitance in series."""
    return total_impedance(omega, phi, sigma_m) \
        + 2.0 / (1j * omega * EDL_CAPACITANCE)