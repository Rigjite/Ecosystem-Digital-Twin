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

Current version: **1.8** (2026-10-20). License: CC BY 4.0.

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
| `scripts/evidence_search.py` | Literature retrieval across PubMed, Europe PMC, OpenAlex, Crossref; emits normalized JSON |
| `tests/TESTS.md` | Saved behavioral tests (T1–T18) with a run log |
| `CHANGELOG.md` | Version history |

## Development and evaluation

The skill was developed iteratively: each capability layer was added
against the failure modes of the previous version, and the package was
scored in repeated external-judge evaluation rounds (the run log,
including scores and the defects found and fixed, is in
`tests/TESTS.md`). Behavioral tests are executed against live projects;
the run log states plainly which are still pending a first live use.

## Citation

Baldanova, R. (2026). *Ecosystem Digital Twin — Agent Skill* (v1.8).
https://github.com/Rigjite/Ecosystem-Digital-Twin

## License

CC BY 4.0 — see [`LICENSE`](LICENSE). You may reuse and adapt the skill
with attribution.
