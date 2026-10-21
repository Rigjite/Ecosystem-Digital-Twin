# Worked example — a small lake, end to end (Tier S)

> **EXAMPLE — a teaching miniature.** The lake, the village, and every
> number below are illustrative, invented to show the shape of a finished
> build. They are not measurements and must never be cited as data.

## Object passport (extract)

- **Object:** Lake Primernoe, 0.8 km², max depth 9 m, one inflow stream,
  one village (900 people) on the north shore, bathing beach, small
  wastewater discharge from the village treatment plant.
- **Owner / decision:** the municipality; the decision is whether to fund
  a constructed wetland on the inflow in next year's budget, and how to
  run bathing-season warnings this year.
- **Maturity:** 3 (Informative) since April 2026, when the alert bands went
  live (2 before that); 4 (Predictive) only after a verified forecast
  season. **Tier:** S.
- **Weights fixed in advance (2026-03-02):** ecosystem outcomes 0.5, cost
  0.2, implementation risk 0.15, time to effect 0.15.
- **Calibration plan, declared before fitting (2026-03-02):** component
  "TP-lag regression" (summer chlorophyll-a from inflow TP load, 2–4 week
  lag); train on 2021–2024 seasons, hold out the 2025 season; baselines
  persistence and monthly climatology from 2021–2024; fail if NSE < 0.5 or
  either baseline is not beaten.

## Data and evidence inventory (extract)

- Open: Sentinel-2 (surface extent, chlorophyll proxy, 2017–today);
  Landsat archive to 1984 (shoreline, catchment land cover); ERA5 meteo;
  regional hydromet station 12 km away (temperature, precipitation).
- Rescued history: the district water yearbooks 1998–2015 give summer
  TP and chlorophyll; the analytical method changed in 2009 — logged in
  the bias and breaks register.
- Client/field: monthly TP, TN, chlorophyll, Secchi, DO profiles from the
  regional lab, 2021–today; village plant discharge reports; a DO sonde
  at the beach since 2023.
- **Gaps stated:** no winter under-ice oxygen data (winter fish-kill risk
  is monitored by testimony and ice records only); no sediment phosphorus
  release measurements (internal loading cannot be calibrated).
- Evidence: eutrophication and bathing-water literature via
  `scripts/evidence_search.py` (English and Russian queries logged);
  thresholds anchored to the national standard, checked at build time —
  not copied from this example.

## Quality gate (extract)

- `qc_series.py` on the beach sonde: a stuck run of 8 identical DO values
  (July 2023, sonde fouling) flagged and quarantined; values untouched.
- `qc_series.py` on the yearbook TP series: Pettitt change point at 2009
  (p < 0.01) — matches the registered method change, so trends are split
  there.

## Indicators selected (extract)

Core lake set: water level; temperature and DO profiles; TP (total and
phosphate fraction), TN (nitrate and ammonium separately); chlorophyll-a;
Secchi; phytoplankton composition in season; cyanobacteria biovolume;
E. coli at the beach (bathing use triggers the sanitary panel); inflow
load (concentration × discharge). Conditional panel added: sediment TP
(internal-loading question; listed as a gap until sampled). Not selected:
PFAS, radionuclides — no source or pathway; reason recorded.

## Pattern memo (extract)

- Summer TP trend (`trend_test.py --breaks 2009-01-01`): 1998–2008 rising,
  Sen slope +0.8 µg/L per year (p = 0.04); 2009–2015 no significant trend.
  No single 1998–2015 trend is reported.
- Ice-off has advanced ~9 days across the Landsat record (high confidence
  as a satellite observation; ecological meaning still being assessed).
- Chlorophyll follows inflow TP with a 2–4 week lag in the monthly series —
  the lead–lag behind the calibrated component below.
- Both recorded blooms followed at least 10 hot, calm days. With n = 2 this
  is a hypothesis that shapes the watch trigger, not a statistical pattern.

## Calibration report (extract)

- TP-lag regression, hold-out 2025 (`skill_scores.py continuous`, split and
  thresholds as declared): NSE 0.58, skill against climatology 0.31,
  against persistence 0.12 → **gate passed**. Only 6 hold-out months
  (May–October 2025): the report states the count and calls the skill
  provisional.
