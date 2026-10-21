"""Figure 8: influence of the electrical double layer on the impedance.

The double layer acts as a capacitance in series with the whole circuit, so it
matters at low frequency and drops out as the frequency rises. The crossover
sits where its reactance equals the medium resistance.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import impedance_model as I

OUT = Path(__file__).resolve().parent / "figures" / "q16_edl_sweep.pdf"
OUT_ZOOM = Path(__file__).resolve().parent / "figures" / "q16_edl_zoom.pdf"


def crossover_frequency(phi):
    """Frequency where the EDL reactance equals the medium resistance."""
    return 1.0 / (2.0 * np.pi * I.medium_resistance(phi) * I.EDL_CAPACITANCE)


def main():
    phi = I.volume_fraction()
    corner = crossover_frequency(phi)

    frequency = np.logspace(2, 6, 500)
    omega = 2.0 * np.pi * frequency

    without = np.abs(I.total_impedance(omega, phi))
    with_edl = np.abs(I.total_impedance_with_edl(omega, phi))

    figure, (top, bottom) = plt.subplots(2, 1, figsize=(8.5, 6.5), sharex=True)

    top.semilogx(frequency, without / 1e3, "k-", lw=1.5, label="without EDL")
    top.semilogx(frequency, with_edl / 1e3, "b-", lw=1.7, label="with EDL")
    top.axvline(corner, color="red", ls="--", lw=0.8,
                label=f"f_EDL = {corner:.3g} Hz")
    top.set_ylabel("|Z| (kOhm)")
    top.set_title("Impedance with and without the electrical double layer")
    top.legend(fontsize=9)
    top.grid(True, which="both", alpha=0.3)

    bottom.semilogx(frequency, with_edl / without, lw=1.7)
    bottom.axhline(1.02, color="gray", ls=":", lw=0.8, label="2% threshold")
    bottom.axvline(corner, color="red", ls="--", lw=0.8)
    bottom.set_xlabel("frequency (Hz)")
    bottom.set_ylabel("ratio with / without")
    bottom.legend(fontsize=9)
    bottom.grid(True, which="both", alpha=0.3)

    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    # A close look at the crossover itself.
    zoom_frequency = np.logspace(np.log10(corner) - 2, np.log10(corner) + 2, 500)
    zoom_omega = 2.0 * np.pi * zoom_frequency
    zoom_without = np.abs(I.total_impedance(zoom_omega, phi))
    zoom_with = np.abs(I.total_impedance_with_edl(zoom_omega, phi))

    zoom_figure, zoom_axis = plt.subplots(figsize=(8.5, 4.2))
    zoom_axis.semilogx(zoom_frequency, zoom_without / 1e3, "k-", lw=1.9,
                       label="without EDL")
    zoom_axis.semilogx(zoom_frequency, zoom_with / 1e3, "r-", lw=1.6,
                       label="with EDL")
    zoom_axis.axvline(corner, color="gray", ls=":", lw=0.9,
                      label=f"f_EDL = {corner:.3g} Hz")
    zoom_axis.set_xlabel("frequency (Hz)")
    zoom_axis.set_ylabel("|Z| (kOhm)")
    zoom_axis.set_title("Zoom on the EDL crossover region")
    zoom_axis.legend(fontsize=9)
    zoom_axis.grid(True, which="both", alpha=0.3)
    zoom_figure.tight_layout()
    zoom_figure.savefig(OUT_ZOOM, bbox_inches="tight")
    plt.close(zoom_figure)
    print(f"Wrote {OUT_ZOOM}")

    print(f"R_m = {I.medium_resistance(phi):.4e} Ohm")
    print(f"f_EDL = {corner:.4e} Hz ({corner/1e3:.2f} kHz)")

    index = int(np.argmin(np.abs(frequency - corner)))
    print(f"At f_EDL: {without[index]/1e3:.2f} kOhm without, "
          f"{with_edl[index]/1e3:.2f} kOhm with, "
          f"ratio {with_edl[index]/without[index]:.3f}")


if __name__ == "__main__":
    main()