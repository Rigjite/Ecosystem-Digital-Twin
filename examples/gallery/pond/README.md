# Gallery entry — pond: small-pond eutrophication miniature (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

Will summer chlorophyll-a exceed the bathing advisory watch levels, and
is the eutrophication trend real?

## Data

Monthly total phosphorus (TP) and chlorophyll-a, 2023-01..2025-12
(`data.csv`, 36 rows). Formulas (no RNG): TP = 45 + 1.0/month +
22·sin(seasonal); chlorophyll = 6 + 0.5·lagged TP + 12·sin(seasonal).
TP runs 23.0–97.0 µg/L, chlorophyll 7.1–65.5 µg/L.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/pond/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py` on chlorophyll) | 36 rows, 0 flagged |
| TP trend (`trend_test.py`) | Increasing, p = 0.0004, Sen slope +12.0 µg/L per year |
| Trophic state, latest month (`trend_test.py --mode tsi`) | TSI composite 65.1, eutrophic |
| Calibration (`skill_scores.py continuous`, hold-out 2025) | Model chlorophyll ~ lagged TP + seasonal term, fitted on training data only: gate pass, ADMITTED, SS_RMSE 1.0, NSE 1.0 |
| Watch (`alert_bands.py`, amber ≥40, red ≥60 µg/L) | 4 alerts (3 amber, 1 red); red episode Aug–Oct 2025 |

The hold-out score is near-perfect by construction: the synthetic series
were generated from exactly the model form that is fitted. The entry
demonstrates the workflow (declared split, hold-out scoring, gate), not
a real model's skill. The watch levels are declared for this miniature,
not a regulatory standard.

## Maturity

3 (Informative): a calibrated component is admitted on a declared
hold-out and the alert bands are live.

## Gaps

- [НЕТ ДАННЫХ] no winter under-ice oxygen data
- [НЕТ ДАННЫХ] no sediment phosphorus release measurements
- [НЕТ ДАННЫХ] no measured inflow discharge (load is not quantified)
