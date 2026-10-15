"""Is the central result an artifact of the calibration? Repeat the
delay experiment with the calibration knocked about -- one sensitive
element at a time moved by 10% -- and check that the strictly monotone
decrease of the Gini ratio with the delay survives. It does: the level
shifts, the shape does not.

Usage:  python scripts/run_robustness.py [n_seeds]
"""
import sys, os
import numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data, game_of_knowledge, BASELINE_R_RATIO

data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
S = slice(200, 1900)

PERTURBATIONS = [("r2_plus10", 1, 1.1), ("r4_minus10", 3, 0.9), ("r5_minus10", 4, 0.9)]

for name, j, f in PERTURBATIONS:
    v = BASELINE_R_RATIO.copy(); v[j] *= f
    means = []
    for delay in range(1, 11):
        runs = np.array([game_of_knowledge(data, delay, r_ratio=v, seed=s)["gini"]
                         for s in range(n)])
        means.append(runs[:, S].mean())
    means = np.array(means)
    np.savez("results/robust_%s.npz" % name, means=means)
    mono = bool((np.diff(means) < 0).all())
    print("%-12s g1=%.3f g10=%.3f span=%+.3f monotone=%s" %
          (name, means[0], means[9], means[0] - means[9], mono))
    print("   ", " ".join("%.3f" % m for m in means))
