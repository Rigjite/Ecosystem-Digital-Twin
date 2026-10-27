# Analytics, forecasting, risk, and preventive action

## Contents
1. Historical data: rescue before conclusions
2. Pattern analysis (`scripts/trend_test.py`)
3. The event catalogue
4. Forecasting events (`scripts/skill_scores.py events | brier`)
5. Risk analytics
6. Preventive measures — trigger–action–response plans
7. Decision options for improving the existing ecosystem
8. Recalibration trigger and continuous revalidation

This layer turns the twin from a description of the present into a tested
instrument for what happens next. Its discipline is strict: a pattern is a
hypothesis until it survives out-of-sample testing; a forecast is a
probability with a verified track record, never a prophecy; and where no
historical data exist, the twin says so and limits itself to monitoring,
analogue evidence, and scenario ranges — it does not invent a past.

## 1. Historical data: rescue before conclusions

Before declaring any variable "unmeasured", search for its history:

- **Long monitoring series** — agency and institute archives, printed
  yearbooks and station logs (many water and weather series run decades
  longer than their digital versions), prior project reports and EIAs.
- **Remote-sensing archives** — Landsat back to 1984 (earlier missions for
  some areas), historical aerial photography, declassified imagery where
  relevant: land cover, water extent, shoreline, fire scars, vegetation.
- **Biological archives** — museum and herbarium collections, historical
  GBIF records, fisheries and hunting statistics, old survey reports with
  re-locatable sampling points.
- **Proxy records** — sediment cores (diatoms, pigments, pollen,
  contaminants), tree rings, ice records: for baselines beyond instrumental
  history, labeled as proxies with dating uncertainty.
- **Documented local and Indigenous knowledge** — flood marks, fish-kill
  memories, phenology calendars: collected with consent, recorded as
  testimony with date and source, never silently converted into instrument
  data.

**Harmonization is part of the rescue.** Historical series arrive with
method changes, moved stations, changed detection limits, revised taxonomy,
and changed sampling seasons. Record every break in a **bias and breaks
register** (date, what changed, how it was handled); a trend computed across
an unrecorded method change is a fabrication risk, and the red team treats
it as one (Gate B).

## 2. Pattern analysis

Run on the harmonized history, before model fitting (Phase 2–3 inputs):

- **Climatology and seasonality** — the object's normal year: means,
  percentiles, timing. Every anomaly claim is relative to this baseline.
- **Trends** — direction and rate with autocorrelation-aware significance:
  `scripts/trend_test.py` runs Mann–Kendall with Sen's slope per segment
  between registered breaks, with the Hamed–Rao (1998) variance correction
  for autocorrelation (trend-free pre-whitening is available for
  comparison but can overstate significance in strongly autocorrelated
  series), or the seasonal Kendall test for monthly water-quality data. A
  Pettitt change point is a flag, not a verdict: it also fires on a smooth
  monotonic trend, so its cause is established before the series is split. A trend across a registered
  method break is reported as separate segments, never as one line.
- **Anomalies and extremes** — exceedance counts, return periods for high
  and low extremes (flood, drought, heat), and how they are changing.
- **Change points and regime shifts** — step changes in mean or variance
  (`scripts/qc_series.py` reports a Pettitt change point for every series);
  candidate drivers recorded next to each break (land use, regulation,
  climate, method change) with the evidence for each.
- **Lead–lag structure** — cross-correlations between drivers and state
  (rainfall → turbidity, heat → oxygen, nutrient load → chlorophyll):
  these nominate early-warning indicators. Correlation nominates; only a
  mechanism plus out-of-sample skill confirms.
- **Spatial patterns** — hotspots of degradation or resilience, source–
  receptor geometry, spread fronts of invasives or pollution plumes.
- **Phenology shifts** — green-up, bloom timing, ice dates, migration and
  spawning timing against the historical baseline.
- **Early-warning signals of regime shift** (rising variance and lag-1
  autocorrelation, slowing recovery after disturbances) — treated as
  hypotheses with a known false-positive rate, useful for raising watch
  levels, never as standalone proof of an approaching tipping point.

Output: a **pattern memo** per object — patterns found, the data behind
each, confidence, and what each pattern would let the twin anticipate.

## 3. The event catalogue

Patterns become prediction through events. Build a catalogue of the adverse
(or valuable) events the owner cares about. One row per event occurrence in
the history:

| Field | Content |
|---|---|
| Event | Named type: hypoxia/fish kill, cyanobacteria bloom, flood, low-flow crisis, pollution episode, invasive first record, pest outbreak, fire/smoke episode, erosion pulse |
| Date and duration | From observations, testimony labeled as such |
| Magnitude | Peak value / extent / class |
| Antecedent conditions | The 3–30 days before: weather, flows, loads, stratification, land state |
| Impact | Ecological, health, economic — as recorded |
| Response taken and its effect | What was done, what it changed |
| Data quality | Instrumented / reported / reconstructed |

An event with fewer than ~5 historical occurrences can be monitored and
scenario-tested but rarely statistically forecast; the catalogue states
the count, and the forecast claims obey it.

