"""Figure 3: time and channel length needed for each particle to settle.

The height obeys an overdamped balance of DEP force, which decays
exponentially with height, against constant gravity. That integral is
inverted in closed form, so the time to travel from the starting height to a
chosen fraction of the way to equilibrium is available directly.
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

OUT = Path(__file__).resolve().parent / "figures" / "q9_settling_time.pdf"

FREQUENCY = 10e6        # Hz
VOLTAGE = 10.0          # V
WIDTH = 10e-6           # m
START_HEIGHT = 50e-6    # m, where every particle begins

# Fraction of the remaining distance still to travel when we call it settled.
TOLERANCES = [(0.1, "90%"), (0.01, "99%"), (0.001, "99.9%")]


def travel_time(radius, density, target_height):
    """Time for the particle to fall from the start to the target height."""
    omega = 2.0 * pi * FREQUENCY
    k_cm = D.clausius_mossotti(omega).real

    drag = 6.0 * pi * D.VISCOSITY * radius
    force_at_electrode = (2.0 * pi * radius**3 * D.medium_eps_m() * abs(k_cm)
                          * 32.0 * pi**2 * VOLTAGE**2 / WIDTH**3)
    net_weight = D.gravity_minus_buoyancy(radius, density)

    ratio = net_weight / force_at_electrode

    def phase(height):
        """Antiderivative of the equation of motion at a given height."""
        u = exp(-3.0 * pi**2 * height / WIDTH)
        return log(abs((u - ratio) / u))

    return (-drag * WIDTH / (3.0 * pi**2 * force_at_electrode * ratio)
            * (phase(target_height) - phase(START_HEIGHT)))


def main():
    labels, rows = [], {name: [] for _, name in TOLERANCES}

    for label, radius, density in D.PARTICLES:
        equilibrium = D.equilibrium_height(radius, density, VOLTAGE, WIDTH, FREQUENCY)
        labels.append(label)
        for fraction, name in TOLERANCES:
            # Still this fraction of the distance away when we stop counting.
            target = equilibrium + fraction * (START_HEIGHT - equilibrium)
            rows[name].append(travel_time(radius, density, target))

    figure, axis = plt.subplots(figsize=(8.5, 5.0))
    positions = np.arange(len(labels))
    width = 0.26

    for index, (_, name) in enumerate(TOLERANCES):
        axis.bar(positions + (index - 1) * width, rows[name], width,
                 label=f"settled to {name}")
    axis.set_xticks(positions)
    axis.set_xticklabels(labels)
    axis.set_ylabel("time to settle (s)")
    axis.set_yscale("log")
    axis.set_title("Time needed to reach equilibrium at 10 V, 10 um, 10 MHz")
    axis.legend()
    axis.grid(True, axis="y", alpha=0.3)
    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    print(f"Mean flow speed: {D.average_velocity()*1e3:.4f} mm/s")
    for index, label in enumerate(labels):
        times = [rows[name][index] for _, name in TOLERANCES]
        print(f"{label}: " + "  ".join(f"{t:.3g} s" for t in times))


if __name__ == "__main__":
    main()