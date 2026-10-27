---
name: ecosystem-digital-twin
description: "An Agent Skill for designing and operating evidence-bound digital twins and linked twin networks of ecosystems (ponds, lakes, rivers, agricultural land, air basins, and biodiversity sites). Guides the 7-stage build cycle (Phases 0–6), enforces strict separation between AI agents and deterministic code, implements counterfactual baselines, safety gates for circular-economy cascades, Value of Information (VoI) assessment, and RO-Crate provenance. Use when modeling an ecosystem, linking multi-ecosystem cascades, analyzing monitoring data, or evaluating environmental and agricultural intervention scenarios."
license: CC-BY-4.0
compatibility: "Bundled scripts need only Python 3.9+ and its standard library. scripts/evidence_search.py needs network access to PubMed, Europe PMC, OpenAlex, and Crossref. Open data (Copernicus Sentinel, Landsat, GBIF, ERA5, SoilGrids, national hydrology and meteo services) is fetched at build time with whatever access the environment has; GIS tooling (QGIS, geopandas) is optional."
metadata:
  version: "2.7"
  skill-author: Rigjita Baldanova
  last-reviewed: "2026-10-26"
---

# Ecosystem Digital Twin — Agent Skill (v2.7)

An Agent Skill for designing and operating evidence-bound digital twins and
networks of linked digital twins across aquatic ecosystems (lakes, ponds,
river basins), agroecosystems (crop fields, smart farming, livestock),
contaminated soils, air basins, and biodiversity conservation sites. A twin
built with this skill is a living, observation-synchronized model of a real
object (or a conceptual pre-project in silico proposal explicitly labeled as
such). It diagnoses current states, warns early of non-linear shifts, and
evaluates environmental and economic interventions against a counterfactual
baseline before physical implementation. Current version: 2.7 (2026-10-26).
License: CC BY 4.0.

## Professional stance

A twin is built to the standard of a senior practitioner. That means:
deep domain knowledge across water, ecosystems, remote sensing, statistics,
and governance; a comparative view — how twins are built in other
countries, with an explicit check that a borrowed pattern transfers to
this object before it is used; evidence first — every number traced to a
verified source, every limit disclosed, no fabricated datum; and
verification that no seniority overrides — every claim is checked against
its primary source before it is used, whatever the builder's experience.

## Non-Negotiables (Strict Rules)

1. **No Fabricated Data & Deterministic Compute Isolation:** Every numerical
   value MUST trace to a verified source (with date, method, and resolution)
   or be computed by deterministic code (`scripts/`). Language models and AI
   agents NEVER invent or manually calculate numbers. Missing parameters MUST
   be stated explicitly as data gaps ([НЕТ ДАННЫХ]).
2. **Explicit Maturity Labeling:** Uncalibrated or conceptual models MUST be
   labeled in writing as a Prototype or Conceptual Proposal — never shipped
   as an operational twin. (How the labels map to the skill's 5-level
   ladder and to exploratory / operational status: the maturity cross-walk
   in Template 1.)
3. **Biodiversity Data Sensitivity:** Precise coordinates of rare or
   sensitive species are NEVER published; they are generalized to a 0.1°
   grid per GBIF sensitive-data protocols
   (`scripts/generalize_coords.py`).
4. **Intervention Priority & Counterfactual Baseline:** Every scenario
   analysis MUST run a parallel Counterfactual ("No-Action") Twin
   (Scenario 0) and evaluate nature-based solutions (e.g. constructed /
   floating wetlands, green buffers) alongside or prior to capital-intensive
   engineered options.
5. **Circular-Economy Safety Gate:** In linked twin networks where waste or
   sediment from one ecosystem is processed into an input for another (e.g.
   Polluted Water Body -> Sludge Treatment Node -> Agricultural Field),
   transfer to the receiving ecosystem is gated by an explicit Safety &
   Standards Gate (Compliance Confirmed? -> Yes / No). Until laboratory
   verification confirms compliance for heavy metals, toxins (e.g.
   microcystins), and pathogens, the baseline pathway defaults to safe
   containment.

## The 7-Stage Operational Cycle (Phases 0–6)

### Build depth: Tier S / M / L

Not every build runs the full cycle. The depth is declared in the Object
Passport (orchestration tier, S / M / L) and every skip is recorded there
with its reason — a Tier S build is a smaller twin, not a sloppier one.

- **Tier S — Diagnostic & Feasibility Twin (3–5 days):** the ten-step path
  in `references/quick-start.md`, in short: Object Passport →
  `scripts/qc_series.py` → `scripts/trend_test.py` (indices + trend) →
  Scenario 0 vs Intervention + VoI/EVSI → Safety Gate → Public Status
  Line. Every other tool (`scripts/drift.py`, `scripts/diversity.py`,
  `scripts/trait_match.py`, the nudge, the model ladder, FAIR
  Signposting) is modular and joins only when the object's task requires
  it.
