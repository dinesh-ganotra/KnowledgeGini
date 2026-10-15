# Input data

`inputs.npz` holds the yearly series driving the simulation (years 1-2014),
extracted from the original study's `DataSimulated.mat`:

| array | meaning | construction |
|---|---|---|
| `Population` | world population, scaled by 1e-5 | Taagepera (2014) closed-form model |
| `GDPPerCapita` | 1990 Geary-Khamis $, scaled by 1/1000 | Maddison (2003), linear interpolation |
| `LEB` | life expectancy at birth | 29.5 up to 1769; Our World in Data thereafter |
| `Knowledge` | new knowledge per year (books) | Lavoie & Schonfeld (2006), anchored at 1 book in year 1 |
| `NewBorn`, `Dead` | yearly counts | derived for consistency with the population trajectory |
| `k_fraction` | age-dependent annual knowledge growth (150 ages) | crystallized-intelligence T-scores of Li et al. (2004), two-term exponential fit |

Full provenance: Appendix B of the manuscript.
