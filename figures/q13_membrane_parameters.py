"""Figure 6: effect of membrane thickness and permittivity on the impedance.

Both parameters act only through the membrane capacitance, so the visible
effect is a shift of the corner frequency rather than a change in contrast.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import impedance_model as I

OUT = Path(__file__).resolve().parent / "figures" / "q13_membrane_parameters.pdf"

FREQUENCY = np.logspace(4, 6, 400)   # Hz
THICKNESSES = [2e-9, 5e-9, 10e-9, 20e-9]      # m
PERMITTIVITIES = [2.0, 4.0, 8.0, 12.0, 16.0]  # relative to epsilon_0


def main():
    phi = I.volume_fraction()
    omega = 2.0 * np.pi * FREQUENCY
    colors = plt.get_cmap("viridis")

    figure, (left, right) = plt.subplots(1, 2, figsize=(11.5, 5.0), sharey=True)

    for index, thickness in enumerate(THICKNESSES):
        impedance = I.total_impedance(omega, phi, thickness=thickness)
        left.semilogx(FREQUENCY, np.abs(impedance) / 1e3, lw=1.6,
                      color=colors(index / 3.0), label=f"{thickness*1e9:.0f} nm")
    left.set_xlabel("frequency (Hz)")
    left.set_ylabel("|Z| (kOhm)")
    left.set_title("Varying membrane thickness")
    left.grid(True, which="both", alpha=0.3)
    left.legend(title="thickness", fontsize=9)

    for index, permittivity in enumerate(PERMITTIVITIES):
        impedance = I.total_impedance(omega, phi, permittivity=permittivity)
        right.semilogx(FREQUENCY, np.abs(impedance) / 1e3, lw=1.6,
                       color=colors(index / 4.0),
                       label=f"{permittivity:.0f}")
    right.set_xlabel("frequency (Hz)")
    right.set_title("Varying membrane permittivity")
    right.grid(True, which="both", alpha=0.3)
    right.legend(title="permittivity / eps_0", fontsize=9)

    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    r_i = I.interior_resistance(phi)
    for thickness in THICKNESSES:
        capacitance = (9.0 * phi * I.CELL_RADIUS / 4.0) * I.membrane_eps() \
            / thickness * I.ELECTRODE_LENGTH * I.kappa()
        print(f"thickness {thickness*1e9:5.1f} nm: C_mem = {capacitance:.3e} F, "
              f"f_mem = {1.0/(2.0*np.pi*r_i*capacitance):.3e} Hz")


if __name__ == "__main__":
    main()