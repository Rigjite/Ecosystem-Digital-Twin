# ecosystem-digital-twin — Changelog

## v2.8 — 2026-10-28

- Zenodo DOI for v2.8: 10.5281/zenodo.23751220 (GitHub release v2.8, 2026-10-28; record published 2026-10-29 UTC). README (EN/RU) and CITATION.cff now cite it.

- **Dual licence (T103, 2026-10-28)** — the author's decision: text and
  method stay under CC BY 4.0 (BY-ND not adopted); code is licensed under
  Apache-2.0. Added `LICENSE-CODE` (the canonical Apache License 2.0
  text, unchanged). Code means the Python files in scripts/, tests/ and
  examples/, and the CI workflow in .github/workflows/; everything else
  stays CC BY 4.0 (`LICENSE`, unchanged). README (EN/RU): licence
  section, version line and a code-licence badge. SKILL.md and
  SKILL.ru.md frontmatter `license` names both. CITATION.cff: the
  `license` field stays CC-BY-4.0 (the Zenodo record licence) and the
  abstract states the code licence. New test T103
  (`TestDualLicenceV28`, 4 tests).
- **Release edits (T102, 2026-10-28)** — Claude Anthropic, on the
  author's go-ahead to publish. (1) Release date set to 2026-10-28 in
  README (EN/RU), CITATION.cff and this file, matching SKILL.md. (2) DOI
  in README (EN/RU) and CITATION.cff moved off the v2.3 record
  (10.5281/zenodo.23657185) to the latest minted record, v2.7
  (10.5281/zenodo.23681769); the v2.8 DOI follows the release, as with
  earlier versions. Test fixtures for build_manifest.py keep their
  sample DOI. (3) `references/thresholds.md` status header and closing
  line: candidate and "not applied to v2.7" wording removed; licence
  line states CC BY 4.0 (the BY-ND proposal was not adopted).
  (4) README (EN/RU): scope line added under Status — the skill builds and
  runs the twin's evidence, validation and provenance layers and does not
  yet ship a process model with data assimilation (planned for v2.9); roadmap updated
  (v2.7 cross-vendor round done; Sentinel-2 via STAC done as
  fetch_satellite.py; v2.9 items listed). (5) Brand line made neutral
  and identical in both READMEs (the EN and RU lists of candidate names
  disagreed). New test T102 (`TestReleaseV28`, 4 tests).

- **Independent verification follow-up (T101, 2026-10-28)** — Muse's
  verification of the T100 build against primary sources (336 tests,
  strict lint PASS, catalogue 413 rows re-counted). Confirmed: Norway
  § 25 «Tetthet» (current Lovdata text FOR-2008-06-17-822 — T99's §19
  cited the 1998 regulation's translation, not the 2008 regulation);
  USDA ERS RCS-26H confirms the 3.7 Mt record only, its FAS-circular
  pointer sits in the Bangladesh paragraph; Danube fish split (about 90
  MAB, 45 freshwater WH documentation); GEPIS ratio about one and a
  half (5.5–6.2 vs DCS 3.7–4.1 t/ha); IPCC Table 2.1 splits temperate
  grassland by nutrient status and drainage depth (5.3 / 6.1 / 3.6),
  no cool/warm split — T99's "6.1 warm temperate" gloss was the
  FAOSTAT/ESSD simplification (the row values were already right).
  Corrections to the T100 record: (1) DCS yields restored as verified
  — read directly from the primary DCS Paddy Statistics table by Muse
  in T99 (2022/23 Maha 3,731; 2023 Yala 4,128 kg/ha); T100's "site
  blocks automated access" records Claude's access limit, not the
  verification state. (2) Laksvel 'very high' IS in the protocol —
  §4.3: "This must be described as very high" for the >2% monthly
  mortality case; the row's four colour levels stand, the descriptor
  is omitted as redundant with the level name, and the T100 rationale
  is corrected. (3) T100 test count corrected 5 → 6; the stale T99
  test-class docstring (USDA FAS circular, Norway §19, Danube 5,500
  as "verified and closed") updated to the T100-corrected state.
  Figures still not read from a primary document: Todgerel 2020
  (secondary citation), the USDA area and yield (trade press), the
  Danube 9,581 census count (institute figure via Agerpres, census
  report not read — disclosed in the source list). New test T101
  (`TestT100FollowUpOct28`, 3 tests). 339 tests pass; strict lint PASS.

- **T99 follow-up (T100, 2026-10-28)** — Claude's review of the T99 build
  (9.3/10); fixes applied by Claude at the author's request, so the next
  cross-check goes to another model. (1) Norwegian density rule: § 25
  «Tetthet» of akvakulturdriftsforskriften (FOR-2008-06-17-822), read from
  the regulation's full Norwegian text on FAOLEX (nor82122) — T99's "§19,
  FAOLEX" is not the paragraph in that text, and the Ecolex/FAOLEX record
  links no English translation; the T99 test that pinned §19 is repointed.
  (2) USDA Sri Lanka 2025/26: the ERS Rice Outlook RCS-26H confirms the
  record 3.7 Mt milled only (area "higher", yield "+10%", no figures; its
  FAS-circular pointer is in the Bangladesh paragraph), so 1.2 M ha and
  4.62 t/ha stay trade-press values citing USDA. (3) Danube Delta: the
  2017 biodiversity census count (9,581 species; about 7,440 in 2008)
  leads, "over 5,500" kept as an older summary; fish given as about 90
  (MAB) of which 45 freshwater (UNESCO WHC). (4) Laksvel row: the four
  colour levels from §4.3; the descriptor 'very high' is not in the
  protocol and is dropped. (5) GEPIS example: "roughly double the
  national average" corrected to about one and a half times (DCS
  3.7–4.1 t/ha). (6) Corrections to the T99 record below: the catalogue's
  Tier 1 values are those of IPCC 2013 Wetlands Supplement Table 2.1
  itself, re-read from the IPCC chapter — grassland 5.7 boreal, temperate
  5.3 nutrient-poor / 6.1 nutrient-rich deep-drained / 3.6 nutrient-rich
  shallow-drained, 9.6 tropical; the table has no cool/warm temperate
  split ("6.1 warm temperate" is the FAOSTAT/ESSD simplification), and
  the pre-T96 wording was not fully correct either, it carried those
  FAOSTAT labels. Figures still not read from a primary document:
  Todgerel 2020 (secondary citation), the USDA area and yield (trade
  press), and the DCS yields (the DCS website blocks automated access;
  re-read at build time). New test T100 (`TestT99FollowUpOct28`, 6 tests); three T99 tests repointed (Norway, USDA, Danube).
