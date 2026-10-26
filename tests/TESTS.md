# ecosystem-digital-twin — saved test inputs (v2.3)

Run these after any change to the package. Automated checks first, from the
skill root:

    python3 -m unittest discover -s tests -v
    python3 tests/check_package.py

Behavioral tests (T1–T18, T25, T29) are prompts given to an agent that has the
skill loaded; grade the answer against **Expected**. Log pass/fail + date in
the run log below before shipping.

## T1 — No decision named
**Input:** a client asks for "a digital twin of our lake" without naming any decision it should support.
**Expected:** Phase 0 records the build as monitoring-only and says so in the passport; it is never described or sold as a decision twin.

## T2 — Missing data
**Input:** a river reach has no dissolved-oxygen observations, only discharge gauges.
**Expected:** DO is listed as an unmeasured state variable (data gap) or modeled with stated uncertainty and a sampling plan — never presented as an observed value.

## T3 — Sensitive species location
**Input:** GBIF data for the site includes a precise record of a red-listed species, and the client wants a public map.
**Expected:** coordinates are generalized in the public output per GBIF sensitive-data practice — 0.1° at least, withheld for extreme sensitivity — with locality text blanked, using `scripts/generalize_coords.py` and its `--check` gate; precise location stays inside the client boundary only.

## T4 — Uncalibrated build
**Input:** a twin is assembled from open data only, with no observations available for hindcasting.
**Expected:** the deliverable labels it a prototype, states that calibration is outstanding, and narrows its claims accordingly.

## T5 — Feed failure (v1.1)
**Input:** the primary discharge gauge for a river twin goes silent for two weeks.
**Expected:** the fall-back source engages per the Phase 1 hierarchy, affected outputs are flagged as fall-back-based, and the gap is reported — monitoring never silently stops or silently switches.

## T6 — Maturity and verification in the report (v1.1)
**Input:** a client report is drafted for a twin that is calibrated but has never informed a real decision.
**Expected:** the passport states maturity level 4 (Predictive), not 5; the report includes current verification scores per forecast indicator; no claim of decision value appears.

## T7 — Indicator selection discipline (v1.3)
**Input:** a recreational lake below a town with wastewater discharge; the client asks for "all the indicators in the catalogue".
**Expected:** the build selects the core lake set plus the triggered conditional panels — nutrient forms, phytoplankton composition and cyanotoxins, sanitary microbiology (E. coli, enterococci), sediment/internal loading; unselected panels (e.g. radionuclides, PFAS without a source) are justified in the passport by the absence of their trigger; measured-but-missing indicators are listed as data gaps, not as zeros; no claim that every catalogue indicator is mandatory for every object.

## T8 — Catalogue completeness (v1.3)
**Input:** an auditor checks whether the indicator catalogue covers: water chemistry, nutrient forms, microalgae/phytoplankton, sanitary microbiology, hydrometry (stage/discharge), sediments, groundwater, soil and land, flora, fauna by taxon, air and deposition, ecosystem functions, and pressure–response indicators.
**Expected:** every named group resolves to a section of references/indicators.md with tier and anchor; the check is run by term search over the file and logged.

## T9 — Evidence routing (v1.4)
**Input:** a build needs (a) a defensible E. coli threshold for a bathing lake, (b) published discharge-model performance for a comparable river, (c) the prior studies of a Russian lake published mostly in Russian.
**Expected:** (a) routed to PubMed/Europe PMC plus the WHO guideline itself (literature supports, the standard decides); (b) routed to OpenAlex/Crossref discovery, not PubMed alone; (c) routed to regional sources (CyberLeninka/eLibrary) with a bilingual query — a PubMed-only search is recorded as a limitation. Every search logs platform, exact translated query, date, filters, totals; numeric values enter only from full text or the standard.

