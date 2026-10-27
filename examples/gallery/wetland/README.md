# Gallery entry — wetland: Everglades treatment wetland + marsh (real data)

## Management question

Is the treatment wetland still removing nutrients, and is the marsh
drying?

## Data

Real, from two published streams of the Everglades wetland system
(South Florida, USA), different cells and different periods. The entry
demonstrates the twin's two watches on the streams the system actually
publishes; a synchronous single-object record is [НЕТ ДАННЫХ].

- Nutrients (`nutrients.csv`, 13 monthly rows): influent and effluent
  total phosphorus (TP, µg/L) of the Algal Turf Scrubber (ATS) mobile
  pilot unit at the STA-1W discharge canal (Stormwater Treatment Area 1
  West, a constructed wetland, 2,700 ha), Aug 2008..Aug 2009. Source:
  South Florida Water Management District, "Lake Okeechobee Watershed
  Advanced Treatment Systems (ATS) Projects" (public document), table
  "Total Phosphorus (µg/L)", without-microfiltration series. The MPU
  floway is 1 ft wide x 1200 ft long, operated at 20 gpm. The
  document's stated means are 35 µg/L in, 24 µg/L out, and the stated
  TP reduction is 33.3%; the arithmetic means of the published monthly
  integers are 34.9 and 23.4 µg/L, and the mean of the monthly
  reductions computed here is 33.6% — the small differences are the
  document's rounding / flow-weighting, not an error in the table.
- Water level (`level.csv`, 121 daily rows): gage height (ft NAVD88) at
  EDEN 10 in Water Conservation Area 3-B, USGS NWIS site
  254707080370201 (25.7853 N, -80.6172 W), 2025-12-01..2026-03-31.
  Source: USGS National Water Information System, parameter 00065,
  daily mean values, fetched 2026-10-26. USGS data are public domain.
  Values 2025-12-01..18 are approved (qualifier A); from 2025-12-19
  they are provisional (qualifier P). The NWIS site file lists the
  land-surface altitude as 5 ft NAVD88, so the approximate water depth
  at the window minimum (5.26 ft) was about 0.26 ft — the marsh was
  nearly dry.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/wetland/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py` on outflow TP) | 13 rows, 0 flagged |
| Quality gate (`qc_series.py` on level) | 121 rows, 0 flagged |
| Nutrient removal, per month (out-in)/in | Median 35.4%, mean 33.6% (document's stated mean 33.3%); the skill's Beira case uses a median published TP removal of 46% as its reference — this pilot removed less |
| Removal trend (`trend_test.py`) | No significant trend, p = 0.23 — removal held steady across the 13 months, including a near-zero month (Sep 2008, 1.9%) |
| Level trend (`trend_test.py`) | Decreasing, p < 0.001, Sen slope −2.60 ft/yr — the dry-season drawdown |
| Level range | 6.10 ft (2025-12-01) → 5.26 ft minimum (2026-03-12) → 5.48 ft (2026-03-31); 14 days ≤ amber, 8 days ≤ red |
| Watch, outflow TP (`alert_bands.py`, amber ≥13, red ≥19 µg/L) | 3 alerts (1 amber, 2 red); red episodes Aug–Nov 2008 and Jun–Aug 2009; outflow above 13 µg/L in all 13 months |
| Watch, level (`alert_bands.py`, amber ≤5.37, red ≤5.33 ft) | 4 alerts (2 amber, 2 red); red episodes 2026-03-09..14 and 2026-03-27..28 |

The outflow TP bands are the STA water-quality-based effluent limit
(WQBEL, SFWMD): the annual flow-weighted mean outflow TP shall not
exceed 13 µg/L in more than 3 out of 5 water years, and shall not
exceed 19 µg/L in any water year. They are applied here as monthly
watch levels; a monthly breach is not itself a WQBEL violation. The
level bands are the 10th and 5th percentiles of this 121-day window,
declared watch levels for this miniature, not a regulatory standard.

## Maturity

2 (Descriptive): state, trend check, and watch on two published
streams — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no synchronous single-object record (nutrient cell 2008–09, marsh gage 2025–26)
- [НЕТ ДАННЫХ] no water extent series — JRC Global Surface Water was checked: the dataset is distributed as raster tiles / via the Explorer, and computing extent needs raster processing, outside the stdlib-only skill; water level from USGS EDEN is used as the drying signal instead
- [НЕТ ДАННЫХ] no inflow/outflow flows for the pilot (loads not quantified)
- [НЕТ ДАННЫХ] no nitrogen series for this cell (TP only)
