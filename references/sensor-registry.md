# Sensor registry — every open source as a sensor, or honestly not one

## Contents
1. How to read this registry
2. Tier rules (four tiers, no others)
3. Part A — Registered virtual sensors (the seven, verbatim)
4. Part B — Source registry table (R01–R59)
5. Coverage summary and counts
6. What remains open

## 1. How to read this registry

A "sensor" here is anything that produces a value for an indicator row in
`references/indicators.md` (§§1–32) — a physical instrument, a satellite
retrieval, a station series, an occurrence record, or a classified map.
A source that produces no value for any indicator row is not a sensor; it
is a context layer, a standard, or literature, and it is registered as
such instead of being dressed up as a measurement.

Each row in Part B carries: the source; the physical quantity; the formula
or algorithm (published, with its citation, or an honest "no closed-form
formula"); the resolution and cadence; the ecosystems and indicator rows
it serves (§ numbers from `references/indicators.md`); the tier; what
calibration it needs; the published skill score (SS_RMSE or equivalent,
with its source — never invented); the validity window; and its limits.

The fetch mechanism for the satellite rows is `scripts/fetch_satellite.py`
(Planetary Computer STAC, no key; Copernicus Data Space needs an account),
documented in `references/data-sources.md` §11. A satellite is a periodic
snapshot, never real-time; the latency table is in `references/data-sources.md` §11.

## 2. Tier rules (four tiers, no others)

- **Core** — all three hold: a closed-form published formula, a published
  skill score with its citation, and a named calibration station or
  calibration path that exists for the object. Only one row in this
  registry meets all three (R05, Secchi depth at Beira). A published
  global accuracy alone does not make a row Core: a classifier or a
  merging algorithm has no closed-form formula, and a global score is
  not a local calibration.
- **Conditional** — a published formula or algorithm exists, but the
  local calibration is missing ([NEXT DATA]), or the score is a published
  generic validation rather than a local one. The row is usable with its
  stated caveat; it is never presented as locally calibrated.
- **Research** — a proxy is proposed, but no published formula or no
  validation exists for it in the skill. Results are research-grade
  until validated for management use.
- **Context-only** — not a sensor: a modelled map or reanalysis, a static
  layer, a boundary or authority list, an exchange standard, or
  literature. It frames the twin; it never produces an indicator value
  by itself. Modelled products (ERA5, CAMS, SoilGrids, GRACE) sit here
  by rule, however useful they are as drivers or priors.

Rules that bind every row: no invented formula, no invented score, no
invented calibration station. Where a formula, score, or station does not
exist, the cell says so — "[NEXT DATA]", "none", or "not published" —
and the row's tier reflects it. A registered virtual sensor is QC'd and
alerted exactly like a physical sensor, and when it leaves calibration
its readings go to the [НЕТ ДАННЫХ] register — never silently used
(`assets/templates.md` §1, "Virtual sensors" block).

## 3. Part A — Registered virtual sensors (the seven, verbatim)

Carried over from `references/worked-examples-new-sections.md`
("Registered virtual sensors — worked example: Beira Lake and the
Langtang slope"). Formulas, coefficients, scores, calibration stations,
and gaps are the same as there; nothing is re-derived or altered here.
Each sensor's full registration (validity window, QC and alert rules)
lives in that file; this part is the index.

### S1 — beira-chla-s2-ndci: chlorophyll-a from Sentinel-2

- Quantity: chlorophyll-a concentration, µg/L.
- Formula: Sentinel-2 MSI L2A, bands B04 (665 nm) and B05 (705 nm).
  NDCI = (R705 − R665) / (R705 + R665); Chl-a = 194.325·NDCI² +
  86.115·NDCI + 14.039 (Mishra & Mishra 2012, Remote Sens. Environ.
  117:394–406; Sentinel-2 B05/B04 are the nearest bands to the MERIS
  708/665 nm calibration).
- Calibration station: Prasad et al. 2024 in-situ chlorophyll-a at the
  Beira sampling stations — published only as interpolated maps (supplement, Figs. S7–S8), with no per-station numeric table.
- Skill score: published generic validation — RMSE 1.43 µg/L for
  Chl-a < 30 µg/L (Mishra & Mishra 2012, as reported in AlgaeMAp,
  Remote Sens. 2021, 13, 2874); Molkov et al. 2019: RMSE 3.02 µg/L.
  Beira-local SS_RMSE: [NEXT DATA] — verified 2026-10-28 (T91):
  not computable from the published record. Prasad et al. 2024 never
  applied NDCI at Beira; chlorophyll-a exists only as interpolated
  supplement maps (Figs. S7–S8), with no per-station numeric table.
  Needed: the authors' raw per-station values (station locations,
  Table S1) paired with same-day Sentinel-2 B04/B05 reflectance, or a
  new paired campaign.
- Tier in Part B: Conditional (R02). Validity: calibrated for
  Chl-a < 30 µg/L; Beira is hypertrophic, so readings above the range
  go to [НЕТ ДАННЫХ].

### S2 — beira-wst-landsat-st: water surface temperature from Landsat 8/9

- Quantity: water surface temperature, °C.
- Formula: USGS Landsat Collection 2 Level-2 surface temperature
  product, split-window algorithm (Gerace, Kleynhans, Eon & Montanaro
  2020, Remote Sens. 12, 224), TIRS bands 10/11.
- Calibration station: Prasad et al. 2024 in-situ surface water
  temperature at the 80 Beira stations, September 2022 and March 2023.
- Skill score: Eon et al. 2023 (Remote Sens. 15, 3370): Landsat 8
  RMSE 0.87 K, Landsat 9 RMSE 0.74 K against TidBit ground
  measurements over lakes. Beira-local SS_RMSE: [NEXT DATA] —
  verified 2026-10-28 (T91): not computable from the published
  record. Prasad et al. 2024 never used Landsat surface temperature
  at Beira, and in-situ temperatures exist only as interpolated
  supplement maps (Figs. S1–S2), with no per-station numeric table.
  Needed: the authors' raw per-station temperatures paired with
  Landsat 8/9 Collection 2 surface-temperature pixels for the
  sampling dates, or a new paired campaign.
- Tier in Part B: Conditional (R12). Validity: cloud-free scenes
  only; satellite measures the skin, the station measures bulk water
  at 0–10 cm — the difference is recorded, not ignored.

### S3 — beira-extent-s2-mndwi: water surface extent from Sentinel-2

- Quantity: water surface area, ha (and the water mask).
- Formula: Modified Normalised Difference Water Index (Xu 2006, Int.
  J. Remote Sens. 27:3025–3033): MNDWI = (Green − SWIR) /
  (Green + SWIR), Sentinel-2 B03 (560 nm) and B11 (1610 nm); water
  where MNDWI > 0.
- Calibration station: surveyed Beira extent, about 65.4 ha (Prasad
  et al. 2024, §2.1).
- Skill score: published validation of the reference product — JRC
  Global Surface Water (Pekel et al. 2016, Nature 540:418–422): under
  1% false water detections and under 5% of water surfaces missed.
  That validation is for the Landsat-based JRC product, not for
  Sentinel-2 MNDWI at Beira. Beira-local skill score: [NEXT DATA] —
  verified 2026-10-28 (T91): not computable from the published
  record. The surveyed extent (about 65.4 ha) is a single total, not
  a shoreline polygon or a mask, and no published MNDWI mask for
  Beira exists. Needed: a surveyed shoreline polygon for a dated
  scene, or station coordinates (Table S1) plus a same-day clear
  Sentinel-2 scene, to score the mask point by point.
- Tier in Part B: Conditional (R03). Validity: the mask is a
  classification, so its score is an accuracy, never converted into a
  pseudo-RMSE.

### S4 — beira-turbidity-s2-dogliotti: turbidity from Sentinel-2

- Quantity: turbidity, FNU (ISO 7027).
- Formula: Dogliotti et al. 2015 (Remote Sens. Environ. 156:157–168),
  Eq. (1): T = A^T · ρw(λ) / (1 − ρw(λ) / C^T); 645 nm: A^T = 228.1
  FNU, C^T = 0.1641; 859 nm: A^T = 3078.9 FNU, C^T = 0.2112. Use
  645 nm when ρw(645) < 0.05, 859 nm when ρw(645) > 0.07, linear
  blend between. Sentinel-2 nearest bands B04 (665 nm) and B8A
  (865 nm); the published coefficients are for MODIS 645/859 nm, so
  the Sentinel-2 application is an adaptation — registered with that
  caveat.
- Calibration station: none at Beira — Prasad et al. 2024 measured no
  in-situ turbidity.
- Skill score: Dogliotti et al. 2015, Table 4, all sites (n = 106):
  RMSE 20.5 FNU, r = 0.97. Beira-local SS_RMSE: [NEXT DATA] —
  verified 2026-10-28 (T91): structurally impossible from the
  published record — Prasad et al. 2024 measured no in-situ
  turbidity at Beira, so there is nothing to score against. Needed:
  a field turbidity campaign (ISO 7027 instrument) paired with
  same-day Sentinel-2 scenes.
- Tier in Part B: Conditional (R04). Validity: published to 1000 FNU;
  FNU is not interchangeable with NTU without stating the instrument.

### S5 — beira-zsd-s2-qaa: Secchi disk depth from Sentinel-2

- Quantity: Secchi disk depth (water transparency), m.
- Formula: Lee et al. 2015 (Remote Sens. Environ. 169:139–149):
  Z_SD = [1 / (2.5 · Min(Kd(λi)))] · ln(|0.14 − Rrs,m| / 0.013),
  Min(Kd) the minimum diffuse attenuation coefficient within 410–665
  nm, Kd from the quasi-analytical algorithm (QAA, Lee et al.
  2002/2009). Applied on Sentinel-2 bands 443, 490, 560 and 665 nm
  (Prasad et al. 2024).
- Calibration station: Prasad et al. 2024 in-situ Secchi disk depth
  (standard 20 cm disk) at the Beira stations.
- Skill score: Beira-local published validation — Prasad et al. 2024,
  §3.3.3: n = 43 (March 2023), R² = 0.670, RMSE 0.049 m, mean
  absolute deviation 0.042 m. The SS_RMSE for this sensor is 0.049 m.
- Tier in Part B: Core (R05) — the only Core row in the registry:
  closed-form formula, cited local score, named calibration station.
  Validity: cloud-free scenes only; Beira ZSD 0.26–0.45 m sits far
  below the Lee et al. 2015 global validation range (1–30+ m), so the
  Beira-local RMSE governs, not the global one.

### S6 — langtang-displacement-s1-insar: slope displacement from Sentinel-1

- Quantity: line-of-sight ground displacement, cm (and rate, mm/day).
- Formula: Sentinel-1 C-band differential InSAR / SBAS time series:
  line-of-sight displacement Δd = λ·Δφ / (4π), λ = 5.55 cm
  (5.405 GHz). Displacement needs an InSAR pair — two passes, days
  apart (SNAP / ASF HyP3 processing). Observation: up to 40 cm
  line-of-sight deformation over 48 days (7 July–24 August 2026) on
  the Langtang detachment slope (ICIMOD 2026); NISAR showed ~30 cm
  over 24 days as independent corroboration.
- Calibration station: none on the detachment slope — no GNSS station
  watched it; the deformation was identified retrospectively.
- Skill score: published accuracy anchors — Sentinel-1 InSAR against
  second-order levelling and GNSS: mean deviations typically within
  ±10 mm (Beijing study, Remote Sens. 2026, 18, 1274); formal
  line-of-sight noise ~1.2 mm against an actual error of 13.8 mm
  vertical and 17.2 mm east–west once systematics are included
  (Dingri 2025 error budget, Remote Sens. 2026, 18, 2252).
  Langtang-local SS_RMSE: [NEXT DATA] — verified 2026-10-28 (T91):
  no ground truth exists for that slope, and none can ever be
  collected retrospectively — the slope collapsed. Corroboration is
  cross-sensor, not ground truth: Roy et al. 2026 (J. Indian Soc.
  Remote Sens., DOI 10.1007/s12524-026-02611-x) confirms the
  precursor with NISAR L-band SBAS InSAR and pixel-offset analysis.
  Needed: a GNSS installation or drone-DEM survey on neighbouring
  at-risk slopes.
- Tier in Part B: Conditional (R09). Validity: 6–12-day revisit;
  coherence is lost over snow, vegetation and fast movement;
  line-of-sight is one component, not 3-D displacement.

### S7 — the seventh registration

There are six named sensor registrations in the worked example (S1–S6
above: five for Beira Lake, one for the Langtang slope). The "seven"
count in the task brief counts the six named sensors plus the
registration pattern itself — the Object Passport "Virtual sensors"
block (`assets/templates.md` §1) as the seventh, reusable registration
form. No seventh sensor with a formula exists in the worked example,
and none is invented here. If a seventh sensor is registered later, it
enters Part A with its formula, station, and score, and Part B gains
its row.

## 4. Part B — Source registry table (R01–R59)

One row per (source × quantity). A source appears in as many rows as
it has distinct quantities; every source in `references/data-sources.md`
appears in at least one row (see §5 for the coverage check). Tiers are
exactly Core, Conditional, Research, Context-only.

| ID | Source | Quantity | Formula / algorithm | Resolution / cadence | Serves — ecosystems and indicator rows (§) | Tier | Calibration | Skill score | Validity window | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| R01 | Sentinel-2 (Copernicus) | NDVI / EVI vegetation state, unitless index | NDVI = (NIR − red) / (NIR + red); EVI = 2.5 × (NIR − red) / (NIR + 6 × red − 7.5 × blue + 1) (Huete et al. 2002); S2 bands B04/B08 (B02 for EVI blue) | 10–20 m, ~5 days | §11 flora, §16 ecosystem functions (primary production), §22 steppe, §28 desert, §29 tundra, §30 forest, §31 cropland, §10 landscape — vegetation cover and condition rows | Conditional | Ground LAI / fCover plots where they exist; none named for a generic object | No single published RMSE for the index itself — [NEXT DATA] for any downstream retrieval | Cloud-free scenes only; index, not a retrieval — accuracy is that of the downstream quantity | The field-twin NDVI stream (`references/data-sources.md` §10); phenology differs by season — compare same-season scenes |
| R02 | Sentinel-2 (Copernicus) | Chlorophyll-a, µg/L | NDCI = (R705 − R665) / (R705 + R665); Chl-a = 194.325·NDCI² + 86.115·NDCI + 14.039 (Mishra & Mishra 2012); S2 B05/B04 — see S1 | 10–20 m, ~5 days | §12 microalgae and phytoplankton — chlorophyll-a rows | Conditional | Prasad et al. 2024 in-situ chlorophyll-a at Beira stations (supplement Figs. S7–S8, interpolated maps only) | RMSE 1.43 µg/L for Chl-a < 30 µg/L (Mishra & Mishra 2012, via AlgaeMAp 2021); RMSE 3.02 µg/L (Molkov et al. 2019); Beira-local SS_RMSE [NEXT DATA] — verified 2026-10-28 (T91): not computable; chlorophyll-a exists only as supplement maps (Figs. S7–S8), no per-station table; NDCI never applied at Beira in the paper | Calibrated for Chl-a < 30 µg/L; Beira is hypertrophic — readings above range go to [НЕТ ДАННЫХ]; cloud-free only | MERIS 708/665 nm coefficients adapted to S2 B05/B04 (published practice, Molkov et al. 2019) |
| R03 | Sentinel-2 (Copernicus) | Water surface area, ha, and water mask | MNDWI = (Green − SWIR) / (Green + SWIR) (Xu 2006); S2 B03/B11; water where MNDWI > 0 — see S3 | 10–20 m, ~5 days | §3 hydrology, §4 surface-water quality, §24 peatlands, §32 wetlands — water extent and hydroperiod rows | Conditional | Surveyed extent, about 65.4 ha at Beira (Prasad et al. 2024, §2.1) | Under 1% false water, under 5% missed (Pekel et al. 2016, for the Landsat-based JRC product, not S2 MNDWI at Beira); Beira-local score [NEXT DATA] — verified 2026-10-28 (T91): not computable; surveyed extent is one total (65.4 ha), not a mask | Classification, not a measurement — score is an accuracy, never a pseudo-RMSE; cloud-free only | Chosen over McFeeters NDWI because it suppresses built-up noise (Beira sits in central Colombo) |
| R04 | Sentinel-2 (Copernicus) | Turbidity, FNU | Dogliotti et al. 2015, Eq. (1): T = A^T · ρw / (1 − ρw / C^T); 645 nm: A^T = 228.1 FNU, C^T = 0.1641; 859 nm: A^T = 3078.9 FNU, C^T = 0.2112; band-switching rule — see S4 | 10–20 m, ~5 days | §4 surface-water quality — turbidity and transparency rows | Conditional | None at Beira — Prasad et al. 2024 measured no in-situ turbidity | RMSE 20.5 FNU (Dogliotti et al. 2015, Table 4, n = 106, r = 0.97); Beira-local SS_RMSE [NEXT DATA] — verified 2026-10-28 (T91): structurally impossible; no in-situ turbidity was measured at Beira | Published to 1000 FNU; FNU is not interchangeable with NTU without stating the instrument | MODIS 645/859 nm coefficients adapted to S2 B04/B8A (ACOLITE implements the algorithm for S2) — registered with that caveat |
| R05 | Sentinel-2 (Copernicus) | Secchi disk depth, m | Lee et al. 2015: Z_SD = [1 / (2.5 · Min(Kd))] · ln(abs(0.14 − Rrs,m) / 0.013), Kd from QAA; S2 bands 443/490/560/665 nm — see S5 | 10–20 m, ~5 days | §4 surface-water quality — transparency rows | Core | Prasad et al. 2024 in-situ Secchi depth (20 cm disk) at Beira stations | RMSE 0.049 m (Prasad et al. 2024, §3.3.3, n = 43, R² = 0.670) — Beira-local published score | Cloud-free only; Beira ZSD 0.26–0.45 m, below the Lee et al. global range (1–30+ m) — the local RMSE governs | The only Core row in the registry and the only Beira-local published skill score in the set |
| R06 | Sentinel-2 (Copernicus) | Burn severity, NBR / dNBR | NBR = (NIR − SWIR) / (NIR + SWIR) (Key & Benson 2006); dNBR = pre-fire NBR − post-fire NBR; S2 B08/B12 | 10–20 m, ~5 days | §30 forest, §22 steppe, §29 tundra, §28 desert — fire extent and post-fire recovery rows | Conditional | Field burn-severity plots where they exist; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Needs a pre-fire and a post-fire scene; a single scene proves nothing | NBR alone does not distinguish fire from logging — shape, roads, and the Hansen/FIRMS cross-checks decide (Zone A comparison, 2026-10-28) |
| R07 | Sentinel-2 (Copernicus) | Snow / ice cover, NDSI | NDSI = (Green − SWIR) / (Green + SWIR) (Hall et al. 1995); S2 B03/B11 | 10–20 m, ~5 days | §21 cryosphere, §29 tundra — snow cover and glacier-area rows | Conditional | Snow-course / stake measurements where they exist; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Cloud-free only; snow under forest canopy is missed | NDSI is a snow-presence index, not a snow-water-equivalent measurement |
| R08 | Sentinel-5P (TROPOMI) | NO2, SO2, O3, aerosol, methane columns | DOAS spectral retrieval (van Geffen et al. 2020 for NO2); no closed-form formula — a retrieval algorithm, not an equation | ~3.5–7 km, daily | §2 air quality — NO2, SO2, O3 rows; §1 climate — methane column | Conditional | Ground air-quality stations (OpenAQ, R27) where they exist | No single published RMSE in the skill — [NEXT DATA] | Column, not surface concentration — do not compare directly with ground-level limits | Tropospheric column vs surface: the conversion needs a profile model |
| R09 | Sentinel-1 (Copernicus) | Line-of-sight ground displacement, cm (and rate, mm/day) | Δd = λ·Δφ / (4π), λ = 5.55 cm (5.405 GHz); D-InSAR / SBAS pair — see S6 | IW 5 × 20 m, 6–12 days | §21 cryosphere — slope displacement, displacement rate and acceleration rows | Conditional | None on the Langtang slope — no GNSS station watched it | Mean deviations within ±10 mm vs levelling/GNSS (Beijing study, Remote Sens. 2026, 18, 1274); formal LOS noise ~1.2 mm vs actual 13.8 mm vertical / 17.2 mm east–west (Dingri 2025); Langtang-local SS_RMSE [NEXT DATA] — verified 2026-10-28 (T91): no ground truth exists and none can ever be collected retrospectively (slope collapsed); cross-sensor agreement only | Coherence lost over snow, vegetation, fast movement; line-of-sight is one component, not 3-D | The 40 cm Langtang signal (48 days) is ~20–30× the error budget; alert on a sustained rate increase, never one acquisition |
| R10 | Sentinel-1 (Copernicus) | Flood extent / open-water map | Backscatter threshold (e.g. Otsu) on VV/VH; method-dependent — no single published formula in the skill | IW 5 × 20 m, 6–12 days | §3 hydrology, §21 cryosphere, §32 wetlands — flood extent and river-damming rows | Research | Gauge level / surveyed flood edge where they exist; none named for a generic object | No published skill score in the skill — [NEXT DATA] | Radar sees water through cloud, but smooth bare soil and tarmac also read dark — false water is common | Research until a threshold method and its validation are registered for the object |
| R11 | Sentinel-1 (Copernicus) | Soil moisture proxy (relative) | Change-detection / TU Wien algorithm on backscatter time series; no closed-form formula in the skill | IW 5 × 20 m, 6–12 days | §9 soil, §31 cropland, §22 steppe — soil-moisture rows | Research | In-situ soil-moisture probes where they exist; none named for a generic object | No published skill score in the skill — [NEXT DATA] | Relative change, not volumetric water content — do not report m³/m³ from this row | SMAP (R21) is the calibrated soil-moisture product; this row is its high-resolution, uncalibrated companion |
| R12 | Landsat 8/9 (USGS) | Water surface temperature, °C | USGS Collection 2 Level-2 surface temperature, split-window algorithm (Gerace et al. 2020), TIRS bands 10/11 — see S2 | 30 m, 16 days (8 with both satellites) | §4 surface-water quality, §25 marine and coastal — water-temperature rows | Conditional | Prasad et al. 2024 in-situ temperature at the 80 Beira stations | RMSE 0.87 K (L8) / 0.74 K (L9) (Eon et al. 2023, vs TidBit lake measurements); Beira-local SS_RMSE [NEXT DATA] — verified 2026-10-28 (T91): not computable; Landsat ST never used at Beira in the paper and in-situ temperatures exist only as supplement maps (Figs. S1–S2) | Cloud-free only; satellite measures skin, station measures bulk at 0–10 cm | Long archive back to 1984 (earlier Landsats) — the baseline source |
| R13 | Landsat 8/9 (USGS) | NDVI / land-cover history | NDVI = (NIR − red) / (NIR + red); Landsat red SR_B4 / NIR SR_B5 | 30 m, 16 days | §10 landscape, §30 forest, §31 cropland — land-use history and extent rows | Conditional | Historical maps / aerial photos where they exist; none named for a generic object | No single published RMSE for the index itself — [NEXT DATA] | 30 m, 16-day revisit — slow refresh; the archive, not the alert layer | `scripts/fetch_satellite.py` uses Landsat C2 L2 as the second catalogue after Sentinel-2 |
| R14 | MODIS / VIIRS (NASA) | Active-fire thermal anomalies (detections) | Contextual thermal-anomaly algorithm (Giglio et al. 2003, 2016, Collection 6); detection, not a closed-form retrieval | VIIRS 375 m / MODIS 1 km, daily | §30 forest, §22 steppe, §24 peatlands — fire occurrence rows | Conditional | Ground fire reports where they exist; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | A detection is a hot pixel, not a confirmed fire perimeter; small fires may be missed | Same algorithm family as FIRMS (R17); this row is the raw product, R17 is the near-real-time feed |
| R15 | MODIS / VIIRS (NASA) | Land surface temperature, surface reflectance, phenology (coarse) | Published MODIS/VIIRS product algorithms; no single closed-form formula in the skill | 250 m–1 km, daily | §1 climate, §11 flora, §29 tundra — phenology and thermal rows | Conditional | Station / fine-resolution satellite cross-check where it exists; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Coarse context only (250 m–1 km), never a local measurement | Daily cadence is the value here; the spatial price is paid in the tier |
| R16 | Copernicus DEM / SRTM | Elevation, slope, catchment boundaries | None — a static elevation layer, not a measurement series | 30–90 m, static | §3 hydrology, §9 soil, §10 landscape — catchment and erosion-risk rows | Context-only | Not applicable — a static layer | Not applicable — a static layer | Near-global 60°N–56°S (SRTM); Copernicus DEM licence varies by product version — verify at build time | Elevation frames the twin; it never produces an indicator value by itself |
| R17 | NASA FIRMS | Active-fire detections, points with time and fire radiative power | Thermal-anomaly detections, contextual algorithm (Giglio et al. 2016, Collection 6); VIIRS 375 m, MODIS 1 km | 375 m (VIIRS) / 1 km (MODIS), near-real-time, < 3 h from overpass | §30 forest, §22 steppe, §24 peatlands, §28 desert — fire occurrence and peat-fire rows | Conditional | Ground fire reports where they exist; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Detections are not ground-confirmed fires; absence of detections is not absence of fire; small or short-lived fires may fall below the threshold | Free, free MAP_KEY via firms.modaps.eosdis.nasa.gov/api/area/; the near-real-time fire layer the twin was missing in the Zone A comparison (Hansen/FIRMS were unreachable there without a key) |
| R18 | Global Forest Watch / Hansen | Tree-cover loss year (lossyear) and 2000 tree cover | Landsat time-series change detection (Hansen et al. 2013, Science 342:850–853); trees defined as vegetation above 5 m; loss is removal or mortality of tree cover in a 30 m pixel | 30 m, annual, 2001–present | §30 forest — forest loss by driver rows; §10 landscape — disturbance rows | Conditional | Stratified random-sample validation against Landsat, MODIS and high-resolution imagery (Hansen et al. 2013) | User's accuracy 87.0% globally for loss; overall accuracy over 99% (skewed by no-change pixels); loss year matched for 75.2% of events, within 1 year for 96.7% (GFW validation of Hansen et al. 2013) | Loss is not deforestation — fire, harvest, disease and storm all count; gain layer ends 2012 in the original product; GLAD weekly and RADD alerts are separate products | Free, CC BY 4.0, download and API; the independent layer that attributes a Zone A patch to a year — the check that failed in this environment (tiles answer 405/403 without a key) |
| R19 | ESA WorldCover | Land-cover class (11 classes: tree cover, shrubland, grassland, cropland, built-up, bare/sparse, snow/ice, water, herbaceous wetland, mangrove, moss/lichen) | Supervised machine-learning classification of Sentinel-1 + Sentinel-2 (ESA WorldCover Product User Manual v1.0); no closed-form formula | 10 m, annual (2020, 2021, …) | §10 landscape, §30 forest, §31 cropland, §26 urban, §32 wetlands, §25 marine — habitat extent, fragmentation and conversion rows | Conditional | Independent reference data (LUCAS validation) | Overall accuracy 74.4% (WorldCover 2020, ESA Product User Manual v1.0); 2021 product target 77% | Class accuracy varies — tree, water and bare/sparse above 80%; shrubland, wetland and moss/lichen lower; grassland overestimated, trees underestimated | Free, annual, 10 m — the finest free global land-cover map in the registry; a map, not a measurement series |
| R20 | GPM IMERG (NASA/JAXA) | Precipitation rate, mm/h (accumulated to mm/day) | Multi-satellite merging, GPM Core Observatory as calibrator (Huffman et al., NASA GPM IMERG Algorithm Theoretical Basis Document); no closed-form formula | 0.1° (~10 km), half-hourly, from 2000; Early Run 4-h latency, Late Run 14-h, Final Run ~3.5 months | §1 climate — precipitation rows; §3 hydrology — flood forcing; §31 cropland — water input rows | Conditional | Rain gauges where they exist; none named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Lower skill over frozen surfaces, complex terrain, and coastal zones; constellation changes can introduce artefacts in multi-year series | Free via NASA Earthdata (free account); the rain input where no gauge exists — a retrieval, not a gauge |
| R21 | SMAP (NASA) | Surface (0–5 cm) and root-zone (0–100 cm) soil moisture, m³/m³ | L-band brightness-temperature assimilation into the NASA Catchment land-surface model, L4_SM product (Reichle et al. 2017, J. Hydrometeorol. 18:2621–2645, DOI 10.1175/JHM-D-17-0063.1) | 9 km, 3-hourly, from 31 March 2015 (within 3 days of real time) | §9 soil, §31 cropland, §22 steppe, §28 desert — soil-moisture rows | Conditional | Core validation sites: 43 surface / 17 root-zone reference pixels in 17 / 7 watersheds; 406 / 311 sparse-network points | ubRMSE 0.038 m³/m³ surface and 0.030 m³/m³ root-zone at 9 km (Reichle et al. 2017); requirement 0.04 m³/m³ or better | 9 km — a basin/field-context value, never a plot measurement; assimilated, not directly sensed | The calibrated soil-moisture product in the registry; Sentinel-1 soil moisture (R11) is its uncalibrated high-resolution companion |
| R22 | Copernicus Marine Service (OSTIA) | Foundation sea surface temperature, °C, and sea-ice fraction | Multi-sensor optimal interpolation of satellite + in-situ SST (Worsfold et al. 2024, Remote Sens. 16, 3358); product SST_GLO_SST_L4_REP_OBSERVATIONS_010_011 | 0.05° (~5 km), daily, 1981–present | §25 marine and coastal — SST and marine-heatwave rows; §27 aquaculture — temperature vs species-optimum rows | Conditional | In-situ SST (ships, buoys) assimilated in the product; no single local station named for a generic object | No single published RMSE in the skill — [NEXT DATA] | Foundation SST — free of diurnal variability, not the skin temperature a farm sensor reads; some large lakes are covered, not all | Free on registration; near-real-time product SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001 is the alert feed, the reprocessed product is the baseline |
| R23 | OpenStreetMap | Roads, settlements, buildings, waterways, land-use polygons | None — a community-maintained map, not a measurement | Vector, updated continuously by contributors | §10 landscape, §26 urban, §30 forest — fragmentation, access and attractant rows (as a layer) | Context-only | Not applicable — a map | Not applicable — a map | Completeness varies by country and by feature; no single accuracy figure | ODbL licence; the roads layer that decides whether a Zone A patch is logging (roads and skid trails) or fire (no roads inside) |
| R24 | WDPA / Protected Planet (UNEP-WCMC / IUCN) | Protected-area boundaries, designation, IUCN category, status year | None — an authority database, not a measurement | Vector, new version monthly | §15 fish and wildlife, §11 flora, §17 pressures — protected-area and certified-share rows (as a layer) | Context-only | Not applicable — an authority database | Not applicable — an authority database | Free for non-commercial use; commercial use via IBAT; some providers requested their data not be shared beyond WDPA managers — as of June 2019: China, the Russian Federation, Estonia, Saint Helena / Ascension / Tristan da Cunha (WDPA User Manual) — check coverage for Russian objects at build time | A boundary frames the object; it never measures the object's state |
| R25 | ERA5 reanalysis (ECMWF) | Temperature, precipitation, wind, radiation, soil-moisture estimates | Model + data assimilation (ECMWF IFS); a reanalysis, not a sensor | Hourly, ~31 km, 1940–present | §1 climate — all driver rows where no station exists | Context-only | Stations, where they exist — station truth over reanalysis | Not applicable as a sensor score — a model product | ~31 km, hourly — a driver, never a local measurement | The default meteo driver when no local station exists (`references/data-sources.md` §10, daily weather stream) |
| R26 | National meteo services (e.g. NOAA, national hydromet) | Station air temperature, precipitation, wind, radiation | None — direct measurement by calibrated instruments | Station-dependent, minutes–hourly | §1 climate — all driver rows | Conditional | The station network itself; calibration and maintenance per service | No single published RMSE in the skill — per-station instrument accuracy, [NEXT DATA] | Coverage is country-specific; a station kilometres away is not the object's weather | Station truth over reanalysis, wherever a station exists |
| R27 | OpenAQ | Ground PM2.5/PM10, NO2, O3 and other pollutant measurements | None — aggregation of station measurements | Station-dependent, hourly where stations report | §2 air quality — PM, NO2, O3 rows; §26 urban — air rows | Conditional | The reporting stations themselves | No single published RMSE in the skill — per-station, [NEXT DATA] | Station coverage varies widely; check per city | An aggregator, not a measurer — the measurement belongs to the station |
| R28 | CAMS (Copernicus Atmosphere Monitoring Service) | PM, NO2, SO2, O3, pollen analyses and forecasts | Model + data assimilation; no closed-form formula | ~11 km (global), hourly–daily | §2 air quality — PM, NO2, SO2, O3 rows | Context-only | Ground stations, before threshold use | Not applicable as a sensor score — a model product | Forecast skill falls with horizon; validate against ground stations before threshold use | The forecast layer for air; the measurement layer is R27 |
| R29 | Open-Meteo (open-meteo.com) | Forecast temperature, precipitation, wind, radiation, humidity, ET₀ | Model output from national weather services (DWD ICON, NOAA GFS, ECMWF IFS, Météo-France, JMA and others); no closed-form formula | Hourly, 1–11 km by model; forecast to 16 days; archive (ERA5) back to 1940 | §1 climate — forecast-weather rows; §31 cropland — irrigation and spray windows | Context-only | National stations, before threshold use | Not applicable as a sensor score — a model product | Free for non-commercial use, no API key (a key is required only for commercial use); model output, not station truth | The forecast-weather stream (`references/data-sources.md` §10); never a substitute for observations in calibration |
| R30 | National hydrology gauges (e.g. USGS NWIS, state services) | Discharge, water level, temperature, some chemistry | None — direct measurement by gauged instruments | Station-dependent, minutes–hourly | §3 hydrology — discharge, level and temperature rows | Conditional | The gauge network itself; rating curves per station | No single published RMSE in the skill — per-gauge, [NEXT DATA] | A gauge measures its cross-section, not the whole reach | The calibration backbone for river twins |
| R31 | GRDC (Global Runoff Data Centre) | Archived discharge series for large rivers | None — archived station series | Monthly / daily archives, historical | §3 hydrology — historical calibration rows | Conditional | The contributing national services | No single published RMSE in the skill — per-series, [NEXT DATA] | Recent years may lag; historical context, not a live feed | Cross-border context where the live gauge is on the other side of a border |
| R32 | GEMStat (UNEP GEMS/Water) and national water-quality portals (e.g. US Water Quality Portal) | Water chemistry and nutrient observations from monitoring programmes | None — laboratory analysis by programme methods | Programme-dependent | §4 surface-water quality, §5 nutrients — chemistry rows | Conditional | Accredited laboratories per programme | No single published RMSE in the skill — per-programme, [NEXT DATA] | Methods and detection limits vary by programme — carry them in the provenance log | The only open route to measured chemistry without a field campaign |
| R33 | JRC Global Surface Water (Copernicus) | Water occurrence, seasonality, transitions since 1984 | Landsat-based expert-system classification (Pekel et al. 2016, Nature 540:418–422); no closed-form formula | 30 m, monthly / annual, 1984–present | §3 hydrology, §16 ecosystem functions (water regulation), §32 wetlands — inundation and hydroperiod rows | Conditional | 40,000+ control points over 32 years (Pekel et al. 2016) | Under 1% false water detections, under 5% of water surfaces missed; permanent-water accuracy 99.5–99.7% (Pekel et al. 2016) | Landsat-based, 30 m — a slow baseline, not an alert feed | The reference product behind the MNDWI score in R03; its validation is for the JRC product, not for Sentinel-2 MNDWI |
| R34 | GRACE / GRACE-FO terrestrial water storage | Basin-scale total water-storage anomalies | Satellite gravimetry, basin-scale inversion; no closed-form formula in the skill | ~300 km, monthly | §8 groundwater — storage-context rows | Context-only | Not applicable as a local sensor — a basin context layer | Not applicable as a local score | Coarse resolution — a groundwater/storage context layer, never a local measurement | Useful for the basin, useless for the field |
| R35 | GLOSS / national sea-level and lake services | Lake and reservoir levels; sea level | None — gauge measurement | Station-dependent | §3 hydrology, §25 marine — level and sea-level-trend rows | Conditional | The gauge network itself | No single published RMSE in the skill — per-gauge, [NEXT DATA] | Coverage is country-specific | The level backbone where a satellite altimeter is too coarse |
| R36 | Agency and institute archives; historical yearbooks and station logs | Long pre-digital monitoring series, event records, method history | None — historical observations | Historical, often decades longer than the digital record | §1 climate, §3 hydrology, §4 water quality — baseline and break rows | Conditional | The originating agency's methods, per period | No single published RMSE — per-period, [NEXT DATA] | Method changes break series — harmonize and log every break in a bias-and-breaks register | Often the only record of the pre-satellite baseline |
| R37 | Client and field sampling | Full chemistry and biology (DO, nutrients, metals, phytoplankton taxonomy, microbiology, sediments) | None — laboratory analysis, accredited where required | Campaign-dependent | §4, §5, §6, §12, §13, §7 — most chemistry and biology rows | Conditional | Accredited laboratory; sampling design before the campaign | No single published RMSE — per-method, [NEXT DATA] | The only source for most biological indicators; design the sampling before promising the twin | Sanitary microbiology, phytoplankton taxonomy, sediment and tissue chemistry normally require accredited laboratory analysis |
| R38 | GBIF | Species occurrence records, global | None — occurrence records, not a measurement series | Record-dependent | §11 flora, §14 invertebrates, §15 fish and wildlife — occurrence rows | Conditional | The contributing datasets; filter to research-grade, dated, georeferenced records | No single published RMSE — occurrence data carry sampling bias, not a score | Observer bias toward roads and settlements — state it; generalize sensitive records before sharing (`scripts/generalize_coords.py`) | Occurrence is presence, not abundance — a record does not prove a population |
| R39 | iNaturalist (research grade export via GBIF) | Occurrence with photos | None — observer records | Record-dependent | §11 flora, §14 invertebrates, §15 fish and wildlife — occurrence rows | Conditional | Research-grade export via GBIF | No single published RMSE — observer data, [NEXT DATA] | Observer bias toward roads and settlements — state it | Photos help identification; they do not remove the bias |
| R40 | eBird / national monitoring schemes | Bird abundance and trends | None — protocol-based counts | Protocol-dependent, seasonal | §15 fish and wildlife — bird rows; §22 steppe, §29 tundra — steppe and tundra bird rows | Conditional | The scheme protocol itself | No single published RMSE in the skill — per-scheme, [NEXT DATA] | Protocol-based — strong for trends, weak for absolute abundance without effort correction | The strongest open bird-trend source in the registry |
| R41 | National red lists and protected-area registries | Conservation status, legal boundaries | None — authority lists | Updated per country, irregular | §15 fish and wildlife, §11 flora — status rows (as a layer) | Context-only | Not applicable — an authority | Not applicable — an authority | Mostly human-maintained country registries and PDFs, not machine-readable APIs — budget manual extraction time | The authority for status; GBIF is not |
| R42 | Movebank | Animal movement and telemetry tracks | None — GPS / telemetry tracks | Track-dependent | §15 fish and wildlife — movement and migration rows | Conditional | The study's own tags and calibration | No single published RMSE in the skill — per-study, [NEXT DATA] | Access is per-study and often restricted; sensitive-species safeguards apply in full | Tracks show where animals go; they do not show how many there are |
| R43 | Museum, herbarium and historical survey records | Pre-digital species occurrences and re-locatable sampling points | None — historical records | Historical | §11 flora, §14 invertebrates, §15 fish and wildlife — baseline occurrence rows | Conditional | The originating collection's methods | No single published RMSE — per-collection, [NEXT DATA] | Taxonomy and effort differ from modern surveys — harmonize before trend use; provenance per record | The baseline before the baseline — often the only record of what was there |
| R44 | SoilGrids (ISRIC) | Soil organic carbon, texture, pH (modelled maps) | Machine-learning model on soil profiles and covariates; no closed-form formula | 250 m, static maps | §9 soil, §22 steppe, §29 tundra, §31 cropland — SOC and texture rows (as a prior) | Context-only | Measured soil points, where they exist | Not applicable as a sensor score — a modelled map | 250 m modelled maps — a prior, not a measurement | A prior frames the sampling plan; it never replaces a soil pit |
| R45 | ESDAC / LUCAS Soil (EU) | Measured topsoil properties and soil survey points | None — laboratory analysis of surveyed points | Point surveys, periodic | §9 soil, §31 cropland — measured soil rows | Conditional | The survey's own laboratory methods | No single published RMSE in the skill — per-survey, [NEXT DATA] | Europe only; strong validation layer where the object is in the EU | The measured counterweight to SoilGrids (R44) inside the EU |
| R46 | National soil and cadastre maps | Field boundaries, soil classes | None — static maps | Static, country-specific | §9 soil, §31 cropland — field and soil-class rows (as a layer) | Context-only | Not applicable — a static map | Not applicable — a static map | Country-specific access | A boundary frames the field; it never measures the soil |
| R47 | CORINE / national land-cover products | Land-cover classes and change | Photo-interpreted classification; no closed-form formula | 100 m, 6-yearly (CORINE) | §10 landscape, §30 forest, §31 cropland — habitat extent and fragmentation rows | Context-only | Photo interpretation | No single published RMSE in the skill — [NEXT DATA] | 100 m and 6-yearly — too coarse and too slow for a single field | The European baseline; WorldCover (R19) is the finer global companion |
| R48 | OGC SensorThings API | Sensor, observation and exchange format | None — an interoperability standard | Not applicable | All sections — live and archived sensor feeds in and out of the twin | Context-only | Not applicable — a standard | Not applicable — a standard | A twin that invents a private format where a standard exists creates conversion debt | A standard is infrastructure, not a source |
| R49 | WaterML 2.0 | Hydrological time-series exchange format | None — an interoperability standard | Not applicable | §3 hydrology — discharge, level and water-quality series exchange | Context-only | Not applicable — a standard | Not applicable — a standard | Format only — the values still come from R30–R32 | A standard is infrastructure, not a source |
| R50 | Darwin Core | Species-occurrence exchange format | None — an interoperability standard | Not applicable | §11, §14, §15 — biodiversity records shared with GBIF-compatible systems | Context-only | Not applicable — a standard | Not applicable — a standard | Format only — the records still come from R38–R40 | A standard is infrastructure, not a source |
| R51 | EML (Ecological Metadata Language) | Ecological dataset and forecast metadata | None — a metadata standard | Not applicable | All sections — dataset description; forecast metadata | Context-only | Not applicable — a standard | Not applicable — a standard | Metadata only — it describes data, it is not data | A standard is infrastructure, not a source |
| R52 | STAC | Earth-observation asset discovery format | None — a discovery standard | Not applicable | All satellite rows (R01–R15, R17–R22) — finding and citing imagery collections reproducibly | Context-only | Not applicable — a standard | Not applicable — a standard | STAC finds the scene; the sensor is the instrument that took it | The catalogue format `scripts/fetch_satellite.py` speaks |
| R53 | CF conventions (netCDF) | Gridded model and reanalysis data format | None — a data convention | Not applicable | §1 climate, §25 marine — model outputs and climate/reanalysis exchange | Context-only | Not applicable — a convention | Not applicable — a convention | Format only — the values still come from R25, R28, R29 | A convention is infrastructure, not a source |
| R54 | RO-Crate | Deliverable packaging format | None — a packaging standard | Not applicable | Phase 6 — the provenance package itself | Context-only | Not applicable — a standard | Not applicable — a standard | Packaging only — it carries the twin, it is not the twin's data | The package format the registry itself is shipped in |
| R55 | Evidence platforms (PubMed / PMC, Europe PMC, OpenAlex, Crossref, Semantic Scholar, AGRIS, CyberLeninka, eLibrary) | Published evidence — prior studies, methods, thresholds, benchmark results | None — literature, not measurements | Publication-dependent | All sections — thresholds and method justification (see `references/evidence-sources.md`) | Context-only | Not applicable — literature | Not applicable — literature | Literature justifies the twin's choices; it is never a source of measurements for the object itself | The one row that justifies every other row's formula and score |
| R56 | In-situ sensors (water sondes, weather stations, soil probes) | Direct physical measurements (temperature, DO, conductivity, soil moisture, weather) | None — direct measurement by calibrated instruments | Minutes–hourly | §1 climate, §3 hydrology, §4 water quality, §9 soil — measured rows | Conditional | Recorded model, calibration dates and drift checks in the provenance log | No single published RMSE — per-instrument, [NEXT DATA] | Uncalibrated sensor series are flagged, not silently trusted | The only real-time layer in the registry — ground telemetry carries the alerts while the satellite carries the trend |
| R57 | Farm records | Inputs, yields, operations diary | None — farmer-reported records | Season-dependent | §23 livestock, §31 cropland — driver-history rows | Conditional | The farm's own books; cross-checked against deliveries where possible | No single published RMSE — per-farm, [NEXT DATA] | Self-reported — the driver history for agro twins, not an independent measurement | Without the diary, the twin cannot tell a management effect from a weather effect |
| R58 | Prior studies and EIA reports | Baselines from earlier work on or near the object | None — earlier studies | Study-dependent | All sections — baseline rows | Context-only | The originating study's methods | Not applicable as a sensor score — per-study | Mine them for baselines; verify methods before reusing numbers | A baseline with an unverified method is a gap with a citation, not a value |
| R59 | Satellite mast proxy (proposed) | Cedar / pine cone-yield index (proxy) | EVI / phenology anomaly as a mast proxy (Fernández-Martínez et al. 2015, Plant Ecology — demonstrated for holm oak Quercus ilex, not for Pinus sibirica) | 10–20 m, ~5 days (Sentinel-2) | §30 forest — mast yield index row (Research, [NEXT DATA]); §15 fish and wildlife — bear-food rows | Research | Ground cone counts on sample plots over several years — does not exist for Buryatia 2026 | No published skill score for Pinus sibirica — [NEXT DATA] | A satellite cannot count pine cones (small, under canopy); it sees canopy, phenology and stress — proxies, not a direct count | From the Barguzinsky bear analysis (2026-10-27): a retrospective 2026 estimate without ground data is provisional only, never a harvest figure; berry shrubs in the understory are almost invisible to 10 m optical satellites |

## 5. Coverage summary and counts

- Registry rows: **59** (R01–R59). Tiers: **Core 1** (R05), **Conditional 35**
  (R01–R04, R06–R09, R12–R15, R17–R22, R26, R27, R30–R33, R35–R40, R42,
  R43, R45, R56, R57), **Research 3** (R10, R11, R59), **Context-only 20**
  (R16, R23–R25, R28, R29, R34, R41, R44, R46–R55, R58).
- Sources covered: every source in `references/data-sources.md` — the 29
  original data sources (6 satellite, 5 atmosphere, 8 water, 6
  biodiversity, 4 soil/land), the 7 interoperability standards, the
  evidence platforms (1 combined row, R55), the 3 client/sensor items
  (in-situ sensors R56, farm records R57, prior studies R58; satellite
  proxies are Part A, S1–S6), and the 8 new sources added 2026-10-28
  (FIRMS R17, Global Forest Watch / Hansen R18, ESA WorldCover R19, GPM
  IMERG R20, SMAP R21, Copernicus Marine Service R22, OpenStreetMap R23,
  WDPA R24) — **48 canonical source names in all**, each appearing in at
  least one registry row.
- Ecosystems served: all 29 indicator-bearing sections (§§1–17 and
  §§21–32) have at least one registry row. §§18–20 are meta sections
  (domain quick sets, indicator metadata, watch-level rules) and are
  served by the catalogue itself, not by sensors — no registry row
  cites them, by design. The thinnest coverage is the deep and
  subterranean systems the catalogue itself does not yet cover as
  domain sections — no registry row can serve a section that does not
  exist.
- The honest headline: only **1 of 59 rows is Core**. The registry is
  mostly Conditional — published methods waiting for a local
  calibration. That is the point of the registry: it shows, per row,
  what is measured and what is still only a method.

## 6. What remains open

- Beira-local SS_RMSE for the chlorophyll-a (R02), water-temperature
  (R12), water-extent (R03) and turbidity (R04) sensors — verified
  2026-10-28 (T91) as negative results, each with its own reason, not
  one shared gap: chlorophyll-a and temperature exist in the published
  record only as interpolated supplement maps (Figs. S7–S8 and S1–S2),
  with no per-station numeric table, and the paper never applied NDCI
  or Landsat surface temperature at Beira; the water extent is a single
  surveyed total (about 65.4 ha), not a mask; turbidity was never
  measured in situ at Beira, so a local score is structurally
  impossible. What each needs is stated at its sensor (S1–S4).
- A Beira-local chlorophyll-a calibration — the NDCI quadratic is
  calibrated below 30 µg/L; Beira is hypertrophic, so a local curve
  from the Prasad stations is needed before the sensor can report
  values instead of a range-limited flag.
- Langtang-local ground truth for the InSAR displacement (R09) — no
  GNSS station on the slope, and the pre-collapse deformation can never
  be scored retrospectively because the slope collapsed (verified
  2026-10-28, T91); the next source is a GNSS installation or
  drone-DEM survey on neighbouring at-risk slopes. Cross-sensor
  agreement (NISAR, Roy et al. 2026) is not ground truth.
- A published skill score for FIRMS (R17), GPM IMERG (R20), Copernicus
  Marine OSTIA SST (R22), MODIS/VIIRS active fire (R14) and NBR (R06)
  — each is [NEXT DATA] in this registry, not a missing row.
- Validation of the two Research satellite rows (R10 flood extent,
  R11 SAR soil moisture) and the mast proxy (R59) against ground data
  for a named object, before either is used for a management decision.
- A seventh named sensor registration (Part A, S7) — none exists yet;
  the next candidate is the FIRMS fire-detection registration for a
  named forest object, once a ground fire report exists to score it
  against.