## 4. Forecasting events

**Predictability audit first** (per event type): is there a forcing the
twin can observe or obtain (weather forecast, upstream gauge, seasonal
climate outlook)? Is the achievable lead time longer than the time the
preventive action needs? If either answer is no, the product is a watch
and a response plan, not a forecast — label it that way.

**Forecast products by horizon:** nowcast (current state estimate, hours);
short-range (days — weather-driven events); sub-seasonal (weeks —
bloom and low-flow development); seasonal (months — drought, fire danger,
water availability); long-range (years — scenario ranges under climate and
land-use pathways, never single-value predictions).

**Method ladder** (climb only as data allows): climatology and persistence
→ statistical models on the pattern memo's lead indicators → process
models with forecast forcing → hybrid/ML components checked against the
simpler rungs. A complex method that cannot beat climatology on hindcast
events is removed, whatever its continuous-metric scores say.

**Event-based validation is mandatory.** In addition to Phase 3 continuous
metrics, every event forecast reports from hindcasts: probability of
detection, false-alarm ratio, critical success index, lead-time
distribution (`scripts/skill_scores.py events`), and — for probabilistic
forecasts — Brier score, Brier skill score against a climatological
probability from the training period, and a reliability table
(`scripts/skill_scores.py brier`). A forecast without hindcast event scores is a
prototype output and is labeled as such wherever it appears.

**Skill horizon — publish the horizon where the forecast dies.** A
forecast that beats persistence at 1 day and loses to it at 3 days is
useful for 1 day and worse than doing nothing at 3 days. Score the
forecast per lead (`scripts/skill_scores.py skill-horizon` — one row per
scored pair: lead, observed, simulated, naive baseline value) and state
the **skill horizon** in the twin's report and on the forecast card
(`assets/templates.md` §5): the longest lead at which the forecast still
beats persistence (SS_RMSE > 0) with every shorter lead also above zero.
A forecast is not trusted beyond its horizon; a longer lead that beats
the baseline after an earlier failure is a non-monotone recovery — noise,
not skill — and the horizon stops at the first failure. (Source: lake
platforms — Meteolakes/COASTLINES report error as a function of forecast
horizon; bias grows with horizon.) A nudged forecast (below) is scored
per lead time by the same curve, like any forecast — its horizon is
reported alongside the correction.

**Observation-nudged forecast.** The cheapest accuracy gain in the
whole borrowing list: correct the forecast with the last residuals.
`scripts/skill_scores.py nudge` shifts a raw forecast value by the mean
model-minus-observed residual over the last N QC-passed
observation/model pairs (N declared in the Object Passport, e.g. 5):
nudged = raw forecast − mean(sim − obs). The correction is recorded in
the registry entry (`assets/templates.md` §5), so it can be checked, and
the nudged forecast is scored per lead time by `skill-horizon` like any
forecast — its horizon is reported alongside the correction, and a nudge
that does not improve the horizon is dropped. This is the transferable
principle of the Meteolakes ensemble Kalman filter (which assimilates
satellite lake-surface temperature and halved the mean prediction error),
not the filter itself: a deterministic bias correction, fully
reproducible, using data the twin already holds. (Source: lake
platforms — Baracchini et al. 2020, Water Res. 172, 115529.)

**Phenomenon-oriented metrics.** A generic score can hide a model that
gets the mean right and misses every event — and events are what the
client pays to foresee. Alongside the generic score, the verification
record reports 2–3 event metrics per phenomenon, computed from the
existing runner outputs by plain arithmetic (onset and peak from the
event catalogue, §3; magnitudes from the indicator series):

