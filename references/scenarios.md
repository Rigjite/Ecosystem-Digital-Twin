# Scenario library — modeling for improvement

Every scenario runs against the calibrated baseline twin and is scored on:
ecosystem outcomes (the domain indicators), cost, implementation risk, time
to visible effect, the exposed fraction per class (exposed ÷ total in
the zone), co-benefits, and equity (who bears the cost, who gains).
Expected directions below are hypotheses to test in the model,
not promised results — the twin's numbers decide.

## Contents
- Scenario taxonomy
- Impact chains
- Exposure inventory and exposed fraction
- Adaptation appraisal and follow-up
- Stochastic scenario generation
- Hindcast reproduction gate
- Driver-perturbation table
- Agriculture
- Pond / lake
- River reach
- Air basin
- Conservation

## Scenario taxonomy — four classes

Every scenario declares one class before it is scored; a scenario without
a declared class is not scored. All classes are judged against Scenario 0.

- **Scenario 0 — No-Action counterfactual.** The frozen baseline twin:
  what the model says would have happened without the measure. Never
  redefined, never replaced by another class (protocol:
  `references/uncertainty-decision.md` §4).
- **Planning scenarios.** External drivers the owner must plan around
  but does not control as interventions: land use, development,
  catchment change, policy and demand shifts. They set the world the
  interventions operate in; they are not measures and never substitute
  for the counterfactual.
- **What-if intervention scenarios.** The measures themselves — prevent,
  mitigate, restore, adapt, monitor — single or combined, over short-
  and long-term horizons. The domain families below all belong here.
- **Storyline scenarios.** A named historical extreme event from the
  object's own record, replayed under changed drivers and scored on
  impacts rather than probabilities. Construction rule: pick the named
  event; state the drivers changed and what is held fixed; state the
  impact scored. A storyline may combine two drivers at once (drought +
  heat) — that is how compound events enter the skill. A storyline is a
  scenario, not a model: it is co-defined with the client, and it runs
  through the existing scenario machinery (`scripts/trend_test.py`,
  `scripts/alert_bands.py`) on the replayed series.
- **Boundary — storyline vs replay.** A storyline replays an event under
  CHANGED drivers (a scenario: what if it happened again, hotter or
  drier?); the replay protocol (`references/uncertainty-decision.md`
  §5) runs the pipeline on the event AS IT HAPPENED (a verification:
  would the twin have warned in time?). The two are recorded separately
  and never substitute for each other: a storyline never claims the
  alert fired, and a replay never claims a changed-driver outcome.

## Impact chains

A scenario's indicators are not its consequences. For each scenario, build
an impact chain — hazard → exposure → vulnerability → impact — that
translates indicator values into consequences the decision-maker pays for
(lost catch, lost yield, closed beaches, dead fish, days of advisory):

- **Hazard** — the indicator value or driver state the scenario produces
  (e.g. total phosphorus 120 µg/L, PM2.5 24-hour mean 40 µg/m³, water
  level 2.4 m).
- **Exposure** — who or what is in the hazard's path (cages, intakes,
  beaches, people, habitats), named per scenario.
- **Vulnerability** — why this exposed element is harmed at this hazard
  level (species sensitivity, intake depth, beach use in season).
- **Impact** — the consequence, computed by a published impact function
  (dose–response) with its source, applicable range, and limits stated
  (e.g. TP → fish-kill probability; drought → yield loss; PM2.5 →
  advisory days).

Each link carries the published function, its source, its applicable range,
and its limits — on the scenario card (`assets/templates.md` §6). A link
with no published function goes to the [НЕТ ДАННЫХ] register and is never
invented; a chain with a missing link reports the impact as unquantified,
not as zero. The chain is arithmetic on the existing scripts' outputs
(`scripts/trend_test.py`, `scripts/alert_bands.py`) — no new code. Its
payoff: impact-based watch levels become possible — alert when the
predicted *impact* crosses a threshold, not just the indicator. (Source:
DestinE Extremes and Climate digital twins — impact-sector models
translating data into tailored climate-impact indicators.)

## Exposure inventory and exposed fraction

The impact chain's Exposure link names who or what is in the hazard's path;
the exposed fraction quantifies it per class. For each scenario, list the
exposed elements (people, assets, habitats, intakes, cages) and, per class,
the exposed fraction — exposed ÷ total in the zone — computed by table
arithmetic from the hazard extent and the exposure inventory. A fraction of
0.8 of the cages means four of five cages sit inside the hazard extent; a
fraction with no inventory behind it is not a number, it is a guess, and
goes to the [НЕТ ДАННЫХ] register. The exposed fraction is part of the
scenario score (see the top of this document): a scenario that leaves a
large fraction exposed scores worse on ecosystem outcomes than one that
does not, whatever its cost. (Source: EDITO — Coastal Risk Projections
report risk as hazard × exposure × vulnerability, with an exposure
inventory (people, assets) and a Flooded Fraction — the flooded portion of
an asset class divided by its total susceptible extent.)

