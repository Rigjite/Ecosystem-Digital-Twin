# World practice base

Surveyed 2026-10-20. What the leading ecosystem and Earth digital twins do,
what this skill borrowed, and what it changed for its own scale (one operator,
one client object at a time — not a supercomputing program). Verify current
project status at build time; all of these evolve.

## Destination Earth (DestinE) — European Commission / ECMWF / ESA / EUMETSAT

A digital twin of the Earth system: platform launched June 2024 with two
priority twins (weather-induced extremes; climate-change adaptation), built
on EuroHPC supercomputers, structured as a Digital Twin Engine over a
federated Data Lake.

- **Borrowed:** data assimilation as the twin's core discipline — the twin is
  continuously constrained by observations, not run once. (→ Phase 4
  assimilation cycle.)
- **Borrowed:** on-demand what-if scenario exploration as the primary user
  interaction. (→ Phase 5.)
- **Improved for this scale:** DestinE measures skill mainly mid-chain
  (forecast accuracy). This skill adds the end-of-chain test — decision
  value: did the twin change a real decision, and did the outcome improve?
  (→ Phase 4, standing verification.)

## BioDT — EU Horizon Europe biodiversity digital twins

Ten prototype digital twins for biodiversity (Horizon Europe project),
built on GBIF, eLTER, DiSSCo and LifeWatch infrastructures, EuroHPC LUMI;
methods published in npj Biodiversity (DOI 10.1038/s44185-025-00116-3) and
the RIO journal special issue (RIO 10: e133474).

- **Borrowed:** FAIR data plus RO-Crate provenance packaging — datasets,
  models, and workflows versioned together so outputs trace to specific
  inputs and parameters. (→ Phase 6 provenance package.)
- **Borrowed:** modular construction — the same workflow modules reused across
  different twins. (→ Phase 2 modularity.)
- **Borrowed:** hybrid models — statistical and process-based combined.
  (→ Phase 2.)
- **Borrowed:** co-creation with stakeholders and end-users from the start,
  and the honest "prototype digital twin" staging. (→ Phase 0 stakeholder
  map and maturity level 1.)

## EU Digital Twin of the Ocean (DTO) — Mercator Ocean / EDITO platform

A dynamic replica of the ocean (current phase EDITO2, 2025–2028, per
Mercator Ocean International) integrating Copernicus Marine and EMODnet
data; flagship applications include a Nature-Based Solution Assessment
(seagrass and coastal vegetation scenarios for the Wadden Sea and Songor
Lagoon), a plastic pollution tracker, and species drift tracking.

- **Borrowed:** the three-layer architecture — real-time monitoring,
  short/medium-term forecasts, impact simulations — kept visibly separate.
  (→ Phase 2.)
- **Borrowed:** nature-based solutions as a first-class scenario family.
  (→ Phase 5, strengthened: NBS are evaluated *first*, and an engineered
  recommendation must justify itself against them.)
- **Borrowed:** local twins nested into the wider infrastructure (the PHAROS
  pattern of site twins feeding the EU DTO). (→ Phase 6 nesting.)

## Delft-FEWS / Deltares — operational water forecasting, Netherlands

The flood and water forecasting platform behind Dutch and many national
forecasting centers; integrates arbitrary models through adapters, with
OpenDA assimilation (Ensemble Kalman and particle filtering, error
correction) and an operational forecast verification system.

- **Borrowed:** the pre-modeling data quality gate — automated validation
  (extremes, rate of change, spatial homogeneity, trend breaks),
  gap-filling protocols, and fall-back data hierarchies so forecasting never
  depends on a single feed. (→ Phase 1.)
- **Borrowed:** verification as a standing operational system, not a one-off
  study: forecasts are archived and routinely re-scored with multiple metrics
  covering quality, value, and consistency. (→ Phase 4.)
- **Improved for this scale:** Deltares verification is largely internal.
  This skill makes the current verification score part of the client
  deliverable — the client sees the twin's measured skill, not its promised
  skill. (→ Phases 4 and 6.)

## Wageningen University & Research — farm digital twins (Digital Future Farm, greenhouse twins)

Validated crop models (WOFOST family) connected to real-time farm data
through the open MODCOM component framework and the FarmMaps data platform;
the Digital Future Farm works explicitly on ethical, legal and societal
aspects (ELSA) alongside the technology.

- **Borrowed:** the closed-loop definition — a true twin is bidirectional:
  data flows in continuously, and decisions flow back to the physical asset.
  A one-off simulation is a model, not a twin. (→ Purpose, Phase 4.)
- **Borrowed:** farm data spaces — the farmer owns the farm's data; sharing
  runs through governed data spaces, not platform capture. (→ Non-negotiables:
  the client's data stays the client's.)
- **Borrowed:** ELSA review as a build step, not an afterthought.
  (→ Phase 0 ethical-legal-societal check.)
- **Borrowed:** dense sensor validation before decision support (greenhouse
  twins validated against 5-minute sensor streams) — the practical root of
  this skill's calibration gate. (→ Phase 3.)
