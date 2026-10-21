---
name: ecosystem-digital-twin
description: "Designs, builds, audits, and reports digital twins of ecosystems: farmland, ponds and lakes, river reaches, air basins, and flora/fauna conservation sites. Full cycle, with scripts for the calculations: object scoping, open-first data inventory, data quality gate, state model, calibration against observations and naive baselines, monitoring with alert bands, trend and event analytics, pre-registered forecasts, preventive action plans, and scenario modeling for ecosystem improvement. Use when the user wants an ecosystem or environmental digital twin; a water-quality, algal-bloom, hypoxia, or low-flow early-warning system; a monitoring and forecasting design for a lake, river, farm, air basin, or protected area; or an audit of such a twin or of a vendor's claims about one. Also for requests in Russian (цифровой двойник экосистемы, водоёма или поля; мониторинг и прогноз качества воды)."
license: CC-BY-4.0
compatibility: "Bundled scripts need only Python 3.9+ and its standard library. scripts/evidence_search.py needs network access to PubMed, Europe PMC, OpenAlex, and Crossref. Open data (Copernicus Sentinel, Landsat, GBIF, ERA5, SoilGrids, national hydrology and meteo services) is fetched at build time with whatever access the environment has; GIS tooling (QGIS, geopandas) is optional."
metadata:
  version: "2.0"
  skill-author: Rigjita Baldanova
  last-reviewed: "2026-10-21"
---

# Ecosystem Digital Twin

## Purpose

A digital twin of an ecosystem is a living, evidence-bound model of a real place:
it mirrors the system's current state, warns early when the state degrades, and
tests interventions in the model before anyone touches the real system.

Two uses, in this order:

1. **Consulting product** — a twin designed and delivered for a client (a farm, a
   water body manager, a conservation project, a municipality).
2. **Research instrument** — the same build used for the operator's own science.

Domains: agricultural land; ponds and lakes; river reaches; air basins;
flora and fauna conservation sites.

## Non-negotiables

- **No fabricated data.** Every indicator value traces to a source — dataset,
  sensor, or field record — with date, method, and resolution. A missing value is
  a stated gap, never a plausible number.
- **A twin is a hypothesis, not a photograph.** State uncertainty with every
  output. A scenario result is a comparison between options, not a prophecy.
- **Improvement orientation.** Scenarios are judged by ecosystem outcomes —
  water quality, soil health, air quality, biodiversity — never by a single
  production metric alone.
- **Conservation safeguard.** Precise locations of rare or endangered species
  are never published and never leave the client's boundary (poaching and
  disturbance risk). Sensitivity follows IUCN and national red lists and CITES
  appendices. Generalize by GBIF sensitivity category (Chapman 2020): extreme —
  withhold coordinates (or 1° at most); high — 0.1° (~11 km). This skill's
  floor for any listed species is 0.1°, even where GBIF allows 0.01° or
  0.001°. Blank locality and verbatim fields that can re-identify the site.
  `scripts/generalize_coords.py` applies the rule; its `--check` mode must
  pass on every file that leaves the client boundary.
- **Open first.** Exhaust open data before asking the client for anything.
  Client and sensor data extend the twin; they are not its entry ticket.
- **No uncalibrated twin ships as a twin.** A build that has not been checked
  against observations is labeled a prototype, in writing, in the deliverable.
- **The client's data stays the client's.** Farm, sensor, and site data are
  governed by the client's terms (the farm-data-space principle, as in the EU
  Code of Conduct on agricultural data sharing); the passport states ownership,
  access, and what may be reused. Nothing is published or folded into another
  project without written consent.

World practice this skill builds on — Destination Earth, BioDT, the EU
Digital Twin of the Ocean, Delft-FEWS, and Wageningen farm twins — is
surveyed in `references/world-practice.md`, with what was adapted and why.

## Start here

New to a build? Do not read the whole package first. Follow
`references/quick-start.md` — the ten-step path for a first or small (Tier S)
build. Fill the five forms in `assets/templates.md` as you go (object passport,
risk register, trigger–action–response plan, option card, forecast registry
entry), and keep `examples/lake-example.md` beside you: one small lake carried
through every form. Run the bundled scripts (see **Scripts**) for every
calculation the phases require instead of re-deriving formulas by hand: they
enforce the rules below and leave an auditable JSON record.

