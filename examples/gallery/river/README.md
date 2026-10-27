# Gallery entry — river reach: Potomac River at Little Falls (real data)

## Management question

Are high-flow days increasing in this reach, and when does flow cross
the declared watch levels?

## Data

Real: USGS National Water Information System, site 01646500 (Potomac
River near Washington, DC, Little Falls pump station), parameter 00060
(discharge), daily values 2026-08-01..2026-10-20 (`data.csv`, 81 rows),
converted from ft³/s to m³/s (× 0.0283168). USGS data are public domain.
Fetched 2026-10-26; values are provisional (qualifier P). Flow runs
37.1–625.8 m³/s; the window contains one flood event, 2026-10-12..20,
peaking at 625.8 m³/s on 2026-10-14.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/river/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py`) | 81 rows, 0 flagged |
| Flow trend (`trend_test.py`) | No significant trend, p = 0.65 — 81 days are too short for a trend claim, and the flood sits at the end of the window |
| Watch (`alert_bands.py`, amber ≥155, red ≥280 m³/s) | 2 alerts; red episode 2026-10-13..16 (peak 625.8 m³/s); 9 days above amber, 4 above red |

The watch levels are the 90th and 95th percentiles of this 81-day
window, rounded — declared watch levels for this miniature, not a
regulatory standard and not a flood stage.

## Maturity

2 (Descriptive): state, trend check, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no water chemistry for this reach (no WPI)
- [НЕТ ДАННЫХ] 81 days is too short for a trend claim
- [НЕТ ДАННЫХ] no rating curve to a flood stage