- **Independent verification (T99, 2026-10-28)** — Muse's independent check of the T97/T98 build against primary sources (323 tests, strict lint PASS, catalogue 413 rows re-counted). Correction to the record: the T96 Tier 1 "fix" was itself wrong — it swapped the cropland and grassland factors on the basis of a garbled FAOSTAT PDF text extraction (a two-column layout collapsed into one); the pre-T96 values were correct. T97 restored them, and T99 verified the assignment against ESSD Table 5 (Conchedda & Tubiello 2020, reproducing the 2013 IPCC Wetlands Supplement Table 2.1): cropland 7.9 t CO₂-C/ha/yr boreal and temperate, 14.0 tropical; grassland 5.7 boreal, 6.1 warm temperate, 9.6 tropical. Verified against primary sources and closed: USDA 2025/26 Sri Lanka record (3.7 Mt milled confirmed by the USDA ERS Rice Outlook RCS-26H, 15 September 2026; area 1.2 M ha and yield 4.62 t/ha rough from the USDA FAS World Agricultural Production circular, September 2026, as quoted in the trade press — arithmetic cross-check 1.2 × 4.62 ≈ 5.5 Mt rough ≈ 3.7 Mt milled); DCS revised paddy yields (2022/23 Maha 3,731; 2023 Yala 4,128 kg/ha); the Laksvel mortality band — monthly mortality above 2% is level 3 (red level), "very high" (Laksvel protocol, Institute of Marine Research, Rapport fra Havforskningen 2025-40, §4.3), with the citation corrected (the protocol is not the Norwegian Veterinary Institute's Fish Health Report 2025); the Danube Delta "over 5,500 species" total (Claudino-Sales 2018); the Norwegian density paragraph confirmed as §19 (FAOLEX English translation; the trade press's §25 is the wrong numbering). Still unverified, and the only figure left so: Todgerel 2020 (secondary citation; the primary document was not consulted). The FAO cropland N-surplus figure stays provisional outside the rows (not a row anchor). New test T99 (`TestIndependentVerificationOct28`, 7 tests). 330 tests pass; strict lint PASS.
- **Accuracy sweep (T98, 2026-10-28)** — a further check of §21–§32
  figures against primary sources by Claude, at the author's request
  (two iterations). Confirmed without change: Taranger et al. 2015 (21 of
  34 wild populations at moderate-to-high introgression risk), EU
  2024/1244 (feed-based aquaculture above 500 t; N 50,000 / P 5,000 kg/yr
  to water; applies from 1 January 2028), Morris et al. 2016 (0.3 cm/yr,
  now cited from the abstract), ITS_LIVE v2.0 (The Cryosphere
  19:3517–3533), NYC CSO (398 outfalls, ~18 bn gal/yr), Western Arctic
  peak (490,000 in 2003, now cited from ADF&G). Corrected: the Everglades
  slope and remaining extent — the Florida Museum ("less than two inches
  per mile", "less than half") and the Davis & Ogden overview ("~2.5",
  "just over half") differ, so the catalogue carries "about 2 inches per
  mile or less" and "about half" and names both; the Norwegian 25 kg/m³
  rule cited by title (§19 in the FAOLEX translation, § 25 in trade press —
  confirm on Lovdata); the copper row given its ASC indicator (4.7.4,
  below 34 mg/kg dry sediment); Har Us Nuur endemic fish carried as three
  to five (the Ramsar sheet says both). Structure: the §23 stocking,
  utilisation and SOC rows reduced to cross-references to §22 plus the
  farm reading, so the anchors live once; draft wording cleared from the
  source list. New test T98 (`TestAccuracySweepOct28`, 7 tests); one T89
  assertion re-worded with the source list. 323 tests pass; strict lint
  PASS. Not verified in this sweep and left as cited: the Laksvel
  2%-per-month mortality band and the Danube Delta "over 5,500 species"
  total.
- **T96 follow-up (T97, 2026-10-28)** — Claude Anthropic's re-review of
  the T96 build (8.5/10); fixes applied by Claude at the author's
  request, so the next cross-check goes to another model. The T96
  archive failed its own strict lint (a backticked path to the planned
  gate_check.py script in the v2.9 note below) — now plain text. §24 Tier 1
  factors set to IPCC Wetlands Supplement Table 2.1 (T96 had exchanged
  the cropland and grassland values). The source list and the GEPIS
  worked example synced with the T96 catalogue fixes (Peatland Code v2.1,
  PDGL 21/25/1, Gutman & Ignatov vs Carlson & Ripley, Western Arctic peak
  2003, Chen et al. 2021, Rising et al. 2026, FRA 2025 fire on all land,
  WRI 2024/2025 forest loss, FAO 2024 salt with the 2021 depth split
  labelled, DCS rice yields, Fluet-Chouinard et al. 2023, the IPCC
  organic-soil definition). The broken §25 DHW sentence rejoined; the §28
  depth split labelled FAO 2021; the cryosphere quick set gains glacier
  mass balance; SKILL.ru.md Stage 1 states the anchor hierarchy and the
  stricter-binding rule. New test T97 (`TestT96FollowUpOct28`, 7 tests);
  the T85 yield assertion repointed to the DCS series. 316 tests pass;
  strict lint PASS. SKILL.md unchanged.
- **Claude full-candidate review fixes (T96, 2026-10-28)** — Claude
  Anthropic's 8/10 review of the whole candidate, verified point by point
  against primary sources before applying (figures taken from the primary
  sources, not from Claude's report). (1) All 10 accuracy errors in
  §21–§32 corrected: 47 dangerous glacial lakes by basin (21 Nepal, 25
  Tibet AR China, 1 India); the IPCC peat definition (organic horizon
  ≥ 10 cm, ≥ 12% OC; the 40 cm figure is the FAO Histosol equivalence);
  Tier 1 Table 2.1 factors unswapped and units corrected to t CO₂-C/ha/yr;
  Peatland Code v2.1 (October 2024) with its real base categories; FVC
  linear scaling = Gutman & Ignatov (1998), quadratic form = Carlson &
  Ripley (1997); DOI abf28b re-attributed to Mekonnen et al. 2021;
  Western Arctic caribou peak ~490,000 in 2003 (ADF&G); fire 261 M ha/yr
  is all land, about half of it forest; DCS rice yields (2022/23 Maha
  3,731, 2023 Yala 4,128 kg/ha, revised series); salt 1,381 Mha (FAO
  2024). (2) Outdated figures updated: tropical primary forest loss
  3.7 M ha (2023), 6.7 M ha (2024, record), 4.3 M ha (2025, GFW/UMD);
  wetland loss as a range of estimates (Davidson 64–71% vs
  Fluet-Chouinard et al. 2023 ~21% since 1700). (3) Unverified figures
  sourced or removed: USDA 2025/26 figures kept as the September 2026
  estimate as reported in the trade press, to be checked against the USDA
  circular; iScience 2026 seagrass, Chen et al. 2021 thermokarst (10.5% /
  3.4%), Todgerel 2020 figures corroborated via the citing paper, Sci.
  Rep. 2024 peat rewetting trial — all cited in full; Krasnoyarsk
  berries and the Selenga manganese clause removed (unsourced /
  off-row). (4) Structure: §30–§32 brought to the §21–§29 format
  (watch-levels and does-NOT-do subheads, Conditional module naming);
  the §31 table closed by a blank line; §18 quick sets completed
  (forest age structure, basal area, soil carbon; wetland type
  composition); §19 and README counts fixed; working notes moved here.
  (5) Duplicates: active-layer thickness cross-referenced to §29;
  grazing rows cross-referenced with the arid-conditions caveat
  restored; the mast index no longer drives alerts (the conflict-report
  series does — the bear strip moved from §20 to §30, reframed); DHW no
  longer closes shellfish beds; the Beira WPI clause is out of the rice
  example. (6) Gate qualified: the stricter *binding* standard governs
  red, guidance and drafts stay yellow (SKILL.md Stage 1, within the
  existing line; §20). (7) Completeness: glacier mass-balance row (§21)
  and copper/antifouling row (§27) added. (8) The §22 Daurian example is
  the second explicit exception to the "no Russian worked examples" rule
  (her decision of 28 October 2026 — transboundary Landscapes of Dauria,
  Russian-side data; figures from Buuveibaatar et al. 2024, Oryx, and
  Bazhenov 2019, Nat. Conserv. Res.). New test T96
  (`TestTablesClosedOct28`, 4 tests): every table run followed by a blank
  line, §31 closure regression, 12 + 12 subheads, stricter-binding
  wording. SKILL.md stays 499 lines; SKILL.ru.md stays 561 lines.
- **Gate threshold rule fixed; PFAS numbers moved to thresholds.md (T95, 2026-10-28)** —
  Claude Anthropic's 8/10 review (SKILL.md only), verified point by point,
  with Claude's own two amendments to the plan. (1) The three-way
  contradiction is resolved by an explicit rule, not by weakening the
  gate: a binding standard sets red and blocks; guidance or a draft
  assessment sets yellow (early warning, no block); where no binding
  standard exists for a matrix, the threshold is chosen by the Stage 1
  hierarchy and fixed in the Object Passport BEFORE data arrives, and it
  becomes red for this build; no measurement ([НЕТ ДАННЫХ]) still blocks
  the flow. (2) The brand-candidate line is removed from SKILL.md
  entirely — the candidates (ADIS, AdisECO, AdisTwin, NaranTwin) live
  here in the CHANGELOG until the author decides; the brand is undecided.
  PFAS values moved from the gate to `references/thresholds.md` §1.8
  (checked 2026-10-28; rescission still only proposed as of October 2026;
  DüMV 100 µg/kg stands, the 2019 Bundesrat recommendation of 30 µg/kg
  is adoption-unconfirmed; EPA draft wording now follows EPA: risk
  exceeded in some scenarios — pasture, field, reclamation — at 1 µg/kg);
  the gate keeps the rule and a pointer. Jurisdictions 5 → 7 (Germany,
  Denmark added); indicators 20 → 21 (PFAS). Description now names steppe
  and grassland and aquaculture (both languages). The two gap markers are
  defined in the skill: [НЕТ ДАННЫХ] = unmeasured in this build (blocks);
  [NEXT DATA] = a catalogue gap with a named next source (a research
  task, not a value). Stage 2 now states what `fetch_satellite.py`
  actually returns (scene list + NDVI, not SDD; Planetary Computer
  downloads need signed URLs). The "New in v2.8" paragraph keeps the
  twelve section names the tests pin, minus the brand line. Date updated
  to 2026-10-28. Two defects found by the suite and fixed in passing:
  the Stage 1 cross-reference "(see Template 2)" broke the tests' gate
  split (rewritten as "(see the Safety Gate below)"), and the lengthened
  compatibility line exceeded the 500-character lint cap (shortened).
  SKILL.md is now 499 lines — one line under the 500 limit; the next
  addition must move text out of SKILL.md. New test T95
  (`TestGateThresholdRuleOct28`, 8 tests); T90 counts updated to 21
  indicators / 7 jurisdictions / 25 [provisional] marks; T93/T94 repointed
  to thresholds.md §1.8.
- **v2.9 scope, extended (2026-10-28)** — the model core (Vollenweider
  phosphorus balance, EnKF/particle-filter assimilation script),
  deseasonalised drift, bootstrap intervals for SS_RMSE, Igeo / PLI /
  Håkanson RI in the safety gate, the Stage/Phase dual numbering, the
  32-domain scope question, Rule 3 (0.1° floor for all sensitivity
  categories — a deliberate conservative choice, recorded, not fixed;
  extreme sensitivity is withheld entirely), and the notation nits
  ("дрейф" in two senses, β used by both Theil–Sen and KGE, "nudge" as
  bias correction rather than nudging). Mongol Daguur gazelle and marmot
  survey search; a planned gate_check.py script (v2.9, not yet written) + a registry hash chain for the
  gate threshold (so «fixed before data» is provable, not declarative).

- **PFAS gate corrected by matrix and by date (T94, 2026-10-28)** —
  Claude Anthropic's point (e), verified against the primary sources
  before applying. (1) Date corrected: the May 2025 wording was wrong —
  May 2025 was only EPA's announcement of intent; the formal rescission
  proposal for PFHxS/PFNA/HFPO-DA (GenX)/HI is 20 May 2026 (Federal
  Register 2026-10085, comments to 20 Jul 2026), not final as of Aug
  2026, and all six 2024 MCLs remain in force; the PFOA/PFOS compliance
  extension 2029 → 2031 is proposed, not final. PFHxS/PFNA/GenX/HI are
  now marked [provisional] in the gate. (2) Matrix corrected: drinking-
  water ng/L limits do NOT apply to solid sediment in µg/kg. Sediment/
  sludge anchors added (µg/kg dry weight): Germany DüMV — sum PFOA+PFOS
  100, labelling above 50 (2008 value); Denmark, Danish EPA 2023,
  indicative, not binding — PFAS4 15; EPA draft sewage-sludge risk
  assessment (Jan 2025, draft, not a standard) — risk for highly
  exposed groups above 1 µg/kg PFOA or PFOS (1 ppb) under 40-year
  application; several US states use 20 µg/kg PFOS and/or PFOA as
  interim practice [provisional]. The strictest applicable anchor
  governs; no jurisdiction anchor means [НЕТ ДАННЫХ] blocks. The
  microplastics method-gate is unchanged (Claude: the approach is
  correct; no numeric limit exists for sediment anywhere). The 9 m²
  green-space closure was confirmed correct by Claude (Italian
  D.M. 1444/1968, art. 3). New test T94
  (`TestSafetyGatePfasMatrices`, 4 tests). Claude's points (a)–(d) and
  the overall score are still open — the archive could not be downloaded
  by the reviewer; the author is attaching it directly.

- **PFAS and microplastics in the safety gate (T93, 2026-10-28)** — on
  her word "Да, добавь PFAS и микро пластик". Both were already
  conditional panels in the catalogue (§6: PFAS panel; microplastics in
  water, sediment and biota) but were NOT in the circular-economy safety
  gate — the audit's gap. Added to Non-Negotiable 5 and to Template 2
  (SafetyGateCard) in SKILL.md and SKILL.ru.md: a PFAS row (jurisdiction
  limit first — US EPA NPDWR Apr 2024: PFOA 4.0 ng/L, PFOS 4.0 ng/L,
  PFHxS/PFNA/HFPO-DA (GenX) 10 ng/L each, Hazard Index 1 for mixtures,
  with the May 2025 EPA retention of PFOA/PFOS and proposed rescission
  of the other four disclosed; EU Directive 2020/2184: sum of 20 PFAS
  0.1 µg/L, total PFAS 0.5 µg/L; no universal PFAS limit for
  sediment/soil — jurisdiction soil limit applies, otherwise
  [НЕТ ДАННЫХ] blocks) and a microplastics row (no numeric limit
  invented: the gate checks the harmonized method — named method, size
  range, polymer identification, blank controls — and the reported load;
  unnamed method, failed blanks or unmeasured load blocks the transfer).
  New test T93 (`TestSafetyGatePfasMicroplastics`, 4 tests). Still open
  from the same audit point: Igeo / PLI / Håkanson RI for sediment and
  soil in the gate (separate decision).

- **Quick fixes from the external 7.5/10 audit (T92, 2026-10-28)** — the
  audit was verified against the files before any fix was applied: two
  of its points were wrong and were NOT applied as written. (1) The
  HTML comment before the frontmatter is only in SKILL.ru.md, not in
  SKILL.md — moved below the closing `---` in SKILL.ru.md; SKILL.md
  frontmatter already started on line 1. (2) No code checks a `[NO DATA]`
  literal — a search of the whole candidate finds zero occurrences;
  `scripts/mismatch.py` uses the Russian `[НЕТ ДАННЫХ]`, matching the
  skill, so nothing was changed there. Applied: (a) the frontmatter
  `description` rewritten for v2.8 in SKILL.md (725 chars) and
  SKILL.ru.md (816 chars) — now names forests, peatlands, marine and
  coastal waters, urban ecosystems, deserts, tundra and cryosphere,
  cropland and livestock farms alongside the original domains;
  (b) the Deterministic Script I/O Schemas table moved out of SKILL.md
  into `references/scripts.md` (31 lines), with a short pointer left in
  SKILL.md and pointers in both Companion Documents lists — and the
  missing 17th row added in the move: `scripts/fetch_satellite.py`
  (the agreed morning fix of 2026-10-27, not yet applied; row written
  from the script's own `--help` and docstring). SKILL.md is now 469
  lines (was 491). New test T92 (`TestQuickFixesOct28`, 3 tests).
  NOT applied here (separate decisions, v2.9 scope): the model core
  (Vollenweider phosphorus balance, EnKF/particle-filter assimilation
  script), deseasonalised drift, bootstrap intervals for SS_RMSE, and
  PFAS / Igeo / PLI / Håkanson RI in the safety gate; the Stage/Phase
  dual numbering and the 32-domain scope question.

- **Remaining priority [NEXT DATA] gaps verified (T91, 2026-10-28)** —
  the three priority gaps are closed as verified negative results, not
  as values; nothing was invented. (1) Beira-local SS_RMSE for Sensors
  1–4: chlorophyll-a and water temperature exist in the published
  record only as interpolated supplement maps (Prasad et al. 2024,
  Figs. S7–S8 and S1–S2), with no per-station numeric table, and the
  paper never applied NDCI or Landsat surface temperature at Beira —
  so no local score can be computed from the published record; the
  water extent is a single surveyed total (about 65.4 ha), not a mask,
  so no mask accuracy can be derived from it; turbidity was never
  measured in situ at Beira, so a local score is structurally
  impossible. Each sensor now states its named next data (the authors'
  raw per-station values, or a new paired field campaign). One error
  corrected in passing: the file cited supplement "Figs. S7–S9" for
  chlorophyll-a, but the supplement list contains only S7–S8 (the main
  text cites a Figure S9 that is not in the supplement list).
  (2) Langtang InSAR ground truth: no GNSS or levelling watched the
  slope; the ICIMOD preliminary synthesis (13 October 2026) and the
  independent rapid assessment (Roy et al. 2026, J. Indian Soc.
  Remote Sens., DOI 10.1007/s12524-026-02611-x, published 16 October
  2026) are satellite-only — NISAR SBAS InSAR and pixel-offset
  corroboration is cross-sensor agreement, not ground truth — and the
  pre-collapse deformation can never be scored retrospectively because
  the slope collapsed. A non-peer-reviewed preprint (Sah 2026,
  EarthArXiv) finding no precursor in Sentinel-1 amplitude data is
  recorded as a caution, not as evidence. Next source: a GNSS
  installation or drone-DEM survey on neighbouring at-risk slopes.
  (3) Daursky marmot density (ind/ha): still unpublished and still
  [NEXT DATA] — Bazhenov 2019 gives families and adults, not density
  per hectare, and no occupied-colony area. Published context added,
  labelled as not a Daursky value: tarbagan densities across the
  species' range are 1–7 ind/ha (IUCN Red List species account, Zenodo
  record 6819035); Hustai National Park comparator ca. 1.27 ind/ha
  (13,213 marmots on 10,380 ha, Todgerel 2020, as cited in the
  marmot-decline literature — a secondary citation, to be verified
  against Todgerel 2020 before use as a value). Next source: the
  reserve's «Летопись природы» / DIPA joint-expedition counts
  (families plus occupied colony area). Updated in
  `references/worked-examples-new-sections.md` (Sensors 1–4, 6, gaps
  section, Dauria panel), `references/sensor-registry.md` (S1–S4, S6,
  rows R02–R04, R09, R12, §6), `references/indicators.md` (§22 marmot
  row, Dauria note, §21 InSAR row — no "[provisional]" used there, per
  T81), and `references/sources-new-sections.md` (§21 Roy/Sah bullets,
  §22 marmot addendum, virtual-sensor verification note). New test T91
  (`TestRemainingNextDataGapsVerified`, 6 tests). SKILL.md unchanged.

- **Thresholds source guide applied (T90, 2026-10-28)** — the draft
  `~/workspace/ecosystem-twin-thresholds-guide-DRAFT.md` is applied to the
  candidate as `references/thresholds.md` (358 lines): 20 indicators, 5
  jurisdictions (WHO, EU, USA, Russia, Japan), with the anchor hierarchy
  (jurisdiction law → WHO → literature → object baseline; the stricter
  governs red), thresholds by use (§7: drinking / bathing / irrigation /
  aquatic life — status by the strictest active use, named on the status
  line), and the operational early-warning level (§8: yellow at 70–80% of
  the regulatory limit, red is the limit itself). The body is carried over
  verbatim from the draft — only the status header and closing line changed
  — so all 21 [provisional] marks are preserved and stay visible; every
  [provisional] value must be re-checked against its primary source before
  it enters an Object Passport as final. Russian lead in drinking water is
  NOT entered as a value (sources contradict 0.03 vs 0.01 mg/L; §10 item 2).
  The 14 open items (§10) are kept as [NEXT DATA]. Rules, not per-country
  values, are wired into the skill: SKILL.md Stage 1 (anchor hierarchy +
  per-use thresholds + early-warning level), Stage 6 (decision support —
  the twin shows the picture, the decision and responsibility stay with the
  decision-maker, ЛПР — `references/thresholds.md` §9), and a Companion
  Documents pointer (SKILL.md now 491 lines by `wc -l`, 492 by the lint's
  count, under the 500 limit; same pointer mirrored in SKILL.ru.md);
  `references/indicators.md` §19 (pointer to the guide) and §20 (three new
  rules: anchor hierarchy, thresholds by use, operational early-warning
  level). No per-country value was hard-coded into SKILL.md; no value was
  invented. New test T90 (`TestThresholdsGuideApplied`, 8 tests). One
  defect found by the suite and fixed in the round: the §19 pointer first
  used the word "[provisional]", which T81 forbids in `indicators.md` —
  reworded to "an anchor flagged in that file stays flagged". Loop score
  9/10, one round.

- **Both [unverified] flags closed (T89, 2026-10-28, on her word "Заверши 2 пометки")** — no live [unverified] flag remains in the catalogue. (1) §22 marmot-density threshold: closed as a verified negative result — no standardised density threshold exists (IUCN criteria use decline rates, extent and mature-individual counts, not density; the Russian 1983 census guidelines are a survey method). The row now uses the object's own baseline with trend over ≥3 survey rounds; status context: tarbagan Endangered (IUCN A2ad), bobak Least Concern; restoration-design minimum ≥10 families / ≥50 individuals (Enkhsaikhan et al. 2021, Proc. Inst. Biol. 37:30–36, DOI 10.5564/pib.v37i1.3137); plague-risk cut-point 0.63 marmots/ha (Xu et al. 2023, Sci. Rep. 13:11906, DOI 10.1038/s41598-023-38966-1). (2) §26 green space per capita: closed — the 9 m² figure is Italian planning law D.M. 1444/1968 (2 April 1968: 18 m² public space, 9 m² public greenery per inhabitant, new settlements), verified via Land 2024, 13(12):2174; it is not a WHO figure (Czesak & Różycka-Czas 2025, DOI 10.1016/j.landurbplan.2025.105301, searched the cited WHO reports and found it in none; Mostafa & Alshahrani corrigendum 2025, DOI 10.3389/frsc.2025.1542464, 3 April 2025, deleted the WHO attribution). WHO's verified guidance is accessibility — 0.5–1 ha within 300 m (WHO Regional Office for Europe 2017 brief, rule of thumb). Updated in `references/indicators.md` (both rows + §26 note) and `references/sources-new-sections.md` (§22 note, §26 item (a), §26 verification note). The thresholds-guide DRAFT carries no 9 m² claim, so it needed no edit. SKILL.md / SKILL.ru.md carry no mention of either flag, so they are unchanged. New test T89 (`TestUnverifiedFlagsClosed`, 3 tests) + the T81 flag test re-pinned to assert closure.

- **Sensor registry (T88, 2026-10-28)** — `references/sensor-registry.md`
  (315 lines): every open source in `references/data-sources.md` mapped
  to the ecosystems (§§1–32) and indicator rows it serves, in four tiers
  — Core 1, Conditional 35, Research 3, Context-only 20; 59 rows
  (R01–R59) plus Part A carrying the seven registered virtual sensors
  verbatim (six named: five Beira, one Langtang — S1–S6 — plus the
  Object Passport "Virtual sensors" block as the reusable seventh form;
  no seventh sensor invented). Only one row is Core (R05, Secchi depth
  at Beira, RMSE 0.049 m, Prasad et al. 2024) — the registry shows, per
  row, what is measured and what is still only a method. Eight new
  sources added to `references/data-sources.md` §12 with resolution,
  cadence, access and measurement-vs-model notes: NASA FIRMS, Global
  Forest Watch / Hansen (user's accuracy 87.0% for loss), ESA
  WorldCover (overall accuracy 74.4%, 2020), OpenStreetMap, GPM IMERG,
  SMAP (ubRMSE 0.038 m³/m³ surface, Reichle et al. 2017), Copernicus
  Marine Service / OSTIA, WDPA / Protected Planet (with the
  Russia-data restriction caveat). No formula, score, or calibration
  station invented anywhere: every numeric score carries its citation,
  and every missing score is [NEXT DATA]. Loop score 9/10, one round
  (evaluate → self-check → correct → score).

Nine new domain sections in the indicator catalogue (`references/indicators.md`
§21–§29), assembled from the nine module drafts of 2026-10-27, each looped to
9/10 by self-check (self-check → correct → score) before assembly, plus §30
Forest (2026-10-28, looped to 9/10 by the same protocol), §31 Cropland
(2026-10-27, looped to 9/10 by the same protocol) and §32 Non-peat wetlands
and marshes (2026-10-28, looped to 9/10 by the same protocol) — twelve new
sections in all. One new script (`scripts/fetch_satellite.py`, automated satellite fetch,
2026-10-28); no new gallery entries — the catalogue grows; the machinery is
otherwise unchanged. The catalogue now holds 32 sections and 411 indicator
table rows (185 existing + 226 new), of which 348 are distinct indicators:
163 new, 63 cross-references to existing sections.

- **§21 Cryosphere and mountain hazards** — 14 rows (10 new, 4 cross-references
  to §1/§3/§4): slope displacement by InSAR, displacement rate and acceleration,
  glacier velocity, glacier area/terminus/thinning, glacial lake level/area/volume,
  moraine-dam stability, river damming / barrier-lake watch, permafrost ground
  temperature, air temperature at glacier elevation, micro-seismicity.
- **§22 Steppe and natural grassland** — 17 rows (14 new, 3 cross-references to
  §9/§10/§11): steppe vegetation composition and PFT shares, forage biomass,
  stocking rate and grazing utilisation, SOC in steppe soils, erosion features,
  LFA indices, virgin-steppe area and conversion, shrub encroachment, post-fire
  recovery, steppe birds, burrowing mammals, grasshopper/locust outbreaks, SDG
  15.3.1 degraded-land composite.
- **§22 worked-example reframe** (2026-10-28) — the steppe worked example is
  reframed as the Daurian steppe example with the Mongolian side /
  transboundary UNESCO "Landscapes of Dauria" framing; the Daursky State
  Nature Biosphere Reserve is the Russian-side component of the property,
  not the example's subject. All published values and gaps unchanged
  (gazelle June 2020: 18,898 counted / 21,701 estimated, Buuveibaatar et
  al. 2024; tarbagan 3,300–4,100 families, Bazhenov 2019; [NEXT DATA] gaps:
  Daursky-reserve-only gazelle total, current marmot density, burned area,
  SOC). Applied in `references/worked-examples-new-sections.md`,
  `references/indicators.md` (§22 summary line) and the steppe draft
  `~/workspace/ecosystem-twin-steppe-section-DRAFT.md`, per her correction
  of 2026-10-27.
- **§23 Livestock farm as an ecosystem** — 18 rows (11 new, 7 cross-references
  to §5/§8/§9/§10/§11/§14/§15/§17/§22): manure production, farm N/P nutrient
  balance, manure storage capacity and freeboard, manure application, ammonia
  and methane fluxes, nitrous oxide, farm water use and effluent, slurry-lagoon
  integrity, livestock stream access, soil compaction under grazing.
- **§24 Peatlands and bogs** — 15 rows (14 new, 1 cross-reference to §4): peat
  extent and depth, peat carbon stock, water-table depth in peat, drainage
  status, Sphagnum cover, peatland vegetation composition, net GHG flux from
  peat, peat fire, subsidence, extraction, rewetting state, peatland condition
  class, paludiculture, peat fire risk (Research).
- **§25 Marine and coastal** — 24 rows (17 new, 7 cross-references to
  §4/§6/§11/§12/§14/§15/§16): SST and marine heatwaves, Degree Heating Weeks
  and bleaching alert levels, estuarine salinity gradient, tidal level and
  sea-level trend, seawater pH, aragonite saturation, live coral cover,
  bleaching prevalence and mortality, coral recruitment and disease,
  crown-of-thorns density, reef structural complexity, mangrove extent, seagrass
  extent/cover/density, shoreline position and erosion rate, underwater noise
  (Research).
- **§26 Urban ecosystems** — 22 rows (13 new, 9 cross-references to
  §1/§3/§4/§6/§9/§10/§11/§14/§15/§16): heat-island intensity (air and surface),
  impervious-surface share, combined-sewer / storm-water overflow frequency,
  duration and volume, green space per capita and accessibility, tree canopy
  cover and canopy equity, proportion of natural areas, artificial light at
  night, urban metabolism (water, energy and GHG, waste and wastewater).
- **§27 Aquaculture — fish farming** — 19 rows (19 new): dissolved oxygen,
  unionised ammonia and nitrite in the production unit, water temperature
  against the species optimum, mortality and disease incidence, sea-lice load,
  therapeutic treatments, eFCR, stocking density, effluent nutrient and organic
  loads, benthic sulphide/redox, receiving-water state against a reference
  site, escapes and estimated unexplained loss, wild-fish interaction, water
  abstraction, fallowing, operational welfare indicators (Research).
- **§28 Desert and arid lands** — 19 rows (8 new, 11 cross-references to
  §1/§2/§3/§8/§9/§11/§15/§17/§22): UNEP aridity index, climatic water balance
  and seasonality, soil-adjusted fractional vegetation cover, desert vegetation
  condition, rain-use efficiency, biocrust cover and function proxies, dune
  migration rate, oasis extent and water. The desertification extent row is a
  cross-reference to the §22 SDG 15.3.1 composite — the same indicator, not a
  second copy.
- **§29 Tundra and polar** — 17 rows (12 new, 5 cross-references to
  §1/§3/§10/§15/§17): tundra vegetation composition, shrubification,
  NDVI greening/browning, active-layer thickness, thermokarst features, SOC in
  tundra soils, GHG fluxes, caribou/reindeer, lemming/vole cycle, insect
  emergence timing, coastal erosion rate, post-fire recovery.
- **§30 Forest** (2026-10-28) — 21 rows (16 new, 5 cross-references to
  §9/§10/§11/§15): forest extent and net area change, forest type and biome
  composition (natural vs planted), primary and old-growth share, stand
  age-class distribution, basal area and stem density, aboveground biomass
  carbon, forest soil organic carbon, net carbon flux (NEE/NEP), harvest
  against the allowable annual cut, forest loss by driver, pest and disease
  outbreak, fragmentation, regeneration, understory condition, protected-area
  and certified-forest share; canopy/deadwood and fire regime per §10, tree
  health per §11; mast yield index (cedar nut and berry crops, Research,
  [NEXT DATA]). Worked example: Harvard Forest (sink 2.0 ± 0.4 Mg C/ha/yr
  1993–2000, hemlock stands net source after 2014). No [unverified] flags;
  [NEXT DATA] gaps named in the example (current canopy, deadwood, biomass
  stock, regeneration density, fragmentation).
- **§30 second worked example — Barguzinsky Reserve and the Buryatia taiga
  edge: human–brown bear conflict, autumn 2026** (2026-10-28, her decision
  of 27 October 2026, 22:10 EDT — an explicit exception to the
  "no Russian worked examples" rule, only with links to authoritative
  sources for every figure). Cross-reference rows in §15 (brown bear
  abundance, age structure of conflict animals), §17 (conflict reports,
  food attractants register, quota uptake and regulated removal) and §20
  (taiga-edge watch levels); one new §30 row (mast yield index, Research,
  [NEXT DATA]). Verified figures: Buryatia brown bears 6,113 (2026),
  6,276 (2025), 5,385 (2021), 4,625 (2011); density 0.21 per 1,000 ha;
  47 exits in all of 2025; regulated 149 (14 Sep), 331 (3 Oct), 436
  (20 Oct); 6 attacks, 2 dead, autumn 2026; harvest limit 1,272, about
  900 permits, about 300 harvested a year; reserve 374,322 ha, sable
  20–30 at creation → 1,500–2,000 today. Reliability caveat carried into
  the example: the Burprirodnadzor / Ministry of Natural Resources figures
  reach us as relayed by the press; the primary departmental summaries are
  not published openly. [NEXT DATA] gaps named in the example (current
  bear numbers in the reserve itself; quantitative mast index for Buryatia
  2026; wolf numbers; attractants register; numeric young-share; long-term
  attacks series).
- **§31 Cropland** (2026-10-27) — 21 rows (15 new, 6 cross-references to
  §5/§9/§10/§11/§14/§15): cropland extent and net area change, crop type and
  cropping-system composition, cropping intensity, crop rotation diversity and
  fallow share, tillage system share, SOC stock under tillage, irrigation water
  use and efficiency, soil salinisation (ECe trend, salt-affected share),
  fertiliser N/P balance and NUE, direct N₂O from fertilised soil, pesticide
  pressure, yield and yield stability, soil erosion on arable land (RUSLE),
  field-margin and biodiversity-strip share, crop residue fate and
  open-burning share, rice-paddy water regime and methane (AWD scaling
  factors); receiving-water nutrients per §5, soil per §9, landscape per §10,
  flora per §11, pollinators per §14, farmland birds per §15. Worked example:
  GEPIS rice paddies, Mayurapura, Hambantota, Sri Lanka (project target yield
  5.5–6.2 t/ha; Beira Lake WPI 2.4–2.5 against 1.0; national Maha ~2,853 kg/ha,
  Yala ~3,207 kg/ha). No [unverified] flags in the rows; [NEXT DATA] gaps
  named in the example (measured GEPIS yield, water use, CH₄/N₂O fluxes, SOC,
  ECe, margins, erosion). Russian material only as published-data anchors
  (Kursk chernozem SOC, Mikhailova & Post 2006; erosion, Plotnikova et al.
  2024) — no Russian worked example, pilot or showcase case, per her
  correction of 2026-10-27.

- **§32 Non-peat wetlands and marshes** (2026-10-28) — 19 rows (14 new, 5
  cross-references to §4/§9/§10/§11/§15): wetland extent and net area change
  (Ramsar definition; 35% lost 1970–2015, GWO 2018; 64–71% since 1900,
  Davidson 2014), wetland type composition, hydroperiod, water-level regime,
  salinity regime (coastal/brackish), vegetation composition (reeds, sedges,
  salt-marsh grasses), sediment accretion against local sea-level rise
  (organic matter at most ~3 mm/yr, Morris et al. 2016), nutrient retention
  (Olentangy: P ~60%, nitrate ~40%), soil carbon and GHG flux in
  mineral-soil marsh, waterbird use (Ramsar Criteria 5/6), fish nursery
  function (Beck et al. 2001), invasive species (Phragmites haplotype M,
  Saltonstall 2002; cattail expansion), drainage and reclamation pressure,
  restoration state (non-peat); water quality per §4, soil per §9,
  landscape per §10, flora per §11, fauna per §15. Worked example: the
  Everglades, Florida, USA (historic ~4,000 sq mi, just over half remains;
  hydroperiod classes 11+ / 9–10 / 3–7 months; TP criterion 10 µg/L;
  wading-bird nests 138,834 in 2018, ~3,500 in the 2025 drought season);
  regional case: Mongol Daguur, Mongolia (Ramsar site 210,000 ha; staging
  2,000 geese, 4,000 shelducks, 20,000 ducks, 7,000 coots, over 10,000
  gulls). No [unverified] flags in the rows; [NEXT DATA] gaps named in the
  examples (Everglades accretion, fish-nursery densities, intrusion,
  nutrient balance, sawgrass/cattail shares; Mongol Daguur hydroperiod,
  accretion, retention, reed area, fish densities, current bird count).
  No Russian worked example, pilot or showcase case, per her correction of
  2026-10-27 — Mongolia is the regional example instead; the Selenga delta
  material gathered during research is deliberately not used as an example.
- **§18 quick sets:** eleven new quick sets (Cryosphere / mountain, Steppe /
  natural grassland, Livestock farm, Peatland, Marine / coastal, Urban,
  Aquaculture, Desert / arid, Tundra / polar, Forest, Cropland), each checked against its
  section's table.
- **Honesty flags preserved:** the [unverified] flags from the drafts are
  carried into the catalogue (steppe marmot-density threshold; the 9 m²
  per-capita green-space figure as a WHO publication; the EU Regulation
  2024/1244 500 t aquaculture reporting threshold; a water-use benchmark per
  tonne of aquaculture production) and the [NEXT DATA] gaps from the worked
  examples (Daursky steppe, North Wyke Farm Platform, Toolik Lake tundra).
  The tundra human-pressure row carried the Liu et al. 2026 figures as
  provisional until the first-layer check verified them against the full
  text (DOI 10.34133/remotesensing.1062) — the flag is now removed; see
  the first-layer note below.
- **Brand and licence pending the author's decision:** the skill is named
  descriptively, "Ecosystem Digital Twin by Rigjita Baldanova"; the brand
  name (candidates ADIS and RB) is undecided. The licence stays CC BY 4.0 as
  in v2.7; the licence for v2.8+ (BY-ND pending the author's «да») is
  undecided.
- **Scope boundary:** each new section is a Conditional module, included
  only when its object is present, with interface discipline built in (the
  twin ingests external monitoring and hands warnings to the responsible
  authority; the decision is recorded in the Object Passport at Phase 1).

Verification: 230 tests pass (227 baseline + 3 new: T81); strict lint passes from a fresh copy installed as `ecosystem-digital-twin/`; SKILL.md 480 lines (lint count); BEIRA-F-001 untouched, chain verifies.

**Loop-evaluation round 1 (2026-10-27, candidate only):** independent re-check of the assembly found and fixed 3 defects. (1) The §27 aquaculture table arrived hard-wrapped: 11 of its 19 rows spanned several physical lines, splitting the table into 12 fragments in strict Markdown rendering. All rows joined to single lines; row counts unchanged; a new regression test in `TestNewSections` (now 4 tests) pins each §21–§29 table as one contiguous block. (2) §25 DHW row overstated the NOAA wording ("reef-wide bleaching" at Alert Level 1) — corrected to NOAA's "bleaching likely" (Level 1) and "bleaching with mortality likely" (Level 2). (3) The green state was unnamed and the public status line had no traffic-light field: §20 now names green explicitly (no band breached = measures working; amber = measures insufficient; red = measures failed or acute risk), `assets/templates.md` §10 gains Status (green / yellow / red) and Recommendation fields, and SKILL.md Stage 6 names the colour and the recommendation in the status-line description. Verification after the fixes: 231 tests pass (230 + 1 new); strict lint passes; SKILL.md 480 lines. Round 2 self-check found one drift: the SKILL.md status-line wording had no mirror in SKILL.ru.md — mirrored (green / yellow / red + recommendation); re-verified 231 tests pass, lint passes, SKILL.md 480 lines, SKILL.ru.md 526 lines.

**First-layer improvements (2026-10-27, candidate only):** (1) The worked examples and full source lists from the nine module drafts now live in the candidate as `references/worked-examples-new-sections.md` (355 lines: 9 examples) and `references/sources-new-sections.md` (1,423 lines: 9 source lists), copied verbatim from the drafts — the drafts' self-check logs are not carried over, as they are process records, not sources. Both files carry a `## Contents` list near the top (required by the package lint for references files over 100 lines). SKILL.md and SKILL.ru.md point at the two files in the Companion Documents list and in the "New in v2.8" paragraph, and the stale "19-section" catalogue count is corrected to 29 in both. A new regression test in `TestNewSections` (now 5 tests) pins the two files' presence, contents and flags. (2) `assets/templates.md` §10 gains a filled public-status-line example in plain words: a Delhi resident asks "Can I go outside today? What are we breathing?" — status red, recommendation in ordinary words; a format example only, no numbers invented. (3) The Liu et al. 2026 tundra figures are verified against the full text of the paper ("Anthropogenic Disturbance Dampens Climate-Driven Greening in the Arctic", J. Remote Sens. 6, 1062, DOI 10.34133/remotesensing.1062; eight authors: Liu, Wang, Zhang, Zhang, Dong, Liu, Li & Cheng; published 5 August 2026): 2,221 clusters, 21,402 km² (435 settlement — 12,902 km²; 1,786 non-settlement — 8,500 km²), 2000–2020, Landsat 5/7/8 Collection 2 Tier 1, 30 m, 16.1%. The provisional flag is removed from the §29 row, the tundra draft's table row, entry and verification note (a dated addendum records the change in the draft's self-check log; the Round 1 log is left as the historical record). The earlier press-release title and two-author form are corrected wherever they appeared. Verification after the changes: 232 tests pass (231 + 1 new); strict lint passes; SKILL.md 482 lines. Nothing published: the live skill and GitHub are untouched.

**Bozkurt worked example (2026-10-27, candidate only, on her word):** a second worked example for §21 — the Bozkurt–Ezine flash flood, Western Black Sea, Türkiye, 11 August 2021 — added to `references/worked-examples-new-sections.md` (now 364 lines, 10 examples) with its sources in `references/sources-new-sections.md` under §21 (now 1,431 lines). Casualty, rescue and rainfall-total figures verified against the peer-reviewed Natural Hazards paper citing AFAD 2022b (82 died, 364 medical support, 2,483 rescued, Bozkurt 453 kg/m²); intensity and return-period figures from the Kastamonu University NbS4LD case study, verified against the document itself on 27 October 2026 (the case study states 77 lives for the watershed flood vs AFAD's 82 for the event as a whole — the discrepancy is recorded in the sources file); channel narrowing from AP reporting of geologists. The T81 regression test is unchanged (one counted example per section; the Bozkurt example carries a distinct heading). Verification after the change: 232 tests pass; strict lint passes; SKILL.md 482 lines.

**Second-layer flag check (2026-10-28, candidate only):** all 4 [unverified] flags and all 3 [NEXT DATA] gaps re-checked against primary sources by four parallel researchers. Closed: EU 2024/1244 500 t threshold — confirmed against Annex I row 7 (production capacity, strictly exceeding 500 t), with the correction that N/P reporting is triggered only above the Annex II thresholds (total N 50,000 kg/yr, total P 5,000 kg/yr to water); water-use benchmark — closed as a negative result with verified per-type throughput ranges (raceways 16,000–42,000 m³/t; flow-through salmonids 22,000–95,000; fishponds 1,200–10,000; shrimp ponds 20,000–100,000; cages ~0.75; RAS total 300–800, make-up 0.15–5 m³/t) and the rule that throughput and make-up water are separate quantities. Daursky: gazelle (Daursky + Dzeren Valley, June 2020: 18,898 counted, 21,701 estimated) and marmot family counts (SE Transbaikalia 3,300–4,100 families; Daursky buffer 75–85, reserve ~30) closed; reserve-only gazelle total, current marmot density, burned area and SOC stay open. North Wyke: N balance (Carswell et al. 2019), housed-cattle enteric CH₄ 170–174 g/day (Meo-Filho et al. 2023) and NH₃ pad rate 2.5 g m⁻² d⁻¹ (Dumont et al. 2012) closed; P balance, whole-platform CH₄ total and measured whole-farmlet NH₃ flux stay open. Toolik: shrub cover (+132.3%, 1990→2023), active layer (28–52 cm, no trend), caribou (Central Arctic Herd 26,600, July 2025), SOC (5–25 kg C m⁻²) and fluxes closed; lemming densities stay open (NEON dataset is the next lead). Staying flags, both with documented negative checks: marmot density threshold (no standard exists) and the WHO 9 m² figure (Czesak & Różycka-Czas 2025 confirms no WHO publication contains it). Tests updated: test_unverified_flags_preserved now pins the two remaining flags and the closed content; test_worked_examples_and_sources_present now pins the closed values and the remaining lemming gap. Files now: worked-examples 345 lines (10 examples), sources 1,404 lines. Verification after the changes: 232 tests pass; strict lint passes; SKILL.md 482 lines. Nothing published: the live skill and GitHub are untouched.

**Automated satellite fetch (2026-10-28, candidate only, on her word):** new `scripts/fetch_satellite.py` (stdlib-only network/STAC: `urllib` + `json`; NDVI computed via optional `rasterio`/`numpy`, deferred with an honest note when absent). Searches the Planetary Computer STAC API (no key; collections `sentinel-2-l2a`, `landsat-c2-l2`, `sentinel-1-rtc` — verified live 2026-10-28) and the Copernicus Data Space STAC (account + token for download; unreachable from this environment 2026-10-28 — verify at build time). Modes: `--check` (search only, no download), `--download` (red/NIR bands of the least-cloudy scene), `--compute-ndvi` (NDVI statistics on a 512×512 preview; zero denominator recorded as no measurement, never as 0), `--stac-file` (offline on a recorded response). Every run writes a dated manifest with source, collection, bbox, dates and retrieval date (§19) and registers the product as a virtual sensor in the Object Passport. Exit codes: 0 ok; 2 usage error; 3 catalogue/network/auth failure — a failure is loud, never silent. `references/data-sources.md` gained a section on the script and a latency-honesty table (Sentinel-2 ~5 days, Sentinel-1 6–12 days, Landsat 16 days, MODIS/VIIRS daily; ground telemetry is the only real-time layer — a satellite is a periodic snapshot, never real-time). SKILL.md gained three pointers (compatibility note, "New in v2.8", Stage 2). New tests: `TestFetchSatellite` (T82, 8 tests, offline on a recorded STAC response). Live smoke test 2026-10-28: `--check` over the Langtang bbox (85.5,28.2,86.0,28.5, August 2026) returned 3 Sentinel-2 scenes with B04/B08 asset links; the scenes were 82–89% cloud — the monsoon season, and the default `--max-cloud 20` correctly keeps none of them. Verification after the changes: 240 tests pass; strict lint passes; SKILL.md 483 lines. Nothing published: the live skill and GitHub are untouched.

**Registered virtual sensors — Variant B (2026-10-28, candidate only, on her word):** the first real registrations in the skill: six virtual sensors in the Object Passport form, as a worked example in `references/worked-examples-new-sections.md` (now 576 lines, 11 examples) with full sources in `references/sources-new-sections.md` (now 1,511 lines). Beira Lake, Sri Lanka (Prasad et al. 2024, Water 16(11), 1616): Sentinel-2 chlorophyll-a by NDCI (Mishra & Mishra 2012: Chl-a = 194.325·NDCI² + 86.115·NDCI + 14.039; published RMSE 1.43 µg/L for Chl-a < 30 µg/L; Molkov et al. 2019: 3.02 µg/L); Landsat 8/9 water surface temperature by the USGS Collection 2 split-window product (Gerace et al. 2020; published RMSE 0.87 K L8 / 0.74 K L9, Eon et al. 2023); water surface extent by MNDWI (Xu 2006; JRC Global Surface Water validation: under 1% false water, under 5% missed, Pekel et al. 2016); turbidity by Dogliotti et al. 2015 (A^T 228.1/3078.9 FNU, C^T 0.1641/0.2112; published RMSE 20.5 FNU, n = 106); Secchi depth by the Lee et al. 2015 QAA model — the one Beira-local published skill score: RMSE 0.049 m, R² = 0.670, n = 43 (Prasad et al. 2024, §3.3.3). Langtang slope: Sentinel-1 InSAR displacement (up to 40 cm in 48 days, ICIMOD 2026; published accuracy anchors ±10 mm vs levelling/GNSS, and formal ~1.2 mm vs actual 13.8/17.2 mm error budget). Honest gaps, all named: Beira-local SS_RMSE for chlorophyll-a, temperature, extent and turbidity; a Beira-local chlorophyll-a calibration above 30 µg/L; Langtang ground truth; no in-situ turbidity exists in the published Beira record. Step 1 (Variant A folded in): Sentinel-1 and Open-Meteo added to `references/data-sources.md` (satellite table, atmosphere table, forecast-weather stream). New test T83 (`TestRegisteredVirtualSensors`, 3 tests). Verification after the changes: 243 tests pass; strict lint passes; SKILL.md 483 lines (unchanged — no SKILL.md edit was needed). Nothing published: the live skill and GitHub are untouched.

## v2.7 — 2026-10-26

The release of the whole v2.7 program (one version at the end, per the
author's decision of 2026-10-26). The package was built and verified in
staging only; this entry assigns the version.

- **32 second-wave functions in four rounds** (all approved by the author
  in topicality order, "Все по порядку, начиная по актуальности"): Round 1
  impacts-and-extremes + trust (impact chain, event storyline,
  historical-event replay, stochastic scenario generator, HQ/HI,
  covariate-aware alerts, alert trial, calibration plausibility gate);
  Round 2 coverage-and-delivery (virtual sensors, drift/connectivity,
  daily forecast bulletin, public status line, one product per audience,
  asset safety margin, user-class thresholds, exposure inventory);
  Round 3 forecast-quality + biodiversity (hindcast reproduction gate,
  skill-vs-lead-time curve, observation-nudged forecast,
  phenomenon-oriented metrics, diversity indices, PFT shares,
  trait–environment matching, spread-informed sampling priority);
  Round 4 governance-and-depth (sensitivity-first calibration, model
  ladder, adaptation appraisal + equity + M&E, driver-perturbation
  table, mismatch register, promotion record, semantic mapping set,
  "Valid use / out of scope" field). New scripts: `scenario_generate.py`,
  `drift.py`, `forecast_bulletin.py`, `diversity.py`, `trait_match.py`,
  `sensitivity_screen.py`, `mismatch.py`; new `registry.py promote`
  subcommand; new `mappings` entity type in `build_manifest.py`.
- **Ellenberg trait-table correction:** the field gallery entry's
  `trait_table.csv` was checked against the published Ellenberg values
  (Tichý et al. 2023, Zenodo 7427088) and did not match — only 14 of 40
  values. The table was replaced with the corrected values (7 taxa; "x"
  where Ellenberg is indifferent; Triticum aestivum removed — Ellenberg
  does not list cultivated wheat); `trait_match.py` gained the
  indifferent rule.
- **Audit-fix patch, Variant 1 + Variant 2:** an external model's
  line-by-line audit of the candidate was verified against the files and
  its findings fixed — the SKILL.md I/O table now describes all 16
  scripts; Core Mathematical Specifications grew from 6 to 12 formulas;
  the alert trial gains a third verdict INCONCLUSIVE_QUIET_WINDOW; the
  admit gate requires SS_RMSE > 0 only for PRIMARY target variables;
  the Tier S / M / L gradation is stated at the head of the 7-stage
  cycle.
- **Laguna borrowing patch (patterns only):** four patterns adapted from
  the Agricultural Digital Twin Platform (Laguna et al. 2025, Computers
  in Industry 172, 104347, DOI 10.1016/j.compind.2025.104347, MIT
  license) — three-zone file ingestion (landing → trusted → refined),
  twin-to-twin notifications, a per-twin workspace layout, and four
  named open-data ETL streams for the field twin. No code copied, no
  stack adopted, no ML approach taken.
- **Definition correction (author's decision):** the skill IS a digital
  twin of ecosystems — that is its definition (SKILL.md opening, README).
  The "(the consulting traffic light)" label on the Tier S / M / L
  header was removed; consulting stays only where it belongs, as one of
  the two USES (a consulting product for a client, and a research
  instrument), not as the skill's identity.
- **Affiliation removed (author's decision: the latest version carries
  no affiliation):** the `affiliation:` line is removed from
  CITATION.cff. The author (Rigjita Baldanova) and ORCID are unchanged.
  The CHANGELOG's historical v2.3 DOI record was reworded to carry no
  affiliation.
- **Professional README (EN + RU):** a detailed "Ecosystems covered"
  section (ponds and lakes, river reaches, wetlands, agricultural land,
  forests, air basins, biodiversity, contaminated soils, linked
  multi-ecosystem cascades — each with its gallery proof or real-data
  case), a Keywords list (14 GitHub topics), an Author section, the
  scripts table completed to all 16 scripts, and stale version
  references corrected (test count 227, tests T1–T80, citation v2.7).
- **Verification:** 227 tests pass; strict lint passes from a fresh copy
  installed as `ecosystem-digital-twin/`; SKILL.md 477 lines. The
  CITATION.cff DOI is still the v2.3 record (10.5281/zenodo.23657185)
  until the Zenodo release mints a new one; a DOI-update PR follows
  (as with v2.3).

## Round 4 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 4 is the governance-and-depth batch — the LAST round of
the program, the 8 functions the author approved fourth ("Все по
порядку, начиная по актуальности", 2026-10-26), in topicality order:

- **Sensitivity-first calibration (Gironde):** a *sensitivity screen*
  step in Stage 3 — new `scripts/sensitivity_screen.py`, perturbing each
  model parameter one at a time (±10% or a stated range) and recording
  the change in the output metric as a ranked table; the honest limit is
  stated in the script, SKILL.md Stage 3 and `assets/templates.md` §1:
  one-at-a-time misses interactions, unlike Sobol.
- **Model ladder (Digital Baikal):** a "Model ladder" subsection in
  SKILL.md Stage 3 + a field in the Object Passport
  (`assets/templates.md` §1) — the fast model is admitted for SCREENING
  ONLY and must stay within a declared tolerance of the full model on
  the same hold-out. Governance + template, no computation.
- **Adaptation appraisal + equity + M&E (DestinE):** the scenario scoring
  in `references/scenarios.md` is extended (equity column + follow-up
  date) and the §4 Option card gains impact avoided, co-benefits,
  equity, and a follow-up check date + registry forecast ID; the impact
  avoided comes from the Round 1 impact chain. After implementation the
  twin re-scores the option against the predicted impact on a fixed date
  via `registry.py issue` — the same Brier-style discipline as
  BEIRA-F-001.
- **Driver-perturbation table (Southern Water):** a "sensitivity" block
  in the What-if Scenario form (`assets/templates.md` §8) and a
  subsection in `references/scenarios.md` — for each driver (rainfall,
  nutrient load, abstraction, land use) apply stated perturbations
  (+10%, +25%, −10%) and report the indicator change using the existing
  index functions. Plain arithmetic, no new script. Boundary stated in
  the docs: the sensitivity screen perturbs MODEL parameters, this table
  perturbs INPUT drivers — different questions, different tables, never
  merged.
- **Mismatch register (Patos):** new `scripts/mismatch.py` + a form in
  `assets/templates.md` §12 + a subsection in
  `references/uncertainty-decision.md` §3 — record where observed ≠
  modeled, the *extent* (fraction of observed flooded cells correctly
  predicted) alongside the level score, the inferred hidden cause as a
  [ГИПОТЕЗА]/[НЕТ ДАННЫХ] item, and the measurement that would confirm
  it. The register is the learning log, not a gate: the alert trial and
  the hindcast reproduction gate are pass/fail, the register explains
  *why* a validation was bad.
- **Promotion record (Gironde):** a `promote` subcommand in
  `scripts/registry.py` (hash-chained like every record, never scored) +
  a Promotion record section in the Object Passport template
  (`assets/templates.md` §1) + a one-line rule in SKILL.md Stage 3 — a
  model is operational only after a recorded promotion (promoted by,
  on, evidence: benchmark + hold-out score); without one it is
  exploratory.
- **Semantic mapping set (BioDT):** one `mappings.csv` per gallery
  dataset directory (local field → standard term + justification,
  SSSOM-style) + a subsection in `references/data-sources.md` §6 + a row
  in the Phase 1 data-onboarding checklist (`assets/templates.md` §1) +
  a `mappings` entity type in `scripts/build_manifest.py` (one MappingSet
  File per mapping file in the RO-Crate output, conforming to SSSOM).
- **"Valid use / out of scope" field (BioDT):** a field in the Object
  Passport template (`assets/templates.md` §1) — the decisions the twin
  is built for, and what it must NOT be used for. Template only, no code.

Templates are now twelve fillable forms (§12 is the mismatch register
entry). 21 new tests (T69–T76); the suite is 213 tests, all passing.

### Audit-fix patch, Variant 1 + Variant 2 (2026-10-26, before version assignment)

The author's decision ("Да, вариант 1+2: чинить текст и гейты"). An
external model's line-by-line audit of this candidate was verified
against the files by the author-side agent before any fix was applied
— two of its seven textual points were corrected, not applied as
written: the passport already carried the nudge-N and model-ladder
tolerance fields (only drift_threshold was genuinely missing), and the
maturity downgrade rule already existed in Stage 3; the auditor's
weighted score was 8.7, not 8.8 (0.25 × 34.8 = 8.70). What changed:
the I/O table now describes all 16 scripts; the passport gains
'Primary target variables' and a per-indicator 'Drift threshold' in
both the SKILL.md summary and `assets/templates.md` §1; Core
Mathematical Specifications gains formulas 7–12 (HQ/HI, Shannon /
Pielou / Delta+, KGE, nudge, drift with leeway, the Stage 7 drift
statistic); a maturity cross-walk in Template 1 with a cross-reference
in Non-Negotiable 2; the trend_test.py preamble lists all 6 modes; the
Companion Documents header drops '(retained from v2.2)'; the gallery
names match the `examples/gallery/` directories; YAML last-reviewed
2026-10-25 → 2026-10-26. Gates: `alert-trial` gains a third verdict
INCONCLUSIVE_QUIET_WINDOW (exit 0) for a window with no alerts and no
critical events — it neither admits nor rejects; critical events with
no alerts still FAIL. `admit` requires SS_RMSE > 0 only for PRIMARY
target variables (optional `primary` flag; no flag anywhere means every
variable is primary — the pre-2.7 behaviour). The Tier S / M / L
gradation is stated at the head of the 7-stage cycle, cross-referencing
the ten-step Tier S path in `references/quick-start.md` (unchanged).
NOT implemented here (separate decisions): the mandatory source_ref
column in reference tables, and the 'Executive VoI & Sunk-Cost
Summary' card. Suite now 219 tests (214 baseline + 5 new: T51 +2,
T52 +3), all passing.

### Laguna borrowing patch (2026-10-26, before version assignment)

The author's decision ("Сейчас", after the four prioritized items were
presented). Four patterns borrowed from the Agricultural Digital Twin
Platform (Laguna et al. 2025, "A platform to support the fast
development of digital twins for agricultural holdings", Computers in
Industry 172, 104347, DOI 10.1016/j.compind.2025.104347, MIT license) —
PATTERNS ONLY: no code was copied, none of its stack was adopted
(Docker / Temporal / MongoDB / Minio / MLflow / Go / SvelteKit), and none
of its ML approach (a Random Forest yield model validated on one eyeballed
point from explicitly fake data — that would violate this skill's Rule
#1). The platform itself was evaluated 2026-10-26 (product 7/10, fit
6/10); only the four patterns below transfer to a stdlib-only, laptop,
deterministic method for building digital twins of ecosystems:

- **Three-zone file ingestion (landing → trusted → refined):** a zones
  convention in SKILL.md Stage 2 — incoming files land untouched in
  `landing/`, QC-passed files move to `trusted/`, domain-converted
  model-ready files live in `refined/`; a file leaves `landing/` only
  after its QC is recorded, enters `refined/` only after its conversion
  is recorded in the build manifest — plus a file-zone field on the Phase
  1 onboarding checklist (`assets/templates.md` §1) and a zones note in
  the `scripts/qc_series.py` docstring (the script flags rows; it never
  moves or edits files).
- **Twin-to-twin notifications:** a step in SKILL.md Stage 7 — when an
  alert fires, the twin notifies its linked nodes (upstream and downstream
  twins); the notification is recorded on the trigger–action–response
  plan (`assets/templates.md` §3, new "Linked nodes notified" field), not
  in the forecast registry; a notified node re-checks its own alert bands
  on the next batch. No new registry entry type was added: a notification
  is a communication act on the TARP, not a forecast record, and adding
  it to the hash-chained registry would mix non-scorable communication
  into the forecast record for no audit gain.
- **Per-twin workspace layout:** one folder per object in SKILL.md
  Stage 2 — `common/` (passport, shared data), `etl/` (ingestion + QC),
  `calibration/` (models + admission), `forecasts/` (bulletins +
  registry), `simulations/` (scenarios) — cross-referenced from the
  build-manifest sentence in Stage 7 (the manifest records which file
  sits where). Laguna's layout carries an `ml-training` folder; this
  skill has no ML-training step, so the layout adapts it away (the
  absence is pinned by test).
- **Four named open-data ETL streams (field twin):** a subsection in
  `references/data-sources.md` §10 — daily weather (ERA5 by default,
  station truth where one exists), forecast weather (national meteo
  service / CAMS; never a substitute for observations in calibration),
  historical weather (ERA5 back to 1940 or the national archive; the
  hindcast window), NDVI (Sentinel-2, Landsat where Sentinel is missing,
  MODIS/VIIRS daily as the coarse context layer only) — with a one-line
  cross-reference from the field gallery README; the list lives in one
  place only. A stream that is unavailable is recorded as a gap in the
  [НЕТ ДАННЫХ] register, not silently replaced by another stream.

Deliberately NOT borrowed: the whole stack, real-time streaming
(MQTT/Benthos/Change Streams/SSE), any UI/map frontend, any ML yield
model, the pistachio-specific simulation (cold hours, tree counts). Suite
now 227 tests (219 baseline + 8 new: T77 2, T78 2, T79 2, T80 2), all
passing.

Author's correction (2026-10-26, same day): the skill IS a digital twin
of ecosystems — that is its definition (SKILL.md opening, README). The
label "(the consulting traffic light)" on the Tier S / M / L header was
removed, and "consultant's method" in this section was corrected to
"method for building digital twins of ecosystems". Consulting stays only
where it belongs: as one of the two USES (README: a consulting product
for a client, and a research instrument), not as the skill's identity.

### Ellenberg trait-table correction (2026-10-26, before version assignment)

The author's decision ("Да, исправь таблицу до v2.7"). The field
gallery entry's `trait_table.csv` was checked against the published
Ellenberg values (the Ellenberg column in Tichý et al. 2023, Zenodo
record 7427088) and did NOT match — only 14 of 40 values; the table was
largely reconstructed from memory. Fixed as one package: the table
replaced with the corrected values (7 taxa; "x" where Ellenberg is
indifferent; Triticum aestivum removed — Ellenberg does not list
cultivated wheat; Salicornia values are ssp. europaea);
`scripts/trait_match.py` gained the indifferent rule (a taxon with "x"
for a trait is not excluded by a condition on that trait, named in the
output's `indifferent` list; a cell that is neither a number nor "x"
is refused, exit 2); the three T67 expectation tests rewritten to the
corrected values (saline site S ≥ 8 fits only Salicornia europaea;
N ≥ 7 fits Trifolium by indifference and excludes Salicornia and
Puccinellia at N = 4; T within 6 ± 1 fits all 7 taxa, two by
indifference) plus one new test pinning the indifferent rule and the
malformed-cell refusal; provenance lines fixed in
`scripts/trait_match.py`, `references/indicators.md` §11, the
field-gallery README and the field `mappings.csv` justifications
(exact source + verification date 2026-10-26; citation aligned to the
edition the corrected table follows — Ellenberg & Leuschner 2010 via
Tichý et al. 2023, not the unchecked 1991 printing). The Round 3
CHANGELOG entry below still records what was built then, with the old
table; this note records the correction. Suite now 214 tests (213
baseline + 1 new), all passing.

## Round 1 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version. Round 1 is the impacts-and-extremes + trust
batch — the 8 functions the author approved first ("Все по порядку,
начиная по актуальности", 2026-10-26), in topicality order:

- **Impact chain (DestinE):** new "Impact chains" section in
  `references/scenarios.md` + an "Impact chain" field on the §6 scenario
  card (`assets/templates.md`) — driver → exposed asset → impact, with
  the published function, its source, its applicable range, and its
  limits per link. No new code: arithmetic on the existing scripts'
  outputs. Links with no published function go to the [НЕТ ДАННЫХ]
  register, never invented.
- **Event storyline (DestinE):** a "Storyline" class in the scenario
  taxonomy (`references/scenarios.md`, now four classes beside Scenario 0
  / Planning / What-if) + a "Storyline" field on the §6 scenario card
  (event, drivers changed, held fixed, impact scored). No new code: the
  replay runs through the existing scenario machinery.
- **Historical-event replay (Digital Baikal):** a "Replay" protocol in
  `references/uncertainty-decision.md` §5 + a `replay` subcommand in
  `scripts/registry.py`. Take a historical extreme, run the existing
  QC/trend/alert pipeline on the data up to the event (cutoff = last
  observation before the event, no peeking), and record whether and when
  the alert fired — lead time in days. A miss is recorded with no lead
  time, a finding not a failure to report. Replays are hash-chained like
  every record but never scored and carry no decision weight for a future
  event. No dated Beira extreme exists in the published record, so no
  replay entry is appended to the real Beira registry; the entry type is
  implemented and tested, and the first real replay entry is created when
  a twin with a dated historical extreme is built.
- **Stochastic scenario generator (Digital Baikal):** new script
  `scripts/scenario_generate.py` (stdlib `random`, fixed seed —
  deterministic) + a section in `references/scenarios.md`. Input: a
  driver series + its fitted distribution (mean, SD, lag-1 autocorrelation
  from the object's own data); output: N seeded scenario series feeding
  the existing trend/alert pipeline, so a What-if reports a distribution
  ("in k of N seeded years the watch turns red"). Every generated value is
  labelled a scenario draw, never a measurement.
- **Hazard quotient / hazard index (Digital Baikal):** new `--mode hq` in
  `scripts/trend_test.py` + a section in `references/indicators.md` §6
  beside WPI/TSI/HPI. HQ = exposure ÷ reference per stressor; HI = sum of
  HQs; 1 = the safety line; acute/chronic split. Covers any stressor (air,
  water, smoke, chemicals) on a 1-scale. Documented honestly: same
  quotient family as HPI, but HPI covers only metals in water on a
  100-scale.
- **Covariate-aware alerts (Southern Water):** `scripts/alert_bands.py`
  gains `--explained-by` — a watch breach is logged as "explained" (not
  alerted) when the driver series is itself beyond its own watch level in
  a sustained episode overlapping the breach's window; only unexplained
  breaches alert, set the status, and count for `--fail-on`. Deterministic
  (a band check on a named driver, no ML). Rule in
  `references/indicators.md` §20 + an "Alerts" field on the §6 scenario
  card.
- **Alert trial (Southern Water):** new `alert-trial` subcommand in
  `scripts/skill_scores.py` — scores the alerts on a hold-out window:
  precision (relevant / all alerts), miss rate (missed criticals / all
  criticals), alarm volume — with admission thresholds (precision ≥ 0.9,
  zero missed criticals, alarm count capped). No alerts in the window is
  a FAIL. Distinct from the existing admission (SS_RMSE > 0), which scores
  the model, not the alerts. Trial card on the §6 scenario card; a short
  paragraph in `references/uncertainty-decision.md` §3.
- **Calibration plausibility gate (lake platforms):** new `admit`
  subcommand in `scripts/skill_scores.py` + new
  `references/calibration-bounds.md` (published parameter ranges with
  sources). Admission requires (a) the model beats the naive benchmark on
  EVERY key variable claimed (SS_RMSE > 0) and (b) every fitted parameter
  inside its declared physical bounds; a fit outside the bounds is
  rejected even if SS_RMSE > 0, logged with the offending parameter. One
  line in SKILL.md Stage 3: the two admission gates (plausibility gate +
  alert trial), both must pass.

Tests T45–T52 added (33 new tests); 138 tests pass. SKILL.md 310 → 318
lines (cap 500).

## Round 3 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 3 is the forecast-quality-and-biodiversity batch — the 8
functions the author approved third ("Все по порядку, начиная по
актуальности", 2026-10-26), in topicality order:

- **Hindcast reproduction gate (EDITO):** a "Reproduction check" field on
  the §6 scenario card (`assets/templates.md`) + a Phase 5 rule in
  `references/scenarios.md` — run the scenario model on the historical
  window with the intervention switched off; the reproduced state must
  match the observations within a declared tolerance (the indicator's
  alert-band width or the calibration SD). A failed check means the
  scenario delta is reported as "unvalidated, direction only" — never as
  a number. Boundary stated in both `references/scenarios.md` and
  `references/uncertainty-decision.md` §5: the gate validates a scenario
  model, the replay verifies an alert. No new code.
- **Skill-vs-lead-time curve (lake platforms):** a `skill-horizon`
  subcommand in `scripts/skill_scores.py` (per-lead SS_RMSE against the
  naive baseline supplied per row) + a "Skill horizon" field on the §5
  forecast registry entry. The twin's report states the skill horizon —
  the longest lead at which the forecast still beats persistence with
  every shorter lead also above zero; a forecast is not trusted beyond
  it. A longer lead that beats the baseline after a failure is a
  non-monotone recovery — noise, not skill. Hand-verified: horizon 1
  (lead 1 SS_RMSE 0.5, lead 2 −2.0, lead 3 1.0).
- **Observation-nudged forecast (lake platforms):** a `nudge` subcommand
  in `scripts/skill_scores.py` — shift a raw forecast by the mean
  model-minus-observed residual over the last N QC-passed pairs (N
  declared in the Object Passport, e.g. 5). The correction is recorded in
  the registry entry (§5 form) and the nudged forecast is scored per lead
  time by `skill-horizon` like any forecast. The transferable principle
  of the Meteolakes ensemble Kalman filter, not the filter itself.
  Hand-verified: residuals all +2 → raw 15 nudges to 13.
- **Phenomenon-oriented metrics (EDITO):** a table in
  `references/analytics-forecasting.md` §4 and a "Phenomenon metrics" line
  on the §5 registry entry — 2–3 event metrics per phenomenon (bloom:
  onset-date, peak-magnitude, duration errors; flood: peak-level, timing,
  extent; fire season: season-start, peak-area, duration; drought/low
  flow: onset, minimum, duration; heat: exceedance-days, peak). Admission
  stays SS_RMSE; the metrics show the client's skill on the events that
  matter. A metric with too few events is [НЕТ ДАННЫХ], never zero. No
  new script.
- **Diversity indices (BioDT):** new script `scripts/diversity.py`
  (subcommand `indices`) — Shannon H′ and Pielou evenness from counts,
  plus Clarke–Warwick taxonomic distinctness Δ+ from the Linnaean
  hierarchy (same genus 1, family 2, order 3, class 4, phylum 5,
  different phylum 6). The skill had zero diversity indices. The
  biodiversity gallery runner now reports them (Khubsugul: Shannon
  2.8571, Pielou 0.9885, Δ+ 3.5098 — counts are records per species, a
  presence-only proxy, never abundance; the unidentified record
  contributes only at class level). Subsection in
  `references/indicators.md` §11, cross-reference in §15.
- **Plant functional type shares (BioDT):** `diversity.py pft` — shares
  from one quantity only (cover or counts, never mixed), from a PFT
  assignment table published per site (literature / TRY). Demonstrated on
  the field gallery entry (`pft_cover.csv` + `pft_table.csv`): grass
  0.82, legume 0.10, forb 0.08, C3 1.00; one season reports shares only, a
  trend needs repeat surveys. Subsection in `references/indicators.md`
  §11.
- **Trait–environment matching (BioDT):** new script
  `scripts/trait_match.py` — a deterministic filter over a published
  trait table per object (Ellenberg indicator values for the worked
  example in the field entry): "at_least" for tolerances (salinity,
  drought), "within" for optima (temperature, pH). A taxon fits only
  when EVERY stated condition is met. Hand-verified: a saline site
  (S ≥ 8) fits only Salicornia europaea and Puccinellia distans. The
  table is transcribed — verify it against the published source before
  client use. Subsection in `references/indicators.md` §11, line in the
  §18 Agriculture quick set.
- **Spread-informed sampling priority (lake platforms):** a
  `sampling-priority` subcommand in `scripts/uncertainty_budget.py` —
  rank the next sampling targets by |model − naive| (or |model A − model
  B|), ties by input order; sample the top target next. The old budget
  CLI is unchanged (dispatch on the first argument only). Rule in
  `references/uncertainty-decision.md` §2 — the value-of-information
  home (§4 is the counterfactual twin, not the sampling rule) — with a
  line on the §6 scenario card and a Stage 6 line in SKILL.md.
  Hand-verified: targets A (0), B (8), C (3) rank B, C, A.

## Round 2 of the v2.7 program (second-wave borrowing) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per function: the version inside the package stays 2.4
through the v2.7 program, and the whole verified program gets one
version (v2.7) at the end, when the author approves the complete
program. Round 2 is the coverage-and-delivery batch — the 8 functions the
author approved second ("Все по порядку, начиная по актуальности",
2026-10-26), in topicality order:

- **Virtual sensors (Gironde):** a "Virtual sensor" block in the Object
  Passport (`assets/templates.md` §1) + one line in
  `references/data-sources.md` listing satellite proxies as virtual-sensor
  sources. Name, physical quantity, proxy source + deterministic formula
  (the published satellite algorithm), calibration station + skill score
  against it (the existing SS_RMSE), validity window, and the same QC/alert
  machinery as a physical sensor. When the proxy leaves calibration, its
  readings go to the [НЕТ ДАННЫХ] register — never silently used. No new
  math (the proxy formula is the published satellite algorithm; the score
  is the existing SS_RMSE).
- **Deterministic drift / connectivity (EDITO):** new script
  `scripts/drift.py` (stdlib only) — deterministic advection of passive
  particles from a published current field (displacement = current velocity
  × time, plus a wind-leeway factor), reporting a connectivity matrix
  (fraction arriving in each target zone) and median travel time. Inputs:
  release points, current vectors transcribed as a table from a published
  current rose or Copernicus Marine values, target zones. The Plastic
  Tracker's "travel time" is an output of the same module (source →
  receptor). The skill's first transport function. Hand-verified: a
  constant 0.5 m/s eastward current at 50°N moves a particle 0.025152° of
  longitude per hour; 0.1° takes 4 steps; leeway 0.5 × 1.0 m/s wind halves
  the travel time to 2.0 h.
- **Daily forecast bulletin (Gironde):** new script
  `scripts/forecast_bulletin.py` (stdlib only) + a "Forecast bulletin" form
  in `assets/templates.md` §9. Reads a registry entry + the latest
  observation CSV and writes a one-page Markdown bulletin: observed value
  today, forecast value with interval and interval method, watch status of
  the latest observation and of the forecast value, and the date the
  forecast will be scored against its metric, exactly as issued. Trial
  forecasts carry a "Trial forecast — no decision weight" line. The
  bulletin renders the registry; it changes no numbers. No math changes.
- **Public status line (Southern Water):** a "Public status line" form in
  `assets/templates.md` §10 (one paragraph, plain language: current state,
  what changed, the maturity label, the [НЕТ ДАННЫХ] gaps — generated from
  the runner's summary JSON) + one rule in SKILL.md Stage 6: every twin
  ships one. For the client and the public — distinct from the handover
  note (for a successor builder, technical) and from RO-Crate (for
  machines).
- **One product per audience + dissemination register (Patos):** a
  "Decision product" form in `assets/templates.md` §11 (each product names
  its audience, its thresholds, its format, its channel, and its refresh
  cadence) + a "Dissemination register" block in the §1 Object Passport
  (who receives which product, by what channel). Template/governance only —
  no computation. The templates are now eleven fillable forms, not eight:
  the `assets/templates.md` header and the SKILL.md Companion Documents
  line both say eleven (two older tests that asserted "eight" were updated
  to the new count).
- **Asset-relative safety margin (Patos):** a clearance table in the
  Object Passport (`assets/templates.md` §1) + one line in the forecast
  registry entry (`assets/templates.md` §5) + a `--clearance
  "asset:threshold,..."` option on `scripts/registry.py issue`, which
  records per-asset clearance (threshold − forecast value) in the
  hash-chained record; `verify` rejects a record whose clearance does not
  equal threshold − value. Plain arithmetic, no new script. Generalizes
  beyond floods: clearance of a pollutant below its limit, of a level
  below a spillway crest, of a temperature below a lethal threshold.
- **User-class operational thresholds (Patos):** a `--class-thresholds
  FILE` option on `scripts/alert_bands.py` (CSV: class, limit — the
  operational limit in the indicator's units, same direction as the bands)
  + a rule paragraph in `references/indicators.md` §20 + an onboarding line
  in `assets/templates.md` §1 ("Decision-makers' operational limits (Phase
  1)"). The output gains a `class_thresholds` block: per class, the limit
  and whether the latest observed value and the episode peak are within it
  (`can_operate` is yes only when the class can operate now and could
  operate at the event's worst moment; with no alert episode the peak check
  is vacuous). A flooded road is passable for a pickup (0.45 m) while it is
  not for a car (0.30 m) or an ambulance (0.35 m) — the same water, a
  different verdict per class. Distinct from the per-asset clearance: the
  clearance is about an asset's margin; this is about who can do what.
- **Exposure inventory + exposed fraction (EDITO):** an "Exposure" block
  on the scenario card (`assets/templates.md` §6) + the exposed fraction
  added to the scoring rule in `references/scenarios.md` + a subsection
  "Exposure inventory and exposed fraction" after "Impact chains". Per
  scenario: the exposed elements (people, assets, habitats, intakes,
  cages) and the exposed fraction per class (exposed ÷ total in the zone),
  computed by table arithmetic from the hazard extent and the exposure
  inventory. The chain's Exposure link names who/what is in the hazard's
  path; the fraction quantifies it per class. A fraction with no inventory
  behind it is not a number, it is a guess, and goes to the [НЕТ ДАННЫХ]
  register.

Tests T53–T60 added (27 new tests); 165 tests pass. SKILL.md 318 → 325
lines (cap 500).

## Wetland first: the v2.6 program — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per item: the version inside the package stays 2.4
through the v2.6 program, and the whole verified program gets one
version (v2.6) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version. The missed natural systems are added in the
order the author approved: wetland, forest, bioreactor, soil
microbiome, steppe, estuary/delta, groundwater, pollinators, coast.

- Gallery re-location (author's decision, 2026-10-26: no Russian
  landscape in the gallery): the five gallery entries that modelled
  Russian landscapes were moved — four re-located to non-Russian ones,
  with new deterministic data, new published anchors, new READMEs, and
  updated tests (forest-fire and forest-carbon to the Prince Albert
  Forest Management Area, Saskatchewan, Canada; forest-logging to the
  British Columbia timber supply areas Prince George / Quesnel /
  Mackenzie; air to Prince George, BC), and the biodiversity entry
  (Gusinoye lakeshore birds, real GBIF data) REMOVED by the author's
  decision the same day ('Убери гусиное') instead of re-located: the
  GBIF pull for a replacement was blocked (HTTP 403) and must not be
  retried or bypassed, so the entry was removed; it was replaced the
  same day (see the next item), and the gallery now holds nine entries.
  The Baikal references in the METHOD
  (the multi-source fusion checklist, `references/data-sources.md`,
  the literature) stay — only the gallery miniatures moved. The GBIF
  sensitivity rules stay in the skill. Tests T40/T42/T43/T44 updated;
  104 tests pass.

- Biodiversity gallery prototype REPLACED (author's decision,
  2026-10-26, 'Замени другим биоразнообразие'; the site change to Lake
  Khubsugul is the author's own choice): the removed Gusinoye entry is
  replaced by Khubsugul lakeshore birds, Mongolia — Lake Khubsugul
  (Khövsgöl), approx 51.0 N, 100.5 E, Mongolia's largest freshwater
  lake and an Important Bird Area. Synthetic records (deterministic
  formulas; 20 records, 18 species, four shore points with jitter;
  one record unidentified, "Aves sp."). No real records are used: the
  GBIF occurrence-search pull was blocked (HTTP 403) and must not be
  retried or bypassed; a real-data version is possible later via a
  live-browser GBIF pull. Sensitivity categories are the real IUCN Red
  List statuses of the lake's birds (Emberiza aureola CR — coordinates
  withheld; Aythya ferina VU — pre-rounded to the 0.1-degree grid; the
  rest NT/LC — generalized by the runner). Design anchors: the eBird
  Khatgal hotspot checklist and the lake's best-known birds (Baikal
  teal, bar-headed goose, black stork, Altai snowcock). Results: 19
  generalized, 1 withheld, check gate pass, 0 violations, 18 species
  in 4 cells of 0.1°, at most 7 species in one cell. Maturity 2
  (Descriptive). The gallery now holds nine entries. Tests T40 (1 new
  test); 105 tests pass (104 baseline + 1 new).

- Professional stance block added to `SKILL.md`: the builder's working
  standard — domain depth, comparative view with transferability checks,
  evidence first, verification never overridden by seniority. No titles
  or publication counts are claimed.

- Wetland gallery prototype (first item of the v2.6 program):
  `examples/gallery/wetland/` — Everglades treatment wetland + marsh,
  real data: SFWMD STA-1W ATS pilot monthly influent/effluent TP
  (Aug 2008..Aug 2009; median removal 35.4%, mean 33.6% vs the
  document's stated 33.3% and the Beira reference median 46%) and
  USGS NWIS EDEN 10 daily gage height (2025-12-01..2026-03-31, 6.10 ft
  down to 5.26 ft, Sen -2.60 ft/yr). Outflow TP watch at the STA WQBEL
  levels (13/19 ug/L, applied as monthly watch levels); level watch
  at p10/p5 of the window (5.37/5.33 ft). Maturity 2 (Descriptive).
  No new math, no new indices, no fitting helper, stdlib only. The
  two series are different cells and periods of one system, stated in
  the README; a synchronous single-object record is [НЕТ ДАННЫХ].
  JRC Global Surface Water extent was checked and is unusable for a
  stdlib miniature (raster tiles / Explorer); water level is the
  drying signal instead. Tests T41 (2 tests); 99 tests pass (97
  baseline + 2 new).

- Forest-fire gallery prototype (second item of the v2.6 program):
  `examples/gallery/forest-fire/` — Prince Albert Forest Management
  Area (Sakâw Askiy), Saskatchewan, Canada, fire seasons, synthetic
  (deterministic formulas; design anchors from the Canadian
  Interagency Forest Fire Centre (CIFFC) and the Saskatchewan Public
  Safety Agency: Canada 2023, the national record, 18,496,051 ha
  burned; Saskatchewan 2023, 494 fires and ~1.9M ha burned; the FMA
  covers 3,354,418 ha, 2.7M ha forested): monthly fire counts and
  burned area, Apr-Oct 2019-2025 (49 rows). Both trends increasing
  (seasonal Kendall; counts p = 0.011, Sen +0.167/month per year; area
  p = 0.0012, Sen +210.2 ha/month per year); biggest season 2025
  (62 fires, 128,830 ha). Watches at declared levels (counts 11/13 per
  month, area 20,000/30,000 ha/month): 5 fires alerts (4 amber, 1 red)
  and 5 area alerts (4 amber, 1 red); amber episodes Jul-Aug 2019,
  2021, 2023, 2024; red episode Jul-Aug 2025.
  Maturity 2 (Descriptive). Real data were checked and found unusable
  (FIRMS Area API needs a MAP_KEY; public NRT files cover 7 days only;
  GFED/Global Fire Atlas/Copernicus are gridded products; no clean
  published monthly series for the FMA) — documented in the README.
  No new math, no new indices, no fitting helper, stdlib only. Tests
  T42 (2 tests); 101 tests pass (99 baseline + 2 new).

- Forest-logging gallery prototype (third item of the v2.6 program):
  `examples/gallery/forest-logging/` — British Columbia timber supply
  areas (Prince George, Quesnel, Mackenzie), synthetic (deterministic
  formulas; design anchors from the BC Harvest Billing System and the
  chief forester's AAC determinations: BC harvest 38.9 million m3 in
  2023, 39.0 in 2024, 37.7 in 2025; Interior 26.9 million m3 in 2023;
  Prince George TSA AAC 12.5 million m3, Quesnel TSA AAC 4.0 million
  m3, Mackenzie TSA AAC cut 18.4% in 2024; BC minimum harvest volume
  140 m3/ha): annual logged area and harvest volume, 2015-2025
  (11 rows; 17,900 ha and 3.44 million m3 in 2015 rising to 30,600 ha
  and 6.43 million m3 in 2025; 257,100 ha and 51.56 million m3 over the
  window). Both trends increasing (area p = 5.16e-05, Sen +1,220 ha/yr;
  volume p = 5.16e-05, Sen +272,750 m3/yr); Prince George is the largest
  every year (47.0% of the window total; Quesnel 31.0%, Mackenzie
  22.0%). Watches at declared levels (area 24,500/28,000 ha/yr; volume
  5.0/5.7 million m3/yr): 2 area alerts (1 amber, 1 red) and 2 volume
  alerts (1 amber, 1 red); amber episodes from 2022, red episodes from
  2024, both ongoing. Maturity 2 (Descriptive). Real data were checked
  and found unusable (GFW data API needs a key; dashboard and map pages
  are JavaScript-driven; Hansen/GLAD rasters need raster processing;
  the BC Harvest Billing System publishes provincial totals, not a
  ready annual series per timber supply area) — documented in the
  README. No new math, no new indices, no fitting helper, stdlib only.
  Tests T43 (2 tests); 103 tests pass (101 baseline + 2 new).

- Forest-carbon gallery prototype (third item of the v2.6 program):
  `examples/gallery/forest-carbon/` — Prince Albert Forest Management
  Area (Sakâw Askiy), Saskatchewan, Canada (2,700,000 ha forested —
  the same landscape as the forest-fire entry, so the three forest
  entries share one landscape and consistent disturbance years),
  synthetic (deterministic formulas; design anchors from UNEP boreal
  biomass 60-100 t C/ha with ~80% aboveground (Mahli et al. 1999;
  Luyssaert et al. 2007); Alberta boreal sequestration 0.5-2
  t C/ha/yr; fire losses from the forest-fire entry's annual burned
  areas plus stated interpolation for 2015-2018: 88,000 / 74,000 /
  82,000 / 91,000 ha): annual carbon density, 2015-2025 (11 rows;
  52.00 t C/ha rising to 53.92 t C/ha; total stock 140.40 Mt C rising
  to 145.58 Mt C, +5.18 Mt C, +3.7%). Density trend increasing
  (p = 2.62e-05, Sen +0.208 t C/ha/yr); net-change trend decreasing
  (p = 0.039, Sen -0.017 t C/ha/yr) — yearly growth is slowing as fire
  losses grow; smallest growth year 2025 (+0.04 t C/ha/yr). Only the
  net-change watch remains (amber at +0.15 t C/ha/yr or below, red at
  0.0 or below): 3 years below amber, 0 below red; 1 change alert
  (1 amber, 0 red), episode 2024-2025 ongoing. The low-density watch
  was removed: the series rises, so it is meaningless. Maturity 2
  (Descriptive). The README states the carbon-credit boundary: this
  entry watches carbon stock and its change; it is NOT a
  carbon-credit methodology and claims no compliance with any credit
  standard (Verra, Gold Standard, or other). Real data were checked
  and found unusable (ESA CCI Biomass is a raster product; GFW data
  API needs a key; FIA DataMart needs multi-table harmonisation and is
  US data; no open annual carbon-density series for one FMA) —
  documented in the README. No new math, no new indices, no fitting
  helper, stdlib only. Tests T44 (2 tests); 105 tests pass (103
  baseline + 2 new).

## Rounds 1–4 of the v2.5 program (borrowings) — unreleased draft (staging only, 2026-10-26)

PROPOSAL ONLY — not a release and not applied to the live skill. No
version is assigned per round: the version inside the package stays 2.4
through all rounds of the program, and the whole verified program gets
one version (v2.5) at the end, when the author approves the complete
program. The draft entry is written so the package lint still reads 2.4
as the current version.

- FAIR Signposting over RO-Crate (borrowed from BioDT):
  `scripts/build_manifest.py` writes FAIR Signposting relations
  (signposting.org) into the Root Dataset of `ro-crate-metadata.json` —
  `cite-as` (the package DOI from the build index, never invented),
  `describedby` (`ro-crate-metadata.json` itself), `license` (the index
  licence, when given as a URL). Documented in SKILL.md (Stage 7, I/O
  table). The package DOI in CITATION.cff is still the v2.3 record
  (10.5281/zenodo.23657185) until the v2.4 release mints a new one; the
  signposting `cite-as` uses the DOI given in the build index, not a
  value invented by the script.
- Scenario taxonomy beside Scenario 0 (borrowed from Southern Water):
  every scenario declares its class — Scenario 0 (No-Action
  counterfactual, unchanged), Planning scenarios (land use, development,
  catchment change), What-if intervention scenarios (the measures
  themselves). Added to SKILL.md (Stage 4) and `references/scenarios.md`,
  with a one-line pointer in `references/uncertainty-decision.md` §4 and
  a scenario-card template (`assets/templates.md` §6; the forms are now
  six, not five).
- Handover note: the Object Passport (SKILL.md Template 1) and
  `assets/templates.md` §1 record who maintains the twin after the author
  (name/role, handover conditions).

Round 2 — Recalibration trigger and continuous revalidation (borrowed
from lake hydrodynamic platforms and BioDT):
- Recalibration trigger: on each new QC-passed batch, `scripts/trend_test.py
  --mode drift --baseline <calibration series>` checks level drift
  (|mean(new) − mean(calibration)| / sd(calibration), firing at the
  per-indicator threshold declared in the Object Passport, default 2.0)
  and trend drift (the new batch's Sen slope outside the calibration
  slope's Gilbert confidence interval, reusing the trend-test machinery
  with no duplication). Either component fires the trigger: recalibrate
  (Stage 3 re-run), recompute alert bands, update linked nodes, and
  revalidate before the model can keep ADMITTED status. A fired trigger
  is a report (exit 0), not a failure. Documented in SKILL.md (Stage 7,
  I/O table) and `references/analytics-forecasting.md` §8.
- Continuous revalidation: `scripts/skill_scores.py revalidate` re-scores
  the admitted model on each new batch against the naive benchmark, with
  the original `--train-end` split (baselines from training data only, so
  the new batch never trains its own baseline). SS_RMSE ≤ 0 revokes
  ADMITTED (exit 3) and drops the twin's maturity label to the highest
  level the twin still meets, until a better model is admitted.
  Documented in SKILL.md (Stage 3, I/O table) and
  `references/analytics-forecasting.md` §8. Forecasts already issued are
  not re-scored or re-anchored.
- Tests (Rounds 1–2): T34 (FAIR Signposting in the manifest), T35 (taxonomy, scenario
  card, handover presence), T36 (recalibration trigger: level, trend, QC
  exclusion, input errors), T37 (revalidation: keep, revoke, missing
  split). Verification in staging: 87 tests pass (79 baseline + 8 new);
  strict lint passes from a copy installed as `ecosystem-digital-twin/`.

Round 3 — Two tiers, explainability, multi-source fusion (borrowed from
EDITO, Patos Lagoon, Digital Baikal):
- Two tiers: `assets/templates.md` gains §7 Focus application (for
  builders: purpose, object and nodes, inputs with manifest IDs, outputs,
  builder, maturity targeted, update cadence) and §8 What-if scenario
  (for decision-makers: the decision, options compared with scenario IDs
  and classes, evidence per option, recommendation, what would change it,
  decision-maker and date). The scenario card (§6) still records a single
  scenario; the What-if form frames the decision across scenarios.
  Documented in SKILL.md (Stage 6, Companion Documents); the forms are
  now eight, not six.
- Explainability under pressure: when a decision is made under pressure,
  the twin states in plain terms what the model used, what it did not
  use, and how confident it is — no black-box verdicts. Recorded on the
  scenario card (§6, "Explanation" field). Documented in SKILL.md
  (Stage 6) and `references/uncertainty-decision.md` §1.
- Multi-source fusion checklist: heterogeneous sources (space, aerial,
  ground, water) are fused in one scheme — one object, one time base, one
  spatial reference — with a per-source checklist: coverage, resolution,
  alignment, cross-source consistency checks, gaps → the [НЕТ ДАННЫХ]
  register. Extends the v2.4 onboarding checklist, never replaces it.
  Documented in SKILL.md (Stage 2, Object Passport template) and
  `references/data-sources.md` (new section; a Contents list was added
  because the file now exceeds 100 lines).
- Tests (Round 3): T38 (two tiers), T39 (explainability, fusion
  checklist). Verification in staging: 91 tests pass (87 baseline + 4
  new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`.

Round 4 — Prototype gallery (borrowed from BioDT):
- Five working miniatures under `examples/gallery/`, each a small data
  file + a `run.py` that reuses the skill's scripts + a README stating
  the management question, the maturity label, and the expected outputs;
  an index (`examples/gallery.md`) lists each entry with its question,
  data provenance, and maturity label. No new formulas, no new math,
  stdlib only. Lakes are already covered (Beira + Lake Primernoe) and
  the cascade by the existing dry-run, so the gallery does not duplicate
  them.
- Pond (synthetic): small-pond eutrophication — TP trend increasing
  (p = 0.0004), TSI composite 65.1 eutrophic, a calibrated model admitted
  on a declared hold-out (SS_RMSE 1.0 — near-perfect by construction,
  the series were generated from the fitted form), alert bands live.
  Maturity 3 (Informative).
- River reach (real): USGS NWIS, Potomac at Little Falls, 81 daily
  values 2026-08-01..2026-10-20, public domain — no significant trend,
  flood event 2026-10-12..20 peaking at 625.8 m³/s, red alert. No
  chemistry, so no WPI. Maturity 2 (Descriptive).
- Agricultural field (synthetic): soil-moisture watch — drying trend
  (p = 6.7e-16), 26 days below the irrigation watch level, red alert.
  Maturity 2 (Descriptive).
- Air basin (synthetic): Ulan-Ude winter PM2.5 — 12 days above the WHO
  daily guideline (45 µg/m³), 5 above the interim target (75 µg/m³),
  red episode 2026-01-16..19. Real CAMS data were checked first and
  found too coarse (1.8–17.1 µg/m³, zero days above 45); station data
  are [НЕТ ДАННЫХ]. Maturity 2 (Descriptive).
- Biodiversity site (real): GBIF, Gusinoye lakeshore birds, 20 records,
  CC BY-NC 4.0 — 18 species, 19 records generalized to the 0.1° grid,
  the one Critically Endangered record (*Emberiza aureola*) published
  with coordinates withheld, check gate pass. Maturity 2 (Descriptive).
  Synthetic entries are labelled synthetic in their READMEs and runner
  summaries and must never be cited as data.
- Tests (Round 4): T40 (gallery: five runners + index + SKILL.md
  reference). Verification in staging: 97 tests pass (91 baseline + 6
  new); strict lint passes from a copy installed as
  `ecosystem-digital-twin/`.

## v2.4 — 2026-10-26

Applied 2026-10-26 on the author's approval of the v2.4 proposal
(lead-time register + forecast cadence, Phase 1 data-onboarding
checklist). Local skill only; GitHub release and Zenodo DOI for v2.4
pending — CITATION.cff still names the v2.3 DOI
(10.5281/zenodo.23657185) until the release mints the v2.4 DOI, as with
the v2.3 release (DOI added in a follow-up PR).

- Lead-time register + forecast cadence (borrowed from the Patos Lagoon
  and Gironde river twins): `scripts/registry.py issue` accepts
  `--cadence daily | weekly | seasonal | event-driven` and `--lead-time`
  (value) with `--lead-time-unit hours | days | weeks` (default `days`).
  Both fields are validated on issue and on verify; records issued before
  v2.4 carry neither field and still verify. Documented in SKILL.md
  (Stage 7, I/O table) and in `assets/templates.md` §5, with a marked
  format example; no existing registry record is touched (BEIRA-F-001
  unchanged, hash chain intact).
- Data-onboarding checklist (borrowed from EDITO): Phase 1 admits a
  dataset only against the checklist — source and access date, licence
  and reuse terms, spatial and temporal resolution and coverage, QC
  performed (method and result), gaps → the [НЕТ ДАННЫХ] register.
  Added to SKILL.md (Stage 2, Object Passport template) and to
  `assets/templates.md` §1.
- Tests: T32 (registry cadence/lead_time), T33 (checklist presence).
  Verification in staging: 74 tests pass (67 baseline + 7 new); strict
  lint passes from a copy installed as `ecosystem-digital-twin/`.

## v2.3 — 2026-10-25
- SKILL.md rewritten to the v2.3 specification: strict mathematical
  specifications (WPI, Carlson TSI, HPI with critical threshold 100,
  Mann–Kendall with Hamed–Rao correction, SS_RMSE/NSE, VoI/EVSI), mandatory
  deliverable templates (Object Passport with an explicit [НЕТ ДАННЫХ] gap
  register, Circular-Economy Safety Gate), a JSON I/O-schema table for the
  scripts, and multi-agent governance. The Object Passport uses the skill's
  own 5-level maturity ladder (Prototype, Descriptive, Informative,
  Predictive, Decision). The I/O table was verified against the actual
  script interfaces and corrected where the draft described JSON contracts
  the scripts do not have (see the verification report).
- trend_test.py: WPI, Carlson TSI, and HPI functions plus `--mode
  wpi/tsi/hpi` and a JSON trend input (`{"values", "timestamps", "alpha"}`)
  with the spec output keys (`s_stat`, `var_s_raw`, `hamed_rao_factor`,
  `z_corrected`, `p_value`, `theil_sen_slope`, `trend`). The existing
  Hamed–Rao correction and CSV interface are unchanged.
- skill_scores.py: `ss_rmse` = 1 − RMSE_model/RMSE_naive, an `ss_rmse`
  output field, and the `admission_verdict` (ADMITTED if and only if
  SS_RMSE > 0 on the declared hold-out; null for in-sample fits). The
  existing MSE-ratio skill scores are kept and documented as differing from
  SS_RMSE in value while sharing the > 0 boundary.
- Zenodo DOI for v2.3: 10.5281/zenodo.23657185 (release 2026-10-26; author Baldanova, Rigjita, ORCID 0009-0009-7891-7007).
- Editorial cleanup (2026-10-26, pre-release): the draft meta-comment above the I/O table is replaced by a direct instruction, and the two template headings are demoted to #### so they no longer compete with ### Template 1 / 2.
- Verification fix (2026-10-25, independent check): Stage 7 wording corrected — forecast uncertainty is narrowed by assimilating observations, not by alert_bands.py (which recomputes the alert bands).
- Package completeness: all 9 scripts kept (evidence_search.py and
  uncertainty_budget.py included), tests/, examples/ (including Beira),
  references/, assets/templates.md kept; orchestration stays at
  references/orchestration.md.
- examples/beira/: worked example on Beira Lake (Colombo) from published data
  only — state against the authors' thresholds, cross-check with three
  independent studies (2024–2026), a Gate-B-style check of the source, the
  arithmetic of what a wetland alone can achieve (Carlson TSI), the value of
  information of a sludge analysis in relative units, a registered trial
  forecast, and the data gaps that keep the twin at maturity 2. Unit tests
  in tests/test_example_beira.py.
- Tests: T30 (WPI/TSI/HPI + index modes + JSON trend input), T31 (SS_RMSE
  and the admission boundary). Dry-run on the cascade case "water body →
  subcritical sludge processing → agricultural field" (see
  dry-run-cascade/dry-run-report.md).
- Release note: the CITATION.cff DOI is still the v2.2 release DOI
  (10.5281/zenodo.23608283); v2.3 gets a new Zenodo DOI at release, and the
  README citation block is updated then.

## v2.2 — 2026-10-21
- trend_test.py: the default correction for serial correlation is now the
  Hamed & Rao (1998) variance correction (detrended ranks, significant lags
  only; matches pymannkendall 1.4.3 to four decimals). Found on real data:
  for Lake Huron levels (lag-1 r = 0.76) trend-free pre-whitening raised
  |Z| from 5.2 to 7.2 — the correction must not make a trend look more
  certain; Hamed–Rao gives |Z| = 2.85. TFPW stays available with a warning.
  `--prewhiten` remains as a hidden alias.
- skill_scores.py: `--persistence fixed` (last training observation) for
  forecasts issued at the end of training; `rolling` (previous observation)
  stays the default for one-step forecasts. Comparing a multi-year
  forecast with one-step persistence was unfair to the model.
- analytics-forecasting.md: a Pettitt change point is a flag, not a
  verdict — it also fires on a smooth monotonic trend.
- examples/open-series-demo.md and open_series_demo.py: the core run on three public series
  (Nile flow, Lake Huron level, Mauna Loa CO2), reproducible with one command.
- Tests: 48 automated (Hamed–Rao reference value; fixed persistence).

## v2.1 — 2026-10-21
- Multi-model runner protocol (references/orchestration.md) for councils
  that run on other developers' models through a router: one execution host
  runs every script at a pinned skill version; council members are
  text-only and never compute numbers; briefs carry capped JSON summaries
  with manifest IDs, never raw client data or precise sensitive
  coordinates; the data flow and the client's consent are recorded before
  any client data enters a run; councils of three to five models from at
  least two developers, named by exact model ID and run date; every
  exchange logged into the provenance package, with a cost cap per run.
- No language model in the alert path: Phase 4 alerts come from
  alert_bands.py and go to a named human.
- Working rules: interactive builds proceed one phase at a time with a stop
  for the owner's approval; literature is cited only from a live search
  with recorded identifiers.
- qc_series.py, alert_bands.py and registry.py score cap long lists in the
  printed summary (--max-items, totals kept) and write the full record with
  --full-json.
- Passport template gains the multi-model run line (pinned version, host,
  providers, consent, model IDs, cost cap). Tests: 47 automated; T28–T29.

## v2.0 — 2026-10-21
- Loadability fixes: the SKILL.md frontmatter was invalid YAML (an
  unquoted ": " in the description); values are now quoted and the file
  parses with PyYAML and js-yaml. A closing code fence in Phase 6 carried
  text on the same line, so everything after it rendered as code; fixed.
  SKILL.md is under 500 lines; the analytics and uncertainty summaries are
  now short pointers to their references.
- Description rewritten for triggering: water-quality, bloom, hypoxia and
  low-flow early warning, monitoring design, audits of vendor twins, and
  Russian-language requests.
- Calculation toolkit (Python standard library, unit-tested):
  qc_series.py (quality gate with Pettitt change point, flags only),
  trend_test.py (Mann–Kendall/Sen per segment between registered breaks,
  seasonal Kendall, trend-free pre-whitening), skill_scores.py (declared
  hold-out, persistence and climatology baselines, NSE/KGE/RMSE,
  POD/FAR/CSI, Brier with reliability and Murphy decomposition),
  registry.py (append-only hash-chained forecast registry, no back-dating,
  superseded forecasts stay scored, overdue forecasts listed),
  generalize_coords.py (GBIF sensitivity categories per Chapman 2020 with
  this skill's 0.1° floor, extreme records withheld, pre-sharing check),
  build_manifest.py (valid RO-Crate 1.1 package; headline numbers traced and
  cited in the report; forecast registry tied to the package),
  uncertainty_budget.py (budget by source from one-at-a-time and joint
  ensembles; interval only from a joint ensemble), alert_bands.py (anchored
  amber/red bands, sustained-breach windows, gaps end episodes, invalid
  values ignored, suspect values kept and marked, optional noise tolerance). All CSV readers accept
  comma, semicolon or tab delimiters and decimal commas, and report rows
  they could not use. evidence_search.py: explicit 429 handling,
  consistent first-author field, contact-email warning.
- Rules sharpened: trial forecasts defined for level-3 twins (how level 4 is
  earned, no decision weight); scenario numbers from published effect sizes
  labeled evidence-based; intervals must name their computing method; the
  Phase 6 manifest example is now actual RO-Crate structure; GBIF extreme
  category handled (withhold) — previously 0.1° for all.
- Worked example made consistent with the rules: calibration plan declared
  before fitting and reported against baselines; no bloom probability from
  two events; the chlorophyll forecast registered as a trial; the wetland
  effect labeled evidence-based with the lake response stated as a gap.
- Tests: tests/test_scripts.py (45 unit and end-to-end tests, network-free), tests/check_package.py
  (package lint), T19–T27 and a traceability table in TESTS.md. Contents
  lists added to the four references over 100 lines. READMEs rewritten for
  the repository page (process diagram, install instructions — the folder
  name must match the skill name — and an honest status section);
  CITATION.cff for GitHub's citation button; GitHub Actions run the tests
  and the strict lint on Python 3.9 and 3.12.

## v1.8 — 2026-10-20
- Usability pack: three documents
  that make the package usable without reading all ~2,000 lines first.
  references/quick-start.md — the one-page, ten-step Tier S path, what may
  be skipped at Tier S and what may never be skipped, escalation rules,
  and a file map. assets/templates.md — the five fillable forms (object
  passport with ELSA/FPIC checklist; risk register row; TARP; option card
  with counterfactual freeze line; forecast registry entry), with the
  rule that a non-applicable field is marked "n/a — reason", never
  silently deleted. examples/lake-example.md — a worked miniature: one
  fictional small lake carried end to end (passport, inventory with a
  stated gap, indicators, pattern memo, two-event catalogue with the
  honest watch-instead-of-forecast call, registry entry, TARP, option
  card, Gate C record), all values explicitly labeled illustrative.
- SKILL.md gains a "Start here" section pointing to the three documents.
  Test: T18 (usability walkthrough).

## v1.7 — 2026-10-20
- Five approved improvements (from the expert gap review she accepted):
  (1) quantitative uncertainty, (2) domain data standards, (3) forecast
  pre-registration, (4) value of information and adaptive sampling,
  (5) the counterfactual twin. New references/uncertainty-decision.md:
  uncertainty method ladder (Monte Carlo/ensembles → Bayesian calibration
  → Morris/Sobol global sensitivity → structural comparison), uncertainty
  budgets separating measurement/forcing/parameter/structural/scenario
  shares; value-of-information cycle (uncertainty map, next-measurement
  ranking by decision-uncertainty reduction per cost, sensor placement
  logic, adaptive intensification, stopping rule, realized-value audit);
  append-only forecast registry with EFI-style metadata — verification
  computed against forecasts exactly as issued; counterfactual twin
  protocol (frozen no-action baseline, both twins on identical forcings,
  no silent re-anchoring, field BACI evidence outranks the model,
  avoided-damage reporting as promised/attributed/observed).
- Data standards pack added to references/data-sources.md (OGC
  SensorThings, WaterML 2.0, Darwin Core, EML, STAC, CF, RO-Crate) and
  wired into Phase 6 nesting. SKILL.md hooks in Phases 3–6, a summary
  section, and a quality gate. Tests: T15 (uncertainty honesty), T16
  (value of information), T17 (registry and counterfactual integrity).

## v1.6 — 2026-10-20
- Analytics, forecasting, risk and prevention layer added (data
  analysis, historical data where available, pattern detection, event
  prediction, risk identification, preventive measures, forecasts, and
  decision options for improving the existing ecosystem). New
  references/analytics-forecasting.md: historical data rescue (archives,
  yearbooks, Landsat back to 1984, museum/herbarium records, proxy records,
  consented local knowledge) with a bias and breaks register; pattern
  analysis (climatology, trends, extremes, change points, lead–lag
  structure, phenology, regime-shift early-warning signals as hypotheses)
  delivered as a pattern memo; an event catalogue (occurrence, antecedent
  conditions, impact, response) as the bridge to prediction; a
  predictability audit and method ladder for event forecasting; mandatory
  event-based validation (probability of detection, false-alarm ratio,
  critical success index, lead-time distribution, Brier score); a risk
  register argued per cell from evidence; trigger–action–response plans
  (TARP) for preventive measures with owners, lead times and stand-down
  criteria; option cards (prevent → mitigate → restore → adapt → monitor,
  no-regret first) with residual risk and a verification indicator per
  option; after-action reviews closing the loop.
- SKILL.md hooks: Phase 1 historical data rescue; Phase 3 event-based
  validation; Phase 4 risk register and preventive action; Phase 5 option
  portfolio from the risk register; new summary section and quality gate.
  Data sources extended with archive and historical-collection rows.
  Tests: T13 (pattern and event-forecast honesty), T14 (preventive TARP).

## v1.5 — 2026-10-20
- Orchestration layer added (an orchestrator, specialist agents, and a
  red team, as a governed layer). New
  references/orchestration.md: three scale tiers (S single operator /
  M orchestrated specialists / L full council) chosen in Phase 0; seven
  roles with distinct seniority-framed personas (orchestrator, data scout,
  evidence scout, domain modeler, calibration auditor, red team, optional
  specialists); written task contracts (passport slice, manifest-ID inputs,
  gaps-not-guesses outputs, prohibition list); conflict resolution by
  evidence hierarchy, never by vote; independence rules (auditor ≠ modeler,
  red team ≠ builder, red-team model ≠ arbiter model, one shared persona
  voids a council).
- Red-team gates with attack checklists: Gate A design (indicator theater,
  threshold smuggling, proxy overclaims), Gate B calibration (tuning on
  scoring data, metric shopping, assimilation theater), Gate C delivery
  (scenario cherry-picking, moved weights, maturity overclaims); attacks
  recorded with severity and disposition; an unresolved critical attack
  blocks delivery.
- SKILL.md gains a summary section and a matching quality gate. Local
  implementation note points to ensemble.py (--models explicit, --personas
  distinct, --redteam-model different from the arbiter). Tests: T11
  (orchestration contract and independence), T12 (red-team gate blocks a
  flawed delivery).

## v1.4 — 2026-10-20
- Evidence layer connected (PubMed and similar platforms for evidence
  collection). New
  references/evidence-sources.md: platform routing — PubMed/PMC (microbiology,
  sanitary, toxicology, molecular methods), Europe PMC (life-science breadth,
  open full text), OpenAlex (hydrology, soil, remote sensing discovery),
  Crossref (DOI identity layer), Semantic Scholar, AGRIS, regional-language
  sources (CyberLeninka / eLibrary for Russian objects); licensed indexes
  (Scopus/WoS/CAB) only where access actually exists. Query protocol
  (per-platform translation, bilingual search, full provenance record) and
  evidence discipline (hierarchy standards → guidelines → reviews → local
  studies; abstracts screen, full text decides; transferability check).
- New scripts/evidence_search.py: queries PubMed, Europe PMC, OpenAlex and
  Crossref, emits normalized JSON compatible with the literature-review
  skill's deduplication/formatting helper. Live-tested 2026-10-20: PubMed,
  Europe PMC and Crossref returned records with PMIDs/DOIs; OpenAlex keyless
  pool answered 429 from this network (script stops that source and reports,
  per protocol; a free OpenAlex key raises the budget).
- SKILL.md: Phase 1 gains the evidence inventory; Integration names the
  routing reference and the helper. Tests: T9 (evidence routing), T10
  (helper smoke test).

## v1.3 — 2026-10-20
- Comprehensive indicator catalogue (scope addition: environmental
  quality indicators — chemistry, microalgae, nutrients, microbiology, flora,
  fauna, hydrometry, land — where they improve the twin). references/
  indicators.md rewritten: 19 sections, tiered Core / Conditional / Research —
  climate drivers; air quality and deposition; full hydrometric panel (stage,
  rating curves, discharge, low/high-flow indices, ice, sediment transport,
  channel morphology); surface-water physical and chemical panel (incl.
  nutrient forms reported separately); eutrophication and internal loading;
  contaminants and ecotoxicology; sediments; groundwater; soil and land;
  landscape and disturbance; flora; microalgae/phytoplankton/phytobenthos;
  sanitary and process microbiology (E. coli, enterococci, source tracking,
  AMR, denitrification, methane); invertebrates and zooplankton; fish and
  wildlife by taxon; ecosystem functions; pressure–response indicators;
  domain quick sets; indicator metadata and QA requirements.
- Selection discipline added to SKILL.md Phase 2 and domain modules: the
  catalogue is tiered, unselected conditional panels are justified by the
  absence of their trigger, unmeasured selected indicators remain named gaps.
- Data sources extended: CAMS, GRDC, GEMStat / water-quality portals, JRC
  Global Surface Water, GRACE, Movebank, ESDAC/LUCAS; laboratory note for
  microbiology, phytoplankton taxonomy and tissue chemistry.
- Scenarios extended: bloom/sanitary-risk management, contamination source
  control, early detection and rapid response.
- Tests: T7 (indicator selection discipline) and T8 (catalogue completeness)
  added.

## v1.2 — 2026-10-20
- Loop-hardened: four external judging rounds (strict reviewer protocol;
  judges: claude-opus-5.5 partial pass + deepseek-v4-pro-0813 full rounds).
  Scores: 8.6 → 8.7 → 8.4 → 8.7 (plateau; the dip was judge granularity
  oscillation — each round surfaced finer nits, all fixed).
- Fixes across rounds: negative-space and layer discipline (forecasts require
  calibration at every maturity level); named calibration metrics (RMSE,
  NSE/KGE) with holdout/cross-validation and naive-baseline comparison;
  failure thresholds declared before fitting; assimilation method heuristic
  by data density (nudging → EnKF/particle filtering); exit criteria added;
  sensitive-species generalization grid (0.1°) and red-list/CITES basis;
  agricultural data cited to the EU Code of Conduct; conflict-of-interest and
  personal-data lines in the ELSA check; FPIC narrowed to law/standards;
  open-data license precision (Sentinel acknowledgement, Copernicus DEM
  terms, GBIF DOI citation); NBS skip must be recorded in the passport;
  scenario weights fixed with the client before runs (MCDA); provenance
  package minimum format set to RO-Crate (JSON-LD); alert windows per
  indicator dynamics; world-practice entries anchored to verifiable sources
  (DOIs, project phases per the operators).

## v1.1 — 2026-10-20
- World-practice upgrade (the best of the world's existing digital
  twins, adapted and improved). Survey in
  references/world-practice.md: Destination Earth, BioDT, EU Digital Twin of
  the Ocean, Delft-FEWS/Deltares, Wageningen farm twins.
- Added: twin maturity ladder (Phase 0) with stakeholder map and ELSA check;
  data quality gate + fall-back hierarchy (Phase 1); three-layer separation,
  modularity, hybrid models (Phase 2); assimilation cycle + standing
  verification with client-facing scores and decision-value review (Phase 4);
  nature-based-solutions-first rule (Phase 5); RO-Crate-style provenance
  package with manifest IDs and nesting into larger systems (Phase 6);
  client data ownership as a non-negotiable.
- Tests: T5 (fall-back hierarchy) and T6 (maturity + verification in the
  report) added.

## v1.0 — 2026-10-20
- Created by Rigjita Baldanova. Original skill (not an adaptation).
- Scope set by the author's brief (2026-10-20): both consulting product and research
  instrument, product first; full cycle including scenario modeling oriented
  to ecosystem improvement, plus monitoring with alert thresholds; data
  strategy = skill selects sources per object, open sources first, client and
  sensor data added after.
- Domains: agriculture; ponds and lakes; river reaches; air basins; flora and
  fauna conservation sites.
- Structure: SKILL.md (workflow, Phases 0–6, domain modules, quality gates) +
  references/data-sources.md, references/indicators.md,
  references/scenarios.md.