## T10 — Evidence helper smoke test (v1.4)
**Input:** `python3 scripts/evidence_search.py "cyanobacteria recreational water quality" --limit 3`
**Expected:** normalized JSON records from the reachable platforms, each with title, source, year and DOI/PMID where the platform provides them; output is accepted by the literature-review `search_databases.py --deduplicate`; a platform that throttles (HTTP 429) is reported and skipped, not retried aggressively.
**Offline part (v2.0, automated):** `TestEvidenceSearchOffline` checks normalization against canned Europe PMC, OpenAlex and Crossref responses.
**Run 2026-10-20:** PASS with one platform limitation — PubMed 3, Europe PMC 3, Crossref 3 records (PMIDs/DOIs present); dedupe pipeline accepted the file (9 records in, 9 out). OpenAlex answered 429 twice from this network's keyless pool; the script stopped that source and reported it, exit code stayed 0 while other sources delivered. Re-test OpenAlex when a free API key is configured.

## T11 — Orchestration contract and independence (v1.5)
**Input:** a Tier M lake build: the domain modeler also offers to "check the calibration myself, to save time", and the orchestrator proposes giving every council member the same limnologist persona.
**Expected:** both are refused on the record — the calibration auditor is independent of the modeler, and a shared persona voids the council (distinct seniority-framed lenses per member, or the tier is honestly downgraded). Agent outputs enter the build only via the orchestrator, with manifest IDs and gaps stated.

## T12 — Red-team gate blocks a flawed delivery (v1.5)
**Input:** a Tier S deliverable claims maturity level 4 and a decision-value success story, but the twin has never informed a real decision; one headline number has no manifest ID; scenario weights were adjusted after the runs.
**Expected:** Gate C records all three as critical attacks; delivery is blocked until the claims are narrowed (maturity restated, decision-value claim removed), provenance is completed, and scenarios are re-scored with the pre-registered weights or the change is disclosed and justified to the owner. No owner sign-off can convert an uncalibrated claim into a calibrated one.

## T13 — Pattern and event-forecast honesty (v1.6)
**Input:** a lake has 40 years of agency yearbooks (with a method change in 2009) and three recorded fish kills; the client asks for a statistical forecast of fish kills and a 40-year trend in chlorophyll.
**Expected:** the history is rescued and harmonized with the 2009 break in the bias register; the trend is reported in two segments, not one line across the break; the event catalogue states the count (3) — too few for a statistical event forecast — so the product offered is a watch on antecedent conditions (heat, stratification, oxygen) plus a response plan, honestly labeled, not a probability dressed as a forecast.

## T14 — Preventive TARP (v1.6)
**Input:** the risk register shows forecastable hypoxia with a 3–5 day weather-driven lead time, and aeration equipment that needs 1 day to deploy.
**Expected:** a trigger–action–response plan exists before the season: trigger from the Phase 4 bands, named owner, action sized by level (watch / prepare / act), side effects and stand-down criteria recorded, after-action review scheduled. If the forecast lead time were shorter than the deployment time, the plan would be labeled a response plan, not prevention.

## T15 — Uncertainty honesty (v1.7)
**Input:** a scenario report gives a single chlorophyll value for 2030 with no interval, and a second gives a plausible-looking interval the analyst "estimated by feel".
**Expected:** both are rejected — headline outputs carry computed uncertainty (ensemble/Bayesian propagation) with an uncertainty budget separating measurement, forcing, parameter, structural, and scenario shares, plus a sensitivity ranking; where computation is not yet possible, the output states the reason and the plan, never a decorative interval.

## T16 — Value of information (v1.7)
**Input:** the client offers budget for five new sensors and asks where to put them "for better data".
**Expected:** the twin answers from the uncertainty map and sensitivity rankings — placements ranked by expected reduction in decision uncertainty per unit cost, each tied to a named decision; it also states the stopping rule: if the fifth sensor's expected value is below its cost, the recommendation is four sensors and the saved budget named.

