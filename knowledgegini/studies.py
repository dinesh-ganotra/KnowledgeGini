"""The parameter studies behind the paper's figures.

Each function here runs the model across seeds and returns everything in
memory; the wrappers in scripts/ save the arrays with experiment-encoded
filenames so a figure can always be traced back to its runs.

A word on the steady-state window. Statistics are taken over the years
in STEADY_YEARS, i.e. years 200-1900 of the 2014-year horizon. The
first ~100 years are the dying-out of the arbitrary year-1 population
and say nothing about the model; the final decades are visibly
non-stationary (GDP per capita surges and the trajectories drift), so
averaging over them would blur level with trend. The same window, up to
rounding, was used in the original analysis.
"""

import numpy as np
from .game_of_knowledge import game_of_knowledge, BASELINE_R_RATIO

STEADY_YEARS = slice(200, 1900)


def steady_state_stats(gini_series):
    seg = gini_series[STEADY_YEARS]
    return float(seg.mean()), float(seg.std())


def introduce_gap(data, delays=range(1, 11), seeds=range(10)):
    """The central experiment of the paper (Fig. 2 family): the Gini
    ratio as a function of the dissemination delay g, every delay run
    across seeds."""
    out = {}
    for d in delays:
        runs = np.array([game_of_knowledge(data, delay_years=d, seed=s)["gini"]
                         for s in seeds])
        out[d] = {"runs": runs, "mean": runs.mean(0), "sd": runs.std(0)}
    return out


def perturb_r_ratio_10percent(data, delay_years=1, seeds=range(10), frac=0.10):
    """The reviewer's sensitivity request: each element of the baseline
    r_ratio moved by +/-10% while the other six stay at baseline. Feeds
    the tornado plot."""
    out = {"baseline": _run_seeds(data, BASELINE_R_RATIO, delay_years, seeds)}
    for j in range(7):
        for factor, tag in [(1 - frac, "minus"), (1 + frac, "plus")]:
            r = BASELINE_R_RATIO.copy()
            r[j] *= factor
            out["r%d_%s10" % (j + 1, tag)] = _run_seeds(data, r, delay_years, seeds)
    return out


def vary_average_category_growth(data, values=np.arange(1.00, 1.101, 0.01),
                                 delay_years=1, seeds=range(10)):
    """Fine sweep of the growth factor of the average-knowledge category
    (the fourth r_ratio element), categories 5-7 held at 1. This sweep
    is what replaced the single-run threshold claim of the earlier
    manuscript: across seeds the dependence turns out smooth and
    near-linear, with no jump anywhere in the range."""
    out = {}
    for v in values:
        r = np.array([0.5, 1.1, 1.12, v, 1.0, 1.0, 1.0])
        out[round(float(v), 2)] = _run_seeds(data, r, delay_years, seeds)
    return out


def stable_society(data, seeds=range(10), delay_years=1):
    """r_ratio = 1 for every category: nobody's resources ever change
    after birth. The Gini ratio settles at 0.33 -- the plateau whose
    closed-form origin is derived in the paper."""
    return _run_seeds(data, np.ones(7), delay_years, seeds)


def stable_society_vs_dispersion(data, stdev_divs=(1.0, 1.5, 2.0, 3.0),
                                 seeds=range(5)):
    """The verification behind the plateau derivation: rerun the stable
    society with the dispersion divisor varied, and compare the
    simulated plateau with CV/sqrt(pi), the Gini ratio of Gaussian
    endowments. The folded-Gaussian correction closes the remaining
    gap; see the dispersion script for the exact comparison."""
    out = {}
    for d in stdev_divs:
        runs = np.array([game_of_knowledge(data, delay_years=1,
                                           r_ratio=np.ones(7), seed=s,
                                           stdev_div=d)["gini"]
                         for s in seeds])
        m, sd = steady_state_stats(runs.mean(0))
        out[d] = {"runs": runs, "mean": runs.mean(0), "sd": runs.std(0),
                  "steady_mean": m, "steady_sd": sd,
                  "predicted": (1.0 / d) / np.sqrt(np.pi)}
    return out


def _run_seeds(data, r_ratio, delay_years, seeds):
    runs = np.array([game_of_knowledge(data, delay_years=delay_years,
                                       r_ratio=r_ratio, seed=s)["gini"]
                     for s in seeds])
    m, s = steady_state_stats(runs.mean(0))
    return {"runs": runs, "mean": runs.mean(0), "sd": runs.std(0),
            "steady_mean": m, "steady_sd": s}
