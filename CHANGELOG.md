# ecosystem-digital-twin — Changelog

## v2.7 — 2026-10-26

The release of the whole v2.7 program (one version at the end, per the
author's decision of 2026-10-26). The package was built and verified in
staging only; this entry assigns the version.

- **32 second-wave functions in four rounds** (all approved by the author
  in topicality order, "Все по порядку, начиная по актуальности"): Round 1
  impacts-and-extremes + trust (impact chain, event storyline,
  historical-event replay, stochastic scenario generator, HQ/HI,
  covariate-aware alerts, alert trial, calibration plausibility gate);
  Round 2 coverage-and-delivery (virtual sensors, drift/connectivity,
  daily forecast bulletin, public status line, one product per audience,
  asset safety margin, user-class thresholds, exposure inventory);
  Round 3 forecast-quality + biodiversity (hindcast reproduction gate,
  skill-vs-lead-time curve, observation-nudged forecast,
  phenomenon-oriented metrics, diversity indices, PFT shares,
  trait–environment matching, spread-informed sampling priority);
  Round 4 governance-and-depth (sensitivity-first calibration, model
  ladder, adaptation appraisal + equity + M&E, driver-perturbation
  table, mismatch register, promotion record, semantic mapping set,
  "Valid use / out of scope" field). New scripts: `scenario_generate.py`,
  `drift.py`, `forecast_bulletin.py`, `diversity.py`, `trait_match.py`,
  `sensitivity_screen.py`, `mismatch.py`; new `registry.py promote`
  subcommand; new `mappings` entity type in `build_manifest.py`.
- **Ellenberg trait-table correction:** the field gallery entry's
  `trait_table.csv` was checked against the published Ellenberg values
  (Tichý et al. 2023, Zenodo 7427088) and did not match — only 14 of 40
  values. The table was replaced with the corrected values (7 taxa; "x"
  where Ellenberg is indifferent; Triticum aestivum removed — Ellenberg
  does not list cultivated wheat); `trait_match.py` gained the
  indifferent rule.
- **Audit-fix patch, Variant 1 + Variant 2:** an external model's
  line-by-line audit of the candidate was verified against the files and
  its findings fixed — the SKILL.md I/O table now describes all 16
  scripts; Core Mathematical Specifications grew from 6 to 12 formulas;
  the alert trial gains a third verdict INCONCLUSIVE_QUIET_WINDOW; the
  admit gate requires SS_RMSE > 0 only for PRIMARY target variables;
  the Tier S / M / L gradation is stated at the head of the 7-stage
  cycle.
- **Laguna borrowing patch (patterns only):** four patterns adapted from
  the Agricultural Digital Twin Platform (Laguna et al. 2025, Computers
  in Industry 172, 104347, DOI 10.1016/j.compind.2025.104347, MIT
  license) — three-zone file ingestion (landing → trusted → refined),
  twin-to-twin notifications, a per-twin workspace layout, and four
  named open-data ETL streams for the field twin. No code copied, no
  stack adopted, no ML approach taken.
- **Definition correction (author's decision):** the skill IS a digital
  twin of ecosystems — that is its definition (SKILL.md opening, README).
  The "(the consulting traffic light)" label on the Tier S / M / L
  header was removed; consulting stays only where it belongs, as one of
  the two USES (a consulting product for a client, and a research
  instrument), not as the skill's identity.
- **Affiliation removed (author's decision: the latest version carries
  no affiliation):** the `affiliation:` line is removed from
  CITATION.cff. The author (Rigjita Baldanova) and ORCID are unchanged.
  The CHANGELOG's historical v2.3 DOI record was reworded to carry no
  affiliation.
- **Professional README (EN + RU):** a detailed "Ecosystems covered"
  section (ponds and lakes, river reaches, wetlands, agricultural land,
  forests, air basins, biodiversity, contaminated soils, linked
  multi-ecosystem cascades — each with its gallery proof or real-data
  case), a Keywords list (14 GitHub topics), an Author section, the
  scripts table completed to all 16 scripts, and stale version
  references corrected (test count 227, tests T1–T80, citation v2.7).
- **Verification:** 227 tests pass; strict lint passes from a fresh copy
  installed as `ecosystem-digital-twin/`; SKILL.md 477 lines. The
  CITATION.cff DOI is still the v2.3 record (10.5281/zenodo.23657185)
  until the Zenodo release mints a new one; a DOI-update PR follows
  (as with v2.3).

## Round 4 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 4 is the governance-and-depth batch — the LAST round of
the program, the 8 functions the author approved fourth ("Все по
порядку, начиная по актуальности", 2026-10-26), in topicality order:

- **Sensitivity-first calibration (Gironde):** a *sensitivity screen*
  step in Stage 3 — new `scripts/sensitivity_screen.py`, perturbing each
  model parameter one at a time (±10% or a stated range) and recording
  the change in the output metric as a ranked table; the honest limit is
  stated in the script, SKILL.md Stage 3 and `assets/templates.md` §1:
  one-at-a-time misses interactions, unlike Sobol.
- **Model ladder (Digital Baikal):** a "Model ladder" subsection in
  SKILL.md Stage 3 + a field in the Object Passport
  (`assets/templates.md` §1) — the fast model is admitted for SCREENING
  ONLY and must stay within a declared tolerance of the full model on
  the same hold-out. Governance + template, no computation.
- **Adaptation appraisal + equity + M&E (DestinE):** the scenario scoring
  in `references/scenarios.md` is extended (equity column + follow-up
  date) and the §4 Option card gains impact avoided, co-benefits,
  equity, and a follow-up check date + registry forecast ID; the impact
  avoided comes from the Round 1 impact chain. After implementation the
  twin re-scores the option against the predicted impact on a fixed date
  via `registry.py issue` — the same Brier-style discipline as
  BEIRA-F-001.
- **Driver-perturbation table (Southern Water):** a "sensitivity" block
  in the What-if Scenario form (`assets/templates.md` §8) and a
  subsection in `references/scenarios.md` — for each driver (rainfall,
  nutrient load, abstraction, land use) apply stated perturbations
  (+10%, +25%, −10%) and report the indicator change using the existing
  index functions. Plain arithmetic, no new script. Boundary stated in
  the docs: the sensitivity screen perturbs MODEL parameters, this table
  perturbs INPUT drivers — different questions, different tables, never
  merged.
- **Mismatch register (Patos):** new `scripts/mismatch.py` + a form in
  `assets/templates.md` §12 + a subsection in
  `references/uncertainty-decision.md` §3 — record where observed ≠
  modeled, the *extent* (fraction of observed flooded cells correctly
  predicted) alongside the level score, the inferred hidden cause as a
  [ГИПОТЕЗА]/[НЕТ ДАННЫХ] item, and the measurement that would confirm
  it. The register is the learning log, not a gate: the alert trial and
  the hindcast reproduction gate are pass/fail, the register explains
  *why* a validation was bad.
- **Promotion record (Gironde):** a `promote` subcommand in
  `scripts/registry.py` (hash-chained like every record, never scored) +
  a Promotion record section in the Object Passport template
  (`assets/templates.md` §1) + a one-line rule in SKILL.md Stage 3 — a
  model is operational only after a recorded promotion (promoted by,
  on, evidence: benchmark + hold-out score); without one it is
  exploratory.
- **Semantic mapping set (BioDT):** one `mappings.csv` per gallery
  dataset directory (local field → standard term + justification,
  SSSOM-style) + a subsection in `references/data-sources.md` §6 + a row
  in the Phase 1 data-onboarding checklist (`assets/templates.md` §1) +
  a `mappings` entity type in `scripts/build_manifest.py` (one MappingSet
  File per mapping file in the RO-Crate output, conforming to SSSOM).
- **"Valid use / out of scope" field (BioDT):** a field in the Object
  Passport template (`assets/templates.md` §1) — the decisions the twin
  is built for, and what it must NOT be used for. Template only, no code.

Templates are now twelve fillable forms (§12 is the mismatch register
entry). 21 new tests (T69–T76); the suite is 213 tests, all passing.

### Audit-fix patch, Variant 1 + Variant 2 (2026-10-26, before version assignment)

The author's decision ("Да, вариант 1+2: чинить текст и гейты"). An
external model's line-by-line audit of this candidate was verified
against the files by the author-side agent before any fix was applied
— two of its seven textual points were corrected, not applied as
written: the passport already carried the nudge-N and model-ladder
tolerance fields (only drift_threshold was genuinely missing), and the
maturity downgrade rule already existed in Stage 3; the auditor's
weighted score was 8.7, not 8.8 (0.25 × 34.8 = 8.70). What changed:
the I/O table now describes all 16 scripts; the passport gains
'Primary target variables' and a per-indicator 'Drift threshold' in
both the SKILL.md summary and `assets/templates.md` §1; Core
Mathematical Specifications gains formulas 7–12 (HQ/HI, Shannon /
Pielou / Delta+, KGE, nudge, drift with leeway, the Stage 7 drift
statistic); a maturity cross-walk in Template 1 with a cross-reference
in Non-Negotiable 2; the trend_test.py preamble lists all 6 modes; the
Companion Documents header drops '(retained from v2.2)'; the gallery
names match the `examples/gallery/` directories; YAML last-reviewed
2026-10-25 → 2026-10-26. Gates: `alert-trial` gains a third verdict
INCONCLUSIVE_QUIET_WINDOW (exit 0) for a window with no alerts and no
critical events — it neither admits nor rejects; critical events with
no alerts still FAIL. `admit` requires SS_RMSE > 0 only for PRIMARY
target variables (optional `primary` flag; no flag anywhere means every
variable is primary — the pre-2.7 behaviour). The Tier S / M / L
gradation is stated at the head of the 7-stage cycle, cross-referencing
the ten-step Tier S path in `references/quick-start.md` (unchanged).
NOT implemented here (separate decisions): the mandatory source_ref
column in reference tables, and the 'Executive VoI & Sunk-Cost
Summary' card. Suite now 219 tests (214 baseline + 5 new: T51 +2,
T52 +3), all passing.

### Laguna borrowing patch (2026-10-26, before version assignment)

The author's decision ("Сейчас", after the four prioritized items were
presented). Four patterns borrowed from the Agricultural Digital Twin
Platform (Laguna et al. 2025, "A platform to support the fast
development of digital twins for agricultural holdings", Computers in
Industry 172, 104347, DOI 10.1016/j.compind.2025.104347, MIT license) —
PATTERNS ONLY: no code was copied, none of its stack was adopted
(Docker / Temporal / MongoDB / Minio / MLflow / Go / SvelteKit), and none
of its ML approach (a Random Forest yield model validated on one eyeballed
point from explicitly fake data — that would violate this skill's Rule
#1). The platform itself was evaluated 2026-10-26 (product 7/10, fit
6/10); only the four patterns below transfer to a stdlib-only, laptop,
deterministic method for building digital twins of ecosystems:

- **Three-zone file ingestion (landing → trusted → refined):** a zones
  convention in SKILL.md Stage 2 — incoming files land untouched in
  `landing/`, QC-passed files move to `trusted/`, domain-converted
  model-ready files live in `refined/`; a file leaves `landing/` only
  after its QC is recorded, enters `refined/` only after its conversion
  is recorded in the build manifest — plus a file-zone field on the Phase
  1 onboarding checklist (`assets/templates.md` §1) and a zones note in
  the `scripts/qc_series.py` docstring (the script flags rows; it never
  moves or edits files).
- **Twin-to-twin notifications:** a step in SKILL.md Stage 7 — when an
  alert fires, the twin notifies its linked nodes (upstream and downstream
  twins); the notification is recorded on the trigger–action–response
  plan (`assets/templates.md` §3, new "Linked nodes notified" field), not
  in the forecast registry; a notified node re-checks its own alert bands
  on the next batch. No new registry entry type was added: a notification
  is a communication act on the TARP, not a forecast record, and adding
  it to the hash-chained registry would mix non-scorable communication
  into the forecast record for no audit gain.
- **Per-twin workspace layout:** one folder per object in SKILL.md
  Stage 2 — `common/` (passport, shared data), `etl/` (ingestion + QC),
  `calibration/` (models + admission), `forecasts/` (bulletins +
  registry), `simulations/` (scenarios) — cross-referenced from the
  build-manifest sentence in Stage 7 (the manifest records which file
  sits where). Laguna's layout carries an `ml-training` folder; this
  skill has no ML-training step, so the layout adapts it away (the
  absence is pinned by test).
- **Four named open-data ETL streams (field twin):** a subsection in
  `references/data-sources.md` §10 — daily weather (ERA5 by default,
  station truth where one exists), forecast weather (national meteo
  service / CAMS; never a substitute for observations in calibration),
  historical weather (ERA5 back to 1940 or the national archive; the
  hindcast window), NDVI (Sentinel-2, Landsat where Sentinel is missing,
  MODIS/VIIRS daily as the coarse context layer only) — with a one-line
  cross-reference from the field gallery README; the list lives in one
  place only. A stream that is unavailable is recorded as a gap in the
  [НЕТ ДАННЫХ] register, not silently replaced by another stream.

Deliberately NOT borrowed: the whole stack, real-time streaming
(MQTT/Benthos/Change Streams/SSE), any UI/map frontend, any ML yield
model, the pistachio-specific simulation (cold hours, tree counts). Suite
now 227 tests (219 baseline + 8 new: T77 2, T78 2, T79 2, T80 2), all
passing.

Author's correction (2026-10-26, same day): the skill IS a digital twin
of ecosystems — that is its definition (SKILL.md opening, README). The
label "(the consulting traffic light)" on the Tier S / M / L header was
removed, and "consultant's method" in this section was corrected to
"method for building digital twins of ecosystems". Consulting stays only
where it belongs: as one of the two USES (README: a consulting product
for a client, and a research instrument), not as the skill's identity.

### Ellenberg trait-table correction (2026-10-26, before version assignment)

The author's decision ("Да, исправь таблицу до v2.7"). The field
gallery entry's `trait_table.csv` was checked against the published
Ellenberg values (the Ellenberg column in Tichý et al. 2023, Zenodo
record 7427088) and did NOT match — only 14 of 40 values; the table was
largely reconstructed from memory. Fixed as one package: the table
replaced with the corrected values (7 taxa; "x" where Ellenberg is
indifferent; Triticum aestivum removed — Ellenberg does not list
cultivated wheat; Salicornia values are ssp. europaea);
`scripts/trait_match.py` gained the indifferent rule (a taxon with "x"
for a trait is not excluded by a condition on that trait, named in the
output's `indifferent` list; a cell that is neither a number nor "x"
is refused, exit 2); the three T67 expectation tests rewritten to the
corrected values (saline site S ≥ 8 fits only Salicornia europaea;
N ≥ 7 fits Trifolium by indifference and excludes Salicornia and
Puccinellia at N = 4; T within 6 ± 1 fits all 7 taxa, two by
indifference) plus one new test pinning the indifferent rule and the
malformed-cell refusal; provenance lines fixed in
`scripts/trait_match.py`, `references/indicators.md` §11, the
field-gallery README and the field `mappings.csv` justifications
(exact source + verification date 2026-10-26; citation aligned to the
edition the corrected table follows — Ellenberg & Leuschner 2010 via
Tichý et al. 2023, not the unchecked 1991 printing). The Round 3
CHANGELOG entry below still records what was built then, with the old
table; this note records the correction. Suite now 214 tests (213
baseline + 1 new), all passing.

## Round 1 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version. Round 1 is the impacts-and-extremes + trust
batch — the 8 functions the author approved first ("Все по порядку,
начиная по актуальности", 2026-10-26), in topicality order:

- **Impact chain (DestinE):** new "Impact chains" section in
  `references/scenarios.md` + an "Impact chain" field on the §6 scenario
  card (`assets/templates.md`) — driver → exposed asset → impact, with
  the published function, its source, its applicable range, and its
  limits per link. No new code: arithmetic on the existing scripts'
  outputs. Links with no published function go to the [НЕТ ДАННЫХ]
  register, never invented.
- **Event storyline (DestinE):** a "Storyline" class in the scenario
  taxonomy (`references/scenarios.md`, now four classes beside Scenario 0
  / Planning / What-if) + a "Storyline" field on the §6 scenario card
  (event, drivers changed, held fixed, impact scored). No new code: the
  replay runs through the existing scenario machinery.
- **Historical-event replay (Digital Baikal):** a "Replay" protocol in
  `references/uncertainty-decision.md` §5 + a `replay` subcommand in
  `scripts/registry.py`. Take a historical extreme, run the existing
  QC/trend/alert pipeline on the data up to the event (cutoff = last
  observation before the event, no peeking), and record whether and when
  the alert fired — lead time in days. A miss is recorded with no lead
  time, a finding not a failure to report. Replays are hash-chained like
  every record but never scored and carry no decision weight for a future
  event. No dated Beira extreme exists in the published record, so no
  replay entry is appended to the real Beira registry; the entry type is
  implemented and tested, and the first real replay entry is created when
  a twin with a dated historical extreme is built.
- **Stochastic scenario generator (Digital Baikal):** new script
  `scripts/scenario_generate.py` (stdlib `random`, fixed seed —
  deterministic) + a section in `references/scenarios.md`. Input: a
  driver series + its fitted distribution (mean, SD, lag-1 autocorrelation
  from the object's own data); output: N seeded scenario series feeding
  the existing trend/alert pipeline, so a What-if reports a distribution
  ("in k of N seeded years the watch turns red"). Every generated value is
  labelled a scenario draw, never a measurement.
- **Hazard quotient / hazard index (Digital Baikal):** new `--mode hq` in
  `scripts/trend_test.py` + a section in `references/indicators.md` §6
  beside WPI/TSI/HPI. HQ = exposure ÷ reference per stressor; HI = sum of
  HQs; 1 = the safety line; acute/chronic split. Covers any stressor (air,
  water, smoke, chemicals) on a 1-scale. Documented honestly: same
  quotient family as HPI, but HPI covers only metals in water on a
  100-scale.
- **Covariate-aware alerts (Southern Water):** `scripts/alert_bands.py`
  gains `--explained-by` — a watch breach is logged as "explained" (not
  alerted) when the driver series is itself beyond its own watch level in
  a sustained episode overlapping the breach's window; only unexplained
  breaches alert, set the status, and count for `--fail-on`. Deterministic
  (a band check on a named driver, no ML). Rule in
  `references/indicators.md` §20 + an "Alerts" field on the §6 scenario
  card.
- **Alert trial (Southern Water):** new `alert-trial` subcommand in
  `scripts/skill_scores.py` — scores the alerts on a hold-out window:
  precision (relevant / all alerts), miss rate (missed criticals / all
  criticals), alarm volume — with admission thresholds (precision ≥ 0.9,
  zero missed criticals, alarm count capped). No alerts in the window is
  a FAIL. Distinct from the existing admission (SS_RMSE > 0), which scores
  the model, not the alerts. Trial card on the §6 scenario card; a short
  paragraph in `references/uncertainty-decision.md` §3.
- **Calibration plausibility gate (lake platforms):** new `admit`
  subcommand in `scripts/skill_scores.py` + new
  `references/calibration-bounds.md` (published parameter ranges with
  sources). Admission requires (a) the model beats the naive benchmark on
  EVERY key variable claimed (SS_RMSE > 0) and (b) every fitted parameter
  inside its declared physical bounds; a fit outside the bounds is
  rejected even if SS_RMSE > 0, logged with the offending parameter. One
  line in SKILL.md Stage 3: the two admission gates (plausibility gate +
  alert trial), both must pass.

Tests T45–T52 added (33 new tests); 138 tests pass. SKILL.md 310 → 318
lines (cap 500).

## Round 3 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 3 is the forecast-quality-and-biodiversity batch — the 8
functions the author approved third ("Все по порядку, начиная по
актуальности", 2026-10-26), in topicality order:

- **Hindcast reproduction gate (EDITO):** a "Reproduction check" field on
  the §6 scenario card (`assets/templates.md`) + a Phase 5 rule in
  `references/scenarios.md` — run the scenario model on the historical
  window with the intervention switched off; the reproduced state must
  match the observations within a declared tolerance (the indicator's
  alert-band width or the calibration SD). A failed check means the
  scenario delta is reported as "unvalidated, direction only" — never as
  a number. Boundary stated in both `references/scenarios.md` and
  `references/uncertainty-decision.md` §5: the gate validates a scenario
  model, the replay verifies an alert. No new code.
- **Skill-vs-lead-time curve (lake platforms):** a `skill-horizon`
  subcommand in `scripts/skill_scores.py` (per-lead SS_RMSE against the
  naive baseline supplied per row) + a "Skill horizon" field on the §5
  forecast registry entry. The twin's report states the skill horizon —
  the longest lead at which the forecast still beats persistence with
  every shorter lead also above zero; a forecast is not trusted beyond
  it. A longer lead that beats the baseline after a failure is a
  non-monotone recovery — noise, not skill. Hand-verified: horizon 1
  (lead 1 SS_RMSE 0.5, lead 2 −2.0, lead 3 1.0).
- **Observation-nudged forecast (lake platforms):** a `nudge` subcommand
  in `scripts/skill_scores.py` — shift a raw forecast by the mean
  model-minus-observed residual over the last N QC-passed pairs (N
  declared in the Object Passport, e.g. 5). The correction is recorded in
  the registry entry (§5 form) and the nudged forecast is scored per lead
  time by `skill-horizon` like any forecast. The transferable principle
  of the Meteolakes ensemble Kalman filter, not the filter itself.
  Hand-verified: residuals all +2 → raw 15 nudges to 13.
- **Phenomenon-oriented metrics (EDITO):** a table in
  `references/analytics-forecasting.md` §4 and a "Phenomenon metrics" line
  on the §5 registry entry — 2–3 event metrics per phenomenon (bloom:
  onset-date, peak-magnitude, duration errors; flood: peak-level, timing,
  extent; fire season: season-start, peak-area, duration; drought/low
  flow: onset, minimum, duration; heat: exceedance-days, peak). Admission
  stays SS_RMSE; the metrics show the client's skill on the events that
  matter. A metric with too few events is [НЕТ ДАННЫХ], never zero. No
  new script.
- **Diversity indices (BioDT):** new script `scripts/diversity.py`
  (subcommand `indices`) — Shannon H′ and Pielou evenness from counts,
  plus Clarke–Warwick taxonomic distinctness Δ+ from the Linnaean
  hierarchy (same genus 1, family 2, order 3, class 4, phylum 5,
  different phylum 6). The skill had zero diversity indices. The
  biodiversity gallery runner now reports them (Khubsugul: Shannon
  2.8571, Pielou 0.9885, Δ+ 3.5098 — counts are records per species, a
  presence-only proxy, never abundance; the unidentified record
  contributes only at class level). Subsection in
  `references/indicators.md` §11, cross-reference in §15.
- **Plant functional type shares (BioDT):** `diversity.py pft` — shares
  from one quantity only (cover or counts, never mixed), from a PFT
  assignment table published per site (literature / TRY). Demonstrated on
  the field gallery entry (`pft_cover.csv` + `pft_table.csv`): grass
  0.82, legume 0.10, forb 0.08, C3 1.00; one season reports shares only, a
  trend needs repeat surveys. Subsection in `references/indicators.md`
  §11.
- **Trait–environment matching (BioDT):** new script
  `scripts/trait_match.py` — a deterministic filter over a published
  trait table per object (Ellenberg indicator values for the worked
  example in the field entry): "at_least" for tolerances (salinity,
  drought), "within" for optima (temperature, pH). A taxon fits only
  when EVERY stated condition is met. Hand-verified: a saline site
  (S ≥ 8) fits only Salicornia europaea and Puccinellia distans. The
  table is transcribed — verify it against the published source before
  client use. Subsection in `references/indicators.md` §11, line in the
  §18 Agriculture quick set.
- **Spread-informed sampling priority (lake platforms):** a
  `sampling-priority` subcommand in `scripts/uncertainty_budget.py` —
  rank the next sampling targets by |model − naive| (or |model A − model
  B|), ties by input order; sample the top target next. The old budget
  CLI is unchanged (dispatch on the first argument only). Rule in
  `references/uncertainty-decision.md` §2 — the value-of-information
  home (§4 is the counterfactual twin, not the sampling rule) — with a
  line on the §6 scenario card and a Stage 6 line in SKILL.md.
  Hand-verified: targets A (0), B (8), C (3) rank B, C, A.

## Round 2 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 2 is the coverage-and-delivery batch — the 8 functions the
author approved second ("Все по порядку, начиная по актуальности",
2026-10-26), in topicality order:

- **Virtual sensors (Gironde):** a "Virtual sensor" block in the Object
  Passport (`assets/templates.md` §1) + one line in
  `references/data-sources.md` listing satellite proxies as virtual-sensor
  sources. Name, physical quantity, proxy source + deterministic formula
  (the published satellite algorithm), calibration station + skill score
  against it (the existing SS_RMSE), validity window, and the same QC/alert
  machinery as a physical sensor. When the proxy leaves calibration, its
  readings go to the [НЕТ ДАННЫХ] register — never silently used. No new
  math (the proxy formula is the published satellite algorithm; the score
  is the existing SS_RMSE).
- **Deterministic drift / connectivity (EDITO):** new script
  `scripts/drift.py` (stdlib only) — deterministic advection of passive
  particles from a published current field (displacement = current velocity
  × time, plus a wind-leeway factor), reporting a connectivity matrix
  (fraction arriving in each target zone) and median travel time. Inputs:
  release points, current vectors transcribed as a table from a published
  current rose or Copernicus Marine values, target zones. The Plastic
  Tracker's "travel time" is an output of the same module (source →
  receptor). The skill's first transport function. Hand-verified: a
  constant 0.5 m/s eastward current at 50°N moves a particle 0.025152° of
  longitude per hour; 0.1° takes 4 steps; leeway 0.5 × 1.0 m/s wind halves
  the travel time to 2.0 h.
- **Daily forecast bulletin (Gironde):** new script
  `scripts/forecast_bulletin.py` (stdlib only) + a "Forecast bulletin" form
  in `assets/templates.md` §9. Reads a registry entry + the latest
  observation CSV and writes a one-page Markdown bulletin: observed value
  today, forecast value with interval and interval method, watch status of
  the latest observation and of the forecast value, and the date the
  forecast will be scored against its metric, exactly as issued. Trial
  forecasts carry a "Trial forecast — no decision weight" line. The
  bulletin renders the registry; it changes no numbers. No math changes.
- **Public status line (Southern Water):** a "Public status line" form in
  `assets/templates.md` §10 (one paragraph, plain language: current state,
  what changed, the maturity label, the [НЕТ ДАННЫХ] gaps — generated from
  the runner's summary JSON) + one rule in SKILL.md Stage 6: every twin
  ships one. For the client and the public — distinct from the handover
  note (for a successor builder, technical) and from RO-Crate (for
  machines).
- **One product per audience + dissemination register (Patos):** a
  "Decision product" form in `assets/templates.md` §11 (each product names
  its audience, its thresholds, its format, its channel, and its refresh
  cadence) + a "Dissemination register" block in the §1 Object Passport
  (who receives which product, by what channel). Template/governance only —
  no computation. The templates are now eleven fillable forms, not eight:
  the `assets/templates.md` header and the SKILL.md Companion Documents
  line both say eleven (two older tests that asserted "eight" were updated
  to the new count).
- **Asset-relative safety margin (Patos):** a clearance table in the
  Object Passport (`assets/templates.md` §1) + one line in the forecast
  registry entry (`assets/templates.md` §5) + a `--clearance
  "asset:threshold,..."` option on `scripts/registry.py issue`, which
  records per-asset clearance (threshold − forecast value) in the
  hash-chained record; `verify` rejects a record whose clearance does not
  equal threshold − value. Plain arithmetic, no new script. Generalizes
  beyond floods: clearance of a pollutant below its limit, of a level
  below a spillway crest, of a temperature below a lethal threshold.
- **User-class operational thresholds (Patos):** a `--class-thresholds
  FILE` option on `scripts/alert_bands.py` (CSV: class, limit — the
  operational limit in the indicator's units, same direction as the bands)
  + a rule paragraph in `references/indicators.md` §20 + an onboarding line
  in `assets/templates.md` §1 ("Decision-makers' operational limits (Phase
  1)"). The output gains a `class_thresholds` block: per class, the limit
  and whether the latest observed value and the episode peak are within it
  (`can_operate` is yes only when the class can operate now and could
  operate at the event's worst moment; with no alert episode the peak check
  is vacuous). A flooded road is passable for a pickup (0.45 m) while it is
  not for a car (0.30 m) or an ambulance (0.35 m) — the same water, a
  different verdict per class. Distinct from the per-asset clearance: the
  clearance is about an asset's margin; this is about who can do what.
- **Exposure inventory + exposed fraction (EDITO):** an "Exposure" block
  on the scenario card (`assets/templates.md` §6) + the exposed fraction
  added to the scoring rule in `references/scenarios.md` + a subsection
  "Exposure inventory and exposed fraction" after "Impact chains". Per
  scenario: the exposed elements (people, assets, habitats, intakes,
  cages) and the exposed fraction per class (exposed ÷ total in the zone),
  computed by table arithmetic from the hazard extent and the exposure
  inventory. The chain's Exposure link names who/what is in the hazard's
  path; the fraction quantifies it per class. A fraction with no inventory
  behind it is not a number, it is a guess, and goes to the [НЕТ ДАННЫХ]
  register.

Tests T53–T60 added (27 new tests); 165 tests pass. SKILL.md 318 → 325
lines (cap 500).

## Wetland first: the v2.6 program — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per item: the version inside the package stays 2.4
through the v2.6 program, and the whole verified program gets one
version (v2.6) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version. The missed natural systems are added in the
order the author approved: wetland, forest, bioreactor, soil
microbiome, steppe, estuary/delta, groundwater, pollinators, coast.

- Gallery re-location (author's decision, 2026-10-26: no Russian
  landscape in the gallery): the five gallery entries that modelled
  Russian landscapes were moved — four re-located to non-Russian ones,
  with new deterministic data, new published anchors, new READMEs, and
  updated tests (forest-fire and forest-carbon to the Prince Albert
  Forest Management Area, Saskatchewan, Canada; forest-logging to the
  British Columbia timber supply areas Prince George / Quesnel /
  Mackenzie; air to Prince George, BC), and the biodiversity entry
  (Gusinoye lakeshore birds, real GBIF data) REMOVED by the author's
  decision the same day ('Убери гусиное') instead of re-located: the
  GBIF pull for a replacement was blocked (HTTP 403) and must not be
  retried or bypassed, so the entry was removed; it was replaced the
  same day (see the next item), and the gallery now holds nine entries.
  The Baikal references in the METHOD
  (the multi-source fusion checklist, `references/data-sources.md`,
  the literature) stay — only the gallery miniatures moved. The GBIF
  sensitivity rules stay in the skill. Tests T40/T42/T43/T44 updated;
  104 tests pass.

- Biodiversity gallery prototype REPLACED (author's decision,
  2026-10-26, 'Замени другим биоразнообразие'; the site change to Lake
  Khubsugul is the author's own choice): the removed Gusinoye entry is
  replaced by Khubsugul lakeshore birds, Mongolia — Lake Khubsugul
  (Khövsgöl), approx 51.0 N, 100.5 E, Mongolia's largest freshwater
  lake and an Important Bird Area. Synthetic records (deterministic
  formulas; 20 records, 18 species, four shore points with jitter;
  one record unidentified, "Aves sp."). No real records are used: the
  GBIF occurrence-search pull was blocked (HTTP 403) and must not be
  retried or bypassed; a real-data version is possible later via a
  live-browser GBIF pull. Sensitivity categories are the real IUCN Red
  List statuses of the lake's birds (Emberiza aureola CR — coordinates
  withheld; Aythya ferina VU — pre-rounded to the 0.1-degree grid; the
  rest NT/LC — generalized by the runner). Design anchors: the eBird
  Khatgal hotspot checklist and the lake's best-known birds (Baikal
  teal, bar-headed goose, black stork, Altai snowcock). Results: 19
  generalized, 1 withheld, check gate pass, 0 violations, 18 species
  in 4 cells of 0.1°, at most 7 species in one cell. Maturity 2
  (Descriptive). The gallery now holds nine entries. Tests T40 (1 new
  test); 105 tests pass (104 baseline + 1 new).

- Professional stance block added to `SKILL.md`: the builder's working
  standard — domain depth, comparative view with transferability checks,
  evidence first, verification never overridden by seniority. No titles
  or publication counts are claimed.

- Wetland gallery prototype (first item of the v2.6 program):
  `examples/gallery/wetland/` — Everglades treatment wetland + marsh,
  real data: SFWMD STA-1W ATS pilot monthly influent/effluent TP
  (Aug 2008..Aug 2009; median removal 35.4%, mean 33.6% vs the
  document's stated 33.3% and the Beira reference median 46%) and
  USGS NWIS EDEN 10 daily gage height (2025-12-01..2026-03-31, 6.10 ft
  down to 5.26 ft, Sen -2.60 ft/yr). Outflow TP watch at the STA WQBEL
  levels (13/19 ug/L, applied as monthly watch levels); level watch
  at p10/p5 of the window (5.37/5.33 ft). Maturity 2 (Descriptive).
  No new math, no new indices, no fitting helper, stdlib only. The
  two series are different cells and periods of one system, stated in
  the README; a synchronous single-object record is [НЕТ ДАННЫХ].
  JRC Global Surface Water extent was checked and is unusable for a
  stdlib miniature (raster tiles / Explorer); water level is the
  drying signal instead. Tests T41 (2 tests); 99 tests pass (97
  baseline + 2 new).

- Forest-fire gallery prototype (second item of the v2.6 program):
  `examples/gallery/forest-fire/` — Prince Albert Forest Management
  Area (Sakâw Askiy), Saskatchewan, Canada, fire seasons, synthetic
  (deterministic formulas; design anchors from the Canadian
  Interagency Forest Fire Centre (CIFFC) and the Saskatchewan Public
  Safety Agency: Canada 2023, the national record, 18,496,051 ha
  burned; Saskatchewan 2023, 494 fires and ~1.9M ha burned; the FMA
  covers 3,354,418 ha, 2.7M ha forested): monthly fire counts and
  burned area, Apr-Oct 2019-2025 (49 rows). Both trends increasing
  (seasonal Kendall; counts p = 0.011, Sen +0.167/month per year; area
  p = 0.0012, Sen +210.2 ha/month per year); biggest season 2025
  (62 fires, 128,830 ha). Watches at declared levels (counts 11/13 per
  month, area 20,000/30,000 ha/month): 5 fires alerts (4 amber, 1 red)
  and 5 area alerts (4 amber, 1 red); amber episodes Jul-Aug 2019,
  2021, 2023, 2024; red episode Jul-Aug 2025.
  Maturity 2 (Descriptive). Real data were checked and found unusable
  (FIRMS Area API needs a MAP_KEY; public NRT files cover 7 days only;
  GFED/Global Fire Atlas/Copernicus are gridded products; no clean
  published monthly series for the FMA) — documented in the README.
  No new math, no new indices, no fitting helper, stdlib only. Tests
  T42 (2 tests); 101 tests pass (99 baseline + 2 new).

- Forest-logging gallery prototype (third item of the v2.6 program):
  `examples/gallery/forest-logging/` — British Columbia timber supply
  areas (Prince George, Quesnel, Mackenzie), synthetic (deterministic
  formulas; design anchors from the BC Harvest Billing System and the
  chief forester's AAC determinations: BC harvest 38.9 million m3 in
  2023, 39.0 in 2024, 37.7 in 2025; Interior 26.9 million m3 in 2023;
  Prince George TSA AAC 12.5 million m3, Quesnel TSA AAC 4.0 million
  m3, Mackenzie TSA AAC cut 18.4% in 2024; BC minimum harvest volume
  140 m3/ha): annual logged area and harvest volume, 2015-2025
  (11 rows; 17,900 ha and 3.44 million m3 in 2015 rising to 30,600 ha
  and 6.43 million m3 in 2025; 257,100 ha and 51.56 million m3 over the
  window). Both trends increasing (area p = 5.16e-05, Sen +1,220 ha/yr;
  volume p = 5.16e-05, Sen +272,750 m3/yr); Prince George is the largest
  every year (47.0% of the window total; Quesnel 31.0%, Mackenzie
  22.0%). Watches at declared levels (area 24,500/28,000 ha/yr; volume
  5.0/5.7 million m3/yr): 2 area alerts (1 amber, 1 red) and 2 volume
  alerts (1 amber, 1 red); amber episodes from 2022, red episodes from
  2024, both ongoing. Maturity 2 (Descriptive). Real data were checked
  and found unusable (GFW data API needs a key; dashboard and map pages
  are JavaScript-driven; Hansen/GLAD rasters need raster processing;
  the BC Harvest Billing System publishes provincial totals, not a
  ready annual series per timber supply area) — documented in the
  README. No new math, no new indices, no fitting helper, stdlib only.
  Tests T43 (2 tests); 103 tests pass (101 baseline + 2 new).

- Forest-carbon gallery prototype (third item of the v2.6 program):
  `examples/gallery/forest-carbon/` — Prince Albert Forest Management
  Area (Sakâw Askiy), Saskatchewan, Canada (2,700,000 ha forested —
  the same landscape as the forest-fire entry, so the three forest
  entries share one landscape and consistent disturbance years),
  synthetic (deterministic formulas; design anchors from UNEP boreal
  biomass 60-100 t C/ha with ~80% aboveground (Mahli et al. 1999;
  Luyssaert et al. 2007); Alberta boreal sequestration 0.5-2
  t C/ha/yr; fire losses from the forest-fire entry's annual burned
  areas plus stated interpolation for 2015-2018: 88,000 / 74,000 /
  82,000 / 91,000 ha): annual carbon density, 2015-2025 (11 rows;
  52.00 t C/ha rising to 53.92 t C/ha; total stock 140.40 Mt C rising
  to 145.58 Mt C, +5.18 Mt C, +3.7%). Density trend increasing
  (p = 2.62e-05, Sen +0.208 t C/ha/yr); net-change trend decreasing
  (p = 0.039, Sen -0.017 t C/ha/yr) — yearly growth is slowing as fire
  losses grow; smallest growth year 2025 (+0.04 t C/ha/yr). Only the
  net-change watch remains (amber at +0.15 t C/ha/yr or below, red at
  0.0 or below): 3 years below amber, 0 below red; 1 change alert
  (1 amber, 0 red), episode 2024-2025 ongoing. The low-density watch
  was removed: the series rises, so it is meaningless. Maturity 2
  (Descriptive). The README states the carbon-credit boundary: this
  entry watches carbon stock and its change; it is NOT a
  carbon-credit methodology and claims no compliance with any credit
  standard (Verra, Gold Standard, or other). Real data were checked
  and found unusable (ESA CCI Biomass is a raster product; GFW data
  API needs a key; FIA DataMart needs multi-table harmonisation and is
  US data; no open annual carbon-density series for one FMA) —
  documented in the README. No new math, no new indices, no fitting
  helper, stdlib only. Tests T44 (2 tests); 105 tests pass (103
  baseline + 2 new).

## Rounds 1–4 of the v2.5 program (borrowings) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per round: the version inside the package stays 2.4
through all rounds of the program, and the whole verified program gets
one version (v2.5) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version.

- FAIR Signposting over RO-Crate (borrowed from BioDT):
  `scripts/build_manifest.py` writes FAIR Signposting relations
  (signposting.org) into the Root Dataset of `ro-crate-metadata.json` —
  `cite-as` (the package DOI from the build index, never invented),
  `describedby` (`ro-crate-metadata.json` itself), `license` (the index
  licence, when given as a URL). Documented in SKILL.md (Stage 7, I/O
  table). The package DOI in CITATION.cff is still the v2.3 record
  (10.5281/zenodo.23657185) until the v2.4 release mints a new one; the
  signposting `cite-as` uses the DOI given in the build index, not a
  value invented by the script.
- Scenario taxonomy beside Scenario 0 (borrowed from Southern Water):
  every scenario declares its class — Scenario 0 (No-Action
  counterfactual, unchanged), Planning scenarios (land use, development,
  catchment change), What-if intervention scenarios (the measures
  themselves). Added to SKILL.md (Stage 4) and `references/scenarios.md`,
  with a one-line pointer in `references/uncertainty-decision.md` §4 and
  a scenario-card template (`assets/templates.md` §6; the forms are now
  six, not five).
- Handover note: the Object Passport (SKILL.md Template 1) and
  `assets/templates.md` §1 record who maintains the twin after the author
  (name/role, handover conditions).

Round 2 — Recalibration trigger and continuous revalidation (borrowed
from lake hydrodynamic platforms and BioDT):
- Recalibration trigger: on each new QC-passed batch, `scripts/trend_test.py
  --mode drift --baseline <calibration series>` checks level drift
  (|mean(new) − mean(calibration)| / sd(calibration), firing at the
  per-indicator threshold declared in the Object Passport, default 2.0)
  and trend drift (the new batch's Sen slope outside the calibration
  slope's Gilbert confidence interval, reusing the trend-test machinery
  with no duplication). Either component fires the trigger: recalibrate
  (Stage 3 re-run), recompute alert bands, update linked nodes, and
  revalidate before the model can keep ADMITTED status. A fired trigger
  is a report (exit 0), not a failure. Documented in SKILL.md (Stage 7,
  I/O table) and `references/analytics-forecasting.md` §8.
- Continuous revalidation: `scripts/skill_scores.py revalidate` re-scores
  the admitted model on each new batch against the naive benchmark, with
  the original `--train-end` split (baselines from training data only, so
  the new batch never trains its own baseline). SS_RMSE ≤ 0 revokes
  ADMITTED (exit 3) and drops the twin's maturity label to the highest
  level the twin still meets, until a better model is admitted.
  Documented in SKILL.md (Stage 3, I/O table) and
  `references/analytics-forecasting.md` §8. Forecasts already issued are
  not re-scored or re-anchored.
- Tests (Rounds 1–2): T34 (FAIR Signposting in the manifest), T35 (taxonomy, scenario
  card, handover presence), T36 (recalibration trigger: level, trend, QC
  exclusion, input errors), T37 (revalidation: keep, revoke, missing
  split). Verification in staging: 87 tests pass (79 baseline + 8 new);
  strict lint passes from a copy installed as `ecosystem-digital-twin/`.

Round 3 — Two tiers, explainability, multi-source fusion (borrowed from
EDITO, Patos Lagoon, Digital Baikal):
- Two tiers: `assets/templates.md` gains §7 Focus application (for
  builders: purpose, object and nodes, inputs with manifest IDs, outputs,
  builder, maturity targeted, update cadence) and §8 What-if scenario
  (for decision-makers: the decision, options compared with scenario IDs
  and classes, evidence per option, recommendation, what would change it,
  decision-maker and date). The scenario card (§6) still records a single
  scenario; the What-if form frames the decision across scenarios.
  Documented in SKILL.md (Stage 6, Companion Documents); the forms are
  now eight, not six.
- Explainability under pressure: when a decision is made under pressure,
  the twin states in plain terms what the model used, what it did not
  use, and how confident it is — no black-box verdicts. Recorded on the
  scenario card (§6, "Explanation" field). Documented in SKILL.md
  (Stage 6) and `references/uncertainty-decision.md` §1.
- Multi-source fusion checklist: heterogeneous sources (space, aerial,
  ground, water) are fused in one scheme — one object, one time base, one
  spatial reference — with a per-source checklist: coverage, resolution,
  alignment, cross-source consistency checks, gaps → the [НЕТ ДАННЫХ]
  register. Extends the v2.4 onboarding checklist, never replaces it.
  Documented in SKILL.md (Stage 2, Object Passport template) and
  `references/data-sources.md` (new section; a Contents list was added
  because the file now exceeds 100 lines).
- Tests (Round 3): T38 (two tiers), T39 (explainability, fusion
  checklist). Verification in staging: 91 tests pass (87 baseline + 4
  new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`.

Round 4 — Prototype gallery (borrowed from BioDT):
- Five working miniatures under `examples/gallery/`, each a small data
  file + a `run.py` that reuses the skill's scripts + a README stating
  the management question, the maturity label, and the expected outputs;
  an index (`examples/gallery.md`) lists each entry with its question,
  data provenance, and maturity label. No new formulas, no new math,
  stdlib only. Lakes are already covered (Beira + Lake Primernoe) and
  the cascade by the existing dry-run, so the gallery does not duplicate
  them.
- Pond (synthetic): small-pond eutrophication — TP trend increasing
  (p = 0.0004), TSI composite 65.1 eutrophic, a calibrated model admitted
  on a declared hold-out (SS_RMSE 1.0 — near-perfect by construction,
  the series were generated from the fitted form), alert bands live.
  Maturity 3 (Informative).
- River reach (real): USGS NWIS, Potomac at Little Falls, 81 daily
  values 2026-08-01..2026-10-20, public domain — no significant trend,
  flood event 2026-10-12..20 peaking at 625.8 m³/s, red alert. No
  chemistry, so no WPI. Maturity 2 (Descriptive).
- Agricultural field (synthetic): soil-moisture watch — drying trend
  (p = 6.7e-16), 26 days below the irrigation watch level, red alert.
  Maturity 2 (Descriptive).
- Air basin (synthetic): Ulan-Ude winter PM2.5 — 12 days above the WHO
  daily guideline (45 µg/m³), 5 above the interim target (75 µg/m³),
  red episode 2026-01-16..19. Real CAMS data were checked first and
  found too coarse (1.8–17.1 µg/m³, zero days above 45); station data
  are [НЕТ ДАННЫХ]. Maturity 2 (Descriptive).
- Biodiversity site (real): GBIF, Gusinoye lakeshore birds, 20 records,
  CC BY-NC 4.0 — 18 species, 19 records generalized to the 0.1° grid,
  the one Critically Endangered record (*Emberiza aureola*) published
  with coordinates withheld, check gate pass. Maturity 2 (Descriptive).
  Synthetic entries are labelled synthetic in their READMEs and runner
  summaries and must never be cited as data.
- Tests (Round 4): T40 (gallery: five runners + index + SKILL.md
  reference). Verification in staging: 97 tests pass (91 baseline + 6
  new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`.

## v2.4 — 2026-10-26

Applied 2026-10-26 on the author's approval of the v2.4 proposal
(lead-time register + forecast cadence, Phase 1 data-onboarding
checklist). Local skill only; GitHub release and Zenodo DOI for v2.4
pending — CITATION.cff still names the v2.3 DOI
(10.5281/zenodo.23657185) until the release mints the v2.4 DOI, as with
the v2.3 release (DOI added in a follow-up PR).

- Lead-time register + forecast cadence (borrowed from the Patos Lagoon
  and Gironde river twins): `scripts/registry.py issue` accepts
  `--cadence daily | weekly | seasonal | event-driven` and `--lead-time`
  (value) with `--lead-time-unit hours | days | weeks` (default `days`).
  Both fields are validated on issue and on verify; records issued before
  v2.4 carry neither field and still verify. Documented in SKILL.md
  (Stage 7, I/O table) and in `assets/templates.md` §5, with a marked
  format example; no existing registry record is touched (BEIRA-F-001
  unchanged, hash chain intact).
- Data-onboarding checklist (borrowed from EDITO): Phase 1 admits a
  dataset only against the checklist — source and access date, licence
  and reuse terms, spatial and temporal resolution and coverage, QC
  performed (method and result), gaps → the [НЕТ ДАННЫХ] register.
  Added to SKILL.md (Stage 2, Object Passport template) and to
  `assets/templates.md` §1.
- Tests: T32 (registry cadence/lead_time), T33 (checklist presence).
  Verification in staging: 74 tests pass (67 baseline + 7 new); strict
  lint passes from a copy installed as `ecosystem-digital-twin/`.

## v2.3 — 2026-10-25
- SKILL.md rewritten to the v2.3 specification: strict mathematical
  specifications (WPI, Carlson TSI, HPI with critical threshold 100,
  Mann–Kendall with Hamed–Rao correction, SS_RMSE/NSE, VoI/EVSI), mandatory
  deliverable templates (Object Passport with an explicit [НЕТ ДАННЫХ] gap
  register, Circular-Economy Safety Gate), a JSON I/O-schema table for the
  scripts, and multi-agent governance. The Object Passport uses the skill's
  own 5-level maturity ladder (Prototype, Descriptive, Informative,
  Predictive, Decision). The I/O table was verified against the actual
  script interfaces and corrected where the draft described JSON contracts
  the scripts do not have (see the verification report).
- trend_test.py: WPI, Carlson TSI, and HPI functions plus `--mode
  wpi/tsi/hpi` and a JSON trend input (`{"values", "timestamps", "alpha"}`)
  with the spec output keys (`s_stat`, `var_s_raw`, `hamed_rao_factor`,
  `z_corrected`, `p_value`, `theil_sen_slope`, `trend`). The existing
  Hamed–Rao correction and CSV interface are unchanged.
- skill_scores.py: `ss_rmse` = 1 − RMSE_model/RMSE_naive, an `ss_rmse`
  output field, and the `admission_verdict` (ADMITTED if and only if
  SS_RMSE > 0 on the declared hold-out; null for in-sample fits). The
  existing MSE-ratio skill scores are kept and documented as differing from
  SS_RMSE in value while sharing the > 0 boundary.
- Zenodo DOI for v2.3: 10.5281/zenodo.23657185 (release 2026-10-26; author Baldanova, Rigjita, ORCID 0009-0009-7891-7007).
- Editorial cleanup (2026-10-26, pre-release): the draft meta-comment above the I/O table is replaced by a direct instruction, and the two template headings are demoted to #### so they no longer compete with ### Template 1 / 2.
- Verification fix (2026-10-25, independent check): Stage 7 wording corrected — forecast uncertainty is narrowed by assimilating observations, not by alert_bands.py (which recomputes the alert bands).
- Package completeness: all 9 scripts kept (evidence_search.py and
  uncertainty_budget.py included), tests/, examples/ (including Beira),
  references/, assets/templates.md kept; orchestration stays at
  references/orchestration.md.
- examples/beira/: worked example on Beira Lake (Colombo) from published data
  only — state against the authors' thresholds, cross-check with three
  independent studies (2024–2026), a Gate-B-style check of the source, the
  arithmetic of what a wetland alone can achieve (Carlson TSI), the value of
  information of a sludge analysis in relative units, a registered trial
  forecast, and the data gaps that keep the twin at maturity 2. Unit tests
  in tests/test_example_beira.py.
- Tests: T30 (WPI/TSI/HPI + index modes + JSON trend input), T31 (SS_RMSE
  and the admission boundary). Dry-run on the cascade case "water body →
  subcritical sludge processing → agricultural field" (see
  dry-run-cascade/dry-run-report.md).
- Release note: the CITATION.cff DOI is still the v2.2 release DOI
  (10.5281/zenodo.23608283); v2.3 gets a new Zenodo DOI at release, and the
  README citation block is updated then.

## v2.2 — 2026-10-21
- trend_test.py: the default correction for serial correlation is now the
  Hamed & Rao (1998) variance correction (detrended ranks, significant lags
  only; matches pymannkendall 1.4.3 to four decimals). Found on real data:
  for Lake Huron levels (lag-1 r = 0.76) trend-free pre-whitening raised
  |Z| from 5.2 to 7.2 — the correction must not make a trend look more
  certain; Hamed–Rao gives |Z| = 2.85. TFPW stays available with a warning.
  `--prewhiten` remains as a hidden alias.
- skill_scores.py: `--persistence fixed` (last training observation) for
  forecasts issued at the end of training; `rolling` (previous observation)
  stays the default for one-step forecasts. Comparing a multi-year
  forecast with one-step persistence was unfair to the model.
- analytics-forecasting.md: a Pettitt change point is a flag, not a
  verdict — it also fires on a smooth monotonic trend.
- examples/open-series-demo.md and open_series_demo.py: the core run on three public series
  (Nile flow, Lake Huron level, Mauna Loa CO2), reproducible with one command.
- Tests: 48 automated (Hamed–Rao reference value; fixed persistence).

## v2.1 — 2026-10-21
- Multi-model runner protocol (references/orchestration.md) for councils
  that run on other developers' models through a router: one execution host
  runs every script at a pinned skill version; council members are
  text-only and never compute numbers; briefs carry capped JSON summaries
  with manifest IDs, never raw client data or precise sensitive
  coordinates; the data flow and the client's consent are recorded before
  any client data enters a run; councils of three to five models from at
  least two developers, named by exact model ID and run date; every
  exchange logged into the provenance package, with a cost cap per run.
- No language model in the alert path: Phase 4 alerts come from
  alert_bands.py and go to a named human.
- Working rules: interactive builds proceed one phase at a time with a stop
  for the owner's approval; literature is cited only from a live search
  with recorded identifiers.
- qc_series.py, alert_bands.py and registry.py score cap long lists in the
  printed summary (--max-items, totals kept) and write the full record with
  --full-json.
- Passport template gains the multi-model run line (pinned version, host,
  providers, consent, model IDs, cost cap). Tests: 47 automated; T28–T29.

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
- Tests: tests/test_scripts.py (45 unit and end-to-end tests, network-free), tests/check_package.py
  (package lint), T19–T27 and a traceability table in TESTS.md. Contents
  lists added to the four references over 100 lines. READMEs rewritten for
  the repository page (process diagram, install instructions — the folder
  name must match the skill name — and an honest status section);
  CITATION.cff for GitHub's citation button; GitHub Actions run the tests
  and the strict lint on Python 3.9 and 3.12.

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
