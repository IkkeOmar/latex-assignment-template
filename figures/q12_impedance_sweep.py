"""Figure 5: impedance amplitude and phase across the frequency sweep.

Plots the total impedance from 10 kHz to 10 MHz and marks the membrane corner
frequency, which is set by the time constant of the cell branch.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import impedance_model as I

OUT = Path(__file__).resolve().parent / "figures" / "q12_impedance_sweep.pdf"

FREQUENCY = np.logspace(4, 6, 400)   # Hz


def main():
    phi = I.volume_fraction()
    omega = 2.0 * np.pi * FREQUENCY

    impedance = I.total_impedance(omega, phi)
    amplitude = np.abs(impedance)
    phase = np.angle(impedance, deg=True)

    r_m = I.medium_resistance(phi)
    r_i = I.interior_resistance(phi)
    c_mem = I.membrane_capacitance(phi)
    membrane_corner = 1.0 / (2.0 * np.pi * r_i * c_mem)

    figure, (top, bottom) = plt.subplots(2, 1, figsize=(8.5, 6.5), sharex=True)

    top.semilogx(FREQUENCY, amplitude / 1e3, "k-", lw=1.8)
    top.axhline(r_m / 1e3, color="gray", ls=":", lw=0.8, label=f"R_m = {r_m/1e3:.1f} kOhm")
    top.axvline(membrane_corner, color="red", ls="--", lw=0.8,
                label=f"f_mem = {membrane_corner:.2e} Hz")
    top.set_ylabel("|Z| (kOhm)")
    top.set_title(f"Total impedance amplitude  (Phi = {phi*100:.2f}%)")
    top.legend(fontsize=9, loc="lower left")
    top.grid(True, which="both", alpha=0.3)

    bottom.semilogx(FREQUENCY, phase, "b-", lw=1.5)
    bottom.axvline(membrane_corner, color="red", ls="--", lw=0.8)
    bottom.axhline(0.0, color="gray", ls=":", lw=0.8)
    bottom.set_xlabel("frequency (Hz)")
    bottom.set_ylabel("phase (degrees)")
    bottom.grid(True, which="both", alpha=0.3)

    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    print(f"R_m = {r_m:.4e} Ohm, R_i = {r_i:.4e} Ohm, C_mem = {c_mem:.4e} F")
    print(f"f_mem = {membrane_corner:.4e} Hz")

    low = amplitude[0]
    high = np.interp(1e6, FREQUENCY, amplitude)
    print(f"|Z| at 10 kHz: {low/1e3:.2f} kOhm")
    print(f"|Z| at 10 MHz: {high/1e3:.2f} kOhm")
    print(f"Change 10 kHz to 10 MHz: {(high - low)/low*100:+.2f}%")


if __name__ == "__main__":
    main()