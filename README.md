# Ecosystem Digital Twin — Agent Skill

English | [Русский](README.ru.md)

An [Agent Skill](https://agentskills.io) for designing and operating
**digital twins of ecosystems**: ponds and lakes, river reaches,
agricultural land, air basins, and flora/fauna conservation sites.

A twin built with this skill is a living, evidence-bound model of a real
place. It mirrors the system's current state, warns early when the state
degrades, and tests interventions in the model before anyone touches the
real system. Two uses, in this order: a **consulting product** delivered
for a client (a farm, a water-body manager, a conservation project, a
municipality), and a **research instrument** for the operator's own
science.

Current version: **2.0** (2026-10-21). License: CC BY 4.0.

## What the skill covers

- **Full build cycle (Phases 0–6):** object passport and decision
  framing → open-first data inventory → state model → calibration and
  validation → monitoring, assimilation, and standing verification →
  improvement scenarios → deliverable as a provenance package
  (RO-Crate manifest).
- **A tiered indicator catalogue** (~200 indicators in 19 sections):
  climate drivers, air quality and deposition, the full hydrometric
  panel, water chemistry and nutrient forms, eutrophication,
  contaminants, sediments, groundwater, soil and land, landscape and
  disturbance, flora, microalgae and phytoplankton, sanitary and
  process microbiology, invertebrates, fish and wildlife, ecosystem
  functions, and pressure–response indicators — each with a tier
  (core / conditional / research) and a named threshold anchor.
- **An evidence layer:** published literature routed across PubMed /
  PMC, Europe PMC, OpenAlex, and Crossref (plus regional-language
  sources), under a strict discipline — standards and guidelines first,
  abstracts screen, full text decides, transferability is checked.
- **Analytics and anticipation:** historical data rescue with a bias
  and breaks register, pattern analysis, an event catalogue,
  predictability audits, event-based forecast validation, a risk
  register, and pre-agreed trigger–action–response plans for preventive
  measures.
- **Uncertainty and proof of effect:** computed uncertainty budgets,
  global sensitivity analysis, value-of-information sampling, an
  append-only forecast registry (pre-registration), and a counterfactual
  "no-action" twin that runs in parallel after a measure is implemented,
  so improvement is measured rather than asserted.
- **Governed multi-agent work:** three orchestration tiers, specialist
  roles with distinct expert personas, written task contracts, and an
  independent red team at design, calibration, and delivery gates.

## Non-negotiables

- No fabricated data — every value traces to a source with date, method,
  and resolution; a missing value is a stated gap.
- No uncalibrated build ships as a twin — it is labeled a prototype, in
  writing.
- Precise locations of sensitive species are never published
  (generalized per GBIF sensitive-data practice).
- Nature-based solutions are evaluated before engineered ones in every
  scenario round; the burden of justification sits on the engineered
  option.

## Install

The skill folder must be named `ecosystem-digital-twin` — the `name` in
`SKILL.md` — whatever this repository is called.

- **Claude Code:** `git clone https://github.com/Rigjite/Ecosystem-Digital-Twin ~/.claude/skills/ecosystem-digital-twin`
- **Claude app (claude.ai, desktop, mobile):** zip the folder so that
  `ecosystem-digital-twin/SKILL.md` sits at the top of the archive, and
  upload it as a custom skill in the app's skills settings.
- **Other Agent Skills clients:** copy the folder into the client's skills
  directory.

Check an install from the skill folder: `python3 tests/check_package.py --strict`.

## Quick start

1. Read [`references/quick-start.md`](references/quick-start.md) — the
   one-page, ten-step path for a first or small build.
2. Fill the five forms in [`assets/templates.md`](assets/templates.md)
   as you go: object passport, risk register, trigger–action–response
   plan, option card, forecast registry entry.
3. Keep [`examples/lake-example.md`](examples/lake-example.md) beside
   you — one small lake carried through every form, end to end.

## Package structure

| Path | Contents |
|---|---|
| `SKILL.md` | The skill itself: rules, phases, domain modules, quality gates |
| `references/indicators.md` | The tiered indicator catalogue and threshold anchors |
| `references/data-sources.md` | Open-first data sources and interoperability standards (SensorThings, WaterML 2.0, Darwin Core, EML, STAC, CF) |
| `references/evidence-sources.md` | Literature platform routing, query protocol, evidence hierarchy |
| `references/analytics-forecasting.md` | Historical data rescue, patterns, event catalogue, forecasting, risk register, preventive plans |
| `references/uncertainty-decision.md` | Quantitative uncertainty, value of information, forecast registry, counterfactual twin |
| `references/orchestration.md` | Multi-agent tiers, role contracts, independence rules, red-team gates |
| `references/scenarios.md` | Scenario library for improvement modeling |
| `references/world-practice.md` | Survey of the world practice the design builds on (Destination Earth, BioDT, EU Digital Twin of the Ocean, Delft-FEWS, Wageningen farm twins) |
| `references/quick-start.md` | The one-page execution path and file map |
| `assets/templates.md` | The five fillable forms |
| `examples/lake-example.md` | A worked miniature build (all values illustrative) |
| `scripts/qc_series.py` | Data quality gate: range, rate, stuck, duplicate, gap, neighbor and change-point checks; flags only |
| `scripts/trend_test.py` | Mann–Kendall / Sen slope per segment between registered breaks; seasonal Kendall; autocorrelation handling |
| `scripts/skill_scores.py` | Calibration and verification: declared hold-out, naive baselines, NSE/KGE/RMSE, POD/FAR/CSI, Brier with reliability |
| `scripts/uncertainty_budget.py` | Uncertainty budget by source from ensemble runs; intervals only from a joint ensemble |
| `scripts/alert_bands.py` | Amber/red alert bands with named anchors and sustained-breach windows |
| `scripts/registry.py` | Append-only, hash-chained forecast registry; scores forecasts exactly as issued |
| `scripts/generalize_coords.py` | Sensitive-species coordinate generalization (GBIF categories, 0.1° floor) with a pre-sharing check |
| `scripts/build_manifest.py` | RO-Crate 1.1 provenance package; checks that every headline number is traced and cited |
| `scripts/evidence_search.py` | Literature retrieval across PubMed, Europe PMC, OpenAlex, Crossref; emits normalized JSON |
| `tests/test_scripts.py`, `tests/check_package.py` | Unit tests of the scripts and the package lint (`python3 -m unittest discover -s tests`) |
| `tests/TESTS.md` | Behavioral and automated tests (T1–T27) with a traceability table and run log |
| `CHANGELOG.md` | Version history |

## Development and evaluation

The skill was developed iteratively: each capability layer was added
against the failure modes of the previous version, and the package was
scored in repeated evaluation rounds (the run log, including scores and
the defects found and fixed, is in `tests/TESTS.md`). Since v2.0 the rules
that can be computed are enforced by scripts with unit tests; behavioral
tests are executed against live projects, and the run log states plainly
which are still pending a first live use.

## Citation

Baldanova, R. (2026). *Ecosystem Digital Twin — Agent Skill* (v2.0).
https://github.com/Rigjite/Ecosystem-Digital-Twin

## License

CC BY 4.0 — see [`LICENSE`](LICENSE). You may reuse and adapt the skill
with attribution.
