---
name: ecosystem-digital-twin
description: "An Agent Skill for designing and operating evidence-bound digital twins and linked twin networks of ecosystems (ponds, lakes, rivers, agricultural land, air basins, and biodiversity sites). Guides the 7-stage build cycle (Phases 0–6), enforces strict separation between AI agents and deterministic code, implements counterfactual baselines, safety gates for circular-economy cascades, Value of Information (VoI) assessment, and RO-Crate provenance. Use when modeling an ecosystem, linking multi-ecosystem cascades, analyzing monitoring data, or evaluating environmental and agricultural intervention scenarios."
license: CC-BY-4.0
compatibility: "Bundled scripts need only Python 3.9+ and its standard library. scripts/evidence_search.py needs network access to PubMed, Europe PMC, OpenAlex, and Crossref. Open data (Copernicus Sentinel, Landsat, GBIF, ERA5, SoilGrids, national hydrology and meteo services) is fetched at build time with whatever access the environment has; GIS tooling (QGIS, geopandas) is optional."
metadata:
  version: "2.3"
  skill-author: Rigjita Baldanova
  last-reviewed: "2026-10-25"
---

# Ecosystem Digital Twin — Agent Skill (v2.3)

An Agent Skill for designing and operating evidence-bound digital twins and
networks of linked digital twins across aquatic ecosystems (lakes, ponds,
river basins), agroecosystems (crop fields, smart farming, livestock),
contaminated soils, air basins, and biodiversity conservation sites. A twin
built with this skill is a living, observation-synchronized model of a real
object (or a conceptual pre-project in silico proposal explicitly labeled as
such). It diagnoses current states, warns early of non-linear shifts, and
evaluates environmental and economic interventions against a counterfactual
baseline before physical implementation. Current version: 2.3 (2026-10-25).
License: CC BY 4.0.

## Non-Negotiables (Strict Rules)

1. **No Fabricated Data & Deterministic Compute Isolation:** Every numerical
   value MUST trace to a verified source (with date, method, and resolution)
   or be computed by deterministic code (`scripts/`). Language models and AI
   agents NEVER invent or manually calculate numbers. Missing parameters MUST
   be stated explicitly as data gaps ([НЕТ ДАННЫХ]).
2. **Explicit Maturity Labeling:** Uncalibrated or conceptual models MUST be
   labeled in writing as a Prototype or Conceptual Proposal — never shipped
   as an operational twin.
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

- **Stage 1 — Object Passport (Phase 0):** Before any calculation, lock
  spatial boundaries, the core management question, regulatory thresholds
  (e.g. WHO, national ambient water/soil standards), maturity level, and
  trophic/pollution indices (WPI, Carlson TSI, HPI, OECD thresholds).
- **Stage 2 — Data Inventory & QC (Phase 1):** Aggregate satellite remote
  sensing (e.g. Sentinel-2 water transparency/SDD), in-situ hydrochemical /
  soil samples, and literature baselines. Screen time series with
  deterministic quality control (`scripts/qc_series.py`). Never interpolate
  across gaps silently.
- **Stage 3 — Model & Calibration Against Benchmark (Phase 2–3):** Formulate
  the mathematical or conceptual state model (`scripts/trend_test.py` with
  Hamed–Rao autocorrelation correction). An operational model is admitted to
  forecasting ONLY if it outperforms a naive inertial benchmark on a held-out
  sample (`scripts/skill_scores.py`). Where sediment/soil exchange
  parameters are unmeasured, evaluate sensitivity across a parameter ensemble
  or explicitly limit the scope to directional scenario comparison.
- **Stage 4 — "What-If" Scenarios vs. "No-Action" (Phase 5):** Compare
  single interventions (e.g. one-off sediment dredging vs. catchment inflow
  interception/wetlands) and combined strategies across short- and
  long-term horizons (e.g. 5, 10, 50 years). Highlight delayed responses and
  the decay of one-off measures when external loading persists.
- **Stage 5 — Independent Red-Team Review:** Audit the twin for post-hoc
  threshold selection, unverified commercial claims, author↔employer data
  loops, and hidden assumptions (e.g. incomplete inflow capture by wetlands
  or unmeasured sediment cores vs. surface water samples).
- **Stage 6 — Human Decision:** Translate complex biogeochemical and
  physical-chemical processes into clear environmental and agricultural
  economic metrics. Final authority to approve interventions or investment
  proposals rests strictly with the human specialist.
- **Stage 7 — Monitoring & Twin Updating (Phase 4 & 6):** Assimilate new
  observations to reject incompatible ensemble members and narrow forecast
  uncertainty, recompute alert bands (`scripts/alert_bands.py`), and update
  all linked nodes.
  Package deliverables with an append-only hash-chain forecast registry
  (`scripts/registry.py`) and RO-Crate 1.1 provenance manifest
  (`scripts/build_manifest.py`).

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

## Mandatory Deliverable Templates

### Template 1: Stage 1 — Object Passport (ObjectPassport)

Every twin workflow MUST open with this structured table:

#### Паспорт цифрового двойника (Stage 1 — Object Passport)

- Объект и пространственные границы: [Название, координаты (обобщенные до
  0.1° при наличии редких видов), площадь/объем, водосбор]
- Статус зрелости (Maturity Label): [Prototype | Descriptive | Informative
  | Predictive | Decision] — the skill's own 5-level ladder; the twin is
  described to the client by its level, never above it.
