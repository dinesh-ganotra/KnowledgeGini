"""Does this code reproduce the published results?

baselines/gap_baseline.csv holds the steady-state Gini ratio per delay
from the runs reported in earlier versions of the manuscript. The test
reruns all ten delays and asks for agreement within 0.02 -- loose on
purpose, because only three seeds are used here to keep the test under
a couple of minutes, and the two implementations draw different random
numbers. What must hold exactly is the shape: the Gini ratio has to
decrease strictly with the delay, and the stable society has to sit on
its 0.33 plateau.
"""
import csv, sys, numpy as np
sys.path.insert(0, ".")
from knowledgegini.game_of_knowledge import load_data, game_of_knowledge

def test_delay_regression():
    data = load_data("data/inputs.npz")
    base = {int(r["gap"]): float(r["mean_200_1900"])
            for r in csv.DictReader(open("baselines/gap_baseline.csv"))}
    means = []
    for d in range(1, 11):
        m = np.mean([game_of_knowledge(data, delay_years=d, seed=s)["gini"][200:1900].mean()
                     for s in range(3)])
        assert abs(m - base[d]) < 0.02, "delay %d: %.3f vs %.3f" % (d, m, base[d])
        means.append(m)
    assert all(np.diff(means) < 0), "Gini must decrease with delay"

def test_stable_plateau():
    data = load_data("data/inputs.npz")
    m = game_of_knowledge(data, delay_years=1, r_ratio=np.ones(7),
                          seed=0)["gini"][200:1900].mean()
    assert abs(m - 0.33) < 0.02, "stable plateau %.3f != 0.33" % m
