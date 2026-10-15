"""The calibration table, rerun: every r_ratio vector tried on the way
to the accepted one, in the order of Table 3 of the manuscript.

Besides the steady-state level, the last two columns report the maximum
of the trajectory and the fraction of steady-state years spent above
0.95 -- that is how an "absorbing state" row of the table shows up in
numbers.

Usage:  python scripts/run_calibration.py [n_seeds]
"""
import sys, os
import numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data, game_of_knowledge

data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
S = slice(200, 1900)

STAGES = [
    ("initial_prior",   [0.5, 1.06, 1.07, 1.30, 1.50, 1.10, 1.20]),
    ("doubling",        [0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
    ("avg_1.6",         [0.5, 1.1, 1.12, 1.6, 1.0, 1.0, 1.0]),
    ("avg_1.10",        [0.5, 1.1, 1.12, 1.10, 1.0, 1.0, 1.0]),
    ("all_ones",        [1, 1, 1, 1, 1, 1, 1]),
    ("accepted",        [0.5, 1.1, 1.12, 1.098, 1.05, 1.03, 1.9]),
]

print("%-16s %-10s %-8s %-8s %s" % ("stage", "steady", "sd", "max", "frac>0.95"))
for name, v in STAGES:
    runs = np.array([game_of_knowledge(data, 1, r_ratio=np.array(v, float),
                                       seed=s)["gini"] for s in range(n)])
    seg = runs[:, S]
    per_seed = seg.mean(1)
    np.savez("results/calib_%s.npz" % name, runs=runs)
    print("%-16s %.3f      %.4f   %.3f    %.2f" %
          (name, per_seed.mean(), per_seed.std(), seg.max(), (seg > 0.95).mean()))