- Ключевой управленческий вопрос: [Целевая задача, горизонт моделирования:
  5 / 10 / 50 лет]
- Нормативная база и пороги: [WHO / ПДК / региональные стандарты, целевые
  индексы WPI, TSI, HPI]
- Связанные узлы (Linked Nodes): [Входной узел -> Текущий двойник ->
  Выходной узел / Нет]
- Реестр пробелов данных ([НЕТ ДАННЫХ]): [Явный список неизмеренных
  параметров]

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
(for `--mode trend` | `wpi` | `tsi` | `hpi`); the table below gives the
exact input and output of each script.

| Script | Input | Output |
|---|---|---|
| `scripts/qc_series.py` | CSV series (time + value columns); flags `--min` / `--max` / `--max-rate` / `--stuck-run` / `--max-gap-hours` | JSON summary: `rows`, `rows_flagged`, `rows_ok`, `flag_counts`, `gaps`, `neighbor`, `change_point`, `gate`; flagged rows written to `--out` CSV with a `qc_flag` column; values never edited |
| `scripts/trend_test.py` | CSV (time/value columns) or JSON `{"values": [float], "timestamps": [float or ISO], "alpha": 0.05}`; `--mode trend` (default) \| `wpi` \| `tsi` \| `hpi`; index modes take JSON | Trend (CSV): per-segment `S`, `var_S`, `Z`, `p_value`, `sen_slope_per_year`, `direction`. Trend (JSON): `s_stat`, `var_s_raw`, `hamed_rao_factor`, `z_corrected`, `p_value`, `theil_sen_slope`, `trend`: `"increasing"` \| `"decreasing"` \| `"no trend"`. `wpi`: `wpi`, `n`, `class`, `terms`. `tsi`: `tsi_sd`, `tsi_chl`, `tsi_tp`, `tsi_composite`, `class`. `hpi`: `hpi`, `critical`, `threshold` (100), `terms` |
| `scripts/skill_scores.py` | CSV; subcommands `continuous` (obs/sim columns + `--train-end`) / `events` / `brier` | JSON metrics: `bias`, `pbias`, `mae`, `rmse`, `nse`, `kge`, `skill_vs_persistence`, `skill_vs_climatology`, `ss_rmse`, `ss_rmse_vs_climatology`; `admission_verdict`: `"ADMITTED"` \| `"REJECTED_BELOW_BENCHMARK"` (null for in-sample fits); `gate` pass/fail |
| `scripts/alert_bands.py` | CSV series + `--amber` / `--red` bands, `--anchor`, `--window-hours` | JSON: `indicator`, `status`, `observations_used`, `observations_ignored`, `alerts` (band, observed extreme, start, end, elapsed hours, anchor, recommended check), `unsustained_breaches` |
| `scripts/generalize_coords.py` | CSV occurrences + sensitivity category | Generalized CSV (coordinates rounded, `footprintWKT`, locality fields blanked); `--check` prints a JSON verdict |
| `scripts/registry.py` | Subcommands `issue` / `resolve` / `verify` / `score` on a JSONL registry | JSON records with a SHA-256 hash chain (`prev_hash`, `hash`); `verify` exits 3 on any tampering |
| `scripts/build_manifest.py` | Build-index JSON (`name`, `datasets`, `models`, `steps`, `outputs`) | `ro-crate-metadata.json` (RO-Crate 1.1) + validation report |
| `scripts/evidence_search.py` | Query string; `--limit` | Normalized JSON records from PubMed, Europe PMC, OpenAlex, Crossref |
| `scripts/uncertainty_budget.py` | CSV ensemble (`output`, `source`, `member`, `value`) | JSON budget: variance, standard deviation, and share per source; median + percentile interval from the joint ensemble only |

## Multi-Agent Governance

Scale agent orchestration to task complexity while preserving security and
provenance (see `references/orchestration.md` for full role contracts and
execution isolation rules): Roles: Orchestrator, Data Collection Agent,
Literature & Standards Agent, Modeler, Calibration Auditor, and Independent
Red Team. Execution Isolation: Only the designated deterministic runner
executes Python scripts in `scripts/`; external/council models receive
anonymized summaries without raw sensitive client data.

## Companion Documents (retained from v2.2)

- `references/quick-start.md` — the ten-step Tier S path for a first build.
- `assets/templates.md` — the five fillable forms (object passport with
  ELSA/FPIC checklist, risk register row, trigger–action–response plan,
  option card, forecast registry entry).
- `references/indicators.md` — the 19-section tiered indicator catalogue.
- `references/analytics-forecasting.md` — history rescue, pattern memo,
  event catalogue, predictability audit.
- `references/uncertainty-decision.md` — uncertainty method ladders,
  value-of-information cycle, counterfactual twin protocol.
- `references/scenarios.md`, `references/data-sources.md`,
  `references/evidence-sources.md`, `references/world-practice.md` —
  scenario families, open-data routing, literature routing, surveyed world
  practice.
- `examples/lake-example.md`, `examples/open-series-demo.md`,
  `examples/beira/` — worked examples.

## Citation

Baldanova, R. (2026). Ecosystem Digital Twin — Agent Skill (Version 2.3).
https://github.com/Rigjite/Ecosystem-Digital-Twin
