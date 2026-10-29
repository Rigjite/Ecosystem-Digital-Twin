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
11. Automated satellite fetch (`scripts/fetch_satellite.py`)
12. New open sources (2026-10-28)

## Satellite and Earth observation

| Source | Gives | Typical resolution / cadence | Used for |
|---|---|---|---|
| Sentinel-2 (Copernicus) | Multispectral imagery, NDVI/EVI, water surface, turbidity and chlorophyll proxies | 10–20 m, ~5 days | Agro state, lake and river surface, habitat extent |
| Sentinel-5P (TROPOMI) | NO2, SO2, O3, aerosol, methane columns | ~3.5–7 km, daily | Air basin state and emission patterns |
| Sentinel-1 (Copernicus) | SAR C-band: InSAR ground displacement, soil moisture, flood extent, water and ice mapping | IW 5 × 20 m, 6–12 days | Slope watch (InSAR pair: two passes, days apart), flood mapping, soil moisture. Free and open, like all Copernicus data |
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
| Open-Meteo (open-meteo.com) | Forecast weather API: temperature, precipitation, wind, radiation, humidity, ET₀ — model output from national weather services (DWD ICON, NOAA GFS, ECMWF IFS, Météo-France, JMA and others) | Hourly, 1–11 km depending on model; forecast to 16 days; historical archive (ERA5) back to 1940 | Free for non-commercial use, no API key and no account (a key is required only for commercial use); model output, not station truth — validate against a station before threshold use |

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
  (national meteo service, CAMS, or Open-Meteo where available); used for irrigation
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

## Automated satellite fetch (`scripts/fetch_satellite.py`)

The manual route above (an agent finding scenes by hand) is automated by
`scripts/fetch_satellite.py`: it searches a public STAC catalogue for
scenes over a bounding box and date range, records the scenes and their
asset links in a manifest, downloads the red / near-infrared bands on
request (`--download`), and computes NDVI where the bands are available
(`--compute-ndvi`). Every product is registered as a virtual sensor in
the Object Passport (§1): name, quantity, formula, source, collection,
bounding box, date range, retrieval date, validity window.

- **Catalogues:** Planetary Computer STAC (no key for search;
  collections `sentinel-2-l2a`, `landsat-c2-l2`, `sentinel-1-rtc`,
  verified live 2026-10-28) and Copernicus Data Space STAC (search open;
  download needs a free account and a token, `--cdse-token`). The
  Copernicus catalogue was unreachable from this environment on
  2026-10-28: verify access at build time; services change.
- **Modes:** `--check` searches only and downloads nothing (the default
  behaviour); `--download` fetches the red / NIR bands of the least-cloudy
  scene (`--all` for every kept scene); `--compute-ndvi` computes NDVI
  statistics from the downloaded bands. `--stac-file` runs the script
  offline on a recorded STAC response.
- **NDVI bands:** Sentinel-2 red B04 / NIR B08; Landsat 8/9 red `red`
  (SR_B4) / NIR `nir08` (SR_B5). NDVI = (NIR − red) / (NIR + red); a zero
  denominator (both bands zero) is not a measurement and is recorded as
  such, never as 0. Statistics are computed on a 512×512 downsampled
  preview and the manifest says so.
- **Sentinel-1:** scenes are searched and recorded; displacement is NOT
  computed by the script — it needs InSAR processing of a pair (SNAP /
  ASF HyP3).
- **No rasterio, no computation:** reading GeoTIFF bands needs the
  optional `rasterio` package. Without it the script records the scenes
  and asset links and marks the computation as deferred — it never
  invents numbers.
- **Failure is loud:** an unreachable catalogue, a 429 rate limit, or a
  refused download exits non-zero with a named reason. Exit codes: 0 ok;
  2 usage error; 3 catalogue / network / auth failure.

### Latency honesty: a satellite is periodic, never real-time

| Source | Revisit | Typical product latency | What it means for warning |
|---|---|---|---|
| Sentinel-2 (L2A) | ~5 days | hours–1 day after sensing | the newest usable scene is usually days old |
| Sentinel-1 (GRD/RTC) | 6–12 days | hours–1 day | displacement needs an InSAR pair: two passes, days apart |
| Landsat 8/9 (C2 L2) | 16 days (8 with both) | ~1 day | long archive; slow refresh |
| MODIS / VIIRS | daily | hours | coarse context only (250 m–1 km), never a local measurement |
| Ground telemetry (gauges, sondes, meteo stations) | minutes–hourly | minutes | the only real-time layer |

