# Analytics, forecasting, risk, and preventive action

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
- **Trends** — direction and rate with autocorrelation-aware significance
  (e.g. Mann–Kendall / Sen slope as a starting point); a trend across a
  registered method break is reported as two segments, not one line.
- **Anomalies and extremes** — exceedance counts, return periods for high
  and low extremes (flood, drought, heat), and how they are changing.
- **Change points and regime shifts** — step changes in mean or variance;
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
distribution, and — for probabilistic forecasts — Brier score and a
reliability statement. A forecast without hindcast event scores is a
prototype output and is labeled as such wherever it appears.

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
