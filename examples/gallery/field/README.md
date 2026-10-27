# Gallery entry — agricultural field: soil-moisture watch (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

Is the field drying toward the irrigation trigger, and when does soil
moisture cross the declared watch levels?

## Data

Daily soil moisture (%), 2026-04-01..2026-06-29 (`data.csv`, 90 rows).
Formula (no RNG): 30 − 0.20/day + seasonal wobble, with three rain
events (+7 points, draining exponentially over ~4 days). Moisture runs
10.9–32.7%.

The four open-data ETL streams for a field twin (daily, forecast and
historical weather, NDVI) are listed in `references/data-sources.md` §10.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/field/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py`) | 90 rows, 0 flagged |
| Moisture trend (`trend_test.py`) | Decreasing, p = 6.7e-16, Sen slope −75.1 %/yr (annualised from the 90-day drying) |
| Watch (`alert_bands.py`, amber <18, red <12 %) | 3 alerts (2 amber, 1 red); red episode from 2026-06-27; 26 days below amber, 3 below red |
| PFT shares (`diversity.py pft`) | Grass 82%, legume 10%, forb 8%; C3 100% — from `pft_cover.csv` (synthetic cover) and `pft_table.csv` (growth form and pathway from the TRY Plant Trait Database, Kattge et al. 2020). One season only: shares, no trend |

The watch levels are declared for this miniature (loam, cereal crop),
not measured field capacity or wilting point. The PFT cover values are
synthetic (declared in `pft_cover.csv`); the PFT assignments (growth
form, C3/C4) are the published TRY values for these species.
`trait_table.csv` carries Ellenberg indicator values (T, F, R, N, S)
for seven taxa — the field species plus two halophytes — the worked
example for `scripts/trait_match.py`. Source: the Ellenberg column in
Tichý et al. 2023, "Ellenberg-type indicator values for European
vascular plant species", Zenodo record 7427088 (Germany source Ellenberg
& Leuschner 2010, the revised edition of Ellenberg et al. 1991);
Salicornia values are ssp. europaea. Verified against the published
table 2026-10-26. "x" means Ellenberg is indifferent for that trait:
the taxon is not excluded by a condition on it.

## Maturity

2 (Descriptive): state, trend, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no measured field capacity or wilting point
- [НЕТ ДАННЫХ] no rain gauge (rainfall is part of the synthetic design)
- [НЕТ ДАННЫХ] one season only, no multi-year baseline
- [НЕТ ДАННЫХ] no PFT trend (one survey: shares only; a trend needs repeat surveys)
