# Gallery entry — air basin: Prince George winter PM2.5 watch (synthetic)

> **SYNTHETIC — a teaching miniature.** Every number below is invented
> by deterministic formulas to show the shape of a finished build. It is
> not a measurement and must never be cited as data.

## Management question

How many winter days exceed the WHO 2021 daily PM2.5 guideline
(45 µg/m³), and when do smog episodes start?

## Data

Daily PM2.5, 2026-01-05..2026-02-28 (`data.csv`, 55 rows). Formula
(no RNG): baseline 14 µg/m³ with a weekly wobble (Mon–Sun
14.0/17.2/18.0/15.8/12.4/10.2/11.0) and three planted wood-smoke
inversion episodes (peaks 121.4, 86.7, 66.2 µg/m³). 10 days above 45,
4 above 75.

Prince George, British Columbia (53.9°N, 122.7°W, ~575 m), sits in
the valley at the confluence of the Nechako and Fraser rivers.
Winter temperature inversions are common: cold air is trapped near
the ground and wood smoke from residential heating — plus industrial
and vehicle emissions — cannot disperse. The BC provincial air
quality objective for PM2.5 is 25 µg/m³ averaged over 24 hours.
On 2026-01-25, inside this window, the BC Air Quality Warning for
Prince George reported a 24-hour average PM2.5 of 33 µg/m³, above
the objective (BC Ministry of Environment and Parks, Air Quality
Warnings, aqwarnings.gov.bc.ca). Winters are the worst season for
air quality in Prince George, and the city Clean Air Bylaw
restricts open burning during advisories.

Real data were checked first: the CAMS model (Open-Meteo) for Prince
George over the same window returns hourly values, but the model grid
is too coarse to resolve the valley inversion, so no model series was
substituted; the BC station network publishes 24-hour averages, and
the full hourly station series for the 55-day window was not pulled
into a CSV for this teaching build. The synthetic series shows what
the twin does once measurements exist.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/air/run.py`). Standard library only.

| Step | Result |
|---|---|
| Quality gate (`qc_series.py`) | 55 rows, 0 flagged |
| PM2.5 trend (`trend_test.py`) | No significant trend, p = 0.40 — episodes do not make a trend |
| Watch (`alert_bands.py`, amber ≥45, red ≥75 µg/m³) | 4 alerts (3 amber, 1 red); red episode 2026-01-14..16 |

Amber is the WHO 2021 daily guideline (45 µg/m³); red is the WHO 2021
interim target 1, daily (75 µg/m³).

## Maturity

2 (Descriptive): state, trend check, and watch — no calibrated forecast.

## Gaps

- [НЕТ ДАННЫХ] no hourly station series pulled for the window (BC network publishes 24-hour averages; Prince George 33 µg/m³ on 2026-01-25, above the provincial objective 25 µg/m³)
- [НЕТ ДАННЫХ] no wind or inversion-height data (episode cause not attributed)
- [НЕТ ДАННЫХ] one winter window only, no multi-year baseline