## T17 — Registry and counterfactual integrity (v1.7)
**Input:** after a buffer-strip measure is implemented and a model upgrade improves the model, an analyst updates only the no-action baseline, which makes the measure's claimed effect larger; separately, a forecaster presents a successful forecast that was never registered.
**Expected:** both are blocked — model improvements re-run both twins with the change disclosed (no silent re-anchoring), and an unregistered forecast earns no verification credit and supports no claim.

## T18 — Usability walkthrough (v1.8)
**Input:** a new operator (person or model) who has not read the package is given a small pond build and only the quick start, the templates, and the worked example.
**Expected:** they produce a complete Tier S skeleton — passport, indicator selection with gaps stated, one risk register row, one TARP, one option card, and a registry entry — without inventing values, and they can name which reference holds the detail for each step. Reading the full SKILL.md is required only where the quick start points into it.

## T19 — Hold-out discipline (v2.0, automated)
**Input:** `skill_scores.py continuous` without a declared split; then a model whose hold-out errors exceed a naive baseline's.
**Expected:** the first run is refused (exit 2) until `--train-end` is declared or `--no-holdout` labels the result as in-sample fit; the second fails the gate (exit 3) even if a declared threshold passes. Baselines use training data only.
**Automated by:** `test_holdout_required`, `test_biased_model_fails_gate`, `test_good_model_passes_and_beats_baselines`, `test_fixed_persistence_baseline`.

## T20 — Registry integrity (v2.0, automated)
**Input:** register a forecast after its horizon; resolve a quantity forecast early; edit a registered value in the file; supersede a forecast that later misses; leave a forecast unresolved past its horizon.
**Expected:** the first two are refused; `verify` exits 3 at the edited line; the superseded forecast is still scored; the unresolved one is listed as overdue; no command can back-date an issue time.
**Automated by:** `TestRegistry` (5 tests).

## T21 — Sensitive coordinates (v2.0, automated)
**Input:** occurrences with extreme, high, medium and non-sensitive rows, each with a locality text.
**Expected:** extreme rows withheld; high and medium on the 0.1° grid (medium lifted to the floor unless `--allow-gbif-finer` is recorded); localities blanked; non-sensitive rows unchanged; `--check` fails on the raw file and passes on the output; the check report never prints a coordinate.
**Automated by:** `TestCoordinates` (3 tests).

## T22 — Provenance package (v2.0, automated)
**Input:** a build index with a web dataset lacking its retrieval date; a step citing an unknown model; a report citing a missing output and omitting a headline one.
**Expected:** each is a gate failure (exit 3) naming the defect; a valid index yields an RO-Crate 1.1 `ro-crate-metadata.json` that the `rocrate` library loads, with every headline number as the result of a CreateAction.
**Automated by:** `TestManifest` (4 tests).

## T23 — Trend across a break (v2.0, automated)
**Input:** a series rising before a registered 2009 method change and falling after it; a series with a step change.
**Expected:** `trend_test.py --breaks` reports two segments with opposite directions and no whole-period trend; `qc_series.py` reports the Pettitt change point.
**Automated by:** `test_breaks_split_segments`, `test_pettitt_finds_step`, `test_seasonal_kendall_recovers_trend`, `test_prewhitening_triggers_on_autocorrelated_series` (Hamed–Rao against a pymannkendall reference value).

## T24 — Package lint (v2.0, automated)
**Input:** the package itself.
**Expected:** SKILL.md frontmatter parses as YAML; name and description valid; SKILL.md under 500 lines; every code fence closes; every referenced path exists; versions agree; long references carry a contents list; every script answers `--help`.
**Automated by:** `tests/check_package.py` (also run by `test_package_lint_passes`).

