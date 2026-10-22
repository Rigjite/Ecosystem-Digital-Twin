# Lake Kotokel — phosphorus scenario analysis

Code behind Table 2, the trajectories of Figure 2 and the twin-update results of:

> Балданова Р.М., Судзуки Т. Цифровые двойники экосистем как инструмент прогноза и предварительной оценки антропогенных воздействий: обзор мировой практики и сценарный анализ на примере оз. Котокель (2026).

```
cd examples/kotokel
python kotokel_phosphorus.py
```

Standard library only (Python 3.9+). Prints, for each scenario, the % change of total phosphorus (TP) at 3, 5, 10 and 50 years for the base parameters and the min–max over the 27-combination grid.

**What it is.** A two-compartment water–sediment TP balance simplified from Chapra & Canale (1991). Morphometry: area 68.9 km² and water renewal 6 yr (Shiretorova et al. 2025), mean depth 3.5 m (Semernoy et al. 2010).

**What it is not.** It is not a calibrated forecast. The initial state is measured (mean TP 80 µg/L, 86 surface samples, May 2024 – March 2025; Shiretorova et al. 2025, *Limnology and Freshwater Biology* 4: 1062–1082), but the measurements cover one year and give no TP time series. Internal phosphorus loading of Lake Kotokel has not been measured, so the settling velocity, burial and release constants are assumed and explored over a grid (vs = 5, 10, 20 m/yr; kb = 0.01, 0.03, 0.05 1/yr; kr = 0.05, 0.10, 0.20 1/yr). The model omits oxygen-dependent release, seasonality and climate change, so it shows the direction and scale of scenario effects, not recovery dates.

Scenarios: S1 +30% external load (shore development without wastewater treatment); S2 −46% external load (median TP removal by created/restored wetlands, Land et al. 2016, assuming the whole inflow passes through them); S3 one-off removal of 50% of mobile sediment P; S4 = S2 + S3.

License: CC BY 4.0, as the rest of this repository.

`value_of_information.py` — which unknown parameter drives the scenario uncertainty: first-order variance shares of kr, vs, kb over the 27-combination grid, and the share of variance explained by the internal-load share (the quantity a sediment-flux measurement determines).

`trophic_classes.py` — the same scenarios in absolute TP (µg/L) against OECD (1982) trophic classes (eutrophic 35–100, hypertrophic > 100 µg/L): how many of the 27 combinations cross 100 µg/L or reach 35 µg/L at 50 years, and the external-load cut needed to reach 35 µg/L, alone and after S3.

`twin_update.py` — the update step of the twin: each of the 27 combinations is taken in turn as the true lake, its internal-load share is "measured" with an error of ±5, ±10 or ±15 percentage points, incompatible combinations are rejected and the forecast is recomputed. Prints the median number of members kept and how much the scenario ranges narrow at 5, 10 and 50 years; also shows that TP monitoring under an unchanged load cannot tell the members apart.

`figures/` — Figures 1–3 of the paper (PNG, 300 dpi): the twin cycle with the AI-agent team, the Lake Kotokel twin cycle, and the scenario trajectories.