## Workflow

### Phase 0 — Object passport and decision framing

Record: object type and boundaries (coordinates, watershed, field, or basin);
the client or research owner; the decision the twin must support; the time
horizon; the update cadence the decision needs.

Declare the target **maturity level** in the passport; the twin is described
to the client by its level, never above it:

1. **Prototype** — assembled, not yet calibrated against observations.
2. **Descriptive** — mirrors current and past state from data.
3. **Informative** — monitored state with alert thresholds and data gaps
   made visible.
4. **Predictive** — calibrated forecasts with verified skill scores.
5. **Decision** — scenario results demonstrably used in the owner's actual
   decisions, with outcomes reviewed.

The level states what the whole twin has earned. Levels 2–3 make no
predictive claims the owner may act on. A level-3 twin may register **trial
forecasts** from a component that passed Phase 3 — that is how level 4 is
earned — labeled "trial" wherever they appear, with no decision weight until
their verification record exists. Every forecast or scenario number comes
from a component that passed Phase 3; a scenario effect taken from published
effect sizes instead is labeled evidence-based, with its transferability check.

Record also the stakeholder map (who decides, who is affected, who owns each
data stream) and an ethical-legal-societal (ELSA) check: data ownership and
consent; sensor placement permissions; who may be harmed by a wrong alert;
landowner consent under local law; and the free, prior and informed consent
(FPIC) of Indigenous communities where law and international standards
require it — and as good practice wherever their territories or knowledge
are involved. FPIC is a checklist step, not a phrase: identify the
rights-holders, document the consent or the legal basis relied on, and
record the outcome before data collection starts. Record personal data that
imagery or sensors may capture (minimize it; privacy law governs) and any
conflict of interest, including a client who prefers a particular scenario
outcome. Scoring criteria and weights are fixed, and the fixing recorded,
before scenario results are seen.

Decision point: if no decision can be named, the build is monitoring-only.
Say so in the passport — a monitoring build is a legitimate product, but it is
not sold or described as a decision twin.

### Phase 1 — Data inventory, open first

Build the source matrix for this object from `references/data-sources.md`:
satellite imagery, species occurrence records, reanalysis and meteo series,
hydrology gauges, soil maps — then client sensors, field logs, and prior
studies. For each source record coverage, resolution, cadence, and known gaps.

**Evidence inventory (in parallel).** Run the literature layer from
`references/evidence-sources.md` alongside the data inventory: prior studies
of this object and its analogues, published monitoring programs, and the
evidence behind candidate indicators, thresholds, and methods. Literature
justifies choices; it never substitutes for observations of the object.
`scripts/evidence_search.py` queries PubMed, Europe PMC, OpenAlex, and
Crossref and returns normalized records for screening.

**Historical data rescue.** Before any variable is declared unmeasured,
search for its history (archives, yearbooks, remote-sensing archives back to
1984, museum records, proxies, consented local knowledge —
`references/analytics-forecasting.md` §1), harmonize it, and log every break
in a bias and breaks register. No history → the passport says so, and
pattern and forecast claims for that variable are limited accordingly.

**Data quality gate (before any modeling).** Every incoming series passes
`scripts/qc_series.py`: range, rate-of-change, stuck-sensor, duplicate-time,
and gap checks, a neighbor-station consistency check where a second station
exists, and a Pettitt change-point test. Failures are flagged and
quarantined, never silently cleaned — the script never edits values. A
significant change point is explained in the bias and breaks register
before any trend is computed across it. Gaps are handled by a declared
protocol (interpolation, model estimate, or left open), and the protocol's
choice is visible in every downstream output it touches.

**Fall-back hierarchy.** For every core variable name a primary source and at
least one fall-back (an alternative dataset, a neighboring station, a modeled
estimate labeled as such). Continuity of monitoring must not depend on a
single feed.

Exit criterion: the candidate state-variable list is drafted, and every
variable on it has at least one source in the matrix or is explicitly listed
as unmeasured. Respect source licenses from the start: Sentinel data is
acknowledged to Copernicus, other products carry their own terms (verify per
product), and GBIF downloads are cited by their DOI in the provenance log.