- **Tier M — Full cycle:** the whole 7-stage cycle on one object or a
  small network — every stage, with the counterfactual twin, the
  uncertainty budget, and the tools above where the task requires them.
  Use when the build spans several domains, makes predictive claims, or
  feeds a client decision with money or health at stake.
- **Tier L — Full cycle + governance:** Tier M plus the multi-agent
  governance in `references/orchestration.md` (roles, contracts, red-team
  gates). Use for regulatory, contested, or public-health builds.

- **Stage 1 — Object Passport (Phase 0):** Before any calculation, lock
  spatial boundaries, the core management question, regulatory thresholds
  (e.g. WHO, national ambient water/soil standards), maturity level, and
  trophic/pollution indices (WPI, Carlson TSI, HPI, OECD thresholds).
- **Stage 2 — Data Inventory & QC (Phase 1):** Aggregate satellite remote
  sensing (e.g. Sentinel-2 water transparency/SDD), in-situ hydrochemical /
  soil samples, and literature baselines. Screen time series with
  deterministic quality control (`scripts/qc_series.py`). Never interpolate
  across gaps silently. Incoming files move through three zones, never
  edited in place: `landing/` — as received, untouched; `trusted/` —
  QC-passed (the `scripts/qc_series.py` gate pass recorded);
  `refined/` — domain-converted and model-ready, the conversion recorded
  in the build manifest. A file leaves `landing/` only after its QC is
  recorded; a file enters `refined/` only after its conversion is
  recorded. Onboard every dataset against the Phase 1
  checklist — source and access date, licence and reuse terms, spatial and
  temporal resolution and coverage, QC performed (method and result),
  gaps → the [НЕТ ДАННЫХ] register. A dataset failing any item is not
  admitted to the twin until the failure is recorded as a gap or the
  dataset is replaced. Heterogeneous sources are then fused in one scheme
  against the fusion checklist (`references/data-sources.md`): per source
  — coverage, resolution, how it aligns with the other sources,
  cross-source consistency checks performed, gaps → the [НЕТ ДАННЫХ]
  register. Fusion extends the onboarding checklist; it never replaces it.
  Biodiversity is reported as richness plus Shannon, Pielou and taxonomic
  distinctness (`scripts/diversity.py indices`), PFT shares
  (`scripts/diversity.py pft`) and trait–environment matching
  (`scripts/trait_match.py`) — richness alone never stands as the
  diversity result. A twin's working folder follows one layout:
  `common/` (passport, shared data), `etl/` (ingestion + QC),
  `calibration/` (models + admission), `forecasts/` (bulletins +
  registry), `simulations/` (scenarios). The build manifest
  (`scripts/build_manifest.py`, Stage 7) records which file sits where.
- **Stage 3 — Model & Calibration Against Benchmark (Phase 2–3):** Formulate
  the mathematical or conceptual state model (`scripts/trend_test.py` with
  Hamed–Rao autocorrelation correction). An operational model is admitted to
  forecasting ONLY if it outperforms a naive inertial benchmark on a held-out
  sample (`scripts/skill_scores.py`). Admission is not once-and-for-all:
  on each new QC-passed batch the admitted model is re-scored on the new
  hold-out (`scripts/skill_scores.py revalidate`); SS_RMSE ≤ 0 revokes
  ADMITTED and the twin's maturity label drops to the highest level the
  twin still meets, until a better model is admitted. Admission has two
  gates, both must pass: the plausibility gate (`scripts/skill_scores.py
  admit` — SS_RMSE > 0 on every PRIMARY target variable declared in the
  Object Passport; secondary background variables are reported, not
  gated — when no variable in the dossier carries a `primary` flag,
  every variable is primary — and every fitted parameter inside its
  declared physical bounds, `references/calibration-bounds.md`) and the
  alert trial (`scripts/skill_scores.py alert-trial` — alert quality,
  not model skill; a quiet window with no alerts and no critical events
  is INCONCLUSIVE_QUIET_WINDOW, which neither admits nor rejects —
  admission then waits for a synthetic stress-test or a historical
  extreme replay). Forecast skill is reported per lead time
  (`scripts/skill_scores.py skill-horizon`): the report states the skill
  horizon — the longest lead at which the forecast still beats
  persistence — and a forecast is not trusted beyond it. A raw forecast
  may be nudged by the mean recent residual (`scripts/skill_scores.py
  nudge`, N declared in the Object Passport); the correction is recorded
  in the registry entry and the nudged forecast is scored per lead time
  like any forecast. The verification record reports phenomenon-oriented
  metrics alongside the generic score (`references/analytics-forecasting.md`
  §4: onset-date, peak and duration errors for the phenomenon at hand) —
  admission stays SS_RMSE, but the client sees skill on the events that
  matter. Before calibrating, run a sensitivity screen
  (`scripts/sensitivity_screen.py`): perturb each model parameter one at
  a time (±10% or a stated range) and record the output change as a
  ranked table; calibrate only the influential parameters and leave the
  rest at literature values — the screen is what makes that choice
  defensible. One-at-a-time misses interactions, unlike Sobol indices;
  the screen ranks, it does not prove independence. The screen perturbs
  MODEL parameters (the calibration knobs); the driver-perturbation
  table (`references/scenarios.md`) perturbs INPUT drivers — different
  questions, different tables, never merged. A twin may carry two
  models of the same object — a FAST model for screening in the field
  and a FULL-SCALE model for the decision (the Model ladder). The fast
  model is admitted for SCREENING ONLY and must stay within a declared
  tolerance of the full model on the same hold-out (checked by
  `scripts/skill_scores.py`); both models are named in the Object
  Passport with the tolerance. A fast model outside its tolerance is not
  used for decisions. A model is operational only after a recorded
  promotion (`scripts/registry.py promote` — promoted by, on, evidence:
  benchmark + hold-out score); without one it is exploratory and its
  outputs are never presented as operational. Where
  sediment/soil exchange parameters are unmeasured, evaluate sensitivity
  across a parameter ensemble or explicitly limit the scope to
  directional scenario comparison.
