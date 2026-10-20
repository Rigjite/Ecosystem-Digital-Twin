---
name: ecosystem-digital-twin
description: Designs and operates digital twins of ecosystems — agricultural land, ponds, lakes, river reaches, air basins, and flora/fauna conservation sites. Full cycle: object scoping, open-first data inventory, state model, calibration against observations, monitoring with alert thresholds, historical pattern analysis, event forecasting and risk analytics, preventive action planning, and scenario modeling aimed at ecosystem improvement. Use when planning, building, auditing, or reporting an ecosystem digital twin, for a client project or for research.
license: CC BY 4.0
compatibility: Starts from open data (Copernicus Sentinel, Landsat, GBIF, ERA5, SoilGrids, national hydrology and meteo services) and open literature platforms (PubMed, Europe PMC, OpenAlex, Crossref) for the evidence layer, and adds client-supplied sensor and field data when available. GIS / remote-sensing tooling (QGIS, geopandas) is used at execution time, not assumed.
metadata:
  version: "1.8"
  skill-author: Rigjita Baldanova
  last-reviewed: "2026-10-20"
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
  disturbance risk). Follow GBIF sensitive-data practice: generalize coordinates
  (to a 0.1-degree grid, roughly 10 km, or coarser) in every shared output.
  Sensitivity is determined by IUCN and national red lists and CITES appendices.
- **Open first.** Exhaust open data before asking the client for anything.
  Client and sensor data extend the twin; they are not its entry ticket.
- **No uncalibrated twin ships as a twin.** A build that has not been checked
  against observations is labeled a prototype, in writing, in the deliverable.
- **The client's data stays the client's.** Farm, sensor, and site data are
  governed by the client's terms (the farm-data-space principle, as in the EU
  Code of Conduct on agricultural data sharing); the twin's
  passport states ownership, access, and what may be reused. Nothing is
  published or folded into another project without written consent.

World practice this skill is built on — Destination Earth, BioDT, the EU
Digital Twin of the Ocean, the Delft-FEWS operational forecasting practice,
and Wageningen farm twins — is surveyed
in `references/world-practice.md`, including what was adapted and what was
improved for this skill's scale.

## Start here — the usability pack

New to a build? Do not read the whole package first. Follow
`references/quick-start.md` — the one-page, ten-step path for a first or
small (Tier S) build. Fill the five forms in `assets/templates.md` as you
go (object passport, risk register, trigger–action–response plan, option
card, forecast registry entry), and keep `examples/lake-example.md` open
beside you: one small lake carried through every form, end to end. The
phases and references below are the detail the quick start points into.

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

Levels 2–3 describe and monitor observed state; they make no predictive
claims. Any forecast or scenario output requires Phase 3 calibration,
whatever the declared level.

Record also the stakeholder map (who decides, who is affected, who owns each
data stream) and a short ethical-legal-societal check: data ownership and
consent, sensor placement permissions, who may be harmed by a wrong alert,
any community whose land or livelihood the twin describes — including the
free, prior and informed consent of Indigenous communities where
required by applicable law and international standards (and as good practice
wherever their territories or knowledge are involved), plus landowner consent
under local law. FPIC is a checklist step, not a phrase: identify the
rights-holders, document the consent obtained or the legal basis relied on,
and record the outcome in the passport before data collection starts —
personal data
that imagery or sensor feeds may capture (minimize it; applicable privacy
law governs), and any conflict of interest — including a client who prefers
a particular scenario outcome. Scoring criteria and weights are fixed before
scenario results are seen, and the fixing is recorded.

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
search for its history per `references/analytics-forecasting.md`: agency
and institute archives, printed yearbooks and station logs, remote-sensing
archives back to 1984, museum and herbarium records, proxy records
(sediment cores, tree rings), and documented local knowledge collected
with consent. Harmonize what is found — method changes, moved stations,
revised taxonomy — and log every break in a bias and breaks register. If
no history exists, the passport says so; pattern and forecast claims for
that variable are then limited accordingly.

**Data quality gate (before any modeling).** Every incoming series passes
validation: range checks, rate-of-change checks, spatial consistency checks,
and trend-break detection. Series that fail are quarantined and flagged, never
silently cleaned. Gaps are handled by a declared protocol (interpolation,
model estimate, or left open) — and the protocol's choice is visible in every
downstream output it touches.

**Fall-back hierarchy.** For every core variable name a primary source and at
least one fall-back (an alternative dataset, a neighboring station, a modeled
estimate labeled as such). Continuity of monitoring must not depend on a
single feed.