A twin that promises real-time warning from a 5-day revisit is
mislabelled. Record the cadence in the Object Passport, date every
scene in the manifest, and let ground telemetry carry the real-time
alerts while the satellite carries the context and the trend between
passes.

## New open sources (2026-10-28)

Added on the author's word ("Собери полный реестр датчиков"). Each row
states whether it is a measurement or a model/context layer; the full
sensor mapping — every source to the ecosystems and indicator rows it
serves, in four tiers — is in `references/sensor-registry.md`.

| Source | Gives | Typical resolution / cadence | Access | Used for |
|---|---|---|---|---|
| NASA FIRMS (Fire Information for Resource Management System) | Active-fire / thermal-anomaly detections (VIIRS 375 m, MODIS 1 km), with time and fire radiative power | 375 m (VIIRS) / 1 km (MODIS), near-real-time, under 3 h from overpass | Free; free MAP_KEY via firms.modaps.eosdis.nasa.gov/api/area/ | Fire occurrence (§30 forest, §22 steppe, §24 peatlands); the near-real-time fire layer the Zone A comparison was missing |
| Global Forest Watch / Hansen (Hansen et al. 2013, Science 342:850–853) | Tree-cover loss year (lossyear) and year-2000 tree cover, from Landsat time series | 30 m, annual, 2001–present | Free, CC BY 4.0, download and API | Forest loss by driver (§30); the independent layer that attributes a patch to a loss year. Loss is not deforestation — fire, harvest, disease and storm all count. User's accuracy 87.0% globally for loss |
| ESA WorldCover | Land-cover class, 11 classes (tree cover, shrubland, grassland, cropland, built-up, bare/sparse, snow/ice, water, herbaceous wetland, mangrove, moss/lichen), from Sentinel-1 + Sentinel-2 | 10 m, annual (2020, 2021, …) | Free | Habitat extent, fragmentation and conversion (§10, §30, §31, §26, §32, §25). Overall accuracy 74.4% (WorldCover 2020, ESA Product User Manual v1.0); class accuracy varies — shrubland, wetland and moss/lichen lower |
| OpenStreetMap | Roads, settlements, buildings, waterways, land-use polygons | Vector, updated continuously by contributors | Free, ODbL licence | Fragmentation, access and attractant layers (§10, §26, §30); the roads layer that decides whether a patch is logging or fire |
| GPM IMERG (NASA/JAXA) | Precipitation rate, half-hourly, accumulated to daily totals | 0.1° (~10 km), half-hourly, from 2000; Early Run 4-h latency, Late Run 14-h, Final Run ~3.5 months | Free via NASA Earthdata (free account) | Precipitation (§1) and flood forcing (§3) where no gauge exists. Lower skill over frozen surfaces, complex terrain, and coastal zones |
| SMAP (NASA) | Surface (0–5 cm) and root-zone (0–100 cm) soil moisture, L4_SM product | 9 km, 3-hourly, from 31 March 2015 | Free via NASA Earthdata (free account) | Soil moisture (§9, §31, §22, §28). ubRMSE 0.038 m³/m³ surface and 0.030 m³/m³ root-zone at 9 km (Reichle et al. 2017, J. Hydrometeorol. 18:2621–2645) |
| Copernicus Marine Service (OSTIA) | Foundation sea surface temperature and sea-ice fraction, daily gap-free maps | 0.05° (~5 km), daily, 1981–present | Free on registration | SST and marine heatwaves (§25); aquaculture temperature vs species optimum (§27). Foundation SST, not skin temperature; some large lakes covered, not all |
| WDPA / Protected Planet (UNEP-WCMC / IUCN) | Protected-area boundaries, designation, IUCN category, status year | Vector, new version monthly | Free for non-commercial use; commercial use via IBAT | Protected-area rows (§15, §11, §17) as a layer. Caveat: some providers requested their data not be shared beyond WDPA managers — as of June 2019: China, the Russian Federation, Estonia, Saint Helena / Ascension / Tristan da Cunha (WDPA User Manual) — check coverage for Russian objects at build time |