- **Stage 4 — "What-If" Scenarios vs. "No-Action" (Phase 5):** Compare
  single interventions (e.g. one-off sediment dredging vs. catchment inflow
  interception/wetlands) and combined strategies across short- and
  long-term horizons (e.g. 5, 10, 50 years). Highlight delayed responses and
  the decay of one-off measures when external loading persists.
  Every scenario declares its class: Scenario 0 — the No-Action
  counterfactual (the baseline every scenario is judged against, never
  redefined); Planning scenarios — external drivers to plan around (land
  use, development, catchment change), not interventions; What-if
  intervention scenarios — the measures themselves (prevent / mitigate /
  restore / adapt / monitor); Storyline scenarios — a named historical
  extreme replayed under changed drivers, scored on impacts. A scenario without a declared class is not
  scored. A scenario delta is trusted as a number only after the
  hindcast reproduction gate passes (`references/scenarios.md` — the
  scenario model must reproduce the observed historical period with the
  intervention switched off); a failed check means the delta is reported
  as "unvalidated, direction only". (Taxonomy: `references/scenarios.md`; counterfactual protocol:
  `references/uncertainty-decision.md` §4.)
- **Stage 5 — Independent Red-Team Review:** Audit the twin for post-hoc
  threshold selection, unverified commercial claims, author↔employer data
  loops, and hidden assumptions (e.g. incomplete inflow capture by wetlands
  or unmeasured sediment cores vs. surface water samples).
- **Stage 6 — Human Decision:** Translate complex biogeochemical and
  physical-chemical processes into clear environmental and agricultural
  economic metrics. The twin serves two tiers of users: Focus
  Applications for the builders who run it, and What-if Scenarios for
  the decision-makers who act on it (`assets/templates.md` §7–§8). When a
  decision is made under pressure, the twin states in plain terms what
  the model used, what it did not use, and how confident it is — no
  black-box verdicts; the explanation is recorded on the scenario card
  (`assets/templates.md` §6). The next sampling targets are ranked by
  model disagreement (`scripts/uncertainty_budget.py sampling-priority`):
  where the models disagree most, the twin samples next. Every twin also ships a public status line
  (`assets/templates.md` §10) — one paragraph in plain language: current
  state, what changed, the maturity label, the [НЕТ ДАННЫХ] gaps —
  generated from the runner's summary JSON; it is for the client and the
  public, distinct from the handover note (for a successor builder,
  technical) and from RO-Crate (for machines). Final authority to approve interventions or
  investment proposals rests strictly with the human specialist.
