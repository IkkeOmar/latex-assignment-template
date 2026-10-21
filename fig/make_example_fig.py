
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.dpi": 200})
PURPLE, CYAN, MUTE = "#7C5CFC", "#38BDF8", "#4B5563"

f = np.logspace(2, 6, 400)
fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.6))

ax[0].loglog(f, 1/np.sqrt(1+(f/1e4)**2), color=PURPLE, lw=1.6, label="model")
ax[0].loglog(f, 1/np.sqrt(1+(f/1e3)**2), color=MUTE, lw=1.4, ls="--", label="variant")
ax[0].axvline(1e4, color=MUTE, ls=":", lw=1)
ax[0].set_xlabel(r"frequency $f$  [Hz]")
ax[0].set_ylabel(r"response  [arb.]")
ax[0].set_title("Single panel", pad=5)
ax[0].legend(fontsize=7.5)

x = np.arange(3)
ax[1].bar(x, [1.0, 2.5, 4.1], color=PURPLE, width=0.6)
ax[1].set_xticks(x); ax[1].set_xticklabels(["1 nm","10 nm","100 nm"])
ax[1].set_ylabel(r"value  [m]")
ax[1].set_title("Bar chart", pad=5)

fig.tight_layout()
import os
HERE = os.path.dirname(os.path.abspath(__file__))

fig.savefig(os.path.join(HERE, "example.pdf"))
fig.savefig(os.path.join(HERE, "example.png"))
print("example figure written to", HERE)
