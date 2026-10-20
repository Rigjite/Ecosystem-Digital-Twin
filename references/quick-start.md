# Quick start — the one-page path

For a first or small build (Tier S). Work the steps in order; each names the
form to fill (`assets/templates.md`) and the reference that holds the detail.
A filled miniature of the whole path is in `examples/lake-example.md`.

## The ten steps

1. **Name the decision.** What will the owner do differently because this
   twin exists? No decision → the build is monitoring-only; say so.
   *(Form: Object passport.)*
2. **Fill the passport.** Object, boundaries, owner, time horizon, update
   cadence, target maturity level, orchestration tier, stakeholders, ELSA /
   FPIC checklist, data ownership. *(Phase 0.)*
3. **Inventory the data, open first.** Source matrix: satellite, gauges,
   species records, meteo, soils — then client and field data. Add the
   evidence inventory (prior studies) and rescue the history (archives,
   yearbooks, old surveys) before calling anything unmeasured.
   *(references/data-sources.md, evidence-sources.md,
   analytics-forecasting.md §1.)*
4. **Pass the quality gate.** Validate every series; quarantine failures;
   name a fall-back source for every core variable. *(Phase 1.)*
5. **Select indicators.** Start from the domain quick set; add core
   indicators for every medium present; add conditional panels only where
   a pressure or decision triggers them. Unmeasured selections stay listed
   as gaps. *(references/indicators.md §18.)*
6. **Build the simplest model that the data can feed.** Drivers → state →
   impacts; monitoring / forecast / impact layers labeled; index or balance
   model before process complexity. *(Phase 2.)*
7. **Calibrate or label.** Hindcast against held-out history; report the
   metrics against a naive baseline. No usable history → the build is a
   **prototype**, in writing. *(Phase 3.)*
8. **Set the bands, the risks, the preventive plans.** Green/amber/red per
   core indicator with named anchors; risk register for the material
   risks; a trigger–action–response plan for each risk that has an
   actionable lead time. *(Phase 4; forms: Risk register, TARP.)*
9. **Run one improvement round.** Nature-based options first; score with
   weights fixed in advance; present the recommendation as an option card
   with residual risk and a verification indicator. *(Phase 5; form:
   Option card.)*
10. **Deliver the package, not a report.** Passport, state with provenance
    IDs, calibration report, bands and verification scores, scenario
    comparison, gaps, maintenance duties — in the RO-Crate manifest
    format. Pass the red-team delivery gate (Gate C) before it ships.
    *(Phase 6; references/orchestration.md.)*

## What Tier S may skip — and what it may never skip

May skip for now: Bayesian uncertainty computation, multi-agent tiers,
compound stress tests, the counterfactual twin (until a measure is
actually implemented). Record each skip in the passport.

May **never** skip: provenance for every number; the prototype label when
uncalibrated; a named anchor for every threshold; the sensitive-species
location rule; gaps stated as gaps.

## When to escalate

Move to Tier M when the build spans several domains, makes predictive
claims, or feeds a client decision with money or health at stake. Move to
Tier L for regulatory, contested, or public-health builds
(references/orchestration.md).

## File map

- `SKILL.md` — the rules and the phases.
- `references/indicators.md` — what to measure.
- `references/data-sources.md` — where measurements and data come from.
- `references/evidence-sources.md` — where published proof comes from.
- `references/analytics-forecasting.md` — history, patterns, events, risk,
  prevention.
- `references/uncertainty-decision.md` — uncertainty, information value,
  forecast registry, counterfactual.
- `references/orchestration.md` — agents, contracts, red-team gates.
- `references/scenarios.md`, `references/world-practice.md` — scenario
  library; the world-practice survey behind the design.
- `assets/templates.md` — the five fillable forms.
- `examples/lake-example.md` — one small build, filled in end to end.
- `scripts/evidence_search.py` — literature retrieval across PubMed,
  Europe PMC, OpenAlex, Crossref.
