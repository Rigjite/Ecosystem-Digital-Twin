# Gallery entry — forest carbon: Prince Albert FMA carbon stock (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

How much carbon does this forest store and accumulate, and is the stock
growing or shrinking?

## Data

Annual carbon density of living biomass, 2015–2025 (`carbon.csv`, 11
rows). Formulas (no RNG): starting density 52.00 t C/ha (2015); each
following year density = previous density + 0.55 t C/ha (gross growth)
− fire loss, where fire loss = burned_ha / 2,700,000 × density × 0.20.
Total stock = density × 2,700,000 ha of forested area. Net change
is the year-to-year difference of the density series, computed by the
runner (plain arithmetic, not a new formula).

The landscape is the Prince Albert Forest Management Agreement (PA FMA)
area, Saskatchewan — the same landscape as the forest-fire entry, so
the three forest entries share one landscape and consistent disturbance
years. Total area 3,354,418 ha, 2.7 million ha forested (Sakaw Askiy
Management Inc.); sustainable harvest rate recalculated to 1.92 million
m³/yr after disturbance exceeded FMP thresholds. The scale and pattern
echo the published record for Canadian boreal forests (design anchors,
NOT data):
- Boreal plant biomass: roughly 60–100 t C/ha, of which around 80% is
  in the above-ground biomass (Mahli et al. 1999; Luyssaert et al.
  2007, via UNEP) — so aboveground living biomass runs about 48–80
  t C/ha. The miniature's starting density (52.0 t C/ha) sits at the
  low end of that range.
- Boreal sequestration: a single hectare of healthy boreal forest can
  sequester between 0.5 and 2 t C/yr (Alberta studies). The miniature's
  gross growth (+0.55 t C/ha/yr) sits at the low end of that range.
- Fire losses use the forest-fire entry's annual burned areas for this
  same FMA (2019–2025: 101,400 / 65,400 / 90,405 / 83,265 / 87,230 /
  103,320 / 128,830 ha) and stated interpolation for 2015–2018
  (88,000 / 74,000 / 82,000 / 91,000 ha, rising toward 2019). The 0.20
  combustion fraction is a stated assumption, not a measured factor.
- Canada 2023 burned 18,496,051 ha, the national record (CIFFC);
  Saskatchewan 2023 burned about 1.9 million ha in 494 fires
  (Saskatchewan Public Safety Agency). The miniature's seasons
  (65,400–128,830 ha) are a small share of the provincial record.

Real data were checked first and found unusable for this miniature:
ESA CCI Biomass (global AGB maps, 100 m, annual 2007/2010/2015–2024,
CC BY 4.0, DOI 10.5285/95913ffb6467447ca72c4e9d8cf30501) is a raster
product (NetCDF/GeoTIFF); extracting a series needs raster processing,
outside the stdlib-only skill — the same raster problem as the JRC and
GFED products in the wetland and forest-fire entries; Global Forest
Watch data API (the only route to an annual series for an
administrative unit) requires a free API key (registration); the
dashboard and map pages are JavaScript-driven — the same key problem
as the forest-logging entry; US Forest Service FIA DataMart offers CSV
downloads without login, but building a clean annual carbon-stock
series means joining PLOT/TREE/COND tables across remeasurement cycles
(heavy harmonisation), and it is US data — off-story for a Saskatchewan
landscape; Canada's National Forest Inventory publishes national and
provincial totals, not an open annual series for one forest management
area.

## Carbon-credit boundary

This entry watches carbon stock and its change. It is NOT a
carbon-credit methodology and claims no compliance with any credit
standard (Verra, Gold Standard, or other). Credit accounting has its
own verification rules — additionality, permanence, leakage,
third-party verification — that this miniature does not implement.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/forest-carbon/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py`) | 11 rows, 0 flagged |
| Carbon-density trend (`trend_test.py`) | Increasing, p = 2.6e-05, Sen slope +0.208 t C/ha/yr |
| Net-change trend (`trend_test.py`, 10 rows, 2016–2025) | Decreasing, p = 0.039, Sen slope −0.017 t C/ha/yr — the yearly growth is slowing as fire losses grow |
| Total stock | 140.40 Mt C (2015) → 145.58 Mt C (2025): +5.18 Mt C, +3.7% |
| Smallest growth year | 2025: +0.04 t C/ha/yr (density 53.92 t C/ha) — the biggest fire year nearly stalled the growth |
| Watch, net change (`alert_bands.py`, amber ≤+0.15, red ≤0.0 t C/ha/yr) | 1 alert (1 amber, 0 red); amber episode 2024–2025, ongoing; 3 years below amber, 0 below red |

The density series rises through the window, so there is no low-density
watch: the decision-relevant signal is the net change, not the level.
The bands are declared watch levels for this miniature: the net-change
amber level (+0.15 t C/ha/yr) is a year when growth nearly stalled —
the fire loss ate almost all of the year's growth; the red level
(0.0 t C/ha/yr) is a year when the stock shrank. They are not a
regulatory standard, and they are not a carbon-credit threshold.

## Maturity

2 (Descriptive): state, trend check, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no measured carbon series for this FMA (ESA CCI Biomass is a raster product; GFW data API needs a key; FIA is US data and needs multi-table harmonisation; the National Forest Inventory publishes national and provincial totals, not an open annual series for one forest management area)
- [НЕТ ДАННЫХ] no logging-removal term for this FMA (losses here are fire only; the forest-logging entry covers British Columbia timber supply areas)
- [НЕТ ДАННЫХ] no soil carbon series (this miniature tracks living biomass carbon only)
- [НЕТ ДАННЫХ] no belowground split (roots are inside the living-biomass total, not measured separately)
- [НЕТ ДАННЫХ] this entry is not a carbon-credit methodology and claims no compliance with any credit standard (Verra, Gold Standard, or other)
