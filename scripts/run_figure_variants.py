"""Multi-seed runs for the variant figures (Figs. 4-7 and 9): the
lowest-category range, the doubling case, and the (a)/(b) pairs.
The r4 sweep behind Fig. 8 comes from run_sensitivity.py instead.

Usage:  python scripts/run_figure_variants.py [n_seeds]
"""
import sys, os
import numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data, game_of_knowledge

data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
S = slice(200, 1900)

VARIANTS = [
    # Fig. 4: lowest category X = 0 ... 1
    *[("fig4_X%.1f" % x, [x, 1, 1, 1, 1, 1, 1]) for x in
      (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)],
    # Fig. 5: doubling of the unskilled category
    ("fig5_double",  [0.5, 2.0, 1, 1, 1, 1, 1]),
    # Fig. 6: unskilled 20% vs 40%
    ("fig6a_r2_1.2", [0.5, 1.2, 1, 1, 1, 1, 1]),
    ("fig6b_r2_1.4", [0.5, 1.4, 1, 1, 1, 1, 1]),
    # Fig. 7: average category no growth vs 60%
    ("fig7a_r4_1.0", [0.5, 1.1, 1.12, 1.0, 1, 1, 1]),
    ("fig7b_r4_1.6", [0.5, 1.1, 1.12, 1.6, 1, 1, 1]),
    # Fig. 9: technocrat category baseline (1.03) vs 20%
    ("fig9a_base",   [0.5, 1.1, 1.12, 1.098, 1.05, 1.03, 1.9]),
    ("fig9b_r6_1.2", [0.5, 1.1, 1.12, 1.098, 1.05, 1.2, 1.9]),
]

print("%-16s steady   sd      max     frac>0.95" % "variant")
for name, v in VARIANTS:
    runs = np.array([game_of_knowledge(data, 1, r_ratio=np.array(v, float),
                                       seed=s)["gini"] for s in range(n)])
    seg = runs[:, S]
    per_seed = seg.mean(1)
    np.savez("results/%s.npz" % name, runs=runs)
    print("%-16s %.3f    %.4f  %.3f   %.2f" %
          (name, per_seed.mean(), per_seed.std(), seg.max(), (seg > 0.95).mean()))
