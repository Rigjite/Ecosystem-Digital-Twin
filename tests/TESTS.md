# ecosystem-digital-twin — saved test inputs (v2.8)

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

## T32 — Forecast cadence and lead time (v2.4, automated)
**Input:** `registry.py issue` with `--cadence seasonal --lead-time 90 --lead-time-unit days`; with `--cadence sometimes`; with `--lead-time 0`, `--lead-time -5`, and `--lead-time-unit weeks` without a `--lead-time`; with `--lead-time 48 --lead-time-unit hours` and with `--lead-time 3` (no unit); a registry record hand-written with an invalid `cadence` (valid hash) and one with a negative `lead_time` value (valid hash); a forecast issued with neither new field.
**Expected:** the first issue records `cadence` "seasonal" and `lead_time` {"value": 90.0, "unit": "days"} and verifies; the invalid cadence is refused (exit 2); a zero or negative lead time is refused (exit 2); a unit without a value is refused (exit 2); `--lead-time 48 --lead-time-unit hours` records hours, and a `--lead-time` without a unit defaults to "days"; each hand-written invalid record fails `verify` (exit 3) at its line, naming the field; the record without the new fields carries `cadence` null and `lead_time` null and still verifies.
**Automated by:** `TestRegistryCadenceLeadTime` (5 tests).

## T33 — Data-onboarding checklist presence (v2.4, automated)
**Input:** the package text itself: SKILL.md Stage 2 and Object Passport template; `assets/templates.md` §1 and §5.
**Expected:** SKILL.md names the Phase 1 checklist with all five items (source and access date; licence; resolution and coverage; QC performed; gaps → [НЕТ ДАННЫХ]); the passport template carries the onboarding line; `assets/templates.md` §1 carries the per-dataset onboarding line and §5 carries the refresh-cadence and lead-time fields.
**Automated by:** `TestOnboardingChecklist` (2 tests).

## T34 — FAIR Signposting in the manifest (Round 1 of the v2.5 program, automated)
**Input:** a build index with `doi` "10.5281/zenodo.23657185" and licence URL; the same index without `doi`; the same index with `doi` "doi.org/10.5281/zenodo.23657185" and bare licence "CC-BY-4.0".
**Expected:** with a DOI, the crate's Root Dataset carries `identifier` "https://doi.org/10.5281/zenodo.23657185" and a `signposting` list of exactly `cite-as` (DOI URL), `describedby` (`ro-crate-metadata.json`, type `application/ld+json`), `license` (licence URL); without a DOI there is no `identifier` and no `cite-as` entry — nothing invented — while `describedby` and `license` remain; a bare DOI is normalized to the https://doi.org/ URL and a bare licence string yields no license link.
**Automated by:** `TestSignposting` (3 tests).

## T35 — Scenario taxonomy, scenario card, handover note (Round 1 of the v2.5 program, automated)
**Input:** the package text itself: SKILL.md Stage 4 and Object Passport template; `references/scenarios.md`; `references/uncertainty-decision.md` §4; `assets/templates.md` §1 and §6.
**Expected:** SKILL.md Stage 4 names the three scenario classes (Scenario 0 No-Action counterfactual, Planning, What-if intervention) and the rule that a scenario without a declared class is not scored; `references/scenarios.md` carries the taxonomy section; `references/uncertainty-decision.md` §4 still freezes the no-action baseline and points at the taxonomy as class 0; `assets/templates.md` §6 is the scenario card with the class field and §1 carries the handover line; SKILL.md Template 1 carries the handover line and the Companion Documents count was six forms at Round 1 (eight since Round 3).
**Automated by:** `TestTaxonomyHandover` (2 tests).

