"""Figures from the gap and sensitivity runs: the Fig. 2 trajectories,
the stationary-vs-delay panel, the tornado plot and the r4 sweep, and
the stable-society plateau.

Usage:  python scripts/make_figures.py
Needs results from run_gap.py and run_sensitivity.py.
"""
import os, sys, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
os.makedirs("figures", exist_ok=True)
STAT = slice(200, 1900)


def stat_mean_sd(runs):
    per_seed = runs[:, STAT].mean(axis=1)
    return per_seed.mean(), per_seed.std()


# ---------------- Figure 2: Gini vs year for g = 1, 6, 10, mean +/- SD ------
fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=300)
colors = {1: "tab:red", 6: "tab:green", 10: "tab:blue"}
years = None
for g in (1, 6, 10):
    z = np.load(f"results/gap_{g}.npz")
    m, s = z["runs"].mean(0), z["runs"].std(0)
    years = np.arange(1, len(m) + 1)
    ax.plot(years, m, color=colors[g], lw=1.0, label=f"{g}-year delay")
    ax.fill_between(years, m - s, m + s, color=colors[g], alpha=0.25, lw=0)
ax.set_xlabel("year"); ax.set_ylabel("Gini ratio")
ax.set_xlim(0, 2100); ax.set_ylim(0, 1)
ax.legend(title="knowledge dissemination delay g", loc="lower right")
ax.set_title("Gini ratio vs year: mean \u00b1 SD over seeds", fontsize=11)
plt.tight_layout(); plt.savefig("figures/fig2_gap_trajectories.png"); plt.close()

# ---------------- Figure 2b: stationary Gini vs delay ------------------------
gaps, ms, ss = [], [], []
for g in range(1, 11):
    z = np.load(f"results/gap_{g}.npz")
    m, s = stat_mean_sd(z["runs"])
    gaps.append(g); ms.append(m); ss.append(s)
fig, ax = plt.subplots(figsize=(5.6, 4.2), dpi=300)
ax.errorbar(gaps, ms, yerr=ss, fmt="o-", color="k", mfc="w", capsize=3)
ax.set_xlabel("knowledge dissemination delay g (years)")
ax.set_ylabel("stationary Gini ratio (mean \u00b1 cross-seed SD)")
ax.set_xticks(gaps)
plt.tight_layout(); plt.savefig("figures/fig2b_stationary_vs_delay.png"); plt.close()

# ---------------- Sensitivity: +/-10% tornado -------------------------------
base = stat_mean_sd(np.load("results/pm10_baseline.npz")["runs"])[0]
labels, lo, hi = [], [], []
for j in range(1, 8):
    labels.append(f"r_ratio({j})")
    lo.append(stat_mean_sd(np.load(f"results/pm10_r{j}_minus10.npz")["runs"])[0])
    hi.append(stat_mean_sd(np.load(f"results/pm10_r{j}_plus10.npz")["runs"])[0])
fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=300)
y = np.arange(7)
ax.barh(y, np.array(hi) - base, left=base, height=0.6, color="0.35", label="+10%")
ax.barh(y, np.array(lo) - base, left=base, height=0.6, color="0.75", label="\u221210%")
ax.axvline(base, color="k", lw=1)
ax.set_yticks(y); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlabel(f"stationary Gini ratio (baseline = {base:.3f})")
ax.legend(loc="lower right")
ax.set_title("Sensitivity of the stationary Gini to \u00b110% in each r_ratio element", fontsize=10.5)
plt.tight_layout(); plt.savefig("figures/fig_sensitivity_tornado.png"); plt.close()

# ---------------- Sensitivity: r4 sweep --------------------------------------
vals, m4, s4 = [], [], []
for f in sorted(glob.glob("results/r4_*.npz")):
    v = float(f.split("_")[-1].replace(".npz", ""))
    m, s = stat_mean_sd(np.load(f)["runs"])
    vals.append(v); m4.append(m); s4.append(s)
sl, ic = np.polyfit(vals, m4, 1)
fig, ax = plt.subplots(figsize=(5.6, 4.2), dpi=300)
ax.errorbar(vals, m4, yerr=s4, fmt="o-", color="k", mfc="w", capsize=3)
ax.plot(vals, ic + sl * np.array(vals), "--", color="0.5", lw=1,
        label=f"linear fit, slope {sl:.2f}")
ax.set_xlabel("annual resource growth of the average-knowledge category")
ax.set_ylabel("stationary Gini ratio (mean \u00b1 cross-seed SD)")
ax.legend()
plt.tight_layout(); plt.savefig("figures/fig_sensitivity_r4sweep.png"); plt.close()

# ---------------- Stable plateau ---------------------------------------------
z = np.load("results/stable.npz")["runs"]
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=300)
for k in range(z.shape[0]):
    ax.plot(np.arange(1, z.shape[1] + 1), z[k], lw=0.6, alpha=0.7)
m, s = stat_mean_sd(z)
ax.axhline(0.33, ls="--", color="k", lw=1)
ax.set_xlabel("year"); ax.set_ylabel("Gini ratio"); ax.set_ylim(0, 1)
ax.set_title(f"Stable configuration (r_ratio = 1): plateau {m:.4f} \u00b1 {s:.4f} across seeds", fontsize=10.5)
plt.tight_layout(); plt.savefig("figures/fig_stable_plateau.png"); plt.close()

print("figures written to figures/:")
for f in sorted(os.listdir("figures")):
    print(" ", f)