- **Stage 7 — Monitoring & Twin Updating (Phase 4 & 6):** Assimilate new
  observations to reject incompatible ensemble members and narrow forecast
  uncertainty, recompute alert bands (`scripts/alert_bands.py`), and update
  all linked nodes. When an alert fires, the twin also notifies its linked
  nodes (upstream and downstream twins) — the notification is recorded on
  the trigger–action–response plan (`assets/templates.md` §3), not in the
  forecast registry; a notified node re-checks its own alert bands on the
  next batch. New data arrive as QC-passed batches
  (`scripts/qc_series.py` gate pass). On each batch the recalibration
  trigger is checked (`scripts/trend_test.py --mode drift --baseline
  <calibration> --drift-threshold <per-indicator>`): level drift
  |mean(new) − mean(calibration)| / sd(calibration) at or above the
  declared threshold, or a new-batch Sen slope outside the calibration
  slope's confidence interval, fires the trigger. When it fires, the model
  is recalibrated (Stage 3 re-run on calibration + new data), alert bands
  are recomputed, linked nodes are updated, and the recalibrated model is
  revalidated before it can keep ADMITTED status; a failed revalidation
  flags the model and drops the maturity label. The drift threshold is
  declared per indicator in the Object Passport — a declared parameter,
  not a universal law. (Rule: `references/analytics-forecasting.md` §8.)
  Package deliverables with an append-only hash-chain forecast registry
  (`scripts/registry.py`) and RO-Crate 1.1 provenance manifest
  (`scripts/build_manifest.py`, which records the twin workspace layout
  from Stage 2). The crate's Root Dataset carries FAIR
  Signposting relations (signposting.org) — `cite-as` (the package DOI,
  never invented), `describedby` (`ro-crate-metadata.json` itself),
  `license` — written by `scripts/build_manifest.py`; when the package is
  served over HTTP the same relations belong in Link headers. Every
  forecast record carries its refresh
  cadence (`daily` | `weekly` | `seasonal` | `event-driven`) and the usable
  warning lead time for the decision (`lead_time`: value + unit, e.g.
  3 days) — a forecast earns its keep only if the warning arrives in time
  to act. Both fields are validated on `issue` and on `verify`; records
  issued before v2.4 carry neither field and still verify.

## Core Mathematical Specifications

All quantitative assessments must adhere strictly to the following equations
(executed via `scripts/`):

1. **Water Pollution Index (WPI / ИЗВ):** WPI = (1/n) Σ_{i=1}^{n} C_i /
   MAC_i, where C_i is the observed concentration of indicator i, MAC_i is
   its regulatory Maximum Allowable Concentration (ПДК), and n is the number
   of core hydrochemical indicators (typically n = 6, including dissolved
   oxygen and BOD5; for DO, the ratio is MAC_DO / C_DO when C_DO < MAC_DO).
2. **Carlson's Trophic State Index (TSI):** TSI(SD) = 60 − 14.41 ln(SD[m]);
   TSI(Chl-a) = 9.81 ln(Chl-a[μg/L]) + 30.6; TSI(TP) = 14.42 ln(TP[μg/L]) +
   4.15. Composite TSI is the arithmetic mean of available components
   (<40 oligotrophic, 40–50 mesotrophic, 50–70 eutrophic, >70
   hypereutrophic).
3. **Heavy Metal Pollution Index (HPI):** HPI = (Σ W_i Q_i) / (Σ W_i),
   W_i = 1/S_i, Q_i = 100 × |M_i − I_i| / (S_i − I_i), where M_i is the
   measured heavy metal concentration (μg/L or mg/kg), S_i is the regulatory
   standard limit, and I_i is the ideal background/guideline value (set to 0
   if strictly toxic). Critical pollution threshold: HPI = 100.
4. **Mann–Kendall Trend Test with Hamed–Rao (1998) Autocorrelation
   Correction:** For a time series x_1, …, x_n, the Mann–Kendall statistic
   is S = Σ_{i=1}^{n−1} Σ_{j=i+1}^{n} sgn(x_j − x_i). Under serial
   autocorrelation, the variance Var(S) is corrected using the effective
   sample size factor n / n_S*: n/n_S* = 1 + [2 / (n(n−1)(n−2))]
   Σ_{k=1}^{n−1} (n−k)(n−k−1)(n−k−2) ρ_k; Var*(S) = Var(S) · (n / n_S*),
   where ρ_k is the autocorrelation function of the ranks of detrended
   observations (using the Theil–Sen median slope β = median((x_j − x_i) /
   (t_j − t_i))) for lags k that are statistically significant at the 95%
   confidence level (|ρ_k| > 1.96/√n).
5. **Benchmark Skill Score (SS_RMSE) & Nash–Sutcliffe Efficiency (NSE):**
   SS_RMSE = 1 − RMSE_model / RMSE_naive; NSE = 1 − Σ_{t=1}^{T} (y_t −
   ŷ_t)^2 / Σ_{t=1}^{T} (y_t − ȳ)^2, where ŷ_t^naive = y_{t−1} (inertial
   random-walk persistence) or seasonal climatology. A model is admitted
   (ADMITTED) to operational forecasting if and only if SS_RMSE > 0 on
   out-of-sample validation data.
6. **Value of Information (VoI / EVSI):** Before approving capital-intensive
   remediation, evaluate whether resolving key parameter uncertainty θ (e.g.
   internal sediment phosphorus flux vs. external catchment loading) changes
   the optimal intervention a ∈ A: EVPI = E_θ[max_{a ∈ A} NPV(a, θ)] −
   max_{a ∈ A} E_θ[NPV(a, θ)]. If the Expected Value of Sample Information
   EVSI > C_survey (cost of sediment coring, toxin assay, or pilot batch
   test), Stage 6 MUST recommend executing the diagnostic survey prior to
   capital deployment.