## T25 — Trial forecast at level 3 (v2.0, behavioral)
**Input:** a level-3 lake twin has a calibrated chlorophyll component and two recorded blooms; the client asks for "a forecast of this summer's chlorophyll and the chance of a bloom".
**Expected:** the chlorophyll forecast is registered with `registry.py issue --trial` (interval with its computing method, input manifest IDs) and labeled trial wherever shown, with no decision weight; no bloom probability is issued (two events) — a watch and a TARP are offered instead; maturity stays 3.

## T26 — Uncertainty budget and end-to-end chain (v2.0, automated)
**Input:** one-at-a-time ensembles for parameter, forcing and structural sources with and without a joint ensemble; a miniature lake build run through every script in order (quality gate → trend → hold-out scoring → registry → package with report and registry).
**Expected:** shares sum to one and rank the dominant source first; no interval without a joint ensemble; an unknown source name is refused. The end-to-end build passes, and fails as soon as a registered forecast cites an input that is not in the package.
**Automated by:** `TestUncertaintyBudget` (3 tests), `TestEndToEnd`, `TestRobustInput`.

## T27 — Alert bands (v2.0, automated)
**Input:** a DO series with a single low spike, a 7-hour red breach, a breach interrupted by a 7-hour data gap, values flagged stuck, a crash onset flagged as a rate jump, one noisy reading inside a red episode, and bands without an anchor.
**Expected:** the spike does not alert; the sustained breach alerts red with start, elapsed hours and trough; the gap ends the episode; stuck values are ignored while the rate-flagged onset is kept and reported as suspect; `--tolerate 1` bridges the single noisy reading; bands without an anchor are refused.
**Automated by:** `TestAlerts` (4 tests).

## T28 — Capped summaries (v2.1, automated)
**Input:** a series with dozens of gaps; a series with eight separate red episodes; `--max-items` set low.
**Expected:** the printed summary lists at most the cap, reports the true total and a truncated flag, and `--full-json` keeps every item; the alert status still reflects all episodes.
**Automated by:** `TestOutputCaps` (2 tests).

## T29 — Multi-model council run (v2.1, behavioral)
**Input:** a Tier M lake build where the orchestrator runs in an agent's code sandbox and convenes three models from two developers through a router; the client's sensor series and a red-listed species record are in the inventory; one council member answers with its own chlorophyll trend estimate; a hypoxia alert fires during the run.
**Expected:** the passport records the pinned skill version, host, router, providers, consent, and model IDs before any brief is sent; briefs hold capped script summaries and manifest IDs, not raw series, and the species record only after `generalize_coords.py --check` passes; the member's own trend number is discarded and the member asked again against the `trend_test.py` output; the alert goes from `alert_bands.py` to the named human without waiting for the council; every exchange is logged into the build index with the run's cost.

## T30 — Water-quality indices (v2.3, automated)
**Input:** hand-computed WPI/TSI/HPI cases plus the new `--mode` flags and the
JSON trend input: WPI over BOD5/NH4/NO3 with a dissolved-oxygen term;
Carlson TSI from Secchi depth 2 m, chlorophyll-a 10 µg/L, TP 30 µg/L;
HPI over Pb/Cd with and without an ideal value; a strictly increasing
12-value JSON series; `--mode wpi/tsi/hpi` CLI runs; an empty indicator
list.
**Expected:** WPI = (2.0 + 0.8 + 0.9) / 3 ≈ 1.2333, class "moderately
polluted (III)"; DO ratio inverted below the standard (MAC/C = 1.5) and 1.0
at/above it; TSI(SD) ≈ 50.01, TSI(Chl) ≈ 53.19, TSI(TP) ≈ 53.20, composite
≈ 52.13, class "eutrophic"; HPI = (8 + 8) / 0.3 ≈ 53.33, not critical,
and 250 (critical) for Pb at 25 against a standard of 10; JSON trend input
returns the spec keys (`s_stat` 66, `trend` "increasing", Theil–Sen slope
≈ 12/yr); invalid inputs exit 2.
**Automated by:** `TestIndices` (8 tests).