Exit criterion: the candidate state-variable list for this object is drafted,
and every variable on it has at least one source in the matrix or is
explicitly listed as unmeasured. Phase 2 finalizes the list against this
matrix. Respect source licenses from the start: Sentinel data is acknowledged to
Copernicus, other products carry their own license terms — verify the
specific obligations per product — and GBIF downloads are cited by their DOI
in the provenance log.

### Phase 2 — State model

Choose state variables and indicators per domain from
`references/indicators.md`. Start from the domain quick set there, include the
core indicators for every medium present, then add conditional panels only
where a pressure, exposure pathway, legal duty, or decision triggers them —
extended water chemistry and nutrient forms, contaminants, sediments,
groundwater, hydrometry, phytoplankton composition, sanitary and process
microbiology, flora, fauna, ecosystem functions, and pressure–response
indicators. The catalogue is tiered, not a promise to measure everything:
conditional panels not selected are justified in the passport by the absence
of their trigger, and selected indicators that cannot yet be measured stay on
the list as named data gaps. Structure the model as drivers → state → impacts:
what acts on the system, what state it produces, what that state does to
ecosystem outcomes.

Keep the twin's three layers separate, as the operational ocean and Earth
twins do: **(1) monitoring** — the state as observed; **(2) forecast** — the
state as projected; **(3) impact simulation** — what the projected state means
for decisions and ecosystem outcomes. A deliverable never blends numbers from
different layers without labeling them.

Build the twin from replaceable modules — data connectors, model components,
indicator calculators — so one module can be upgraded or swapped (a better
classifier, a new sensor feed, a revised model) without rebuilding the twin.
Where both exist, prefer **hybrid models**: a process model for mechanism plus
a statistical or ML component for the residuals and the patterns the process
model misses, each checking the other.

Exit criterion: every state variable has a named layer (monitoring,
forecast, or impact), a model component, and an uncertainty statement.

Start simple: index models, balance models, and statistical baselines first.
Add process complexity (hydrodynamic, biogeochemical, dispersion) only where
the data inventory can feed and check it. A complex model on thin data is a
defect, not an achievement.

### Phase 3 — Calibration and validation

Hindcast the model against historical observations the model did not train on.
For statistical and index models, enforce the separation explicitly: a held-
out period or cross-validation folds, declared before fitting — never tune on
the data used to score. Report fit with named metrics per indicator (e.g.
RMSE and bias for continuous variables; Nash–Sutcliffe or KGE for flows) and
always against a naive baseline (persistence or seasonal mean): a twin that
cannot beat the baseline has no forecast skill, and says so. Failure
thresholds are declared before fitting (e.g. NSE below 0.5 for flows, or any
score at or below the naive baseline) and recorded with the calibration
report — a calibration is failed by its declared thresholds, not by feel.
Where no historical observations exist for hindcasting, calibration is
impossible by definition: the build remains a prototype (Phase 0 ladder),
verification is qualitative only — expert review of plausibility and internal
consistency — and the deliverable states this in place of any skill score. Report also the
periods and conditions where the model fails, and what would improve it. A failed calibration narrows the twin's
claims — record the narrowing in the deliverable rather than tuning silently.
Event forecasts are validated as events, not only as continuous series:
from hindcasts report probability of detection, false-alarm ratio,
critical success index, lead-time distribution, and — for probabilistic
forecasts — Brier score with a reliability statement
(`references/analytics-forecasting.md`). A forecast without hindcast event
scores is a prototype output and is labeled as such wherever it appears.

**Quantitative uncertainty.** Headline outputs carry computed uncertainty,
not adjectives (`references/uncertainty-decision.md`): Monte Carlo or
ensemble propagation as the default, Bayesian calibration where the data
support it, and a global sensitivity analysis naming the inputs that drive
each headline result. Every headline output ships with an uncertainty
budget separating measurement, forcing, parameter, structural, and
scenario contributions. A number whose uncertainty cannot yet be computed
is published with the reason — never with a decorative interval.

### Phase 4 — Monitoring, assimilation, and verification

For each core indicator set green / amber / red bands, anchored to a regulation,
a standard, or the object's own baseline statistics — the anchor is named in
the passport. An alert requires a breach sustained over a defined window, not a
single spike. Set the window per indicator dynamics — hours to a day for
dissolved oxygen and air-pollution episodes; days to weeks for chlorophyll
and vegetation anomalies — and record the window with the band. Alert
output states: indicator, observed value, band breached,
duration (window start timestamp plus elapsed time), likely drivers, and
the recommended human check.

