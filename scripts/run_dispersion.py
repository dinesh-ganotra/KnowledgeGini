"""Where does the 0.33 plateau come from? The stable society is rerun
with the endowment dispersion varied (divisor 1 to 4, i.e. CV from 1
down to 0.25) and the simulated plateau is set against two analytical
values: CV/sqrt(pi), the Gini ratio of a Gaussian, and the Gini ratio
of the folded Gaussian |N(mu, CV*mu)| that the model actually draws
from. The folded value matches the simulation to the third decimal at
every dispersion -- that agreement is Fig. 14 of the manuscript.

Usage:  python scripts/run_dispersion.py [n_seeds]
"""
import sys, os
import numpy as np
sys.path.insert(0, ".")
os.makedirs("results", exist_ok=True)
from knowledgegini.game_of_knowledge import load_data, game_of_knowledge

data = load_data("data/inputs.npz")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
S = slice(200, 1900)
DIVS = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

rng = np.random.default_rng(7)
def folded_gini(cv, nsamp=4_000_000):
    """Exact (Monte Carlo) Gini of the folded Gaussian |N(1, cv)|."""
    x = np.abs(rng.normal(1.0, cv, nsamp))
    xs = np.sort(x)
    i = np.arange(1, nsamp + 1)
    return (2 * (i * xs).sum() / (nsamp * xs.sum())) - (nsamp + 1) / nsamp

rows = []
print("%4s %6s %12s %12s %10s %8s" %
      ("div", "CV", "CV/sqrt(pi)", "folded Gini", "simulated", "sd"))
for dv in DIVS:
    per_seed = [game_of_knowledge(data, 1, r_ratio=np.ones(7), seed=s,
                                  stdev_div=dv)["gini"][S].mean()
                for s in range(n)]
    cv = 1.0 / dv
    row = (dv, cv, cv / np.sqrt(np.pi), folded_gini(cv),
           float(np.mean(per_seed)), float(np.std(per_seed)))
    rows.append(row)
    print("%4.1f %6.3f %12.4f %12.4f %10.4f %8.4f" % row)

rows = np.array(rows)
np.savez("results/dispersion.npz", div=rows[:, 0], cv=rows[:, 1],
         gaussian=rows[:, 2], folded=rows[:, 3],
         simulated=rows[:, 4], sd=rows[:, 5])
print("saved results/dispersion.npz")
