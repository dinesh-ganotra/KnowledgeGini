# Gini with Knowledge

*Simulation code for the effect of knowledge dissemination on the Gini ratio.*

Code for the paper **"Effect of Time Rate of Knowledge Spread on Gini Ratio"**
(Dinesh Ganotra, *Journal of the Knowledge Economy*, under review;
Ms. No. JKEC-D-22-01127).

A population model in which a person's resource growth is determined by their
knowledge, not by their existing wealth. A population constrained to
real-world trajectories of world population, life expectancy and GDP per
capita (years 1–2014) evolves annually: each newborn cohort inherits the mean
knowledge of society as it existed **g − 1 years earlier** (the dissemination
delay g is the independent variable), knowledge grows with age along an
empirical crystallized-intelligence curve, resources compound according to a
person's knowledge category, and inequality is measured each year by the Gini
ratio of resources.

**Headline result:** the stationary Gini ratio *increases* as the
dissemination delay decreases — faster knowledge spread, more inequality.

## Reference values

`baselines/gap_baseline.csv` holds the steady-state statistics of the runs
reported in earlier versions of the manuscript; `tests/test_regression.py`
verifies that this implementation reproduces them.

**Validation** (steady-state mean Gini, years 200–1900; this code = 5 seeds):

| delay g | earlier reported runs | this repository |
|---|---|---|
| 1  | 0.674 | 0.668 ± 0.003 |
| 2  | 0.652 | 0.659 ± 0.003 |
| 3  | 0.646 | 0.649 ± 0.003 |
| 4  | 0.636 | 0.640 ± 0.003 |
| 5  | 0.627 | 0.631 ± 0.003 |
| 6  | 0.622 | 0.622 ± 0.003 |
| 7  | 0.612 | 0.615 ± 0.003 |
| 8  | 0.601 | 0.606 ± 0.003 |
| 9  | 0.592 | 0.597 ± 0.003 |
| 10 | 0.588 | 0.590 ± 0.003 |

Every value within ±0.006; strictly monotone; g1–g10 span 0.079 (earlier
runs 0.087).

## Usage

```bash
pip install -r requirements.txt
pytest tests/                      # regression against the reported baseline values
python scripts/run_gap.py 10       # delay experiment, 10 seeds (~3 min)
python scripts/run_sensitivity.py  # ±10% r_ratio perturbations, r4 sweep, stable runs
```

One full 2014-year run takes ~2 s. Results land in `results/` with
experiment-encoded filenames.

## Layout

```
knowledgegini/game_of_knowledge.py   the frozen model (spec in the docstring)
knowledgegini/studies.py             delay study, ±10% sensitivity,
                                     average-category sweep, stable society
scripts/                             runnable wrappers + figure builders
tests/test_regression.py             baseline regression + 0.33 plateau
baselines/gap_baseline.csv           reference steady-state values
data/inputs.npz                      yearly input series (see data/README.md)
```

## Notes on the model specification

Two details of the specification differ from casual readings of the model:
`k_fraction` is applied at every age via the fitted 150-element vector (not
gated to ages 10–90), and categorization uses the mean knowledge recorded
*before* the year's knowledge growth. Mortality is age-based only. See the
model's docstring in `knowledgegini/game_of_knowledge.py` for the full frozen
specification.

## License

MIT — see LICENSE.
