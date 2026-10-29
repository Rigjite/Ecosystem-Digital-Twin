# Templates — the twelve fillable forms

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
- Decision-makers' operational limits (Phase 1): for each decision-maker,
  their operational limit in the same units as the indicator ____
- ELSA checklist: data ownership and consent ____ / sensor placement
  permissions ____ / who may be harmed by a wrong alert ____ / FPIC where
  triggered — rights-holders identified ____, consent or legal basis ____,
  outcome recorded ____ / landowner consent ____ / personal data in feeds
  ____ / conflicts of interest ____
- Data ownership and reuse terms (client data stays the client's): ____
- Data onboarding (Phase 1 checklist), per dataset: source and access date ____ / licence and reuse terms ____ / spatial and temporal resolution and coverage ____ / QC performed (method, result) ____ / file zone (landing / trusted / refined) ____ / semantic mapping (mappings.csv — local field → standard term + justification, per dataset) ____ / gaps → [НЕТ ДАННЫХ] register ____
- Virtual sensors (registered proxy sensors): per virtual sensor — name ____ / physical quantity ____ / proxy source + deterministic formula (the published satellite algorithm) ____ / calibration station ____ / skill score against the station (SS_RMSE) ____ / validity window ____ / QC and alert machinery as a physical sensor ____ / when the proxy leaves calibration, its readings go to the [НЕТ ДАННЫХ] register — never silently used ____
- Fusion checklist (multi-source), per source: coverage ____ / resolution ____ / alignment with the other sources ____ / cross-source consistency checks ____ / gaps → [НЕТ ДАННЫХ] register ____
- Interoperability standards adopted (per data type) and deviations: ____
- Scenario scoring criteria and weights — fixed before results (date): ____
- Calibration plan, declared before fitting: hold-out split ____ / naive
  baselines ____ / failure thresholds ____
- Primary target variables (the management question is decided on these):
  ____ — SS_RMSE > 0 is required for these in the plausibility gate
  (`scripts/skill_scores.py admit`); secondary background variables are
  reported, not gated. When no variable is named here, every variable is
  primary.
- Drift threshold, per indicator: ____ (e.g. 2.0 calibration SDs;
  `scripts/trend_test.py --mode drift`) — a declared parameter, not a
  universal law; the script default 2.0 applies only when the passport
  declares nothing.
- Sensitivity screen (`scripts/sensitivity_screen.py`): parameter ____ /
  perturbation ____ / output change ____ / rank ____ — calibrate only the
  influential parameters; the rest stay at literature values
- Model ladder: fast model (screening only) ____ / full model ____ /
  declared tolerance between them on the same hold-out ____ / hold-out
  check (SS_RMSE of each, date) ____
- Promotion record: status (exploratory | operational) ____ / promoted
  by (name/role) ____ / on (date) ____ / evidence (benchmark + hold-out
  score) ____ / registry entry ID ____ (`scripts/registry.py promote`)
- Valid use / out of scope: valid use (the decisions this twin is built
  for) ____ / out of scope (what the twin must NOT be used for) ____
- Nudge window N (number of last QC-passed observation/model pairs used
  for the bias correction, e.g. 5; `scripts/skill_scores.py nudge`): ____
- Clearance table (asset-relative safety margin): per named asset — asset ____ / threshold (value, unit, anchor) ____ / forecast value ____ / clearance (threshold − forecast value) ____. A positive clearance is the margin the asset has; a negative clearance means the forecast crosses the asset's threshold. Generalizes beyond floods: clearance of a pollutant below its limit, of a level below a spillway crest, of a temperature below a lethal threshold.
- Skipped elements (Tier S) and why: ____
- Multi-model runs: skill version pinned (tag/commit) ____ / execution host
  ____ / router and providers receiving briefs ____ / client consent to this
  data flow ____ / council model IDs ____ / cost cap per run ____
- Handover (who maintains the twin after the author): name/role ____ /
  handover conditions ____
- Dissemination register (who receives which product, by what channel): per
  product — product ____ / audience ____ / channel ____ / who receives it ____

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
- Linked nodes notified: ____ (upstream/downstream twins warned when the trigger fires; the notification is recorded here, not in the forecast registry — a notified node re-checks its own alert bands on the next batch)
- After-action review date and reviewer: ____

## 4. Option card (Phase 5)

- Option name / class (prevent / mitigate / restore / adapt / monitor): ____
- Nature-based? ____ (if an engineered option is recommended over an
  available nature-based one, the justification): ____
- Expected effect on domain indicators — value, evidence (twin run /
  published effect size / analogue), confidence: ____
- Time to visible effect: ____
- Cost and implementation risk: ____
- Impact avoided (from the impact chain, `references/scenarios.md` —
  value, published function, confidence): ____
- Co-benefits: ____
- Equity — who bears the cost ____ / who gains ____
- Follow-up check date ____ / predicted impact registered as forecast
  ID ____ (`scripts/registry.py issue`, scored on the check date)
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
- Refresh cadence: ____ (daily / weekly / seasonal / event-driven)
- Usable warning lead time for the decision: ____ (value + unit, e.g. 3 days)
- Value or probability: ____ / interval ____ / how the interval was
  computed ____ (no method → no interval)
- Trial forecast (level-3 twin, no decision weight)? ____
- Calibrated component it comes from, with its hold-out scores: ____
- Model and version: ____
- Input data (manifest IDs): ____
- Verification metric declared in advance: ____
- Clearance per asset — asset ____ / threshold ____ / forecast value ____ / clearance (threshold − forecast value) ____ (recorded by `scripts/registry.py issue --clearance "asset:threshold,..."`)
- Supersedes (ID, if a correction): ____
- Outcome (recorded after the horizon closes): ____
- Verification score (computed against this entry, exactly as issued): ____
- Skill horizon — the longest lead at which the forecast still beats
  persistence (`scripts/skill_scores.py skill-horizon`), with its unit: ____
- Nudge correction applied (mean residual over the last N QC-passed
  observations, N = ____, correction = ____, recorded here for
  verification): ____
- Phenomenon metrics — event metrics alongside the generic score
  (`references/analytics-forecasting.md` §4: onset-date error, peak
  error, duration error for the phenomenon at hand): ____

Example of the new fields (v2.4; a format example, not a
registered forecast): a seasonal forecast with a usable warning lead time
of `90 days` — the preparation window the decision needs.

## 6. Scenario card (Phase 5)

- Scenario ID: ____
- Class: ____ (0 No-Action counterfactual / Planning / What-if intervention / Storyline)
- Storyline (Storyline class only) — event ____ / drivers changed ____ / held fixed ____ / impact scored ____
- Question it answers: ____
- Driver or intervention tested: ____
- Compared against: Scenario 0, frozen on (date, manifest ID): ____
- Indicators scored: ____
- Alerts — alerts fired (band, start, lead time), alert trial verdict
  (`scripts/skill_scores.py alert-trial`), breaches explained by a named
  driver (`scripts/alert_bands.py --explained-by` — driver and its bands
  stated, never assumed): ____
- Reproduction check — the scenario model run on the historical window
  with the intervention switched off: window (dates) ____ / tolerance
  declared ____ / reproduced state vs observations ____ / result
  (pass / fail) ____. A failed check means the scenario delta is
  reported as "unvalidated, direction only" — never as a number
  (`references/scenarios.md`, hindcast reproduction gate): ____
- Impact chain — driver → exposed asset → impact, with the published
  function, its source, its applicable range, and its limits per link
  (a link with no published function goes to the [НЕТ ДАННЫХ] register): ____
- Exposure — the exposed elements (people, assets, habitats, intakes,
  cages) and the exposed fraction per class (exposed ÷ total in the zone),
  computed by table arithmetic from the hazard extent and the exposure
  inventory: ____
- Sampling priority — the next sampling targets ranked by model spread
  (`scripts/uncertainty_budget.py sampling-priority`): ____
- Expected effect — value, evidence (twin run / published effect size /
  analogue), confidence: ____
- Explanation — what drove the result, in one or two sentences (what the
  model used, what it did not use, confidence): ____
- Uncertainty: ____
- Horizon: ____

## 7. Focus application (for builders)

One application the twin is built to serve — the builder's view of one
job, not the whole twin.

- Application ID: ____
- Purpose — what the twin is built to do, and the decision it serves: ____
- Object and linked nodes: ____
- Inputs — datasets with manifest IDs: ____
- Outputs — indicators, alert bands, registry entries: ____
- Who builds it (builder name/role): ____
- Maturity level targeted: ____
- Update cadence the application needs: ____

## 8. What-if scenario (for decision-makers)

Frames one decision across the scenarios that bear on it — unlike the
scenario card (§6), which records a single scenario.

- Decision ID: ____
- The decision to be made, and by whom: ____
- Options compared — scenario IDs with classes: ____
- Evidence per option — twin run / published effect size / analogue,
  confidence: ____
- Recommendation: ____
- What would change the recommendation: ____
- Sensitivity (driver-perturbation table) — per driver: driver ____ /
  perturbation (+10% / +25% / −10%) ____ / indicator ____ / delta ____ /
  watch level crossed? ____
- Decision-maker and date: ____

## 9. Forecast bulletin (for the client)

One page per forecast — the client-facing rendering of a registry entry,
not the record of truth (the registry entry is). Generated by
`scripts/forecast_bulletin.py` from the registry entry + the latest
observation CSV; it renders them, it changes no numbers.

- Forecast ID and target: ____
- Issued at: ____
- Observed value today (latest observation, date): ____
- Forecast value (and interval, with how the interval was computed): ____
- Watch status (of the latest observation and of the forecast value, against the stated bands): ____
- Date the forecast will be scored (horizon end) and the verification metric: ____
- Trial forecast (no decision weight)? ____
- Generated by: `scripts/forecast_bulletin.py` ____

## 10. Public status line (for the client and the public)

One paragraph in plain language, generated from the runner's summary JSON —
the twin's state as a client or a member of the public would read it. It is
for the client and the public, distinct from the handover note (for a
successor builder, technical) and from RO-Crate (for machines).

- Current state: ____
- Status (green / yellow / red — from the §20 bands; green means no band breached): ____
- Recommendation (what to do, in plain words): ____
- What changed since the last status line: ____
- Maturity label (the skill's 5-level ladder, never above the level earned): ____
- Gaps ([НЕТ ДАННЫХ]): ____

Example — a filled status line in plain words (a format example only:
it shows the shape of the answer, not a real reading — no numbers are
invented here, the air state is given only as the colour the §20 bands
would give). A Delhi resident asks in plain words: "Can I go outside
today? What are we breathing?"

- Current state: the air today is heavily polluted — the twin's air
  indicators sit in the red band, and the pollution has been building
  since yesterday.
- Status: red.
- Recommendation: stay indoors today if you can. If you must go out,
  wear a mask, keep away from busy roads, and come back inside as soon
  as you can. Keep the windows closed. Check again tomorrow morning —
  the twin will say whether the air has cleared.
- What changed since the last status line: the air moved from yellow
  to red overnight as the pollution built up.
- Maturity label: Descriptive.
- Gaps ([НЕТ ДАННЫХ]): no street-level sensor in this neighbourhood —
  the reading comes from the nearest monitoring station.

## 11. Decision product (for the client)

One product per audience: the same twin rendered for one group of users,
in their format, through their channel, on their cadence. A twin that
produces a report nobody reads is useless — each group gets its product
in its channel.

- Product name: ____
- Audience (who it is for): ____
- Thresholds (the levels that trigger this product's message): ____
- Format (map / bulletin / table / message): ____
- Channel (WhatsApp / email / app / public board / TV): ____
- Refresh cadence (daily / weekly / event-driven): ____

## 12. Mismatch register entry (calibration audit)

One entry per failed validation — the lesson, not the score.

- Entry ID: ____
- Object and date: ____
- Prediction (model + version, what was predicted): ____
- Observed extent ____ / modeled extent ____ / extent score (fraction
  of observed positives correctly predicted, `scripts/mismatch.py`) ____
- Misses (observed but not modeled — where): ____
- False alarms (modeled but not observed — where): ____
- Inferred hidden cause ([ГИПОТЕЗА] / [НЕТ ДАННЫХ]): ____
- Measurement that would confirm it: ____
- Follow-up date: ____
