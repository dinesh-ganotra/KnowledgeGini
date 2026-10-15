"""The variant figures: Fig. 4 (lowest category, flat to the eye and
that is the point), Fig. 5 (doubling), and the two-panel pairs of
Figs. 6, 7 and 9. Fig. 8 is built by make_figures.py.

Usage:  python scripts/make_variant_figures.py     (needs run_figure_variants.py)
"""
import os, sys, glob, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
os.makedirs("figures", exist_ok=True)
S = slice(200, 1900)


def traj_panel(ax, key, letter, vec_label):
    runs = np.load("results/%s.npz" % key)["runs"]
    m, sd = runs.mean(0), runs.std(0)
    years = np.arange(1, len(m) + 1)
    ax.fill_between(years, m - sd, m + sd, color="0.72", lw=0)
    ax.plot(years, m, color="k", lw=0.9)
    ax.set_ylim(0, 1.05); ax.set_xlim(0, 2100)
    ax.set_xlabel("year", fontsize=9.5)
    ax.set_title("(%s)  r_ratio = %s" % (letter, vec_label), fontsize=9, loc="left")
    ax.tick_params(labelsize=8.5)
    steady = runs[:, S].mean()
    return steady


# ---- Fig. 4: flat panel vs X -------------------------------------------------
xs, ms, sds = [], [], []
for f in sorted(glob.glob("results/fig4_X*.npz")):
    x = float(re.search(r"X([\d.]+)\.npz", f).group(1))
    runs = np.load(f)["runs"]
    per_seed = runs[:, S].mean(1)
    xs.append(x); ms.append(per_seed.mean()); sds.append(per_seed.std())
fig, ax = plt.subplots(figsize=(5.8, 4.0), dpi=300)
ax.errorbar(xs, ms, yerr=sds, fmt="o-", color="k", mfc="w", ms=6, capsize=3, lw=1.2)
ax.axhline(0.330, ls="--", color="0.55", lw=1)
ax.set_xlabel("annual resource factor X of the lowest-knowledge category", fontsize=10)
ax.set_ylabel("steady-state Gini ratio\n(mean ± cross-seed SD)", fontsize=10)
ax.set_ylim(0.30, 0.36); ax.tick_params(labelsize=9)
plt.tight_layout()
plt.savefig("figures/fig4_lowest_category.png", bbox_inches="tight", facecolor="white")
plt.close()

# ---- Fig. 5: doubling, single trajectory panel -------------------------------
fig, ax = plt.subplots(figsize=(6.2, 4.0), dpi=300)
traj_panel(ax, "fig5_double", "", "[0.5, 2, 1, 1, 1, 1, 1]")
ax.set_title("r_ratio = [0.5, 2, 1, 1, 1, 1, 1]", fontsize=9.5)
ax.set_ylabel("Gini ratio", fontsize=10)
plt.tight_layout()
plt.savefig("figures/fig5_doubling.png", bbox_inches="tight", facecolor="white")
plt.close()

# ---- Figs. 6, 7, 9: two-panel pairs ------------------------------------------
PAIRS = [
    ("fig6", ("fig6a_r2_1.2", "[0.5, 1.2, 1, 1, 1, 1, 1]"),
             ("fig6b_r2_1.4", "[0.5, 1.4, 1, 1, 1, 1, 1]")),
    ("fig7", ("fig7a_r4_1.0", "[0.5, 1.1, 1.12, 1.0, 1, 1, 1]"),
             ("fig7b_r4_1.6", "[0.5, 1.1, 1.12, 1.6, 1, 1, 1]")),
    ("fig9", ("fig9a_base",   "baseline (6th element 1.03)"),
             ("fig9b_r6_1.2", "baseline with 6th element 1.2")),
]
for name, (ka, la), (kb, lb) in PAIRS:
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), dpi=300, sharey=True)
    sa = traj_panel(axes[0], ka, "a", la)
    sb = traj_panel(axes[1], kb, "b", lb)
    axes[0].set_ylabel("Gini ratio", fontsize=10)
    plt.tight_layout()
    plt.savefig("figures/%s_pair.png" % name, bbox_inches="tight", facecolor="white")
    plt.close()
    print("%s: (a) steady %.3f  (b) steady %.3f" % (name, sa, sb))

print("figures written:")
for f in sorted(os.listdir("figures")):
    if f.startswith(("fig4", "fig5", "fig6", "fig7", "fig9")):
        print(" ", f)