| Phenomenon | Event metrics (alongside the generic score) |
|---|---|
| Bloom (cyanobacteria / chlorophyll) | onset-date error (days, forecast − observed); peak-magnitude error (forecast − observed peak, in the indicator's units); duration error (days) |
| Flood | peak-level error (m, forecast − observed); timing error (hours/days, forecast − observed peak time); extent error (fraction of observed flooded cells correctly predicted) |
| Fire season | season-start error (days); peak-burned-area error (ha); season-duration error (days) |
| Drought / low flow | onset-date error (days); minimum-level/flow error; duration error (days) |
| Heat / air stagnation | exceedance-days error (days above the watch level); peak-concentration error |

The admission rule stays SS_RMSE — the phenomenon metrics do not
admit or reject a model; they show the client the model's skill on the
events that matter, next to the generic score, on the forecast card
(`assets/templates.md` §5, "Phenomenon metrics"). A metric that cannot
be computed yet (too few events in the catalogue — §3 states the ~5
minimum) is reported as [НЕТ ДАННЫХ] with the count, never as zero.
(Source: EDITO — Focus-application validation requires "phenomenon
oriented metrics" alongside uncertainty quantification; Drévillon,
Digital Ocean Forum 2025; Capet et al. 2020.)

## 5. Risk analytics

Maintain a **risk register** for the object, reviewed at every Phase 4
verification cycle:

| Field | Content |
|---|---|
| Hazard | The event or slow pressure (from the event catalogue and emerging-risk scan) |
| Pathway | How it reaches the ecosystem component |
| Exposed element | Species, habitat, water use, soil function, health |
| Likelihood | From historical frequency and current forecast — with the evidence named |
| Impact | Severity if it occurs, on the domain indicators |
| Vulnerability | Why this object is more or less susceptible (state, buffers, connectivity) |
| Detectability | Lead time and the indicator that would warn |
| Confidence | Data and model basis for the row as a whole |
| Owner | Who watches this risk and who can act |

Rules: likelihood and impact are argued from evidence per cell, not
multiplied into a single score that hides the reasoning; slow pressures
(eutrophication, salinization, fragmentation, groundwater decline) sit in
the same register as acute events; an **emerging-risk scan** (climate
trend, land-use change, new species pathways, new sources) runs at least
annually and can add rows before any event has occurred.

## 6. Preventive measures — trigger–action–response plans

Every material risk with an actionable lead time gets a **TARP** (trigger–
action–response plan), agreed with the owner before the season, not
improvised during the event:

- **Trigger** — indicator, threshold, and sustained window (from Phase 4
  bands and the event catalogue's antecedent conditions).
- **Preventive action** — the pre-agreed measure, sized to the trigger
  level (watch / prepare / act).
- **Owner and lead time** — who executes, and confirmation that the
  forecast lead time exceeds the action's required lead time.
- **Cost and side effects** — including ecological side effects of the
  measure itself.
- **Stand-down criteria** — when the action is reversed or closed.
- **After-action review** — did the event occur, did the measure change
  the outcome, what updates the catalogue and the register.

Examples by domain (adapted per object, never copied as a checklist):
pre-emptive aeration or mixing ahead of a forecast hypoxia window; bathing
advisories and livestock warnings ahead of a bloom; flow releases or
abstraction limits ahead of a low-flow crisis; fuel and fire-danger
measures ahead of fire weather; storm-season buffer and drain maintenance
ahead of erosion pulses; rapid removal at an invasive species' first
confirmed record; irrigation rescheduling ahead of drought; emission
curtailment during forecast air-stagnation episodes; grazing or visitor
restrictions ahead of sensitive breeding windows.

## 7. Decision options for improving the existing ecosystem

Scenario work (Phase 5) draws its option portfolio from the risk register
and the pattern memo, structured as **prevent → mitigate → restore →
adapt → monitor**, with no-regret and low-regret options surfaced first
(measures that pay off across scenarios). Every option is an **option
card**:

- expected effect on the domain indicators, with its evidence (twin run,
  published effect size, or analogue) and confidence;
- time to visible effect; cost and implementation risk; reversibility;
- residual risk after the option (what can still go wrong);
- the monitoring indicator and review date that will prove or disprove the
  expected effect — an option without a verification indicator is a hope,
  not a plan;
- interaction with other options (synergies, conflicts, sequencing).

After implementation, outcomes are reviewed against the card at the stated
date; the review updates the event catalogue, the risk register, and the
option library. This closes the loop: analysis → forecast → prevention →
action → measured outcome → better analysis.

## 8. Recalibration trigger and continuous revalidation

A twin that is never re-checked goes stale silently. On every new batch
of observations the twin runs two deterministic checks, in this order.

**What counts as new data.** A batch of observations for an indicator
the twin already models, passed through `scripts/qc_series.py` (gate
pass). Flagged rows are excluded from both checks below; a batch that
fails the QC gate is quarantined, never fed to the trigger.

**The recalibration trigger** (`scripts/trend_test.py --mode drift
--baseline <calibration series>`). Two drift components; either fires
the trigger:
- Level drift: |mean(new batch) − mean(calibration)| / sd(calibration).
  Fires at or above the drift threshold, declared per indicator in the
  Object Passport (default 2.0 calibration SDs) — a declared parameter,
  not a universal law.
- Trend drift: the new batch's Sen slope outside the calibration
  slope's Gilbert confidence interval (needs at least 8 new values;
  otherwise the trend component is not assessed and the level
  component decides).
When the trigger fires: recalibrate (Stage 3 re-run on calibration +
new data), recompute alert bands (`scripts/alert_bands.py`), update all
linked nodes, and revalidate the recalibrated model before it can keep
ADMITTED status. A fired trigger is a normal event, not a failure: the
drift check exits 0 and reports `trigger` and `action`.

**Continuous revalidation** (`scripts/skill_scores.py revalidate`). On
each new batch, the admitted model is re-scored on the new hold-out
against the naive benchmark, with the original `--train-end` split
(baselines built from training data only — the new batch never trains
its own baseline). SS_RMSE ≤ 0 revokes ADMITTED: the model loses its
forecasting status, the twin's maturity label drops to the highest
level the twin still meets, and the drop is recorded in the Object
Passport. A better model is admitted only by passing revalidation
itself. Forecasts already issued are not re-scored or re-anchored
(T17): they stay scored as issued.

**Recording.** A recalibration is recorded in the build index as a new
model version with its new hold-out and SS_RMSE, and in the passport
(maturity label, drift threshold, batch date). The forecast registry is
untouched.