- Fails in: the 2025 heat wave month (under-predicts by ~40%) — consistent
  with uncalibrated internal loading.
- Not calibrated: internal phosphorus loading (no data). The twin therefore
  does not quantify how fast the lake responds to a cut in inflow load.

## Event catalogue (extract)

| Year | Event | Antecedents | Impact | Response |
|---|---|---|---|---|
| 2019 | Cyanobacteria bloom, 3 weeks | Heat wave, calm, high TP | Beach closed 12 days | Advisory only |
| 2022 | Bloom + small fish kill | Heat, stratification, DO crash at depth | Fish loss, press attention | Emergency aeration, late |

Two bloom events in the record — far below what a statistical event
forecast needs. **No bloom probability is issued.** The product is a
**watch** on antecedent conditions plus the TARP below, labeled as such.

## Forecast registry entry (extract) — trial forecast

- **ID:** LP-F-001, registered with `registry.py issue` on 2026-05-04,
  before the season; latest chain hash e-mailed to the municipality officer.
- **Forecast:** July–August 2026 mean chlorophyll-a at the deep station:
  22 mg/m³, interval 14–31 mg/m³ (95% regression prediction interval).
- **Status:** **trial** — the lake twin is at level 3; this forecast earns
  level 4 only if verified, and carries no decision weight this season.
- **Model:** TP-lag regression v0.2 (calibrated, see above); inputs ds-03
  (lab chemistry), ds-05 (inflow load). **Metric declared:** absolute error
  and interval hit, computed by `registry.py score` against this entry.

## TARP (extract) — LP-T-01, bloom and bathing risk

- **Trigger:** surface temperature > 23 °C for 5 days + cyanobacteria
  biovolume above the amber band on two consecutive samplings.
- **Watch:** sampling twice weekly; beach signage prepared.
- **Act:** bathing advisory issued by the municipality's named officer;
  aerator deployed to the deep basin.
- **Lead time:** the aerator needs 1 day; 5–7-day weather forecasts give
  the watch several days beyond that — prevention is feasible, and the plan
  says why. If that margin disappeared, this would be relabeled a response
  plan.
- **Stand-down:** two consecutive samplings below the amber band.
- **After-action review:** at season close, with the LP-F-001 score.

## Option card (extract) — the budget decision

- **Option:** constructed wetland on the inflow (nature-based, evaluated
  first). Class: mitigate.
- **Expected effect:** inflow TP load −30 to −45% within 2–3 years.
  **Evidence-based, not a twin forecast:** the range applies published
  wetland retention (systematic review tier; transferability recorded:
  climate zone, loading rate, wetland-to-catchment area ratio) to the
  measured inflow load. The lake's chlorophyll response is **not
  quantified** — internal loading is uncalibrated; the card says so.
- **Cost/risk:** land lease on 1.2 ha of marginal farmland; maintenance
  duty named. **Reversibility:** high. **Residual risk:** blooms remain
  possible in hot years even after load cuts — the TARP stays in force.
- **Value of information:** two seasons of sediment TP sampling would let
  the twin quantify the lake response; cost stated next to the budget item.
- **Verification:** inflow TP load and summer chlorophyll, reviewed at
  year 3 against this card. **Counterfactual:** on funding approval, the
  no-action baseline twin is frozen (configuration archived with manifest
  IDs) and both twins run on the same observed weather thereafter.

## Deliverable and gate

The package ships at maturity 3: the bloom product is a watch, LP-F-001 is
labeled trial, winter oxygen and internal loading are stated gaps.
`build_manifest.py --report` passes (every headline number cites its
`[out-…]` ID). A red-listed orchid record on the shore (GBIF) appears in the
public summary only on the 0.1° grid; `generalize_coords.py --check`
passes. Gate C red-team record: three material attacks — threshold anchor
re-checked against the current national standard; satellite chlorophyll
proxy relabeled as a proxy; LP-F-001 shown in the public summary without
its trial label — all three fixed before delivery.
