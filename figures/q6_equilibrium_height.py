"""Figure 2: equilibrium height of the five particles against voltage and electrode width.

Part of the particle sits in the same equilibrium whether it is 150 nm or 600 nm
wide, because equilibrium is where the DEP force balances gravity and gravity
scales with volume. The five panels use the same colour scale so they can be
compared directly.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import dep_model as D

OUT = Path(__file__).resolve().parent / "figures" / "q6_equilibrium_height.pdf"

FREQUENCY = 10e6       # Hz
VOLTAGE = np.linspace(1.0, 20.0, 60)                        # V
WIDTH = np.logspace(np.log10(2e-6), np.log10(50e-6), 60)   # m

# Equilibrium sits below the electrode when the field gradient falls off fast
# enough for gravity to take over, so only accept solutions inside the channel.
CHANNEL_HEIGHT = 100e-6


def equilibrium_height(radius, density, voltage, width):
    """Height for this particle, or nan if the particle will not be held."""
    height = D.equilibrium_height(radius, density, voltage, width, FREQUENCY)
    if height != height or height > CHANNEL_HEIGHT:
        return np.nan
    return height


def main():
    voltage_grid, width_grid = np.meshgrid(VOLTAGE, WIDTH)
    scale = np.linspace(0, 80, 9)   # micrometres

    figure, axes = plt.subplots(1, 5, figsize=(20.0, 4.4), sharey=True)
    colors = plt.get_cmap("viridis")

    for axis, (label, radius, density) in zip(axes, D.PARTICLES):
        heights = np.vectorize(equilibrium_height)(radius, density,
                                                   voltage_grid, width_grid)
        filled = np.where(np.isnan(heights), np.nan, heights * 1e6)
        axis.contourf(voltage_grid * 1e6, width_grid * 1e6, filled,
                      levels=scale, cmap=colors)
        axis.set_title(label)
        axis.set_xlabel("V0 (V)")
        axis.set_yscale("log")

    axes[0].set_ylabel("electrode width (um)")
    figure.colorbar(axes[-1].collections[0], ax=axes, label="equilibrium height (um)")
    figure.suptitle("Equilibrium height against voltage and electrode width")
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    for label, radius, density in D.PARTICLES:
        height = equilibrium_height(radius, density, 10.0, 10e-6)
        print(f"{label}: y_eq = {height*1e6:.3f} um")


if __name__ == "__main__":
    main()