"""Figure 4: trajectory of each particle through the channel.

Turns the settling time into distance along the channel, so the height can be
plotted against position instead of against time. All five particles start at
the same point and separate as they fall towards their own equilibrium.
"""
import sys
from math import exp, log, pi
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import dep_model as D

OUT = Path(__file__).resolve().parent / "figures" / "q10_trajectories.pdf"

FREQUENCY = 10e6
VOLTAGE = 10.0
WIDTH = 10e-6
START_HEIGHT = 50e-6
CHANNEL_LENGTH = 500e-6   # m, length drawn on the plot


def height_at_time(radius, density, elapsed):
    """Height of the particle after a given time, or its equilibrium height."""
    omega = 2.0 * pi * FREQUENCY
    k_cm = D.clausius_mossotti(omega).real

    equilibrium = D.equilibrium_height(radius, density, VOLTAGE, WIDTH, FREQUENCY)

    drag = 6.0 * pi * D.VISCOSITY * radius
    force_at_electrode = (2.0 * pi * radius**3 * D.medium_eps_m() * abs(k_cm)
                          * 32.0 * pi**2 * VOLTAGE**2 / WIDTH**3)
    net_weight = D.gravity_minus_buoyancy(radius, density)

    ratio = net_weight / force_at_electrode
    factor = force_at_electrode * (3.0 * pi**2 / WIDTH) / drag

    start = exp(-3.0 * pi**2 * START_HEIGHT / WIDTH)
    start_phase = log(abs((start - ratio) / start))

    # Past the settling time the particle simply sits at equilibrium.
    if elapsed * factor > start_phase - 1e-12:
        return equilibrium

    remaining = start_phase - factor * elapsed
    fraction = abs((ratio / exp(remaining)) - 1.0)
    return -(WIDTH / (3.0 * pi**2)) * (-log(fraction)


def main():
    flow_speed = D.average_velocity()
    distances = np.linspace(0.0, CHANNEL_LENGTH, 400)

    figure, axis = plt.subplots(figsize=(9.0, 5.0))
    colors = plt.get_cmap("viridis")

    for index, (label, radius, density) in enumerate(D.PARTICLES):
        times = distances / flow_speed
        heights = np.array([height_at_time(radius, density, t) for t in times])

        axis.plot(distances * 1e3, heights * 1e6, lw=1.8,
                  color=colors(index / 4.0), label=label)

        equilibrium = D.equilibrium_height(radius, density, VOLTAGE, WIDTH, FREQUENCY)
        axis.plot(distances[-1] * 1e3, equilibrium * 1e6, "o",
                  color=colors(index / 4.0), markersize=6)

    axis.set_xlabel("distance along channel (mm)")
    axis.set_ylabel("height above electrode (um)")
    axis.set_title(f"Trajectories at {VOLTAGE:.0f} V, {WIDTH*1e6:.0f} um electrodes, "
                   f"{FREQUENCY/1e6:.0f} MHz")
    axis.legend(fontsize=9)
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    for label, radius, density in D.PARTICLES:
        equilibrium = D.equilibrium_height(radius, density, VOLTAGE, WIDTH, FREQUENCY)
        print(f"{label}: settles at {equilibrium*1e6:.3f} um")


if __name__ == "__main__":
    main()