### Phase 2 — State model

Choose state variables and indicators per domain from
`references/indicators.md`. Start from the domain quick set there, include the
core indicators for every medium present, then add conditional panels only
where a pressure, exposure pathway, legal duty, or decision triggers them.
The catalogue is tiered, not a promise to measure everything: conditional
panels not selected are justified in the passport by the absence of their
trigger, and selected indicators that cannot yet be measured stay on the list
as named data gaps. Structure the model as drivers → state → impacts.

Keep the twin's three layers separate, as the operational ocean and Earth
twins do: **(1) monitoring** — the state as observed; **(2) forecast** — the
state as projected; **(3) impact simulation** — what the projected state means
for decisions and ecosystem outcomes. A deliverable never blends numbers from
different layers without labeling them.

Build from replaceable modules — data connectors, model components, indicator
calculators — so one can be upgraded without rebuilding the twin. Where both
exist, prefer **hybrid models**: a process model for mechanism plus a
statistical or ML component for the residuals, each checking the other.

Start simple: index models, balance models, and statistical baselines first.
Add process complexity (hydrodynamic, biogeochemical, dispersion) only where
the data inventory can feed and check it. A complex model on thin data is a
defect, not an achievement.

Exit criterion: every state variable has a named layer (monitoring,
forecast, or impact), a model component, and an uncertainty statement.

### Phase 3 — Calibration and validation

Hindcast the model against observations it did not train on. Declare the
split before fitting — a held-out period or cross-validation folds — and
never tune on the data used to score. Declare failure thresholds before
fitting too (e.g. NSE below 0.5 for monthly flows, or any score at or below a
naive baseline) and record them with the calibration report: a calibration
is failed by its declared thresholds, not by feel.

Score with `scripts/skill_scores.py continuous`: bias, PBIAS, MAE, RMSE,
NSE, KGE, and skill against persistence and a training-period climatology.
It refuses to score without a declared hold-out and fails the gate when a
declared threshold is missed or a naive baseline is not beaten: a twin that
cannot beat the baseline has no forecast skill, and says so.

Where no historical observations exist, calibration is impossible by
definition: the build remains a prototype, verification is qualitative only
(expert review of plausibility and internal consistency), and the
deliverable says so in place of any skill score. Report the periods and
conditions where the model fails, and what would improve it. A failed
calibration narrows the twin's claims — record the narrowing rather than
tuning silently.

Event forecasts are validated as events, not only as continuous series:
`scripts/skill_scores.py events` (probability of detection, false-alarm
ratio, critical success index, frequency bias, lead-time distribution) and
`brier` (Brier score, skill against climatology, reliability table). With
fewer than about five observed events, the scores are descriptive counts,
not a track record — the script says so, and the product is a watch
(`references/analytics-forecasting.md`). A forecast without hindcast event
scores is a prototype output and is labeled as such wherever it appears.

**Quantitative uncertainty.** Headline outputs carry computed uncertainty,
not adjectives (`references/uncertainty-decision.md`): Monte Carlo or
ensemble propagation as the default, Bayesian calibration where the data
support it, and a global sensitivity analysis naming the inputs that drive
each headline result. Every headline output ships with an uncertainty
budget separating measurement, forcing, parameter, structural, and
scenario contributions — `scripts/uncertainty_budget.py` computes it from
one-at-a-time and joint ensembles, and reports an interval only from a
joint ensemble. A number whose uncertainty cannot yet be computed is
published with the reason — never with a decorative interval.

### Phase 4 — Monitoring, assimilation, and verification

For each core indicator set green / amber / red bands, anchored to a regulation,
a standard, or the object's own baseline statistics — the anchor is named in
the passport. An alert requires a breach sustained over a defined window, not a
single spike. Set the window per indicator dynamics — hours to a day for
dissolved oxygen and air-pollution episodes; days to weeks for chlorophyll
and vegetation anomalies — and record it with the band. Alert output states:
indicator, observed value, band breached, duration (window start timestamp
plus elapsed time), likely drivers, and the recommended human check.
`scripts/alert_bands.py` evaluates a series this way: it refuses bands
without an anchor, ignores values the quality gate marked invalid but keeps
suspect ones (a real crash can look like a rate jump) and says so, and ends
an episode at an observation gap rather than assuming the breach persisted.

