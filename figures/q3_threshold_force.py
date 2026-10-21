"""Figure 1: threshold force as a function of radius and observation time.

Sweeps particle radius and observation time over the ranges chosen in Q3 and
plots the threshold force on a surface.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import dep_model as D

OUT = Path(__file__).resolve().parent / "figures" / "q3_threshold_force.pdf"


def main():
    radii = np.linspace(50e-9, 1000e-9, 60)      # m
    times = np.logspace(-3, 1, 60)               # s

    radius_grid, time_grid = np.meshgrid(radii, times)
    forces = np.vectorize(D.threshold_force)(radius_grid, time_grid)

    # Plot in femtonewtons on a log scale so the whole range is readable.
    force_fN = np.log10(forces * 1e15)

    figure = plt.figure(figsize=(8.0, 6.0))
    axis = figure.add_subplot(111, projection="3d")
    axis.plot_surface(radius_grid * 1e9, np.log10(time_grid), force_fN,
                      cmap="viridis", edgecolor="none", alpha=0.92)

    axis.set_xlabel("particle radius (nm)", labelpad=12)
    axis.set_ylabel("log10 observation time (s)", labelpad=12)
    axis.set_zlabel("log10 threshold force (fN)", labelpad=12)
    axis.set_title("Threshold force against radius and observation time")

    figure.tight_layout()
    figure.savefig(OUT, bbox_inches="tight")
    plt.close(figure)
    print(f"Wrote {OUT}")

    print(f"Threshold force at 150 nm after 1 s: {D.threshold_force(150e-9, 1.0):.3e} N")
    print(f"Threshold force at 600 nm after 1 s: {D.threshold_force(600e-9, 1.0):.3e} N")


if __name__ == "__main__":
    main()