7. **Hazard Quotient / Hazard Index (HQ/HI):** HQ_i = exposure_i /
   reference_i per stressor (exposure ≥ 0, reference > 0; duration
   "acute" or "chronic", default "chronic"); HI = Σ_i HQ_i, split by
   duration into HI_acute and HI_chronic; unsafe when HI > 1 (threshold
   1). The published HI is often reported per target organ — the script
   sums by duration and keeps the target on each term, so a per-target HI
   is read off the terms. (`scripts/trend_test.py --mode hq`.)
8. **Biodiversity indices — Shannon, Pielou, taxonomic distinctness
   (Δ+):** Shannon H′ = −Σ_i p_i ln p_i (natural logarithm throughout),
   p_i = count_i / N; Pielou J′ = H′ / ln(S), S = number of species with
   count > 0 (undefined for S < 2); Δ+ = mean Clarke–Warwick taxonomic
   distance over all pairs of species present, where the distance between
   two taxa is the weight of the deepest rank (genus → phylum) at which
   both are known and equal — genus 1, family 2, order 3, class 4,
   phylum 5 — and 6 when the pair shares no rank at all (different
   phyla); Δ+ is undefined with fewer than two taxa with taxonomy.
   (`scripts/diversity.py indices`.)
9. **Kling–Gupta Efficiency (KGE):** KGE = 1 − √((r − 1)² + (α − 1)² +
   (β − 1)²), where r is the Pearson correlation between observed and
   simulated, α = σ_sim / σ_obs, β = mean_sim / mean_obs.
   (`scripts/skill_scores.py continuous`.)
10. **Observation nudge:** nudged = raw forecast − mean(sim − obs) over the
    last N QC-passed observation/model pairs (N declared in the Object
    Passport, default 5); residual = sim − obs. The correction is recorded
    in the registry entry, and the nudged forecast is scored per lead time
    like any forecast. (`scripts/skill_scores.py nudge`.)
11. **Drift — Lagrangian transport with wind leeway:** per step dt,
    Δlat = (v + leeway × wind_v) × dt / 111320 and Δlon = (u + leeway ×
    wind_u) × dt / (111320 × cos(lat)), with (u, v) the current field
    value at the latest time ≤ the step time and leeway = 0 meaning
    current only (1° latitude = 111320 m; 1° longitude = 111320 ×
    cos(lat) m). Arrival is the first step inside a target zone;
    connectivity = arrivals / released; travel time is the arrival step's
    hours. The current field is spatially uniform per time step and the
    zones are rectangles without a coastline mask — a screening
    (0D) model of open water or a straight reach, not a hydrodynamic
    model of a lake with bays or a winding river. (`scripts/drift.py`.)
12. **Drift statistic (Stage 7):** drift level = |mean(new batch) −
    mean(calibration)| / sd(calibration); the trigger fires at or above
    the declared per-indicator threshold (default 2.0 calibration SDs),
    or when a new-batch Sen slope falls outside the calibration slope's
    confidence interval. (`scripts/trend_test.py --mode drift`.)

## Mandatory Deliverable Templates

### Template 1: Stage 1 — Object Passport (ObjectPassport)

Every twin workflow MUST open with this structured table:

#### Паспорт цифрового двойника (Stage 1 — Object Passport)

- Объект и пространственные границы: [Название, координаты (обобщенные до
  0.1° при наличии редких видов), площадь/объем, водосбор]
- Статус зрелости (Maturity Label): [Prototype | Descriptive | Informative
  | Predictive | Decision] — the skill's own 5-level ladder; the twin is
  described to the client by its level, never above it.
- Maturity cross-walk: Prototype (ladder level 1) is also called a
  Conceptual Proposal — an uncalibrated or conceptual model, exploratory,
  never presented as operational. A model is operational only after
  ADMITTED + a recorded promotion (`scripts/registry.py promote`);
  operational corresponds to Predictive / Decision on the ladder. Without
  the promotion a model is exploratory, even when ADMITTED. On a failed
  revalidation the label drops to the highest level the twin still meets
  (Stage 3).
- Ключевой управленческий вопрос: [Целевая задача, горизонт моделирования:
  5 / 10 / 50 лет]
- Primary target variables: [The variables the management question is
  decided on — SS_RMSE > 0 is required for these in the plausibility gate
  (`scripts/skill_scores.py admit`); secondary background variables are
  reported, not gated. When no variable is named here, every variable is
  primary.]
- Drift threshold (per indicator): [Declared per indicator, e.g. 2.0
  calibration SDs; `scripts/trend_test.py --mode drift` — a declared
  parameter, not a universal law; the script default 2.0 applies only when
  the passport declares nothing.]
