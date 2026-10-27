# Data sources — open first

For every source: record in the twin's provenance log the dataset name, version
or collection, spatial and temporal coverage actually used, retrieval date,
and the service's stable identifier or URL as of the build date.
Verify current access terms and coverage at build time; services change.

## Contents
1. Satellite and Earth observation
2. Atmosphere and climate
3. Water
4. Biodiversity
5. Soil and land
6. Interoperability standards
7. Evidence sources (literature platforms)
8. Client and sensor data (added after the open layer)
9. Multi-source fusion
10. Field-twin open-data streams

## Satellite and Earth observation

| Source | Gives | Typical resolution / cadence | Used for |
|---|---|---|---|
| Sentinel-2 (Copernicus) | Multispectral imagery, NDVI/EVI, water surface, turbidity and chlorophyll proxies | 10–20 m, ~5 days | Agro state, lake and river surface, habitat extent |
| Sentinel-5P (TROPOMI) | NO2, SO2, O3, aerosol, methane columns | ~3.5–7 km, daily | Air basin state and emission patterns |
| Landsat 8/9 (USGS) | Multispectral + thermal, long archive back to 1984 (earlier Landsats) | 30 m, 16 days | Baselines, land-use history, water temperature proxy |
| MODIS / VIIRS (NASA) | Daily surface reflectance, LST, fire, ocean/lake color | 250 m–1 km, daily | Long series, phenology, event detection |
| Copernicus DEM / SRTM | Elevation | 30–90 m | Catchment boundaries, flow routing, erosion risk. Copernicus DEM: distributed under ESA/EC terms that vary by product version — verify the current license at build time; NASA SRTM: public domain, near-global 60°N–56°S (USGS derivative products may differ) — record which DEM and which license was used |

## Atmosphere and climate

| Source | Gives | Notes |
|---|---|---|
| ERA5 reanalysis (ECMWF) | Temperature, precipitation, wind, radiation, soil moisture estimates | Hourly, ~31 km; the default meteo driver when no local station exists |
| National meteo services (e.g. NOAA, national hydromet) | Station observations | Prefer station truth over reanalysis where stations exist |
| OpenAQ | Aggregated ground air-quality measurements | Station coverage varies widely; check per city |
| CAMS (Copernicus Atmosphere Monitoring Service) | Atmospheric composition analyses and forecasts: PM, NO2, SO2, O3, pollen | Model/assimilation product — validate against ground stations before threshold use |

## Water

| Source | Gives | Notes |
|---|---|---|
| National hydrology gauges (e.g. USGS NWIS, state services) | Discharge, level, temperature, some chemistry | The calibration backbone for river twins |
| GRDC (Global Runoff Data Centre) | Archived discharge series for large rivers worldwide | Historical calibration and cross-border context; recent years may lag |
| GEMStat (UNEP GEMS/Water) and national water-quality portals (e.g. US Water Quality Portal) | Water chemistry and nutrient observations from monitoring programs | Methods and detection limits vary by program — carry them in the provenance log |
| JRC Global Surface Water (Copernicus) | Water occurrence, seasonality, transitions since 1984 | Inundation and wetland hydroperiod context; 30 m Landsat-based |
| GRACE / GRACE-FO terrestrial water storage | Basin-scale total water storage anomalies | Coarse resolution — a groundwater/storage context layer, never a local measurement |
| GLOSS / national sea-level and lake services | Lake and reservoir levels | Coverage is country-specific |
| Agency and institute archives; historical yearbooks and station logs | Long pre-digital monitoring series, event records, method history | Often decades longer than the digital record; harmonize method changes and log every break in a bias and breaks register (references/analytics-forecasting.md) |
| Client and field sampling | Full chemistry and biology | The only source for most biological indicators; design the sampling before promising the twin. Sanitary microbiology, phytoplankton taxonomy, sediment and tissue chemistry normally require accredited laboratory analysis — budget and turnaround belong in the data plan |

## Biodiversity

| Source | Gives | Notes |
|---|---|---|
| GBIF | Species occurrence records, global | Filter to research-grade, dated, georeferenced records; generalize sensitive records before sharing (`scripts/generalize_coords.py`) |
| iNaturalist (research grade export via GBIF) | Occurrence with photos | Observer bias toward roads and settlements — state it |
| eBird / national monitoring schemes | Bird abundance and trends | Protocol-based; strong for trend indicators |
| National red lists and protected-area registries | Conservation status, legal boundaries | The authority for status; GBIF is not. Mostly human-maintained country registries and PDFs, not machine-readable APIs — budget manual extraction time |
| Movebank | Animal movement and telemetry tracks | Access is per-study and often restricted; sensitive-species safeguards apply in full |
| Museum, herbarium and historical survey records | Pre-digital species occurrences and re-locatable sampling points | Taxonomy and effort differ from modern surveys — harmonize before trend use; provenance per record |

## Soil and land

| Source | Gives | Notes |
|---|---|---|
| SoilGrids (ISRIC) | Soil properties incl. organic carbon, texture, pH | 250 m modeled maps — a prior, not a measurement |
| ESDAC / LUCAS Soil (EU) | Measured topsoil properties and soil survey points | Europe only; strong validation layer where the object is in the EU |
| National soil and cadastre maps | Field boundaries, soil classes | Country-specific access |
| CORINE / national land-cover products | Land-cover classes and change | Basis for habitat extent and fragmentation |

## Interoperability standards

Open formats are what let a local twin nest into regional and national
systems (Phase 6). Adopt per data type at build time and record the choices
in the passport:

| Standard | Covers | Use |
|---|---|---|
| OGC SensorThings API | Sensors, observations, and their exchange | Live and archived sensor feeds in and out of the twin |
| WaterML 2.0 | Hydrological time series | Discharge, level, and water-quality series exchange with hydrology services |
| Darwin Core | Species occurrence data | Biodiversity records shared with GBIF-compatible systems |
| EML (Ecological Metadata Language) | Ecological dataset and forecast metadata | Dataset description; forecast metadata alongside the registry (references/uncertainty-decision.md) |
| STAC | Earth-observation asset discovery | Finding and citing satellite/aerial imagery collections reproducibly |
| CF conventions (netCDF) | Gridded model and reanalysis data | Model outputs and climate/reanalysis exchange |
| RO-Crate | Deliverable packaging | The provenance package itself (Phase 6) |

A twin that invents a private format where a standard exists creates
conversion debt for its owner; deviations are recorded with their reason.

### Semantic mapping sets (`mappings.csv`)

Every dataset directory carries a small mapping file — one row per local
field: `file, local_field, standard_term, standard, justification`.
Each local field maps to a standard term (Darwin Core for biodiversity
fields, Schema.org for generic measurement fields) with a justification
for the mapping, SSSOM-style — or is explicitly recorded as unmapped,
with the reason (no standard term exists for the field, e.g. Ellenberg
indicator values or plant functional types). An unmapped field is a
recorded fact, never a silently dropped column: a reader of the mapping
can tell a considered non-mapping from a forgotten field. The mapping is
checked at onboarding — one row in the Phase 1 checklist
(`assets/templates.md` §1) — and the mapping files are RO-Crate
entities in the provenance package (`scripts/build_manifest.py`
`mappings`: one MappingSet entity per mapping file, `about` the dataset
it maps, conforming to the SSSOM specification). Cross-domain borrowings
are stated in the justification (e.g. Darwin Core `eventDate` borrowed
as the observation timestamp for a non-biodiversity series), never
presented as native uses of the standard. The gallery entries each
carry a `mappings.csv` (see `examples/gallery/*/mappings.csv`).

## Evidence sources (literature platforms)

Published evidence — prior studies, methods, thresholds, benchmark results —
is routed separately in `references/evidence-sources.md`: PubMed / PMC and
Europe PMC for life-science and health evidence, OpenAlex and Crossref for
cross-disciplinary discovery and DOI verification, Semantic Scholar, AGRIS,
and regional-language sources (for Russian objects: CyberLeninka and, where
access exists, eLibrary). Literature justifies the twin's choices; it is
never a source of measurements for the object itself.

## Client and sensor data (added after the open layer)

- In-situ sensors (water sondes, weather stations, soil probes): record model,
  calibration dates, and drift checks in the provenance log; uncalibrated
  sensor series are flagged, not silently trusted.
- Satellite proxies as virtual sensors: a proxy (e.g. Sentinel-2
  chlorophyll-a, Landsat water temperature) becomes a registered virtual
  sensor in the passport (`assets/templates.md` §1) — name, quantity,
  published formula, calibration station, SS_RMSE, validity window; it is
  QC'd and alerted like a physical sensor, and its readings go to the
  [НЕТ ДАННЫХ] register when it leaves calibration (Gironde: 120 virtual
  sensors, simulated from satellite imagery; this is the deterministic
  version — a published formula and a skill score, no ML).
- Farm records: inputs, yields, operations diary — the driver history for agro
  twins.
- Prior studies and EIA reports: mine them for baselines; verify methods
  before reusing numbers.

## Multi-source fusion

Heterogeneous sources (space, aerial, ground, water) are fused in one
scheme — one object, one time base, one spatial reference — before any
indicator is computed from them. Fusion is checked per source against the
checklist below; it extends the Phase 1 onboarding checklist
(`SKILL.md` Stage 2), it never replaces it:

- Coverage: the source's spatial and temporal coverage actually used, and
  what it does not cover.
- Resolution: spatial and temporal resolution, against the decision's
  needs — a coarse source is a context layer, never a local measurement.
- Alignment: how the source aligns with the others — common grid, datum,
  and time base; resampling and harmonization steps named, with their
  method.
- Cross-source consistency: checks performed between independent sources
  (e.g. satellite surface against gauge level, reanalysis against station
  truth, modelled soil against measured points) — agreement and
  disagreement both recorded.
- Gaps: what no source covers → the [НЕТ ДАННЫХ] register; a fused
  product never hides a gap the sources do not fill.

## Field-twin open-data streams

A field twin is fed by four named open-data streams — the same four the
platform literature uses for agricultural holdings (Laguna et al. 2025,
"A platform to support the fast development of digital twins for
agricultural holdings", Computers in Industry 172, 104347, DOI
10.1016/j.compind.2025.104347 — patterns adapted, no code copied; see the
CHANGELOG borrowing note) — each pulled on its own cadence and recorded
in the Phase 1 onboarding checklist with source and access date:

- **Daily weather** — observed temperature, precipitation, wind and
  radiation for the current season; ERA5 reanalysis by default, a national
  meteo station where one exists (station truth over reanalysis).
- **Forecast weather** — the short-range forecast for the same variables
  (national meteo service, or CAMS where available); used for irrigation
  and spray windows, never as a substitute for observations in
  calibration.
- **Historical weather** — the multi-year series for the same variables
  (ERA5 back to 1940, or the national archive); the baseline the current
  season is compared against, and the hindcast window.
- **NDVI** — vegetation state from Sentinel-2 (10–20 m, ~5 days) or
  Landsat (30 m, 16 days) where Sentinel coverage is missing; MODIS/VIIRS
  daily as the coarse context layer, never as the field measurement.

A stream that is unavailable for the object is recorded as a gap in the
[НЕТ ДАННЫХ] register, not silently replaced by another stream: forecast
weather is not historical weather, and a modelled index is not an
observation.
