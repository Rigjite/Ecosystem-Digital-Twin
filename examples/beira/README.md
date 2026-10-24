# Worked example — Beira Lake, Colombo (published data only)

A real urban lake, run through the skill as far as published data allow. Every input number has a source; nothing comes from unpublished or company documents. Where data are missing the example says so (`[НЕТ ДАННЫХ]`) instead of filling the gap.

Run: `python3 beira_twin.py` (or `--json`). Standard library only.

## What it shows

| Step | Skill phase | Result |
|---|---|---|
| 1. State vs thresholds | Passport → indicators | Water Pollution Index above 1 in both seasons with the whole ±SD band above it; wet season hypertrophic by N and P; heavy-metal index above 100 in the wet season only [P24] |
| 1b. Cross-check | Evidence layer | Three independent studies agree: WPI 1.856 in Sep 2023 – Feb 2024 [P25]; more than 93 % of the surface in poor condition and hypereutrophic [D24]; the microcystin toxin gene *mcyA* in every 2026 sample [A26] |
| 2. Source check | Gate B style check of the source | The published mean wet-season TSI(TP) (129.09) corresponds to the published *maximum* TP (5.84 mg/L → TSI 129.2). Recorded as an open question for the authors before the mean is used for calibration — not as an error claim |
| 3. Decision arithmetic | Scenario screening | A wetland at the median published TP removal (46 %) [L16] leaves even the least polluted point hypertrophic (TSI 90.5 → 81.7) [C77]. Leaving the hypertrophic class needs a 52–97 % cut in TP, and the response lags 10–15 years [J05]. A wetland is necessary but not sufficient |
| 4. Value of information | Decision under uncertainty | In relative units (disposal = 1), analysing the sludge before choosing the field route saves 0.04–0.4 of the disposal cost; it is worth doing whenever it costs less than that |
| 5. Forecast registry | Predictive claims earned in advance | One trial forecast registered with `scripts/registry.py` (wet season 2027, WPI > 1, p = 0.9); the hash chain verifies |
| 6. Gaps | Maturity | Stops at maturity 2 (Descriptive): no station-level series, no sediment chemistry, no loads, no measured microcystin concentrations since 2013–2014, no costs |

The forecast in `registry.jsonl` can be reproduced with:

```bash
python3 ../../scripts/registry.py issue --registry registry.jsonl --id BEIRA-F-001 \
  --kind probability --value 0.9 \
  --target "Beira Lake, wet season 2027: mean Water Pollution Index of the four basins above 1.0 (P24 method), no comprehensive measures in place" \
  --horizon-end 2027-12-31 --model "persistence of the 2022-2023 state" --model-version 1 \
  --inputs P24 --metric brier --trial
python3 ../../scripts/registry.py verify --registry registry.jsonl
```

## Management context (2025–2026, press reports)

A restoration task force convened by the Western Province governor in May 2025 brings together more than twenty agencies, companies and universities [N25]. In January 2026 a Rs 2.5 billion plan was announced: 192 illegal sewage discharge points identified (most reported closed), dredging, aerators and solar-powered waste boats [N26a]. In June 2026 the plan added the diversion of ten sewage canals to a pumping station and the sea outfall; earlier chemical treatment attempts were reported to have failed [N26b]. In July 2026 a private donor offered to fund a short-term seawater intake [N26c]. None of these reports gives water-quality measurements.

For a twin this changes the questions, not the method: the scenarios in step 3 are now real decisions; dredged sludge will exist soon, so the sludge analysis in step 4 is due before the material is moved; and any seawater intake adds salinity to the checks of the field route.

## Limits

- Step 3 assumes in-lake TP falls in proportion to the external load cut — an optimistic bound; internal loading from sediments slows the response.
- Step 4 uses relative costs and a parameter grid, not prices; it shows how the decision turns on the probability that processed sludge complies, which only a laboratory analysis can establish.
- The probability in step 5 is an expert judgment from persistence, registered as a trial forecast with no decision weight.
- [P25] and [A26] are symposium abstracts: useful as cross-checks, not as calibration data.

## Sources

- [P24] Prasad S., Wei Y., Chaminda T. et al. Spatiotemporal assessment of water pollution for Beira Lake, Sri Lanka. *Water* 2024, 16(11), 1616. doi:10.3390/w16111616
- [D24] Dharmarathna D., Galagedara R., Himanujahn S., Karunaratne S., Athapattu B. Assessment of pollution state of Beira Lake in Sri Lanka using water quality index, trophic status, and principal component analysis. *Aquatic Ecology* 2024, 58, 159–174. doi:10.1007/s10452-023-10052-8
- [P25] Perera K.A.B.P., Perera H.A.C.C. A comparative assessment of water pollution in Beira Lake and Ihalagama Lake in the Western Province of Sri Lanka. 29th International Forestry and Environment Symposium, University of Sri Jayewardenepura, 2025 (abstract). https://journals.sjp.ac.lk/index.php/fesympo/article/view/8262
- [A26] Arachchi G.J.B., Jayasinghe M.T., Ravi K. et al. Morphological and molecular characterization of microcystin-LR producing cyanobacteria in Beira and Boralesgamuwa lakes, Sri Lanka. 2026 (abstract). doi:10.31357/fesympo.v30.8999
- [C77] Carlson R.E. A trophic state index for lakes. *Limnology and Oceanography* 1977, 22(2), 361–369. doi:10.4319/lo.1977.22.2.0361
- [L16] Land M. et al. How effective are created or restored freshwater wetlands for nitrogen and phosphorus removal? A systematic review. *Environmental Evidence* 2016, 5, 9. doi:10.1186/s13750-016-0060-0
- [J05] Jeppesen E. et al. Lake responses to reduced nutrient loading — an analysis of contemporary long-term data from 35 case studies. *Freshwater Biology* 2005, 50(10), 1747–1771. doi:10.1111/j.1365-2427.2005.01415.x
- [N25] A breath of new life to the Beira. *The Sunday Times* (Sri Lanka), 21 September 2025. https://www.sundaytimes.lk/250921/news/a-breath-of-new-life-to-the-beira-612996.html
- [N26a] Sri Lanka to spend Rs 2.5bn to save Beira Lake. *EconomyNext*, 19 January 2026. https://economynext.com/sri-lanka-to-spend-rs-2-5bn-to-save-beira-lake-258113/
- [N26b] Pollution checked, stench gone: Beira clean-up project begins. *The Sunday Times* (Sri Lanka), 7 June 2026. https://www.sundaytimes.lk/260607/news/pollution-checked-stench-gone-beira-clean%E2%80%91up-project-begins-644898.html
- [N26c] Beira Lake clean-up project to be launched. *Ada Derana*, 9 July 2026. https://www.adaderana.lk/news/cmrddx0sv000b356q294bse8d