**Assimilation cycle — what makes it a twin rather than a model.** Every new
observation batch (a) updates the twin's state, and (b) is scored against what
the twin forecast for that moment. The twin is thereby kept continuously
constrained by reality, in the manner of numerical weather prediction, at
whatever cadence the data allows. Method follows data density: error
correction or nudging for sparse series; Ensemble Kalman or particle
filtering where sensor density and model structure support them. Working
heuristic: nudging and error correction suit series whose gaps exceed the
system's response time; ensemble methods require observations at least as
frequent as the fastest dynamic being corrected, plus an ensemble the
operator can actually run — if either fails, downgrade the method, never
the honesty. The chosen method is named in the passport.

**Standing verification.** Forecasts are pre-registered in the twin's
append-only forecast registry before their outcomes are knowable —
forecast ID, issue time, horizon, value or probability with interval,
model version, input manifest IDs, and the verification metric declared
(`references/uncertainty-decision.md`). Verification is computed against
the registry exactly as issued, never reconstructed later. Registered
forecasts are archived, never overwritten, and re-scored on schedule with
more than one metric. The current verification
score per indicator is part of every client report: a falling score triggers
recalibration or an honest narrowing of the twin's claims — and, at review
points, an assessment of decision value: did the twin's guidance change a real
decision, and did the outcome improve? A twin can be accurate and useless;
only the second check catches that.

**Risk register and preventive action.** Maintain the object's risk
register (hazard, pathway, exposed element, likelihood, impact,
vulnerability, detectability, confidence, owner) and review it at every
verification cycle, with an emerging-risk scan at least annually. Every
material risk with an actionable lead time carries a pre-agreed
trigger–action–response plan: the trigger from the alert bands, the
preventive measure, its owner, the lead time it needs, its side effects,
and its stand-down criteria — agreed before the season, not improvised
during the event (`references/analytics-forecasting.md`).

**Value of information.** Each verification cycle also reviews where the
next measurement would most reduce decision uncertainty per unit cost —
from the sensitivity rankings and uncertainty budgets — and adapts the
sampling plan accordingly: sensor placement, extra dates, or intensified
sampling inside a forecast window (`references/uncertainty-decision.md`).
When the expected value of further measurement falls below its cost, the
plan says so and stops growing the network.

### Phase 5 — Scenario modeling for improvement

Build scenarios from `references/scenarios.md`: load reductions, buffer and
restoration measures, land-use changes, emission cuts, water-regime changes.
Run each against the baseline twin. Score every scenario on: ecosystem outcomes
(per domain indicators), cost, implementation risk, and time to effect — a
multi-criteria scoring with weights agreed with the client and recorded
before the runs (see Phase 0), never weights chosen after results are known.
Recommend one, with its trade-offs stated. Never optimize silently for yield,
discharge convenience, or any single metric. Draw the option portfolio from
the risk register and the pattern memo — prevent → mitigate → restore →
adapt → monitor — with no-regret and low-regret options surfaced first, and
present each option as an option card: expected effect with its evidence,
time to effect, cost, reversibility, residual risk, and the monitoring
indicator and review date that will prove or disprove the effect
(`references/analytics-forecasting.md`). When a measure is implemented,
freeze the no-action baseline twin as the counterfactual and run both
twins on the same observed forcings thereafter: the reported effect of the
measure is the difference, with its uncertainty, and any later model
improvement re-runs both twins with the change disclosed — never the
baseline alone (`references/uncertainty-decision.md`).

**Nature-based solutions are evaluated first.** In every scenario round, the
nature-based options (restoration, buffers, corridors, rewetting, green
infrastructure), where they exist for the problem at hand, are modeled before
engineered ones. If no nature-based variant is modeled in a round, the reason
(no applicable NBS, no data to model it, client-excluded with the exclusion
recorded) is written into the object passport — skipping NBS silently is a
defect, skipping it on the record is a decision. If the recommendation
favors an engineered option over an available nature-based one, the
deliverable must state why — the burden of justification sits on the
engineered option, not on nature.

### Phase 6 — Deliverable and handover

Client deliverable contains: object passport (with maturity level); current
state with evidence and provenance per indicator; calibration report;
monitoring bands, alert rules, and current verification scores; scenario
comparison and the recommendation; uncertainty and data gaps; update cadence
and the owner's maintenance duties. Research use adds the full provenance log
and model configuration to the project archive.

**Provenance package.** The deliverable ships as a structured package, not a
loose report: a manifest lists every dataset (with version and retrieval
date), every model component and its version, the workflow that produced each
result, and the parameter set. Minimum format: an RO-Crate (JSON-LD) manifest
at the package root — dataset, model, workflow, and parameter entities with
persistent identifiers where they exist — so the package stays readable by
external systems and reviewers without this skill's tooling. Compact shape:

```json
{ "datasets": [{"id": "ds-01", "name": "...", "version": "...", "retrieved": "YYYY-MM-DD"}],
  "models":   [{"id": "m-01", "component": "...", "version": "..."}],
  "workflow": [{"step": "...", "tool": "...", "parameters": "..."}],
  "outputs":  [{"value": "...", "evidence": ["ds-01", "m-01"]}] }
``` Every headline number in the report carries the
manifest ID of its evidence. Any result can then be re-traced and re-run by
the client or by a reviewer — trust is a property of the package, not of the
author's reputation.

**Nesting.** Build outputs in open formats so a local twin can feed a
regional or national system (a farm into a catchment twin, a lake into a
basin program) without rework. Use the domain standards recorded in
`references/data-sources.md` — SensorThings for sensor exchange, WaterML
2.0 for hydrology series, Darwin Core for occurrences, EML for ecological
and forecast metadata, STAC for imagery, CF for gridded data — and record
the choices and any deviation in the passport. A twin designed as a dead
end is a design defect at this skill's standard.

## Orchestration, multi-agent work, and red team

Builds run at one of three orchestration tiers, chosen in Phase 0 and
recorded in the passport (full protocol: `references/orchestration.md`):

- **Tier S — single operator** (default): one operator runs all phases;
  one independent red-team pass before delivery.
- **Tier M — orchestrated specialists**: an orchestrator coordinates a data
  scout, an evidence scout, and a domain modeler in parallel workstreams,
  with a calibration auditor independent of the modeler; red team at the
  calibration and delivery gates.
- **Tier L — full council**: Tier M plus a heterogeneous council — a
  distinct seniority-framed expert persona per member, never one shared
  persona — for design and scenario decisions on regulatory, health,
  large-money, or contested builds; red team at all three gates.

The orchestrator owns the passport, task contracts, and conflict resolution
(by the evidence hierarchy, never by vote) and is the single client-facing
voice. The two human decisions — Phase 0 framing and the Phase 5
recommendation sign-off — are never delegated to agents.

The **red team** attacks the build at defined gates — design (indicator
theater, threshold smuggling, proxy overclaims), calibration (tuning on
scoring data, metric shopping, assimilation theater), and delivery
(scenario cherry-picking, weights moved after results, claims above the
maturity level). It is independent of the builders it attacks; where models
differ per role, its model differs from the arbiter's. Every attack is
recorded with severity and disposition (fixed / claim narrowed / risk
accepted with owner sign-off); an unresolved critical attack blocks
delivery. Multi-agent overhead is justified by stakes and predictive
claims, never by the availability of tooling — and the red-team pass is
the last element cut from a budget, never the first.

## Analytics, forecasting, and preventive action

The analytics layer (`references/analytics-forecasting.md`) runs across
Phases 1–5. It rescues and harmonizes historical data before conclusions
are drawn; mines it for patterns — seasonality, trends, extremes, change
points, lead–lag structure, phenology shifts — recorded in a pattern memo
with confidence per pattern; and builds the object's **event catalogue**
(past adverse events with their antecedent conditions, impacts, and the
responses taken), which is the bridge from description to anticipation.
Event forecasts pass a predictability audit (an observable forcing and a
lead time longer than the preventive action needs — otherwise the product
is a watch and a response plan, honestly labeled), climb a method ladder
from climatology to hybrid models only as hindcast event scores justify,
and are always probabilistic with verified track records. Risks live in a
maintained register, preventive measures in pre-agreed
trigger–action–response plans, and improvement options in reviewed option
cards — so the loop closes: analysis → forecast → prevention → action →
measured outcome → better analysis. Where no historical data exist, none
of this is simulated: the build states the absence and narrows its claims.

## Uncertainty, information value, and the counterfactual

Four methods (`references/uncertainty-decision.md`) convert the twin's
honesty into arithmetic. **Quantitative uncertainty** is computed for every
headline output — ensembles or Bayesian calibration, global sensitivity
analysis, and an uncertainty budget that separates measurement, forcing,
parameter, structural, and scenario contributions. **Value of information**
spends the monitoring budget where it most reduces decision uncertainty,
adapts sampling to forecast windows, and stops expanding the network when
further measurement costs more than it teaches. The **forecast registry**
pre-registers every forecast in append-only form before its outcome is
knowable, so verification scores are evidence, not narrative. And the
**counterfactual twin** — the frozen no-action baseline, run in parallel
on the same forcings — turns implemented measures into measured effects
and avoided-damage reports: what was promised, what the model attributes,
and what was observed, kept as three distinct numbers.