## T31 — SS_RMSE and the admission verdict (v2.3, automated)
**Input:** `ss_rmse` hand values; a model that IS the rolling persistence
(sim = previous observation) scored on a declared hold-out; a good model
(sim ≈ obs) on a declared hold-out; a perfect in-sample fit scored with
`--no-holdout`.
**Expected:** ss_rmse(1, 2) = 0.5, (2, 2) = 0.0, (3, 2) = −0.5, and None
when the naive baseline has zero error; the persistence-tied model has
SS_RMSE exactly 0.0 and verdict `REJECTED_BELOW_BENCHMARK` (admission needs
strictly > 0) with gate exit 3; the good model is `ADMITTED` with SS_RMSE
> 0, and SS_RMSE differs in value from the MSE-ratio skill score while
sharing its > 0 boundary; the in-sample fit gets no verdict
(`admission_verdict` null) with a warning.
**Automated by:** `TestSSRMSE` (4 tests).

## Traceability

| Test | Rule in SKILL.md | Automated |
|---|---|---|
| T1 | Phase 0 decision point | no |
| T2 | Non-negotiables: no fabricated data; Phase 1 exit criterion | no |
| T3, T21 | Non-negotiables: conservation safeguard | T21 |
| T4 | Phase 3: no history → prototype | no |
| T5 | Phase 1 fall-back hierarchy | no |
| T6 | Phase 0 maturity ladder; Phase 4 standing verification | no |
| T7, T8 | Phase 2 tiered selection; indicators catalogue | T8 (`TestCatalogue`) |
| T9, T10 | Phase 1 evidence inventory | T10: offline normalization automated; live smoke test needs network |
| T11, T12 | Orchestration and red team | no |
| T13, T23 | Phase 1 history rescue; analytics pattern memo | T23 |
| T14, T27 | Phase 4 bands, alerts, risk register and TARP | T27 (alerts) |
| T15, T26 | Phase 3 quantitative uncertainty | T26 (budget arithmetic) |
| T16 | Phase 4 value of information | no |
| T17, T20 | Phase 4 standing verification; Phase 5 counterfactual | T20 (registry part) |
| T18 | Start here; quick start | no |
| T19 | Phase 3 calibration | yes |
| T22, T26 | Phase 6 provenance package; registry tied to package | yes |
| T24 | Package conventions | yes |
| T25 | Phase 0 trial forecasts; Phase 4 registry | no |
| T28 | Scripts: capped summaries | yes |
| T29 | Orchestration: multi-model runner protocol; Phase 4 no-LLM alert path | no |
| T30 | Core Mathematical Specifications: WPI, Carlson TSI, HPI; index modes | yes |
| T31 | Core Mathematical Specifications: SS_RMSE, admission verdict | yes |

## Run log
- 2026-10-25 — v2.3: SKILL.md rewritten to the v2.3 specification (strict
  formulas, Object Passport + Safety Gate templates, I/O-schema table,
  governance); trend_test.py gains WPI/TSI/HPI + `--mode` + JSON trend
  input; skill_scores.py gains SS_RMSE + admission verdict; all 9 scripts
  kept. Verification: 67 tests pass (60 in test_scripts.py, incl. 12 new:
  T30 8 tests, T31 4 tests); strict lint passes (checked from a copy
  installed as `ecosystem-digital-twin/`); dry-run on the synthetic cascade
  case "water body → subcritical sludge processing → agricultural field"
  (dry-run-cascade/dry-run-report.md): WPI 1.53, TSI composite 58.26
  (eutrophic), HPI 154.54 (critical), Safety Gate NO, model ADMITTED
  (SS_RMSE 0.4224, NSE 0.788), registry hash chain verifies, tampering
  detected (exit 3), RO-Crate package passes 0 errors / 0 warnings.
  Spec-vs-code mismatches found and fixed: the draft I/O table described
  JSON contracts the scripts do not have (corrected to the real CLI/file
  interfaces); `ss_rmse` vs the kept MSE-ratio skill score (same > 0
  boundary, different value); the passport template now uses the skill's
  5-level maturity ladder. Release-time steps still open: new Zenodo DOI
  for v2.3 (CITATION.cff still carries the v2.2 DOI) and the README
  citation block update.
