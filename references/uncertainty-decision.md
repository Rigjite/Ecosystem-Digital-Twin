# Uncertainty, information value, forecast registry, and the counterfactual twin

Four methods that turn the twin's honesty from wording into arithmetic and
institutions. They are used at decision and predictive maturity levels;
simpler builds state why they are not yet applied.

## 1. Quantitative uncertainty

Every headline output carries a **computed** uncertainty, not an adjective.

**Sources, always separated in the report:** measurement error; input and
forcing error (weather, loads, boundary conditions); parameter uncertainty;
structural (model-choice) uncertainty; scenario uncertainty (the future
itself). A single blended "±" that hides which source dominates is a defect.

**Method ladder** (climb as stakes and compute allow):

1. **Error propagation / Monte Carlo ensembles** — vary inputs and
   parameters within their documented distributions; report prediction
   intervals and exceedance probabilities, not just means.
2. **Bayesian calibration** where data support it — priors documented from
   the evidence layer (`references/evidence-sources.md`), posterior ranges
   reported; a prior without a named source is an opinion, labeled as such.
3. **Global sensitivity analysis** — screening (Morris) then variance-based
   indices (Sobol or equivalent) on the headline outputs: which inputs and
   parameters actually drive the result. This ranking is the input to
   value-of-information analysis (section 2).
4. **Structural comparison** — at least two model structures or a hybrid
   pair for decision-level claims; where structures disagree, the
   disagreement is reported as part of the uncertainty.

**Uncertainty budget.** Each headline output ships with a small budget
table: source → contribution to total variance (or a ranked qualitative
share where computation is not yet possible, labeled as such). The budget
tells the client what would have to improve for the answer to sharpen —
and what cannot improve because the uncertainty is in the future itself.

Rule: a number whose uncertainty cannot be computed yet is published with
the reason and the plan to compute it — never with a decorative interval
invented for appearance.

## 2. Value of information and adaptive sampling

Monitoring budgets are finite; the twin spends them where they matter.

- **Uncertainty map.** Maintain a map/register of where and when decision-
  relevant uncertainty is highest (places, seasons, variables) — from the
  sensitivity ranking and the uncertainty budgets.
- **Next-measurement recommendation.** At every verification cycle, rank
  candidate measurements (new sensor, extra sampling dates, one-off survey)
  by expected reduction in decision uncertainty per unit cost. State the
  decision each candidate serves; a measurement that serves no decision is
  not recommended, however interesting scientifically.
- **Sensor placement** follows the same logic: gradient coverage (inflow →
  center → outflow; upwind → source → downwind), event capture (the place
  where the event shows first), redundancy for the fall-back hierarchy,
  and access/maintenance reality.
- **Adaptive intensification.** When a forecast's uncertainty crosses the
  threshold where a pending decision flips, sampling intensifies for that
  window (event-based sampling), then returns to baseline cadence.
- **Stopping rule.** When the expected value of the next measurement falls
  below its cost, say so and stop expanding the network. The twin that
  always wants more sensors is a budget risk, not a quality signal.
- **Realized value is checked.** Each recommendation records the expected
  uncertainty reduction; the next cycle compares what was realized. A
  value-of-information practice that never audits itself becomes guesswork.

## 3. Forecast registry and pre-registration

Predictive claims are earned in public, in advance.

- **Every forecast is registered before its outcome is knowable:** forecast
  ID; issue timestamp; quantity or event; horizon; value or probability
  with its interval; model and version; input data by manifest ID; the
  verification metric declared for it. The registry is **append-only** —
  entries are never edited after issue; corrections are new entries that
  reference the old.
- **Verification is computed against the registry**, exactly as issued —
  never reconstructed from memory or from a later model version. This is
  what makes the standing verification scores in Phase 4 evidence rather
  than narrative.
- **Metadata follows the ecological-forecasting community convention**
  (Ecological Forecasting Initiative practice): forecast, model, and
  uncertainty described in a standard, machine-readable form so scores are
  comparable across builds and across time.
- A forecast found to have been issued but not registered is treated as
  not issued: it earns no verification credit and supports no claim.

## 4. The counterfactual twin — proving improvement

When the owner implements a measure, the twin splits:

- **Freeze the no-action baseline.** At the implementation decision, the
  baseline twin's configuration, parameters, and management inputs are
  frozen and archived with manifest IDs. This frozen twin is the
  counterfactual: what the model says would have happened without the
  measure.
- **Run both twins on the same observed forcings.** Weather, inflows, and
  other external drivers are identical; only the management inputs differ.
  The difference between the action twin and the counterfactual — reported
  with its uncertainty (section 1) — is the twin's estimate of the
  measure's effect and of damage avoided.
- **No silent re-anchoring.** If the model is later improved, both twins
  are re-run and the change in the estimated effect is logged and
  disclosed. Retroactively improving a claimed effect by quietly updating
  only the baseline is fabrication, and the red team treats it as such
  (Gate C).
- **Field evidence outranks the counterfactual.** Where BACI-type field
  data (before–after/control–impact) or direct measurements of the effect
  exist, they decide; the counterfactual is the estimate used where and
  until such data arrive, labeled as model-based.
- **Avoided-damage reporting.** Each review cycle reports: observed state,
  counterfactual state, estimated effect with interval, and the option
  card's predicted effect (Phase 5) next to both — so the owner sees what
  was promised, what the model attributes, and what was measured, as three
  distinct numbers.

This mode is what turns a twin from a monitoring expense into proof of
impact — for the owner's own decisions first, and for funders and
regulators when they ask what the money bought.