## T36 — Recalibration trigger (Round 2 of the v2.5 program, automated)
**Input:** `trend_test.py --mode drift --baseline <calibration>` on a new batch: a level-shifted batch (mean 14 against a calibration mean 10, sd ~1); a stable batch (mean 10); a rising batch (8 → 12, same mean as the calibration); a stable batch with one wild row (50.0) flagged `range` in a `qc_flag` column; a run without `--baseline` and a batch of 2 values.
**Expected:** the shifted batch fires the trigger (`trigger` true, `action` "recalibrate", `drift_level` > 2, trend quiet); the stable batch stays quiet (`trigger` false, `action` "no action", `drift_level` < 0.5, trend quiet); the rising batch fires on trend alone (`level_fires` false, `trend_fires` true, Sen slope ≈ +5.3/yr outside the calibration slope's confidence interval); the flagged wild row is excluded (`rows_excluded_qc` 1) and the batch stays quiet; both input errors exit 2.
**Automated by:** `TestDrift` (5 tests).

## T37 — Continuous revalidation (Round 2 of the v2.5 program, automated)
**Input:** `skill_scores.py revalidate <combined series> --train-end <original split> --previous-verdict ADMITTED --previous-ss-rmse 0.4`: a new batch the model still tracks (sim ≈ obs); the same setup with the model stuck at a constant in the new batch; a run without `--train-end`.
**Expected:** the good batch keeps admission (exit 0, SS_RMSE > 0.9, verdict ADMITTED, `transition` "ADMITTED -> ADMITTED", `revoked` false, `maturity_action` "keep"); the degraded batch revokes it (exit 3, SS_RMSE < 0, verdict REJECTED_BELOW_BENCHMARK, `status` NOT_ADMITTED, `transition` "ADMITTED -> NOT_ADMITTED", `revoked` true, `maturity_action` "drop"); the run without `--train-end` exits 2.
**Automated by:** `TestRevalidate` (3 tests).

## T38 — Two tiers: Focus Application and What-if Scenario (Round 3 of the v2.5 program, automated)
**Input:** the package text itself: `assets/templates.md` §7 and §8; SKILL.md Stage 6 and Companion Documents.
**Expected:** `assets/templates.md` §7 is the Focus Application form (purpose, object and nodes, inputs with manifest IDs, outputs, builder, maturity targeted, update cadence) and §8 is the What-if Scenario form (decision, options compared with scenario IDs and classes, evidence per option, recommendation, what would change it, decision-maker and date), distinct from the §6 scenario card, which records a single scenario; SKILL.md Stage 6 names the two tiers (Focus Applications for builders, What-if Scenarios for decision-makers) and the Companion Documents count is eight forms.
**Automated by:** `TestTwoTiers` (2 tests).

## T39 — Explainability under pressure and multi-source fusion checklist (Round 3 of the v2.5 program, automated)
**Input:** the package text itself: SKILL.md Stages 2 and 6 and Object Passport template; `references/uncertainty-decision.md` §1; `references/data-sources.md`; `assets/templates.md` §1 and §6.
**Expected:** SKILL.md Stage 6 states the explainability rule (what the model used, what it did not use, confidence — no black-box verdicts) and the §6 scenario card carries an "Explanation" field; `references/uncertainty-decision.md` §1 carries the explainability paragraph; SKILL.md Stage 2 names the fusion checklist (coverage, resolution, alignment, cross-source consistency checks, gaps → [НЕТ ДАННЫХ]) as an extension of the onboarding checklist; `references/data-sources.md` carries the fusion section and a Contents list; the Object Passport template and `assets/templates.md` §1 carry the fusion line; Scenario 0 is unchanged (frozen baseline, class 0).
**Automated by:** `TestExplainabilityFusion` (2 tests).

## T40 — Prototype gallery: one working twin per task type (Round 4 of the v2.5 program, automated)
**Input:** the five gallery entries under `examples/gallery/` and the gallery index `examples/gallery.md`.
**Expected:** each `run.py` runs clean and prints a summary JSON whose expected outputs match the run: pond — TP trend increasing (p < 0.01), TSI composite 65.1 eutrophic, calibration gate pass, ADMITTED, SS_RMSE > 0.9, alerts red (3 amber, 1 red); river — no significant trend, max flow 625.8 m³/s, 9 days above amber, 4 above red, alerts red (1 red); field — moisture trend decreasing (p < 0.01), 26 days below amber, 3 below red, alerts red (1 red); air — no significant trend, 10 days above amber, 4 above red, alerts red (1 red); re-located Oct 26, 2026 from Ulan-Ude to Prince George, BC (new synthetic series, same question and bands; see the run log); biodiversity — 20 records, 18 species, 19 generalized to the 0.1° grid, 1 withheld (the *Emberiza* record), check gate pass, 0 violations, 18 species in 4 cells of 0.1°, at most 7 species in one cell; replaced Oct 26, 2026 (Gusinoye removed by the author's decision, Khubsugul lakeshore birds, Mongolia, synthetic records — the GBIF pull was blocked, HTTP 403; see the run log). `examples/gallery.md` lists all five entries with question, data provenance, and maturity; SKILL.md Companion Documents names the gallery.
**Automated by:** `TestGallery` (6 tests).

## T41 — Wetland gallery prototype: Everglades treatment wetland + marsh (first item of the v2.6 program, automated)
**Input:** the wetland gallery entry under `examples/gallery/wetland/` (`nutrients.csv`, `level.csv`, `run.py`, `README.md`) and the gallery index `examples/gallery.md`.
**Expected:** `run.py` runs clean and prints a summary JSON whose expected outputs match the run: 13 monthly TP rows, 0 QC flags; median removal 35.4%, mean 33.6% (document's stated mean 33.3%), Beira reference median 46%; removal trend no significant trend (p ≈ 0.23); level 121 daily rows, 0 QC flags, decreasing trend (p < 0.001, Sen −2.60 ft/yr), start 6.10 ft, min 5.26 ft, end 5.48 ft, 14 days below amber, 8 below red; outflow TP alerts red (1 amber, 2 red); level alerts red (2 amber, 2 red). `examples/gallery.md` lists the wetland entry with question, data provenance, and maturity; SKILL.md Companion Documents names the wetland.
**Automated by:** `TestWetland` (2 tests).

## T42 — Forest-fire gallery prototype: Prince Albert FMA fire seasons (second item of the v2.6 program, automated)
**Input:** the forest-fire gallery entry under `examples/gallery/forest-fire/` (`fires.csv`, `run.py`, `README.md`) and the gallery index `examples/gallery.md`.
**Expected:** `run.py` runs clean and prints a summary JSON whose expected outputs match the run: 49 monthly rows (Apr–Oct 2019–2025), 0 QC flags on both series; fire-count trend increasing (seasonal Kendall, p ≈ 0.011, Sen +0.17/month per year); burned-area trend increasing (p ≈ 0.0012, Sen +210 ha/month per year); biggest season 2025 (62 fires, 128,830 ha); 2019 season 101,400 ha and 2021 season 90,405 ha; 13 months above amber and 7 above red for counts, 17 and 5 for area; fires alerts red (4 amber, 1 red); area alerts red (4 amber, 1 red). `examples/gallery.md` lists the forest-fire entry with question, data provenance, and maturity; SKILL.md Companion Documents names the forest fire. The data are synthetic (deterministic formulas) with design anchors from the CIFFC 2023 national record, Saskatchewan 2023, and the Prince Albert FMA; the README documents the real-data check (FIRMS API key, 7-day NRT files, gridded products, no published annual series for the FMA).
**Automated by:** `TestForestFire` (2 tests).

## T43 — Forest-logging gallery prototype: British Columbia timber supply areas (third item of the v2.6 program, automated)
**Input:** the forest-logging gallery entry under `examples/gallery/forest-logging/` (`logging.csv`, `run.py`, `README.md`) and the gallery index `examples/gallery.md`.
**Expected:** `run.py` runs clean and prints a summary JSON whose expected outputs match the run: 11 annual rows (2015–2025), 0 QC flags on both series; logged-area trend increasing (p ≈ 5.2e-05, Sen +1,220 ha/yr); harvest-volume trend increasing (p ≈ 5.2e-05, Sen +272,750 m³/yr); biggest year 2025 (30,600 ha, 6,426,000 m³); Prince George is the largest district (47.0% of the 2015–2025 total; Quesnel 31.0%, Mackenzie 22.0%); 2015 total 17,900 ha / 3,436,800 m³; 2020 total below 2019 (slowdown dip); 4 years above amber and 2 above red for both area and volume; area alerts red (1 amber, 1 red); volume alerts red (1 amber, 1 red). `examples/gallery.md` lists the forest-logging entry with question, data provenance, and maturity; SKILL.md Companion Documents names the forest logging. The data are synthetic (deterministic formulas) with design anchors from BC harvest totals and the Prince George / Quesnel / Mackenzie AACs; the README documents the real-data check (GFW data API key, JavaScript-driven dashboard/map pages, gridded products, BC regional totals only).
**Automated by:** `TestForestLogging` (2 tests).

## T44 — Forest-carbon gallery prototype: Prince Albert FMA carbon stock (third forest entry, fourth item of the v2.6 program, automated)
**Input:** the forest-carbon gallery entry under `examples/gallery/forest-carbon/` (`carbon.csv`, `run.py`, `README.md`) and the gallery index `examples/gallery.md`.
**Expected:** `run.py` runs clean and prints a summary JSON whose expected outputs match the run: 11 annual rows (2015–2025), 0 QC flags; carbon-density trend increasing (p ≈ 2.6e-05, Sen +0.208 t C/ha/yr); net-change trend decreasing (p ≈ 0.039, Sen −0.017 t C/ha/yr); total stock 140.40 Mt C (2015) rising to 145.58 Mt C (2025), +5.18 Mt C (+3.7%); smallest growth year 2025 (+0.04 t C/ha/yr, density 53.92 t C/ha); 3 years below amber and 0 below red for net change; change alerts amber (1 amber, 0 red) — the amber episode 2024–2025 is ongoing. The density series rises through the window, so there is no low-density watch: the decision-relevant signal is the net change. `examples/gallery.md` lists the forest-carbon entry with question, data provenance, and maturity; SKILL.md Companion Documents names the forest carbon; the README states the carbon-credit boundary (not a carbon-credit methodology, no compliance with Verra, Gold Standard, or any other credit standard). The data are synthetic (deterministic formulas) with design anchors from UNEP boreal biomass, Alberta sequestration, and the forest-fire entry's burned areas; the README documents the real-data check (ESA CCI Biomass raster, GFW data API key, FIA multi-table harmonisation and US data, National Forest Inventory totals only).
**Automated by:** `TestForestCarbon` (2 tests).

## T45 — Impact chain (Round 1 of the v2.7 program, automated)
**Input:** `references/scenarios.md` ("Impact chains" section) and the §6 scenario card in `assets/templates.md`.
**Expected:** each impact chain is driver → exposed asset → impact, with the published function, its source, its applicable range, and its limits per link; a link with no published function goes to the [НЕТ ДАННЫХ] register and is never invented; a chain with a missing link reports the impact as unquantified, not as zero. The chain is arithmetic on the existing scripts' outputs — no new code.
**Automated by:** `TestImpactChain` (1 test).

## T46 — Event storyline (Round 1 of the v2.7 program, automated)
**Input:** the scenario taxonomy in `references/scenarios.md` and the §6 scenario card in `assets/templates.md`.
**Expected:** the taxonomy has four classes (0 No-Action counterfactual, Planning, What-if intervention, Storyline); a Storyline names an event from the object's own record, states the drivers changed and what is held fixed, and states the impact scored; the boundary vs replay is stated in both `references/scenarios.md` and `references/uncertainty-decision.md` §5 (storyline replays under changed drivers — a scenario; replay runs the pipeline on the event as it happened — a verification).
**Automated by:** `TestStoryline` (1 test).

## T47 — Historical-event replay (Round 1 of the v2.7 program, automated)
**Input:** `scripts/registry.py replay` on a temp copy of the Beira registry, with a synthetic series whose alert start is computed by `scripts/alert_bands.py`.
**Expected:** the replay record carries type "replay", event (named), event date, data cutoff, alert fired (yes/no), lead time in days (when the alert fired), method, inputs (manifest ids), model and version; the chain verifies (2 records); `score` ignores replay records (no forecast rows for them); the real Beira registry still verifies with 1 record. Refused (exit 2): data cutoff after the event date, an alert that fired with no lead time, a miss claiming a lead time, a duplicate replay id.
**Automated by:** `TestReplay` (3 tests).

## T48 — Stochastic scenario generator (Round 1 of the v2.7 program, automated)
**Input:** `scripts/scenario_generate.py` on a small driver series.
**Expected:** the fitted mean, sample SD and lag-1 autocorrelation match hand values (mean 11.6, SD ≈ 1.1402, rho ≈ −0.2231 for [10, 12, 11, 13, 12]); the same seed produces a byte-identical CSV and a different seed produces different draws; the output has the input's length and N+1 columns; the first draw of scenario 1 pins the RNG stream (mean + SD × gauss). With `--watch`, the summary reports the breach share in [0,1] (0 for an unreachable band, 1 for a band every value crosses). Every generated value is labelled a scenario draw, never a measurement.
**Automated by:** `TestScenarioGenerate` (5 tests).

## T49 — Hazard quotient / hazard index (Round 1 of the v2.7 program, automated)
**Input:** `scripts/trend_test.py --mode hq` on a JSON `{"stressors": [...]}` list.
**Expected:** HQ = exposure / reference per stressor; HI = the sum, split acute/chronic; 1 is the safety line. The Bychkov fire-smoke acute triple (suspended solids 11.3, formaldehyde 1.4, carbon monoxide 1.2) gives HI acute 13.9, unsafe; a safe case (PM2.5 0.4 + NO2 0.5) gives HI 0.9, not unsafe. Refused (exit 2): empty stressor list, reference ≤ 0, negative exposure, unknown duration, missing reference. `references/indicators.md` §6 documents HQ/HI beside HPI and states the honest note (same quotient family as HPI, but HPI covers only metals in water on a 100-scale).
**Automated by:** `TestHazardQuotientIndex` (5 tests).

## T50 — Covariate-aware alerts (Round 1 of the v2.7 program, automated)
**Input:** `scripts/alert_bands.py --explained-by driver.csv --driver-amber ">=25"` on a main series with a sustained breach and a driver series.
**Expected:** a breach overlapping a sustained driver episode is logged in `explained_breaches` (with the driver episode that explains it) and does not alert, does not set the status, and does not count for `--fail-on`; a breach with no driver episode alerts; a brief driver spike explains nothing. Refused (exit 2): `--explained-by` without `--driver-amber`, missing driver file, missing driver column. `references/indicators.md` §20 documents the rule; the §6 scenario card carries an Alerts field naming the driver and its bands.
**Automated by:** `TestCovariateAwareAlerts` (6 tests).

## T51 — Alert trial (Round 1 of the v2.7 program, automated)
**Input:** `scripts/skill_scores.py alert-trial` on a CSV with one row per alert or critical event (kind, relevant).
**Expected:** precision = relevant alerts / all alerts; miss rate = missed critical events / all critical events; alarm volume = the alert count. Verdict PASS at precision 0.9 with zero missed criticals (the Wessex-shape trial: 9 relevant of 10 alerts, 2 critical events both alerted); FAIL (exit 3) when precision is below the minimum, when a critical event is missed, or when the alarm count exceeds `--max-alarms`; FAIL when critical events are present but no alerts fired (the model stayed silent when it mattered). A window with no alerts AND no critical events is INCONCLUSIVE_QUIET_WINDOW (exit 0): nothing to score — it neither admits nor rejects, and admission waits for a synthetic stress-test or a historical extreme replay. Refused (exit 2): unknown kind, non-binary relevant, missing column. `references/uncertainty-decision.md` §3 states the trial is a separate gate from model admission — both must pass.
**Automated by:** `TestAlertTrial` (9 tests).

## T52 — Calibration plausibility gate (Round 1 of the v2.7 program, automated)
**Input:** `scripts/skill_scores.py admit` on a JSON dossier `{"variables": [{"name", "ss_rmse", "primary" (optional)}], "parameters": [{"name", "value", "bounds": [lo, hi], "source"}]}`.
**Expected:** ADMITTED (exit 0) when every PRIMARY target variable's SS_RMSE > 0 and every fitted parameter is inside its declared bounds; a secondary background variable below the benchmark does not block admission (buffered pH at SS_RMSE −0.05 with primaries passing → ADMITTED), and the output echoes each variable's `primary` flag. REJECTED (exit 3) naming the offending parameter when a parameter is outside its bounds even with SS_RMSE > 0 (growth rate 3.5 against bounds [0.2, 2.0] — Reynolds 2006), and when any PRIMARY variable's SS_RMSE ≤ 0. Backward compatibility: when no variable in the dossier carries a `primary` flag, every variable is primary (the pre-2.7 behaviour) — a background variable below the benchmark then blocks admission. Refused (exit 2): empty variables list, missing ss_rmse, inverted bounds, malformed JSON, missing file. `references/calibration-bounds.md` states the bounds come from the literature, not from the fit; SKILL.md Stage 3 states the two gates, both must pass.
**Automated by:** `TestAdmit` (8 tests).

## T53 — Virtual sensors (Round 2 of the v2.7 program, automated)
**Input:** the Object Passport in `assets/templates.md` §1 and the "Client and sensor data" section of `references/data-sources.md`.
**Expected:** the passport carries a "Virtual sensor" block (name, physical quantity, proxy source + deterministic formula, calibration station, skill score against it (SS_RMSE), validity window, QC and alert machinery as a physical sensor; when the proxy leaves calibration, its readings go to the [НЕТ ДАННЫХ] register — never silently used); `references/data-sources.md` lists satellite proxies as virtual-sensor sources (Sentinel-2 chlorophyll-a, Landsat water temperature; Gironde: 120 virtual sensors — a published formula and a skill score, no ML).
**Automated by:** `TestVirtualSensor` (2 tests).

## T54 — Deterministic drift / connectivity (Round 2 of the v2.7 program, automated)
**Input:** `scripts/drift.py` on release-points, current-vector, and target-zone CSVs.
**Expected:** displacement = (current + leeway × wind) × dt; 1° lat = 111,320 m, 1° lon = 111,320 × cos(lat) m evaluated at the particle's latitude each step; arrival = first step inside a target zone (a release point inside a zone arrives at 0 hours). Output JSON: per zone arrivals, connectivity (fraction of released particles arriving), median travel time (null when none arrives); per particle arrived zone and travel hours (null when it never arrives). Hand-verified: constant current u = 0.5 m/s east at 50°N = 0.025152° lon/hour; 0.1° takes 4 steps → connectivity 0.5 (2 release points, 1 arrives), median travel 4.0 h; with leeway 0.5 × wind-u 1.0 m/s the speed doubles → 2.0 h. Refused (exit 2): missing columns, non-numeric values, non-positive step or max hours, empty release or target tables.
**Automated by:** `TestDriftModule` (5 tests).

## T55 — Daily forecast bulletin (Round 2 of the v2.7 program, automated)
**Input:** `scripts/forecast_bulletin.py` on a temp registry with a forecast entry (issued via `scripts/registry.py issue`) and an observations CSV.
**Expected:** the bulletin is one page of Markdown with the forecast id and target, issued time, model, refresh cadence and usable warning lead time, the observed value today (latest observation, with date), the forecast value with interval and interval method, the watch status of the latest observation and of the forecast value (against `--amber`/`--red`, else "not stated (no bands given)"), and "This forecast will be scored on <horizon-end> against the <metric> metric, exactly as issued." Trial forecasts carry a "Trial forecast — no decision weight" line. The bulletin renders the registry; it changes no numbers. Refused (exit 2): missing file, unknown id, record not a forecast, missing columns, no observations, bad band spec, bands pointing different ways, red inside amber. The "Forecast bulletin" form exists in `assets/templates.md` §9.
**Automated by:** `TestForecastBulletin` (4 tests).

## T56 — Public status line (Round 2 of the v2.7 program, automated)
**Input:** the "Public status line" form in `assets/templates.md` §10 and the Stage 6 rule in SKILL.md.
**Expected:** the form is one paragraph in plain language — current state, what changed since the last status line, the maturity label, the [НЕТ ДАННЫХ] gaps — generated from the runner's summary JSON, for the client and the public, distinct from the handover note (for a successor builder, technical) and from RO-Crate (for machines). SKILL.md Stage 6 states that every twin ships one.
**Automated by:** `TestPublicStatusLine` (2 tests).

## T57 — One product per audience + dissemination register (Round 2 of the v2.7 program, automated)
**Input:** the "Decision product" form in `assets/templates.md` §11 and the "Dissemination register" block in the §1 Object Passport.
**Expected:** each decision product names its audience, its thresholds, its format, its channel, and its refresh cadence; the passport's dissemination register records who receives which product, by what channel. The templates are twelve fillable forms (§1 passport, §2 risk register, §3 TARP, §4 option card, §5 forecast registry entry, §6 scenario card, §7 focus application, §8 what-if scenario, §9 forecast bulletin, §10 public status line, §11 decision product, §12 mismatch register entry — added in Round 4 of the v2.7 program) — the `assets/templates.md` header and the SKILL.md Companion Documents line both say twelve.
**Automated by:** `TestDecisionProduct` (3 tests).

## T58 — Asset-relative safety margin (Round 2 of the v2.7 program, automated)
**Input:** `scripts/registry.py issue --clearance "asset:threshold,..."` on a quantity forecast (value 2.4 m), plus the clearance table in the §1 Object Passport and the clearance line in the §5 forecast registry entry.
**Expected:** the record carries per-asset clearance (threshold − forecast value): pier 2.5 → 0.1, pump 1.8 → −0.6; the chain still verifies (1 record); a record without `--clearance` has no clearance field and still verifies. `validate_forecast_fields` rejects a clearance entry whose clearance does not equal threshold − value, a non-numeric threshold, an unnamed asset, or a non-list clearance. Refused (exit 2): a pair without a colon, a non-numeric threshold, an unnamed asset. The docs state the formula and the generalization (clearance of a pollutant below its limit, of a level below a spillway crest, of a temperature below a lethal threshold).
**Automated by:** `TestAssetClearance` (5 tests).

## T59 — User-class operational thresholds (Round 2 of the v2.7 program, automated)
**Input:** `scripts/alert_bands.py --class-thresholds classes.csv` (CSV: class, limit) on a flood-depth series peaking at 0.40 m, plus the rule paragraph in `references/indicators.md` §20 and the onboarding line in `assets/templates.md` §1.
**Expected:** the output gains a `class_thresholds` block: per class, the limit and whether the latest observed value and the episode peak are within it — at peak 0.40 m, car (0.30) no, ambulance (0.35) no, pickup (0.45) yes; when the latest value drops below the limit after the peak (latest 0.25, peak 0.40, car 0.30), latest_within is yes, peak_within is no, can_operate is no. Refused (exit 2): missing file, missing class or limit column, non-numeric limit, duplicate class. The docs state the rule, the Phase 1 onboarding line ("for each decision-maker, their operational limit in the same units as the indicator"), and the distinction from the per-asset clearance (clearance is an asset's margin; this is who can do what).
**Automated by:** `TestUserClassThresholds` (4 tests).

## T60 — Exposure inventory + exposed fraction (Round 2 of the v2.7 program, automated)
**Input:** the "Exposure" block on the §6 scenario card in `assets/templates.md` and the scoring rule + subsection in `references/scenarios.md`.
**Expected:** the card lists the exposed elements (people, assets, habitats, intakes, cages) and the exposed fraction per class (exposed ÷ total in the zone), computed by table arithmetic from the hazard extent and the exposure inventory; the scoring rule includes the exposed fraction; the subsection "Exposure inventory and exposed fraction" sits after "Impact chains" and states the boundary (the chain's Exposure link names who/what is in the hazard's path; the fraction quantifies it per class; a fraction with no inventory behind it is not a number, it is a guess, and goes to the [НЕТ ДАННЫХ] register) and the source (EDITO — Coastal Risk Projections, hazard × exposure × vulnerability, Flooded Fraction). The fraction is table arithmetic: four of five cages is 0.8.
**Automated by:** `TestExposureInventory` (2 tests).

## T61 — Hindcast reproduction gate (Round 3 of the v2.7 program, automated)
**Input:** the "Reproduction check" field on the §6 scenario card in `assets/templates.md` and the "Hindcast reproduction gate" subsection in `references/scenarios.md`.
**Expected:** the card records the historical window reproduced with the intervention switched off, the declared tolerance, the reproduced state vs observations, and the pass/fail result; a failed check means the scenario delta is reported as "unvalidated, direction only" — never as a number. The subsection states the rule (run the scenario model on the historical window with the intervention off; the tolerance is the indicator's alert-band width or the calibration SD, declared before the run) and the boundary against the replay protocol (the gate validates a scenario model; the replay verifies an alert — a passed gate never claims the alert fired, a successful replay never validates a scenario delta); the same boundary is stated in `references/uncertainty-decision.md` §5. SKILL.md Stage 4 states the gate.
**Automated by:** `TestHindcastGate` (2 tests).

## T62 — Skill-vs-lead-time curve (Round 3 of the v2.7 program, automated)
**Input:** `scripts/skill_scores.py skill-horizon` on a CSV with one row per scored forecast pair (lead, obs, sim, naive — the naive column is the persistence/climatology baseline value for that pair, supplied by the caller from the same hold-out).
**Expected:** per lead bin, SS_RMSE = 1 − RMSE_model / RMSE_naive; the skill horizon is the longest lead with SS_RMSE > 0 and every shorter lead also above zero. Hand-verified: lead 1 SS_RMSE 0.5 (model rmse 1.0, naive 2.0), lead 2 SS_RMSE −2.0 (model 3.0, naive 1.0), lead 3 SS_RMSE 1.0 — the horizon is 1, and the lead-3 recovery is reported as a non-monotone recovery warning, not as horizon. No skill at the shortest lead gives a null horizon. A forecast is not trusted beyond its horizon. Refused (exit 2): missing columns, no usable rows. The "Skill horizon" field is on the §5 forecast registry entry form; `references/analytics-forecasting.md` §4 states the rule and the source (lake platforms — Meteolakes/COASTLINES report error as a function of forecast horizon).
**Automated by:** `TestSkillHorizon` (4 tests).

## T63 — Observation-nudged forecast (Round 3 of the v2.7 program, automated)
**Input:** `scripts/skill_scores.py nudge` on a CSV of recent QC-passed observation/model pairs (time, obs, sim) with `--forecast` (the raw forecast value) and `--n` (default 5, declared in the Object Passport).
**Expected:** nudged = raw forecast − mean(sim − obs) over the last N pairs. Hand-verified: residuals all +2 (sim runs 2 above obs) → raw 15 nudges to 13, correction −2.0. `--n 2` uses only the last 2 pairs; `--n` larger than the available pairs uses what exists and warns. The correction is recorded in the registry entry (`assets/templates.md` §5, "Nudge correction applied") and the N window in the passport (§1); the nudged forecast is scored per lead time by `skill-horizon` like any forecast. Refused (exit 2): fewer than 2 usable pairs, `--n` below 1. The rule is in `references/analytics-forecasting.md` §4 (the transferable principle of the Meteolakes ensemble Kalman filter, not the filter itself).
**Automated by:** `TestNudge` (4 tests).

## T64 — Phenomenon-oriented metrics (Round 3 of the v2.7 program, automated)
**Input:** the "Phenomenon-oriented metrics" subsection in `references/analytics-forecasting.md` §4 and the "Phenomenon metrics" line on the §5 forecast registry entry form in `assets/templates.md`.
**Expected:** the table gives 2–3 event metrics per phenomenon alongside the generic score — bloom (onset-date error, peak-magnitude error, duration error), flood (peak-level error, timing error, extent error), fire season (season-start error, peak-burned-area error, season-duration error), drought/low flow (onset-date error, minimum-level/flow error, duration error), heat/air stagnation (exceedance-days error, peak-concentration error). The admission rule stays SS_RMSE; the metrics show the client's skill on the events that matter. A metric that cannot be computed yet (too few events in the catalogue) is reported as [НЕТ ДАННЫХ] with the count, never as zero. No new script: the metrics are plain arithmetic on existing runner outputs.
**Automated by:** `TestPhenomenonMetrics` (1 test).

## T65 — Diversity indices (Round 3 of the v2.7 program, automated)
**Input:** `scripts/diversity.py indices` on a counts CSV (species, count) with `--taxonomy` (species, genus, family, order, class, phylum).
**Expected:** Shannon H′ = −Σ p ln p (natural log), Pielou J′ = H′ / ln(S), Clarke–Warwick taxonomic distinctness Δ+ = mean pairwise taxonomic distance (same genus 1, family 2, order 3, class 4, phylum 5, different phylum 6; a pair agrees at the deepest rank where both are known and equal). Hand-verified: counts 10, 5, 5 → H′ 1.0397, J′ = H′/ln 3; three species in one genus → Δ+ 1.0; two Aythya + one Anser → Δ+ 5/3; a record known only to class contributes at distance 4. On the Khubsugul counts (18 species, 20 records): H′ 2.8571, J′ 0.9885, Δ+ 3.5098; the unidentified record (Aves sp.) is named in the warnings. Species missing from the taxonomy are excluded from Δ+ and named. Refused (exit 2): a negative count, no species above zero. The biodiversity gallery runner now reports the indices (Shannon 2.8571, Δ+ 3.5098 in the summary) and the README states the counts are records per species (presence-only proxy, never abundance). The subsection is in `references/indicators.md` §11 with a cross-reference in §15.
**Automated by:** `TestDiversity` (5 tests).

## T66 — Plant functional type shares (Round 3 of the v2.7 program, automated)
**Input:** `scripts/diversity.py pft` on a cover/count CSV (species, cover) with `--pft-table` (species, pft, pathway, source), demonstrated on the field gallery entry (`examples/gallery/field/pft_cover.csv` + `pft_table.csv`).
**Expected:** shares from one quantity only (cover or counts, never mixed): the field entry gives grass 0.82, legume 0.10, forb 0.08, C3 1.00. Species missing from the PFT table are excluded from the shares and named (their cover stays in the total, so the shares do not sum to 1 — the unassigned share is stated, not hidden). The assignment table is published per site (TRY Plant Trait Database, Kattge et al. 2020, for the field entry); a trend needs repeat surveys, one survey reports shares only. The field runner reports the shares in its summary and the README states the cover values are synthetic (declared) and the assignments are the published TRY values. The subsection is in `references/indicators.md` §11.
**Automated by:** `TestPFTShares` (3 tests).

## T67 — Trait–environment matching (Round 3 of the v2.7 program, automated)
**Input:** `scripts/trait_match.py` on a trait table CSV (taxon + trait columns, values numeric or "x" for indifferent) with `--conditions` (JSON: {trait: {mode, value, window?}}), demonstrated on the field gallery entry's `trait_table.csv` (Ellenberg indicator values T, F, R, N, S; the Ellenberg column in Tichý et al. 2023, Zenodo 7427088 — Germany source Ellenberg & Leuschner 2010, the revised edition of Ellenberg et al. 1991; verified 2026-10-26).
**Expected:** a taxon fits only when EVERY stated condition is met. "at_least" (a tolerance: salinity, drought) requires the taxon's value to reach the site's value; "within" (an optimum: temperature, pH) requires it within the declared window around the site's value. A taxon marked indifferent ("x") for a trait is NOT excluded by a condition on that trait, and the output names it in `indifferent`. Hand-verified on the corrected field table (7 taxa): a saline site (S ≥ 8) fits only Salicornia europaea (Puccinellia distans S = 7); N ≥ 7 fits Trifolium pratense (indifferent N — it is not excluded), Lolium perenne, Taraxacum officinale, Elymus repens and Cirsium arvense, and excludes Salicornia europaea and Puccinellia distans (N = 4); T within 6 ± 1 fits all 7 taxa, two of them (Trifolium, Taraxacum) by indifference. Failing taxa are named with the failed condition and the values on both sides. Refused (exit 2): an unknown trait column, an unknown mode, a 'within' rule without a window, a trait cell that is neither a number nor "x". The table is the published Ellenberg values as transcribed in Tichý et al. 2023, verified 2026-10-26; Salicornia values are ssp. europaea. The subsection is in `references/indicators.md` §11 with a line in the §18 Agriculture quick set.
**Automated by:** `TestTraitMatch` (5 tests).

## T68 — Spread-informed sampling priority (Round 3 of the v2.7 program, automated)
**Input:** `scripts/uncertainty_budget.py sampling-priority` on a targets CSV (target + model/naive, or model_a/model_b).
**Expected:** disagreement = |a − b|; the ranking is descending by disagreement, ties broken by input order (deterministic, stated); the top target is named as `sample_next`. Hand-verified: A (10 vs 10 → 0), B (12 vs 20 → 8), C (15 vs 12 → 3) ranks B, C, A; sample_next is B. The old budget CLI (`uncertainty_budget.py ensemble.csv`) is unchanged — the dispatch is on the first argument only. Refused (exit 2): missing target column, neither value-column pair present, no usable targets. The rule is in `references/uncertainty-decision.md` §2 (value of information and adaptive sampling — the VoI home; §4 is the counterfactual twin, not the sampling rule) with a line on the §6 scenario card and a Stage 6 line in SKILL.md.
**Automated by:** `TestSamplingPriority` (4 tests).

## T69 — Sensitivity-first calibration (Round 4 of the v2.7 program, automated)
**Input:** `scripts/sensitivity_screen.py` on a model file (callable `run(params) -> float`) + a params JSON (each parameter has a `perturb` fraction or `range` endpoints) + an optional `--baseline`.
**Expected:** each parameter is perturbed one at a time (±perturb or the range endpoints), the output metric is recomputed, and the ranked table orders parameters by |metric change| descending, ties broken by input order (deterministic, stated). Hand-verified: run(p) = 2a + 0.1b + c, baseline 26.0 → ranking a (2.0) > c (0.5) > b (0.05). Refused (exit 2): no `run` callable, `run` returns a non-number, both `perturb` and `range` given, non-positive `perturb`. The honest limit is stated in the script docstring, SKILL.md Stage 3 and `assets/templates.md` §1: one-at-a-time misses interactions, unlike Sobol. Boundary vs the driver-perturbation table (T72) is stated in both docs: the screen perturbs MODEL parameters, the table perturbs INPUT drivers — different questions, different tables, never merged.
**Automated by:** `TestSensitivityScreen` (4 tests).

## T70 — Model ladder (Round 4 of the v2.7 program, automated)
**Input:** the "Model ladder" subsection in SKILL.md Stage 3 + the Model ladder field in the Object Passport template (`assets/templates.md` §1).
**Expected:** the fast model is admitted for SCREENING ONLY and must stay within a declared tolerance of the full model on the same hold-out, checked by `skill_scores.py`; a fast model outside its tolerance is not used for decisions. Governance + template, no computation.
**Automated by:** `TestModelLadder` (2 tests).

## T71 — Adaptation appraisal with equity + post-implementation follow-up (Round 4 of the v2.7 program, automated)
**Input:** the extended scenario scoring in `references/scenarios.md` (equity column + follow-up date) + the §4 Option card fields (impact avoided, co-benefits, equity, follow-up check date + registry forecast ID).
**Expected:** every adaptation option is scored on cost, impact avoided (from the Round 1 impact chain — the link is stated in the docs), co-benefits, and equity (who bears the cost, who gains); after implementation the twin re-scores the option against the predicted impact on a fixed date via `registry.py issue` with the predicted impact as the forecast value and the check date as the horizon end, scored on arrival — the same Brier-style discipline as BEIRA-F-001. Hand-verified via the registry: predicted impact 20, observed 24 → abs_error 4.0.
**Automated by:** `TestAdaptationFollowUp` (2 tests).

## T72 — Driver-perturbation table (Round 4 of the v2.7 program, automated)
**Input:** the "Driver-perturbation table" subsection in `references/scenarios.md` + the "Sensitivity" block on the §8 What-if Scenario form (`assets/templates.md` §8).
**Expected:** for each driver (rainfall, nutrient load, abstraction, land use) the table applies stated perturbations (+10%, +25%, −10%) and reports the indicator delta using the existing index functions — plain arithmetic, no new script. The boundary vs the sensitivity screen (T69) is stated in both docs: the screen perturbs MODEL parameters, the table perturbs INPUT drivers — different questions, different tables, never merged.
**Automated by:** `TestDriverPerturbationTable` (1 test).

## T73 — Mismatch register (Round 4 of the v2.7 program, automated)
**Input:** `scripts/mismatch.py --observed obs.csv --modeled mod.csv` (cell, value; 0/1) + optional `--register reg.jsonl --id M-001 --cause "..." --confirm-measurement "..." --model "..." --model-version "..."`.
**Expected:** extent = hits ÷ observed positives (null when there are no observed positives), misses (observed but not modeled), false alarms (modeled but not observed), hits; `--register` appends a JSONL entry (id, model, extent, misses, false_alarms, cause, confirm_measurement). Hand-verified: observed {A,B,C}, modeled {B,C,D} → extent 2/3, misses [A], false alarms [D]. Refused (exit 2): mismatched cell sets, non-binary values, empty tables, `--register` without the cause/confirm-measurement fields, duplicate id. The register is the learning log, not a gate (stated in `references/uncertainty-decision.md` §3 and `assets/templates.md` §12): the alert trial and the hindcast reproduction gate are pass/fail — a failed gate revokes admission — while the register explains *why* a validation was bad and turns the failure into the next data requirement. A failed validation with no register entry is a score with no lesson.
**Automated by:** `TestMismatchRegister` (4 tests).

## T74 — Promotion record (Round 4 of the v2.7 program, automated)
**Input:** `scripts/registry.py promote --registry reg.jsonl --id PROM-001 --model ... --model-version ... --promoted-by "name (role)" --evidence "benchmark + hold-out score"`.
**Expected:** the promotion is hash-chained like every record, status `operational`, with the signer, the registration clock, and the evidence; `registry.py score` ignores it (a promotion is governance, not a forecast); `verify` passes. Hand-verified: PROM-001 promoted by "R. Baldanova (lead modeler)" → operational; score reports 0 scored, chain ok. Refused (exit 2): duplicate id, missing `--promoted-by`, blank promoter, blank evidence. SKILL.md Stage 3 rule: a model is operational only after a recorded promotion; without one it is exploratory and its outputs are never presented as operational. The Object Passport template (§1) carries the promotion record fields.
**Automated by:** `TestPromotionRecord` (3 tests).

## T75 — Semantic mapping set (Round 4 of the v2.7 program, automated)
**Input:** `examples/gallery/*/mappings.csv` (one per gallery dataset directory: file, local_field, standard_term, standard, justification) + `scripts/build_manifest.py` `mappings` in the build index.
**Expected:** every header column of every gallery CSV is either mapped to a standard term (Darwin Core for biodiversity fields, Schema.org for generic measurement fields) or recorded as unmapped with a reason (no standard term exists, e.g. Ellenberg indicator values or plant functional types); every mapping carries a justification. The manifest builder emits one MappingSet File entity per mapping file (`about` the dataset it maps, `conformsTo` the SSSOM specification), listed in the Root Dataset's `hasPart`; validation refuses an unknown dataset id, a missing `path`, or a duplicate mapping id. Hand-verified: a pond mapping emits one MappingSet entity about `examples/gallery/pond/data.csv`, SSSOM-conformant, in `hasPart`. Cross-domain borrowings are stated in the justification (e.g. Darwin Core `eventDate` borrowed as the observation timestamp for a non-biodiversity series), never presented as native uses of the standard.
**Automated by:** `TestSemanticMappings` (4 tests).

## T76 — "Valid use / out of scope" field (Round 4 of the v2.7 program, automated)
**Input:** the Object Passport template (`assets/templates.md` §1).
**Expected:** the passport carries a "Valid use / out of scope" field: the decisions the twin is built for, and what the twin must NOT be used for. Template only, no code.
**Automated by:** `TestValidUseField` (1 test).

## T77 — Three-zone file ingestion (Laguna borrowing patch, automated)
**Input:** the zones convention in SKILL.md Stage 2 + the file-zone field on the Phase 1 onboarding checklist (`assets/templates.md` §1) + the zones note in the `scripts/qc_series.py` docstring.
**Expected:** incoming files move through three zones, never edited in place: `landing/` (as received, untouched), `trusted/` (QC-passed, the gate pass recorded), `refined/` (domain-converted and model-ready, the conversion recorded in the build manifest). A file leaves `landing/` only after its QC is recorded; a file enters `refined/` only after its conversion is recorded. The QC script flags rows — it never moves or edits files. Documentation only, no new script.
**Automated by:** `TestThreeZoneIngestion` (2 tests).

## T78 — Twin-to-twin notifications (Laguna borrowing patch, automated)
**Input:** the notification step in SKILL.md Stage 7 + the "Linked nodes notified" field on the trigger–action–response plan (`assets/templates.md` §3).
**Expected:** when an alert fires, the twin notifies its linked nodes (upstream and downstream twins); the notification is recorded on the TARP, not in the forecast registry; a notified node re-checks its own alert bands on the next batch. No new registry entry type — a notification is a communication act on the TARP, not a forecast record; adding it to the hash-chained registry would mix non-scorable communication into the forecast record for no audit gain. Documentation + template only, no code.
**Automated by:** `TestTwinToTwinNotification` (2 tests).

## T79 — Per-twin workspace layout (Laguna borrowing patch, automated)
**Input:** the workspace layout in SKILL.md Stage 2 + the cross-reference from the build-manifest sentence in Stage 7.
**Expected:** a twin's working folder follows one layout: `common/` (passport, shared data), `etl/` (ingestion + QC), `calibration/` (models + admission), `forecasts/` (bulletins + registry), `simulations/` (scenarios); the build manifest records which file sits where. Laguna's layout carries an `ml-training` folder — this skill has no ML-training step, so the layout adapts it away (the absence is pinned by test, not assumed). Documentation only, no code.
**Automated by:** `TestTwinWorkspaceLayout` (2 tests).

## T80 — Four named open-data ETL streams, field twin (Laguna borrowing patch, automated)
**Input:** the "Field-twin open-data streams" subsection in `references/data-sources.md` §10 + the one-line cross-reference in the field gallery README (`examples/gallery/field/README.md`).
**Expected:** the field twin is fed by four named open-data streams — daily weather (ERA5 by default, station truth where one exists), forecast weather (national meteo service / CAMS; never a substitute for observations in calibration), historical weather (ERA5 back to 1940 or the national archive; the hindcast window), NDVI (Sentinel-2, Landsat where Sentinel is missing, MODIS/VIIRS daily as the coarse context layer only). A stream that is unavailable is recorded as a gap in the [НЕТ ДАННЫХ] register, not silently replaced by another stream. The list lives in one place only (`references/data-sources.md` §10); the gallery README points at it and does not repeat it. Documentation only, no code.
**Automated by:** `TestFieldTwinEtlStreams` (2 tests).

## T81 — New domain sections §21–§29 (v2.8, automated)
**Input:** the package text itself: `references/indicators.md` (§21–§29, §18) and SKILL.md.
**Expected:** the catalogue carries eleven new sections — §21 Cryosphere and mountain hazards (14 table rows), §22 Steppe and natural grassland (17), §23 Livestock farm (18), §24 Peatlands and bogs (15), §25 Marine and coastal (24), §26 Urban ecosystems (22), §27 Aquaculture (19), §28 Desert and arid lands (19), §29 Tundra and polar (17), §30 Forest (20), §31 Cropland (21) — 206 new table rows in total; §18 carries the eleven matching quick sets; SKILL.md names the eleven sections and the descriptive name "Ecosystem Digital Twin by Rigjita Baldanova"; the [unverified] flags from the drafts are preserved in the catalogue; each new section's table is one contiguous block (no hard-wrapped row splits it). First-layer additions (2026-10-27): `references/worked-examples-new-sections.md` and `references/sources-new-sections.md` carry the eleven worked examples and the eleven full source lists, verbatim from the drafts, each with a `## Contents` list; the §29 Liu et al. 2026 figures are verified against the full text (DOI 10.34133/remotesensing.1062) — 21,402 km², no "provisional" left in the catalogue. Second-layer check (2026-10-28): the EU 2024/1244 500 t threshold and the water-use benchmark are closed against primary sources; the Daursky, North Wyke and Toolik worked examples now carry published values, with the remaining gaps named (Daursky-reserve-only gazelle total, current marmot density, burned area, SOC; North Wyke P balance, whole-platform CH₄ total, measured whole-farmlet NH₃ flux; Toolik lemming densities); the marmot and WHO flags remain, with documented negative checks.
**Automated by:** `TestNewSections` (5 tests).

## T82 — Automated satellite fetch (v2.8, automated)
**Input:** a recorded STAC response (3 Sentinel-2 scenes: cloud 12.5%, 45%, no value; B04/B08 data assets plus an overview asset) and the script CLI.
**Expected:** `parse_scenes` returns the 3 scenes with ids, datetimes, cloud covers and only the data bands (B04, B08 — the overview asset is not a band); the NDVI formula gives (300−100)/(300+100) = 0.5, (200−200)/(200+200) = 0.0, and no value when both bands are zero; `--check` writes `manifest.json` and `virtual-sensor.json` (sensor `satellite-sentinel-2-ndvi`, quantity NDVI, formula `(NIR - red) / (NIR + red)`, collection `sentinel-2-l2a`, validity window names the periodic cadence) and downloads nothing; the default `--max-cloud 20` keeps the 12.5% scene and the scene with no cloud value and drops the 45% scene; a malformed bbox is rejected (exit 2); an unreachable catalogue exits 3 with "unreachable"; Copernicus + Landsat is rejected (exit 2, "not served"); `--help` exits 0. No network is used by any test.
**Automated by:** `TestFetchSatellite` (8 tests).

## T83 — Registered virtual sensors, Variant B (v2.8, automated)
**Input:** the package text itself: `references/worked-examples-new-sections.md`, `references/sources-new-sections.md`, `references/data-sources.md`.
**Expected:** six virtual sensors are registered in the Object Passport form as a worked example — Beira Lake: Sentinel-2 chlorophyll-a (NDCI, Mishra & Mishra 2012; RMSE 1.43 µg/L below 30 µg/L; Molkov et al. 2019: 3.02 µg/L), Landsat 8/9 water surface temperature (Gerace et al. 2020 split-window; Eon et al. 2023: 0.87 K L8 / 0.74 K L9), water extent (MNDWI, Xu 2006; Pekel et al. 2016: under 1% false water, under 5% missed), turbidity (Dogliotti et al. 2015; RMSE 20.5 FNU, n = 106), Secchi depth (Lee et al. 2015 QAA; Beira-local RMSE 0.049 m, R² = 0.670, n = 43, Prasad et al. 2024); Langtang slope: Sentinel-1 InSAR displacement (40 cm / 48 days, ICIMOD 2026; ±10 mm against levelling/GNSS). Every registration carries a published formula, a named calibration station, and a skill score or an explicit [NEXT DATA] gap (five sensor-level gaps); the Secchi-depth sensor is the one Beira-local published skill score. `references/data-sources.md` carries a Sentinel-1 row in the satellite table and an Open-Meteo row in the atmosphere table (free, no API key). Documentation only, no code.
**Automated by:** `TestRegisteredVirtualSensors` (3 tests).

## T84 — Forest module §30 (v2.8, automated)
**Input:** the package text itself: `references/indicators.md`, `SKILL.md`, `SKILL.ru.md`, `references/worked-examples-new-sections.md`, `references/sources-new-sections.md`.
**Expected:** the catalogue carries a tenth new section — §30 Forest (21 table rows: 16 new indicators, 5 cross-references to §9/§10/§11/§15), one contiguous table block; §18 carries a matching Forest quick set; SKILL.md and SKILL.ru.md name §30 and the updated counts (32-section catalogue; 226 new table rows: 163 new indicators plus 63 cross-references); the Harvard Forest worked example carries published values (net uptake 2.0 ± 0.4 Mg C/ha/yr 1993–2000, pretreatment basal area 29.6–53.0 m²/ha, hemlock stands net source after 2014) with the remaining gaps named ([NEXT DATA]: current canopy, deadwood, biomass stock, regeneration density, fragmentation); the §30 source list carries the FRA 2025 figures (4.14 B ha, 714 Gt) and the Pan et al. 2011, Barford et al. 2001, Curtis et al. 2018 and Finzi et al. 2020 DOIs; no §30 indicator row carries an [unverified] flag; one [NEXT DATA] row is allowed — the mast yield index, added 2026-10-28 with the Barguzinsky bear example. Loop score 9/10 (draft, 2026-10-28).
**Automated by:** `TestForestSection` (5 tests).

## T87 — Barguzinsky bear worked example, second example for §30 (v2.8, automated)
**Input:** the package text itself: `references/indicators.md`, `SKILL.md`, `SKILL.ru.md`, `references/worked-examples-new-sections.md`, `references/sources-new-sections.md`.
**Expected:** the second worked example for §30 — Barguzinsky Reserve and the Buryatia taiga edge: human–brown bear conflict, autumn 2026 — carries verified figures only (Buryatia brown bears 6,113 in 2026, 6,276 in 2025, 5,385 in 2021, 4,625 in 2011; density 0.21 per 1,000 ha; 47 exits in all of 2025; regulated 149 by 14 September, 331 by 3 October, 436 by 20 October; 6 attacks, 2 dead; harvest limit 1,272, about 900 permits, about 300 harvested a year; reserve 374,322 ha, sable 20–30 at creation → 1,500–2,000 today), each with its authoritative source in the §30 source list (Burprirodnadzor via Burunen and MK Ulan-Ude; Vedomosti; Seldon; SakhaNews; UlanMedia; Yuga.ru; reserve profile via Wikipedia / Big Russian Encyclopedia / FGBU "Zapovednoe Podlemorye"), plus the reliability caveat (departmental figures as relayed by the press; primary summaries not published openly) and the named [NEXT DATA] gaps (bear numbers in the reserve itself; quantitative mast index for Buryatia 2026; wolf numbers; attractants register; numeric young-share; long-term attacks series); cross-reference rows in §15 (brown bear abundance, age structure), §17 (conflict reports, attractants register, quota uptake) and §20 (taiga-edge watch levels), and one new §30 row (mast yield index, Research, [NEXT DATA]). Added on her decision of 27 October 2026, 22:10 EDT — an explicit exception to the "no Russian worked examples" rule, only with links to authoritative sources for every figure.
**Automated by:** `TestBarguzinskyBearExample` (4 tests).

## T86 — Non-peat wetlands and marshes module §32 (v2.8, automated)
**Input:** the package text itself: `references/indicators.md`, `SKILL.md`, `SKILL.ru.md`, `references/worked-examples-new-sections.md`, `references/sources-new-sections.md`.
**Expected:** the catalogue carries a twelfth new section — §32 Non-peat wetlands and marshes (19 table rows: 14 new indicators, 5 cross-references to §4/§9/§10/§11/§15), one contiguous table block; §18 carries a matching Non-peat wetlands and marshes quick set; SKILL.md and SKILL.ru.md name §32 and the updated counts (32-section catalogue; 225 new table rows: 162 new indicators plus 63 cross-references); the Everglades worked example carries published values (historic ~4,000 sq mi, just over half remains; hydroperiod classes 11+ / 9–10 / 3–7 months; TP criterion 10 µg/L; wading-bird nests 138,834 in 2018, ~3,500 in the 2025 drought season) with the remaining gaps named ([NEXT DATA]: Everglades accretion, fish-nursery densities, intrusion, nutrient balance, sawgrass/cattail shares; Mongol Daguur hydroperiod, accretion, retention, reed area, fish densities, current bird count); the Mongol Daguur regional case carries the Ramsar staging counts (2,000 geese, 4,000 shelducks, 20,000 ducks, 7,000 coots, over 10,000 gulls); no Russian worked example, pilot or showcase case anywhere in the module, by her correction of 2026-10-27; the §32 source list carries the Ramsar GWO 2018 figures (12.1 M km², 35% lost 1970–2015) and the Davidson 2014, Saltonstall 2002 and Beck et al. 2001 DOIs; no §32 indicator row carries an [unverified] flag or a [NEXT DATA] gap. Loop score 9/10 (draft, 2026-10-28).
**Automated by:** `TestWetlandsSection` (5 tests).

## T85 — Cropland module §31 (v2.8, automated)
**Input:** the package text itself: `references/indicators.md`, `SKILL.md`, `SKILL.ru.md`, `references/worked-examples-new-sections.md`, `references/sources-new-sections.md`.
**Expected:** the catalogue carries an eleventh new section — §31 Cropland (21 table rows: 15 new indicators, 6 cross-references to §5/§9/§10/§11/§14/§15), one contiguous table block; §18 carries a matching Cropland quick set; SKILL.md and SKILL.ru.md name §31 and the updated counts (31-section catalogue; 206 new table rows: 148 new indicators plus 58 cross-references); the GEPIS rice-paddy worked example carries published values (project target yield 5.5–6.2 t/ha; Beira Lake WPI 2.4–2.5 against 1.0; national Maha ~2,853 kg/ha, Yala ~3,207 kg/ha; paddy ET Maha 470 mm, Yala 677 mm) with the remaining gaps named ([NEXT DATA]: measured GEPIS yield, water use, CH₄/N₂O fluxes, SOC, ECe, margins, erosion); the §31 source list carries the SOLAW 2025, FAO salt-affected-soils 2024 (1,381 Mha), FAOSTAT fertiliser (185 Mt, 2022) and pesticide (3.54 Mt, 2021) figures and the Borrelli et al. 2017, Bowles et al. 2020, Albrecht et al. 2020, Mikhailova & Post 2006 and Prasad et al. 2024 DOIs; no §31 indicator row carries an [unverified] flag or a [NEXT DATA] gap. Russian material only as published-data anchors (Kursk chernozem SOC; erosion) — no Russian worked example, pilot or showcase case, per her correction of 2026-10-27. Loop score 9/10 (draft, 2026-10-27).
**Automated by:** `TestCroplandSection` (5 tests).

## T88 — Full sensor registry (v2.8, automated)
**Input:** the package text itself: `references/sensor-registry.md`, `references/data-sources.md`, `references/indicators.md`, `SKILL.md`.
**Expected:** `references/sensor-registry.md` maps every open source to the ecosystems and indicator rows it serves: 59 rows (R01–R59), tiers exactly Core 1, Conditional 35, Research 3, Context-only 20; all 48 canonical source names from `references/data-sources.md` appear (29 original data sources, 7 standards, evidence platforms, 3 client/sensor items, 8 new sources); all 29 indicator-bearing sections (§§1–17 and §§21–32) are served and no row cites the meta sections §§18–20; the seven registered virtual sensors are carried verbatim (six named: five Beira, one Langtang — S1–S6 — plus the Object Passport "Virtual sensors" block as the reusable seventh form, with an explicit note that no seventh sensor with a formula exists); the only Core row is R05 (Secchi depth at Beira, RMSE 0.049 m, Prasad et al. 2024); every numeric score claim in the table carries a citation and every missing score is [NEXT DATA]; `references/data-sources.md` §12 adds the 8 new sources (NASA FIRMS, Global Forest Watch / Hansen, ESA WorldCover, OpenStreetMap, GPM IMERG, SMAP, Copernicus Marine Service / OSTIA, WDPA / Protected Planet with the Russia-data restriction caveat) and a pointer to the registry; SKILL.md carries a one-line pointer. Loop score 9/10 (2026-10-28).
**Automated by:** `TestSensorRegistry` (7 tests).

## T89 — Both [unverified] flags closed (v2.8, automated)
**Input:** the package text itself: `references/indicators.md`, `references/sources-new-sections.md`.
**Expected:** no live `[unverified]` flag marker remains in any indicator table row of `references/indicators.md`; the §22 marmot row uses the object's own baseline with trend over ≥3 survey rounds and carries the verified anchors (tarbagan Endangered IUCN A2ad, bobak Least Concern; Enkhsaikhan et al. 2021 founder minimums ≥10 families / ≥50 individuals, DOI 10.5564/pib.v37i1.3137; Xu et al. 2023 plague cut-point 0.63 marmots/ha, DOI 10.1038/s41598-023-38966-1); the §26 green-space row attributes 9 m² to Italian law D.M. 1444/1968 (18 m² public space, 9 m² greenery per inhabitant) with the Czesak 2025 negative check and the Mostafa & Alshahrani 2025 corrigendum (DOI 10.3389/frsc.2025.1542464), and WHO's verified guidance is accessibility (0.5–1 ha within 300 m); `references/sources-new-sections.md` carries no "REMAINS [unverified]" and both §22/§26 notes read RESOLVED. No standard or WHO publication invented: both closures are verified negative results. Loop score 9/10 (2026-10-28).
**Automated by:** `TestUnverifiedFlagsClosed` (3 tests) + `TestNewSections.test_both_unverified_flags_closed`.

## T92 — Quick fixes from the external 7.5/10 audit (v2.8, candidate only)

**Expected:** frontmatter `description` in SKILL.md and SKILL.ru.md names the v2.8 domains (forests, peatlands, marine and coastal waters, urban ecosystems, deserts, tundra and cryosphere, cropland, livestock farms) and stays within 1024 characters; the Deterministic Script I/O Schemas table lives in `references/scripts.md` with all 17 script rows including `scripts/fetch_satellite.py`, and SKILL.md carries only a short pointer (under 500 lines); SKILL.ru.md starts with `---` on line 1 and its HTML comment sits below the frontmatter.

## T102 — TestReleaseV28 (2026-10-28, 4 tests)

Release edits for v2.8 by Claude Anthropic on the author's go-ahead to
publish. Pins: one release date (2026-10-28) in README (EN/RU),
CITATION.cff and CHANGELOG; one DOI across README (EN/RU) and
CITATION.cff, moved off the v2.3 record to the latest minted record (v2.7)
until the v2.8 DOI is minted; no candidate or BY-ND wording left in
`references/thresholds.md`; the README scope line (no process-model core
with data assimilation until v2.9) in both languages; brand candidates not
listed in either README.
Run: 343 tests, all pass; strict lint PASS (2026-10-28, T102).

## T101 — TestT100FollowUpOct28 (2026-10-28, 3 tests)

Muse's verification of the T100 build against primary sources. Pins the
corrections to the T100 record: DCS yields restored as verified (Muse
T99, primary DCS Paddy Statistics table — 2022/23 Maha 3,731, 2023 Yala
4,128 kg/ha); the Laksvel 'very high' descriptor is the protocol's own
wording (§4.3, "This must be described as very high") and the T100
rationale is corrected; the T100 test class holds six tests (the
CHANGELOG said five). The stale T99 test-class docstring is updated to
the T100-corrected state.
Run: 339 tests, all pass; strict lint PASS (2026-10-28, T101).

## T100 — TestT99FollowUpOct28 (2026-10-28, 6 tests)

Claude's review of the T99 build (9.3/10), fixes applied by Claude at the
author's request. Pins: the Norwegian density rule as § 25 «Tetthet» of
FOR-2008-06-17-822 in the catalogue and the source list (T99's §19 is not
the paragraph in the regulation's full text on FAOLEX); the four Laksvel
colour levels from §4.3 without the unsourced 'very high'; the USDA area
and yield status (trade press — the ERS Outlook confirms production only);
the GEPIS target as about one and a half times the DCS national average;
the CHANGELOG correction of the T99 Tier 1 record (IPCC Table 2.1 has no
cool/warm temperate split); README.md and README.ru.md giving the same
test count (README.ru.md still said 227). Three T99 tests repointed
(Norway, USDA, Danube 2017 census).
Run: 336 tests, all pass; strict lint PASS (2026-10-28, T100).

## T99 — TestIndependentVerificationOct28 (2026-10-28, 7 tests)

Independent verification of the T97/T98 build by Muse against primary sources. Pins: the Tier 1 factors in the correct assignment (cropland 7.9 boreal/temperate and 14.0 tropical, grassland 5.7 boreal — the T96 swap is not to return; verified against ESSD Table 5); the Laksvel mortality band cited from the primary protocol (Rapport fra Havforskningen 2025-40, §4.3; above 2% is level 3 red, "very high"); the Norwegian density paragraph confirmed as §19 (FAOLEX); the USDA 2025/26 record cited to the ERS Rice Outlook RCS-26H and the FAS World Agricultural Production circular, September 2026; the Danube 5,500-species total cited to Claudino-Sales 2018; Todgerel 2020 still flagged as a secondary citation (primary document not consulted); the CHANGELOG record of the T99 verification and the Tier 1 correction.
Run: 330 tests, all pass; strict lint PASS (2026-10-28, T99).

## T98 — TestAccuracySweepOct28 (2026-10-28, 7 tests)

Further accuracy sweep of §21–§32 by Claude (two iterations, at the
author's request). Pins: Everglades slope and remaining extent carried as
"about 2 inches per mile or less" and "about half" with both sources
named; the Norwegian density rule cited by title, not by an unconfirmed
paragraph; the copper row's ASC Indicator 4.7.4 and 34 mg/kg; the three
§23 grazing rows as cross-references to §22 (the Wyoming B-1320 anchor
appears once in the catalogue); Morris et al. 2016 cited from its
abstract; Har Us Nuur endemic fish as "three to five"; no draft wording
left in the source list. One T89 assertion re-worded with the source list
("this section" for "this draft").
Run: 323 tests, all pass; strict lint PASS (2026-10-28, T98).

## T97 — TestT96FollowUpOct28 (2026-10-28, 7 tests)

Claude Anthropic's re-review of the T96 build (8.5/10), fixes applied by
Claude at the author's request (so the next cross-check should be done by
another model). The T96 archive as shipped did not pass its own lint: the
v2.9 note in CHANGELOG.md named the planned gate_check.py script as a
backticked path that does not exist, so `test_package_lint_passes` failed
(308 of 309) — the "309 pass" line under T96 below predates that edit.
Fixed: the CHANGELOG path (now plain text, "planned, not yet written");
§24 Tier 1 factors, which T96 had re-swapped, set to IPCC 2013 Wetlands
Supplement Table 2.1 (cropland 7.9 boreal and temperate, 14.0 tropical;
grassland 5.7 boreal, temperate 5.3 / 6.1 / 3.6 by nutrient status and
drainage depth, 9.6 tropical; t CO₂-C/ha/yr); `references/sources-new-sections.md`
synced with the catalogue (Tier 1 and the IPCC organic-soil definition,
Peatland Code v2.1, the 47 PDGL split 21/25/1, Gutman & Ignatov 1998 and
the Carlson & Ripley quadratic form, Western Arctic peak 2003, Chen et al.
2021, Rising et al. 2026, FRA 2025 fire on all land, WRI forest loss 2024
and 2025, FAO 2024 salt with the 2021 depth split labelled, DCS rice
yields, Fluet-Chouinard et al. 2023); the GEPIS worked example now carries
the DCS yields; the broken §25 DHW sentence rejoined; the §28 depth split
labelled as FAO 2021; the cryosphere quick set gains glacier mass balance
and points active-layer thickness to §29; SKILL.ru.md Stage 1 now states
the anchor hierarchy and the stricter-binding rule, as SKILL.md does. The
T85 assertion that pinned the old 2,853 kg/ha study average now pins the
DCS 3,731 kg/ha. Tests pin each fix; all seven fail on the T96 build and
pass here. SKILL.md unchanged (499 lines by wc, 500 by the linter).
Run: 316 tests, all pass; strict lint PASS (2026-10-28, T97).

## T96 — TestTablesClosedOct28 (2026-10-28, 4 tests)

Claude Anthropic's full-candidate review (8/10), verified against primary
sources before applying. All 10 accuracy errors in §21–§32 corrected (47
glacial lakes by basin; IPCC peat definition; Tier 1 Table 2.1 factors and
CO₂-C units; Peatland Code v2.1; FVC linear = Gutman & Ignatov, quadratic =
Carlson & Ripley; Mekonnen et al. 2021 DOI; caribou peak ~490,000 in 2003;
fire 261 M ha = all land; DCS rice yields 2022/23 Maha 3,731 / 2023 Yala
4,128 kg/ha; salt 1,381 Mha FAO 2024); forest loss updated to 2024 (6.7 M
ha, record) and 2025 (4.3 M ha); wetland loss as a range of estimates
(Davidson 64–71% vs Fluet-Chouinard ~21%); unverified figures sourced
(USDA September 2026 estimate, iScience 2026 seagrass, Chen et al. 2021
thermokarst, Todgerel 2020 corroboration, Sci. Rep. 2024 peat rewetting)
or removed (Krasnoyarsk berries, Selenga manganese); §30–§32 brought to
the §21–§29 format; §31 table closed; §18 quick sets completed; §19 and
README counts fixed; working notes moved to CHANGELOG; bear strip moved
from §20 to §30 with the alert role on the conflict-report series; gate
qualified — the stricter binding standard governs red, guidance and drafts
stay yellow; glacier mass-balance and copper/antifouling rows added; §22
Daurian example signed as the second explicit exception (her decision of
28 October 2026). Tests pin: every table run followed by a blank line; §31
closure regression; 12 watch-levels and 12 does-NOT-do subheads; stricter
binding standard wording in SKILL.md and §20. SKILL.md stays 499 lines;
SKILL.ru.md stays 561 lines.
Run: 309 tests, all pass (2026-10-28, T96).

## T95 — TestGateThresholdRuleOct28 (2026-10-28, 8 tests)

Claude Anthropic's 8/10 review (SKILL.md only), verified point by point
before applying, with Claude's own two amendments: (1) the gate rule —
binding standard = red + block, guidance/draft = yellow, no standard ->
threshold by the Stage 1 hierarchy fixed in the passport before data
arrives and red for this build, no measurement still blocks; (2) the
brand line removed from SKILL.md entirely (candidates ADIS, AdisECO,
AdisTwin, NaranTwin now live in CHANGELOG only). PFAS numbers moved to
references/thresholds.md §1.8 (21 indicators, 7 jurisdictions, 25
[provisional] marks); description names steppe/grassland and aquaculture
in both languages; the two gap markers are defined; Stage 2 states the
script returns scenes + NDVI, not SDD; date 2026-10-28. Tests pin: PFAS
numbers in §1.8 and out of the gate; both gate-rule cases; no "ADIS" in
either SKILL file; steppe/aquaculture in both descriptions; 7
jurisdictions; markers defined; date updated; satellite scope. T90 counts
updated (21/7/25); T93/T94 repointed to §1.8. Two suite-found defects
fixed in passing: Stage 1 "(see Template 2)" broke the gate split;
the lengthened compatibility line exceeded the 500-character lint cap.
Run: 305 tests, all pass (2026-10-28, T95).
`ecosystem-digital-twin/`; SKILL.md 499 lines (one under the 500 limit).

## T94 — TestSafetyGatePfasMatrices (2026-10-28, 4 tests)

Claude Anthropic's point (e), verified against the primary sources before
applying: (1) Federal Register 2026-10085 — rescission proposal 20 May
2026, comments to 20 Jul 2026, not final as of Aug 2026 (the "May 2025"
wording was wrong: May 2025 was only EPA's announcement of intent);
(2) EPA draft sewage-sludge risk assessment, 14 Jan 2025 — 1 ppb risk
for highly exposed groups, draft, not a standard (secondary summaries
consistent); (3) German DüMV — sum PFOA+PFOS 100 µg/kg, labelling above
50 µg/kg (2008 value); (4) Danish EPA 2023 report — indicative PFAS4
15 µg/kg, "very likely to protect groundwater and freshwater".
Tests pin: rescission date May 2026, not 2025; the four values marked
[provisional]; sediment anchors present and water limits excluded from
solids; microplastics row unchanged. The T93 test asserting "май 2025"
was updated to the corrected date. Run: 297 tests, all pass (2026-10-28, T94).
passes from a copy installed as `ecosystem-digital-twin/`.

## T93 — PFAS and microplastics in the safety gate (v2.8, candidate only)

**Expected:** Non-Negotiable 5 and Template 2 (SafetyGateCard) in SKILL.md and SKILL.ru.md name PFAS and microplastics; the PFAS row carries the jurisdictional anchors (US EPA NPDWR Apr 2024 PFOA/PFOS 4.0 ng/L, EU Directive 2020/2184 sum of 20 PFAS 0.1 µg/L, total PFAS 0.5 µg/L) with the May 2025 EPA reconsideration disclosed; the microplastics row states that no numeric limit is invented and gates on the harmonized method and the reported load, with [НЕТ ДАННЫХ] blocking.

## T91 — Remaining priority [NEXT DATA] gaps verified (v2.8, automated)
**Input:** the package text itself: `references/worked-examples-new-sections.md`, `references/sensor-registry.md`, `references/indicators.md`, `references/sources-new-sections.md`.
**Expected:** the three priority gaps are verified negative results, not values: Beira-local SS_RMSE for Sensors 1–4 is [NEXT DATA] with a per-sensor reason (chlorophyll-a and temperature exist only as interpolated supplement maps, Figs. S7–S8 and S1–S2, with no per-station numeric table, and the paper never applied NDCI or Landsat surface temperature at Beira; the water extent is a single surveyed total, about 65.4 ha, not a mask; turbidity was never measured in situ at Beira); no Beira-local SS_RMSE value is invented anywhere; the supplement citation is corrected to Figs. S7–S8 (the main text's Figure S9 does not appear in the supplement list); Langtang ground truth is [NEXT DATA] with cross-sensor corroboration (Roy et al. 2026, DOI 10.1007/s12524-026-02611-x) distinguished from ground truth, and the pre-collapse deformation can never be scored retrospectively; the Daursky marmot density (ind/ha) is still unpublished and still [NEXT DATA], with published context labelled as not a Daursky value (species range 1–7 ind/ha, IUCN species account, Zenodo 6819035; Hustai National Park comparator ca. 1.27 ind/ha, Todgerel 2020, secondary citation) and the named next source (the reserve's «Летопись природы» / DIPA joint-expedition counts). No "[provisional]" appears in `references/indicators.md` (T81 rule). Loop score 9/10 (2026-10-28).
**Automated by:** `TestRemainingNextDataGapsVerified` (6 tests).

## T90 — Thresholds source guide applied (v2.8, automated)
**Input:** the package text itself: `references/thresholds.md`, `references/indicators.md`, `SKILL.md`.
**Expected:** `references/thresholds.md` carries the draft guide verbatim (body identical to the draft except the status header and closing line): 20 indicators, 5 jurisdictions (WHO, EU, USA, Russia, Japan), anchor hierarchy, thresholds by use, operational early-warning level (yellow at 70–80% of the regulatory limit), decision support (§9, ЛПР), 14 open items as [NEXT DATA]; all 21 [provisional] marks preserved and visible; no [unverified] flag anywhere in the file; Russian lead in drinking water NOT entered as a value (the §1.7 row reads "Не проверено", §10 item 2 records the 0.03 vs 0.01 mg/L contradiction); key anchors present (nitrate 50 mg/L WHO/EU, PM2.5 WHO 5 µg/m³, DHW Alert Level 1 at 4 ≤ DHW < 8, Everglades TP 10 µg/L, Carlson TSI classes). SKILL.md carries the rules (Stage 1 anchor hierarchy, Stage 6 decision support with ЛПР, Companion pointer) and stays under 500 lines; `references/indicators.md` §19 points to the guide and §20 carries the three new rules (anchor hierarchy, thresholds by use, operational early-warning level); no per-country value is hard-coded into SKILL.md. Loop score 9/10 (2026-10-28).
**Automated by:** `TestThresholdsGuideApplied` (8 tests).

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
| T32 | Phase 4 standing verification; forecast registry (cadence, lead time) | yes |
| T33 | Phase 1 data inventory; onboarding checklist | yes |
| T34 | Phase 6 provenance package; FAIR Signposting | yes |
| T35 | Phase 5 scenarios; Phase 0 passport handover | yes |
| T36 | Stage 7 monitoring; recalibration trigger (drift) | yes |
| T37 | Stage 3 admission; continuous revalidation | yes |
| T38 | Stage 6 human decision; two tiers | yes |
| T39 | Stage 6 explainability; Stage 2 fusion checklist | yes |
| T40 | Companion Documents gallery; one working twin per task type | yes |
| T41 | Companion Documents gallery; wetland prototype | yes |
| T42 | Companion Documents gallery; forest-fire prototype | yes |
| T43 | Companion Documents gallery; forest-logging prototype | yes |
| T44 | Companion Documents gallery; forest-carbon prototype | yes |
| T45 | Phase 5 scenarios: impact chain on the scenario card | yes |
| T46 | Phase 5 scenarios: Storyline class in the taxonomy | yes |
| T47 | Phase 4 standing verification; replay protocol in uncertainty-decision §5 | yes |
| T48 | Phase 5 scenarios: seeded scenario generation | yes |
| T49 | Core Mathematical Specifications: HQ/HI beside WPI/TSI/HPI | yes |
| T50 | Phase 4 bands, alerts; covariate-aware alert rule (indicators §20) | yes |
| T51 | Stage 3 admission; alert trial as a separate gate | yes |
| T52 | Stage 3 admission; calibration plausibility gate (calibration-bounds) | yes |
| T53 | Phase 1 data onboarding; virtual sensors in the Object Passport | yes |
| T54 | Phase 3 transport; deterministic drift / connectivity module | yes |
| T55 | Phase 4 standing verification; daily forecast bulletin | yes |
| T56 | Stage 6 human decision; public status line per twin | yes |
| T57 | Stage 6 human decision; one product per audience + dissemination register | yes |
| T58 | Phase 4 standing verification; asset-relative safety margin in the registry | yes |
| T59 | Phase 4 bands, alerts; user-class operational thresholds (indicators §20) | yes |
| T60 | Phase 5 scenarios; exposure inventory + exposed fraction on the scenario card | yes |
| T61 | Phase 5 scenarios; hindcast reproduction gate on the scenario card | yes |
| T62 | Phase 3 forecast skill; skill-vs-lead-time curve + skill horizon | yes |
| T63 | Phase 3 forecast skill; observation-nudged forecast | yes |
| T64 | Phase 4 standing verification; phenomenon-oriented metrics in the verification record | yes |
| T65 | Phase 2 indicator catalogue; diversity indices (Shannon, Pielou, taxonomic distinctness) | yes |
| T66 | Phase 2 indicator catalogue; plant functional type shares | yes |
| T67 | Phase 2 indicator catalogue; trait–environment matching | yes |
| T68 | Phase 4 value of information; spread-informed sampling priority | yes |
| T69 | Phase 3 calibration; sensitivity-first calibration (sensitivity screen) | yes |
| T70 | Phase 3 calibration; model ladder (fast model screening only) | yes |
| T71 | Phase 5 scenarios; adaptation appraisal (equity + post-implementation follow-up) | yes |
| T72 | Phase 5 scenarios; driver-perturbation table | yes |
| T73 | Phase 4 standing verification; mismatch register (learning log) | yes |
| T74 | Phase 3 calibration; promotion record (exploratory → operational, signed) | yes |
| T75 | Phase 1 data onboarding; semantic mapping sets (mappings.csv + RO-Crate MappingSet) | yes |
| T76 | Phase 0 decision point; "Valid use / out of scope" field in the Object Passport | yes |
| T77 | Phase 1 data onboarding; three-zone file ingestion (landing / trusted / refined) | yes |
| T78 | Phase 4 & 7 linked nodes; twin-to-twin notification on the TARP | yes |
| T79 | Phase 0–6 build; per-twin workspace layout (common / etl / calibration / forecasts / simulations) | yes |
| T80 | Phase 1 data onboarding; four named open-data ETL streams for the field twin | yes |
| T81 | Phase 2 indicator catalogue; new domain sections §21–§31 and §18 quick sets | yes |
| T82 | Phase 1 data onboarding; automated satellite fetch + latency honesty | yes |
| T83 | Phase 1 data onboarding; registered virtual sensors with published formulas and skill scores | yes |
| T84 | Phase 2 indicator catalogue; Forest module §30, quick set, worked example, sources | yes |
| T86 | Phase 2 indicator catalogue; Non-peat wetlands and marshes module §32, quick set, worked example, regional case, sources | yes |
| T85 | Phase 2 indicator catalogue; Cropland module §31, quick set, worked example, sources | yes |
| T87 | Phase 2 indicator catalogue; Barguzinsky bear worked example (second §30 example), cross-reference rows, sources | yes |
| T88 | Phase 1 data onboarding; full sensor registry, four tiers, registered virtual sensors | yes |
| T89 | Phase 2 indicator catalogue; both [unverified] flags closed as verified negative results (marmot density, WHO 9 m²) | yes |
| T90 | Phase 1/2 threshold anchors; thresholds source guide applied, anchor hierarchy, thresholds by use, operational early-warning level | yes |
| T91 | Phase 1/2 calibration; remaining priority [NEXT DATA] gaps verified as negative results (Beira-local SS_RMSE Sensors 1–4, Langtang ground truth, Daursky marmot density) | yes |

## Run log
- 2026-10-28 — v2.8 PFAS and microplastics in the safety gate (T93, candidate only, on her word "Да, добавь PFAS и микро пластик"). Both were already conditional panels in the catalogue (§6) but not in the gate. Added to Non-Negotiable 5 and Template 2 (SafetyGateCard) in SKILL.md and SKILL.ru.md: PFAS row with jurisdictional anchors (US EPA NPDWR Apr 2024: PFOA/PFOS 4.0 ng/L, PFHxS/PFNA/GenX 10 ng/L, Hazard Index 1; May 2025 retention of PFOA/PFOS and proposed rescission of the other four disclosed; EU Directive 2020/2184: sum of 20 PFAS 0.1 µg/L, total PFAS 0.5 µg/L; no universal sediment/soil PFAS limit — jurisdiction soil limit or [НЕТ ДАННЫХ] blocks) and a microplastics row with no invented numeric limit (gate checks the harmonized method — named method, size range, polymer ID, blank controls — and the reported load; unnamed method, failed blanks or unmeasured load blocks). New test T93 (`TestSafetyGatePfasMicroplastics`, 4 tests). Verification: full test suite passes (293 tests); strict lint passes from a copy installed as 'ecosystem-digital-twin/' — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 quick fixes from the external 7.5/10 audit (T92, candidate only, on her word "Да, внеси быстрые правки"). Audit verified against the files first: two points were wrong and were NOT applied as written — the HTML comment before the frontmatter is only in SKILL.ru.md (SKILL.md frontmatter already starts on line 1), and no code checks a `[NO DATA]` literal (zero occurrences in the whole candidate; mismatch.py uses Russian `[НЕТ ДАННЫХ]`). Applied: frontmatter description rewritten for v2.8 in SKILL.md (725 chars) and SKILL.ru.md (816 chars), now naming forests, peatlands, marine and coastal waters, urban ecosystems, deserts, tundra and cryosphere, cropland and livestock farms; Deterministic Script I/O Schemas table moved from SKILL.md to `references/scripts.md` (31 lines) with a short pointer in SKILL.md and pointers in both Companion Documents lists, plus the missing 17th row added in the move — `scripts/fetch_satellite.py` (the agreed morning fix of 2026-10-27, not yet applied; row written from the script's own --help and docstring). SKILL.md now 469 lines (was 491). Two existing tests repointed to the moved table (drift documented, class-thresholds documented — content preserved, location changed, no assertion weakened). New test T92 (`TestQuickFixesOct28`, 3 tests). Verification: full test suite passes (289 tests); strict lint passes from a copy installed as 'ecosystem-digital-twin/' — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 remaining priority [NEXT DATA] gaps verified (T91, candidate only). (1) Beira-local SS_RMSE Sensors 1–4: verified negative results — chlorophyll-a and temperature exist only as interpolated supplement maps (Figs. S7–S8, S1–S2), no per-station table, and the paper never applied NDCI or Landsat ST at Beira; extent is one total (65.4 ha), not a mask; turbidity never measured in situ. Corrected the "Figs. S7–S9" citation (supplement list has only S7–S8). (2) Langtang ground truth: no GNSS/levelling; ICIMOD synthesis and Roy et al. 2026 (DOI 10.1007/s12524-026-02611-x) are satellite-only; pre-collapse deformation can never be scored retrospectively; Sah 2026 EarthArXiv preprint recorded as a caution, not evidence. (3) Daursky marmot density still unpublished and still [NEXT DATA]; context added (species range 1–7 ind/ha, IUCN species account, Zenodo 6819035; Hustai comparator ca. 1.27 ind/ha, Todgerel 2020, secondary citation) with the named next source (reserve «Летопись природы» / DIPA counts). Updated worked-examples, sensor-registry, indicators (§22, §21 InSAR row; no "[provisional]" in indicators.md, per T81), sources-new-sections (§21, §22, virtual-sensor note). New test T91 (`TestRemainingNextDataGapsVerified`, 6 tests). Three test-side wording defects found by the suite and fixed (line-wrap fragments, regex window); no file content was weakened to pass a test. Verification: full test suite passes (286 tests, 280 baseline + 6 new); strict lint passes from a copy installed as 'ecosystem-digital-twin/' — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 thresholds source guide applied (T90, candidate only). Added: `references/thresholds.md` (358 lines) — the draft guide carried over verbatim (body identical except status header and closing line): 20 indicators, 5 jurisdictions (WHO, EU, USA, Russia, Japan); anchor hierarchy (jurisdiction law → WHO → literature → object baseline; stricter governs red), thresholds by use (§7), operational early-warning level (§8, yellow at 70–80% of the regulatory limit), decision support (§9, ЛПР); all 21 [provisional] marks preserved; Russian lead in drinking water NOT entered as a value (§1.7 row "Не проверено", §10 item 2); 14 open items kept as [NEXT DATA]. Rules wired into SKILL.md Stage 1, Stage 6 and Companion Documents (now 491 lines by `wc -l`, 492 by lint count, under 500; pointer mirrored in SKILL.ru.md) and into `references/indicators.md` §19/§20. No per-country value hard-coded into SKILL.md; no value invented. New test T90 (`TestThresholdsGuideApplied`, 8 tests). One defect found by the suite and fixed: the §19 pointer first used the word "[provisional]", forbidden in `indicators.md` by T81 — reworded. Verification: full test suite passes (280 tests, 272 baseline + 8 new); strict lint passes from a copy installed as 'ecosystem-digital-twin/' — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 both [unverified] flags closed (T89, candidate only, on her word "Заверши 2 пометки"). (1) §22 marmot-density threshold closed as a verified negative result: no standardised density threshold exists — IUCN criteria use decline rates, extent and mature-individual counts, not density; the Russian 1983 census guidelines are a survey method. Row now uses the object's own baseline with trend over ≥3 survey rounds; status context tarbagan Endangered (IUCN A2ad), bobak Least Concern (Bazhenov 2019); restoration-design minimum ≥10 families / ≥50 individuals (Enkhsaikhan et al. 2021, Proc. Inst. Biol. 37:30–36, DOI 10.5564/pib.v37i1.3137, verified against the paper's text); plague-risk cut-point 0.63 marmots/ha (Xu et al. 2023, Sci. Rep. 13:11906, DOI 10.1038/s41598-023-38966-1, verified against PMC). (2) §26 green space per capita closed: 9 m² is Italian planning law D.M. 1444/1968 (2 April 1968: 18 m² public space, 9 m² public greenery per inhabitant, new settlements), verified via Land 2024, 13(12):2174; not a WHO figure — Czesak & Różycka-Czas 2025 (DOI 10.1016/j.landurbplan.2025.105301) searched the cited WHO reports and found it in none, and Mostafa & Alshahrani corrigendum 2025 (Front. Sustain. Cities 7:1542464, DOI 10.3389/frsc.2025.1542464, 3 April 2025) deleted the WHO attribution (Figure 4, Table 1, Conclusion). WHO's verified guidance is accessibility — 0.5–1 ha within 300 m (WHO Regional Office for Europe 2017 brief, rule of thumb, verified against the WHO PDF). Updated in `references/indicators.md` (both rows + §26 note) and `references/sources-new-sections.md` (§22 note, §26 item (a), §26 verification note). The thresholds-guide DRAFT carries no 9 m² claim, so it needed no edit; SKILL.md / SKILL.ru.md carry no mention of either flag, so they are unchanged. New test T89 (`TestUnverifiedFlagsClosed`, 3 tests) + T81 flag test re-pinned to assert closure. Remaining [NEXT DATA] gaps for these rows: current marmot density (individuals/ha) for a named object (Daursky worked example); no [NEXT DATA] gap for the green-space row — the Italian benchmark and the WHO accessibility rule are both verified. Verification: full test suite passes (272 tests, 269 baseline + 3 new); strict lint passes from a copy installed as 'ecosystem-digital-twin/' — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 full sensor registry (T88, candidate only, on her word "Собери полный реестр датчиков"). Added: `references/sensor-registry.md` (315 lines) — Part A carries the seven registered virtual sensors verbatim (six named: five Beira, one Langtang — S1–S6 — plus the Object Passport "Virtual sensors" block as the reusable seventh form, with an explicit note that no seventh sensor with a formula exists and none is invented); Part B is a 59-row table (R01–R59) mapping every source in `references/data-sources.md` to the ecosystems (§§1–32) and indicator rows it serves, in four tiers — Core 1 (R05, Secchi depth at Beira, RMSE 0.049 m, Prasad et al. 2024), Conditional 35, Research 3, Context-only 20; all 48 canonical source names appear, and all 29 indicator-bearing sections (§§1–17, §§21–32) are served. Eight new sources added to `references/data-sources.md` §12 (now 265 lines) with resolution, cadence, access and measurement-vs-model notes: NASA FIRMS (VIIRS 375 m, < 3 h, free MAP_KEY), Global Forest Watch / Hansen (user's accuracy 87.0% for loss, Hansen et al. 2013), ESA WorldCover (overall accuracy 74.4%, 2020), OpenStreetMap (ODbL), GPM IMERG (0.1°, half-hourly, v07), SMAP (ubRMSE 0.038 m³/m³ surface, Reichle et al. 2017), Copernicus Marine Service / OSTIA (daily, 0.05°), WDPA / Protected Planet (free non-commercial; Russia-data restriction caveat). No formula, score, or calibration station invented anywhere: every numeric score carries its citation, every missing score is [NEXT DATA] (43 occurrences). One-line pointer added to SKILL.md (now 485 lines by the lint's count, under the 500 limit); CHANGELOG.md entry added. New test T88 (`TestSensorRegistry`, 7 tests). Loop score 9/10, one round (evaluate → self-check → correct → score). Defects found and fixed in the round: (1) R05's formula contained literal "|" characters (absolute-value bars) that split the markdown table row — replaced with abs(...) notation; (2) two test-string mismatches against hard-wrapped file text (S7 sentence, WDPA caveat phrase) — test wording corrected, no registry content changed; (3) the §5 coverage claim ("all 32 sections") was wrong — §§18–20 are meta sections no sensor serves, and §16 was unserved — fixed by adding §16 to R01 and R33 and correcting the claim to the 29 indicator-bearing sections, with a new section-coverage test pinning it. Verification: full test suite passes (269 tests, 262 baseline + 7 new); strict lint passes from a copy installed as 'ecosystem-digital-twin/' (exit 0, no errors or warnings) — in place it fails only on the pre-existing folder-name artefact, as before. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 Barguzinsky bear worked example, second example for §30 (candidate only, on her decision of 27 October 2026, 22:10 EDT — an explicit exception to the "no Russian worked examples" rule, only with links to authoritative sources for every figure). Source: `~/workspace/buryatia-bears-analysis.md` (sections 3.1, 4, 6). Added: second worked example in `references/worked-examples-new-sections.md` (now 901 lines) with verified figures (Buryatia bears 6,113 / 6,276 / 5,385 / 4,625; density 0.21 per 1,000 ha; 47 exits in 2025; regulated 149 / 331 / 436; 6 attacks, 2 dead; harvest limit 1,272, about 900 permits, about 300 harvested a year; reserve 374,322 ha; sable 20–30 at creation → 1,500–2,000 today) and the reliability caveat (departmental figures as relayed by the press; primary summaries not published openly); bear source list (12 sources) and verification note in `references/sources-new-sections.md` (now 1,990 lines); cross-reference rows in §15 (2: brown bear abundance, age structure), §17 (3: conflict reports, attractants register, quota uptake) and a taiga-edge watch-level paragraph in §20; one new §30 row (mast yield index, Research, [NEXT DATA]). [NEXT DATA] gaps named in the example (bear numbers in the reserve itself; quantitative mast index for Buryatia 2026; wolf numbers; attractants register; numeric young-share; long-term attacks series). Counts updated in SKILL.md, SKILL.ru.md, CHANGELOG.md. Catalogue now 32 sections, 411 rows (185 + 226), 348 distinct indicators (163 new, 63 cross-references). New test T87 (`TestBarguzinskyBearExample`, 4 tests); T81 §30 fragment count re-pinned (23 lines); T84 counts re-pinned (21 rows, 16 new, exactly one [NEXT DATA] row allowed — the mast index). Verification: full test suite passes (262 tests, 18.6 s); strict lint passes from a copy installed as 'ecosystem-digital-twin/' (exit 0, no errors or warnings) — in place it fails only on the pre-existing folder-name artefact, as before; SKILL.md 483 lines, unchanged. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 Non-peat wetlands and marshes module §32 (candidate only, on her word, with her correction of 2026-10-27: no Russian worked example, pilot or showcase case — Mongolia is the regional example instead): draft `~/workspace/ecosystem-twin-wetlands-section-DRAFT.md`, looped to 9/10 in one round (evaluate → self-check → correct → score). §32 Non-peat wetlands and marshes in `references/indicators.md` (19 rows: 14 new, 5 cross-references to §4/§9/§10/§11/§15) with a Non-peat wetlands and marshes quick set in §18; Everglades worked example and Mongol Daguur regional case, and full source list, in `references/worked-examples-new-sections.md` (now 802 lines) and `references/sources-new-sections.md` (now 1,912 lines). Figures verified against primary sources: Ramsar GWO 2018 (12.1 M km², 54% permanent / 46% seasonal, 35% lost 1970–2015), Davidson 2014 (64–71% since 1900; DOI 10.1071/MF14173, verified), Sklar et al. 2005 (TP 10 µg/L), Davis & Ogden 1994 (historic ~4,000 sq mi, hydroperiod 11+ / 9–10 / 3–7 months), SFWMD wading-bird reports (138,834 nests in 2018; ~3,500 in the 2025 drought season — via Audubon / Palm Beach Post reporting of SFWMD reports, flagged in the verification note), Saltonstall 2002 (DOI 10.1073/pnas.032477999, verified against PMC), Beck et al. 2001 (DOI 10.1641/0006-3568(2001)051[0633:TICAMO]2.0.CO;2, verified), Mongol Daguur staging counts (Ramsar Information Sheet 1997; EAAF SIS EAAF024, 2017). No [unverified] flags in §32; [NEXT DATA] gaps named in both examples (Everglades accretion, fish-nursery densities, intrusion, nutrient balance, sawgrass/cattail shares; Mongol Daguur hydroperiod, accretion, retention, reed area, fish densities, current bird count). Catalogue now 32 sections, 405 rows (180 + 225), 342 distinct indicators (162 new, 63 cross-references). Counts updated in SKILL.md, SKILL.ru.md, CHANGELOG.md, README.md. New test T86 (`TestWetlandsSection`, 5 tests); T81 counts re-pinned to 12 worked examples / 12 source lists and the §32 fragment count; T84 count pins updated to the 32-section totals (fixing the one stale Russian 30-section assertion left by the §31 application). Coordinator correction 2026-10-28: the T85 entry DOES exist in TESTS.md (## T85 and traceability row) and the TestCroplandSection class exists in test_scripts.py — the §32 run-log note to the contrary was an error. Verification: full test suite passes (258 tests, coordinator-verified) and the non-strict package lint passes; the strict lint fails on one pre-existing check only — the candidate folder name 'ecosystem-twin-v2.8-candidate' differs from the skill name 'ecosystem-digital-twin' (a directory-name artefact, not §32 content; strict lint passes from a copy installed as 'ecosystem-digital-twin/'); SKILL.md 483 lines, unchanged. Nothing published: the live skill and GitHub are untouched.
- 2026-10-27 — v2.8 Cropland module §31 (candidate only, on her approval of 2026-10-27): draft `~/workspace/ecosystem-twin-cropland-section-DRAFT.md`, looped to 9/10 in one round (evaluate → self-check → correct → score). §31 Cropland in `references/indicators.md` (21 rows: 15 new, 6 cross-references to §5/§9/§10/§11/§14/§15) with a Cropland quick set in §18; GEPIS rice-paddy worked example and full source list in `references/worked-examples-new-sections.md` (now 701 lines) and `references/sources-new-sections.md` (now 1,737 lines). Figures verified against primary sources: FAO SOLAW 2025 (agriculture 4.8 B ha, 72% of withdrawals; irrigated 22.5% of croplands, 48% of crop value, +76% yields; 1.6 B ha degraded, 60% agricultural; 64% of agricultural land at pesticide-pollution risk), FAO salt-affected soils 2024 (1,381 Mha, 10.7% of land; 10% of irrigated and rainfed cropland; yield losses up to 70%), FAOSTAT Brief 90 (fertiliser 185 Mt in 2022: N 108, P 42, K 35), FAOSTAT Brief 70 (pesticides 3.54 Mt, 2.26 kg/ha, 2021), Borrelli et al. 2017 (cropland erosion 12.7 t/ha/yr, 17 Pg/yr; DOI 10.1038/s41467-017-00232-0), Bowles et al. 2020 (+28.1% maize yield, drought losses cut 14.0–89.9%; DOI 10.1016/j.oneear.2020.02.007), Albrecht et al. 2020 (flower strips +16% pest control; DOI 10.1111/ele.13576), Luo et al. 2010 (no-till no total SOC gain to 40 cm), Mikhailova & Post 2006 (Kursk chernozem SOC 0–2 m: grassland 462, meadow 451, arable 387, fallow 349 t/ha; DOI 10.1111/j.1365-2389.2005.00741.x), Plotnikova et al. 2024 (SOC falls with erosion degree, Kursk; DOI 10.3390/agronomy14081607), Prasad et al. 2024 (Beira Lake WPI 2.4–2.5; DOI 10.3390/w16111616), Wanasinghe et al. 2023 (paddy ET Maha 470 mm, Yala 677 mm; DOI 10.4038/tar.v34i2.8626), IPCC 2019 Refinement rice scaling factors (single drainage 0.71, multiple 0.55). No [unverified] flags in §31; [NEXT DATA] gaps named in the GEPIS example (measured yield, water use, CH₄/N₂O fluxes, SOC, ECe, margins, erosion); USDA 2025/26 record figures flagged as press-reported estimates, not yet checked against the USDA release; the FAO cropland N-surplus figure kept out of the row anchor (underlying brief not directly read). Russian material only as published-data anchors — no Russian worked example, pilot or showcase case, per her correction of 2026-10-27 (the parent task's "Russia stays in" instruction predates that correction; conflict flagged in the handoff). One fix during application: the word "provisional" removed from the §31 indicators.md note because T81 asserts it absent from the catalogue. Catalogue now 31 sections, 386 rows (180 + 206), 328 distinct indicators (148 new, 58 cross-references). Counts updated in SKILL.md, SKILL.ru.md, CHANGELOG.md, README.md. New test T85 (`TestCroplandSection`, 5 tests); T81 counts re-pinned to 11 worked examples / 11 source lists and the §31 fragment count; T84 counts re-pinned to 31 sections / 206 rows. Verification: 253 tests pass; strict lint passes; SKILL.md 483 lines, unchanged. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 Forest module §30 (candidate only, on her word «Лес добавь также с модулем»): draft `~/workspace/ecosystem-twin-forest-section-DRAFT.md`, looped to 9/10 in one round (evaluate → self-check → correct → score). §30 Forest in `references/indicators.md` (20 rows: 15 new, 5 cross-references to §9/§10/§11/§15) with a Forest quick set in §18; Harvard Forest worked example and full source list in `references/worked-examples-new-sections.md` (now 635 lines) and `references/sources-new-sections.md` (now 1,625 lines). Figures verified against primary sources: FAO FRA 2025 (4.14 B ha, 32%; net loss 4.12 M ha/yr; deforestation 10.9 M ha/yr; primary 1.18 B ha; carbon 714 Gt; 813 M ha protected), FRA 2020, Pan et al. 2011 (2.4 ± 0.4 Pg C/yr), Barford et al. 2001 (2.0 ± 0.4 Mg C/ha/yr), Finzi et al. 2020 (NEP ~300 hardwood / ~450 hemlock g C/m²/yr; source after 2014), Ellison et al. 2010 (basal area 29.6–53.0 m²/ha; girdled dead in 30 months), Curtis et al. 2018 (commodity 27%, forestry 26%, shifting agriculture 24%, wildfire 23%; DOI 10.1126/science.aau3445, verified — the journal-page DOI form first written was an invented guess and removed), Andela et al. 2017 (−24.3 ± 8.8%), Müller & Bütler 2010 deadwood 20–50 m³/ha (SoEF 2020 European average 11.5 m³/ha), BC mountain pine beetle >18.3 M ha / 731 M m³. No [unverified] flags in §30; [NEXT DATA] gaps named in the Harvard example (current canopy, deadwood, biomass stock, regeneration density, fragmentation). Catalogue now 30 sections, 365 rows (180 + 185), 313 distinct indicators (133 new, 52 cross-references). Counts updated in SKILL.md, SKILL.ru.md, CHANGELOG.md, README.md. New test T84 (`TestForestSection`, 5 tests); T81 counts re-pinned to 10 worked examples / 10 source lists and the §30 fragment count; T83 tail bounded at §30; row-count filter fixed (the §11 row «Indicator and diagnostic species presence» was miscounted as a header). Verification: 248 tests pass; strict lint passes; SKILL.md 483 lines, unchanged. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 registered virtual sensors, Variant B (candidate only, on her word): six virtual sensors registered in the Object Passport form as a worked example (`references/worked-examples-new-sections.md`, now 576 lines) with full sources (`references/sources-new-sections.md`, now 1,511 lines). Beira Lake: Sentinel-2 chlorophyll-a (NDCI, Mishra & Mishra 2012; RMSE 1.43 µg/L below 30 µg/L; Molkov et al. 2019: 3.02 µg/L), Landsat 8/9 water surface temperature (Gerace et al. 2020 split-window; Eon et al. 2023: 0.87 K L8 / 0.74 K L9), water extent (MNDWI, Xu 2006; Pekel et al. 2016: under 1% false water, under 5% missed), turbidity (Dogliotti et al. 2015; RMSE 20.5 FNU, n = 106), Secchi depth (Lee et al. 2015 QAA; Beira-local RMSE 0.049 m, R² = 0.670, n = 43, Prasad et al. 2024). Langtang slope: Sentinel-1 InSAR displacement (40 cm / 48 days, ICIMOD 2026; ±10 mm against levelling/GNSS). Every formula and skill score read from the cited paper itself on 2026-10-28; five local-score gaps named honestly ([NEXT DATA]). Sentinel-1 and Open-Meteo added to `references/data-sources.md`. New test T83 (`TestRegisteredVirtualSensors`, 3 tests). Verification: 243 tests pass; strict lint passes; SKILL.md 483 lines, unchanged. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 automated satellite fetch (candidate only, on her word): new `scripts/fetch_satellite.py` (stdlib-only STAC: `urllib` + `json`; NDVI via optional `rasterio`/`numpy`, deferred without it); Planetary Computer STAC verified live 2026-10-28 (3 Sentinel-2 scenes over the Langtang bbox, B04/B08 links; 82–89% cloud, correctly dropped by the default `--max-cloud 20`); Copernicus Data Space STAC unreachable from this environment — account needed, verify at build time. `references/data-sources.md` gained a script section and a latency-honesty table (satellite periodic, never real-time; ground telemetry the only real-time layer); SKILL.md gained three pointers. New test T82 (`TestFetchSatellite`, 8 tests, offline on a recorded STAC response). Verification: 240 tests pass; strict lint passes; SKILL.md 483 lines. Nothing published: the live skill and GitHub are untouched.
- 2026-10-28 — v2.8 second-layer flag check (candidate only): all 4 [unverified] flags and all 3 [NEXT DATA] gaps re-checked against primary sources. Closed: EU 2024/1244 500 t (Annex I row 7; N/P reporting only above Annex II thresholds N 50,000 / P 5,000 kg/yr); water-use benchmark (no universal benchmark; per-type throughput ranges, throughput vs make-up kept separate). Daursky: gazelle 18,898 counted / 21,701 estimated (June 2020) and marmot families (3,300–4,100 regional; 75–85 buffer, ~30 reserve) closed; reserve-only gazelle total, current marmot density, burned area, SOC stay open. North Wyke: N balance, housed-cattle CH₄ 170–174 g/day, NH₃ pad rate 2.5 g m⁻² d⁻¹ closed; P balance, whole-platform CH₄ total, measured whole-farmlet NH₃ flux stay open. Toolik: shrub cover +132.3%, active layer 28–52 cm (no trend), caribou 26,600, SOC 5–25 kg C m⁻², fluxes closed; lemming densities stay open (NEON dataset next lead). Staying flags with documented negative checks: marmot threshold (no standard exists) and WHO 9 m² (Czesak & Różycka-Czas 2025). Tests updated (two T81 tests re-pinned). Verification: 232 tests pass; strict lint passes; SKILL.md 482 lines. Nothing published: the live skill and GitHub are untouched.
- 2026-10-27 — v2.8 first-layer improvements (candidate only): (1) worked examples and full source lists from the nine module drafts moved into the candidate as `references/worked-examples-new-sections.md` (355 lines, 9 examples) and `references/sources-new-sections.md` (1,423 lines, 9 source lists), copied verbatim by script and re-checked block by block — all 9 examples verbatim; the 8 shorter source blocks end exactly where each draft's "## Self-check log" begins (the logs are process records, not sources, and are not carried over); the two [NEXT DATA] gaps (Daursky, Toolik) are present; the third "[NEXT DATA]" mention in the drafts sits in the tundra self-check log and describes the Toolik gap, so nothing is lost. Both files carry a `## Contents` list near the top (package lint requires it for references files over 100 lines). SKILL.md / SKILL.ru.md point at the two files; the stale "19-section" count is corrected to 29 in both. New regression test in `TestNewSections` (now 5 tests). (2) `assets/templates.md` §10 gains a filled status-line example in plain words (Delhi resident asking about the air; status red; recommendation in ordinary words; format example only, no numbers invented). (3) Liu et al. 2026 verified against the full text of the paper ("Anthropogenic Disturbance Dampens Climate-Driven Greening in the Arctic", J. Remote Sens. 6, 1062, DOI 10.34133/remotesensing.1062; eight authors; published 5 August 2026): 2,221 clusters, 21,402 km² (435 settlement — 12,902 km²; 1,786 non-settlement — 8,500 km²), 2000–2020, Landsat 5/7/8 Collection 2 Tier 1, 30 m, 16.1%. The provisional flag is removed from the §29 row, the tundra draft's table row, entry and verification note (dated addendum in the draft's self-check log; Round 1 log left as history). The earlier press-release title and two-author form are corrected wherever they appeared. Verification: 232 tests pass (231 + 1 new); strict lint passes; SKILL.md 482 lines. Nothing published: the live skill and GitHub are untouched.
- 2026-10-27 — v2.8 loop-evaluation round 1 (candidate only): independent re-check of the assembly found and fixed 3 defects. (1) The §27 aquaculture table arrived hard-wrapped: 11 of its 19 rows spanned several physical lines, splitting the table into 12 fragments in strict Markdown rendering (only the first fragment rendered as a table). All rows joined to single lines (93 lines → 21: header + separator + 19 rows); row counts unchanged. New regression test in `TestNewSections` (now 4 tests) pins each §21–§29 table as one contiguous block. (2) §25 DHW row overstated the NOAA wording ("reef-wide bleaching" at Alert Level 1) — corrected to NOAA's "bleaching likely" (Level 1) and "bleaching with mortality likely" (Level 2), verified against the NOAA Coral Reef Watch alert ladder (HotSpot ≥1 °C, DHW ≥4 / ≥8 °C-weeks). (3) The green state was unnamed and the public status line had no traffic-light field: §20 now names green explicitly (no band breached = measures working; amber = measures insufficient; red = measures failed or acute risk), `assets/templates.md` §10 gains Status (green / yellow / red) and Recommendation fields, SKILL.md Stage 6 names the colour and the recommendation in the status-line description. Verification after the fixes: 231 tests pass (230 + 1 new); strict lint passes; SKILL.md 480 lines. Nothing published: the live skill and GitHub are untouched. Round 2 self-check found one drift: the SKILL.md status-line wording had no mirror in SKILL.ru.md — mirrored (green / yellow / red + recommendation); re-verified 231 tests pass, lint passes, SKILL.md 480 lines, SKILL.ru.md 526 lines.
- 2026-10-27 — v2.8 assembly (candidate only, unreleased draft): nine new domain sections §21–§29 integrated into `references/indicators.md` from the nine 9/10 module drafts (165 new table rows: 118 new indicators, 47 cross-references; catalogue now 29 sections, 345 rows, 298 distinct indicators); nine new §18 quick sets, each checked against its section's table; version assigned 2.7 → 2.8 in SKILL.md (YAML, title, Current version, Citation), SKILL.ru.md, CITATION.cff, README.md / README.ru.md (badge, Current version, Citation, Ecosystems covered, brand note), tests/TESTS.md title, and the `scripts/evidence_search.py` User-Agent; descriptive name 'Ecosystem Digital Twin by Rigjita Baldanova' in the titles; brand name pending the author's decision (candidates ADIS and RB); licence stays CC BY 4.0 (BY-ND for v2.8+ pending her «да»). New test T81 (`TestNewSections`, 3 tests). One assembly decision: the §28 desertification-extent row is a cross-reference to the §22 SDG 15.3.1 composite (same indicator, not a second copy); one label change: the §18 quick set is 'Cryosphere / mountain' (draft said 'Mountain / cryosphere') to match the section title. Verification: 230 tests pass; strict lint passes from a fresh copy installed as `ecosystem-digital-twin/`; SKILL.md 480 lines; BEIRA-F-001 untouched, chain verifies. Nothing published: the live skill and GitHub are untouched.
- 2026-10-26 — v2.7 RELEASE (author's decision, 'Внести последнюю версию. Оформить профессионально', 23:05 EDT; staging only, prepared for the GitHub release): version assigned 2.4 → 2.7 in SKILL.md (YAML, title, Current version, Citation), CITATION.cff, README.md / README.ru.md (badge, Current version, Citation v2.7), tests/TESTS.md title, and the `scripts/evidence_search.py` User-Agent. Affiliation removed from CITATION.cff (author's decision: the latest version carries no affiliation); the CHANGELOG's historical v2.3 DOI record was reworded to carry no affiliation (the v2.7 CHANGELOG entry and this run-log entry record the removal itself). Definition corrected (author's decision): the skill IS a digital twin of ecosystems; the '(the consulting traffic light)' label removed from the Tier S / M / L header and 'consultant's method' corrected in the CHANGELOG. Professional README (EN + RU): 'Ecosystems covered' (nine domains, each with its gallery proof or real-data case), Keywords (14 GitHub topics), Author section, scripts table completed to all 16 scripts, stale references corrected (227 tests, T1–T80, roadmap and citation v2.7). CHANGELOG v2.7 release entry created (the one version at the end). Verification: 227 tests pass; strict lint passes from a fresh copy installed as `ecosystem-digital-twin/`; SKILL.md 477 lines. The CITATION.cff DOI is still the v2.3 record (10.5281/zenodo.23657185) until the Zenodo release mints a new one; a DOI-update PR follows. Nothing published: the GitHub release is a separate step.
- 2026-10-26 — Laguna borrowing patch (author's decision, 'Сейчас', after the four prioritized items were presented; staging only, unreleased draft): four patterns borrowed from the Agricultural Digital Twin Platform (Laguna et al. 2025, Computers in Industry 172, 104347, DOI 10.1016/j.compind.2025.104347, MIT license) — PATTERNS ONLY, no code copied, none of its stack adopted (Docker / Temporal / MongoDB / Minio / MLflow / Go / SvelteKit), none of its ML approach (a Random Forest yield model validated on one eyeballed point from explicitly fake data — that would violate Rule #1). (1) Three-zone file ingestion in SKILL.md Stage 2 + a file-zone field on the Phase 1 onboarding checklist (`assets/templates.md` §1) + a zones note in the `scripts/qc_series.py` docstring: landing (as received, untouched) → trusted (QC-passed) → refined (domain-converted, model-ready); a file leaves landing only after its QC is recorded, enters refined only after its conversion is recorded. (2) Twin-to-twin notifications in SKILL.md Stage 7 + a "Linked nodes notified" field on the TARP (`assets/templates.md` §3): when an alert fires, the twin notifies its linked nodes; recorded on the TARP, not in the forecast registry; a notified node re-checks its own alert bands on the next batch. No new registry entry type — a notification is a communication act on the TARP, not a forecast record. (3) Per-twin workspace layout in SKILL.md Stage 2, cross-referenced from the Stage 7 build-manifest sentence: common / etl / calibration / forecasts / simulations; Laguna's ml-training folder is adapted away (this skill has no ML-training step, pinned by test). (4) Four named open-data ETL streams for the field twin in `references/data-sources.md` §10 (daily, forecast, historical weather, NDVI — ERA5, national meteo, Sentinel-2/Landsat, MODIS/VIIRS as context) with a one-line cross-reference from the field gallery README; the list lives in one place only. One test-expectation slip fixed during the build (capital "A file enters" vs the file's lowercase after a semicolon). Verification in staging: 227 tests pass (219 baseline + 8 new: T77 2, T78 2, T79 2, T80 2); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Audit-fix patch, Variant 1 + Variant 2 (author's decision, 'Да, вариант 1+2: чинить текст и гейты'; staging only, unreleased draft): an external model's line-by-line audit of the v2.7 candidate was verified against the files by the author-side agent (21:10 EDT) and its findings fixed here. Text (Variant 1): the SKILL.md I/O table now describes all 16 scripts (rows added for `scripts/sensitivity_screen.py`, `scripts/forecast_bulletin.py`, `scripts/mismatch.py`, transcribed from the code); the Object Passport gains a 'Primary target variables' field and a per-indicator 'Drift threshold' field in both the SKILL.md Template 1 summary and `assets/templates.md` §1; Core Mathematical Specifications gains formulas 7–12 (HQ/HI, Shannon/Pielou/Delta+ with the natural-log base and the Clarke–Warwick rank weights as implemented, KGE, nudge, drift with leeway, the Stage 7 drift statistic) — the original 6 formulas untouched; a maturity cross-walk in Template 1 (Prototype = Conceptual Proposal = ladder level 1, exploratory; operational = ADMITTED + recorded promotion = Predictive/Decision; downgrade follows the existing Stage 3 rule) with a one-line cross-reference in Non-Negotiable 2; the trend_test.py preamble now lists all 6 modes; the Companion Documents header drops the stale '(retained from v2.2)'; the gallery names now match the `examples/gallery/` directories (forest-fire, forest-logging, forest-carbon, biodiversity); YAML last-reviewed 2026-10-25 → 2026-10-26. Gates (Variant 2): `skill_scores.py alert-trial` gains a third verdict INCONCLUSIVE_QUIET_WINDOW (exit 0) for a window with no alerts and no critical events — it neither admits nor rejects; critical events with no alerts still FAIL; `skill_scores.py admit` requires SS_RMSE > 0 only for PRIMARY target variables (optional `primary` flag per variable; when no variable carries the flag, every variable is primary — the pre-2.7 behaviour, backward compatible); the Tier S / M / L gradation ('Консалтинговый светофор') is stated in SKILL.md at the head of the 7-stage cycle and cross-references the ten-step Tier S path in `references/quick-start.md` (unchanged — it already was the Tier S path). Two audit points were corrected during verification and NOT applied as written: the auditor claimed the passport lacked the nudge-N and model-ladder tolerance fields (both are in `assets/templates.md` §1 — only drift_threshold was genuinely missing) and claimed no maturity downgrade rule existed (SKILL.md Stage 3 states it); the auditor's weighted score was 8.7, not 8.8 (0.25 × 34.8 = 8.70). The audit's source_ref-column requirement for reference tables and the 'Executive VoI & Sunk-Cost Summary' card were NOT implemented (separate decisions, offered later). Four gallery tests (`TestWetland`, `TestForestFire`, `TestForestLogging`, `TestForestCarbon`) asserted the old space-separated gallery names in SKILL.md and were updated to the hyphenated directory names; the gallery line was re-wrapped so the asserted substrings stay on one line. Verification in staging: 219 tests pass (214 baseline + 5 new: T51 +2, T52 +3; the T51 count is 9, not 7, and T52 is 8, not 5); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Ellenberg trait-table correction (author's decision, 'Да, исправь таблицу до v2.7'; staging only, unreleased draft): the field gallery entry's `trait_table.csv` was checked against the published Ellenberg values (the Ellenberg column in Tichý et al. 2023, Zenodo 7427088) and did NOT match — only 14 of 40 values, largely reconstructed from memory. Replaced with the corrected table (7 taxa; "x" where Ellenberg is indifferent; Triticum aestivum removed — Ellenberg does not list cultivated wheat; Salicornia values are ssp. europaea). `scripts/trait_match.py` gained the indifferent rule: a taxon with "x" for a trait is not excluded by a condition on that trait, and the output names it in `indifferent`; a cell that is neither a number nor "x" is refused (exit 2). The three T67 expectation tests were rewritten to the corrected values (saline site S ≥ 8 fits only Salicornia europaea; N ≥ 7 fits Trifolium by indifference and excludes Salicornia and Puccinellia at N = 4; T within 6 ± 1 fits all 7 taxa, two by indifference) plus one new test pinning the indifferent rule and the malformed-cell refusal. Provenance lines fixed in `scripts/trait_match.py`, `references/indicators.md` §11 and the field-gallery README (exact source + verification date 2026-10-26); the field `mappings.csv` justifications aligned to the same citation. Verification in staging: 214 tests pass (213 baseline + 1 new; the T67 count is 5, not 4); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 4 of the v2.7 program (second-wave borrowing, governance-and-depth, LAST round; staging only, unreleased draft): all 8 functions built in the approved order — Sensitivity-first calibration (Gironde), Model ladder (Digital Baikal), Adaptation appraisal + equity + M&E (DestinE), Driver-perturbation table (Southern Water), Mismatch register (Patos), Promotion record (Gironde), Semantic mapping set (BioDT), "Valid use / out of scope" field (BioDT). New scripts `scripts/sensitivity_screen.py`, `scripts/mismatch.py`; new subcommand `scripts/registry.py promote`; new `mappings` entity type in `scripts/build_manifest.py` (one MappingSet File per `mappings.csv`, SSSOM-conformant); new forms in `assets/templates.md` §12 (mismatch register entry) — twelve fillable forms, not eleven — and new fields in §1 (model ladder, promotion record, valid use / out of scope, semantic mapping) and §4 (adaptation appraisal) and §8 (driver-perturbation sensitivity block); new subsections in `references/scenarios.md` (adaptation appraisal + M&E, driver-perturbation table), `references/uncertainty-decision.md` §3 (mismatch register — the learning log, not a gate) and `references/data-sources.md` §6 (semantic mapping sets). Boundaries stated in the docs: sensitivity screen perturbs MODEL parameters, driver-perturbation table perturbs INPUT drivers (never merged); the mismatch register is the learning log, distinct from the pass/fail gates (alert trial, hindcast reproduction gate). Three older tests that asserted "eleven" fillable forms were updated to the new count, and the T57 entry updated. Two slips found and fixed during the build: a Round 3 test (`TestExposureInventory`) asserted the old scenario-scoring wording that F3 changed (updated with a Round 4 comment — the scoring rule genuinely changed), and a case slip in the T69/T70 assertions ("One-at-a-time" / "(the Model ladder)" capitalization). One docs edit failed on a wrong `old_text` and was retried with the correct text. Verification in staging: 213 tests pass (192 Round 3 baseline + 21 new); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 3 of the v2.7 program (second-wave borrowing, forecast-quality + biodiversity; staging only, unreleased draft): all 8 functions built in the approved order — Hindcast reproduction gate (EDITO), Skill-vs-lead-time curve (lake platforms), Observation-nudged forecast (lake platforms), Phenomenon-oriented metrics (EDITO), Diversity indices (BioDT), Plant functional type shares (BioDT), Trait–environment matching (BioDT), Spread-informed sampling priority (lake platforms). New scripts `scripts/diversity.py`, `scripts/trait_match.py`; new subcommands `scripts/skill_scores.py skill-horizon`, `scripts/skill_scores.py nudge`, `scripts/uncertainty_budget.py sampling-priority`; new fields on the §5 forecast registry entry (skill horizon, nudge correction, phenomenon metrics) and the §6 scenario card (reproduction check, sampling priority); new subsections in `references/scenarios.md` (hindcast gate), `references/analytics-forecasting.md` §4 (skill horizon, nudge, phenomenon metrics), `references/indicators.md` §11 (diversity, PFT shares, trait matching) and §2 of `references/uncertainty-decision.md` (sampling priority — the VoI home, not §4). The biodiversity gallery runner now reports Shannon 2.8571 / Pielou 0.9885 / Δ+ 3.5098; the field gallery runner now reports PFT shares (grass 0.82, legume 0.10, forb 0.08, C3 1.00). Two slips found and fixed during the build: `trait_match.py` raised an uncaught KeyError (exit 1) for a 'within' rule without a window (now a ValueError, exit 2), and `uncertainty_budget.py`'s sampling-priority dispatch never fired because `main()` was called with `argv=None` (now normalized to sys.argv[1:]); a third was a test-expectation slip (float rendering 0.0, not 0). Verification in staging: 192 tests pass (165 Round 2 baseline + 27 new); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 2 of the v2.7 program (second-wave borrowing, coverage-and-delivery; staging only, unreleased draft): all 8 functions built in the approved order — Virtual sensors (Gironde), Deterministic drift / connectivity (EDITO), Daily forecast bulletin (Gironde), Public status line (Southern Water), One product per audience + dissemination register (Patos), Asset-relative safety margin (Patos), User-class operational thresholds (Patos), Exposure inventory + exposed fraction (EDITO). New scripts `scripts/drift.py`, `scripts/forecast_bulletin.py`; new options `scripts/registry.py issue --clearance`, `scripts/alert_bands.py --class-thresholds`; new forms in `assets/templates.md` §9 (forecast bulletin), §10 (public status line), §11 (decision product) — eleven fillable forms, not eight; new rule paragraphs in `references/indicators.md` §20 (user-class thresholds) and subsection in `references/scenarios.md` (exposure inventory and exposed fraction). Two older tests that asserted "eight" fillable forms were updated to the new count. Verification in staging: 165 tests pass (138 Round 1 baseline + 27 new); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 1 of the v2.7 program (second-wave borrowing, impacts-and-extremes + trust; staging only, unreleased draft): all 8 functions built in the approved order — Impact chain (DestinE), Event storyline (DestinE), Historical-event replay (Digital Baikal), Stochastic scenario generator (Digital Baikal), Hazard quotient / hazard index (Digital Baikal), Covariate-aware alerts (Southern Water), Alert trial (Southern Water), Calibration plausibility gate (lake platforms). New script `scripts/scenario_generate.py`; new subcommands `scripts/registry.py replay`, `scripts/skill_scores.py alert-trial`, `scripts/skill_scores.py admit`; new reference `references/calibration-bounds.md`; new `references/indicators.md` §20 (watch levels and alert rules). Two admission gates, both must pass (plausibility gate + alert trial); storyline vs replay boundary stated in both `references/scenarios.md` and `references/uncertainty-decision.md` §5. Verification in staging: 138 tests pass (105 baseline + 33 new); strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Biodiversity gallery entry REPLACED (author's decision, 'Замени другим биоразнообразие'): the removed Gusinoye lakeshore-birds entry is replaced by Khubsugul lakeshore birds, Mongolia (Lake Khubsugul / Khövsgöl, approx 51.0 N, 100.5 E) — synthetic records (deterministic formulas, 20 records, 18 species); the GBIF pull for real records was blocked (HTTP 403) and must not be retried or bypassed, so no real records are used and a real-data version is possible later via a live-browser GBIF pull. Sensitivity categories are the real IUCN Red List statuses of the lake's birds (Emberiza aureola CR withheld, Aythya ferina VU pre-rounded, the rest NT/LC generalized to 0.1°). The gallery now holds nine entries. Verification in staging: 105 tests pass; strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Biodiversity gallery entry REMOVED (author's decision, 'Убери гусиное'): the Gusinoye lakeshore-birds entry (real GBIF data, 20 records) is removed from the gallery instead of re-located — the GBIF pull for a replacement was blocked (HTTP 403) and the author chose removal. The gallery now holds eight entries; the GBIF sensitivity rules (generalize to 0.1°, withhold extreme records) stay in the skill (Non-Negotiable 3, `scripts/generalize_coords.py`). The entry is preserved in the v2.5 staging package as the program record. Verification in staging: 104 tests pass; strict lint passes from a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Gallery re-location (author's decision: no Russian landscape in the gallery):
  forest-fire, forest-logging, forest-carbon, and air re-located to
  non-Russian landscapes (fire and carbon: Prince Albert FMA,
  Saskatchewan; logging: British Columbia timber supply areas Prince
  George / Quesnel / Mackenzie; air: Prince George, BC winter PM2.5),
  with new deterministic data, new published anchors, new READMEs, and
  updated T40/T42/T43/T44. The
  biodiversity entry (Gusinoye, real GBIF data) is NOT yet re-located:
  the GBIF occurrence-search API returned HTTP 403 from this
  environment and the request must not be retried or bypassed, so the
  new pull is pending a live-browser fetch. Verification in staging:
  105 tests pass; strict lint passes from a copy installed as
  `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Forest-carbon gallery prototype (third forest entry, fourth item of the v2.6 program; staging only, unreleased draft):
  Prince Albert FMA carbon stock under `examples/gallery/forest-carbon/`
  (synthetic annual carbon density, 2015–2025; design anchors from
  UNEP boreal biomass, Alberta sequestration, and the forest-fire
  entry's burned areas; the README states the carbon-credit boundary —
  not a carbon-credit methodology, no compliance with any credit
  standard), index row in `examples/gallery.md`, SKILL.md Companion
  Documents names the forest carbon. Verification in staging: 105 tests
  pass (103 baseline + 2 new); strict lint passes from a copy installed
  as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Forest-logging gallery prototype (third item of the v2.6 program; staging only, unreleased draft):
  British Columbia timber supply areas (Prince George, Quesnel,
  Mackenzie) under `examples/gallery/forest-logging/` (synthetic
  annual logged area and harvest volume, 2015–2025; design anchors from
  BC harvest totals and the Prince George / Quesnel / Mackenzie AACs),
  index row in `examples/gallery.md`, SKILL.md Companion Documents names
  the forest logging. Verification in staging: 103 tests pass (101
  baseline + 2 new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Forest-fire gallery prototype (second item of the v2.6 program; staging only, unreleased draft):
  Prince Albert FMA fire seasons under `examples/gallery/forest-fire/`
  (synthetic monthly fire counts and burned area, Apr–Oct 2019–2025;
  design anchors from the CIFFC 2023 national record, Saskatchewan
  2023, and the Prince Albert FMA), index row in
  `examples/gallery.md`, SKILL.md Companion Documents names the forest
  fire. Verification in staging: 101 tests pass (99 baseline + 2 new);
  strict lint passes from a copy installed as
  `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Wetland gallery prototype (first item of the v2.6 program; staging only, unreleased draft):
  Everglades treatment wetland + marsh under `examples/gallery/wetland/`
  (SFWMD STA-1W monthly TP 2008–09; USGS EDEN 10 daily level
  2025–26), index row in `examples/gallery.md`, SKILL.md Companion
  Documents names the wetland. Verification in staging: 99 tests pass
  (97 baseline + 2 new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 4 of the v2.5 program (borrowings; staging only, unreleased draft):
  prototype gallery (T40): five working entries under `examples/gallery/`
  (pond, river, field, air, biodiversity) plus the gallery index
  `examples/gallery.md`; SKILL.md Companion Documents names the gallery.
  Verification in staging: 97 tests pass (91 baseline + 6 new);
  strict lint passes from a copy installed as `ecosystem-digital-twin/`;
  BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 3 of the v2.5 program (borrowings; staging only, unreleased draft):
  two tiers — Focus Application and What-if Scenario forms (T38);
  explainability under pressure and multi-source fusion checklist (T39).
  Verification in staging: 91 tests pass (87 baseline + 4 new);
  strict lint passes from a copy installed as `ecosystem-digital-twin/`;
  BEIRA-F-001 untouched, chain verifies.
  recalibration trigger on drift (T36) and continuous revalidation
  (T37). Verification in staging: 87 tests pass (79 baseline + 8 new);
  strict lint passes from a copy installed as `ecosystem-digital-twin/`;
  BEIRA-F-001 untouched, chain verifies.
- 2026-10-26 — Round 1 of the v2.5 program (borrowings; staging only, unreleased draft):
  FAIR Signposting over RO-Crate (T34), scenario taxonomy beside
  Scenario 0 with scenario card (T35), handover note. Verification in
  staging: 79 tests pass (74 baseline + 5 new); strict lint passes from
  a copy installed as `ecosystem-digital-twin/`; BEIRA-F-001 untouched,
  chain verifies.
- 2026-10-26 — v2.4 (applied to the live skill on the author's approval):
  lead-time register + forecast cadence (T32) and the Phase 1
  data-onboarding checklist (T33). Verification (live skill): 74 tests
  pass (67 baseline + 7 new); strict lint passes from a copy installed
  as `ecosystem-digital-twin/`; BEIRA-F-001 untouched, chain verifies.
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
