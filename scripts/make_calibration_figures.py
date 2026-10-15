"""Figures for the calibration subsection: the 2x3 small-multiples of
the tried vectors (Fig. 11) and the delay experiment under perturbed
calibrations (Fig. 13).

Usage:  python scripts/make_calibration_figures.py
Needs results from run_gap.py, run_calibration.py and run_robustness.py.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
os.makedirs("figures", exist_ok=True)
S = slice(200, 1900)

# ---------------- Figure: calibration stages (2x3 small multiples) ----------
STAGES = [
    ("initial_prior", "(a) initial prior", "[0.5, 1.06, 1.07, 1.30, 1.50, 1.10, 1.20]"),
    ("doubling",      "(b) doubling test", "[0.5, 2, 1, 1, 1, 1, 1]"),
    ("avg_1.6",       "(c) average category 1.6", "[0.5, 1.1, 1.12, 1.6, 1, 1, 1]"),
    ("avg_1.10",      "(d) average category 1.10", "[0.5, 1.1, 1.12, 1.10, 1, 1, 1]"),
    ("all_ones",      "(e) stable reference", "[1, 1, 1, 1, 1, 1, 1]"),
    ("accepted",      "(f) accepted", "[0.5, 1.1, 1.12, 1.098, 1.05, 1.03, 1.9]"),
]
fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.0), dpi=300, sharex=True, sharey=True)
for i, (ax, (key, name, vec)) in enumerate(zip(axes.flat, STAGES)):
    runs = np.load("results/calib_%s.npz" % key)["runs"]
    m, s = runs.mean(0), runs.std(0)
    years = np.arange(1, len(m) + 1)
    ax.fill_between(years, m - s, m + s, color="0.75", lw=0)
    ax.plot(years, m, color="k", lw=0.8)
    ax.axhline(1.0, color="0.5", lw=0.6, ls=":")
    ax.set_title(name, fontsize=9.5, fontweight="bold", loc="left")
    ax.text(0.03, 0.04, vec, transform=ax.transAxes, fontsize=7.5, color="0.25")
    ax.set_ylim(0, 1.05); ax.set_xlim(0, 2100)
    if i >= 3: ax.set_xlabel("year", fontsize=9)
    if i % 3 == 0: ax.set_ylabel("Gini ratio", fontsize=9)
    ax.tick_params(labelsize=8)
plt.tight_layout()
plt.savefig("figures/fig_calibration_stages.png", bbox_inches="tight", facecolor="white")
plt.close()

# ---------------- Figure: robustness of the delay result --------------------
delays = np.arange(1, 11)
base = np.array([np.load("results/gap_%d.npz" % d)["runs"][:, S].mean()
                 for d in delays])
SERIES = [
    ("baseline [0.5, 1.1, 1.12, 1.098, 1.05, 1.03, 1.9]", base, "-", "o"),
    ("r2 +10%",  np.load("results/robust_r2_plus10.npz")["means"],  "--", "s"),
    ("r4 −10%", np.load("results/robust_r4_minus10.npz")["means"], "-.", "^"),
    ("r5 −10%", np.load("results/robust_r5_minus10.npz")["means"], ":", "D"),
]
fig, ax = plt.subplots(figsize=(6.6, 4.6), dpi=300)
for label, m, ls, mk in SERIES:
    ax.plot(delays, m, color="k", ls=ls, marker=mk, mfc="w", ms=6, lw=1.3, label=label)
ax.set_xlabel("knowledge dissemination delay g (years)", fontsize=10)
ax.set_ylabel("steady-state Gini ratio", fontsize=10)
ax.set_xticks(delays); ax.tick_params(labelsize=9)
# legend placed in the empty band between the curve clusters
ax.legend(fontsize=8.5, title="calibration", title_fontsize=9,
          loc="center right", bbox_to_anchor=(0.99, 0.40), framealpha=1.0)
plt.tight_layout()
plt.savefig("figures/fig_robustness_delay.png", bbox_inches="tight", facecolor="white")
plt.close()

print("figures written to figures/:")
for f in sorted(os.listdir("figures")):
    print(" ", f)
