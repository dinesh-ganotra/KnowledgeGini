"""The plateau-derivation figure (Fig. 14): simulated stable-society
plateau vs endowment CV, against the Gaussian closed form CV/sqrt(pi)
and the exact folded-Gaussian curve.

Usage:  python scripts/make_plateau_figure.py      (needs run_dispersion.py)
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
os.makedirs("figures", exist_ok=True)
z = np.load("results/dispersion.npz")

rng = np.random.default_rng(7)
def folded_gini(cv, n=1_500_000):
    x = np.abs(rng.normal(1.0, cv, n))
    xs = np.sort(x); i = np.arange(1, n + 1)
    return (2 * (i * xs).sum() / (n * xs.sum())) - (n + 1) / n

grid = np.linspace(0.20, 1.05, 35)
pred = np.array([folded_gini(c) for c in grid])

fig, ax = plt.subplots(figsize=(6.6, 4.6), dpi=300)
ax.plot(grid, grid / np.sqrt(np.pi), "--", color="0.55", lw=1.2,
        label=r"Gaussian: $G=\mathrm{CV}/\sqrt{\pi}$")
ax.plot(grid, pred, "-", color="k", lw=1.4,
        label=r"folded Gaussian $|N(\mu,\,\mathrm{CV}\cdot\mu)|$ (exact)")
ax.errorbar(z["cv"], z["simulated"], yerr=z["sd"], fmt="o", color="k",
            mfc="w", ms=7, capsize=3, lw=1.2,
            label="simulated plateau (stable society)", zorder=5)
ax.axvline(2/3, color="0.4", lw=0.8, ls=":")
i = int(np.argmin(np.abs(z["cv"] - 2/3)))
ax.annotate("model dispersion\nCV = 2/3  →  %.3f" % z["simulated"][i],
            xy=(2/3, z["simulated"][i]), xytext=(0.74, 0.24), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", lw=0.8, color="0.3"))
ax.set_xlabel("coefficient of variation of endowments, CV = σ/μ", fontsize=10)
ax.set_ylabel("steady-state Gini ratio of the stable society", fontsize=10)
ax.tick_params(labelsize=9)
ax.legend(fontsize=8.5, loc="upper left")
plt.tight_layout()
plt.savefig("figures/fig_plateau_derivation.png", bbox_inches="tight", facecolor="white")
print("figures/fig_plateau_derivation.png written")