- Нормативная база и пороги: [WHO / ПДК / региональные стандарты, целевые
  индексы WPI, TSI, HPI]
- Связанные узлы (Linked Nodes): [Входной узел -> Текущий двойник ->
  Выходной узел / Нет]
- Реестр пробелов данных ([НЕТ ДАННЫХ]): [Явный список неизмеренных
  параметров]
- Онбординг данных (Phase 1 checklist): [По каждому набору данных —
  источник и дата доступа, лицензия, разрешение и охват, выполненный QC,
  пробелы → [НЕТ ДАННЫХ]]
- Синтез источников (fusion checklist): [По каждому источнику — охват,
  разрешение, согласование с другими источниками, проверки
  согласованности, пробелы → [НЕТ ДАННЫХ]]
- Передача сопровождения (Handover): [Кто ведёт двойника после автора —
  имя/роль, условия передачи]

Full fillable passport form with the ELSA/FPIC checklist, stakeholder map,
and fall-back hierarchy: `assets/templates.md` §1.

### Template 2: Circular-Economy Safety Gate (SafetyGateCard)

Required whenever material (sediment, treated water, biomass, soil
conditioner) crosses ecosystem boundaries:

#### Шлюз безопасности циркулярного каскада (Circular-Economy Safety Gate)

- Маршрут потока: [Узел-источник] -> [Технология переработки] ->
  [Узел-реципиент]
- Лабораторный контроль тяжелых металлов (As, Cd, Pb, Hg, Cr, Cu, Zn, Ni):
  [Подтверждено / НЕТ ДАННЫХ / Превышение] (HPI = ...)
- Контроль органических токсинов и цианотоксинов (микроцистины и др.):
  [Подтверждено / НЕТ ДАННЫХ / Превышение]
- Санитарно-микробиологический и фитопатогенный контроль: [Подтверждено /
  НЕТ ДАННЫХ / Превышение]
- Вердикт шлюза (Compliance Confirmed?): [YES — Допуск к внесению | NO —
  Блокировка потока, направление на безопасное изолированное хранение]

## Deterministic Script I/O Schemas

All scripts use only the Python standard library, read CSV (comma,
semicolon, or tab; decimal commas accepted) or JSON, print a JSON record,
and never edit their inputs (`scripts/registry.py` only appends to its
registry). Exit codes: 0 done or gate passed, 2 input error, 3 gate failed.
Run any of them with `--help`.

`scripts/trend_test.py` accepts both CSV time series and JSON payloads
(for `--mode trend` | `wpi` | `tsi` | `hpi` | `hq` | `drift`); the table
below gives the exact input and output of each script.