## Adaptation appraisal and follow-up

Scoring a scenario is not the end of the appraisal: an adaptation option
is appraised on one table — cost, impact avoided, co-benefits, and
equity (who bears the cost, who gains). An option that is cheap for the
owner and costly for the neighbours scores worse on equity than one whose
costs and gains fall on the same people; the equity column is what
public-sector and donor-funded clients ask for first. The impact avoided
comes from the option's impact chain (above): the chain's published
function turns the indicator change into the consequence (lost catch,
lost yield, closed beaches); without a chain the impact avoided is
[НЕТ ДАННЫХ], not a number.

After an option is implemented, the twin re-scores it against the
predicted impact on a fixed date — a "did the measure work?" check. The
predicted impact and the check date are registered in the forecast
registry (`scripts/registry.py issue`: the predicted impact as the
forecast value, the check date as the horizon end, metric `abs_error`
for a quantity or `brier` for a probability), and scored when the date
arrives (`scripts/registry.py score`) — the same Brier-style discipline
as BEIRA-F-001. The follow-up date and the registry forecast ID are
recorded on the option card (`assets/templates.md` §4). A predicted
impact that is never registered earns no verification credit, like any
unregistered forecast. (Source: DestinE generic adaptation modelling
framework — appraising adaptation options and identifying cost-effective
measures that deliver just and equitable climate solutions, from impact
assessment to monitoring and evaluation.)

## Stochastic scenario generation

A single deterministic scenario cannot answer "how bad could it get?".
`scripts/scenario_generate.py` fits an AR(1) process to a driver series
from the object's own data (mean, sample SD, lag-1 autocorrelation) and
generates N seeded scenario series of the same length — e.g. 100 weather
years. The seed is fixed and recorded in the output, so a run is
reproducible from its summary alone. Every generated value is labelled a
scenario draw, never a measurement: the output CSV and the JSON summary
both say so, and a generated series must never be cited as observed data.

The scenarios feed the existing pipeline — one generated column at a time
into `scripts/trend_test.py` / `scripts/alert_bands.py` — so a What-if
scenario reports a distribution instead of a single path (e.g. "in 78 of
100 seeded years the watch turns red"). With `--watch`, the summary
reports how many of the N series breach the band at least once; that is a
breach count, not a sustained alert — sustained alerts come from feeding a
generated column to `alert_bands.py`. The fitted distribution comes from
the input series itself; no external parameters are smuggled in. (Source:
Digital Baikal — the stochastic "weather generators" of Kargapolova,
Laboratory of Stochastic Problems, ICMMG.)

## Hindcast reproduction gate

Before a scenario's intervention delta is trusted, the scenario model
must first reproduce the observed historical period with the intervention
switched off — "does the app reproduce the current situation (historical
period)?" (EDITO validation question, Drévillon, Digital Ocean Forum
2025; from Capet et al. 2020). The skill scores scenarios against
Scenario 0, but nothing so far requires the scenario model itself to
reproduce history — a model can give a plausible delta without being
able to reproduce the present.

- **Run the scenario model on the historical window with the intervention
  switched off.** The window is the observed historical period the
  scenario claims to start from; the model runs on the same drivers and
  inputs as the scenario, minus the intervention.
- **Require the reproduced state to match the observations within a
  declared tolerance** — the indicator's alert-band width or the
  calibration SD, declared on the scenario card before the run. The
  tolerance is a declared parameter, not a universal law; a tolerance
  chosen after seeing the mismatch is post-hoc and fails the gate.
- **If the check fails, the scenario delta is reported as "unvalidated,
  direction only" — never as a number.** The direction (up/down) may
  still be reported, with the failed check stated next to it; the
  magnitude is not a finding, it is a guess.
- **Record the check on the scenario card** (`assets/templates.md` §6,
  "Reproduction check"): window, tolerance, reproduced state vs
  observations, pass/fail.

**Boundary — hindcast gate vs replay.** The hindcast gate checks the
scenario MODEL before its delta is trusted (does this model reproduce
the historical period it claims to start from?); the replay protocol
(`references/uncertainty-decision.md` §5) checks whether the TWIN
would have warned in time about a historical extreme (a verification of
the alert pipeline on the event as it happened). The two answer
different questions and are recorded separately: a passed gate never
claims the alert fired, and a successful replay never validates a
scenario delta. (Source: EDITO — the Focus-application validation
question "does the app reproduce the current situation (historical
period)?".)

