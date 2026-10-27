# Gallery entry — forest fire: Prince Albert FMA fire seasons (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

Are forest fires becoming more frequent or larger in this landscape,
and when does the fire season cross watch levels?

## Data

Monthly fire counts and burned area, fire seasons April–October,
2019–2025 (`fires.csv`, 49 rows). Formulas (no RNG): counts = base
(Apr 2, May 8, Jun 7, Jul 9, Aug 10, Sep 5, Oct 2) × year multiplier
(2019: 1.25, 2020: 1.00, 2021: 1.30, 2022: 1.15, 2023: 1.20,
2024: 1.30, 2025: 1.45) + deterministic wobble −1/0/+1; burned area =
counts × mean fire size (Apr 400, May 2200, Jun 1200, Jul 1800,
Aug 2000, Sep 700, Oct 300 ha) × size multiplier (2019: 1.20,
2020: 1.00, 2021: 1.05, 2022: 1.05, 2023: 1.10, 2024: 1.20,
2025: 1.30). Counts run 1–15 fires/month; burned area 300–39,000 ha/month.

The landscape is the Prince Albert Forest Management Agreement (PA FMA)
area, Saskatchewan (3,354,418 ha total, 2.7 million ha forested;
Sakaw Askiy Management Inc., Forest Management Plan 2018–2038), and
the scale and pattern echo the published Canadian record (design
anchors, NOT data): Canada 2023 burned 18,496,051 ha, the national
record (CIFFC) — about 250% above the previous record (1995:
7,105,998 ha) and about 8 times the national average of ~2.5 million
ha/yr; Saskatchewan 2023 saw 494 fires and about 1.9 million ha
burned (Saskatchewan Public Safety Agency) — about five times the size
of Prince Albert National Park (387,500 ha), and more than in 2015;
2025 passed 7.5 million ha burned nationally by mid-August (CIFFC).
The miniature's seasons (65,400–128,830 ha) burn 2.4–4.8% of the
FMA's forested area each year, a small share of the provincial record,
and its 2025 season (128,830 ha) is a new record, the endpoint of the
rising trend.

Real data were checked first and found unusable for this miniature:
NASA FIRMS Area API (the only route to a filtered multi-year series
for a bounding box) requires a free MAP_KEY (registration); FIRMS
public NRT CSVs are global files covering only the last 7 days; the
FIRMS archive and yearly summary by country need a login code or an
interactive form, and the summary is country-level only; GFED5,
Global Fire Atlas and Copernicus Burnt Area are gridded products whose
series need raster processing, outside the stdlib-only skill; no
published annual fire series exists for the PA FMA itself — the
provincial and national totals above are the anchors, not a series.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/forest-fire/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py` on both series) | 49 rows, 0 flagged |
| Fire-count trend (`trend_test.py`, seasonal Kendall) | Increasing, p = 0.011, Sen slope +0.17 fires/month per year |
| Burned-area trend (`trend_test.py`, seasonal Kendall) | Increasing, p = 0.0012, Sen slope +210 ha/month per year |
| Annual totals | 2019: 52 fires / 101,400 ha; 2020: 44 / 65,400 ha; 2021: 55 / 90,405 ha; 2022: 49 / 83,265 ha; 2023: 52 / 87,230 ha; 2024: 55 / 103,320 ha; 2025: 62 / 128,830 ha (biggest season) |
| Watch, fires (`alert_bands.py`, amber ≥11, red ≥13 per month) | 5 alerts (4 amber, 1 red); red episode Jul–Aug 2025; amber episodes Jul–Aug 2019, 2021, 2023, 2024; 13 months above amber, 7 above red |
| Watch, area (`alert_bands.py`, amber ≥20,000, red ≥30,000 ha/month) | 5 alerts (4 amber, 1 red); red episode Jul–Aug 2025; amber episodes Jul–Aug 2019, 2021, 2023, 2024; 17 months above amber, 5 above red |

The bands are declared watch levels for this miniature: the fire-count
amber band (11) sits below p90 of the 2019–2025 monthly window (13.0
fires/month) and the red band (13) sits at p90/p95 (13.0); the area
red band (30,000 ha/month) is approximately p90 of the window
(29,316 ha/month). They are not a regulatory standard.

## Maturity

2 (Descriptive): state, trend check, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no measured fire series for this FMA (FIRMS Area API needs a MAP_KEY; public NRT files cover 7 days only; GFED/Global Fire Atlas/Copernicus are gridded products)
- [НЕТ ДАННЫХ] no ignition causes (lightning vs human) in this miniature
- [НЕТ ДАННЫХ] no fuel moisture or fire-weather series (the trend is counts and area only, not cause)
- [НЕТ ДАННЫХ] no post-fire recovery series (burn-scar revegetation is not tracked here)