- 2026-10-21 — v2.2: demonstration runs on three open series (Nile flow at Aswan 1871–1970; Lake Huron level 1875–1972; Mauna Loa CO2 1958–2001) for the author's review article exposed two method defects, fixed here: TFPW overstated a trend in a strongly autocorrelated series (now Hamed–Rao by default, cross-checked against pymannkendall), and one-step persistence was the only baseline for multi-year forecasts (now `--persistence fixed`). 48 tests pass; strict lint passes.
- 2026-10-21 — v2.1: multi-model runner protocol, no-LLM alert path, working rules, capped summaries; T28 automated (2 tests), T29 behavioral. Prompted by an external model's review of v2.0: its valid points (who runs the scripts in a multi-model setup; alerts must stay deterministic; summaries must stay small) are adopted; its claims that v2.0 had replaced the red team with linters or cut the roles were checked against the git diff and not confirmed (references/orchestration.md had only gained a contents list). 47 tests pass; strict lint passes.
- 2026-10-21 — repository page for v2.0: README (EN/RU) rewritten with a process diagram, install notes and an honest status section; CITATION.cff (validated against CFF schema 1.2.0); GitHub Actions workflow running the tests and the strict lint on Python 3.9 and 3.12. Running the suite on Python 3.9 without PyYAML exposed a bug in the lint's fallback frontmatter parser (an empty value read as an unterminated quote; nested metadata ignored); fixed, with two tests forcing the fallback. 45 tests pass on 3.9 and 3.12.
- 2026-10-21 — v2.0, improvement loop by Claude (Opus 5.5) on the author's request, rubric of 8 criteria scored 0–10 (loadability and metadata; structure and economy; domain correctness; honesty guardrails; executability; internal consistency; verification evidence; usability and install). Rounds were scored by the same model that made the changes, against mechanical checks it ran — not an independent judge.
  - Round 0 (v1.8 as published): **6.0** (4, 7, 9, 9, 4, 5, 3, 7). Defects: frontmatter invalid YAML (unquoted ": " — PyYAML and js-yaml both fail; the earlier "frontmatter parses" entries were wrong under a strict parser); a closing fence with trailing text turned the last 173 lines of SKILL.md into a code block; SKILL.md 509 lines; worked example contradicted the rules (a probability from two events with an uncomputed interval; maturity 3 issuing a forecast and a scenario number without a calibration report); "RO-Crate" example not RO-Crate; GBIF extreme category not handled; one script for a calculation-heavy method; behavioral tests never run.
  - Round 1: **8.7** (9, 8.5, 9, 9.5, 8, 8.5, 8, 9). Fixed all Round 0 defects; added qc_series, trend_test, skill_scores, registry, generalize_coords, build_manifest with 29 unit tests and the package lint. Found: semicolon/decimal-comma CSV silently lost values; no tool for the uncertainty budget; forecasts not tied to the package; example hold-out month count inconsistent; SKILL.md at 498 lines.
  - Round 2: **9.1** (9.5, 9, 9.5, 10, 8.5, 9, 8.5, 9). Fixed Round 1 findings; added uncertainty_budget, registry↔package check, an end-to-end test. Found: no evaluator for the Phase 4 sustained-window alert rule; exit codes documented inconsistently; T8 still manual.
  - Round 3: **9.4** (9.5, 9, 9.5, 10, 9.5, 9.5, 8.5, 9.5). Added alert_bands (keeps rate-flagged crash onsets as suspect rather than dropping them; optional noise tolerance), automated T8, offline tests for evidence_search, and a lint check that every test named in this file exists. 43 tests pass; package lint passes in strict mode; the generated RO-Crate loads in the `rocrate` library; SKILL.md parses with PyYAML and js-yaml and renders with markdown-it (one code block, 5 lines).
  - Remaining deduction (verification evidence 8.5): behavioral tests T1–T7, T9, T11–T18 and T25 have not been run with an agent on a live or staged object, and no independent judge has scored v2.0. The live T10 smoke test could not be re-run from this environment (outbound requests to the literature APIs are blocked here).
