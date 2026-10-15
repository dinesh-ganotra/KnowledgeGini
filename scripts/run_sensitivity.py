"""The sensitivity runs: +/-10% on every r_ratio element, the fine
sweep of the average-knowledge category, and the stable society.

Everything lands in results/ under names the figure scripts expect
(pm10_*, r4_*, stable).

Usage:  python scripts/run_sensitivity.py [n_seeds]
"""
import sys, os, numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data
from knowledgegini.studies import (perturb_r_ratio_10percent,
                                       vary_average_category_growth,
                                       stable_society)
data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
pm = perturb_r_ratio_10percent(data, seeds=range(n))
for k, r in pm.items():
    np.savez("results/pm10_%s.npz" % k, runs=r["runs"])
    print("pm10 %-12s: %.3f" % (k, r["steady_mean"]))
sw = vary_average_category_growth(data, seeds=range(n))
for v, r in sw.items():
    np.savez("results/r4_%.2f.npz" % v, runs=r["runs"])
    print("r4=%.2f: %.3f" % (v, r["steady_mean"]))
st = stable_society(data, seeds=range(n))
np.savez("results/stable.npz", runs=st["runs"])
print("stable: %.4f" % st["steady_mean"])
