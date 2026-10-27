# Gallery entry — forest logging: British Columbia timber supply areas (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

Where and how much forest is being lost to logging in this landscape,
and is the loss accelerating?

## Data

Annual logged area by timber supply area and harvest volume, 2015–2025
(`logging.csv`, 11 rows). Formulas (no RNG): logged area rises from
17,900 ha/yr (2015) to 30,600 ha/yr (2025) with one shared dip in 2020
(slowdown year); harvest volume = logged area × mean yield (192–210
m³/ha, deterministic wobble), 3.44–6.43 million m³/yr. Total over the
window: 257,100 ha logged, 51.56 million m³ harvested.

The landscape is three real British Columbia timber supply areas —
Prince George, Quesnel, Mackenzie — and the scale and pattern echo the
published record for the province (design anchors, NOT data):
- BC timber harvest: 38.9 million m³ (2023), 39.0 (2024), 37.7 (2025);
  Interior 26.9 million m³ in 2023 (BC Harvest Billing System, "2025
  Economic State of British Columbia's Forestry Sector"). The
  miniature's three-TSA total (3.4–6.4 million m³/yr) is a small share
  of the provincial harvest, as actual harvest runs well below the
  allowable cut.
- Prince George Timber Supply Area: allowable annual cut (AAC)
  12.5 million m³ (2011, reduced from a 14.9 peak; pre-beetle 9.3);
  base-case forecast initial harvest 10.1 million m³ for 10 years.
- Quesnel Timber Supply Area: AAC 4.0 million m³ (pre-beetle 2.34);
  mid-term timber supply projection 1.15 million m³/yr.
- Mackenzie Timber Supply Area: AACs cut 18.4% in 2024 to align harvest
  with the Chief Forester's May 2023 AAC determination.
- Minimum harvest volume 140 m³/ha (BC Mid-Term Timber Supply
  Project); the miniature's yields (192–210 m³/ha) sit above that
  merchantability threshold, as interior mature stands run higher.

Real data were checked first and found unusable for this miniature:
Global Forest Watch data API (the only route to an annual series for an
administrative unit) requires a free API key (registration); GFW
dashboard and map pages are JavaScript-driven, and the annual
tree-cover-loss series is not in the fetchable page text; Hansen / GLAD
gridded data need raster processing, outside the stdlib-only skill;
BC publishes harvest totals by region in the Economic State of the
Forest Sector and the Harvest Billing System, not an open annual series
by timber supply area; published aggregates give no clean annual series
for three TSAs.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/forest-logging/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py` on both series) | 11 rows, 0 flagged |
| Logged-area trend (`trend_test.py`) | Increasing, p = 5.2e-05, Sen slope +1,220 ha/yr |
| Harvest-volume trend (`trend_test.py`) | Increasing, p = 5.2e-05, Sen slope +272,750 m³/yr |
| Where (district shares, 2015–2025) | Prince George 47.0%, Quesnel 31.0%, Mackenzie 22.0% — Prince George is the largest loss every year |
| Biggest year | 2025: 30,600 ha logged, 6,426,000 m³ harvested |
| Watch, area (`alert_bands.py`, amber ≥24,500, red ≥28,000 ha/yr) | 2 alerts (1 amber, 1 red); amber episode from 2022, red episode from 2024, both ongoing; 4 years above amber, 2 above red |
| Watch, volume (`alert_bands.py`, amber ≥5.0, red ≥5.7 million m³/yr) | 2 alerts (1 amber, 1 red); amber episode from 2022, red episode from 2024, both ongoing; 4 years above amber, 2 above red |

The bands are declared watch levels for this miniature: the area amber
level (24,500 ha/yr) sits between the 2015–2021 maximum (23,800) and
the 2022 value (25,400); the area red level (28,000 ha/yr) sits
between the 2023 value (26,900) and the 2024 value (28,700); the
volume amber level (5.0 million m³/yr) sits between the 2021 value
(4.81) and the 2022 value (5.21); the volume red level (5.7 million
m³/yr) sits between the 2023 value (5.35) and the 2024 value (5.94).
They are not a regulatory standard, and they are not the allowable
annual cut (AAC) of any timber supply area.

## Maturity

2 (Descriptive): state, trend check, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no measured logging series for these timber supply areas (GFW data API needs a key; dashboard and map pages are JavaScript-driven; Hansen/GLAD rasters need raster processing; BC publishes regional harvest totals, not an open annual series by timber supply area)
- [НЕТ ДАННЫХ] no split of loss by driver in this miniature (the GFW total-loss anchors mix logging, fire, and other disturbances; the miniature's series is logging only, by design)
- [НЕТ ДАННЫХ] no regeneration or reforestation series (net change is not tracked here)
- [НЕТ ДАННЫХ] no illegal-logging estimate (official harvest only, by design)
