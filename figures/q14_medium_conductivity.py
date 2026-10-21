"""Figure 7: how the medium conductivity changes the impedance contrast.

Raising the medium conductivity lowers the medium resistance, so the parallel
medium branch takes over and the cell's own frequency response fades.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import impedance_model as I

OUT = Path(__file__).resolve().parent / "figures" / "q14_medium_conductivity.pdf"

FREQUENCY = np.logspace(4, 6, 400)   # Hz
CONDUCTIVITIES = [0.05, 0.1, 0.5, 1.0]   # S/m


def main():
    phi = I.volume_fraction()
    omega = 2.0 * np.pi * FREQUENCY
    colors = plt.get_cmap("viridis")

    figure, axis = plt.subplots(figsize=(8.5, 5.5))

    for index, sigma in enumerate(CONDUCTIVITIES):
        amplitude = np.abs(I.total_impedance(omega, phi, sigma))

        # Compare the two ends of the range the question asks about.
        high = np.interp(1e6, FREQUENCY, amplitude)
        change = (high - amplitude[0]) / amplitude[0] * 100

        axis.semilogx(FREQUENCY, amplitude / 1e3, lw=1.7,
                      color=colors(index / 3.0),
                      label=f"{sigma} S/m ({change:+.1f}%)")

    axis.set_xlabel("frequency (Hz)")
    axis.set_ylabel("|Z| (kOhm)")
    axis.set_title(f"Medium conductivity dependence  (Phi = {phi*100:.2f}%)")
    axis.set_ylim(bottom=0)
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=10, loc="lower left")

    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    for sigma in CONDUCTIVITIES:
        amplitude = np.abs(I.total_impedance(omega, phi, sigma))
        high = np.interp(1e6, FREQUENCY, amplitude)
        print(f"sigma = {sigma} S/m: R_m = {I.medium_resistance(phi, sigma):.3e} Ohm, "
              f"R_i = {I.interior_resistance(phi, sigma):.3e} Ohm, "
              f"high/low = {amplitude[0]/high:.3f}")


if __name__ == "__main__":
    main()