| Script | Input | Output |
|---|---|---|
| `scripts/qc_series.py` | CSV series (time + value columns); flags `--min` / `--max` / `--max-rate` / `--stuck-run` / `--max-gap-hours` | JSON summary: `rows`, `rows_flagged`, `rows_ok`, `flag_counts`, `gaps`, `neighbor`, `change_point`, `gate`; flagged rows written to `--out` CSV with a `qc_flag` column; values never edited |
| `scripts/trend_test.py` | CSV (time/value columns) or JSON `{"values": [float], "timestamps": [float or ISO], "alpha": 0.05}`; `--mode trend` (default) \| `wpi` \| `tsi` \| `hpi` \| `hq` \| `drift`; index modes take JSON | Trend (CSV): per-segment `S`, `var_S`, `Z`, `p_value`, `sen_slope_per_year`, `direction`. Trend (JSON): `s_stat`, `var_s_raw`, `hamed_rao_factor`, `z_corrected`, `p_value`, `theil_sen_slope`, `trend`: `"increasing"` \| `"decreasing"` \| `"no trend"`. `wpi`: `wpi`, `n`, `class`, `terms`. `tsi`: `tsi_sd`, `tsi_chl`, `tsi_tp`, `tsi_composite`, `class`. `hpi`: `hpi`, `critical`, `threshold` (100), `terms`. `hq`: `hi`, `hi_acute`, `hi_chronic`, `unsafe`, `threshold` (1), `terms`. `drift` (`--baseline <calibration.csv>`, `--drift-threshold` default 2.0): `drift_level`, `trend_fires`, `trigger`, `action` (`"recalibrate"` \| `"no action"`); exit 0 report, 2 input error |
| `scripts/skill_scores.py` | CSV; subcommands `continuous` (obs/sim columns + `--train-end`) / `events` / `brier` / `revalidate` (combined series + original `--train-end`) / `alert-trial` (kind/relevant rows: alerts + critical events) / `admit` (JSON dossier: variables + parameters with bounds) / `skill-horizon` (lead/obs/sim/naive rows: per-lead SS_RMSE + skill horizon) / `nudge` (recent obs/sim pairs + `--forecast`: bias-corrected forecast) | JSON metrics: `bias`, `pbias`, `mae`, `rmse`, `nse`, `kge`, `skill_vs_persistence`, `skill_vs_climatology`, `ss_rmse`, `ss_rmse_vs_climatology`; `admission_verdict`: `"ADMITTED"` \| `"REJECTED_BELOW_BENCHMARK"` (null for in-sample fits); `gate` pass/fail. `revalidate` adds a `revalidation` block (`status`, `transition`, `revoked`, `maturity_action`): SS_RMSE ≤ 0 on the new hold-out revokes ADMITTED (exit 3) and drops the maturity label. `alert-trial` reports `precision`, `miss_rate`, `alarm_volume`, `verdict` (PASS/FAIL/INCONCLUSIVE_QUIET_WINDOW; a window with no alerts and no critical events is INCONCLUSIVE_QUIET_WINDOW — it neither admits nor rejects, and admission waits for a synthetic stress-test or a historical extreme replay). `admit` reports `verdict` (ADMITTED/REJECTED) with the offending PRIMARY variable or parameter named; SS_RMSE > 0 is required only for primary variables (flagged `primary` in the dossier; when no variable carries the flag, every variable is primary). `skill-horizon` reports `per_lead` (SS_RMSE per lead) and `skill_horizon` (longest lead beating persistence, null when the shortest lead fails). `nudge` reports `mean_residual`, `raw_forecast`, `nudged_forecast` |
| `scripts/sensitivity_screen.py` | Python model file defining `run(params: dict) -> float` + params JSON (`{"parameters": [{"name", "value", "perturb" (fraction in (0, 1)) \| "range": [lo, hi]}]}`); `--metric` (default `output`), `--out` | JSON: `metric`, `baseline` (output at the declared values), per-parameter `value`, `perturbed_values`, `outputs`, `abs_change`, `rel_change` (null when the baseline is 0), `rank` (by relative change; baseline-0 rows rank by absolute change below the ranked ones); `rule` (calibrate only the influential parameters) and `limit` (one-at-a-time misses interactions, unlike Sobol indices); exit 0, 2 input error |
| `scripts/alert_bands.py` | CSV series + `--amber` / `--red` bands, `--anchor`, `--window-hours`; `--explained-by <driver.csv>` + `--driver-amber` / `--driver-red` (a breach the driver explains is logged, not alerted); `--class-thresholds FILE` (CSV class, limit) maps the latest value and the episode peak to one verdict per decision-maker class | JSON: `indicator`, `status`, `observations_used`, `observations_ignored`, `alerts` (band, observed extreme, start, end, elapsed hours, anchor, recommended check), `explained_breaches` (with the driver episode that explains them), `class_thresholds` (limit, latest/peak within, `can_operate`), `unsustained_breaches` |
| `scripts/generalize_coords.py` | CSV occurrences + sensitivity category | Generalized CSV (coordinates rounded, `footprintWKT`, locality fields blanked); `--check` prints a JSON verdict |
| `scripts/registry.py` | Subcommands `issue` / `resolve` / `replay` / `promote` / `verify` / `score` on a JSONL registry; `issue` accepts `--cadence daily` \| `weekly` \| `seasonal` \| `event-driven` and `--lead-time` (value) with `--lead-time-unit hours` \| `days` \| `weeks` (default `days`); `--clearance "asset:threshold,..."` records per-asset clearance (threshold − forecast value); `promote` records a signed promotion (promoted by, on, evidence) moving a model from exploratory to operational | JSON records with a SHA-256 hash chain (`prev_hash`, `hash`); `verify` exits 3 on any tampering or any invalid `cadence` / `lead_time` / `clearance` value |
| `scripts/forecast_bulletin.py` | Registry JSONL (`--registry`) + forecast id (`--id`) + observations CSV (time, value columns; decimal commas accepted) + optional `--amber` / `--red` bands (e.g. `>=25`) | One-page dated Markdown bulletin (stdout or `--output` file): observed value today, forecast value with interval, watch status of the latest observation and the forecast, the scoring date (horizon end) and the verification metric; exit 0 when written, 2 on input error (missing file, unknown forecast id, a record that is not a forecast, missing time/value columns, no observations, an unparsable band, bands pointing different ways, or a red band inside the amber band) |
| `scripts/drift.py` | Release points CSV (`id`, `lat`, `lon`) + current field CSV (`time`, `u`, `v` in m/s) + target zones CSV (`zone`, `lat_min`, `lat_max`, `lon_min`, `lon_max`); `--step-hours` / `--max-hours` / `--leeway` / `--wind-u` / `--wind-v` | JSON: per zone `arrivals`, `connectivity` (fraction of released particles arriving), `median_travel_hours` (null when none arrives); per particle `arrived_zone` and `travel_hours` (null when it never arrives) |
| `scripts/scenario_generate.py` | Driver series CSV (time + value columns); `--n` seeded series, `--seed`, `--out` (required), `--watch` (band spec, e.g. `>=25`) | CSV of N+1 columns (input + N scenario draws, every value labelled a scenario draw) + JSON summary: fitted mean, SD, lag-1 autocorrelation, seed, breach share with `--watch` |
| `scripts/diversity.py` | Subcommands `indices` (counts CSV: species, count; `--taxonomy` CSV: species, genus, family, order, class, phylum) / `pft` (cover/count CSV: species, cover; `--pft-table` CSV: species, pft, pathway, source) | JSON: `richness`, `total`, `shannon`, `pielou`, `delta_plus` (null with fewer than two taxa with taxonomy), `per_species`; `pft` reports `shares_by_pft` and `shares_by_pathway` |
| `scripts/trait_match.py` | Trait table CSV (taxon + trait columns: numeric, or "x" for indifferent) + `--conditions` JSON ({trait: {mode `at_least` \\| `within`, value, window?}}) | JSON: `fits` (taxa meeting every condition), `fails` (taxon + the failed conditions with values on both sides), `indifferent` (taxa not excluded by a condition on a trait the source marks "x") |
| `scripts/build_manifest.py` | Build-index JSON (`name`, `datasets`, `models`, `steps`, `outputs`, `mappings`; optional `doi`) | `ro-crate-metadata.json` (RO-Crate 1.1) with FAIR Signposting entries (`cite-as` / `describedby` / `license`) on the Root Dataset + one MappingSet File per `mappings.csv` + validation report |
| `scripts/evidence_search.py` | Query string; `--limit` | Normalized JSON records from PubMed, Europe PMC, OpenAlex, Crossref |
| `scripts/uncertainty_budget.py` | CSV ensemble (`output`, `source`, `member`, `value`) | JSON budget: variance, standard deviation, and share per source; median + percentile interval from the joint ensemble only. Subcommand `sampling-priority` (targets CSV: target + model/naive or model_a/model_b) ranks the next sampling targets by \|model − naive\| descending and names the top target to sample next |
| `scripts/mismatch.py` | Two CSVs (`--observed`, `--modeled`: `cell`, `value` 0/1, the same cell set); with `--register FILE`, `--id`, `--cause` and `--confirm-measurement` are required (the cause may be the literal `[НЕТ ДАННЫХ]`) | JSON: `n_cells`, `n_observed`, `n_modeled`, `extent` (fraction of observed positives correctly predicted; null when no observed positives), `hits`, `misses`, `false_alarms`, `rule`; with `--register`, the entry is appended to the JSON-lines register; exit 0, 2 input error (differing cell sets, a value other than 0/1, an empty table, a missing register field) |

