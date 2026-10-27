# Calibration bounds — declared physical ranges for fitted parameters

A fit can be good and still be wrong: a model that beats its benchmark with
a physically impossible parameter has fitted the noise, not the ecosystem.
Admission therefore requires, besides SS_RMSE > 0 on every PRIMARY target
variable declared in the Object Passport (secondary background variables
are reported, not gated; when no variable in the dossier carries a
`primary` flag, every variable is primary), that every fitted parameter
sits inside a declared physical bound
(`scripts/skill_scores.py admit`). A parameter outside its bounds is
REJECTED even when SS_RMSE > 0, and the verdict names it.

Rules for the bounds table:

- **Bounds come from the literature, not from the fit.** Fitting the bounds
  to the fitted values makes the gate meaningless. Each build declares its
  own bounds from the literature for its object and its fitted parameters,
  with a source per bound.
- **A bound without a source is not a bound.** The dossier records the
  source per parameter; the verdict prints it with the failure.
- **The table below is an example starting set**, not a universal table:
  the right bound depends on the object, the climate, and the model form.
  Replace it per build; keep the source column.

| Parameter | Typical published range | Source |
|---|---|---|
| Phytoplankton maximum specific growth rate | 0.2–2.0 d⁻¹ (at ~20 °C) | Reynolds, The Ecology of Phytoplankton, 2006; Eppley 1972, Fish. Bull. 70: 1063–1085 |
| Light attenuation coefficient (Kd), lakes | 0.1–5 m⁻¹ | Kirk, Light and Photosynthesis in Aquatic Ecosystems, 3rd ed., 2011 |
| Sediment–water phosphorus release rate | 0–10 mg P m⁻² d⁻¹ | Søndergaard et al. 2003, Hydrobiologia 506–509: 135–145 |
| Manning's roughness coefficient, open channels | 0.02–0.08 s m⁻¹/³ | Chow, Open-Channel Hydraulics, 1959 |
| Soil organic-carbon decomposition rate | 0.001–0.1 d⁻¹ (labile to recalcitrant pools) | Parton et al. 1987, Soil Sci. Soc. Am. J. 51: 1173–1179 |
| Forest net primary production | 0.2–2.0 kg C m⁻² yr⁻¹ (boreal to temperate) | Luyssaert et al. 2007, Glob. Change Biol. 13: 2509–2537 |

(Source of the gate: the lake hydrodynamic platforms of Baracchini et al. —
a fit that beats the benchmark with an impossible parameter is rejected.)
