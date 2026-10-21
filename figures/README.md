# Figure scripts

Python scripts that generate every figure in the assignment.

Run any of them from this folder:

```bash
python3 q12_impedance_sweep.py
```

Figures land in `figures/` as vector PDF.

## Shared models

| File | Contents |
|---|---|
| `dep_model.py` | Constants, water properties, the five particles, Brownian motion, the threshold force, the Clausius-Mossotti factor, gravity minus buoyancy, and the equilibrium height. |
| `impedance_model.py` | The cell-medium volume fraction, the four circuit components, the two parallel branches, and the total impedance with and without the double layer. |

## Figure scripts

| File | Produces |
|---|---|
| `q3_threshold_force.py` | Threshold force against particle radius and observation time. |
| `q6_equilibrium_height.py` | Equilibrium height against voltage and electrode width, one panel per particle. |
| `q9_settling_time.py` | Time to settle for each particle, for three tolerance levels. |
| `q10_trajectories.py` | Height against distance along the channel for all five particles. |
| `q12_impedance_sweep.py` | Impedance amplitude and phase across the frequency sweep. |
| `q13_membrane_parameters.py` | Effect of membrane thickness and permittivity. |
| `q14_medium_conductivity.py` | Effect of the medium conductivity on the impedance contrast. |
| `q16_edl.py` | Impedance with and without the double layer, plus a zoom on the crossover. |

## Notes

The two model files hold the physics. The figure scripts only choose ranges and
draw, so changing a parameter in one place updates every figure.

All units are SI. The medium is water at 20 degrees Celsius unless stated
otherwise.

The only dependencies are `numpy` and `matplotlib`.