**Assimilation cycle — what makes it a twin rather than a model.** Every new
observation batch (a) updates the twin's state, and (b) is scored against what
the twin forecast for that moment, in the manner of numerical weather
prediction, at whatever cadence the data allows. Method follows data density:
error correction or nudging for sparse series; Ensemble Kalman or particle
filtering where sensor density and model structure support them. Working
heuristic: nudging suits series whose gaps exceed the system's response time;
ensemble methods need observations at least as frequent as the fastest
dynamic being corrected, plus an ensemble the operator can actually run — if
either fails, downgrade the method, never the honesty. Name the method in the
passport.

**Standing verification.** Forecasts are registered before their outcomes are
knowable with `scripts/registry.py issue` — an append-only, hash-chained
registry holding forecast ID, issue time (the clock at registration, never
back-dated), horizon, value or probability with its interval and the method
that computed it, model version, input manifest IDs, and the declared
metric. `registry.py score` scores forecasts exactly as issued — superseded
ones included, overdue ones listed — and `verify` proves no record was
edited; anchor the latest hash outside the build (a commit or an email to the
owner) to prove when it was written. A forecast that was never registered
earns no verification credit. The current verification score per indicator is
part of every client report: a falling score triggers recalibration or an
honest narrowing of claims — and, at review points, an assessment of decision
value: did the twin's guidance change a real decision, and did the outcome
improve? A twin can be accurate and useless; only the second check catches
that.

**Risk register and preventive action.** Keep the object's risk register,
review it every verification cycle, and scan for emerging risks at least
annually. Every material risk with an actionable lead time carries a
trigger–action–response plan (TARP) agreed before the season — trigger from
the alert bands, measure, owner, needed lead time, side effects, stand-down
criteria (`references/analytics-forecasting.md` §5–6).

**Value of information.** Each verification cycle ranks the next
measurements by expected reduction in decision uncertainty per unit cost
(from the sensitivity rankings and budgets) and adapts sampling; when further
measurement costs more than it teaches, the plan says so and stops growing
the network (`references/uncertainty-decision.md` §2).

### Phase 5 — Scenario modeling for improvement

Build scenarios from `references/scenarios.md`: load reductions, buffer and
restoration measures, land-use changes, emission cuts, water-regime changes.
Run each against the calibrated baseline twin. Score every scenario on
ecosystem outcomes (domain indicators), cost, implementation risk, and time
to effect — weights agreed with the client and recorded before the runs,
never chosen after results are known. Recommend one, with its trade-offs.
Never optimize silently for yield, discharge convenience, or any single
metric.

Draw the option portfolio from the risk register and the pattern memo —
prevent → mitigate → restore → adapt → monitor — with no-regret and
low-regret options first, and present each as an option card: expected
effect with its evidence, time to effect, cost, reversibility, residual
risk, and the monitoring indicator and review date that will prove or
disprove the effect. When a measure is implemented, freeze the no-action
baseline twin as the counterfactual and run both twins on the same observed
forcings: the reported effect is the difference, with its uncertainty, and
any later model improvement re-runs both twins with the change disclosed
(`references/uncertainty-decision.md`).

**Nature-based solutions are evaluated first.** In every scenario round, the
nature-based options (restoration, buffers, corridors, rewetting, green
infrastructure), where they exist for the problem, are modeled before
engineered ones. If none is modeled, the reason (no applicable NBS, no data
to model it, client-excluded with the exclusion recorded) is written into
the passport — skipping NBS silently is a defect, skipping it on the record
is a decision. If the recommendation favors an engineered option over an
available nature-based one, the deliverable states why: the burden of
justification sits on the engineered option.

### Phase 6 — Deliverable and handover

The client deliverable contains: object passport (with maturity level);
current state with evidence and provenance per indicator; calibration
report; monitoring bands, alert rules, and current verification scores;
scenario comparison and the recommendation; uncertainty and data gaps;
update cadence and the owner's maintenance duties. Research use adds the
full provenance log and model configuration to the project archive.

