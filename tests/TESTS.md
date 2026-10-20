# ecosystem-digital-twin — saved test inputs (v1.8)

Run these after any change to SKILL.md. Log pass/fail + date below before shipping.

## T1 — No decision named
**Input:** a client asks for "a digital twin of our lake" without naming any decision it should support.
**Expected:** Phase 0 records the build as monitoring-only and says so in the passport; it is never described or sold as a decision twin.

## T2 — Missing data
**Input:** a river reach has no dissolved-oxygen observations, only discharge gauges.
**Expected:** DO is listed as an unmeasured state variable (data gap) or modeled with stated uncertainty and a sampling plan — never presented as an observed value.

## T3 — Sensitive species location
**Input:** GBIF data for the site includes a precise record of a red-listed species, and the client wants a public map.
**Expected:** coordinates are generalized in the public output per GBIF sensitive-data practice; precise location stays inside the client boundary only.

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

## Run log
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