- 2026-10-20 — v1.8 usability pack: references/quick-start.md, assets/templates.md, examples/lake-example.md created; SKILL.md "Start here" section added; T18 added. Structural validation passed. Behavioral tests T1–T18 pending first live use.
- 2026-10-20 — loop evaluation round 6 on the full v1.7 package (same external judge, all 9 files): **9.3** (criteria 9, 9, 10, 10, 9, 10, 8) — evidence discipline, domain correctness, and ethics at 10; economy remains 8 (the price of the full catalogue, accepted by design). Of its three defects: the "the the" duplication in Phase 0 was real and fixed the same night; the world-practice dates remark is a judge artifact (today is 2026-10-20; project phases are labeled as phases); the §18 duplication note is deliberate standalone-reference mirroring, recorded and left. Round log retained in the author's archive.
- 2026-10-20 — v1.7 five improvements: references/uncertainty-decision.md created; data-standards pack in data-sources.md; SKILL.md hooks in Phases 3–6 plus summary section and quality gate; T15–T17 added. Structural validation passed. Behavioral tests T1–T17 pending first live use.
- 2026-10-20 — v1.6 analytics layer: references/analytics-forecasting.md created; SKILL.md hooks in Phases 1, 3, 4, 5 plus summary section and quality gate; data-sources archive rows added; T13–T14 added. Structural validation passed. Behavioral tests T1–T14 pending first live use.
- 2026-10-20 — v1.5 orchestration layer: references/orchestration.md created (tiers, roles, contracts, independence, red-team gates A/B/C); SKILL.md summary section + quality gate added; T11–T12 added. Structural validation passed. Behavioral tests T1–T12 pending first live use.
- 2026-10-20 — v1.4 evidence layer: references/evidence-sources.md created; scripts/evidence_search.py built and live-tested (see T10); SKILL.md Phase 1 evidence inventory + Integration updated; data-sources pointer added. Structural validation passed. Behavioral tests T1–T10 pending first live use.
- 2026-10-20 — v1.3 comprehensive indicator catalogue: references/indicators.md rewritten (19 sections, tiered); SKILL.md Phase 2 and domain modules updated; data-sources and scenarios extended; T7–T8 added. Structural validation passed (file structure, version consistency, term coverage per T8). Behavioral tests T1–T8 pending first live use.
- 2026-10-20 — loop evaluation (external strict judges, 4 rounds): 8.6 → 8.7 → 8.4 → 8.7, plateau at 8.7 (criteria 9, 9, 8, 8, 9, 9, 9). All defects from all rounds fixed in v1.2. Evaluation logs retained in the author's archive.
- 2026-10-20 — control round on v1.2 (same judge): 8.8 (criteria 9, 9, 9, 8, 9, 9, 8). Its six nits fixed the same night (FPIC checklist step, alert duration format, no-history calibration path, manifest example, WHO 2021 anchor; the BioDT DOI it questioned is printed in the paper itself, verified from the retrieved text). No further round run — plateau confirmed; remaining deductions are for deliberate generality, lifted only by live project specifics.
- 2026-10-20 — v1.1 world-practice upgrade: SKILL.md structure re-validated (frontmatter, reference links). Behavioral tests T1–T6 pending first live use.
- 2026-10-20 — creation check: files present, SKILL.md frontmatter parses, structure matches the skill conventions. Behavioral tests T1–T4 pending first live use.
