# Templates — the five fillable forms

Copy a form, replace every `____` with the build's content, delete nothing
silently: a field that does not apply is marked `n/a — reason`, so a reader
can tell a considered omission from a forgotten one.

## 1. Object passport (Phase 0)

- Object name / type: ____
- Boundaries (coordinates, watershed, field, basin): ____
- Owner (client or research owner) and contact role: ____
- Decision the twin must support: ____ (none → monitoring-only, stated)
- Time horizon / update cadence the decision needs: ____
- Target maturity level (1 prototype – 5 decision): ____ / level earned
  today, with the evidence: ____
- Orchestration tier (S / M / L) and reason: ____
- Stakeholders: who decides ____ / who is affected ____ / who owns each
  data stream ____
- ELSA checklist: data ownership and consent ____ / sensor placement
  permissions ____ / who may be harmed by a wrong alert ____ / FPIC where
  triggered — rights-holders identified ____, consent or legal basis ____,
  outcome recorded ____ / landowner consent ____ / personal data in feeds
  ____ / conflicts of interest ____
- Data ownership and reuse terms (client data stays the client's): ____
- Interoperability standards adopted (per data type) and deviations: ____
- Scenario scoring criteria and weights — fixed before results (date): ____
- Calibration plan, declared before fitting: hold-out split ____ / naive
  baselines ____ / failure thresholds ____
- Skipped elements (Tier S) and why: ____
- Multi-model runs: skill version pinned (tag/commit) ____ / execution host
  ____ / router and providers receiving briefs ____ / client consent to this
  data flow ____ / council model IDs ____ / cost cap per run ____

## 2. Risk register row (Phase 4)

- Risk ID: ____
- Hazard (event or slow pressure): ____
- Pathway to the ecosystem: ____
- Exposed element (species, habitat, water use, soil function, health): ____
- Likelihood — with the evidence named: ____
- Impact on domain indicators: ____
- Vulnerability (why this object, this state): ____
- Detectability — warning indicator and lead time: ____
- Confidence in this row as a whole: ____
- Owner (watches / can act): ____
- Linked TARP ID (if actionable): ____
- Review date: ____

## 3. Trigger–action–response plan, TARP (Phase 4)

- TARP ID / linked risk ID: ____
- Trigger: indicator ____ / threshold ____ / sustained window ____ /
  alert band (amber / red) ____
- Watch action (prepare level): ____
- Preventive action (act level): ____
- Owner and executor: ____
- Lead time the action needs vs forecast lead time available: ____ / ____
- Cost and side effects (incl. ecological): ____
- Stand-down criteria: ____
- After-action review date and reviewer: ____

## 4. Option card (Phase 5)

- Option name / class (prevent / mitigate / restore / adapt / monitor): ____
- Nature-based? ____ (if an engineered option is recommended over an
  available nature-based one, the justification): ____
- Expected effect on domain indicators — value, evidence (twin run /
  published effect size / analogue), confidence: ____
- Time to visible effect: ____
- Cost and implementation risk: ____
- Reversibility: ____
- Residual risk after the option: ____
- Verification indicator and review date: ____
- On implementation: counterfactual baseline frozen on (date, manifest
  ID): ____

## 5. Forecast registry entry (Phases 3–4)

Register with `scripts/registry.py issue`; this form is the human-readable
copy, not the record of truth.

- Forecast ID: ____
- Issued at (registration clock, before the outcome is knowable): ____
- Quantity or event forecast (what, where, unit): ____
- Horizon end: ____
- Value or probability: ____ / interval ____ / how the interval was
  computed ____ (no method → no interval)
- Trial forecast (level-3 twin, no decision weight)? ____
- Calibrated component it comes from, with its hold-out scores: ____
- Model and version: ____
- Input data (manifest IDs): ____
- Verification metric declared in advance: ____
- Supersedes (ID, if a correction): ____
- Outcome (recorded after the horizon closes): ____
- Verification score (computed against this entry, exactly as issued): ____