## Multi-Agent Governance

Scale agent orchestration to task complexity while preserving security and
provenance (see `references/orchestration.md` for full role contracts and
execution isolation rules): Roles: Orchestrator, Data Collection Agent,
Literature & Standards Agent, Modeler, Calibration Auditor, and Independent
Red Team. Execution Isolation: Only the designated deterministic runner
executes Python scripts in `scripts/`; external/council models receive
anonymized summaries without raw sensitive client data.

## Companion Documents

- `references/quick-start.md` — the ten-step Tier S path for a first build.
- `assets/templates.md` — the twelve fillable forms (object passport with
  ELSA/FPIC checklist, risk register row, trigger–action–response plan,
  option card, scenario card, forecast registry entry, focus application,
  what-if scenario, forecast bulletin, public status line, decision product,
  mismatch register entry).
- `references/indicators.md` — the 19-section tiered indicator catalogue.
- `references/analytics-forecasting.md` — history rescue, pattern memo,
  event catalogue, predictability audit.
- `references/uncertainty-decision.md` — uncertainty method ladders,
  value-of-information cycle, counterfactual twin protocol.
- `references/calibration-bounds.md` — declared physical ranges for fitted
  parameters (the plausibility gate: a fit outside its bounds is rejected
  even when it beats the benchmark).
- `references/scenarios.md`, `references/data-sources.md`,
  `references/evidence-sources.md`, `references/world-practice.md` —
  scenario families, open-data routing, literature routing, surveyed world
  practice.
- `examples/lake-example.md`, `examples/open-series-demo.md`,
  `examples/beira/` — worked examples.
- `examples/gallery.md` — prototype gallery: one working twin per task
  type (pond, river, field, air, biodiversity,
  wetland, forest-fire, forest-logging, forest-carbon), each a small data
  file + runner + README.

## Citation

Baldanova, R. (2026). Ecosystem Digital Twin — Agent Skill (Version 2.7).
https://github.com/Rigjite/Ecosystem-Digital-Twin