## Driver-perturbation table

A what-if scenario becomes a table a client can act on when each driver
is perturbed one at a time and the indicator delta is reported. For each
driver (rainfall, nutrient load, abstraction, land use), apply stated
perturbations (+10%, +25%, −10%) and report the indicator change using
the existing index functions (WPI/TSI/HPI, `scripts/trend_test.py`) —
plain arithmetic, no new math. Each row records the driver, the
perturbation, the indicator delta, and whether the watch level is
crossed. The perturbations are stated before the run; a perturbation
chosen after seeing the result is post-hoc.

**Boundary — driver table vs sensitivity screen.** The
driver-perturbation table perturbs INPUT drivers (which external driver
moves the indicator — a decision question: what if the farm expands,
what if abstraction rises?); the sensitivity screen
(`scripts/sensitivity_screen.py`, SKILL.md Stage 3) perturbs MODEL
parameters (which calibration knob matters for the fit). Different
questions, different tables, never merged: a driver that moves the
indicator is not a parameter to calibrate, and a parameter that matters
for the fit is not a driver to plan around. (Source: Southern Water —
what-if analyses simulate one driver at a time (rainfall, pollution
event, infrastructure failure) and planning changes (land-use change,
new development) to see the indicator response.)

## Agriculture

- **Nutrient regime change** (rate, timing, placement): expect lower N/P
  surplus and leakage; watch yield and soil carbon side effects.
- **Cover crops and rotation change**: expect soil carbon and moisture gains,
  erosion reduction; effect horizon 2–5 years.
- **Buffer strips along watercourses**: expect nutrient and sediment delivery
  cuts to the receiving water; costs are land taken out of production.
- **Irrigation scheduling by soil moisture**: expect water savings and less
  nutrient wash-off; requires trustworthy sensor or model moisture.

## Pond / lake

- **External load reduction** (inflow N/P): expect slow chlorophyll response
  where internal loading dominates — model the lag explicitly.
- **Internal load management** (aeration, sediment treatment, drawdown):
  expect faster oxygen and phosphorus response; costs and ecological side
  effects are the risk column.
- **Shoreline and macrophyte restoration**: expect habitat and clarity gains;
  horizon 2–5 years.
- **Biomanipulation** (fish community change): expect clarity gains in suitable
  shallow lakes; flag as high-uncertainty, specialist-reviewed scenario.
- **Bloom and sanitary-risk management** (load cuts, mixing, bathing advisories):
  score on phytoplankton composition shift, cyanotoxin frequency, and fecal
  indicator classes — chlorophyll alone does not prove the water is safer.

## River reach

- **Effluent limit tightening**: expect DO/BOD improvement downstream; model
  low-flow conditions, not annual averages.
- **Riparian buffer restoration**: expect temperature, sediment, and nutrient
  gains; horizon 3–10 years for shading.
- **Environmental flow restoration**: expect habitat availability gains;
  conflicts with abstraction users belong in the risk column.
- **Barrier removal / fish passage**: expect connectivity gains; sediment
  release pulse is the known short-term cost.
- **Contamination source control** (wastewater, stormwater, industrial or
  agricultural sources): score on contaminant and sanitary indicators at the
  exposure point and downstream, with detection limits stated — a modeled
  concentration drop below the analytical limit is not a measured recovery.

## Air basin

- **Source emission cuts** (industry, heating, traffic variants): expect
  concentration and deposition improvements downwind; dispersion model
  decides the pattern, intuition does not.
- **Green infrastructure** (shelter belts, urban greening): expect local
  deposition and microclimate effects; basin-wide claims require evidence.

## Conservation

- **Corridor creation / stepping stones**: expect connectivity gains for
  target species; verify with species movement data where it exists.
- **Invasive species control**: expect native indicator recovery; model
  re-invasion pressure from surrounding land, using as the minimum data
  basis the invasive species' occurrence records and the land-cover map of
  the surrounding matrix (propagule sources and corridors).
- **Pressure reduction** (grazing, visitors, road closure): expect habitat
  recovery trends; horizon usually 3+ years.
- **Protected-area boundary options**: compare habitat coverage and
  fragmentation across boundary variants; the deliverable compares, the
  decision stays with the governing body.
- **Early detection and rapid response** (eDNA and targeted surveys for
  invasives or disease): expect value only where a response protocol and
  budget exist; a detection capability without a response pathway is
  monitoring, not management.