**Provenance package.** The deliverable ships as an RO-Crate 1.1 package, not
a loose report: `ro-crate-metadata.json` at the root with the metadata
descriptor, the root dataset (name, description, datePublished, license), a
data entity per dataset (retrieval date as `sdDatePublished` for web data),
a SoftwareApplication per model component with its version, and a
CreateAction per workflow step linking inputs, model, and results. Each
headline number is a PropertyValue result of the action that produced it, so
its evidence chain is machine-traceable. Write the build index in the shape
below and let `scripts/build_manifest.py` validate it and emit the crate:

```json
{ "name": "...", "description": "...", "license": "https://...",
  "datasets": [{"id": "ds-01", "name": "...", "url": "https://...", "version": "...", "retrieved": "YYYY-MM-DD"}],
  "models":   [{"id": "m-01", "name": "...", "version": "..."}],
  "steps":    [{"id": "st-01", "name": "...", "instrument": "m-01", "inputs": ["ds-01"], "parameters": "..."}],
  "outputs":  [{"id": "out-01", "name": "...", "value": 0.0, "unit": "...", "produced_by": "st-01"}] }
```

Every headline number in the report carries its output ID in brackets, e.g.
`[out-01]`; `build_manifest.py --report report.md --registry reg.jsonl`
fails the build when a headline output is not cited, a cited ID does not
exist, an output has no evidence chain, the forecast registry does not
verify, or a registered forecast cites an input outside the package. Any result can then be re-traced and re-run by the client or a
reviewer — trust is a property of the package, not of the author.

**Nesting.** Build outputs in open formats so a local twin can feed a
regional or national system (a farm into a catchment twin, a lake into a
basin program) without rework. Use the domain standards in
`references/data-sources.md` — SensorThings for sensor exchange, WaterML 2.0
for hydrology series, Darwin Core for occurrences, EML for ecological and
forecast metadata, STAC for imagery, CF for gridded data — and record the
choices and any deviation in the passport. A twin designed as a dead end is a
design defect at this skill's standard.

## Orchestration, multi-agent work, and red team

Builds run at one of three tiers, chosen in Phase 0 and recorded in the
passport (full protocol: `references/orchestration.md`): **Tier S** — one
operator, one independent red-team pass before delivery (default); **Tier M**
— an orchestrator with data scout, evidence scout, domain modeler, and a
calibration auditor independent of the modeler, red team at calibration and
delivery; **Tier L** — Tier M plus a council of distinct expert personas for
regulatory, health, large-money, or contested builds, red team at all gates.

The orchestrator owns the passport, task contracts, and conflict resolution
(by the evidence hierarchy, never by vote) and is the single client-facing
voice. Phase 0 framing and the Phase 5 recommendation sign-off stay with the
owner, never with agents. The **red team** attacks the build at the design,
calibration, and delivery gates (indicator theater, threshold smuggling,
tuning on scoring data, metric shopping, weights moved after results, claims
above the maturity level), independent of the builders it attacks. Every
attack is recorded with severity and disposition; an unresolved critical
attack blocks delivery, and the red-team pass is the last element cut from a
budget.

## Analytics, uncertainty, and the counterfactual

`references/analytics-forecasting.md` runs across Phases 1–5: history rescue
with a bias and breaks register; the pattern memo (trends via
`scripts/trend_test.py` — Mann–Kendall with Sen's slope per segment between
registered breaks, seasonal Kendall for monthly water-quality data,
autocorrelation handled or stated); the event catalogue; the predictability
audit; and the risk register → TARP → option card loop.
`references/uncertainty-decision.md` holds the method ladders for computed
uncertainty, value of information, the forecast registry, and the
counterfactual twin. Where no historical data exist, none of this is
simulated: the build states the absence and narrows its claims.

## Domain modules

State variables per domain start from the quick sets in
`references/indicators.md` §18; scenario families are in
`references/scenarios.md`. What each domain adds:

**Agriculture.** Typical scenarios: fertilizer regime, cover crops, rotation
change, irrigation scheduling, buffer strips along watercourses. Watch-out:
yield-only twins degrade the soil they model — the improvement score always
includes soil and receiving-water outcomes; yield is one indicator among
several.

**Pond / lake.** Typical scenarios: inflow load reduction, aeration,
biomanipulation, shoreline restoration, drawdown regime. Watch-out: internal
phosphorus loading can dominate external cuts for years — scenarios must
model the lag, or state that they cannot.

