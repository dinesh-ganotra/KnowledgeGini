"""The central experiment: the Gini ratio vs the dissemination delay.

Runs the model for g = 1..10, each across seeds, and prints the
steady-state level per delay. Two spreads are reported side by side:
the temporal sd (how much a trajectory wobbles year to year) and the
much smaller cross-seed sd (how much the level moves between seeds) --
it is the second one that decides whether differences between delays
mean anything.

Usage:  python scripts/run_gap.py [n_seeds]      (default 10, ~3 min)
"""
import sys, os, numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data
from knowledgegini.studies import introduce_gap, steady_state_stats
data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
res = introduce_gap(data, seeds=range(n))
for d, r in res.items():
    np.savez("results/gap_%d.npz" % d, runs=r["runs"], mean=r["mean"], sd=r["sd"])
    m, s = steady_state_stats(r["mean"])
    cross = r["runs"][:, 200:1900].mean(1).std()
    print("delay=%2d: steady %.3f (temporal sd %.3f, cross-seed sd %.4f)" % (d, m, s, cross))
