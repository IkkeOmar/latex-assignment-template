"""Physical constants and material properties for the dielectrophoresis part (Q1-Q10).

Everything is in SI units. The medium is water at 20 degrees Celsius.
"""
from math import log, pi, sqrt

# Constants
BOLTZMANN = 1.380649e-23      # J/K
EPSILON_0 = 8.854187817e-12  # F/m
GRAVITY = 9.81               # m/s^2

# Water at 20 degrees Celsius
VISCOSITY = 1.002e-3         # Pa.s
MEDIUM_DENSITY = 1.003e3     # kg/m^3
TEMPERATURE = 293.15         # K

# Particle and medium electrical properties, from the assignment table
PARTICLE_EPS_R = 2.5         # relative permittivity
PARTICLE_SIGMA = 0.0185      # S/m
MEDIUM_EPS_R = 80.0          # relative permittivity
MEDIUM_SIGMA = 0.016         # S/m

# The five particles: label, radius in metres, density in kg/m^3
PARTICLES = [
    ("P1  150 nm, 1050", 150e-9, 1050),
    ("P2  600 nm, 1050", 600e-9, 1050),
    ("P3  600 nm, 1100", 600e-9, 1100),
    ("P4  600 nm, 1200", 600e-9, 1200),
    ("P5  600 nm, 1500", 600e-9, 1500),
]


def particle_eps_p():
    """Absolute permittivity of the particle."""
    return PARTICLE_EPS_R * EPSILON_0


def medium_eps_m():
    """Absolute permittivity of the medium."""
    return MEDIUM_EPS_R * EPSILON_0


def diffusion_coefficient(radius):
    """Stokes-Einstein diffusion coefficient of a sphere."""
    return BOLTZMANN * TEMPERATURE / (6.0 * pi * VISCOSITY * radius)


def brownian_delta_3d(radius, delta_t):
    """Root-mean-square random displacement of the particle over delta_t."""
    d = diffusion_coefficient(radius)
    return sqrt(6.0 * d * delta_t)


def threshold_force(radius, delta_t):
    """Smallest force that moves the particle by three standard deviations.

    The displacement is three times the Brownian scatter, and the force follows
    from the Stokes drag that would produce that displacement in delta_t.
    """
    delta = brownian_delta_3d(radius, delta_t)
    velocity = 3.0 * delta / delta_t
    return 6.0 * pi * VISCOSITY * radius * velocity


def clausius_mossotti(omega):
    """Complex Clausius-Mossotti factor of the particle in the medium.

    Conduction is folded in through the complex permittivity, so the factor
    depends on frequency. The real part sets the in-phase force, and a negative
    value means negative dielectrophoresis, which pushes the particle towards
    weaker fields.
    """
    particle_complex = PARTICLE_EPS_R * EPSILON_0 - 1j * PARTICLE_SIGMA / omega
    medium_complex = MEDIUM_EPS_R * EPSILON_0 - 1j * MEDIUM_SIGMA / omega
    return ((particle_complex - medium_complex)
            / (particle_complex + 2.0 * medium_complex))


def dep_force_constant(radius, omega):
    """Coefficient of the field gradient in the DEP force, F = C * |grad E^2|."""
    eps_m = medium_eps_m()
    k_cm = abs(clausius_mossotti(omega).real)
    return 2.0 * pi * eps_m * radius**3 * k_cm


def equilibrium_height(radius, density, voltage, width, frequency):
    """Height above the electrode where DEP force balances gravity.

    Returns nan when there is no balance point: either the DEP is positive
    rather than negative, or the field at the electrode is too weak to hold the
    particle up.
    """
    omega = 2.0 * pi * frequency
    k_cm = clausius_mossotti(omega).real

    net_weight = gravity_minus_buoyancy(radius, density)
    if k_cm >= 0.0 or net_weight <= 0.0:
        return float("nan")

    force_needed = net_weight / (2.0 * pi * radius**3 * medium_eps_m() * abs(k_cm))
    gradient_at_electrode = pi**3 * voltage**2 / (2.0 * width**3)

    if gradient_at_electrode < force_needed:
        return float("nan")

    return width / (2.0 * pi) * log(gradient_at_electrode / force_needed)


def gravity_minus_buoyancy(radius, particle_density):
    """Net weight of the particle, which is what balances the DEP force.

    Positive when the particle is denser than the medium and therefore sinks.
    """
    return 4.0 / 3.0 * pi * radius**3 * GRAVITY * (particle_density - MEDIUM_DENSITY)


def average_velocity():
    """Mean flow speed for 1 microlitre per hour through a 100 by 100 micrometre channel."""
    flow_rate = 1e-12 / 3600.0   # 1 uL/h in m^3/s
    area = (100e-6) ** 2          # channel cross-section
    return flow_rate / area