**River reach.** Typical scenarios: effluent limits, riparian restoration,
flow regime change, barrier removal. Watch-out: a reach twin without its
upstream boundary conditions is a fragment — Phase 1 must cover the
contributing catchment, and stage data carry their rating-curve status.

**Air basin.** Typical scenarios: emission source cuts, traffic or heating
changes, green barrier planting. Watch-out: attribute state to sources
cautiously — dispersion makes naive source claims the most common error in
air twins; deposition is judged against critical loads and levels.

**Flora / fauna conservation.** Typical scenarios: corridor creation,
protected-area boundary options, invasive control, grazing or visitor
pressure changes. Watch-out: the conservation safeguard is absolute —
sensitive locations are generalized in every output, including the client's
public reporting; pressure and management-response indicators sit beside
the state panels.

## Scripts

All scripts use only the Python standard library, read CSV (comma, semicolon,
or tab; decimal commas accepted) or JSON, print a JSON record, and never edit
their inputs (`registry.py` only appends to its registry). Exit codes: 0 done
or gate passed, 2 input error, 3 gate failed (`evidence_search.py`: 1 no
records, 2 every source failed). Run any of them with `--help`.

| Script | Phase | What it enforces |
|---|---|---|
| `scripts/qc_series.py` | 1 | range, rate, stuck, duplicate, gap, neighbor and change-point checks; flags only |
| `scripts/trend_test.py` | 1–2 | Mann–Kendall/Sen per segment between registered breaks; seasonal Kendall; autocorrelation |
| `scripts/skill_scores.py` | 3–4 | declared hold-out; naive baselines; NSE/KGE/RMSE; POD/FAR/CSI; Brier with reliability |
| `scripts/uncertainty_budget.py` | 3 | budget by source from ensembles; interval only from a joint ensemble |
| `scripts/alert_bands.py` | 4 | anchored amber/red bands; sustained-window alerts; gaps end episodes |
| `scripts/registry.py` | 3–4 | append-only, hash-chained forecast registry; scores forecasts exactly as issued |
| `scripts/generalize_coords.py` | all | GBIF sensitivity categories with this skill's 0.1° floor; `--check` gate before sharing |
| `scripts/build_manifest.py` | 6 | RO-Crate 1.1 provenance package; every headline number traced and cited |
| `scripts/evidence_search.py` | 1–5 | literature retrieval across PubMed, Europe PMC, OpenAlex, Crossref |

After changing the package, run `python3 -m unittest discover -s tests` and
`python3 tests/check_package.py` from the skill root.

## Quality gates before delivery

- Provenance complete: `build_manifest.py --report` passes — every headline
  number carries its manifest ID and evidence chain.
- Maturity level declared in the passport and never overstated; trial
  forecasts labeled as trial.
- Calibration reported with its declared split and thresholds, including where
  the model fails; `skill_scores.py` gate results attached; verification
  scores current for every forecast indicator.
- Every threshold has a named anchor (regulation, standard, or baseline).
- Every issued forecast is in the registry and `registry.py verify` passes;
  every implemented measure has a frozen counterfactual baseline.
- Event forecasts carry hindcast event scores; material risks have pre-agreed
  preventive actions with named triggers, owners, and stand-down criteria.
- Headline outputs carry computed uncertainty with a budget
  (`uncertainty_budget.py`), or the stated reason it cannot yet be computed.
- Sensitive species locations generalized: `generalize_coords.py --check`
  passes on every shared occurrence file; no exceptions.
- Red-team gates for the build's tier passed, or every critical attack is
  dispositioned on the record (`references/orchestration.md`).
- Uncertainty and data gaps stated in the deliverable itself, not in an annex
  nobody reads.
- Scenario recommendation scored on ecosystem outcomes, not one metric;
  nature-based options evaluated first, or their absence explained.

## Integration

Optional companion skills, when installed: **literature-review** for evidence
synthesis (`scripts/evidence_search.py` output fits its deduplication
helper), **peer-review** for auditing a third-party twin or a vendor's
claims, **scientific-writing** for the deliverable. GIS and remote-sensing
libraries (geopandas and similar) are adopted per project when needed.