## Domain modules

**Agriculture.** State: soil moisture, soil organic carbon, nutrient balance
(N/P/K), soil biology where decisions depend on it, NDVI/EVI dynamics, erosion
risk, receiving-water nutrient and sediment state, pollinators where crops or
field margins matter, yield as one indicator among several.
Typical scenarios: fertilizer regime, cover crops, rotation change, irrigation
scheduling, buffer strips along watercourses. Watch-out: yield-only twins
degrade the soil they model — the improvement score always includes soil and
water outcomes.

**Pond / lake.** State: water level and residence time, dissolved oxygen,
temperature and stratification profile, pH and conductivity, chlorophyll-a,
Secchi depth, nutrient forms and N/P loading, phytoplankton composition and
cyanobacteria risk, macrophyte, zooplankton, benthos and fish community
indicators, sanitary microbiology where people or animals use the water. Typical scenarios: inflow load reduction, aeration, biomanipulation,
shoreline restoration, drawdown regime. Watch-out: internal phosphorus loading
can dominate external cuts for years — scenarios must model the lag.

**River reach.** State: the full hydrometric panel (stage with rating-curve
status, discharge, low- and high-flow indices, flood and inundation regime),
water temperature, dissolved oxygen, nutrient forms and loads, sediment
transport and substrate condition, macroinvertebrate and diatom/phytobenthos
indices, continuity for fish passage. Typical scenarios: effluent limits, riparian restoration, flow regime
change, barrier removal. Watch-out: a reach twin without its upstream boundary
conditions is a fragment — Phase 1 must cover the contributing catchment.

**Air basin.** State: PM2.5/PM10, NO2/NOx, SO2, O3, NH3 where agriculture or
sensitive habitats are in scope, deposition onto soil and water against
critical loads and levels, emission inventory by sector, meteorological
dispersion conditions. Typical scenarios: emission source cuts,
traffic or heating changes, green barrier planting. Watch-out: attribute state
to sources cautiously — dispersion makes naive source claims the most common
error in air twins.

**Flora / fauna conservation.** State: habitat extent and connectivity, flora
composition and red-list plant populations, species richness and indicator
species, fauna occupancy, abundance and population trends by taxon present
(birds, mammals, amphibians, fish, invertebrates and pollinators as the site
supports), disease and eDNA screening where triggered, pressure indicators
(fragmentation, invasive species, disturbance) and management-response
indicators (actions delivered, recovery trajectory).
Typical scenarios: corridor creation, protected-area boundary options,
invasive control, grazing or visitor pressure changes. Watch-out: the
conservation safeguard above is absolute — sensitive locations are generalized
in every output, including the client's public reporting.

## Quality gates before delivery

- Provenance complete: every number in the deliverable traces to a source and
  carries its manifest ID in the provenance package.
- Maturity level declared in the passport and never overstated to the client.
- Calibration reported, including where the model fails; verification scores
  current for every forecast indicator.
- Every threshold has a named anchor (regulation, standard, or baseline).
- Red-team gates for the build's tier passed, or every critical attack is
  dispositioned on the record (references/orchestration.md).
- Event forecasts carry hindcast event scores (detection, false alarms,
  lead time); material risks have pre-agreed preventive actions with named
  triggers, owners, and stand-down criteria.
- Headline outputs carry computed uncertainty with a budget, or the stated
  reason it cannot yet be computed; every issued forecast is in the
  registry; every implemented measure has a frozen counterfactual
  baseline.
- Sensitive species locations generalized; no exceptions.
- Uncertainty and data gaps stated in the deliverable itself, not in an annex
  nobody reads.
- Scenario recommendation scored on ecosystem outcomes, not one metric;
  nature-based options were evaluated first, or their absence is explained.

## Integration

- **literature-review** — builds the evidence base for indicator choice,
  thresholds, and scenario expectations. Platform routing, the query
  protocol, and the evidence hierarchy for this skill live in
  `references/evidence-sources.md`; cross-platform retrieval runs through
  `scripts/evidence_search.py`, whose normalized output feeds the
  literature-review deduplication and formatting helper.
- **peer-review** — the audit stance for reviewing a third-party twin or a
  vendor's claims about one.
- **scientific-writing** — the client deliverable and research reporting.
- Component execution skills (geopandas and similar GIS, remote-sensing, and
  domain libraries from open skill collections) may be adopted separately when
  a live project needs them; this skill does not depend on them.
