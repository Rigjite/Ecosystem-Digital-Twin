# Open-series demonstration of the computational core

Three public series, run through the bundled scripts exactly as an agent
would. Unlike `lake-example.md`, every number here is a real result that
anyone can reproduce:

    pip install statsmodels
    python3 examples/open_series_demo.py --out demo_out

(statsmodels only fetches the data; the scripts themselves need nothing but
the standard library. Lake Huron comes from Rdatasets and needs network
access.) Results below were produced with skill v2.2, statsmodels 0.15.0
and Python 3.13 on 2026-10-21.

## Data

| Series | Period | Unit | Source |
|---|---|---|---|
| Nile flow at Aswan | 1871–1970, annual | 10^8 m³ | Cobb (1978), Biometrika 65: 243–251, doi:10.1093/biomet/65.2.243 |
| Lake Huron level | 1875–1972, annual | feet (converted to m) | Brockwell & Davis (1996), Introduction to Time Series and Forecasting, Springer |
| CO2 at Mauna Loa | 1958–2001, weekly | ppm | Keeling & Whorf (2004), CDIAC, Oak Ridge National Laboratory |

## Results

| Series | Check | Result |
|---|---|---|
| Nile | Pettitt change point (`qc_series.py`) | after 1898, p < 1e-6; mean 1097.8 → 850.0 (−22.6%) |
| Nile | Mann–Kendall, whole period, Hamed–Rao (`trend_test.py`) | Sen −2.6 ×10^8 m³/yr per year; Z = −2.82; p = 0.005 |
| Nile | Same, with the 1899 break registered | 1871–1898: p = 0.67; 1899–1970: p = 0.34 — no trend in either segment |
| Lake Huron | Mann–Kendall: none / TFPW / Hamed–Rao | Z = −5.16 / −7.25 / −2.85 (lag-1 r = 0.76; n/n* = 3.29); Sen −7.7 mm/yr (95% CI −13.0 to −2.6) |
| Lake Huron | Hold-out 1951–1972: linear trend fitted on 1875–1950 (`skill_scores.py`, fixed persistence) | NSE −1.33; KGE −0.13; RMSE 0.60 m; bias −0.46 m; SS −1.00 vs persistence, −1.07 vs climatology → gate fail |
| Lake Huron | Hold-out 1951–1972: AR(1), one year ahead (rolling persistence) | NSE 0.58; KGE 0.71; RMSE 0.25 m; SS 0.10 vs persistence, 0.63 vs climatology → gate pass |
| CO2 | Quality gate | 59 of 2284 weekly values missing, flagged, nothing edited |
| CO2 | Seasonal Kendall | 1.375 ppm/yr (95% CI 1.367–1.383); by decade 0.80, 1.25, 1.59, 1.60 |

## What the run taught the skill

- A whole-period trend can be a step in disguise (Nile): register breaks
  before computing trends.
- A trend that is significant in history can be worthless as a forecast
  (Lake Huron): the naive-baseline gate catches it.
- Trend-free pre-whitening raised |Z| above the uncorrected value on a
  strongly autocorrelated series; Hamed–Rao is the default since v2.2.
- One-step persistence is an unfair baseline for multi-year forecasts;
  `--persistence fixed` exists since v2.2.
- Pettitt also fires on a smooth monotonic rise (CO2, 1980): a change point
  is a flag for an expert, not a verdict.
