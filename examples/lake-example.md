# Worked example — a small lake, end to end (Tier S)

> **EXAMPLE — a teaching miniature.** The lake, the village, and every
> number below are illustrative, invented to show the shape of a finished
> build. They are not measurements and must never be cited as data.

## Object passport (extract)

- **Object:** Lake Primernoe, 0.8 km², max depth 9 m, one inflow stream,
  one village (900 people) on the north shore, bathing beach, small
  wastewater discharge from the village treatment plant.
- **Owner / decision:** the municipality; the decision is whether to fund
  a constructed wetland on the inflow in next year's budget, and how to
  run bathing-season warnings this year.
- **Maturity target:** 3 (Informative) this year; 4 (Predictive) only
  after the first verified forecast season. **Tier:** S.
- **Weights fixed in advance:** ecosystem outcomes 0.5, cost 0.2,
  implementation risk 0.15, time to effect 0.15.

## Data and evidence inventory (extract)

- Open: Sentinel-2 (surface extent, chlorophyll proxy, 2017–today);
  Landsat archive to 1984 (shoreline, catchment land cover); ERA5 meteo;
  regional hydromet station 12 km away (temperature, precipitation).
- Rescued history: the district water yearbooks 1998–2015 give summer
  TP and chlorophyll (method change in 2009 — break logged in the bias
  register; trends reported in two segments).
- Client/field: monthly TP, TN, chlorophyll, Secchi, DO profiles from the
  regional lab, 2021–today; village plant discharge reports.
- **Gap stated:** no winter under-ice oxygen data — winter fish-kill risk
  is monitored by testimony and ice records only, and the passport says so.
- Evidence: eutrophication and bathing-water literature via PubMed /
  Europe PMC; thresholds anchored to national standards, checked at build
  time — not copied from this example.

## Indicators selected (extract)

Core lake set: water level; temperature and DO profiles; TP (total and
phosphate fraction), TN (nitrate and ammonium separately); chlorophyll-a;
Secchi; phytoplankton composition in season; cyanobacteria biovolume;
E. coli at the beach (bathing use triggers the sanitary panel); inflow
load (concentration × discharge). Conditional panel added: sediment TP
(internal-loading question). Not selected: PFAS, radionuclides — no
source or pathway; reason recorded in the passport.

## Pattern memo (extract)

- Blooms in the record cluster after ≥10 hot, calm days with surface
  temperature above ~23 °C (illustrative pattern, moderate confidence).
- Ice-off has advanced ~9 days across the Landsat record (high confidence
  as a satellite observation; ecological meaning still being assessed).
- Chlorophyll responds to inflow TP with a 2–4 week lag in the monthly
  series — the lead–lag that makes a bloom watch possible.

## Event catalogue (extract)

| Year | Event | Antecedents | Impact | Response |
|---|---|---|---|---|
| 2019 | Cyanobacteria bloom, 3 weeks | Heat wave, calm, high TP | Beach closed 12 days | Advisory only |
| 2022 | Bloom + small fish kill | Heat, stratification, DO crash at depth | Fish loss, press attention | Emergency aeration, late |

Two bloom events in the record — below the threshold for a statistical
event forecast. The product is therefore a **watch** on antecedent
conditions plus the TARP below, honestly labeled, not a probability.

## Forecast registry entry (extract)

- **ID:** LP-F-001. **Issued:** before the season, timestamped.
- **Forecast:** "At least one amber bloom-watch trigger (TARP LP-T-01)
  will fire this bathing season" — probability 0.7, interval 0.5–0.85,
  from the antecedent pattern, model v0.1 (index model).
- **Metric declared:** Brier score at season close, computed against this
  entry exactly as issued.

## TARP (extract) — LP-T-01, bloom and bathing risk

- **Trigger:** surface temperature > 23 °C for 5 days + cyanobacteria
  biovolume above the amber band on two consecutive samplings.
- **Watch:** sampling twice weekly; beach signage prepared.
- **Act:** bathing advisory issued by the municipality's named officer;
  aerator deployed to the deep basin (needs 1 day; forecast/watch lead
  time is ~1–2 weeks — prevention is feasible, and the plan says why).
- **Stand-down:** two consecutive samplings below the amber band.
- **After-action review:** at season close, with the forecast score.

## Option card (extract) — the budget decision

- **Option:** constructed wetland on the inflow (nature-based, evaluated
  first). **Expected effect:** inflow TP load −30 to −45% in 2–3 years
  (twin run on the load balance + published wetland effect sizes;
  confidence moderate; internal sediment loading will delay the lake's
  response — the lag is modeled, not hidden).
- **Cost/risk:** land lease on 1.2 ha of marginal farmland; maintenance
  duty named. **Reversibility:** high. **Residual risk:** blooms remain
  possible in hot years even after load cuts — the TARP stays in force.
- **Verification:** inflow TP load and summer chlorophyll, reviewed at
  year 3 against this card. **Counterfactual:** on funding approval, the
  no-action baseline twin is frozen (configuration archived with manifest
  IDs) and both twins run on the same observed weather thereafter.

## Deliverable and gate

Package ships at maturity 3 with the prototype limits stated (bloom
product is a watch, winter oxygen is a gap), every headline number
carrying a manifest ID, and the Gate C red-team record attached: two
material attacks (threshold anchor re-checked against the current
national standard; satellite chlorophyll proxy relabeled as a proxy in
the public summary) — both dispositioned as fixed before delivery.
