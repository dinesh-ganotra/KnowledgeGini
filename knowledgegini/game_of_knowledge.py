"""The Game of Knowledge.

The name is a nod to Conway's Game of Life: a population evolves under a
handful of local rules, and a global quantity -- here the inequality of
resources, measured by the Gini ratio -- emerges on its own.

Every simulated person carries four numbers: life span, age, knowledge
and resources. Year after year newborns arrive, everyone's knowledge
grows along the crystallized-intelligence curve, people are placed into
seven knowledge categories relative to the population mean, and their
resources compound category-wise. The one knob of interest is the
dissemination delay g: how old the societal knowledge is that a newborn
cohort inherits. The paper's central result is that smaller g -- faster
spread of knowledge -- settles at a *higher* steady-state Gini ratio.

The code began life in Matlab (GameOfKnowledgeVer5.m,
RedistributeResourceAndKnowledge.m, AnalyzeResult.m); this is a
line-faithful Python port with seed control added, so every figure of
the paper can be reproduced exactly. The yearly loop below is frozen:
it reproduces what the original code actually did, which in two or
three places is not what a casual reading of the paper might suggest --
those places are flagged in the steps.

  Year 1: N(1) persons; life ~ round|N(LEB1, LEB1/1.5)|,
  age ~ round|N(20, 20/1.5)|, resources ~ |N(G1, G1/1.5)|,
  knowledge = Knowledge(1) for everyone. Zero life spans are discarded.

  Each year t = 2..T:
    1. record M(t), the mean knowledge of the living population
       (taken before the newborns' knowledge is appended);
    2. births: NB(t) newborns, life ~ round|N(LEB(t), LEB(t)/1.5)|,
       age = 1, resources = 0.1*|N(G(t), G(t)/1.5)|,
       knowledge = M(t-(delay_years-1)) for t > 10, else M(t) --
       identical for the whole cohort. This is the only place the
       dissemination delay enters the model;
    3. ageing: age += 1 for everyone;
    4. mortality: remove persons with life - age <= 0. Mortality is by
       age only -- the resource-ranked removal present in the Matlab
       source was dead code, never called, so it is not ported;
    5. knowledge growth: K *= k_fraction[age], the fitted 150-element
       crystallized-intelligence ratio vector. It is applied at every
       age, not gated to ages 10-90; ages beyond the vector reuse its
       last value;
    6. categorization: nearest of {1,5,10,12,15,17,20}/15 * meanK,
       where meanK is the mean recorded before step 5's growth -- the
       order of operations of the original loop;
    7. resources: R *= r_ratio[category];
    8. record the Gini ratio of the resources vector.

Throughout, every Gaussian draw uses sigma = mean/stdev_div (default
1.5, i.e. a fixed coefficient of variation of 2/3) -- the StDevDiv
convention of the original code. This single dispersion choice is what
sets the 0.33 plateau of the stable society; see the dispersion study.
"""

import numpy as np

BASELINE_R_RATIO = np.array([0.5, 1.1, 1.12, 1.098, 1.05, 1.03, 1.9])
K_LEVELS = np.array([1, 5, 10, 12, 15, 17, 20]) / 15.0
STDEV_DIV = 1.5


def load_data(path="data/inputs.npz"):
    """Load the yearly input series and the k_fraction vector."""
    z = np.load(path)
    return {k: z[k] for k in z.files}


def gini(resources):
    """Gini ratio of a resources vector.

    Computed exactly as the original AnalyzeResult.m did: sort, build the
    Lorenz curve over x = linspace(0, 1, N), and integrate by the
    trapezoidal rule. For the population sizes here the difference from
    the textbook pairwise formula is negligible, but keeping the same
    estimator keeps the regression against the published runs clean.
    """
    r = np.sort(resources)
    lorenz = np.cumsum(r) / r.sum()
    x = np.linspace(0.0, 1.0, r.size)
    return 1.0 - 2.0 * np.trapezoid(lorenz, x)


def game_of_knowledge(data, delay_years, r_ratio=None, seed=0, t_end=None,
                      stdev_div=None):
    """
    Run one simulation and return its yearly series.

    data        : dict from load_data().
    delay_years : the dissemination delay g, 1..10. Newborns of year t
                  inherit the mean knowledge of year t-(g-1); g = 1
                  means they get the current mean.
    r_ratio     : the 7 category-wise resource growth factors. Defaults
                  to the published baseline.
    seed        : RNG seed; pass None for a nondeterministic run.
    t_end       : last simulated year index (default: the full horizon,
                  2014 years).
    stdev_div   : dispersion divisor d; every Gaussian draw then uses
                  sigma = mean/d. Left at the default 1.5 everywhere
                  except in the stable-society dispersion study, which
                  varies it to verify the origin of the 0.33 plateau.

    Returns a dict with 'gini' (length T; the year-1 entry is 0),
    'population' and 'mean_knowledge'.
    """
    rng = np.random.default_rng(seed)
    r_ratio = BASELINE_R_RATIO if r_ratio is None else np.asarray(r_ratio, float)
    d = STDEV_DIV if stdev_div is None else float(stdev_div)
    LEB, G = data["LEB"], data["GDPPerCapita"]
    NB, K1 = data["NewBorn"].astype(int), data["Knowledge"][0]
    kf = data["k_fraction"]
    T = int(t_end or len(LEB))

    def draw(mean, n):
        return np.abs(rng.normal(mean, mean / d, n))

    # Year 1: the founding population. Its statistics barely matter --
    # it dies out within about a century, which is the initialization
    # transient visible at the left edge of every trajectory figure.
    n0 = int(data["Population"][0])
    life = np.rint(draw(LEB[0], n0))
    age = np.rint(np.abs(rng.normal(20.0, 20.0 / d, n0)))
    alive = life > 0
    life, age = life[alive], age[alive]
    res = draw(G[0], n0)[alive]
    kno = np.full(life.size, K1)

    gini_series = np.zeros(T)
    pop = np.zeros(T, int)
    mean_k = np.zeros(T)
    pop[0] = life.size

    for t in range(2, T + 1):          # calendar year t; arrays index t-1
        i = t - 1
        mean_k[i] = kno.mean()                                  # step 1
        nb = NB[i]                                              # step 2
        if nb > 0:
            nb_life = np.rint(draw(LEB[i], nb))
            nb_res = 0.1 * draw(G[i], nb)
            src = i - (delay_years - 1) if t > 10 else i
            life = np.concatenate([life, nb_life])
            age = np.concatenate([age, np.ones(nb)])
            res = np.concatenate([res, nb_res])
            kno = np.concatenate([kno, np.full(nb, mean_k[src])])
        age += 1.0                                              # step 3
        alive = (life - age) > 0                                # step 4
        life, age, res, kno = life[alive], age[alive], res[alive], kno[alive]
        meanK = kno.mean()                                      # steps 5-7
        idx = np.clip(age.astype(int) - 1, 0, kf.size - 1)      # Matlab is 1-based
        kno = kno * kf[idx]
        cat = np.argmin(np.abs(kno[:, None] - (K_LEVELS * meanK)[None, :]), axis=1)
        res = res * r_ratio[cat]
        gini_series[i] = gini(res)                              # step 8
        pop[i] = life.size

    return {"gini": gini_series, "population": pop, "mean_knowledge": mean_k}
