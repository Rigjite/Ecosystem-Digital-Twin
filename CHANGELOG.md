# ecosystem-digital-twin — Changelog

## v2.0 — 2026-10-21
- Loadability fixes: the SKILL.md frontmatter was invalid YAML (an
  unquoted ": " in the description); values are now quoted and the file
  parses with PyYAML and js-yaml. A closing code fence in Phase 6 carried
  text on the same line, so everything after it rendered as code; fixed.
  SKILL.md is under 500 lines; the analytics and uncertainty summaries are
  now short pointers to their references.
- Description rewritten for triggering: water-quality, bloom, hypoxia and
  low-flow early warning, monitoring design, audits of vendor twins, and
  Russian-language requests.
- Calculation toolkit (Python standard library, unit-tested):
  qc_series.py (quality gate with Pettitt change point, flags only),
  trend_test.py (Mann–Kendall/Sen per segment between registered breaks,
  seasonal Kendall, trend-free pre-whitening), skill_scores.py (declared
  hold-out, persistence and climatology baselines, NSE/KGE/RMSE,
  POD/FAR/CSI, Brier with reliability and Murphy decomposition),
  registry.py (append-only hash-chained forecast registry, no back-dating,
  superseded forecasts stay scored, overdue forecasts listed),
  generalize_coords.py (GBIF sensitivity categories per Chapman 2020 with
  this skill's 0.1° floor, extreme records withheld, pre-sharing check),
  build_manifest.py (valid RO-Crate 1.1 package; headline numbers traced and
  cited in the report; forecast registry tied to the package),
  uncertainty_budget.py (budget by source from one-at-a-time and joint
  ensembles; interval only from a joint ensemble), alert_bands.py (anchored
  amber/red bands, sustained-breach windows, gaps end episodes, invalid
  values ignored, suspect values kept and marked, optional noise tolerance). All CSV readers accept
  comma, semicolon or tab delimiters and decimal commas, and report rows
  they could not use. evidence_search.py: explicit 429 handling,
  consistent first-author field, contact-email warning.
- Rules sharpened: trial forecasts defined for level-3 twins (how level 4 is
  earned, no decision weight); scenario numbers from published effect sizes
  labeled evidence-based; intervals must name their computing method; the
  Phase 6 manifest example is now actual RO-Crate structure; GBIF extreme
  category handled (withhold) — previously 0.1° for all.
- Worked example made consistent with the rules: calibration plan declared
  before fitting and reported against baselines; no bloom probability from
  two events; the chlorophyll forecast registered as a trial; the wetland
  effect labeled evidence-based with the lake response stated as a gap.
- Tests: tests/test_scripts.py (43 unit and end-to-end tests, network-free), tests/check_package.py
  (package lint), T19–T27 and a traceability table in TESTS.md. Contents
  lists added to the four references over 100 lines. READMEs gain install
  instructions (folder name must match the skill name).

## v1.8 — 2026-10-20
- Usability pack: three documents
  that make the package usable without reading all ~2,000 lines first.
  references/quick-start.md — the one-page, ten-step Tier S path, what may
  be skipped at Tier S and what may never be skipped, escalation rules,
  and a file map. assets/templates.md — the five fillable forms (object
  passport with ELSA/FPIC checklist; risk register row; TARP; option card
  with counterfactual freeze line; forecast registry entry), with the
  rule that a non-applicable field is marked "n/a — reason", never
  silently deleted. examples/lake-example.md — a worked miniature: one
  fictional small lake carried end to end (passport, inventory with a
  stated gap, indicators, pattern memo, two-event catalogue with the
  honest watch-instead-of-forecast call, registry entry, TARP, option
  card, Gate C record), all values explicitly labeled illustrative.
- SKILL.md gains a "Start here" section pointing to the three documents.
  Test: T18 (usability walkthrough).

## v1.7 — 2026-10-20
- Five approved improvements (from the expert gap review she accepted):
  (1) quantitative uncertainty, (2) domain data standards, (3) forecast
  pre-registration, (4) value of information and adaptive sampling,
  (5) the counterfactual twin. New references/uncertainty-decision.md:
  uncertainty method ladder (Monte Carlo/ensembles → Bayesian calibration
  → Morris/Sobol global sensitivity → structural comparison), uncertainty
  budgets separating measurement/forcing/parameter/structural/scenario
  shares; value-of-information cycle (uncertainty map, next-measurement
  ranking by decision-uncertainty reduction per cost, sensor placement
  logic, adaptive intensification, stopping rule, realized-value audit);
  append-only forecast registry with EFI-style metadata — verification
  computed against forecasts exactly as issued; counterfactual twin
  protocol (frozen no-action baseline, both twins on identical forcings,
  no silent re-anchoring, field BACI evidence outranks the model,
  avoided-damage reporting as promised/attributed/observed).
- Data standards pack added to references/data-sources.md (OGC
  SensorThings, WaterML 2.0, Darwin Core, EML, STAC, CF, RO-Crate) and
  wired into Phase 6 nesting. SKILL.md hooks in Phases 3–6, a summary
  section, and a quality gate. Tests: T15 (uncertainty honesty), T16
  (value of information), T17 (registry and counterfactual integrity).

## v1.6 — 2026-10-20
- Analytics, forecasting, risk and prevention layer added (data
  analysis, historical data where available, pattern detection, event
  prediction, risk identification, preventive measures, forecasts, and
  decision options for improving the existing ecosystem). New
  references/analytics-forecasting.md: historical data rescue (archives,
  yearbooks, Landsat back to 1984, museum/herbarium records, proxy records,
  consented local knowledge) with a bias and breaks register; pattern
  analysis (climatology, trends, extremes, change points, lead–lag
  structure, phenology, regime-shift early-warning signals as hypotheses)
  delivered as a pattern memo; an event catalogue (occurrence, antecedent
  conditions, impact, response) as the bridge to prediction; a
  predictability audit and method ladder for event forecasting; mandatory
  event-based validation (probability of detection, false-alarm ratio,
  critical success index, lead-time distribution, Brier score); a risk
  register argued per cell from evidence; trigger–action–response plans
  (TARP) for preventive measures with owners, lead times and stand-down
  criteria; option cards (prevent → mitigate → restore → adapt → monitor,
  no-regret first) with residual risk and a verification indicator per
  option; after-action reviews closing the loop.
- SKILL.md hooks: Phase 1 historical data rescue; Phase 3 event-based
  validation; Phase 4 risk register and preventive action; Phase 5 option
  portfolio from the risk register; new summary section and quality gate.
  Data sources extended with archive and historical-collection rows.
  Tests: T13 (pattern and event-forecast honesty), T14 (preventive TARP).

## v1.5 — 2026-10-20
- Orchestration layer added (an orchestrator, specialist agents, and a
  red team, as a governed layer). New
  references/orchestration.md: three scale tiers (S single operator /
  M orchestrated specialists / L full council) chosen in Phase 0; seven
  roles with distinct seniority-framed personas (orchestrator, data scout,
  evidence scout, domain modeler, calibration auditor, red team, optional
  specialists); written task contracts (passport slice, manifest-ID inputs,
  gaps-not-guesses outputs, prohibition list); conflict resolution by
  evidence hierarchy, never by vote; independence rules (auditor ≠ modeler,
  red team ≠ builder, red-team model ≠ arbiter model, one shared persona
  voids a council).
- Red-team gates with attack checklists: Gate A design (indicator theater,
  threshold smuggling, proxy overclaims), Gate B calibration (tuning on
  scoring data, metric shopping, assimilation theater), Gate C delivery
  (scenario cherry-picking, moved weights, maturity overclaims); attacks
  recorded with severity and disposition; an unresolved critical attack
  blocks delivery.
- SKILL.md gains a summary section and a matching quality gate. Local
  implementation note points to ensemble.py (--models explicit, --personas
  distinct, --redteam-model different from the arbiter). Tests: T11
  (orchestration contract and independence), T12 (red-team gate blocks a
  flawed delivery).

## v1.4 — 2026-10-20
- Evidence layer connected (PubMed and similar platforms for evidence
  collection). New
  references/evidence-sources.md: platform routing — PubMed/PMC (microbiology,
  sanitary, toxicology, molecular methods), Europe PMC (life-science breadth,
  open full text), OpenAlex (hydrology, soil, remote sensing discovery),
  Crossref (DOI identity layer), Semantic Scholar, AGRIS, regional-language
  sources (CyberLeninka / eLibrary for Russian objects); licensed indexes
  (Scopus/WoS/CAB) only where access actually exists. Query protocol
  (per-platform translation, bilingual search, full provenance record) and
  evidence discipline (hierarchy standards → guidelines → reviews → local
  studies; abstracts screen, full text decides; transferability check).
- New scripts/evidence_search.py: queries PubMed, Europe PMC, OpenAlex and
  Crossref, emits normalized JSON compatible with the literature-review
  skill's deduplication/formatting helper. Live-tested 2026-10-20: PubMed,
  Europe PMC and Crossref returned records with PMIDs/DOIs; OpenAlex keyless
  pool answered 429 from this network (script stops that source and reports,
  per protocol; a free OpenAlex key raises the budget).
- SKILL.md: Phase 1 gains the evidence inventory; Integration names the
  routing reference and the helper. Tests: T9 (evidence routing), T10
  (helper smoke test).

## v1.3 — 2026-10-20
- Comprehensive indicator catalogue (scope addition: environmental
  quality indicators — chemistry, microalgae, nutrients, microbiology, flora,
  fauna, hydrometry, land — where they improve the twin). references/
  indicators.md rewritten: 19 sections, tiered Core / Conditional / Research —
  climate drivers; air quality and deposition; full hydrometric panel (stage,
  rating curves, discharge, low/high-flow indices, ice, sediment transport,
  channel morphology); surface-water physical and chemical panel (incl.
  nutrient forms reported separately); eutrophication and internal loading;
  contaminants and ecotoxicology; sediments; groundwater; soil and land;
  landscape and disturbance; flora; microalgae/phytoplankton/phytobenthos;
  sanitary and process microbiology (E. coli, enterococci, source tracking,
  AMR, denitrification, methane); invertebrates and zooplankton; fish and
  wildlife by taxon; ecosystem functions; pressure–response indicators;
  domain quick sets; indicator metadata and QA requirements.
- Selection discipline added to SKILL.md Phase 2 and domain modules: the
  catalogue is tiered, unselected conditional panels are justified by the
  absence of their trigger, unmeasured selected indicators remain named gaps.
- Data sources extended: CAMS, GRDC, GEMStat / water-quality portals, JRC
  Global Surface Water, GRACE, Movebank, ESDAC/LUCAS; laboratory note for
  microbiology, phytoplankton taxonomy and tissue chemistry.
- Scenarios extended: bloom/sanitary-risk management, contamination source
  control, early detection and rapid response.
- Tests: T7 (indicator selection discipline) and T8 (catalogue completeness)
  added.

## v1.2 — 2026-10-20
- Loop-hardened: four external judging rounds (strict reviewer protocol;
  judges: claude-opus-5.5 partial pass + deepseek-v4-pro-0813 full rounds).
  Scores: 8.6 → 8.7 → 8.4 → 8.7 (plateau; the dip was judge granularity
  oscillation — each round surfaced finer nits, all fixed).
- Fixes across rounds: negative-space and layer discipline (forecasts require
  calibration at every maturity level); named calibration metrics (RMSE,
  NSE/KGE) with holdout/cross-validation and naive-baseline comparison;
  failure thresholds declared before fitting; assimilation method heuristic
  by data density (nudging → EnKF/particle filtering); exit criteria added;
  sensitive-species generalization grid (0.1°) and red-list/CITES basis;
  agricultural data cited to the EU Code of Conduct; conflict-of-interest and
  personal-data lines in the ELSA check; FPIC narrowed to law/standards;
  open-data license precision (Sentinel acknowledgement, Copernicus DEM
  terms, GBIF DOI citation); NBS skip must be recorded in the passport;
  scenario weights fixed with the client before runs (MCDA); provenance
  package minimum format set to RO-Crate (JSON-LD); alert windows per
  indicator dynamics; world-practice entries anchored to verifiable sources
  (DOIs, project phases per the operators).

## v1.1 — 2026-10-20
- World-practice upgrade (the best of the world's existing digital
  twins, adapted and improved). Survey in
  references/world-practice.md: Destination Earth, BioDT, EU Digital Twin of
  the Ocean, Delft-FEWS/Deltares, Wageningen farm twins.
- Added: twin maturity ladder (Phase 0) with stakeholder map and ELSA check;
  data quality gate + fall-back hierarchy (Phase 1); three-layer separation,
  modularity, hybrid models (Phase 2); assimilation cycle + standing
  verification with client-facing scores and decision-value review (Phase 4);
  nature-based-solutions-first rule (Phase 5); RO-Crate-style provenance
  package with manifest IDs and nesting into larger systems (Phase 6);
  client data ownership as a non-negotiable.
- Tests: T5 (fall-back hierarchy) and T6 (maturity + verification in the
  report) added.

## v1.0 — 2026-10-20
- Created by Rigjita Baldanova. Original skill (not an adaptation).
- Scope set by the author's brief (2026-10-20): both consulting product and research
  instrument, product first; full cycle including scenario modeling oriented
  to ecosystem improvement, plus monitoring with alert thresholds; data
  strategy = skill selects sources per object, open sources first, client and
  sensor data added after.
- Domains: agriculture; ponds and lakes; river reaches; air basins; flora and
  fauna conservation sites.
- Structure: SKILL.md (workflow, Phases 0–6, domain modules, quality gates) +
  references/data-sources.md, references/indicators.md,
  references/scenarios.md.
