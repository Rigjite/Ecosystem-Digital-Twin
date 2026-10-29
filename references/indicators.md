# Indicators and threshold anchors

## Contents
1 Climate and weather drivers · 2 Air quality and deposition · 3 Hydrology
and hydrometry · 4 Surface-water physical and chemical quality · 5 Nutrients
and eutrophication · 6 Contaminants · 7 Sediments · 8 Groundwater · 9 Soil and
land · 10 Landscape and disturbance · 11 Flora · 12 Microalgae and
phytoplankton · 13 Microbiology · 14 Invertebrates · 15 Fish and wildlife ·
16 Ecosystem functions · 17 Pressures and management response · **18 Domain
quick sets (start here)** · 19 Indicator metadata and quality requirements ·
20 Watch levels and alert rules · 21 Cryosphere and mountain hazards · 22 Steppe and natural grassland · 23 Livestock farm · 24 Peatlands and bogs · 25 Marine and coastal · 26 Urban ecosystems · 27 Aquaculture · 28 Desert and arid lands · 29 Tundra and polar · 30 Forest · 31 Cropland · 32 Non-peat wetlands and marshes

This is a catalogue, not a universal checklist. A twin selects indicators by
the object's media, pressures, decisions, and available evidence. Including an
indicator means the twin can state its source, method, unit, frequency,
baseline, uncertainty, and threshold anchor. An indicator that cannot be
measured or credibly modeled is recorded as a data gap, never silently dropped
and never replaced by a plausible value.

Tiers used below:

- **Core** — include for every object where the medium or component is present,
  unless the passport records why it is not applicable.
- **Conditional** — include when the named pressure, exposure pathway, legal
  duty, or management decision is present.
- **Research** — include when the research question, method, budget, and quality
  control justify it; label results as research-grade until validated for
  management use.

Threshold bands are set per object. Anchors below are starting points to verify
against the law and standards of the object's jurisdiction at build time —
never copy a number into a deliverable without its named source.

## 1. Climate and weather drivers

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Air temperature: mean, minima, maxima, extremes | Thermal forcing on water, soil, species, and phenology | Core | WMO practice; station or reanalysis baseline |
| Precipitation: totals, intensity, dry spells, extreme events | Water input, erosion, flood and drought forcing | Core | National hydrometeorological practice; object baseline |
| Snowpack depth and snow-water equivalent; snowmelt timing | Seasonal storage and spring flow | Conditional — cold climates | Hydromet station practice; basin baseline |
| Evapotranspiration and vapor-pressure deficit | Drying pressure and irrigation demand | Core for land and shallow waters | FAO-56 / reanalysis / flux or remote-sensing products, locally checked |
| Soil and water heat sums; growing degree days | Biological timing and productivity | Conditional | Crop, species, or lake-process literature for the object |
| Frost days, freeze–thaw cycles, heatwave duration | Stress events and infrastructure/ecosystem damage windows | Core | Object climate baseline; WMO extreme indices |
| Wind speed and direction; mixing and dispersion conditions | Lake mixing, air dispersion, seed/pollutant transport | Core for lakes and air basins | Station/reanalysis baseline; dispersion-model requirements |
| Solar radiation and cloud cover | Primary production, heating, evaporation | Conditional | Reanalysis or station baseline |
| Drought indices (SPI, SPEI or national equivalent) | Meteorological and agricultural drought state | Core for land, rivers, wetlands | National drought service practice |
| Fire-weather index and lightning/fire occurrence | Wildfire pressure | Conditional — fire-prone systems | National fire-danger system |

## 2. Air quality and atmospheric deposition

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| PM2.5 and PM10: annual, 24-hour, episode peaks | Human and ecosystem particulate exposure | Core | WHO Air Quality Guidelines 2021; stricter national limits where applicable |
| Coarse dust deposition | Soil, snow, water and vegetation loading | Conditional | National deposition methods; object baseline |
| NO, NO2, NOx | Combustion pressure, eutrophying and acidifying deposition, vegetation exposure | Core | WHO AQG; CLRTAP critical levels for vegetation |
| SO2 and sulfate deposition | Acidification pressure | Core | WHO AQG; CLRTAP critical loads |
| Ozone (O3), including AOT40 where used | Vegetation injury and health exposure | Core | WHO AQG; CLRTAP critical levels |
| Ammonia (NH3) and ammonium deposition | Agricultural nitrogen pressure on sensitive habitats | Conditional — agriculture or sensitive habitats | CLRTAP critical levels/loads; national habitat guidance |
| Carbon monoxide (CO) | Combustion episodes and urban pressure | Conditional | WHO AQG; national limits |
| VOCs and benzene | Industrial/traffic toxic pressure | Conditional | National air-quality standards |
| Metals and PAHs in particles/deposition | Toxic and persistent pollutant loading | Conditional | National/regional standards; deposition baseline |
| Nitrogen and sulfur total deposition | Acidification and eutrophication of soils and waters | Core | Empirical critical loads under UNECE CLRTAP, per ecosystem type |
| Pollen and airborne fungal spores | Public-health and phenology signal | Conditional | National aerobiology networks |
| Visibility / aerosol optical depth | Aerosol burden where ground stations are sparse | Research | Satellite product validation against ground truth |

## 3. Hydrology and hydrometry — the water-gauge panel

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Water level / stage, with datum and rating-curve status | Immediate water state for lakes, rivers, wetlands, groundwater-fed systems | Core | National hydrometric practice; gauge datum in provenance log |
| Discharge and flow velocity | Habitat, transport, load calculation, water availability | Core for rivers and inflows/outflows | National hydrometric standards; environmental-flow rules |
| Runoff volume and runoff depth | Catchment water yield and storage change | Core | Basin water balance; object baseline |
| Flow-duration curve; Q90/Q95 and other low-flow indices | Drought habitat and abstraction pressure | Core for rivers | National low-flow and environmental-flow practice |
| Peak flow, flood frequency, flood duration, inundation extent | Flood risk, floodplain connection, disturbance regime | Core | Flood-frequency analysis; floodplain management plan |
| Baseflow index and recession rate | Groundwater support and drought resilience | Conditional | Hydrograph-separation method stated in provenance |
| Hydrograph timing: onset, centroid, snowmelt peak | Seasonal regime shift | Conditional — seasonal systems | Object baseline hydrograph |
| Flashiness index | Hydrologic instability from land use, drainage, or regulation | Conditional | Published index method; basin baseline |
| Lake/reservoir residence time and flushing rate | Response time to load changes and blooms | Core for lakes | Water balance; bathymetry-based volume |
| Stratification: onset, strength, turnover dates | Oxygen, nutrient recycling, habitat compression | Core for stratified lakes | Limnological monitoring practice |
| Ice-on, ice-off, ice thickness | Winter ecology, safety, seasonal regime | Conditional — cold climates | National ice observation practice |
| Channel cross-section, bed level, bank retreat | Channel change, habitat loss, infrastructure risk | Core for river reaches | Repeat survey protocol |
| Suspended-sediment concentration and sediment load | Erosion, turbidity, contaminant and nutrient transport | Core for rivers; conditional for lakes | National sediment monitoring practice |
| Bedload movement or proxy | Channel stability and spawning substrate disturbance | Conditional | Specialist survey protocol |
| Groundwater–surface-water exchange indicators | Gaining/losing reaches, wetland support, baseflow source | Conditional | Hydrogeological assessment; paired gauges |

## 4. Surface-water physical and chemical quality

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Water temperature profile | Thermal habitat, stratification, species limits | Core | National water standards; species-specific limits |
| Dissolved oxygen: concentration, saturation, diurnal range, bottom-water minima | Survival of fish and benthos; respiration/production balance | Core | National standards; WFD-type classes in the EU. ~2 mg/L is a widely used literature alert value for severe hypoxia — a typical anchor, not a standard |
| pH | Acid/base state, metal mobility, treatment and habitat stress | Core | National standards; WFD-type classes |
| Redox potential | Sediment and bottom-water reducing conditions | Conditional | Method stated; used with oxygen and nutrient data, not alone |
| Electrical conductivity, salinity, total dissolved solids, mineralization | Ionic load, road salt, mining, irrigation and seawater intrusion pressure | Core | National standards; object baseline for natural waters |
| Turbidity and total suspended solids | Light, erosion, sediment and contaminant transport | Core | National standards; object baseline |
| Transparency: Secchi depth and light attenuation | Light climate for macrophytes and primary production | Core for lakes and clear rivers | Lake/river type baselines |
| Color and dissolved organic carbon (DOC) | Catchment carbon export, treatment burden, light attenuation | Conditional | Object baseline; drinking-water guidance where relevant |
| Alkalinity and hardness | Buffering capacity and organism requirements | Core | National standards; geology-specific baseline |
| Major ions: Ca, Mg, Na, K, chloride, sulfate, bicarbonate | Salinization, acidification, source fingerprinting | Conditional | Hydrochemical classification; object baseline |
| Silica (dissolved reactive silicon) | Diatom production and nutrient-ratio balance | Conditional — diatom-relevant waters | Limnological practice; object baseline |

## 5. Nutrients, organic matter and eutrophication

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Total phosphorus and soluble reactive phosphorus / orthophosphate | Phosphorus availability and eutrophication risk | Core | WFD-type class boundaries; national standards |
| Total nitrogen; dissolved inorganic nitrogen | Nitrogen availability and downstream export | Core | WFD-type class boundaries; national standards |
| Ammonium, nitrite, nitrate — reported separately | Toxicity (ammonium), treatment state, source and process diagnosis | Core | National standards; do not merge into one nitrogen number when decisions depend on the form |
| Total and dissolved organic carbon | Organic loading, color, microbial substrate | Conditional | Object baseline; treatment guidance where relevant |
| BOD5 and COD | Biodegradable and total oxygen-demanding load | Core for impacted waters | National standards; WFD-type classes |
| Chlorophyll-a (and phaeophytin where used) | Algal biomass and trophic state | Core | OECD / WFD class boundaries per water type |
| Trophic state index or class | Communicable eutrophication status | Core for lakes | OECD or national classification, method named |
| Hypolimnetic oxygen depletion rate | Internal eutrophication pressure in stratified lakes | Conditional — stratified lakes | Limnological practice; lake baseline |
| Internal phosphorus loading estimate | Sediment legacy effect and recovery lag | Conditional — eutrophic lakes | Sediment/water methods stated; scenario models must carry the lag |
| Nutrient loads (concentration × discharge) and catchment export coefficients | Actual mass delivered downstream, not just concentration | Core for rivers and lake inflows | Catchment plans; WFD-type targets |
| N:P and Si:N / Si:P ratios | Nutrient limitation and diatom versus cyanobacteria risk | Conditional | Limnological literature for the water type |
| Primary production and ecosystem respiration | Functional eutrophication and carbon balance | Research | Free-water or chamber methods with QA stated |

## 6. Contaminants and ecotoxicological pressure

Include only where a source, pathway, legal duty, or prior finding justifies
testing; contaminant panels are expensive and a negative result is bounded by
the detection limit and sampling date.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Priority metals in water/sediment/biota: Hg, Cd, Pb, As, Cu, Zn, Ni, Cr and others by source | Toxic pressure, mining/industrial/urban signal | Conditional | Environmental quality standards; sediment-quality guidelines; tissue limits where applicable |
| Mercury methylation indicators and methylmercury in fish | Food-web mercury risk | Conditional — mercury sources or fish consumption | Fish tissue guidance; specialist protocol |
| Pesticides: current-use and legacy compounds by catchment use | Agricultural and vector-control pressure | Conditional | Environmental quality standards; catchment pesticide inventory |
| PAHs, PCBs and other persistent organic pollutants | Combustion, industrial and legacy contamination | Conditional | Environmental quality standards; sediment guidelines |
| Petroleum hydrocarbons | Spills, runoff, ports, roads and industry | Conditional | National standards; incident protocols |
| PFAS panel | Persistent industrial/urban contamination | Conditional — known or suspected sources | Jurisdictional guidance; method detection limits stated |
| Pharmaceuticals and personal-care contaminants | Wastewater pressure on aquatic organisms | Conditional — wastewater influence | Research or regulatory watch-list methods |
| Microplastics in water, sediment, and biota | Plastic particle pressure and transport | Conditional / Research | Harmonized sampling method named; size range and blank controls mandatory |
| Radionuclides | Nuclear, mining, or medical/industrial legacy pressure | Conditional | National radiation monitoring rules |
| Sediment toxicity and whole-effluent toxicity tests | Integrated biological effect where chemistry alone is inconclusive | Conditional | Standard bioassay protocols |
| Biomarkers and tissue burdens in sentinel species | Exposure and effect inside organisms | Research | Peer-reviewed protocol; ethics and permits for animal sampling |

### Hazard quotient and hazard index (HQ/HI)

**HQ = exposure / reference value** per stressor — the exposure divided
by its regulatory or guideline reference (ПДК, WHO guideline, occupational
limit, or a published screening value, stated on the term). **HI = the sum
of the HQs**, split into acute and chronic; **1 is the safety line — above
1 is unsafe**. The same quotient family as HPI, but HPI covers only metals
in water on a 100-scale; HQ/HI covers any stressor — air, water, smoke,
chemicals — on a 1-scale, with the acute/chronic split. Computed by
`scripts/trend_test.py --mode hq` from a JSON `{"stressors": [...]}` list
(name, exposure, reference, duration acute/chronic, target organ where
known). A reference must be > 0 and an exposure >= 0; a stressor with no
published reference goes to the [НЕТ ДАННЫХ] register, never to a guessed
denominator. The published HI is often reported per target organ — the
function sums by duration and keeps the target on each term, so a
per-target HI is read off the terms.

*Example — fire smoke, Baikal region (Bychkov & Fereferov 2022):* acute
HQ 11.3 (suspended solids), 1.4 (formaldehyde), 1.2 (carbon monoxide) —
HI acute 13.9, far above the safety line; chronic HI 12.7 (respiratory),
6.3 (cardiovascular), 5.9 (mortality). Any single stressor above 1 already
makes the exposure unsafe; the sum shows the combined burden.

## 7. Sediments and substrate

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Grain-size distribution and substrate composition | Habitat quality, erosion/deposition environment | Core for benthic systems | Survey protocol |
| Sediment organic matter and nutrient content | Benthic food, oxygen demand, internal loading risk | Core for lakes and slow rivers | Limnological/sediment practice |
| Sediment oxygen demand | Bottom oxygen pressure | Conditional | Chamber/core methods |
| Sedimentation and erosion rates | Basin infilling, turbidity, habitat burial or loss | Conditional | Repeat bathymetry, traps, or dated cores |
| Substrate embeddedness and fine-sediment cover | Spawning and macroinvertebrate habitat quality in rivers | Core for gravel-bed rivers | National habitat survey protocol |
| Large woody debris frequency and function | River habitat complexity and geomorphic process | Conditional | River habitat survey protocol |
| Macrophyte-bed sediment condition | Rooting, nutrient exchange, habitat stability | Conditional | Lake macrophyte survey protocol |

## 8. Groundwater and subsurface water

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Groundwater level / depth to water | Aquifer state, wetland and baseflow support | Core where groundwater matters | National groundwater monitoring practice |
| Groundwater temperature and electrical conductivity | Flow paths, salinization, surface-water connection | Conditional | Hydrogeological baseline |
| Nitrate and other nutrients in groundwater | Agricultural and septic leakage | Core in agricultural/settled catchments | Drinking-water and groundwater standards |
| Major ions and hydrochemical facies | Aquifer evolution and source fingerprinting | Conditional | Hydrogeological classification |
| Pesticides, metals, PFAS or hydrocarbons in groundwater | Contaminant plumes and legacy pressure | Conditional | Groundwater quality standards |
| Recharge estimate and abstraction balance | Sustainability of withdrawals | Conditional | Water-balance / water-rights accounting |
| Groundwater-dependent ecosystem indicators | Springs, wetlands, baseflow reaches at risk from drawdown | Conditional | Ecohydrogeology assessment |

## 9. Soil and land quality

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Soil organic carbon / organic matter trend | Soil health, carbon storage, water holding | Core | Object baseline; direction over 3–5 years matters more than one value |
| Soil moisture by depth and plant-available water | Drought, irrigation, wetland hydroperiod, erosion | Core | Crop/ecosystem-specific guidance; sensor calibration required |
| Soil temperature | Germination, microbial activity, permafrost/freeze risk where present | Conditional | Object baseline |
| Texture, bulk density, compaction, infiltration rate | Rooting, runoff generation, traffic damage | Core | National soil survey methods |
| Soil pH, electrical conductivity, salinity, sodicity | Fertility, salinization, irrigation suitability | Core | National soil guidance |
| Total and available N, P, K; C:N ratio | Fertility and leakage risk | Core for land systems | Agronomy/soil guidance; nutrient-balance rules |
| Soil microbial biomass carbon/nitrogen; soil respiration | Biological activity and carbon turnover | Conditional / Research | Standard soil biology methods |
| Earthworm and soil mesofauna indicators | Soil structure, litter processing, soil food web | Conditional | Soil biodiversity monitoring protocols |
| Erosion rate / erosion risk class | Soil loss and downstream sediment delivery | Core for sloping or disturbed land | RUSLE-family models plus field evidence |
| Ground cover: vegetation, litter, biological crust, bare soil | Erosion protection and habitat surface state | Core | Field/remote-sensing protocol |
| Soil contaminants: metals, PAHs, pesticides, PFAS where sourced | Legacy pollution and food-chain risk | Conditional | Soil quality standards |
| Land cover and land-use change rate | Habitat conversion and pressure trajectory | Core | CORINE/national products; object time series |
| Soil sealing and impervious surface share | Infiltration loss and runoff pressure | Conditional — settled catchments | Land-cover products; planning data |

## 10. Landscape, habitat structure and disturbance

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Habitat extent by class and change rate | Carrying capacity and conversion pressure | Core | Object baseline from land-cover time series |
| Patch size distribution, edge density, core area | Fragmentation and interior-habitat loss | Core | Landscape ecology metrics, classes named |
| Connectivity and corridor function | Movement between populations and habitat units | Core | Species or guild movement model; field validation where possible |
| Riparian buffer width, continuity, and condition | Shading, filtering, bank stability, corridor value | Core for waters | Riparian guidance; management plan |
| Wetland hydroperiod and inundation duration | Wetland function and breeding/feeding habitat | Core for wetlands | Wetland classification and monitoring practice |
| Floodplain inundation extent, timing, duration | Lateral connectivity and floodplain productivity | Core for floodplain rivers | Remote sensing plus gauge thresholds |
| Lake shoreline development and littoral habitat condition | Littoral pressure and nursery habitat | Conditional — lakes | Lake habitat survey protocol |
| Canopy cover, stand structure, deadwood volume | Forest habitat quality and carbon storage | Conditional — forests | National forest inventory practice |
| Disturbance footprint: roads, tracks, recreation, grazing, logging, drainage | Pressure intensity and recovery need | Core | Management plan limits; object baseline |
| Fire regime: burned area, severity, return interval | Disturbance regime shift | Conditional — fire systems | Remote sensing fire products; management records |
| Invasive species cover and spread front | Displacement pressure on native communities | Core | Object baseline; any new invasive record is at least amber |
| Artificial light and noise where wildlife decisions depend on them | Behavioral disturbance | Conditional | Protected-area or species guidance |
| Re-invasion / propagule pressure for invasive control scenarios | Whether control will hold | Conditional | Occurrence records plus surrounding land-cover matrix; inflow pathways |

## 11. Flora and vegetation

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Plant species richness and diversity by stratum | Community condition and change | Core | Fixed-plot or transect protocol; object baseline |
| Native versus alien species composition | Integrity and invasion state | Core | Regional flora; invasive lists |
| Indicator and diagnostic species presence | Habitat type, moisture, nutrient and disturbance state | Core | Phytosociological / national habitat protocols |
| Red-list plant species occurrence and population size | Conservation outcome and legal duty | Core where present | National/IUCN red lists; sensitive-location safeguards apply |
| Vegetation cover by stratum; LAI | Structure, productivity, erosion protection | Core | Field protocol and remote sensing cross-check |
| Biomass and net primary production proxies (NDVI/EVI) | Productivity and stress | Core | Object multi-year baseline; field calibration for biomass claims |
| Phenology: green-up, flowering, senescence dates | Climate shift and food-web timing | Conditional | Phenology networks; remote-sensing time series |
| Macrophyte species composition, coverage, maximum colonization depth | Lake/river littoral state and nutrient/light condition | Core for lakes and slow rivers | WFD-type macrophyte methods; lake baselines |
| Tree and shrub health: defoliation, dieback, regeneration | Forest condition and recruitment | Conditional — woody systems | Forest inventory/health protocols |
| Rare plant community extent and condition | Habitat conservation priority | Conditional | Habitat classification and red lists of habitats where they exist |
| Genetic diversity of target populations | Long-term viability for restoration/conservation breeding | Research | Population genetics protocol; permits and ethics |

### Diversity indices

Richness alone misleads: a site can keep its species count while losing
its evenness and its taxonomic breadth. Report Shannon H′, Pielou
evenness J′, and Clarke–Warwick taxonomic distinctness Δ+ together
(`scripts/diversity.py indices` — natural logarithm throughout):

- **Shannon H′ = −Σ p_i ln p_i** — diversity of the count distribution;
  falls when one species dominates.
- **Pielou J′ = H′ / ln(S)** — evenness, 0–1; 1 means every species is
  equally abundant.
- **Δ+ (taxonomic distinctness)** — mean taxonomic distance over all
  pairs of species present, from the Linnaean hierarchy (same genus 1,
  same family 2, same order 3, same class 4, same phylum 5, different
  phylum 6). The stdlib-feasible cousin of BioDT's phylogenetic-diversity
  prototype (Faith's PD needs a phylogeny; Δ+ needs only the taxonomic
  tree the skill already uses via the GBIF backbone). A pair agrees at
  the deepest rank where both taxa are known and equal; a rank unknown
  for either cannot agree.

Counts from presence-only records are records per species — a proxy,
stated as such, never silently treated as abundance. Species missing
from the taxonomy table are excluded from Δ+ and named. (Source: BioDT
— Islam et al. 2026, npj Biodiversity 5:5; Clarke & Warwick 1998,
taxonomic distinctness.)

### Plant functional type shares

Group the site's species into plant functional types (PFTs — grasses /
forbs / legumes; C3 / C4; growth form) and track PFT shares and their
trends instead of species lists alone (`scripts/diversity.py pft`).
Shares come from one quantity only — cover or counts, never mixed — and
the assignment table is published per site (literature / TRY Plant
Trait Database, Kattge et al. 2020). A trend needs repeat surveys; one
survey reports shares only. For farm and grassland clients, PFT shares
are the management signal (grazing, mowing, fertilizer); a species list
does not answer the management question. (Source: BioDT — the grassland
prototype on GRASSMIND; the model itself does not transfer, the PFT
concept does.)

### Trait–environment matching

Screen a taxon list against published environmental-tolerance tables
(temperature, soil acidity, salinity, drought) and return which taxa fit
the site's extremes (`scripts/trait_match.py`, fed by a trait table per
object). A taxon fits when every stated tolerance is met: an "at-least"
trait (e.g. salinity tolerance) must reach the site's value; an
"optimum" trait (e.g. temperature, pH) must fall within the declared
window around the site's value. A taxon marked indifferent ("x") for a
trait is not excluded by a condition on that trait. The table is
published per object (Ellenberg indicator values for the worked
example in the field gallery entry — the Ellenberg column in Tichý et
al. 2023, "Ellenberg-type indicator values for European vascular plant
species", Zenodo record 7427088; Germany source Ellenberg & Leuschner
2010, the revised edition of Ellenberg et al. 1991. Verified against
that transcription 2026-10-26; Salicornia values are ssp. europaea) —
a table transcribed for a build is verified against the published
source before client use. The answer is
the list that fits the site's extremes, not a ranking: it answers "which
wild relatives / resilient varieties suit this site". (Source: BioDT —
the crop wild relatives prototype, ModGP workflow; the deterministic
filter is the transferable core.)

## 12. Microalgae, phytoplankton and aquatic primary producers

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Phytoplankton total biomass / biovolume | Algal production and eutrophication state | Core for lakes, reservoirs, slow rivers | WFD-type phytoplankton methods |
| Phytoplankton taxonomic composition and indicator taxa | Nutrient, mixing, grazing and climate diagnosis; early warning of shifts | Core for monitored lakes | Expert microscopy or validated imaging/AI classification; reference collection named |
| Diatom indices from planktonic or benthic samples | Integrated nutrient and organic pollution signal | Conditional | National diatom indices and sampling protocols |
| Phytobenthos / benthic algal biomass and composition | Littoral and riverbed production and nutrient state | Conditional | WFD-type phytobenthos methods; national bioassessment |
| Cyanobacteria biomass/biovolume and share of total phytoplankton | Bloom risk and ecosystem shift | Core | WHO recreational water guidance levels; national alert frameworks |
| Cyanotoxins: microcystins and others by local risk | Human and animal exposure risk | Conditional — blooms or recreational/drinking use | WHO Guidelines on recreational water quality (2021), Vol. 1; drinking-water guidance where applicable |
| Harmful algal bloom frequency, duration, spatial extent | Event burden and trend | Core for bloom-prone waters | Satellite plus in-situ confirmation; no satellite-only health claims |
| Phycocyanin and chlorophyll fluorescence profiles | Rapid cyanobacteria and algal vertical structure screening | Conditional | Sonde methods with microscopy/grab-sample validation |
| Benthic macroalgae / macrophyte primary production indicators | Coastal, lake and river productivity where macroalgae matter | Conditional | Habitat survey protocols |

## 13. Microbiology and microbial processes

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Escherichia coli and total coliforms | Fecal contamination and sanitary state of recreational/contact waters | Core where human contact, drinking, shellfish, or irrigation use matters | WHO recreational water guidance; national sanitary standards |
| Intestinal enterococci | Fecal contamination, especially marine and recreational waters | Core for bathing waters | EU Bathing Water Directive practice; WHO guidance |
| Fecal indicator trend after rainfall / discharge events | Event-driven contamination pathways | Conditional | Event sampling design; rainfall and discharge covariates recorded |
| Microbial source tracking markers | Human versus animal fecal sources where remediation choice depends on it | Conditional | Validated qPCR/marker protocol; results reported with detection limits |
| Pathogen testing: Salmonella, Campylobacter, enteric viruses, protozoa as relevant | Direct health risk where exposure decision requires it | Conditional | Public-health laboratory protocols; not a routine substitute for indicators |
| Antimicrobial resistance indicators (e.g. resistant E. coli, resistance genes) | Wastewater and agricultural resistance pressure | Conditional / Research | Harmonized environmental AMR methods where available |
| Soil and sediment microbial biomass and activity | Decomposition, nutrient cycling, soil biological state | Conditional | Standard soil/sediment microbiology methods |
| Nitrification and denitrification potential/rates | Nitrogen retention and removal capacity | Conditional — nutrient scenarios | Process assays or model parameters calibrated to observations |
| Methanogenesis / methane ebullition and flux in wetlands and lakes | Greenhouse-gas function and carbon balance | Conditional — carbon projects or eutrophic waters | Chamber, bubble-trap, or eddy/flux methods with QA |
| eDNA microbial and cyanobacterial community profiles | Early detection and community shifts | Research | Validated primers/controls; positive detections confirmed before management action |

## 14. Invertebrates, zooplankton and benthos

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Zooplankton biomass, composition, size structure | Fish food base, grazing control of algae, lake food-web state | Core for lakes | Limnological sampling protocol |
| Macroinvertebrate indices: EPT richness, BMWP/ASPT-type scores, national metrics | Integrated biological water quality | Core for rivers; conditional for lakes | National bioassessment protocols |
| Benthic invertebrate density, biomass, sensitive taxa | Sediment habitat and oxygen/food conditions | Core | National benthic protocols |
| Mollusc populations, including unionids where present | Long-lived integrators of flow, substrate and water quality | Conditional | Species monitoring protocols; permits for protected species |
| Aquatic invasive invertebrate occurrence and spread | New pressure and eradication window | Core where pathways exist | Early-detection protocol; confirmed identification before response |
| Terrestrial and soil invertebrate indicators | Pollination, decomposition, soil and litter function | Conditional | Pollinator/soil monitoring schemes |
| Pollinator abundance and diversity | Pollination service and pesticide/land-use pressure | Conditional — agro and flowering habitats | Standard transect/pan-trap protocols with effort recorded |

## 15. Fish, wildlife and fauna

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Fish species composition, abundance / CPUE, biomass | Aquatic community state and fishery/food-web condition | Core for fish-bearing waters | Standard survey gear with effort and selectivity stated |
| Fish age/size structure and recruitment | Population sustainability and bottleneck years | Conditional | Fisheries assessment protocol |
| Fish migration / passage counts and spawning use | Connectivity and barrier effect | Conditional — migratory species | Counter, telemetry, redd/nest or spawning survey protocol |
| Amphibian occupancy, calling activity, breeding success | Wetland condition, hydroperiod, disease and contaminant pressure | Core for wetlands/ponds | Occupancy protocol with detection probability |
| Reptile occurrence and habitat use | Dry/wet habitat mosaic condition | Conditional | Survey protocol; protected-species permits |
| Bird abundance, territory occupancy, breeding success | Habitat quality across scales; strong trend detection | Core for conservation sites | eBird/national monitoring scheme protocols |
| Diversity indices (Shannon, Pielou, taxonomic distinctness Δ+) | Community diversity beyond richness — see §11 | Core for conservation sites | `scripts/diversity.py indices`; taxonomy from the GBIF backbone |
| Mammal occupancy, relative abundance, reproduction signs | Habitat use and disturbance; camera/acoustic effort recorded | Conditional | Camera-trap or track protocol; sensitive locations generalized |
| Bat activity and roost occupancy | Insect base, light/noise and habitat condition | Conditional | Acoustic monitoring protocol |
| Target and red-list species population trend | Conservation outcome | Core where present | Monitoring-scheme trends; a declining trend is red regardless of absolute numbers |
| Wildlife disease prevalence where relevant (e.g. amphibian chytrid, white-nose syndrome) | Emerging biological risk | Conditional | Veterinary/wildlife disease protocols |
| Roadkill and other direct mortality counts | Infrastructure and disturbance pressure | Conditional | Road/transect survey protocol |
| eDNA detections for rare or invasive fauna | Early detection and presence screening | Conditional / Research | Validated assay, controls, and confirmation protocol before irreversible action |
| Brown bear abundance: state-monitoring count (individuals) and trend | The conflict species itself — whether the pressure comes from numbers or from behaviour | Core where large carnivores range near settlements; see also §30 | State-monitoring count with method and date; the Barguzinsky / Buryatia taiga-edge worked example (§30) carries the published series — Buryatia 4,625 (2011), 5,385 (2021), 6,276 (2025), 6,113 (2026) — and the lesson that behaviour, not numbers, drove the autumn 2026 exits |
| Age structure of conflict animals: share of 2–3-year-old animals among exits to settlements | The driver class — young animals expelled by adults are the ones that come out | Conditional — where human–wildlife conflict is recorded; see also §30 | Brigade and inspectorate records; qualitative anchor: "practically all exits are 2–3-year-old animals" (Burprirodnadzor, 2026); the numeric share is [NEXT DATA] — not estimated |

## 16. Ecosystem functions and services

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Gross primary production, net ecosystem production, respiration | Carbon and oxygen function | Research / Conditional | Free-water, chamber, flux or model methods with uncertainty |
| Carbon stocks: soil, biomass, sediment | Stored carbon and loss risk | Core for climate-relevant projects | Inventory methods; repeat measurement interval stated |
| Greenhouse-gas fluxes: CO2, CH4, N2O | Net climate effect of wetlands, lakes, soils | Conditional — carbon or restoration decisions | Flux protocols; do not infer from carbon stock alone |
| Nutrient retention and removal efficiency | Water-purification function of wetlands, buffers, floodplains | Core for restoration scenarios | Inflow/outflow load balance |
| Sediment retention and flood attenuation | Downstream protection function | Conditional | Event-based monitoring and model validation |
| Pollination service indicators | Crop/wild plant reproductive support | Conditional | Pollinator protocol plus flower/visitation data |
| Fish and forage production indicators | Provisioning function, subordinate to ecosystem state | Conditional | Fisheries/forage assessment; never the sole success metric |
| Recreational water safety status | Human-use service and health protection | Conditional — recreation waters | Bathing-water classification and sanitary indicators |

## 17. Pressures, management response and governance indicators

State indicators without pressure and response indicators cannot explain why
the system changed or whether management worked. Record these alongside the
state panels whenever decisions or scenarios are in scope.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Land-use shares and change in the contributing catchment/airshed | Diffuse pressure trajectory | Core | Land-cover time series; catchment accounting |
| Point-source discharge volumes and pollutant loads | Permitted and actual effluent pressure | Core where point sources exist | Permits, operator reports, independent sampling where available |
| Fertilizer, manure and pesticide inputs | Agricultural pressure and scenario levers | Core for agro/catchments | Farm records; sales/regional statistics labeled as estimates |
| Water abstraction volumes and timing | Flow and groundwater pressure | Core where abstraction exists | Water-rights and metering records |
| Flow regulation: dam releases, hydropeaking, diversion schedules | Artificial hydrologic regime | Conditional | Operator rules and gauge records |
| Impervious area and road density | Runoff, fragmentation, mortality and pollutant pressure | Conditional | Land-cover and infrastructure data |
| Visitor, grazing, fishing, hunting and forestry pressure | Direct use pressure | Conditional | Management records; counters; permits |
| Emissions inventory by source sector | Air-pressure drivers and scenario levers | Core for air basins | Official inventories; facility reports |
| Restoration and protection actions implemented: area, type, date, cost | Management response actually delivered | Core for decision twins | Project records verified in field/remote sensing |
| Compliance and enforcement indicators | Whether rules are changing pressure | Conditional | Regulator records; report uncertainty and incentives |
| Response lag and recovery trajectory after action | Whether the ecosystem is responding on the expected timescale | Core for decision twins | Before–after/control–impact design where feasible |
| Human–wildlife conflict reports: exits to settlements (events/week by district) | The event series that sets the watch level — the earliest operational signal after the mast index | Core where large carnivores range near settlements; see also §30 | Brigade / 112 / inspectorate logs with date and place; case values (Buryatia, autumn 2026): 47 in all of 2025; 15–20 a day at the peak; 59 in the week of 13–19 October |
| Food attractants register: dumps, unclosed containers, unattended livestock, garden fruit | What pulls animals to settlements — the removable cause | Conditional — where human–wildlife conflict is recorded; see also §30 | District register with place and type; no published register was found for Buryatia — [NEXT DATA] |
| Quota uptake and regulated removal: harvested animals against the permitted limit | Whether the regulated removal is actually happening — and how much of the conflict response is culling | Conditional — where a harvest limit exists; see also §30 | Permit and harvest records; case values (Buryatia, brown bear 2026): limit 1,272, about 900 permits issued, about 300 harvested a year; regulated (forced cull) 149 (14 Sep), 331 (3 Oct), 436 (20 Oct) |

## 18. Domain quick sets

Use these as the starting selection; then add conditional panels from the
sections above as pressures are identified.

- **Agriculture:** climate drivers; soil moisture, carbon, nutrients, biology
  and erosion; nutrient balance and input records; NDVI/EVI and phenology;
  receiving-water nutrient and sediment indicators; pollinators where crops or
  field margins matter; land-cover and buffer condition; PFT shares and
  trait–environment matching where the management question is which
  varieties or wild relatives suit the site.
- **Pond / lake:** hydrology and water level; stratification and ice where
  relevant; oxygen, pH, conductivity, transparency; nutrient forms and loads;
  chlorophyll and trophic state; phytoplankton composition and cyanobacteria;
  macrophytes; zooplankton and benthos; fish; littoral habitat; sanitary
  microbiology where people or animals use the water.
- **River reach:** full hydrometric panel; temperature, oxygen, BOD/COD;
  nutrient forms and loads; sediment transport and substrate; macroinvertebrate
  and diatom/phytobenthos indices; fish passage and riparian condition;
  upstream land use, effluent and abstraction pressures.
- **Air basin:** PM, NOx, SO2, O3 and NH3 where relevant; deposition to soil and
  water; dispersion meteorology; emission inventory; vegetation critical-level
  exceedance and sensitive-habitat critical-load exceedance.
- **Flora / fauna conservation:** habitat extent, connectivity and disturbance;
  flora composition and red-list populations; fauna occupancy, abundance and
  trends by taxon present; invasive species and disease where relevant;
  management actions and recovery trajectory; sensitive locations always
  generalized outside the client boundary.

- **Cryosphere / mountain:** slope displacement by InSAR and its rate and
  acceleration; glacier velocity, glacier mass balance where a glacier
  is present, and lake level/area/volume; moraine-dam
  freeboard where a moraine-dammed lake exists; permafrost ground
  temperature where permafrost terrain is present (active-layer
  thickness per §29); temperature at glacier elevation and freezing-level altitude
  as pressure; precipitation and rain-on-snow; upstream turbidity as
  the collapse signal; downstream river level as the evacuation
  warning; snowpack and avalanche danger where relevant;
  micro-seismicity as research-grade only.
- **Steppe / natural grassland:** steppe vegetation composition and PFT
  shares (notably *Stipa* share); bare ground, litter and crust share;
  forage biomass and its trend; stocking rate against carrying capacity
  and grazing utilisation; SOC stock in steppe soils (0–30 cm);
  erosion features (rills, gullies, wind scour); LFA stability /
  infiltration / nutrient-cycling indices where a field team runs them;
  virgin-steppe area and conversion rate; shrub encroachment and
  fragmentation; burned area and fire return interval; steppe birds
  (great bustard, steppe eagle, demoiselle crane) and burrowing mammals
  (marmot colonies); the SDG 15.3.1 degraded-land composite.
- **Livestock farm:** pasture condition and forage yield; stocking rate
  against carrying capacity and grazing utilisation; soil organic carbon
  under pasture (0–30 cm) and compaction under grazing (bulk density,
  infiltration); manure production and the farm N/P nutrient balance;
  manure storage capacity and freeboard; manure application timing, rate
  and method; nitrate in farm drains, boreholes and receiving water;
  ammonia and methane fluxes (enteric + manure) and nitrous oxide;
  farm water use and effluent; slurry-lagoon integrity and overflow
  risk; livestock stream access and riparian buffer condition;
  farm-boundary biodiversity (margins, hedgerows, pasture birds);
  land-use change on the farm.
- **Peatland / bog:** peat depth and peat carbon stock; water-table depth
  in peat (seasonal mean) and ditch/canal density; Sphagnum cover and
  peat-forming vegetation; net GHG flux from peat (CO₂, CH₄, N₂O) with
  the IPCC Wetlands Supplement Tier 1 factors as the fallback anchor;
  peat fire occurrence and burnt area; subsidence rate where drained;
  extraction area and volume where applicable; rewetting state
  (share rewetted, ditch blocks, water-table recovery); peatland
  condition class; waterborne carbon loss where a draining stream
  exists; paludiculture area on rewetted peat; peat fire risk as
  research-grade only.
- **Marine / coastal:** sea-surface temperature anomaly and marine
  heatwave category; Degree Heating Weeks and the NOAA bleaching alert
  level for reefs; salinity and the estuarine gradient; seawater pH and
  aragonite saturation state; live hard coral cover, bleaching prevalence
  and recruitment; macroalgal cover as the phase-shift signal;
  crown-of-thorns density where the species occurs; mangrove extent and
  change (Global Mangrove Watch) and soil carbon stock where carbon is in
  scope; seagrass extent, cover and shoot density; marine HAB occurrence
  and cell density; shoreline position and erosion/accretion rate; marine
  litter and non-indigenous species where they are management concerns;
  underwater noise as research-grade only.
- **Urban:** urban heat-island intensity (air and surface) and
  heat-health warning days; impervious-surface share and runoff
  volume per event; combined-sewer / storm-water overflow frequency,
  duration and volume; stormwater retention and green-infrastructure
  capacity; green space per capita and accessibility within 300 m /
  5 minutes; tree canopy cover and canopy equity by district;
  green-space connectivity and proportion of natural areas (Singapore
  Index); native species in built-up areas; urban blue-space extent
  and connectivity; urban stream temperature excess; urban soil
  contamination screening where justified; population noise exposure
  against WHO guideline values; artificial light at night against
  the natural-sky baseline; urban metabolism — water, energy and GHG,
  waste and wastewater treatment. Air-pollutant concentrations
  themselves stay in §2; water chemistry stays in §4; contaminants
  stay in §6; soil chemistry stays in §9.
- **Aquaculture — fish farming:** dissolved oxygen in the production unit
  (concentration, % saturation, dawn minimum) and unionised ammonia and
  nitrite in the unit, with pH and temperature alongside; water temperature
  against the species optimum; daily and cumulative mortality and disease
  incidence with the veterinary health plan; sea-lice load where salmonids
  are caged; eFCR (with FFDR/PRE where the standard requires them);
  stocking density and standing biomass; effluent nitrogen and phosphorus
  load per tonne of production and effluent BOD/COD/solids; benthic
  sulphide and redox beneath and beyond the cage array; receiving-water
  state against a reference site; escape events and estimated unexplained
  loss; water abstraction and use per tonne; fallowing between cycles;
  wild-fish interaction (lice and introgression risk) at production-area
  scale; operational welfare indicators as research-grade only.
- **Desert / arid lands:** UNEP aridity index and seasonal water balance;
  soil-adjusted fractional vegetation cover and perennial-vs-ephemeral
  share, always read against rainfall; rain-use efficiency and the SDG
  15.3.1 desertification extent where desertification is the question;
  biological soil crust cover and disturbance; salinisation trajectory
  (ECe trend, salt-affected share) and sodicity where irrigation or shallow
  groundwater is present; sand drift potential and dune migration where
  dunes threaten an asset; dust-storm event frequency by WMO visibility
  class; oasis extent and grove condition paired with groundwater depth,
  trend and salinity; ephemeral-water flow days and playa inundation;
  desert endemic-species occupancy and water-point access; arid rangeland
  utilisation against the forage pulse.
- **Tundra / polar:** tundra vegetation composition and PFT shares
  (dwarf shrubs, sedges, grasses, mosses, lichens); shrub cover and
  shrubification; NDVI/MaxNDVI greening vs browning; active-layer
  thickness and its trend (ground temperature itself per §21);
  thermokarst features (thaw lakes, retrogressive thaw slumps,
  subsidence); SOC stock in tundra soils (0–30 cm); snow cover duration
  and rain-on-snow / icing events; thaw-pond and lake area; caribou /
  reindeer abundance and calving success; lemming/vole cycle state;
  migratory bird breeding success and insect emergence timing; coastal
  erosion rate where the tundra meets the sea; burned area and fire
  return interval; human infrastructure footprint as a §17 pressure;
  CO₂/CH₄ fluxes where a carbon decision is in scope.
- **Forest:** forest extent and net area change (FAO definition: >0.5 ha,
  trees >5 m, canopy >10%); forest type and biome composition, natural vs
  planted; primary and old-growth forest area and share — any loss is at
  least amber; stand age-class distribution; basal area and stem density by diameter class; forest soil organic carbon stock; aboveground biomass carbon stock (IPCC five pools; 714 Gt
  total forest carbon, FRA 2025); net carbon flux (NEE/NEP) — a sink that
  flips to a source is red; harvested area and volume against the allowable
  annual cut; forest loss by driver (Curtis et al. 2018 shares); pest and
  disease outbreak, area and mortality; forest fragmentation (core area,
  edge density, patch size); regeneration (seedling/sapling density,
  natural-regeneration share); canopy cover, stand structure and deadwood
  volume per §10; tree and shrub health per §11; forest fire regime per
  §10; protected-area share and certified-forest share.
- **Cropland:** cropland extent and net area change; crop type and cropping-system
  composition, cropping intensity; crop rotation diversity and fallow share;
  tillage system share (conventional / reduced / no-till); SOC stock under tillage
  (0–30 cm) and trend; irrigation water use and efficiency; soil salinisation (ECe
  trend, salt-affected share); fertiliser N/P balance, NUE and runoff; direct N₂O
  from fertilised soil; pesticide pressure; yield and yield stability; soil erosion
  on arable land (RUSLE); field-margin and biodiversity-strip share and condition;
  crop residue fate and open-burning share; rice-paddy water regime and methane
  (paddies only); receiving-water nutrients and sediment per §5; soil condition per
  §9; landscape structure per §10; flora per §11; pollinators and soil
  invertebrates per §14; farmland birds and mammals per §15.

- **Non-peat wetlands and marshes:** wetland extent and net area change
  (Ramsar definition; 35% of natural wetlands lost 1970–2015, GWO 2018;
  loss since 1900 estimated 64–71% (Davidson 2014), contested at ~21% since 1700 (Fluet-Chouinard et al. 2023) — present as a range); wetland type composition (freshwater/brackish/salt marsh, floodplain, reed bed, sedge meadow) per §32; hydroperiod — flooded duration and
  timing (Everglades classes: sloughs 11+ months, sawgrass ridges 9–10
  months, short marshes 3–7 months); water-level regime — stage,
  amplitude, rate of change, connectivity (compartmentalisation by levees
  and canals is the red pattern); salinity regime for coastal and brackish
  marshes — trend and intrusion events (a freshwater marsh turning
  brackish is at least amber); vegetation composition — reed, sedge and
  salt-marsh grass shares (a dominant-species flip, sawgrass → cattail,
  is at least amber); sediment accretion against local sea-level rise
  (organic matter alone contributes at most ~3 mm/yr, Morris et al. 2016;
  accretion persistently below sea-level rise is red); nutrient retention
  — inflow–outflow N/P (Olentangy: P ~60%, nitrate ~40%, Fink & Mitsch;
  net export is red); waterbird use — breeding, staging, moulting counts
  (Ramsar Criteria 5 and 6; a count below its 1% flyway threshold is
  red); fish nursery function — juvenile density, growth, survival vs an
  unvegetated reference (Beck et al. 2001); invasive species —
  Phragmites haplotype M (Saltonstall 2002), cattail expansion in enriched
  zones (a native haplotype lost is red); drainage and reclamation
  pressure — drained share, ditch density, conversion rate (any net loss
  of natural marsh is at least amber); surface-water quality in the marsh
  per §4 (Everglades TP criterion 10 µg/L — an Everglades number, not a
  general standard).

## 19. Indicator metadata and quality requirements

Every indicator in a build carries a metadata record:

- definition and exact variable measured (not a proxy silently renamed);
- unit, method, instrument or survey protocol, and taxonomic resolution where
  biological;
- spatial unit and temporal frequency; sampling effort and detection
  probability for species data;
- baseline period and threshold anchor (law, standard, literature, or object
  statistics) with source and date checked;
- detection limit, precision, QA flags, missing-data treatment, and known
  bias (observer, gear, satellite, or sensor drift);
- uncertainty statement and the decision the indicator can and cannot support;
- provenance ID linking the value to the deliverable's manifest.

An indicator without this record is a draft indicator. It may guide sampling
design; it must not carry a client-facing conclusion.

Threshold anchors for the 21 core indicators are tabulated in
`references/thresholds.md` (WHO, EU, USA, Russia, Japan, Germany, Denmark), with the anchor
hierarchy, per-use tables, and the operational early-warning rule; §20
applies them as bands. An anchor flagged in that file stays flagged until
re-checked against its primary source; it is not a final passport value
before that check.

## 20. Watch levels and alert rules

A watch level is an amber or red band on an indicator, set per object from
its anchor (law, standard, literature, or the object's own baseline
statistic). A breach becomes an alert only when it is sustained — the
indicator stays in the band for at least the window (`scripts/alert_bands.py`
`--window-hours`); a single spike never alerts. An observation gap longer
than the maximum gap ends the episode. Every band carries its anchor; a
band without one is refused by the script.

**The green state.** An indicator with no band breached is green: the
preventive measures are working and nothing beyond routine monitoring is
needed. Amber means the measures are insufficient — act on the cause, not
only on the level. Red means the measures have failed or the risk is acute
— act now. The public status line states the colour in plain words, with
the recommendation that follows from it.

**Anchor hierarchy.** Jurisdiction law first, then WHO or international
guidance, then literature, then the object's own baseline; where two
standards apply, the stricter binding standard governs the red band; guidance and drafts stay yellow. Every band records its
anchor, its source, and its date in the Object Passport.

**Thresholds by use.** One indicator can be green for one use and red for
another — drinking, bathing, irrigation, aquatic life. The twin's status is
set by the strictest use active on the object, and the status line names the
use that set it. Distinct from user-class thresholds below (who can operate),
this is about what the water, air, or soil is used for.

**Operational early-warning level.** The regulatory limit is red; yellow
sits at 70–80% of the regulatory limit, or on a trend that reaches the limit
within the reaction time — a builder's decision recorded in the passport with
its justification, never presented as law. See `references/thresholds.md`
§§7–8.

**Covariate-aware alerts.** A breach is logged as *explained*, not
alerted, when a named driver series (rainfall, flow, temperature) is itself
beyond its own watch level in a sustained episode overlapping the breach's
window (`scripts/alert_bands.py --explained-by driver.csv --driver-amber ...`).
Only unexplained breaches alert, set the status, and count for `--fail-on`.
The driver's own episode must be sustained for the same window — a brief
driver spike explains nothing. Explained breaches are listed separately
(`explained_breaches`), with the driver episode that explains them, so the
decision is auditable and the explanation is never silent. The driver and
its bands are named on the scenario card's Alerts field, never assumed.
(Source: Southern Water — Stormharvester learns "normal behaviour" and
silences wet-weather alarms; this is the deterministic version: a band
check on a named driver, no ML.)

**User-class operational thresholds.** One indicator, one forecast value —
but a different operational limit per decision-maker class
(`scripts/alert_bands.py --class-thresholds classes.csv`, CSV columns
class, limit, in the indicator's units, same direction as the bands). The
output gains a `class_thresholds` block: per class, the limit and whether
the latest observed value and the episode peak are within it — `can_operate`
is yes only when the class can operate now (latest value within its limit)
and could operate at the event's worst moment (peak within its limit); with
no alert episode the peak check is vacuous and only the latest value
decides. A flooded road is passable for a pickup (limit 0.45 m) while it is
not for a car (0.30 m) or an ambulance (0.35 m) — the same water, a
different verdict per class. Distinct from the per-asset clearance
(`scripts/registry.py --clearance`): the clearance is about an asset's
margin; this is about who can do what. The limits are recorded in Phase 1
onboarding, in the Object Passport (`assets/templates.md` §1): for each
decision-maker, their operational limit in the same units as the indicator.
(Source: Patos Lagoon — different user classes get different thresholds.)


## 21. Cryosphere and mountain hazards

Include this section when the object is in, or downstream of, steep
glacierised or permafrost terrain — a glacier, a glacial lake, a steep
rock-ice slope above a valley, or a settlement, road, hydropower plant or
farm below one. For all other objects the passport records "not
applicable: no glacierised or steep mountain terrain in the contributing
catchment" and the section is not carried. Where it applies, the twin
states for each indicator the last observation date and the observation
gap: a precursor panel with a stale last date is a data gap, not a clean
bill of health.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Slope surface displacement by InSAR (Sentinel-1, line-of-sight) | Whether a rock-ice slope is moving, and how fast — the direct precursor of a collapse | Core for mountain objects | Copernicus Sentinel-1 time series (12-day single-satellite repeat; 6-day with the two-satellite constellation — Sentinel-1C launched December 2024 restored the 6-day cycle, Sentinel-1A ended June 2026, Sentinel-1D launched November 2025; check the acquisition plan for the object and period); object baseline displacement series. Case value, not a threshold: up to 40 cm in 48 days preceded the Langtang Lirung collapse (ICIMOD 2026). No ground truth exists for that slope — the ICIMOD synthesis and the independent rapid assessment (Roy et al. 2026, DOI 10.1007/s12524-026-02611-x) are satellite-only, and a local SS_RMSE for the pre-collapse deformation can never be computed retrospectively (see sensor-registry S6/R09). Alert on sustained rate increase, never on one acquisition |
| Displacement rate and acceleration (derived: mm/day and change of rate) | Whether movement is speeding up — acceleration, not absolute displacement, is the failure signal | Core for mountain objects | Object baseline rate; inverse-velocity / tertiary-creep behaviour as research context (Fukuzono 1985; §20 watch levels with a weeks-long window). No universal threshold exists: the failure rate is site-specific (geology, slope, ice content) and must be set from the object's own baseline and a named source. Honest limit: the accelerating-rate signal is established for soil and rock landslides; for rock-ice avalanches it is a research hypothesis, not a demonstrated precursor — the ICIMOD synthesis does not establish that Langtang's slope deformation was accelerating in the final days |
| Glacier surface velocity and its change | Glacier flow state; acceleration or slowdown against baseline | Core where a glacier is present | Feature-tracking / InSAR velocity fields (Copernicus; NASA MEaSUREs ITS_LIVE v2.0, The Cryosphere 19:3517–3533, 2025; national glacier monitoring); object baseline |
| Glacier area, terminus position, and thinning rate | Glacier retreat and unloading of the slope; new lake formation | Conditional — where glacier change drives lake formation or slope unloading | Repeat optical/SAR mapping; Randolph Glacier Inventory (RGI 7.0, 2023; doi:10.5067/f6jmovy5navz) and GLIMS as the outline baseline — note the RGI is a snapshot, not designed for glacier-by-glacier rates of area change, so rates come from repeat mapping against it; national glacier inventory; object baseline |
| Glacier mass balance: annual net mass balance, m w.e./yr | The core climate variable for glacier state — whether the glacier is gaining or losing mass overall | Core where a glacier is present | WGMS global glacier mass-balance series (GCOS core climate variable); geodetic + glaciological methods; object baseline and trend. Speed, area and thinning are not substitutes: a glacier can thin while advancing, or slow while losing mass |
| Glacial lake level, area, and volume; lake growth rate | GLOF hazard state and trajectory | Core where a glacial lake exists | Repeat satellite mapping (optical + SAR) plus gauge where installed; object baseline and rate of rise; UNDP/ICIMOD dangerous-lake assessments as the screening source |
| Moraine-dam stability: crest freeboard, seepage, dam geometry, ice core | Whether the natural dam holding a glacial lake is degrading | Conditional — where a moraine-dammed lake exists | Field survey + repeat DEM; freeboard against design storm; UNDP/ICIMOD dangerous-lake assessments as the screening source (2020 assessment: 47 glacial lakes classified potentially dangerous across the Koshi, Gandaki and Karnali basins — 21 in Nepal, 25 in Tibet AR China, 1 in India; the 2026 project prioritises four lakes for lowering — Thulagi, Lower Barun, Lumding Tsho and Hongu-2). A shrinking freeboard is the warning, not a single number |
| River damming / barrier-lake formation and breach watch | Whether a collapse has dammed a river, and whether the dam is about to breach — the secondary-flood mechanism | Conditional — where a collapse can reach a river above exposed reaches | Satellite + gauge detection of a new lake and of a sudden level drop downstream; breach is the flood trigger, so the watch level is the dam's presence, not the river's normal state |
| Permafrost ground temperature; rock-glacier velocity | Whether frozen ground is warming and thawing — the slow destabiliser of steep rock slopes | Conditional — where permafrost terrain is present | Borehole ground-temperature series per GTN-P (Thermal State of Permafrost, TSP); rock-glacier velocity from InSAR / feature tracking; object baseline and trend. Active-layer thickness is §29 — cross-reference, do not duplicate. No universal threshold: warming at depth can precede surface change by years |
| Air temperature at glacier elevation; freezing-level altitude; positive degree-days | Thermal pressure on ice and permafrost; the background that raises risk | Core | Station + reanalysis (ERA5); object baseline and trend. Honest limit: a pressure, not a trigger — no temperature value predicts the day of a collapse |
| Precipitation totals and intensity; rain-on-snow events | Water input and loading on snow and slopes | Core; see also §1 | National hydrometeorological practice; object baseline; rain-on-snow recorded as a named event class |
| Micro-seismicity and icequakes (event rate, magnitude distribution) | Cracking and slip inside ice and rock — a possible short-term precursor | Research | Seismic-network records where they exist; no validated operational threshold; results are research-grade until validated for management use |
| River turbidity and suspended-sediment load upstream of exposed reaches | The "something already happened upstream" signal | Conditional — where downstream exposure exists; see also §3/§4 | Object baseline; sustained exceedance under §20. A sharp sustained rise is the collapse signal, not a water-quality event |
| Downstream river level / stage and discharge (warning function) | The evacuation warning — effectively no lead time near the source, hours far downstream | Core for rivers; see also §3 | National hydrometric practice; pre-agreed evacuation trigger levels per §20 user-class thresholds (different limits per decision-maker class). Case values from Langtang (ICIMOD 2026): the collapse struck at 08:37 NST and the surge reached the border corridor in ~7 minutes; SMS alerts went out at 09:15–09:16, after the corridor was already hit; the flood wave reached Galchhi at 10:28, Malekhu at 11:50, Mugling at 13:00 and Devghat at 15:20 — near-source lead time was effectively zero, far-downstream lead time was hours |
| Snowpack depth, snow-water equivalent, and avalanche danger level | Snow load and avalanche hazard | Conditional — cold climates; see also §1 | Hydromet station practice; national avalanche-service danger scale. Avalanche danger is a forecast product, not a measured state — state its source and scale |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is different:
for a slow precursor such as deformation, the window is **weeks**, not
hours, and the alert logic is on **rate and acceleration**, not on an
absolute value. A deformation episode ends when the rate returns to
baseline for the window, or when the observation gap exceeds the maximum
gap set in the Object Passport (for example two Sentinel-1 revisit
cycles): a gap beyond it ends the episode and the indicator is recorded
as stale, never as quiet. The
covariate-aware rule (§20) applies in reverse for temperature: a
temperature breach does not "explain away" a deformation breach — heat is
a pressure that raises the risk, not an explanation that cancels the
warning. The user-class thresholds (§20) are the evacuation levels: the
same river level can mean "evacuate the riverside settlement" for one
class and "stop hydropower intake" for another; both limits are recorded
in Phase 1 onboarding in the Object Passport.

### What this section does NOT do

- It does **not predict the day or hour of a collapse**. It watches
  precursors and states the lead time each one gives: weeks for
  deformation, effectively none near the source and hours far downstream
  for river level (Langtang: the surge reached the border corridor in
  ~7 minutes; the flood wave took ~1 hour 50 minutes to reach Galchhi
  and ~6 hours 40 minutes to reach Devghat). A twin that claims a
  collapse date from these indicators is over-claiming and must be
  refused at the Phase 4 verification gate.
- It does **not replace a geotechnical or glaciological hazard assessment
  or an official warning system**. It is an interface: it ingests hazard
  monitoring (InSAR, lake surveys, seismic networks, gauges), turns it
  into watch levels and pre-agreed trigger–action–response plans for the
  twin's object and the people downstream, and records the handoff to the
  responsible authority. The twin never issues a public evacuation
  warning itself.
- It does **not set a universal deformation threshold**. There is none.
  The 40 cm in 48 days before Langtang is a case value from one slope,
  not a standard. Every threshold is object-specific, set from the
  object's own baseline, and carries its named source and date.
- It does **not treat a satellite gap as safety**. Sentinel-1 revisits
  every 12 days as a single satellite and every 6 days as a
  two-satellite constellation; a fast acceleration can develop between
  passes, and InSAR measures line-of-sight displacement only (not full
  3D), is practically insensitive to north–south motion, and
  decorrelates over snow and vegetation and in steep radar shadow
  (ascending and descending passes together mitigate the geometry
  limits only partly). The twin states the last observation date; a
  stale panel is a data gap.
- It does **not confuse the two mechanisms**. A lake panel does not warn
  of a slope collapse, and a slope panel does not warn of a lake breach.
  Langtang was a slope collapse whose debris dammed the Lhende Khola
  and left two temporary lakes downstream — but the flood itself was
  the debris surge, not a lake breach (the two lakes breached on 28 and
  31 August without secondary disaster); a GLOF is a lake that breaches
  its own dam. Both panels are needed, and a clean lake reading says
  nothing about the slope above it.
- It does **not use temperature as a trigger**. Temperature, freezing
  level and degree-days are pressures that raise the background risk.
  No temperature value is a collapse warning, and the "one degree
  dislodged the glacier" framing is not supported: the cause is not
  established, and rock weakness and glacier change are in the causal
  picture alongside warming.
- It does **not promote research-grade indicators to warnings**.
  Micro-seismicity and icequake forecasting stay Research until a
  validated operational threshold exists for the object.

Scope boundary: this section is a Conditional module, included only when the object is in or below steep glacierised terrain — with interface discipline built in: the twin ingests external hazard data (InSAR, lake surveys, seismic networks, gauges), never claims to be the warning authority, and records every handoff to the responsible authority. The decision is recorded in the Object Passport at Phase 1.

## 22. Steppe and natural grassland

Include this section when the object is natural steppe or grassland, or a
mosaic in which natural steppe is a named component — a steppe reserve, a
grazed rangeland, a steppe–wetland complex, or a farm whose pastures include
never-ploughed steppe. For all other objects the passport records "not
applicable: no natural steppe or grassland in the object" and the section is
not carried. Where it applies, the twin states for each indicator the last
observation date and the observation gap: a grazing or fire panel with a
stale last date is a data gap, not a clean bill of health. Steppe is a
slow system on a fast calendar: vegetation and soil indicators are read
seasonally at most, and a trend needs repeat surveys over years — one
survey reports a state, never a trend.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Steppe vegetation composition: share of native perennial grasses (notably *Stipa* spp.), forbs, legumes, annuals and weeds; PFT shares | Whether the community is still steppe or sliding toward weed/annual dominance — the composition signal, not the cover signal | Core | Fixed-plot or transect protocol; PFT shares per §11 (`scripts/diversity.py pft`); object baseline. Shares from one quantity only — cover or counts, never mixed |
| Vegetation cover by stratum; bare ground, litter and biological soil crust share | Erosion protection and surface state; bare ground is the early warning | Core; see also §9/§11 | Field protocol + remote-sensing cross-check; IIRH bare-ground indicator (Pellant et al. 2000/2020, indicator 4) and LFA soil-cover features (Tongway & Hindley 2004). Object baseline; direction over years matters more than one value |
| Aboveground biomass / forage yield and its trend (field clipping; NDVI/EVI as proxy) | Productivity and the forage base for grazing and wildlife | Core | Object multi-year baseline; NDVI/EVI per §11 with field calibration for biomass claims — no satellite-only biomass claim. IIRH annual production (indicator 15) |
| Grazing intensity: stocking rate (livestock units/ha) against the site's carrying capacity; grazing pressure index | Whether grazing is within what the site can carry — the central management number for steppe | Core where grazing occurs | Farm/herder records + carrying capacity from the ecological-site description or national rangeland practice; object baseline. No universal stocking rate exists: carrying capacity is site-specific (soil, climate, vegetation type) and must be set from the object's own baseline and a named source |
| Grazing utilisation: proportion of annual forage consumed; residual stubble height / post-grazing cover | How hard the animals actually ate — the check on the stocking-rate number | Conditional — grazed objects | Field protocol (utilisation cages / paired grazed–ungrazed plots); object baseline. Starting anchor, not a standard: the rangeland profession's long-standing "take half, leave half" rule of thumb — a 50% proper-use factor on annual growth (Univ. of Arizona Extension; Wyoming Extension B-1320) — with the documented caveats that it is commonly misunderstood (only ~25% of production is actually available to livestock once trampling, wildlife and waste are counted) and that lower rates apply in arid conditions. Set from the object's own baseline and a named source |
| Soil organic carbon stock in steppe soils (0–30 cm), chernozem where present; SOC trend | Soil health and carbon storage — steppe soils are among the world's largest SOC stores | Core | FAO Global Assessment of Soil Carbon in Grasslands (baseline SOC stocks, 0–30 cm); UNCCD LDN carbon-stocks sub-indicator (SDG 15.3.1). Case value, not a threshold: FAO estimates that raising SOC by 0.3% in the 0–30 cm layer over 20 years of improved management could sequester 0.3 t C/ha/yr. Object baseline; trend over 3–5+ years |
| Soil erosion features: rills, water-flow patterns, erosional pedestals/terracettes, gullies, wind scour and blowouts, depositional areas | Whether soil is being lost, and by water or wind | Core | IIRH indicators 1, 2, 3, 5, 6 (Pellant et al., TR 1734-6 v5, 2020); field survey protocol; object baseline. A new gully or blowout is at least amber |
| Landscape function indices: soil stability, infiltration, nutrient cycling (LFA) | Whether the soil surface still holds water and cycles nutrients — the functional summary of the surface indicators | Conditional — where a field team can run LFA; Research where only remote sensing exists | Tongway & Hindley (2004) Landscape Function Analysis: 11 soil-surface features → three indices (stability, infiltration, nutrient cycling). Indices are 0–100 scores from the LFA workbook; no universal pass mark — set from the object's own baseline and reference site |
| Virgin (never-ploughed) steppe area and conversion rate; share of steppe never ploughed | How much true steppe is left and how fast it is being lost to the plough | Core | Land-cover time series (CORINE / national products; §9/§10); UNCCD LDN land-cover-change sub-indicator. Any new ploughing of virgin steppe is recorded as a conversion event, not a gradual change |
| Shrub / woody encroachment: woody cover share and its trend | Whether steppe is closing into scrub — a degradation pathway that also cuts forage and bird habitat | Core | Repeat remote sensing + field check; UNCCD LDN interpretation matrix names woody (bush) encroachment as a case where the one-out-all-out rule needs care. Object baseline; trend, not one value |
| Steppe fragmentation: patch size distribution, core area, road/track density, edge density | Whether the steppe still works as one landscape or as isolated fragments | Conditional — where conversion or infrastructure is present; see also §10 | Landscape-ecology metrics per §10, classes named; object baseline |
| Fire: burned area, fire season, fire return interval | The disturbance regime — too frequent fire and too rare fire are both degradation | Core for fire-prone steppe; see also §10 | Remote-sensing fire products (MODIS burned area) + management/fire-service records; object baseline and reference interval. Case values, not thresholds: European forest-steppe regions are characterised by low-frequency, cool-season, low-severity fires with an average return interval of several decades (Valkó et al. 2018, citing Archibald et al. 2013; Lysenko 2008); sagebrush steppe historically 60–110 years, now under 5 years where cheatgrass has invaded. No universal steppe fire interval exists |
| Post-fire recovery: time for cover and composition to return to pre-fire state | Whether the steppe recovers or ratchets down after each fire | Conditional — where fires occur | Repeat plot/remote-sensing monitoring; object baseline. Recovery slower than the reference interval is the warning |
| Steppe bird indicators: great bustard presence/counts and breeding success; steppe eagle, demoiselle crane, saker falcon occupancy where present | Habitat quality across scales — bustards need large, open, low-disturbance steppe; their absence is a landscape verdict | Core for conservation objects; Conditional for grazed steppe | National monitoring-scheme / eBird-type protocols per §15; IUCN Red List status as context (great bustard *Otis tarda* Vulnerable; steppe eagle *Aquila nipalensis* Endangered). Sensitive locations generalised per §11/§15. A declining trend is red regardless of absolute numbers |
| Burrowing small mammals: bobak/tarbagan marmot colony density and occupancy; ground-squirrel abundance | Keystone engineers of the steppe — their colonies shape grassland structure and feed eagles; their loss is an early warning | Conditional — where present | Colony counts / burrow surveys; camera-trap or track protocol per §15; object baseline — trend vs the object's own baseline over ≥3 survey rounds; no universal density threshold exists (IUCN criteria use decline rates, extent of occurrence / area of occupancy and mature-individual counts, not density; the Russian 1983 census guidelines are a survey method; no density standard was found in the published literature). Status context: tarbagan *Marmota sibirica* Endangered (IUCN criterion A2ad), bobak *Marmota bobak* Least Concern (Bazhenov 2019, DOI 10.24189/ncr.2019.008). Restoration-design minimum, not a status threshold: ≥10 families and ≥50 individuals for a successful reintroduction (Enkhsaikhan et al. 2021, Proc. Inst. Biol. 37:30–36, DOI 10.5564/pib.v37i1.3137). Separate epidemiological cut-point: heavy rainfall raises plague risk only at ≥0.63 marmots/ha (Xu et al. 2023, Sci. Rep. 13:11906, DOI 10.1038/s41598-023-38966-1) — a plague-risk signal, not a population-status standard. Literature case values are not standards (e.g. 2.0–3.0 habitable holes/ha for tarbagan in the Dzeren valley before the mid-20th century; bobak family density 0.4/ha on favourable habitat, 0.1/ha on marginal habitat). Current marmot density (individuals/ha) for a named object is still unpublished — see the Daursky worked example. Published context, not a Daursky value: tarbagan densities across the species' range are 1–7 ind/ha (IUCN Red List species account, Zenodo record 6819035); a named-object comparator in Mongolia is Hustai National Park, ca. 1.27 ind/ha (13,213 marmots on 10,380 ha, Todgerel 2020, as cited in the marmot-decline literature; the 13,213 / 10,380 ha figures are corroborated by the citing paper's text, the primary Todgerel 2020 document was not consulted). Next source for Daursky: the reserve's own «Летопись природы» / DIPA joint-expedition counts (families plus occupied colony area). |
| Grasshopper / locust outbreak density and area affected | Outbreak pressure on forage and neighbouring crops; a steppe event with off-site consequences | Conditional — outbreak-prone regions | National plant-protection-service outbreak records; object baseline. Density classes for locusts from the FAO Desert Locust Bulletin glossary (adults per 400 m foot transect): isolated <25/ha (0–1 adult), scattered 25–500/ha (1–20 adults), group ≥500/ha (20+ adults) — defined for Desert Locust (*Schistocerca gregaria*); steppe grasshopper thresholds (e.g. Italian locust) come from the national plant-protection service, not from these classes |
| Land-degradation composite: share of land degraded under SDG 15.3.1 (one-out-all-out across land cover, land productivity, SOC) | The headline verdict — degraded if any one of the three sub-indicators shows degradation | Core for decision twins | UNCCD Good Practice Guidance for SDG indicator 15.3.1; the three sub-indicators are land-cover change, land productivity (NPP) and SOC stocks. One-out-all-out (1OAO): an area is degraded if any sub-indicator degrades — with the documented caveat that 1OAO can misread deliberate remediation (e.g. removing invasive plants lowers biomass) |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is
**seasonal to multi-year**, not hours: steppe vegetation, SOC and woody
cover are read once or twice a year, and a trend needs repeat surveys, so
the window is set in seasons or years in the Object Passport, and a single
year's low biomass never alerts on its own. An observation gap longer
than the maximum gap ends the episode and the indicator is recorded as
stale, never as quiet. The covariate-aware rule (§20) applies in its
normal direction here: a drought episode (SPI/SPEI, §1) that is itself
sustained can *explain* a biomass or cover breach — the breach is logged
as explained, not alerted — but drought never explains a grazing breach:
a stocking rate above carrying capacity is a management decision, not a
weather event, and the driver that "explains" it does not exist. The
user-class thresholds (§20) are the grazing and fire limits: the same
stocking rate can mean "reduce the herd now" for the herder, "suspend the
grazing lease" for the reserve manager, and "no action" for the
conservation officer watching bustard breeding — all three limits are
recorded in Phase 1 onboarding in the Object Passport, in the same units
(livestock units/ha, or hectares burned per season).

### What this section does NOT do

- It does **not cover cropland**. A ploughed field is a §17 land-use
  change, and its crops belong to the skill's existing "field" panels.
  This section watches the steppe that remains, and records each
  conversion as a loss event.
- It does **not set a universal stocking rate, fire interval, or SOC
  threshold**. There is none. Carrying capacity depends on soil, climate
  and vegetation type; the fire interval depends on the steppe type
  (forest steppe burns on a scale of decades; sagebrush steppe
  historically on a scale of 60–110 years); SOC depends on soil type and
  depth. Every threshold is object-specific, set from the object's own
  baseline, and carries its named source and date.
- It does **not treat a green satellite image as a healthy steppe**.
  NDVI/EVI rise with weeds and annuals as readily as with native
  perennials; a green field of invasive annuals is not steppe recovery.
  Composition (PFT shares, *Stipa* share) is the check on the greenness
  number, and a biomass claim without field calibration is refused.
- It does **not confuse drought with overgrazing**. A dry year lowers
  biomass everywhere; overgrazing lowers it where the animals are, and
  leaves the signatures — bare ground, pedestals, litter loss, weed
  invasion — that drought alone does not. The twin records the drought
  covariate (§1) alongside the grazing indicators so the two are never
  read apart, and never lets one explain away the other silently.
- It does **not promote a single bird species to a whole-assemblage
  verdict**. The great bustard is a flagship and a landscape indicator,
  but research on Iberian agro-steppes found it is not a good surrogate
  for all agro-steppe species of conservation concern; further indicator
  species are needed to represent the assemblage. The twin carries a
  small set of steppe birds and mammals, not one mascot.
- It does **not use the LDN one-out-all-out rule blindly**. The UNCCD
  guidance itself warns that 1OAO can produce a counterintuitive
  verdict — for example, removing invasive plants reduces biomass, which
  reads as productivity loss, while the change is in fact remediation.
  The twin records the three sub-indicators separately and names the
  reason whenever the composite and the field evidence disagree.
- It does **not treat the qualitative rangeland-health rating as
  monitoring**. The IIRH 17-indicator protocol (Pellant et al.) is a
  rapid, qualitative, moment-in-time assessment; its authors state it is
  not to be used for temporal monitoring. The twin uses its indicators as
  the field checklist and tracks quantitative measures over time; a
  single IIRH rating is a state, never a trend.

Scope boundary: this section is a Conditional module, included only when the object contains natural steppe or grassland — with interface discipline built in: the twin ingests external monitoring frameworks (UNCCD LDN reporting, national rangeland monitoring, FAO grassland SOC assessment, IIRH field protocols), never claims to set the stocking rate or the burn plan itself, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

Worked example (Daurian steppe, transboundary Landscapes of Dauria — Russian-side data): gazelle counts and marmot family counts are now published values (see worked example): Daursky + Dzeren Valley protected areas, June 2020 total count 18,898 gazelles in 475 groups, density 3.30/km², estimated 21,701 (95% CI 20,616–22,785) (Buuveibaatar et al. 2024, Oryx 58(6):759–768, DOI 10.1017/S0030605323001515); tarbagan families in SE Transbaikalia 3,300–4,100 (9,200–11,500 adults), Daursky buffer zone NE of Lake Zun-Torey 75–85 families, Daursky Reserve at Lake Barun-Torey ~30 families, mean family size 2.8 ± 0.3 (Bazhenov 2019, Nat. Conserv. Res. 4(1):83–92, DOI 10.24189/ncr.2019.008). Remaining [NEXT DATA] gaps: a Daursky-reserve-only gazelle total, current marmot density (ind/ha), burned area, and SOC values — not invented. Marmot context (not a Daursky value): species range 1–7 ind/ha (IUCN species account, Zenodo record 6819035); Hustai National Park comparator ca. 1.27 ind/ha (13,213 marmots / 10,380 ha, Todgerel 2020, as cited in the marmot-decline literature; the 13,213 / 10,380 ha figures are corroborated by the citing paper's text, the primary Todgerel 2020 document was not consulted). Next source for the Daursky density: the reserve's «Летопись природы» / DIPA joint-expedition counts (families plus occupied colony area).

## 23. Livestock farm as an ecosystem

Include this section when the object is a livestock farm, a grazed holding,
or a mosaic in which livestock farming is a named component — a dairy or
beef farm, a sheep holding, a mixed crop–livestock farm, a pastoral
rangeland holding. For all other objects the passport records "not
applicable: no livestock farming in the object" and the section is not
carried. Where it applies, the twin states for each indicator the last
observation date and the observation gap: a nutrient-balance or methane
panel with a stale last date is a data gap, not a clean bill of health.
The farm is a fast system on a slow calendar in two directions at once:
a slurry store can overtop in a week, while soil organic carbon and
pasture composition need years of repeat surveys — so the window is set
per indicator in the Object Passport, and a single season's forage yield
never alerts on its own.

Cross-references below are deliberate: where §1–§17 already carry an
indicator, this section points at it and adds only the farm-specific
reading.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Pasture condition: sward composition (PFT shares per §11), cover, bare ground, weed/invasive share; forage yield and its trend | Whether the pasture is still productive grassland or sliding toward bare ground and weeds — the farm's ecological base | Core where pasture present; see also §22 | Field protocol + remote-sensing cross-check; object multi-year baseline; NDVI/EVI per §11 with field calibration for biomass claims — no satellite-only biomass claim |
| Stocking rate against carrying capacity (livestock units/ha) | Whether grazing is within what the site can carry — the central number for the farm, shared with §22 | Core where grazing occurs; see §22 | Method and anchors as in §22 (grazing-intensity row — carrying capacity from the ecological-site description or national rangeland practice; no universal stocking rate). Farm reading: herd records per paddock and season against the farm's own carrying-capacity estimate. Case value, not a standard: a 2025 assessment of 100 Mongolian soum found 58 exceeded pasture carrying capacity, on average by about 20%, and in the most extreme cases by two to three times |
| Grazing utilisation: proportion of annual forage consumed; residual stubble height / post-grazing cover | How hard the animals actually ate — the check on the stocking-rate number | Conditional — grazed objects; see §22 | Method and starting anchor as in §22 (grazing-utilisation row — the "take half, leave half" rule of thumb with its documented caveats; not a standard). Farm reading: utilisation per paddock and grazing rotation, read alongside the stocking-rate row above |
| Soil organic carbon stock under pasture (0–30 cm) and its trend | Soil health and carbon storage under grazing | Core; see §9/§22 | Method and anchors as in §22 (SOC row — FAO Global Assessment of Soil Carbon in Grasslands; UNCCD LDN carbon-stocks sub-indicator) and §9. Farm reading: grazed against rested or ungrazed paddocks, same depth (0–30 cm); object baseline; trend over 3–5+ years |
| Soil compaction under grazing: bulk density, penetration resistance, infiltration rate (top 0–10 cm) | Whether trampling is sealing the soil surface — the grazing-specific soil damage that §9 does not separate out | Core where grazing occurs; see §9 | National soil survey methods; object baseline (grazed vs ungrazed or rested comparison). Case values, not thresholds: long-term grazing in Oklahoma tall-grass prairie cut surface infiltration from 28.5 cm/day (ungrazed) to 5–7 cm/day under grazing, with bulk-density and penetration increases confined to the upper 10 cm; a literature review finds treading effects are confined to the soil surface (0–0.1 m) and are short-lived. No universal compaction threshold exists |
| Manure production: volume/mass of manure and slurry produced, by type and store | The size of the nutrient stream the farm must handle — the input to every balance below | Core | Farm records (animal numbers × standard excretion coefficients from the national inventory); object baseline. Coefficients come from the jurisdiction's inventory, never from memory |
| Farm nutrient balance: N and P inputs vs outputs, farm-gate surplus (kg N/ha/yr, kg P/ha/yr) | Whether the farm accumulates nutrients that must go somewhere — soil, water or air | Core | FAO LEAP nutrient-flow guidelines (nutrient balance = inputs − outputs; nutrient use efficiency = outputs/inputs × 100). Object baseline; trend matters more than one value. Case anchor, not a standard: the EU Nitrates Directive caps livestock manure applied to land at 170 kg N/ha/yr (derogations to 250 kg N/ha/yr exist in some Member States under conditions) |
| Manure storage capacity and freeboard: months of storage; freeboard vs minimum; store integrity (cracks, leaks, seepage) | Whether the farm can hold its manure until spreading is safe — the overflow risk in one number | Core where slurry/manure is stored | Jurisdiction's storage rules; object baseline. Case anchors from England (not standards elsewhere): SSAFO requires at least 4 months' slurry storage; NVZ rules require 22 weeks for cattle slurry and 26 weeks for pig slurry; freeboard minimum 300 mm for steel/concrete stores, 750 mm for earth-banked stores; stores at least 10 m from inland or coastal waters (GOV.UK guidance). A store at or below freeboard in the wet season is at least amber |
| Manure application: timing, rate and method; spreading on frozen, waterlogged, flooded or snow-covered land; spreading before forecast heavy rain | Whether manure is applied when the crop and soil can use it, or when it will run off or leach | Core where manure is spread | Jurisdiction's rules (closed periods, buffer distances, no-spread conditions); farm application records. Case anchor from England's Farming Rules for Water: applications must meet the nutrient needs of the crop or soil, not empty the store; spreading to empty a full store is a breach. No-spread conditions (frozen, waterlogged, flooded, snow-covered land) are the standard no-spread set in EU practice |
| Nitrate leaching to groundwater and surface water: nitrate in farm drains, boreholes and receiving water | Whether farm nitrogen is reaching water — the downstream verdict on the balance above | Core; see §5/§8 | National standards; object baseline. Anchor: the EU Groundwater and Drinking Water Directives set the maximum allowable nitrate concentration at 50 mg NO3/l; EEA reporting for 2016–2019 found 14.1% of groundwater monitoring stations exceeded it. The farm's own drain/borehole trend is the alert, not the regional mean |
| Ammonia emissions: NH3 flux from housing, stores and spreading (kg NH3/yr or per livestock unit) | The farm's nitrogen loss to air — and the deposition pressure on neighbouring habitats | Core for housed livestock and slurry systems; see §2 | National emission inventory methods (e.g. EMEP/EEA Guidebook factors); object baseline. Context, not a farm threshold: agriculture is responsible for about 93% of total ammonia emissions in the EU (EEA assessment). No farm-level ammonia concentration standard exists; the anchor is the inventory factor and the farm's own trend |
| Methane emissions: enteric fermentation + manure management (kg CH4/yr or per livestock unit; CO2-eq with the GWP stated) | The farm's largest climate signal, split by source so the two are never merged | Core for ruminant farms; Conditional for pigs/poultry | IPCC inventory methods (Tier 1/2/3 by data available); GWP100 stated on the term — IPCC AR6: 27.0 for non-fossil (biogenic) methane, 29.8 for fossil methane. Context: enteric fermentation 39% and manure 10% of livestock supply-chain emissions (Gerber et al. 2013); the twin reports the farm's own flux, never the global share as a farm value |
| Nitrous oxide emissions from manure and fertilised pasture (kg N2O/yr) | The farm's second climate gas, from the same nitrogen the balance tracks | Conditional — where manure or fertiliser N is applied | IPCC inventory methods; GWP100 273 (AR6). Context, not a farm value: livestock's long-shadow assessment attributed about 65% of anthropogenic N2O largely to manure (Steinfeld et al. 2006) |
| Farm water use and effluent: drinking water, wash water, yard runoff; effluent volume, BOD/COD, E. coli where it reaches water | Whether the farm's water demand and its dirty water are accounted for — the farm's water footprint in one panel | Core where livestock are housed or wash water is produced; see §3/§4/§5/§13 | Farm meter/records; national standards for the receiving water. Context: livestock production accounts for more than 8% of global human water use, mostly for irrigating feed crops (Steinfeld et al. 2006) — a sector figure, not a farm benchmark; the farm's own metered use and its trend are the indicator |
| Slurry-lagoon / store integrity and overflow risk: structural condition, freeboard trend, rainfall on the store, spill history | Whether the store will hold through the wet season — the single-point failure of the farm | Core where a lagoon or store exists | Inspection protocol + freeboard log; rainfall covariate (§1). Any recorded spill or overtop is red and is recorded as an event, not a trend |
| Livestock stream access and riparian condition: fenced vs open stream frontage; buffer width, continuity and condition; bank damage, faecal input points | Whether animals can stand in the water — the direct faecal and bank-erosion pathway | Core where a watercourse crosses or borders the farm; see §10 | Riparian guidance; object baseline. Case anchors, not standards: US EPA review of buffer-width science and state/federal guidance — buffers generally 15–30 m wide; NYSDEC three-zone concept totals at least 100 ft (~30 m) for minimum water-quality protection. Invertebrate diversity in UK riparian margins rose only where margins were ≥5.4 m wide (SRUC). No universal buffer width exists |
| Farm-boundary biodiversity: field margins, hedgerows and their condition; pasture-bird occupancy and breeding success; pollinator strips where present | Whether the farm's edge still holds wildlife — the ecosystem indicator, not a farm-management score | Conditional — where margins/hedgerows exist; see §11/§14/§15 | National monitoring-scheme / transect protocols per §11/§14/§15; object baseline. A declining trend is red regardless of absolute numbers. Hedgerow and margin extent are state, not management effort |
| Land-use change on the farm: pasture ploughed to arable, wetland drained, new hard standing | Whether the farm's ecological base is shrinking | Core; see §9/§10/§17 | Land-cover time series; object baseline. Any new ploughing of never-ploughed pasture is recorded as a conversion event, not a gradual change (see §22) |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is set **per
indicator**, because the farm runs on two clocks at once. Slurry freeboard,
store integrity and spill events run on a **days-to-weeks** window: a lagoon
at its freeboard limit during a wet week is amber now, and a spill is red
on the day it happens, not after a window — an event, not a trend. Nutrient
balance, nitrate in drains, methane and ammonia fluxes run on a
**seasonal-to-annual** window: one season's surplus never alerts on its
own, and a trend needs repeat years. SOC, pasture composition and
hedgerow condition run on a **multi-year** window, as in §22. An
observation gap longer than the maximum gap ends the episode and the
indicator is recorded as stale, never as quiet. The covariate-aware rule
(§20) applies in its normal direction here: a sustained rainfall episode
(§1) that is itself beyond its own watch level can *explain* a nitrate or
runoff breach — the breach is logged as explained, not alerted — but rain
never explains a full slurry store, a winter spreading, or a stocking rate
above carrying capacity: those are management decisions, not weather
events, and the driver that "explains" them does not exist. The
user-class thresholds (§20) are the nutrient and storage limits: the same
170 kg N/ha/yr manure cap can mean "reduce applications now" for the
farmer, "suspend the spreading permit" for the regulator, and "no action"
for the downstream water company watching a different intake — all three
limits are recorded in Phase 1 onboarding in the Object Passport, in the
same units (kg N/ha/yr, or months of storage).

### What this section does NOT do

- It does **not cover animal health, disease, breeding or feeding
  rations**. A sick animal, a breeding decision and a ration formulation
  are veterinary and farm-management matters. This section watches the
  farm's ecological state — soil, water, nutrients, emissions, pasture —
  not the animals' health or the farm's business.
- It does **not set a universal stocking rate, nutrient surplus, buffer
  width or methane threshold**. There is none. Carrying capacity depends
  on soil, climate and vegetation type; the nutrient surplus that is safe
  depends on soil, crop and hydrology; buffer width depends on slope,
  soil and what the buffer must filter (15–30 m in the US EPA review is
  a range of guidance, not a standard); methane depends on species,
  diet and system. Every threshold is object-specific, set from the
  object's own baseline, and carries its named source and date.
- It does **not treat the farm's global share as a farm value**. "14.5%
  of anthropogenic emissions" (Gerber et al. 2013) and "more than 8% of
  global human water use" (Steinfeld et al. 2006) are sector figures
  from life-cycle assessments; they describe the sector, not this farm.
  The twin reports the farm's own flux in kg/yr, never the global share
  as if it were measured here.
- It does **not confuse a full store with a spreading need**. Spreading
  manure to empty a store is not a crop need: England's Farming Rules
  for Water require every application to meet the nutrient needs of the
  crop or soil, and spreading because the store is full is a breach.
  The twin records the store level and the crop need as two separate
  indicators so one can never silently justify the other.
- It does **not treat a green pasture as a healthy pasture**. NDVI/EVI
  rise with weeds and fertiliser-driven ryegrass as readily as with a
  diverse sward; a green field of annuals is not pasture recovery.
  Composition (PFT shares, weed share, bare ground) is the check on the
  greenness number, and a biomass claim without field calibration is
  refused.
- It does **not use the nutrient balance as a verdict on its own**. A
  farm can run a surplus and still not pollute (deep soil, no drains,
  dry year) or run a balance and still pollute (a leaking lagoon, a
  winter spreading, open stream access). The twin carries the balance,
  the store, the application record and the receiving-water nitrate
  together; no single one of them is the verdict.
- It does **not promote a single bird species to a whole-farm verdict**.
  Pasture birds are a landscape signal, but one species does not
  represent the assemblage; the twin carries margins, hedgerows and a
  small set of birds together, not one mascot.

Scope boundary: this section is a Conditional module, included only when the object contains livestock farming — with interface discipline built in: the twin ingests external inventory and regulatory frameworks (FAO LEAP nutrient-flow guidelines, IPCC inventory methods, the EU Nitrates Directive, national storage and spreading rules), never claims to set the stocking rate, the spreading plan or the ration itself, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

Worked example (North Wyke Farm Platform): published values now carried (see worked example): N balance 2011–2016 (only high-sugar grass positive, +11.9 kg N ha⁻¹ a⁻¹; high-sugar grass + clover transition −248 kg N ha⁻¹ a⁻¹) (Carswell et al. 2019, Agric. Ecosyst. Environ. 283:106572, DOI 10.1016/j.agee.2019.106572); housed-cattle enteric CH₄ 170–174 g/day (Meo-Filho et al. 2023, Animal 17:100726, DOI 10.1016/j.animal.2023.100726); NH₃ 2.5 g m⁻² d⁻¹ NH₃-N on experimental out-wintering pads (Dumont et al. 2012, Agric. Ecosyst. Environ. 160:82–90, DOI 10.1016/j.agee.2012.04.019) and modelled farmlet range 4.1–9.0 kg N ha⁻¹ a⁻¹ (Carswell et al. 2019). Remaining [NEXT DATA] gaps: farm-gate P balance, a whole-platform annual CH₄ total, and a directly measured whole-farmlet NH₃ flux — not invented.

## 24. Peatlands and bogs

Include this section when the object is, contains, or directly affects a
peatland or bog — a raised bog, blanket bog, fen on deep peat, tropical
peat swamp, or a drained, extracted or rewetted peat site. For all other
objects the passport records "not applicable: no peatland in the object or
its contributing catchment" and the section is not carried. Where it
applies, the twin states for each indicator the last observation date and
the observation gap: a water-table panel with a stale last date is a data
gap, not a stable water table. Peat depth is measured by coring or probing
at the same points each survey; a single historical depth figure is a
baseline, not a current state.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Peat extent and peat depth (m), by peatland type (bog, fen, tropical peat swamp) | Whether the object is a peatland at all, and how much peat body exists to protect or lose | Core | Peat defined as organic soil ≥ 30 cm thick (convention used in the Russian national inventory — MDPI, Land 2021; other frameworks differ: the IPCC 2006 definition (Wetlands Supplement) is an organic horizon ≥ 10 cm thick, with ≥ 12% organic carbon when a horizon under 20 cm is mixed to 20 cm, plus water-saturation conditions — the 40 cm figure in the Supplement is the FAO Histosol equivalence (≥ 40 cm of peat within the uppermost 100 cm), not the IPCC definition — so the twin states which definition it uses for the object); national peat inventory / Global Peatland Map (UNEP/Greifswald Mire Centre); field coring and probing. Depth change is measured at fixed points — a one-off depth is a baseline, not a trend |
| Peat carbon stock and carbon density (t C/ha; total t C for the site) | The size of the carbon store at stake — the number the whole section exists to protect | Core | Derived: peat depth × dry bulk density × carbon concentration (standard method, IPCC Wetlands Supplement; Global Peatlands Assessment). No universal threshold — set from the object's own baseline; the anchor is the stock, not a "safe" number |
| Water-table depth in peat (mean annual, cm below surface; seasonal range; dipwell network) | The master variable: whether the peat is waterlogged and storing carbon, or aerated and oxidising | Core | Dipwell / piezometer network, manual or logged; Ramsar Briefing Note 10: rewetting raises the annual average water table to around the peat surface. Couwenberg et al. (2011): CH₄ efflux is near zero with mean annual water level below −20 cm and rises steeply above it — the −20 cm line is a documented inflection in the CH₄ response, not a management target; IPCC Wetlands Supplement Ch. 3 gives the CH₄ emission factors for rewetted peatlands by climate zone and nutrient status |
| Drainage status: ditch and canal density (km/km²) and share of area drained | How much of the peatland is under drainage pressure, and where the water table is being pulled down | Core | GIS mapping from imagery / national drainage records; object baseline. A rising ditch density is the warning; there is no universal "acceptable" density |
| Sphagnum cover (%) and peat-forming vegetation cover | Whether peat is still being formed — Sphagnum is the peat builder of bogs; its loss means the system has stopped accumulating | Core for bogs | Field quadrats / vegetation survey; national peatland condition assessment practice (e.g. IUCN UK Peatland Programme condition categories). See also §11 for general vegetation; this indicator is peat-specific because it measures the peat-forming function, not species richness |
| Peatland vegetation composition: cover of peat-forming sedges, cotton grass, and bog specialist species vs. dryland / invasive species | Direction of change: wet peat-forming community vs. drying, scrub encroachment, or agricultural weeds | Conditional — where vegetation change is the management signal | Vegetation survey; object baseline; GEST (Greenhouse gas Emission Site Types) vegetation classes as the link to GHG estimates (Couwenberg et al. 2011) |
| Net greenhouse-gas flux from peat (CO₂, CH₄, N₂O; t CO₂-C/ha/yr — multiply by 44/12 for t CO₂e/ha/yr) | Whether the peatland is a net source or sink — the climate verdict on the site | Core where monitoring exists; Conditional otherwise | Chamber or eddy-covariance measurement; IPCC 2013 Wetlands Supplement Tier 1 default emission factors by land use and climate zone, Table 2.1, Ch. 2, on-site CO₂-C from drained organic soils (cropland: 7.9 t CO₂-C/ha/yr boreal and temperate, 14.0 tropical; grassland: 5.7 boreal; temperate 5.3 nutrient-poor, 6.1 nutrient-rich deep-drained, 3.6 nutrient-rich shallow-drained; 9.6 tropical — the table splits temperate grassland by nutrient status and drainage depth, not by cool/warm climate) as the Tier 1 anchor where no site measurement exists; GEST vegetation proxy as a lower-cost estimate. See also §16 for carbon-stock accounting and §13 for methanogenesis |
| Peat fire occurrence and burnt area (ha; smouldering depth; repeat-burn frequency) | Whether drained peat is burning — smouldering peat fire is the most destructive and hardest-to-extinguish fire type on the object | Core where drained peat is present | Satellite burnt-area mapping (Landsat/Sentinel-2) + ground verification; national fire records. Case value, not a threshold: 19.8 thousand ha burnt in Moscow region peatlands in 2010 (Landsat-5 TM). A peat fire is a red watch level by occurrence, not by size |
| Peat surface subsidence rate (mm/yr) | The slow, measurable loss of the peat body under drainage — oxidation made visible as the ground sinks | Conditional — where peat is drained | Subsidence poles / levelling / InSAR; object baseline. Subsidence is a cumulative loss indicator: a steady rate over years is the signal, not a single year's value |
| Peat extraction area (ha under extraction) and extraction volume (m³/yr) | The direct removal of the peat body, and whether extraction is expanding, stable, or closed | Conditional — where extraction occurs or occurred | Concession / licence records + imagery; IPCC Wetlands Supplement peat-extraction reporting categories. Closed extraction sites are carried as "former extraction, restoration state" — see the rewetting indicator below |
| Rewetting state: share of drained area rewetted (%), ditch blocks installed (count), water-table recovery vs. pre-drainage baseline | Whether restoration is actually happening and working — the only indicator that records recovery, not loss | Core for restoration objects | Project records (ditch-block locations, water-table series before/after); Ramsar Briefing Note 10: rewetting raises the annual average water table to around the peat surface (the IPCC Good Practice Guidance wording is "the return of the water table to predrainage levels"). A rewetted site that still shows a deep water table is recorded as "rewetting attempted, not achieved", never as restored |
| Peatland condition / degradation class (near-natural / degraded / rewetted / under extraction) | The management summary: one class per management unit, carrying the judgement the other indicators support | Conditional | National classification where one exists (e.g. IUCN UK Peatland Programme, Peatland Code v2.1, October 2024: bogs — Actively eroding, Drained, Modified bog, Cropland-drained, Grassland intensive / extensive; fens — Cropland-drained, Grassland intensive / extensive, Modified fen); otherwise Ramsar degradation criteria (drainage, extraction, fire, vegetation change). The class is derived from the indicators above, never assigned by impression |
| Waterborne carbon loss from peat (DOC/POC export, t C/yr) | Carbon leaving the peatland in water — the loss pathway the flux towers do not see | Conditional — where a draining stream exists; see also §4 | Stream gauging + DOC concentration (IPCC Wetlands Supplement waterborne-carbon reporting); object baseline |
| Paludiculture / wet land use on rewetted peat (ha; crop or use type) | Whether rewetted peat supports a productive wet use instead of reverting to drainage | Conditional — where rewetted land is in productive use | Farm / project records; paludiculture as defined by Wichtmann et al. (2016): production on wet peatland while preserving the peat carbon stock. See also §17 for land-use pressure |
| Peat fire risk: combined water-table depth, drought index, and peat moisture (derived index) | The forward-looking warning — whether the site is entering a burnable state before any fire starts | Research | Derived from the water-table indicator + meteorological drought indices; no validated operational threshold exists for a combined peat-fire index — results are research-grade until validated for the object. The water-table depth itself is the operational warning; the index is not a substitute for it |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is
**seasonal**, not hourly: water-table depth is judged on the mean over the
growing season (or the annual mean), because a peatland water table
naturally fluctuates, rising above the surface in wet periods and falling
well below it in a very dry season — even near-natural tropical peat swamp
forest shows a normal range to about −0.44 m with extremes to −0.84 m
(tropical peatland rewetting trial, Sci. Rep. 2024, DOI 10.1038/s41598-024-60462-3).
A single dry-week dip is not a breach; a growing-season mean that stays
below the object's own baseline for the season is. A water-table episode
ends when the seasonal mean returns to baseline, or when the dipwell
record goes stale — a missing season is recorded as a data gap, never as
a stable water table. The covariate-aware rule (§20) applies in a
specific way here: a deep water table **explains** a high CO₂ flux — it
does not excuse it. The two indicators breach together, and the alert
stands on both; the water table is the cause, the flux is the
consequence, and neither cancels the other. The one genuine covariate
exception is CH₄ after rewetting: a CH₄ rise in the first years after
rewetting is the expected, documented response (IPCC Wetlands Supplement
Ch. 3), and a CH₄ breach in that window is recorded as "rewetting
transient, expected" with the rewetting date attached — it does not
cancel the CO₂ improvement, and it does not extend indefinitely. The
user-class thresholds (§20) are the fire and restoration decisions: the
same water-table reading can mean "raise the alarm with the fire service"
for one class and "open the ditch-block work plan" for another; both
limits are recorded in Phase 1 onboarding in the Object Passport. Peat
fire is the exception to the sustained-breach rule: a confirmed peat fire
alerts on occurrence, because smouldering peat cannot be waited out.

### What this section does NOT do

- It does **not duplicate the generic wetland, soil, vegetation or carbon
  sections**. Hydrology (§3), surface-water quality (§4), soil (§9),
  landscape/habitat (§10), flora (§11), microbiology including
  methanogenesis (§13), ecosystem services including carbon stocks and
  GHG fluxes (§16) and pressures (§17) are cross-referenced, not
  repeated. An indicator appears here only where peatland genuinely
  needs its own measurement — peat depth, peat carbon density,
  water-table depth in peat, ditch density, Sphagnum cover, rewetting
  state, peat fire. If a quantity is already measured in §3–§17, the
  twin uses that measurement and this section points at it.
- It does **not set a universal water-table target**. Ramsar's guidance
  is "around the peat surface" and the IPCC documents a CH₄ inflection
  near −20 cm, but the right water table depends on peatland type
  (bog, fen, tropical peat swamp), climate, and prior land use. Every
  target is set from the object's own baseline and carries its named
  source and date.
- It does **not treat a rewetted site as restored**. Rewetting restores
  some functions; full recovery of fauna and flora may take decades to
  centuries, and some species may never return (peatland restoration
  literature: Lode 1999 — redevelopment of a fen or bog landscape is a
  long-term process, probably centuries; Scientific Reports 2024 — full
  restoration to the original ecosystem cannot be a rapid process and may
  take some decades). The twin
  records "rewetted" only when the water table has returned to near the
  peat-forming level, and records vegetation and GHG recovery separately
  — a wet site with no Sphagnum is rewetted, not restored.
- It does **not use CH₄ alone as the climate verdict**. Rewetting raises
  CH₄ while cutting CO₂ and N₂O by far more; the net CO₂-equivalent
  balance is the verdict, and a CH₄ rise in the first years after
  rewetting is expected, not a failure. A twin that reports CH₄ without
  the net balance is misreporting the site.
- It does **not predict peat fires from a single dry week**. Fire risk
  in drained peat is a combination of water-table depth, drought and
  peat moisture over a season. The water-table indicator is the
  operational warning; the combined fire-risk index stays Research
  until a validated operational threshold exists for the object.
- It does **not claim a carbon-credit value**. Peat carbon stock is a
  physical quantity; its value as a credit depends on the certification
  scheme, the baseline, additionality and permanence rules, and the
  market. The twin reports tonnes of carbon and tonnes of CO₂e, and
  hands any credit claim to the scheme's own methodology (e.g. the UK
  Peatland Code, MoorFutures, or the EU Carbon Removals and Carbon
  Farming Regulation 2024/3012) — it never issues a credit estimate
  itself.
- It does **not promote research-grade indicators to warnings**. The
  combined peat-fire-risk index stays Research until validated; GEST
  vegetation-based GHG estimates are a lower-cost proxy, not a
  replacement for measured fluxes where a credit or a regulatory
  decision depends on the number.

Scope boundary: this section is a Conditional module, included only when the object is, contains, or directly affects a peatland — with interface discipline built in: the twin ingests external peatland data (national peat inventories, IPCC Wetlands Supplement factors, Ramsar guidance, restoration-project records), never claims to be the inventory authority or the fire authority, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

## 25. Marine and coastal

Include this section when the object is in, touches, or is driven by the
sea — open or coastal seawater, an estuary, a lagoon, a mangrove forest, a
seagrass meadow, a coral reef, a saltmarsh, or a shoreline whose position
moves. For all other objects the passport records "not applicable: no
marine or coastal component in the contributing catchment" and the section
is not carried. Where it applies, the twin states for each indicator the
last observation date and the observation gap: a bleaching panel whose last
field survey is a year old is a data gap, not a clean bill of health —
satellite heat stress can be current while the reef itself has not been
seen since the last bleaching season.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Sea-surface temperature (SST) and SST anomaly against the local climatology | The heat state of the water — the driver behind bleaching, marine heatwaves and range shifts | Core | Satellite SST (NOAA OISST / Copernicus OSTIA) plus in-situ logger where installed; anomaly against the object's own climatological baseline |
| Marine heatwave occurrence, duration and category | Whether the water has been abnormally warm long enough to count as a heatwave, and how severe | Core | Hobday et al. (2016, 2018) definition: SST above the 90th percentile of the local climatology for at least 5 consecutive days. Categories by intensity relative to the climatology-to-90th-percentile difference: Moderate 1–2×, Strong 2–3×, Severe 3–4×, Extreme >4× (Hobday et al. 2018, via Mercator Ocean / IPCC AR6 SYR) |
| Degree Heating Weeks (DHW) and NOAA Coral Reef Watch bleaching alert level | Accumulated heat stress on a reef — the operational bleaching warning | Core for reefs | NOAA Coral Reef Watch: HotSpot ≥1 °C and DHW ≥4 °C-weeks = bleaching likely (Alert Level 1); DHW ≥8 °C-weeks = bleaching with mortality likely (Level 2); alert levels 1–5 at DHW ≥4, ≥8, ≥12, ≥16, ≥20 °C-weeks (levels 3–5 added 15 December 2023). DHW is accumulated over a 12-week window above the local Maximum Monthly Mean climatology |
| Salinity and the estuarine salinity gradient (surface and bottom, along the channel) | Where fresh and salt water meet, how far salt intrudes, and whether the mixing regime is shifting | Core for estuaries and coastal lagoons | In-situ CTD / sonde profiles and fixed stations; object baseline and seasonal cycle. No universal threshold — set from the object's own baseline: the gradient, its seasonal range and the salt-intrusion limit are site-specific |
| Tidal water level, tidal range and relative sea-level trend | Inundation regime for mangroves, saltmarsh and low coasts, and the slow pressure of sea-level rise | Conditional — where inundation or sea-level rise drives the object | Tide-gauge record and satellite altimetry; object baseline and trend. No universal threshold — set from the object's own baseline and the local tidal regime |
| Seawater pH (total scale) | Acidity of the water — the direct ocean-acidification signal | Core | GOA-ON minimum measurement suite: pH on the total scale, with temperature and salinity measured alongside so the carbonate system can be calculated. Climate-quality uncertainty 0.003, weather-quality 0.02 (Newton et al. 2015 / GOA-ON). No universal threshold — set from the object's own baseline and seasonal cycle |
| Aragonite saturation state (Ω_ar) | Whether calcifying organisms (corals, shellfish) can build and keep their skeletons | Conditional — where calcifying organisms matter | Calculated from two of the four carbonate-system parameters (pH, total alkalinity, pCO₂, dissolved inorganic carbon) plus temperature and salinity (GOA-ON). Ω_ar < 1 means aragonite is thermodynamically unstable and dissolves; most surface waters are currently supersaturated (Ω_ar roughly 2–4 in warm waters, lower toward the poles; around reefs currently ~3.3 on average). Uncertainty follows the GOA-ON carbonate-ion objectives — 1% relative standard uncertainty at climate quality, 10% at weather quality — implying about 0.04 and 0.2 in Ω_ar at typical surface values. No universal threshold for harm — set from the object's own baseline and the tolerance of its calcifiers |
| Bottom-water dissolved oxygen and hypoxia extent (marine) | Whether the seabed and lower water column are losing oxygen — the marine "dead zone" signal | Conditional — where stratification, nutrients or enclosed basins create hypoxia risk; see also §4 | In-situ oxygen sensors and profiles; object baseline. Hypoxia is conventionally reported against low-oxygen bands; no universal threshold is set here — set from the object's own baseline and the jurisdiction's marine water-quality standard |
| Live hard coral cover (% of substratum) | The headline state of a reef — how much living reef-building coral is there | Core for reefs | GCRMN / AIMS Long-Term Monitoring Program methods: line-intercept or photo-quadrat transects, percent cover by category (hard coral, soft coral, algae, dead coral, sand, rubble). Object baseline and trend; no universal "good" percentage — reefs differ by region and exposure |
| Coral bleaching prevalence and post-bleaching mortality | How much of the coral bleached in a heat event, and how much of it died | Core for reefs | Field bleaching surveys during and after heat events (GCRMN / AIMS LTMP): percent of colonies bleached, partially bleached, pale or dead, by genus where possible; re-survey after the event to separate bleaching from mortality. Read alongside DHW — heat stress predicts risk, the survey records what actually happened |
| Coral recruitment (juvenile coral density) | Whether the reef is replacing itself — the recovery signal after bleaching or storm damage | Conditional — where recovery capacity is the question | Settlement tiles and small-quadrat counts of juvenile corals (GCRMN methods); object baseline. No universal threshold — set from the object's own baseline |
| Coral disease prevalence | Disease load on the reef — a stress signal that rises after bleaching and runoff events | Conditional — where disease is observed or suspected | Field survey recording disease signs by colony (GCRMN / AIMS LTMP practice); object baseline. No universal threshold — set from the object's own baseline |
| Crown-of-thorns starfish density (Acanthaster spp.) | Outbreak pressure on a reef — a predator that eats living coral and compounds bleaching losses | Conditional — Indo-Pacific reefs where the species occurs | Manta-tow and transect counts (AIMS LTMP method); outbreak status against the management authority's own outbreak definition. No universal threshold — set from the jurisdiction's outbreak criteria |
| Reef structural complexity (rugosity / relief) | The three-dimensional habitat the reef provides — what fish and invertebrates live in, and what storm waves meet | Conditional — where habitat structure or coastal protection is the question | Rugosity chain-and-tape or photogrammetry-derived relief (GCRMN / AIMS practice); object baseline. No universal threshold — set from the object's own baseline |
| Macroalgal cover on reef substratum | The coral–algal balance — a reef shifting from coral to algae is a reef losing its builders | Conditional — where phase shift is the question; see also §12 | Same transects as coral cover (GCRMN benthic categories: macroalgae, Halimeda, encrusting coralline algae, turf); object baseline and the coral:algae ratio. No universal threshold — set from the object's own baseline |
| Mangrove extent and change (area, gain/loss) | How much mangrove forest exists and whether it is growing or shrinking | Core for mangroves | Global Mangrove Watch (GMW): 2010 baseline from ALOS PALSAR radar and Landsat optical data with an Extremely Randomized Trees classifier, at 94.0% overall accuracy (Bunting et al. 2018, Remote Sens. 10:1669), refined to 95.1% with Sentinel-2 in GMW v3.0 (Bunting et al. 2022); change detection from JERS-1, ALOS PALSAR and ALOS-2 PALSAR-2, in eleven epochs 1996–2020 (1996, 2007–2010, annually 2015–2020). GMW is the official mangrove dataset used by UNEP for reporting on SDG indicator 6.6.1 (change in the extent of water-related ecosystems). Object baseline from the GMW epoch series |
| Mangrove canopy condition, fragmentation and species composition | The health and structure of the forest behind the area figure — a large but degraded mangrove is not the same as a healthy one | Conditional — where forest condition, not just area, is the question; see also §11 | Remote-sensing canopy indices (e.g. NDVI) plus field plots for species, stem density and basal area; object baseline. No universal threshold — set from the object's own baseline |
| Mangrove soil carbon stock (top 1 m) and total ecosystem carbon stock | The blue-carbon store — what is at stake if the mangrove is cleared or drowned | Conditional — where carbon accounting or climate finance is in scope; see also §16 | IPCC 2013 Wetlands Supplement (Supplement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories): top-metre soil carbon as the standard reporting profile; Tier 1 default 471 Mg C ha⁻¹ for the top metre (IPCC 2013, Ch. 4; quoted in Murdiyarso et al. 2021, Sci. Rep., and in Carbon Balance Manage. 2023). Deeper soils can hold substantially more — Bintuni Bay, Indonesia measured a further 776 Mg C ha⁻¹ at 100–300 cm, taking total soil carbon to 1,250 Mg C ha⁻¹ (Murdiyarso et al. 2021) — so sample below 1 m where conversion excavates deeper. Site-specific measurement replaces the Tier 1 default at build time |
| Seagrass extent, percent cover and shoot density | How much seagrass meadow exists and how dense and healthy it is | Core where seagrass meadows exist | Seagrass-Watch / SeagrassNet methods: quadrat percent cover (0.25 m² quadrats) and shoot density counts; meadow extent from aerial/drone/satellite mapping. Most-used methods in the published literature (500-study meta-analysis, Rising, Bulling & Sweet, iScience 29(3):114871, DOI 10.1016/j.isci.2026.114871): environmental parameters (44% of studies), percent cover (41%), biomass (40%), distribution/extent (39%), species composition (37%). Fixed-plot methods and remote underwater videography are the methods shown to reliably detect a 10% habitat loss; remote maps alone generally cannot detect losses below 30–50% (Schultz et al. 2015, PLOS ONE 10(9):e0138378). No universal threshold — set from the object's own baseline |
| Marine harmful algal bloom (HAB) occurrence, extent and cell density of the toxic species | Whether a toxic bloom is present, where it is, and whether it threatens shellfish, fisheries or bathers | Core where HAB risk exists; see also §12 | NOAA HAB Observing System (HABSOS) and HAB Operational Forecast System (HAB-OFS): satellite ocean-colour (chlorophyll anomaly) plus field cell counts — e.g. for Karenia brevis, a chlorophyll anomaly of 1 mg m⁻³ indicates a likely increase of about 10×10⁴ cells l⁻¹ (Stumpf et al. 2003; Tomlinson et al. 2004, 2009) — plus HABscope portable-microscope cell counts and public-health reports, feeding the next-30-hour beach-level respiratory-irritation forecasts (updated every 3 hours). Chlorophyll is a biomass proxy, not a cell count: the laboratory relationship (1 µg l⁻¹ chlorophyll ≈ 10⁵ cells l⁻¹) holds only when K. brevis dominates the phytoplankton and breaks down at very high concentrations (Stumpf et al. 2003), and satellite detection is limited to concentrations above ~5×10⁴ cells l⁻¹ (Tester et al. 1998) — far above the 5,000 cells l⁻¹ shellfish-closure level — so the twin never reports a cell count it did not measure. No universal threshold — alert levels come from the jurisdiction's shellfish and bathing-water rules |
| Shoreline position and coastal erosion / accretion rate (m yr⁻¹) | Whether the coast is retreating, stable or advancing, and how fast — the direct measure of coastal loss | Core for eroding or low-lying coasts | Repeat shoreline mapping (satellite, aerial, LiDAR, field survey) against a fixed baseline; rate from the object's own time series. No universal threshold — the warning is the rate and its acceleration against the object's own baseline, plus the distance remaining to the nearest asset or habitat |
| Marine litter density (beach and seafloor) | The visible pollution load on the shore and seabed | Conditional — where litter is a management concern; see also §6 | MSFD Descriptor 10: beach-litter surveys (items per 100 m of strandline, standardised protocols) and seafloor-litter trawl or dive counts. Object baseline; no universal threshold — set from the jurisdiction's standard and the object's own baseline |
| Non-indigenous marine species occurrence and spread | Whether introduced species are arriving and establishing — the invasion signal | Conditional — where shipping, aquaculture or warming brings new species; see also §14/§15 | MSFD Descriptor 2: trends in abundance, temporal occurrence and spatial distribution of non-indigenous species, in particular invasive ones; ratio of invasive to native species. Object baseline; no universal threshold — set from the jurisdiction's list and the object's own baseline |
| Underwater noise levels | The acoustic pressure on marine life from shipping, construction and seismic work | Research | MSFD Descriptor 11: introduction of energy, including underwater noise. No validated operational threshold for a twin's watch levels — record the data where it exists, do not build alerts on it until the jurisdiction sets a standard |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is different
for each panel, and the panels must not be confused with each other. For
heat, the window is already built into the metric: DHW is a 12-week
accumulation, and a marine heatwave by definition lasts at least 5 days, so
a one-day warm spike never alerts on either. For bleaching, the alert is
two-stage: the satellite heat-stress panel (DHW / alert level) is the
warning, and the field bleaching survey is the confirmation — a DHW alert
with no field survey is a warning with an unconfirmed outcome, and a field
survey showing bleaching with no DHW record is an event with an unexplained
cause; both are recorded, neither replaces the other. For slow state
indicators — coral cover, mangrove extent, seagrass cover, shoreline
position — the window is **seasons to years**: a single survey showing a
drop is a flag for re-survey, not a red level, and the watch level is set
on the **rate and direction of change** against the object's own baseline,
not on an absolute percentage. The covariate-aware rule (§20) applies in
full: a bleaching alert during a marine heatwave is not "explained away"
by the heat — the heat is the cause, and the alert stands; conversely, a
coral-cover drop during a known cyclone or flood is recorded with its
cause attached, and the recovery watch (recruitment) is what the twin
follows next. The user-class thresholds (§20) are the action levels: the
same DHW value can mean "warn bathers" for a public-health authority and "mobilise the
bleaching survey team" for a reef manager; both limits are recorded in Phase 1 onboarding in the Object Passport. Shellfish-bed closures follow biotoxin and harmful-algal-bloom thresholds, not DHW, so they are not set from a DHW reading. And the same honesty rule as in §21 holds: a stale panel is a data gap, never a clean
bill of health — a reef not surveyed since the last bleaching season is
recorded as "last observed [date], gap [n] months", not as green.

### What this section does NOT do

- It does **not duplicate the freshwater and general panels**. Nutrients,
  contaminants, sediments, general flora, phytoplankton, microbiology,
  benthos, fish and ecosystem services already live in §§4–7 and §§11–16
  and are cross-referenced, not re-listed. A twin for an estuary still
  carries §5 for nutrients and §6 for contaminants; this section adds
  only the salt, the tide and the mixing that make an estuary an estuary.
- It does **not predict the day a reef will bleach or a coast will erode**.
  DHW predicts heat-stress risk, not the date a colony bleaches; a
  shoreline rate projects a trend, not the storm that takes the next
  metres. A twin that claims a bleaching date or an erosion date from
  these indicators is over-claiming and must be refused at the Phase 4
  verification gate.
- It does **not set a universal threshold where none exists**. Salinity,
  pH, coral cover, mangrove condition, seagrass cover and shoreline rate
  have no universal "good" number. Every one of them is set from the
  object's own baseline, carries its named source and date, and is
  re-verified against the jurisdiction's law and standards at build time.
  The numbers in this section that *are* standards — DHW ≥4 and ≥8
  °C-weeks, the Hobday heatwave definition, Ω_ar < 1 — are named with
  their source and are not to be copied without it.
- It does **not treat a satellite reading as a field observation**. DHW,
  GMW extent, satellite chlorophyll and satellite SST are remote-sensing
  products with their own error: SST is a skin temperature, GMW maps are
  classifications with ~95% overall accuracy, and satellite chlorophyll
  cannot be converted into a cell count of a toxic species. The twin
  states the product, its date and its limitation; a satellite panel
  never stands in for a field survey it did not replace.
- It does **not confuse the four sub-domains**. A heat panel does not warn
  of mangrove loss, a mangrove panel does not warn of reef bleaching, a
  salinity panel does not warn of ocean acidification, and a clean coral
  reading says nothing about the seagrass meadow next to it. Each panel
  is carried only where its habitat exists, and a clean reading in one
  says nothing about the others.
- It does **not replace a marine management authority or an official
  warning system**. It is an interface: it ingests monitoring (NOAA
  Coral Reef Watch, GMW, GOA-ON, national HAB forecasts, tide gauges),
  turns it into watch levels and pre-agreed trigger–action–response
  plans for the twin's object and the people who use it, and records the
  handoff to the responsible authority. The twin never issues a public
  bleaching warning, shellfish closure or bathing ban itself.
- It does **not promote research-grade indicators to warnings**.
  Underwater noise stays Research until a validated operational threshold
  exists for the object. Coral calcification rate is not listed at all:
  it is a research measurement with no agreed operational form for a
  twin's watch levels, and belongs in a research annex, not in this
  catalogue, until a standard exists.

Scope boundary: this section is a Conditional module, included only when the object has a marine or coastal component — with interface discipline built in: the twin ingests external marine monitoring (NOAA Coral Reef Watch, Global Mangrove Watch, GOA-ON, national HAB and tide-gauge networks), never claims to be the warning authority, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

## 26. Urban ecosystems — the city as an ecosystem

Include this section when the object is a city, a district, a
neighbourhood, an urban river or water body, or an urban green-space
network — in short, when the built environment itself is part of the
system being twinned, not merely a pressure on it. For all other
objects the passport records "not applicable: no urban fabric in the
object boundary or its contributing catchment" and the section is not
carried. Where it applies, the twin states the object boundary
precisely (administrative city, district, catchment, or
neighbourhood), because every per-capita and per-area indicator in
this section depends on it, and records the reference area used for
the urban–rural comparison (the rural station, ring, or land-cover
class it is compared against) — a heat-island value without a named
reference is not a measurement.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Urban heat-island intensity, air temperature: urban minus rural reference, day and night separately | How much hotter the city runs than its countryside — the city's own climate, and the driver of heat-health risk, cooling demand and ozone formation | Core | US EPA Heat Islands programme: US cities typically 1–7 °F warmer by day, 2–5 °F warmer at night; object baseline and named rural reference. Case value, not a threshold: New York City Urban Heat Index 9.7 °F (Climate Central 2024). No universal threshold — set from the object's own baseline |
| Surface urban heat island: land-surface temperature, urban minus rural reference | Where the heat sits — hot roofs, roads and yards, and the cool islands of parks and water — at a resolution air stations cannot give | Core | Satellite land-surface temperature (Landsat / ECOSTRESS / MODIS); object baseline. Surface and air heat islands are different quantities — never report one as the other |
| Heat-health warning days and tropical nights (minimum temperature above the local heat-health threshold) | The nights that do not cool — the part of the heat island that kills, because the body cannot recover | Core where heat-health decisions are in scope; see also §1 | Local heat-health warning system / national meteorological service thresholds; object baseline. No universal temperature value — the threshold is the jurisdiction's own |
| Impervious-surface share of the object area | How much of the city cannot absorb rain — the single number that drives runoff, flooding, groundwater loss and stream damage | Core | Land-cover products (CORINE / national / Sentinel-1/2 impervious-surface mapping); object baseline. Literature anchor, not a standard: stream degradation is reported to begin at about 10% impervious cover of a watershed and to become severe at about 25% (Schueler, via US EPA) — a screening signal, not a limit |
| Stormwater runoff coefficient and runoff volume per rainfall event | How much of each rain becomes runoff, and how fast — the event-scale behaviour the impervious share only implies | Core for urban catchments; see also §3 | Rainfall–runoff monitoring / calibrated model; object baseline and event catalogue. Compare against the pre-development or target coefficient, never against a universal value |
| Combined-sewer / storm-water overflow frequency, duration and volume (per outfall and city total) | How often untreated wastewater reaches the river, for how long, and how much — the urban water system's failure mode | Core where a combined sewer exists | National discharge permits (e.g. US EPA CSO Policy / SPDES permits; EU Urban Waste Water Treatment Directive (EU) 2024/3019, Annex V point 2(a): indicative, non-binding objective that storm-water overflow represents no more than 1% of the annual collected urban wastewater load calculated in dry weather conditions — by 31 December 2035 for agglomerations of 100,000 p.e. and above, by 31 December 2040 for 10,000 p.e. and above. The 2% figure in the same Directive (Article 5(2)(b), recital 11) is the trigger for listing 10,000–100,000 p.e. agglomerations, not the Annex V objective). Case value: New York City, ~18 billion gallons/year from 398 outfalls (NYSDEC) |
| Stormwater retention and green-infrastructure capacity: volume retained on site per event; share of rainfall managed by green infrastructure | Whether the city is absorbing its rain where it falls — the performance of rain gardens, permeable paving, green roofs and detention, against the grey system | Core where green infrastructure is a management measure; see also §16 | Municipal green-infrastructure programme targets and monitoring (e.g. NYC Green Infrastructure Program: ~1.67 billion gallons/year of CSO flow removed by 2030 under the 2023 CSO Order modification — a programme target, not a measured outcome; the 2012 agreement estimate was ~1.5 billion gallons/year); object baseline |
| Green space per capita (public green space, m² per resident) | How much green each resident has — the quantity side of urban green provision | Core | Italian planning-law benchmark, not a WHO standard: D.M. 1444/1968 (2 April 1968) requires a minimum of 18 m² per inhabitant for public spaces in new settlements, 9 m² of which for public greenery — the 9 m² figure is real, its attribution is Italian law (verified via Land 2024, 13(12):2174). The 50 m² 'ideal' is a widely cited value in reviews, with no standard behind it — report it as a review value, never as a standard. WHO gives no per-capita figure: its verified guidance is accessibility — 0.5–1 ha within 300 m (WHO Regional Office for Europe 2017 brief, rule of thumb; see the accessibility row below). Czesak & Różycka-Czas 2025 (Landsc. Urban Plan. 257, 105301, DOI 10.1016/j.landurbplan.2025.105301) searched the WHO reports cited for the figure and found it in none of them; Mostafa & Alshahrani corrigendum 2025 (Front. Sustain. Cities 7:1542464, DOI 10.3389/frsc.2025.1542464, 3 April 2025) deleted the WHO attribution (Figure 4, Table 1, Conclusion) from the published paper. Benchmark rule: use the jurisdiction's own planning standard where one exists, else the object's baseline. Companion framework: UN-Habitat / SDG 11.7.1 (share of built-up area that is open space for public use) |
| Green-space accessibility: share of residents within 300 m / 5 minutes' walk of a public green space of at least 0.5–1 ha | Whether the green space exists where people live — the equity side, which a citywide per-capita average hides | Core | WHO Regional Office for Europe, "Urban green spaces: a brief for action" (2017): "As a rule of thumb, urban residents should be able to access public green spaces of at least 0.5–1 hectare within 300 metres' linear distance (around 5 minutes' walk) of their homes" — a rule of thumb, not a standard; national planning standards where they exist |
| Urban tree canopy cover, % of object area, by district | How much of the city is shaded from above — cooling, stormwater interception, air-quality and habitat value in one number | Core | Remote-sensing canopy mapping (aerial imagery / lidar); object baseline. Historical reference goal, not a current recommendation: American Forests' 2002 guidance set a 40% overall canopy goal (15% central business district, 25% urban neighbourhoods, 50% suburbs); American Forests withdrew the universal 40% recommendation in 2017 ("it depends" — set the goal from the object's climate, density and land use) |
| Tree-canopy equity: canopy cover and Tree Equity Score by neighbourhood / income group | Who gets the shade — the distribution of canopy against deprivation, which decides whether planting reduces inequity or decorates the already-green districts | Conditional — where equity is a management question | American Forests Tree Equity Score (launched June 2021), 0–100 at census block-group level, canopy goal adjusted for building density; city tree inventory + census data |
| Green-space connectivity and ecological-network coherence | Whether green patches function as a network animals and plants can move through, or as isolated islands | Core for urban biodiversity objects; see also §10 | Singapore Index on Cities' Biodiversity, Indicator 2 (connectivity / ecological networks to counter fragmentation; effective mesh size method). §10 connectivity methods apply within the city |
| Proportion of natural areas in the city | How much of the city is still natural, restored or naturalised habitat rather than lawn, planting or paving | Conditional | Singapore Index on Cities' Biodiversity, Indicator 1: (natural + restored + naturalised area) ÷ city area × 100%; scoring bands in the Index manual (4 points above 20%) |
| Native species in built-up areas: native bird, vascular-plant and butterfly species recorded in built-up areas, and their change | Whether the built city still supports native wildlife — the urban biodiversity outcome, not the park inventory | Core for urban biodiversity objects; see also §11, §14, §15 | Singapore Index on Cities' Biodiversity, Indicators 3–8 (native species in built-up areas; change in number of native vascular plants, birds, butterflies and two city-chosen taxa). Sensitive locations generalised per the skill's §15 rule |
| Urban blue space: extent, connectivity and daylighting of urban water bodies (streams, ponds, canals, waterfront) | Whether the city's water is present, connected and alive, or buried, channelised and cut off | Conditional — where an urban water body is in scope; see also §3, §4 | Object baseline from land-cover / hydrographic mapping; daylighting and de-culverting recorded as management actions (§17). Water chemistry itself is §4 — this indicator is about the water body's presence and connection, not its chemistry |
| Urban stream and pond temperature excess over the rural reference | Thermal pollution from hot runoff off roofs and roads — the heat island written into the water | Conditional — where urban streams or ponds are in scope; see also §4 | Paired urban/rural temperature loggers; object baseline. No universal threshold — set from the object's own baseline |
| Urban soil contamination screening: share of sampled plots exceeding the jurisdiction's soil screening value, by contaminant (lead and others by source) | The legacy in the ground — lead paint, fill, industry and traffic, where children play and food is grown | Conditional — where a source, pathway or prior finding justifies testing; see also §6, §9 | Jurisdictional soil quality standards / screening values; sampling protocol and detection limits stated per §6. A negative result is bounded by its detection limit and date |
| Population exposure to environmental noise: share of residents above Lden / Lnight by source (road, rail, aircraft) | How many people live with noise that the evidence links to annoyance, sleep disturbance and cardiovascular effects — noise as an ecological pressure, not a nuisance | Core where noise decisions are in scope; see also §10 (wildlife) | WHO Environmental Noise Guidelines for the European Region (2018): road traffic below 53 dB Lden and 45 dB Lnight; railway 54 / 44 dB; aircraft 45 / 40 dB (recommendations, not legal limits). EU Environmental Noise Directive 2002/49/EC strategic noise mapping as the reporting method |
| Artificial light at night: zenith sky brightness and upward radiance; share of the object above the natural-sky baseline | How much of the night is gone — skyglow as a pressure on nocturnal wildlife, migration, pollinators and human sleep | Conditional; Research for species-level effect claims | Falchi et al. 2016, The New World Atlas of Artificial Night Sky Brightness (VIIRS-based; ~83% of the world's population lives under light-polluted skies). No universal ecological threshold exists — report against the natural-sky baseline and the object's own trend |
| Urban metabolism — water: total water supplied per capita per day, and share from local vs imported sources | How much water the city drinks, and how far it reaches to get it | Core for city objects | ISO 37120 (Sustainable cities and communities — indicators for city services and quality of life) and SDG 6 / UN-Habitat city data; utility records. No universal threshold — set from the object's own baseline and the supply system's capacity |
| Urban metabolism — energy and greenhouse gases: total final energy per capita; GHG emissions per capita (Scopes 1, 2 and, where available, 3) | The city's energy appetite and its climate footprint — the outflow side of the heat island | Core for city objects | Global Protocol for Community-Scale GHG Emission Inventories (GPC) — WRI / C40 / ICLEI; ISO 37120. No universal threshold — set from the object's own baseline and the city's climate target |
| Urban metabolism — waste and wastewater: municipal solid waste generated per capita; recycling / diversion rate; share of wastewater receiving treatment | What the city throws away and what it returns to the river — the other outflow, and the one the twin can verify | Core for city objects | ISO 37120; SDG 11.6.1 (solid waste regularly collected with adequate final discharge) and SDG 6.3.1 (wastewater safely treated); municipal records. No universal threshold — set from the object's own baseline and the jurisdiction's targets |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for
the window, a single spike never alerts — applies, but the window is
different for different panels, and the city forces one new discipline
on top: **never alert on a citywide average alone**.

- **Heat.** The window is **days, including nights**: a heat-island
  breach is a run of hot days *and* tropical nights, because a single
  hot afternoon is weather and a week of nights that do not cool is
  the health event. The alert is on the urban–rural difference *and*
  on the absolute temperature against the local heat-health threshold
  — a small island on top of a heatwave is still dangerous. A
  heat-health warning issued by the meteorological service is a
  covariate, not an explanation: it does not "explain away" a heat
  breach, it confirms it.
- **Stormwater and overflows.** The window is **the event**: an
  overflow episode is one rainfall event's discharge, and the watch
  level is on frequency and volume over the season, not on a single
  outfall's single spill. The covariate-aware rule (§20) applies
  here in its proper form: a runoff or turbidity breach *is*
  explained by a named rainfall episode that is itself beyond its own
  watch level for the same window — rain explains the runoff, it
  does not excuse the overflow. An overflow during dry weather is
  never explained by rain; it is a system failure and alerts at once.
- **Green space, canopy and connectivity.** These move on **years**,
  not hours. Their watch levels are trend bands: a district whose
  canopy is falling, or whose per-capita green space is falling as
  population grows, is amber even while the citywide average is
  flat. The §20 sustained-breach rule becomes a sustained-trend
  rule — two successive surveys in the same direction — and a
  single survey is never an alert.
- **Noise and light.** These are long-term exposure indicators.
  Their watch levels are population shares above the WHO guideline
  values, recomputed on each strategic noise map or sky-brightness
  survey (typically every 5 years under the EU Environmental Noise
  Directive). A single noisy night or a single bright event never
  alerts; a rising share of exposed residents does.
- **Metabolism.** Water, energy, waste and wastewater are reported
  against the city's own baseline and its own targets, with the
  §20 window set to the reporting period (month, season, year). A
  breach is a sustained exceedance of the city's own target, not a
  universal number — there is no universal per-capita water or
  energy threshold, and inventing one would be the error this
  section exists to prevent.
- **User-class thresholds (§20).** The same city state means
  different things to different people, and the twin records the
  limit per class in Phase 1 onboarding: the same heat-island value
  can mean "open cooling centres" for the health department,
  "restrict outdoor work" for an employer, and "no outdoor play"
  for a school; the same overflow can mean "close the beach" for
  bathers and "stop the intake" for a water utility; the same noise
  level can be acceptable for a road and unacceptable for a hospital
  or a school. The limits are recorded in the Object Passport, one
  row per decision-maker class, in the indicator's own units.
- **The district rule.** Every indicator in this section that can be
  computed by district is computed by district. A citywide green
  space per capita of 20 m² that is 40 m² in one district and 2 m²
  in another is not a green city; it is a green district and a
  deprived one. The twin reports the citywide value, the
  district range, and the lowest district — and the watch level is
  set on the lowest district, not the average.

### What this section does NOT do

- It does **not duplicate §2, §3, §4, §6, §9, §10, §11 or §16**.
  PM2.5, NO2 and ozone are §2; discharge, stage and flood extent
  are §3; dissolved oxygen, pH, turbidity and nutrients in urban
  water are §4; metals, PAHs, PFAS and microplastics are §6; soil
  organic carbon, texture and erosion are §9; patch size and
  corridor function are §10; species richness and vegetation cover
  are §11; carbon stocks and nutrient retention are §16. This
  section adds only what those sections do not say about a city —
  the heat gap, the sealing, the overflow, the reachability of
  green, the canopy equity, the noise and light, and the metabolism.
  Where a measurement belongs to an existing section, the table
  says so in the row.
- It does **not set a universal threshold for the city**. There is
  no universal per-capita water use, no universal energy use, no
  universal heat-island limit, no universal ecological light
  threshold. The anchors that do exist in the literature — WHO
  noise guideline values, the EU 1% indicative storm-water-overflow
  objective (Annex V, non-binding), the ~10% impervious-cover
  screening signal — are named with their source and their status
  (guideline, recommendation, indicative objective, screening
  signal), and every other threshold is set from the object's own
  baseline. Two figures that circulate as standards are not:
  the 9 m² per-capita green-space figure is Italian planning law
  (D.M. 1444/1968: 18 m² public space, 9 m² public greenery per
  inhabitant), widely misattributed to WHO — no WHO publication
  contains it (Czesak & Różycka-Czas 2025; the WHO guidance is
  accessibility, 0.5–1 ha within 300 m) — and the American Forests
  40% canopy goal is a 2002 guidance withdrawn by American Forests
  in 2017 — both are historical references, never thresholds. A twin that copies a
  number from another city into this city's passport is
  over-claiming and must be refused at the Phase 4 verification
  gate.
- It does **not treat a citywide average as the state of the city**.
  Heat, canopy, green space, noise and overflow exposure are
  unequal by district by design — that is the finding, not a
  footnote. The district rule above is part of the section, not
  an optional refinement.
- It does **not confuse a programme target with a measured outcome**.
  A city's green-infrastructure plan promising 1.67 billion gallons
  of CSO reduction by 2030 is a target; the twin reports the
  measured retention and the measured overflow, and the gap between
  them, year by year.
- It does **not predict heat deaths or flood damage from these
  indicators alone**. Heat-island intensity, impervious share and
  overflow volume are pressures and states; mortality and damage
  need exposure, vulnerability and dose–response evidence that
  belongs to the health and flood assessments the twin interfaces
  with, not to this catalogue.
- It does **not replace the city's own plans or warning systems**.
  It is an interface: it ingests the heat-health warning, the
  noise map, the sewer telemetry, the canopy survey and the utility
  accounts, turns them into watch levels and pre-agreed
  trigger–action–response plans for the twin's object, and records
  the handoff to the responsible authority. The twin never issues a
  public heat warning, beach closure or evacuation order itself.
- It does **not use a single survey as a trend**. Canopy, green
  space, connectivity and natural-area share change on multi-year
  timescales; one survey reports a state, two surveys in the same
  direction report a trend, and a twin that calls one survey a
  decline is over-claiming.

Scope boundary: this section is a Conditional module, included only when the object is a city, a district, or an urban water body or green-space network — with interface discipline built in: the twin ingests external city data (heat-health warnings, noise maps, sewer telemetry, canopy surveys, utility accounts, ISO 37120 city reporting), never claims to be the warning authority, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

## 27. Aquaculture — fish farming

Include this section when the object is a managed fish-production system —
ponds, cages, raceways or RAS producing fish for food. For all other objects
the passport records "not applicable: no managed fish production in the
object" and the section is not carried. Where it applies, the twin states
for each indicator the species, the life stage, the production system, and
the cycle dates: a mortality rate, a feed conversion ratio and a stocking
density are meaningless without the species and the cycle they belong to.
Indicators already covered elsewhere are cross-referenced, not repeated:
surface-water quality in the receiving water is §4; nutrient concentrations
and eutrophication state are §5; contaminants are §6; sanitary microbiology
is §13; wild fish populations are §15; fish production as an ecosystem
service is §16; point-source discharge volumes and farm inputs as pressures
are §17. This section adds only what those sections cannot say: the state
of the water *inside the production unit*, the health of the *stocked*
population, the *efficiency* of the production, and the farm's *load* on
the receiving water and on wild fish.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Dissolved oxygen in the production unit: concentration, % saturation, dawn minimum, diurnal range | Whether the stocked fish can breathe — the first production constraint, measured where the fish are, not in the lake outside | Core | ASC Tropical Marine Finfish Standard 2.2.1–2.2.2: weekly average DO saturation on farm ≥70%; at most 5% of weekly samples below 2 mg/L. FAO aquaponics table (Somerville et al. 2014): >4 mg/L for warm-water species, >6 mg/L for rainbow trout. §4's ~2 mg/L severe-hypoxia alert applies to the receiving water, not as a farm operating limit |
| Unionised ammonia (NH₃) in the production unit, with total ammonia nitrogen (TAN), pH and temperature recorded alongside | Acute toxicity risk to the stocked fish; NH₃ is the toxic form and its share of TAN rises with pH and temperature, so TAN alone does not answer the question | Core | Boyd, *Water quality management in aquaculture*, and UF/IFAS (FA-16): 0.02–0.05 mg/L unionised ammonia safe for many species; sub-lethal effects from ~0.01–0.06 mg/L depending on species (growth slightly reduced at 0.06 mg/L in channel catfish); tissue damage above 0.05 mg/L; lethal short-term exposure 0.4–2.0 mg/L. Report NH₃ and TAN separately; see also §5, which records the nitrogen forms in the receiving water. |
| Nitrite (NO₂⁻) in the production unit | Methemoglobinemia risk — nitrite blocks oxygen transport even when oxygen in the water is adequate | Core | FAO aquaponics table: <1 mg/L total nitrite for most species, <0.3 mg/L for rainbow trout; desirable below 0.1 mg/L in general pond criteria (CMFRI training-manual cap 0.5 mg/L nitrite-N). Report as nitrite, not merged into total nitrogen; see also §5 |
| Water temperature in the production unit against the species' optimum range | Thermal stress and growth state; temperature also drives oxygen solubility, ammonia toxicity and disease | Core | FAO aquaponics table, species optima: common carp 25–30 °C, Nile tilapia 27–30 °C, rainbow trout 14–16 °C, channel catfish 24–30 °C, barramundi 26–29 °C. Species- and stage-specific: no universal temperature threshold — set from the species' published optimum and the object's own baseline |
| Daily and cumulative mortality rate of the stocked population (% per day / per month / per cycle), by cause where known | The single most honest production-and-welfare signal; a rising rate is the early warning of disease, water failure or handling damage | Core | Object baseline and cycle history; the Laksvel welfare protocol bands monthly mortality as level 0 (green) below 0.3%, level 1 (yellow) 0.3–0.7%, level 2 (orange) 0.7–2% and level 3 (red level) above 2% (Laksvel protocol, Institute of Marine Research, Rapport fra Havforskningen 2025-40, §4.3). Syndromic surveillance from monthly mortality data (Oliveira et al. 2024, *Transbound. Emerg. Dis.*; 19,119 farm-months, 1,618 cohorts) detected pancreas-disease outbreaks with 80.5–87.4% sensitivity but a 45.3–53.2% false-alarm rate — a mortality alert prompts investigation, not a diagnosis. No universal mortality threshold — set from the object's own baseline |
| Disease incidence and notifiable-disease events; veterinary health plan in force | Whether disease is present, spreading, or reportable — and whether anyone qualified is watching | Core | WOAH *Aquatic Animal Health Code*, Ch. 1.4 (aquatic animal disease surveillance) and Ch. 4.1 (biosecurity): early detection, prompt reporting to the Competent Authority, surveillance by trained personnel. ASC Salmon Standard (v1.4 §5.1/§8): a fish health plan approved by a veterinarian, vaccination where effective vaccines exist for high-risk diseases, disease testing of smolt before transfer (100% of smolt groups tested for select diseases of regional concern before entering grow-out). §13 covers pathogens in the water; this indicator covers disease in the stock |
| Sea-lice / ectoparasite load (adult female lice per fish, by species where relevant) | Parasite pressure on the stock and, in salmonids, the spillover risk to wild fish | Conditional — salmonid cage farming | Norway: fewer than 0.5 adult female lice per fish on average, and 0.2 during the wild-smolt migration period (Norwegian Food Safety Authority / BarentsWatch; Forskrift om lakselusbekjempelse). Weekly counts reported to the authority when water exceeds 4 °C. The Norwegian "traffic light" system regulates production-area volume on lice-driven mortality in wild salmonids |
| Therapeutic treatments per production cycle (antibiotics, antiparasitics, medicinal and non-medicinal delousing), with method and mortality after treatment | Treatment burden and its own welfare cost — delousing itself injures fish | Conditional | ASC Salmon Standard v1.4, Indicator 5.2.13: antibiotic treatments limited to three per production cycle, and antibiotics critical for human health avoided. Note: the ASC Farm Standard v1.0.1A supersedes the Salmon Standard and sets species-specific treatment limits via Indicator 4.4.13 → Appendix 2 (2.5) — check that appendix before use (conservation groups report the Farm Standard salmon limit as six per cycle). Norwegian data (Overton et al., via ResearchGate): thermal delousing raised mortality in 31% of treatments, mechanical in 25%, hydrogen peroxide in 21% (2012–2017). Record treatment and post-treatment mortality together, never treatment alone |
| Economic feed conversion ratio (eFCR), with forage-fish dependency ratio (FFDR) and protein retention efficiency (PRE) where the standard requires them | Feed efficiency — the farm's core economic and environmental ratio: feed in against fish out, counting uneaten feed and losses | Core | ASC Farm Standard v1.0.1A, Appendix 2 (2.2), Indicator 2.12.5: eFCR = total feed use (tonnes) / net production (tonnes), net production = harvested − stocked (all-in-all-out), per Aas et al. 2019. Published Norwegian cage-salmon FCR (Aquacult. Environ. Interact. 2023; data 2011–2020): 1.06 (north), 1.11 (central), 1.17 (south) kg dry feed per kg fish wet weight. (The paper reports FCR; the ASC eFCR definition counts mortality via net production.) No universal "good" eFCR — compare within species, system and cycle |
| Stocking density and standing biomass (kg/m³; fish/m³ and mean weight alongside) | Crowding pressure on water quality, disease and welfare | Core | Norway: maximum allowed density in salmon farming 25 kg fish per m³ (akvakulturdriftsforskriften, FOR-2008-06-17-822, the Norwegian regulation on the operation of aquaculture establishments, § 25 «Tetthet»: the density per production unit of broodstock and food fish of salmon and rainbow trout "skal uansett ikke overstige 25 kg/m³" — shall in no case exceed 25 kg/m³; slaughter pens and closed production units excepted. Paragraph read from the full Norwegian text on FAOLEX, nor82122). ASC position statement on stocking density: density is a welfare indicator but the ASC sets no single universal kg/m³ threshold — it is assessed with other operational welfare indicators per species and system. No universal threshold — set from the jurisdiction's law and the species' welfare evidence |
| Effluent nutrient load: nitrogen and phosphorus mass discharged per tonne of production (concentration × flow, per cycle and per year) | The farm's actual nutrient export — a load, not a concentration; the number the receiving water feels | Core | §5 for concentrations and trophic state in the receiving water; this indicator is the mass. EU Regulation 2024/1244 (OJ L, 2.5.2024; applies from 1 January 2028): Annex I row 7 brings feed-based aquaculture exceeding 500 t annual production capacity into scope; N/P releases are then reported annually only above the Annex II thresholds (total N 50,000 kg/yr, total P 5,000 kg/yr to water); water/energy use and production volume are reported under Art. 6(1)(d)–(e). Verified against the regulation text (EUR-Lex CELEX:32024R1244). US EPA CAAP guidelines (40 CFR 451, 2004) set no numerical limits for facilities producing ≥100,000 lb/year — they require best-management practices to minimise solids, BOD and nutrients. No universal load limit — set from the permit and the receiving water's capacity |
| Effluent organic load and solids (BOD₅, COD, total suspended solids in the discharge) | Oxygen-demanding and particulate waste leaving the farm | Core for flow-through, raceway and RAS discharge; Conditional for open cages (no discrete effluent) | §5 for BOD₅/COD in the receiving water; US EPA 40 CFR 451 BMP duties (efficient feed management; routine cleaning of rearing units and settling basins; minimise discharge of accumulated solids during inventorying, grading and harvest). Limits, where they exist, are in the discharge permit — the twin records the permit value, never a generic one |
| Benthic impact beneath and beyond the farm: sediment sulphide (S²⁻), redox potential (Eh), benthic fauna state | Whether farm waste is smothering the seabed or lakebed under the cages | Conditional — marine and lake cage farming | ASC Salmon Standard v1.4, Criterion 2.1.1: redox potential > 0 mV **or** sulphide ≤ 1,500 µM in sediment outside the allowable zone of effect (AZE; default 30 m from a cage array) — farms choose one of the two, not both. Corroborated by the Saldanha Bay monitoring protocol (citing ASC 2017). Nova Scotia Environmental Monitoring Program: stations above 3,000 µM resampled until below 1,500 µM. §7 covers sediments generally; this indicator is the farm-footprint reading |
| Copper and antifouling substances in sediment beneath and beyond the farm | The persistent chemical footprint of the cages — copper from nets and antifouling treatments accumulates in sediment | Conditional — where copper-based antifouling is used | ASC Salmon Standard, Indicator 4.7.4: where copper-treated nets or copper antifoulants are used, copper in sediment below 34 mg/kg dry weight (as applied in published ASC audit reports, e.g. Icelandic Environment Agency monitoring 2024); object baseline against a reference site. Outside ASC there is no universal limit — set from the permit and the receiving environment |
| Receiving-water state around the farm against a reference site (DO, TAN, total phosphorus, chlorophyll-a at farm and reference stations) | Whether the farm is changing the water around it, measured against a place the farm does not touch | Conditional — where a receiving water exists | ASC Tropical Marine Finfish Standard 2.2.3: quarterly recording of TAN, nitrate and total phosphorus on the farm and at a reference site; reference site at least 500 m from the edge of the net-pen array, in a location following similar upwelling patterns and not influenced by aquaculture or other anthropogenic nutrient inputs. §4/§5/§12 supply the methods; this indicator supplies the paired design |
| Escape events: number of fish escaped per event and per cycle; estimated unexplained loss (EUL) | Containment failure and the genetic and ecological risk to wild fish | Core for open systems (cages, ponds, raceways); not applicable to closed RAS with no escape pathway — record why | ASC Farm Standard v1.0.1A, Indicator 2.4.11: maximum 300 known escapes per production cycle or year, whichever is stricter, for marine salmonids (6% of stocked population for other fish); exceedance must be notified to the certification body by the next working day, for cancellation of certification. (The "one exception in 10 years" in the old Salmon Standard v1.1/v1.4 does not survive in the Farm Standard.) ASC Farm Standard Interpretation Manual, Indicator 2.4.12: zero mass escapes for species in EICAT categories MR/MV — for marine salmonids, more than 5,000 individuals at once counts as a mass escape; for other fish, more than 6% of the stocked population at once. EUL = stocking count − harvest count − mortalities − recorded escapes (ASC Salmon Standard audit guidance). §15 watches the wild population; this indicator watches the farm's contribution to it |
| Wild-fish interaction: lice-induced mortality risk to wild salmonids in the production area; genetic introgression risk in wild populations | The farm's effect beyond its boundary, at population scale | Conditional — salmonid farming in waters with wild salmonids; Research elsewhere | Taranger et al. 2015 (*ICES J. Mar. Sci.* 72(3):997; 2010–2012 data): 21 of 34 investigated wild salmon populations at moderate-to-high risk of genetic introgression from escaped farmed salmon; lice-driven mortality assessed per production area under the traffic-light system (green 0–10%, yellow 10–30%, red >30% likely lice-induced mortality of wild salmon). This is an area-scale indicator — it cannot be read off a single farm's lice count alone |
| Water abstraction and water use (m³ per tonne of production; consumptive vs. through-flow), and discharge volume | How much water the farm takes and returns — the quantity question, distinct from its quality | Core for land-based systems (ponds, raceways, RAS); Conditional for cages | §3 for hydrology and §17 for abstraction as a pressure; this indicator is the farm's own water account (intake, recirculation rate, discharge). No universal water-use benchmark per tonne exists — compare within system type and state whether the figure is total throughput or make-up/consumptive water. Throughput: raceways 16,000–42,000 m³/t; flow-through salmonids 22,000–95,000 m³/t (Bergheim et al. 2013); fishponds 1,200–10,000, shrimp ponds 20,000–100,000 m³/t (Campanati et al. 2022, Rev. Fish. Sci. Aquac. 30(2):143–169, DOI 10.1080/23308249.2021.1897520); cages ~0.75 m³/t freshwater input. RAS: total use 300–800 m³/t (Bergheim et al. 2013, salmonids); make-up water 0.15–0.5 m³/t (Victorian RAS, DPI 2008) to ~5 m³/t (Timmons & Ebeling 2013). No certification standard sets a m³/t limit (ASC RAS Module: ≤50% of natural flow diverted, >90% returned). Set from the permit, the source's availability, and comparable systems of the same type, and state the comparison |
| Fallowing and site rotation: fallow duration between cycles, synchronised fallowing across a management area | Whether the site and the seabed/lakebed get a recovery break, and whether disease cycles are broken | Conditional — cage and pond systems | ASC Farm Standard Interpretation Manual v1.0.1, Indicator 2.4.21: fallowing periods must be timed to occur outside the out-migration period of native salmonids; RSPCA comparison table records synchronised fallowing across a farm management area as standard practice. Duration is site- and system-specific — record the plan and whether it was kept, not a generic number |
| Operational welfare indicators (fin damage, skin lesions, eye damage, behaviour / appetite, cleaner-fish mortality where cleaner fish are used) | Fish welfare as observed on the fish, not inferred from water chemistry alone | Research | ASC position statement: welfare is assessed through multiple operational welfare indicators (OWIs) tailored per species and system, not a single threshold. Cleaner-fish welfare is a live concern in salmon farming (high cleaner-fish mortality reported in the literature and in Norwegian reporting) — record it where cleaner fish are stocked. Research-grade until a validated scoring protocol exists for the object |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is different
for a living production system than for a river: for dissolved oxygen and
ammonia in the production unit the window is **hours, and the dawn minimum
is the reading that matters**, because fish die at dawn when oxygen is
lowest after a night of respiration, not at the daily mean. A DO breach
that lasts one dawn is an event; a DO breach on three consecutive dawns is
a pattern and alerts. For mortality the window is **days to a month**: the
Laksvel framing (monthly mortality above 2% is level 3, the red level) is
the shape to copy — a single day's dead-fish count never alerts, a
sustained rise against the farm's own baseline does.
For sea lice the window is the **weekly count**: the Norwegian limit is a
weekly-reported average, and a farm that sits above 0.5 adult female lice
per fish across the reporting week is in breach, not a farm with one high
sample. For effluent loads the window is the **cycle or the year**: a load
is a mass over time, and a single high-concentration sample is not a load
breach. An observation gap longer than the maximum gap ends the episode —
and for a production unit a gap in DO or mortality recording during a
heatwave or a disease event is itself recorded as a data gap, never as a
quiet period.

The covariate-aware rule (§20) applies in its normal direction here, with
one reversal to note. A DO breach explained by a sustained high-temperature
episode is logged as explained, not alerted — temperature is a named driver
with its own watch level, and the explanation is recorded with the driver
episode. But a mortality breach is **never** explained away by a lice
breach or a temperature breach: disease, parasites and heat are pressures
that raise mortality, not excuses that cancel it. The twin logs the
covariates alongside the mortality episode so the cause can be investigated;
it does not silence the mortality alert because a cause is visible.

The user-class thresholds (§20) are the farm's operating limits: the same
dissolved-oxygen reading can mean "reduce feeding and start aeration" for
the farm manager, "stop harvesting and grading" for the harvest crew, and
"notify the regulator" for the compliance officer — and for salmonids, the
lice limit differs by class of wild fish at risk (0.2 adult female lice per
fish during smolt migration, 0.5 otherwise). All limits are recorded in
Phase 1 onboarding in the Object Passport, per decision-maker class, in the
indicator's own units.

### What this section does NOT do

- It does **not certify a farm**. ASC, GLOBALG.A.P., Best Aquaculture
  Practices and national permits are certification and licensing systems
  with auditors; this section borrows their indicators and their
  definitions, and a twin that reports them is not a certificate. The
  twin records the farm's numbers against the standard's requirements and
  states the gap; it never claims the farm "passes ASC".
- It does **not set a universal dissolved-oxygen, ammonia, density or
  feed-conversion threshold**. There is none that holds across species,
  life stages and systems: trout need >6 mg/L where carp grow at >4 mg/L;
  Norway caps salmon density at 25 kg/m³ where RSPCA Assured caps seawater
  enclosures at 17 kg/m³ (site maximum 15 kg/m³); eFCR differs by region
  even within Norwegian salmon. Every
  threshold is species-, system- and jurisdiction-specific, set from the
  named source and the object's own baseline.
- It does **not confuse concentration with load**. A farm can meet every
  concentration limit in its permit and still deliver a large nutrient
  load to a small receiving water, because load is concentration times
  flow times time. The effluent indicators in this section are loads per
  tonne of production; the §5 indicators are concentrations in the
  receiving water. Both panels are needed, and a clean concentration
  reading says nothing about the load.
- It does **not treat the receiving water as the farm**. The lake or the
  coastal water around a cage array has its own state, watched by §4/§5/
  §12/§15; the production unit has its own state, watched here. A clean
  lake reading says nothing about the fish inside the cages, and a sick
  stock says nothing, by itself, about the lake.
- It does **not diagnose disease from mortality alone, and it does not
  prescribe treatment**. Mortality is the alarm; diagnosis needs
  veterinary examination, laboratory confirmation under the WOAH *Aquatic
  Manual*, and a veterinarian's health plan. The twin records the
  mortality episode, the lice count, the water state and the treatments
  given; it never recommends a drug, a dose or a delousing method.
- It does **not count escapes from a stocking-minus-harvest arithmetic
  alone**. Estimated unexplained loss is a reconciliation, not a count:
  it lumps counting error, unrecorded mortality and real escapes. The
  twin reports EUL alongside recorded escapes and the counting method's
  accuracy, and never presents EUL as the number of fish that escaped.
- It does **not promote research-grade welfare indicators to warnings**.
  Fin damage, behaviour scores and cleaner-fish mortality stay Research
  until a validated scoring protocol exists for the object and the
  species.

Scope boundary: this section is a Conditional module, included only when the object is a managed fish-production system — with interface discipline built in: the twin ingests farm and regulatory data (farm production records, veterinary reports, lice counts, discharge permits, ASC audit reports), never claims to certify the farm or to prescribe treatment, and records every handoff to the veterinarian and the regulator. The decision is recorded in the Object Passport at Phase 1.

## 28. Desert and arid lands

Include this section when the object is in, or directly affected by, arid or
semi-arid land — a desert, a dry rangeland, an irrigated dryland farm, an
oasis, a dune field, or a settlement, road, or farm downwind of one. The
entry test is the UNEP aridity index (below): an object with AI below 0.65
qualifies; an object with AI above 0.65 qualifies only where a named arid
process (dust source, dune encroachment, oasis groundwater, salinisation)
reaches it. For all other objects the passport records "not applicable: no
arid land in the object or its contributing catchment" and the section is not
carried. Where it applies, the twin states for each indicator the last
observation date and the observation gap: a desert panel with a stale last
date is a data gap, not a clean bill of health — and in drylands, where
change is slow until it is sudden, a gap of years can hide the whole story.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| UNEP aridity index AI = P / PET (mean annual precipitation over mean annual potential evapotranspiration) | Whether the object is arid at all, and which aridity class it sits in — the entry test for this whole section | Core for every object in this section | UNEP (1992), *World Atlas of Desertification*: hyper-arid AI < 0.05; arid 0.05–0.20; semi-arid 0.20–0.50; dry sub-humid 0.50–0.65; drylands AI < 0.65. PET by FAO-56 Penman–Monteith where data allow, Thornthwaite only where they do not; method named in §19. A class boundary crossed on a 30-year normal is a regime statement, not an alert |
| Climatic water balance and its seasonality (P − PET by month/season; length of the dry season; timing of the water pulse) | When water is available and when it is not — the pulse that desert life waits for; the annual AI alone cannot say this | Core | Object baseline from station/reanalysis (§1); FAO-56 PET. No universal threshold — set from the object's own baseline |
| Fractional vegetation cover in arid lands (FVC), soil-adjusted (SAVI / MSAVI) | How much of the ground is actually covered by living plants, once the bright soil background is corrected for — NDVI alone over-reads soil and under-reads sparse cover | Core | linear scaling after Gutman & Ignatov (1998), FVC = (VI − VI_soil) / (VI_veg − VI_soil) on the chosen index (NDVI by default; SAVI/MSAVI where soil brightness dominates), with the soil and vegetation end-members set per object from its own bare and fully vegetated pixels (lower-Heihe practice: the 5th and 95th percentiles of the scene NDVI distribution — see Sources). Quadratic form, FVC ≈ (scaled NDVI)², after Carlson & Ripley (1997). See also §11 |
| Desert vegetation condition: perennial vs ephemeral (annual) cover share; post-rain green-up magnitude and duration | Whether the vegetation that is there is the long-lived backbone or a brief annual flush — a green flush after rain is not recovery | Core | Object baseline; repeat satellite + field plots. Read always against rainfall (§1) and the water balance above: greenness without its rain covariate is not evidence either way |
| Rain-use efficiency (NPP or FVC per unit rainfall) and land-productivity trend against rainfall | Whether productivity is falling faster than the rain explains — the separation of climate-driven decline from degradation-driven decline | Conditional — where desertification is the management question | UNCCD Good Practice Guidance for SDG 15.3.1, productivity sub-indicator (NPP trend). Rain-use efficiency (NPP or NDVI per unit rainfall) as the climate-adjustment aid: RUE = NDVI per unit rainfall (Zdruli et al., "Mapping desertification: constraints and challenges"); Trends.Earth lists Rain Use Efficiency as one of its four land-productivity trajectory indicators for SDG 15.3.1 |
| Biological soil crust cover, composition and disturbance state (light cyanobacterial vs dark lichen/moss crust; cover %, patchiness; trampling/grazing breaks) | Whether the living skin of the soil is intact — crusts fix carbon and nitrogen, bind the surface against wind and water, and hold moisture; a broken crust is degradation that a greenness index cannot see | Core for arid soils | Belnap (USGS Fact Sheet 065-01, 2001): crusts comprise over 70% of the living ground cover in many arid lands; Belnap et al. (2001) and Belnap & Eldridge (2001): crusts as indicators of ecological health and of physical disturbance (livestock, vehicles, foot traffic). Field protocol + repeat photography; colour/darkness as the field proxy for maturity (Belnap 2008; USGS Fact Sheet 065-01, 2001). No universal cover threshold — set from the object's own baseline |
| Biocrust function proxies: crust chlorophyll-a, exopolysaccharides, soil aggregate stability under the crust | Whether the crust is still doing its work, not merely present — cover without function is a thin record | Research | Bowker et al. (2008): chlorophyll-a a moderate-to-excellent predictor of soil stability within soil groups (R² 0.21–0.75) across Grand Staircase-Escalante. Research-grade until validated for management use on the object |
| Soil salinisation trajectory: ECe (saturated-paste electrical conductivity) trend, salt-affected area share, depth to saline water table | Whether salt is accumulating in the root zone, and how fast — the slow process that ends irrigation and kills palm groves | Core where irrigation, shallow groundwater, or saline parent material is present; see also §9 | FAO Global Status of Salt-Affected Soils (2024): more than 1,381 million ha salt-affected worldwide (10.7% of global land). Depth split from the earlier FAO Global Map of Salt-Affected Soils (2021), not from the 2024 report: 424 million ha of topsoil (0–30 cm) and 833 million ha of subsoil (30–100 cm) salt-affected; 20–50% of irrigated soils in all continents too salty (FAO 2021). Classification anchor (Richards 1954, via FAO): saline soil ECe > 4 dS/m; saline-sodic ECe > 4 dS/m and SAR > 13. The 4 dS/m line is a classification, not an alert — the alert is the trend against the object's baseline and the tolerance of its vegetation |
| Sodicity: sodium adsorption ratio (SAR) / exchangeable sodium percentage (ESP), dispersion and structural decline | Whether sodium is destroying soil structure even where total salt looks moderate — sodic soil seals, crusts, and will not take water | Conditional — where SAR/ESP is elevated or irrigation water is sodic; see also §9 | Richards (1954) classification via FAO: SAR > 13 with ECe > 4 dS/m is saline-sodic; high SAR alone is sodic. No universal threshold — set from the object's own baseline and its soil texture |
| Wind erosion and sand drift potential (Fryberger & Tsoar drift potential, DP, in vector units; resultant drift direction) | How much sand the wind is capable of moving, and where it is carrying it — the pressure behind dune advance and dust emission | Core where dunes, sand sheets, or erodible bare soil are present; see also §1 (wind) | Fryberger & Tsoar method, from wind speed/direction records above the entrainment threshold. Case value, not a threshold: Khartouran Erg, NE Iran, 30-year DP = 173 vector units, classed low, sand carried to the south-west (Rahdari & Rodríguez-Seijo 2021). No universal DP threshold — set from the object's own baseline |
| Dune migration rate and sand-encroachment front advance (dune-crest displacement; area of newly sand-covered productive land) | Whether the sand is actually moving onto fields, roads, settlements and oases — the realised harm, not the potential | Conditional — where mobile dunes threaten an asset | Repeat satellite / field survey of dune crests and sand-front position; object baseline. No universal threshold — set from the object's own baseline and the distance to the exposed asset |
| Sand/dust-storm event frequency, duration and severity (days per year by WMO visibility class) | How often the air itself becomes the hazard — distinct from the §2 concentration panel, which measures how dirty the air is, not how often it closes roads and schools | Core for dust-exposed objects; see also §2 | WMO visibility classes (McTainsh & Pitblado 1987, Earth Surf. Process. Landforms 12(4):415–424, as tabulated by FAO): dust haze (dust in suspension, not raised at the station) usually below 10 km; blowing dust (dust or sand raised at the time of observation) 1–10 km; dust storm (strong winds lifting large quantities of dust) below 1,000 m; severe dust storm below 200 m. Count events by class, per year and per season. WMO SDS-WAS (launched 2007) regional centres as the forecast source |
| Dust-storm source-area activity: bare erodible surface share, source-area dust-emission frequency (satellite AOD / dust optical depth over the source) | Where the dust is coming from, and whether the source is growing — the upwind panel for a downwind object | Conditional — where the object is downwind of a named source, or is itself a source; see also §2 | SDS-WAS / Copernicus dust products (dust optical depth, surface concentration); object baseline. No universal threshold — set from the object's own baseline |
| Desertification extent: proportion of land degraded, SDG indicator 15.3.1 | Same composite as §22 — see §22 for the method; the desertification reading applies the UNCCD scope (arid, semi-arid and dry sub-humid land) | Core where desertification is the management question; see §22 | UNCCD Good Practice Guidance for SDG 15.3.1, Version 2 (2025 release); report the three sub-indicators separately alongside the combined figure |
| Oasis extent and palm-grove / oasis vegetation condition (oasis area; grove LAI / NDVI; dead and dying palm share) | Whether the oasis is holding its ground or contracting — the green island is the whole livelihood | Core where an oasis is present; see also §11 | Repeat satellite mapping (Landsat/Sentinel-2) + grove census; object baseline. Case value, not a threshold: in the Boudenib oasis, Morocco, palm LAI 1.25–1.5 corresponded to high groundwater (piezometric level reaching 8 m), LAI 0.5–0.8 to periods of reduced groundwater availability (Geosciences 2025, 15(3):104) |
| Oasis water: depth to groundwater, water-table trend, and water salinity (EC) — read as a pair with grove condition | Whether the water under the oasis can still reach the roots and whether it is still fit for the palms — falling water and rising salt together are the oasis failure mode | Core where an oasis is present; see also §8 | National groundwater monitoring practice; paired gauge + EC record. Case value, not a threshold: in the Boudenib oasis, the best palm growth corresponded to groundwater depths of 8–9 m — a site value, not a standard. Alert on a sustained falling trend and a sustained EC rise together, never on one reading |
| Ephemeral water: wadi / ephemeral-stream flow days per year; playa and ephemeral-lake inundation frequency, duration and extent; time since last inundation | Whether the water that arrives in pulses still arrives — in deserts, a dry wadi that never flows and a playa that never floods are a lost regime, not a normal dry season | Core where ephemeral water is present; see also §3 | Gauge / satellite inundation mapping; object baseline. No universal threshold — set from the object's own baseline; a multi-year absence against a baseline of regular inundation is at least amber |
| Desert biodiversity: arid-adapted and endemic species occupancy and trend; water-point dependence; nomadic / migratory movement of desert fauna | Whether the species that only this desert holds are still here, and whether they can still reach water — desert fauna live by movement and by scattered water, and both are easily broken | Conditional — where arid-adapted, endemic or red-list desert species are present; see also §15 | National / IUCN red lists; occupancy protocol with detection probability; sensitive locations generalised per §19 / GBIF rules. Cold-desert anchor case: the Mongolian Gobi holds the world's largest populations of khulan (Asiatic wild ass) and goitered gazelle, the endemic Gobi bear, and one of three remaining wild Bactrian camel populations — movement and water-point access are the monitoring questions, not head counts alone |
| Arid rangeland utilisation: stocking against the forage pulse (livestock numbers vs post-rain forage; recovery time after grazing) | Whether grazing is taking the regrowth the land needs to recover — in drylands the forage arrives in a pulse and the damage is done between pulses | Conditional — where pastoral grazing is a pressure; see also §17 | National rangeland practice; object baseline. No universal stocking threshold — set from the object's own baseline and its rainfall year |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is different:
for a slow process such as salinisation, crust loss or desertification
extent, the window is **seasons to years**, not hours, and the alert logic
is on **trend and rate**, not on an absolute value. A salinisation episode
ends when ECe returns to baseline for the window, or when the observation
gap exceeds the maximum gap (a soil survey gap of several years ends the
episode and the indicator is recorded as stale, never as quiet). For
dust storms the window is the opposite: an event is hours to days, and the
watch level is the **count per season**, so a single storm never alerts —
a season with a sustained excess over the object's baseline does.

The covariate-aware rule (§20) is the heart of this section and it applies
in one direction above all: a vegetation breach is logged as *explained*,
not alerted, when rainfall is itself below its own watch level in a
sustained episode overlapping the breach's window — a dry year explains a
brown year. Only an *unexplained* vegetation breach alerts: greenness
falling while the rain was normal is degradation, and greenness falling
faster than the rain explains is degradation too. The same rule applies in
reverse for dust: a dust-storm excess is not explained away by high wind
alone — wind is the mechanism, not an excuse; the question is whether the
source surface was bare enough to feed it, so the covariate that can
explain a dust breach is a wet-season soil-moisture or cover recovery, not
the wind that carried it. The driver and its bands are named on the
scenario card's Alerts field, never assumed.

The user-class thresholds (§20) are the livelihood limits: the same
groundwater depth can mean "palms survive" for a date farmer, "stock can
water" for a herder, and "the oasis holds" for a settlement — and the same
visibility can mean "roads open" for one class and "schools close" for
another. All limits are recorded in Phase 1 onboarding in the Object
Passport, in the indicator's own units. Where a limit is a vegetation
tolerance (a palm's salinity limit, a crop's ECe limit), it is a
classification anchor from the literature, not an operational limit set by
the twin — the twin records whose limit it is and its source.

### What this section does NOT do

- It does **not call every dry place desertified**. Desertification in the
  UNCCD sense is land degradation in arid, semi-arid and dry sub-humid
  areas. Hyper-arid land is not desertified by definition, however degraded
  it looks, and a dry year is not desertification. A twin that labels a
  hyper-arid dune field or a drought year "desertified" is misusing the
  treaty term and must be refused at the Phase 4 verification gate.
- It does **not read greenness as health**. In drylands, greenness follows
  rain. A green flush after rain is not recovery, a brown year in a dry year
  is not degradation, and an NDVI trend without its rainfall covariate is
  not evidence. The rain-use efficiency and productivity-against-rainfall
  readings exist precisely to stop this mistake.
- It does **not use NDVI alone on bright soil**. Bare desert soil is bright,
  and NDVI over bright soil confounds soil and leaf. The section requires
  the soil-adjusted cover (SAVI/MSAVI, per-object end-members) for the
  cover claim; an NDVI-only cover figure in a desert is a draft indicator
  until the soil correction is shown.
- It does **not set a universal salinity, aridity or dust threshold**. The
  4 dS/m line classifies a soil as saline; it does not say when a given
  palm, crop or rangeland fails — that is the species' own tolerance, and
  the Boudenib 8–9 m groundwater depth is one oasis's value, not a
  standard. Every threshold is object-specific, set from the object's own
  baseline, and carries its named source and date.
- It does **not treat a dust concentration as a dust storm**. §2 measures
  how dirty the air is (PM2.5/PM10, µg/m³); this section counts how often
  the visibility collapses below 1,000 m and for how long. A high-PM day
  with no storm and a storm day with a moderate daily PM mean are
  different facts, and the twin keeps them on different panels.
- It does **not replace a UNCCD national report, a rangeland assessment,
  or an official dust warning**. It is an interface: it ingests national
  desertification reporting (SDG 15.3.1), rangeland surveys and SDS-WAS
  forecasts, turns them into watch levels and pre-agreed
  trigger–action–response plans for the twin's object and the people who
  depend on it, and records the handoff to the responsible authority. The
  twin never issues a public dust warning itself.
- It does **not promote research-grade indicators to warnings**. Biocrust
  function proxies (chlorophyll-a, exopolysaccharides) stay Research until
  validated for management use on the object, and the rain-use efficiency
  reading uses its confirmed method source (Zdruli et al.; Trends.Earth SDG 15.3.1 indicator).
- It does **not mistake a planted shelterbelt for a recovered ecosystem**.
  A green wall of planted trees can hold sand while the soil beneath it
  keeps salinising and the crust beneath it stays broken. Vegetation,
  soil, salt and water are separate panels, and a clean reading on one
  says nothing about the others.

Scope boundary: this section is a Conditional module, included only when the object is in or affected by arid land — with interface discipline built in: the twin ingests external desertification and dust data (UNCCD SDG 15.3.1 reporting, FAO salt-affected-soils maps, SDS-WAS forecasts, national rangeland surveys), never claims to be the reporting or warning authority, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

## 29. Tundra and polar

Include this section when the object is arctic or alpine tundra, or a
mosaic in which tundra is a named component — a tundra reserve, a
reindeer-herding range, a permafrost research site, an arctic coastal
settlement's hinterland, or a mine/oil-field lease on tundra. For all
other objects the passport records "not applicable: no tundra in the
object" and the section is not carried. Where it applies, the twin
states for each indicator the last observation date and the observation
gap: a vegetation or thaw panel with a stale last date is a data gap,
not a clean bill of health. Tundra is a slow system on a fast calendar:
vegetation, soil carbon and shrub cover are read once a year at most,
and a trend needs repeat surveys over years — one survey reports a
state, never a trend. The one exception is the event scale: a
rain-on-snow winter or a tundra fire can change the object in days, and
those indicators are read on the event, not the season.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Tundra vegetation composition: shares of dwarf shrubs, sedges, grasses, forbs, mosses and lichens; PFT shares | Whether the community is still tundra or sliding toward shrub dominance or graminoid dominance — the composition signal, not the cover signal | Core | Fixed-plot or transect protocol (ITEX network protocol; CAFF Circumpolar Biodiversity Monitoring Program, CBMP, terrestrial plan); PFT shares per §11 (`scripts/diversity.py pft`); object baseline. Shares from one quantity only — cover or counts, never mixed. Lichen share is tracked separately: it is the reindeer winter forage base, and shrub expansion displaces it |
| Shrub cover and shrubification: tall-shrub and dwarf-shrub cover share, shrub height and growth, shrublines | Whether shrubs are infilling, growing taller and advancing — the most widespread vegetation change in the warming Arctic | Core | Repeat remote sensing + field plots; object baseline and trend. Case values, not thresholds: shrubification is a pan-Arctic trend since the 1980s (Mekonnen et al., Environ. Res. Lett. 2021, 16:053001, doi 10.1088/1748-9326/abf28b; Tape et al. 2006, 202 pairs of oblique aerial photographs ~1950–2000, widespread alder/willow/dwarf-birch expansion on the Alaskan North Slope; Moffat et al. 2016, tall-shrub cover increased at 55% and dwarf-shrub cover at 74% of 38 sites across the Tuktoyaktuk Coastlands, 1980–2013). Honest limit: shrub cover is stable or decreasing at many ITEX sites, and NDVI does not track shrub growth in all tundra landscapes — report the field and satellite evidence separately |
| NDVI / greenness trend: MaxNDVI and time-integrated NDVI, greening vs browning share of the object | Productivity and the direction of vegetation change — greening, browning or stable — at the scale the satellite sees | Core | Object multi-year baseline; NDVI/EVI per §11 with field calibration — no satellite-only biomass or composition claim. Case values, not thresholds: 37.3% of the Arctic greened, 4.7% browned, 58% unchanged, 1985–2016 (Berner et al. 2020, Landsat); 42% greening and 3% browning, 1982–2014 (GIMMS-3g+, Park et al. 2016); 13% greening and 1% browning, 2000–2018 (MODIS, Myers-Smith et al. 2020); 2020 set record-high circumpolar mean MaxNDVI in all four satellite records (NOAA Arctic Report Card, Tundra Greenness). The fractions depend on sensor, resolution and period — never quote one without naming all three |
| Active-layer thickness and its trend; permafrost table depth | How deep the ground thaws each summer — the direct measure of thaw, and the driver of subsidence, thermokarst and infrastructure risk | Core; ground temperature itself is §21 — cross-reference, do not duplicate | CALM (Circumpolar Active Layer Monitoring) mechanical-probing protocol + borehole temperature per GTN-P; object baseline and trend. Case value, not a threshold: permafrost ground temperature near the depth of zero annual amplitude rose 0.39 ± 0.15 °C in the continuous zone and 0.29 ± 0.12 °C globally, 2007–2016 (Biskaborn et al. 2019). Honest limit (IPCC SROCC, cited in the permafrost literature): only medium confidence that active-layer thickness has increased region-wide, because trends vary by site and probing underestimates degradation where the surface subsides as ground ice melts |
| Thermokarst features: thaw-lake area and number, retrogressive thaw slumps (count, area, retreat rate), ground subsidence, ice-wedge polygon degradation | Where ice-rich permafrost is collapsing — the visible face of thaw, and a carbon and sediment source | Core where ice-rich permafrost is present | Repeat high-resolution remote sensing + field survey; object baseline. Case values, not thresholds: Banks Island, Canadian High Arctic — ~60 active retrogressive thaw slumps in 1984, more than 4,000 in 2013, a sixty-fold increase, with 85% of new slumps forming after four hot summers (1998, 2010, 2011, 2012) (Lewkowicz & Way 2019, Nat. Commun. 10:1727); slump retreat rates up to ~38 m/yr (Noatak Valley, Alaska). A new slump field is at least amber |
| Soil organic carbon stock in tundra soils (0–30 cm, 0–100 cm, 0–300 cm); SOC trend | Soil health and the carbon at risk — tundra soils hold more carbon than the atmosphere | Core | Northern Circumpolar Soil Carbon Database (NCSCD) baseline; object baseline; trend over 5+ years. Case values, not thresholds: northern permafrost region SOC 1,460–1,600 Pg (Hugelius et al. 2014; Schuur et al. 2015); ~200 Pg in the 0–30 cm layer, ~500 Pg in 0–100 cm, ~1,024 Pg in 0–300 cm (Tarnocai et al. 2009, via the permafrost-carbon literature). No universal SOC threshold exists; the warning is the trend and the thaw exposure, not one value |
| Greenhouse-gas fluxes: CO₂ and CH₄, growing-season and cold-season | Whether the tundra is a net sink or a net source — the climate verdict on the whole panel | Conditional — carbon decisions; Research where only modelled | Chamber, eddy-covariance or flux-tower protocol with QA; do not infer flux from carbon stock alone (§16). Case value, not a threshold: a circumpolar synthesis of non-summer CO₂ fluxes found cold-season release 2–3 times higher than previously estimated, such that the region as a whole could already be a net source of ~0.6 Pg C/yr (Natali et al. 2019, Nat. Clim. Change 9:852–857) |
| Snow cover duration, snow depth and snow-water equivalent; rain-on-snow and melt–freeze icing events | Winter habitat, insulation and the icing risk — rain-on-snow is the single most destructive tundra weather event for herbivores | Core; see also §1 | Hydromet station practice + satellite snow products; rain-on-snow recorded as a named event class with extent and ice-layer thickness where measured. Case values, not thresholds: November 2013 rain-on-snow on the Yamal Peninsula killed 61,000 reindeer of ~275,000–300,000 (about 22%), the region's largest recorded mortality episode (Forbes et al. 2016, Biol. Lett. 12:20160966); ~20,000 died in the November 2006 event. An icing event covering the winter forage area is red for the herding class |
| Surface water: thaw-pond and lake area, number and drainage events; wetland extent | Hydrology of a thawing landscape — new lakes form as old ones drain | Conditional — where thaw lakes are present; see also §3 | Repeat remote sensing + gauge where installed; object baseline. A lake drainage event is recorded as an event, not a gradual change; the North Slope landscape is ~84% lakes or drained thermokarst lake basins (Hinkel et al. 2005, via the Drew Point literature) |
| Caribou / reindeer abundance, calving success, calf survival and migration timing | The keystone herbivore and the food-security indicator for northern communities — their decline is the tundra's loudest faunal signal | Core for conservation and herding objects; Conditional otherwise | Aerial survey / herd census + calving-ground monitoring per §15; CAFF/CARMA herd data; object baseline and trend. Case values, not thresholds: migratory wild caribou/reindeer have lost nearly two-thirds of global abundance in the past three decades (WWF Arctic, from data since 1970); the Bathurst herd fell from ~470,000 in 1986 to fewer than 7,000 in 2022; the Western Arctic herd peaked at ~490,000 in 2003 (ADF&G) and fell to ~188,000 by 2021; the Bathurst decline is partly a natural cycle but warmer summers, roads, traffic and mines have contributed, and conservation actions have not led to recovery; the Qamanirjuaq calving ground shifted to the edge of an operational gold mine (NOAA Arctic Report Card 2024, Migratory Tundra Caribou). A declining trend is red regardless of absolute numbers. Sensitive calving-ground locations generalised per §11/§15 |
| Lemming / vole abundance and cycle state (peak, decline, low, increase) | The base of the tundra food web — predators, owls and foxes track the lemming cycle; its loss cascades | Conditional — where present | Trapping / snap-trap index or sign surveys per §15; object baseline over at least one full cycle. Case values, not thresholds: lemming cycles have a median periodicity of 3.7 years and are detected 55% of the time across 24 circumpolar time series (Gauthier et al. 2024, Proc. R. Soc. B; Krebs review); there is presently no Arctic-wide collapse of the cycles, though they are sporadic at most sites and warm spells at snow onset reduce abundance. A single low year is the cycle, not an alert — the alert is the absence of a peak across two expected cycles |
| Migratory bird breeding success: shorebirds, waterfowl, seabirds where present; arrival and hatch timing | Breeding-habitat quality and phenology match — birds time hatching to the insect peak | Conditional — where breeding habitat is present; see also §15 | Nest monitoring / breeding-bird survey protocols per §15; CAFF CBMP; object baseline. No universal threshold: breeding success is judged against the site's own multi-year mean, and a mismatch year is recorded with the insect-emergence covariate |
| Insect emergence timing and abundance (notably chironomids / mosquitoes) | The food pulse for breeding birds and the phenology-mismatch signal | Conditional — where bird breeding is watched; Research where only modelled | Emergence traps / sweep-net protocol; object baseline. A shift in emergence relative to bird hatch dates is the indicator, not the absolute date |
| Coastal erosion rate (arctic coastal tundra): bluff retreat, m/yr; land area lost | How fast the coast is being eaten — permafrost bluffs collapse in blocks when undercut by waves | Conditional — arctic coastal tundra | Repeat high-resolution satellite / shoreline survey; object baseline and trend. Case values, not thresholds: Drew Point, Beaufort Sea coast, Alaska — mean annual erosion 17.2 m/yr for 2007–2016, 2.5 times faster than historic rates (Jones et al. 2018, USGS; ~7 m/yr in 1955–1979), with open-water-season rates from 6.7 m/yr (2010) to over 22 m/yr (2007, 2012, 2016); erosional TOC flux ~1,369 kg C/m/yr in the 21st century, nearly double the previous half-century (Shakun et al. / USGS, Front. Earth Sci. 2020). A retreat rate above the site's historic rate is at least amber |
| Fire: burned area, severity, season, fire return interval | The disturbance regime — fire was largely absent from tundra for ~11,000 years and is now increasing | Core for fire-prone tundra; see also §10 | Remote-sensing fire products (MODIS burned area) + management/fire-service records; object baseline. Case values, not thresholds: the 2007 Anaktuvuk River fire burned 1,039 km² of Alaska's North Slope — the largest fire on record for the tundra biome, doubling the cumulative area burned since 1950 — and released ~2.1 Tg C, about as much as the tundra biome's annual net C sink averaged over the last quarter of the 20th century, 60% of it from soil organic matter (Mack et al. 2011, Nature 475:489–492). No universal tundra fire interval exists; any fire on previously unburned tundra is recorded as an event |
| Post-fire recovery: vegetation return, permafrost response, thermokarst initiation after fire | Whether the tundra recovers or ratchets down after each fire — fire plus thaw is the compounding risk | Conditional — where fires occur | Repeat plot/remote-sensing monitoring; object baseline. Wildfire was disproportionately responsible for 10.5% of the thermokarst area detected 1950–2015 across 4,700 km² of Arctic Alaska while burning only 3.4% of the landscape (Chen et al. 2021, One Earth 4(12)). Recovery slower than the reference interval is the warning |
| Human pressure on tundra: infrastructure footprint (roads, pads, pipelines, mines, oil/gas), vehicle tracks, dust deposition, disturbance of calving and breeding areas | The direct pressure — a road across a calving ground changes the herd before the climate does | Conditional — where infrastructure is present; see also §17 | Land-cover / infrastructure mapping + management records; object baseline. Case value, not a threshold: a pan-Arctic study found 2,221 human-footprint clusters covering 21,402 km², with disturbed areas browning while stable areas greened (Liu et al. 2026, J. Remote Sens. 6, 1062, DOI 10.34133/remotesensing.1062 — verified against the full text). Any new infrastructure inside a calving ground or breeding area is at least amber |

### How §20 watch levels apply here

The catalogue's alert rule — a breach alerts only when sustained for the
window, a single spike never alerts — applies, but the window is
**seasonal to multi-year**, not hours: tundra vegetation, SOC, shrub
cover and active-layer thickness are read once a year at most, and a
trend needs repeat surveys, so the window is set in seasons or years in
the Object Passport, and a single year's low NDVI or one warm summer
never alerts on its own. An observation gap longer than the maximum gap
ends the episode and the indicator is recorded as stale, never as quiet.
Two tundra-specific rules sit on top of §20. **First, the cycle rule:**
lemming abundance, caribou numbers and bird breeding success are
cyclical or strongly variable by nature — a single low year is the
cycle, and the alert is the failure of the cycle itself (no lemming peak
across two expected cycles; a caribou herd still falling after
harvesting has stopped, as the Bathurst herd has). **Second, the
covariate-aware rule (§20) applies in its normal direction, with one
reversal:** a sustained warm-summer episode (temperature, §1) that is
itself in its own watch band can *explain* a greening or a thaw-lake
breach — the breach is logged as explained, not alerted — but warming
never explains a caribou breach or a rain-on-snow mortality event:
those are the consequences warming produces, not weather that excuses
them, and a rain-on-snow event is itself the driver that explains the
reindeer mortality, recorded with its extent and ice thickness. The
user-class thresholds (§20) are the herder's, the infrastructure
operator's and the conservation manager's: the same rain-on-snow icing
can mean "move the herd now" for the herder, "no action" for the
infrastructure operator, and "record the mortality event" for the
conservation manager; the same active-layer deepening can mean
"reinforce the foundations" for the operator and "watch the thermokarst"
for the reserve manager — all limits recorded in Phase 1 onboarding in
the Object Passport, in the same units (ice extent in km², active-layer
depth in cm, herd size in animals).

### What this section does NOT do

- It does **not duplicate §21**. Permafrost ground temperature, glacier
  velocity, glacial lakes, slope deformation and moraine dams live in
  §21; this section watches the tundra ecosystem on the frozen ground
  and cross-references §21 for the ground itself. A twin that carries
  both sections states the handoff explicitly; a twin that carries only
  this section records the permafrost temperature as a §21 gap, not as
  absent.
- It does **not set a universal shrub-cover, active-layer, SOC or fire
  threshold**. There is none. Shrubification rates, active-layer depth
  and SOC stocks depend on latitude, soil, ice content and vegetation
  type; the fire interval for tundra has no historical baseline at all
  (fire was largely absent for ~11,000 years). Every threshold is
  object-specific, set from the object's own baseline, and carries its
  named source and date.
- It does **not treat a greener satellite image as a healthier tundra**.
  NDVI rises with shrub invasion as readily as with native graminoid
  recovery; a green field of tall willow is not tundra recovery, and
  browning can be a single icing winter, not a collapse. Composition
  (PFT shares, lichen share) is the check on the greenness number, and
  a biomass claim without field calibration is refused.
- It does **not confuse a low year with a collapse**. Lemmings,
  caribou and breeding birds are cyclical: a low lemming year, a poor
  breeding season or one bad calving year is the cycle. The twin
  records the cycle phase alongside the value and alerts only on the
  failure of the cycle — the missing peak, the herd still falling after
  the pressure is removed.
- It does **not let warming explain away its own consequences**. A
  warm summer can explain a greening breach; it cannot explain a
  caribou decline, a reindeer die-off or a new thaw-slump field. Those
  are the consequences, and the twin records the driver (§1
  temperature, the rain-on-snow event) alongside them so the chain is
  visible, never silent.
- It does **not treat a single hot summer as a thaw verdict**.
  Thermokarst and active-layer change are multi-year processes with
  large site-to-site variation; the IPCC's own assessment gives only
  medium confidence to a region-wide active-layer increase. The twin
  reports the site trend with its uncertainty, and a one-year
  deepening is a state, never a trend.
- It does **not promote a carbon-stock number to a flux claim**.
  Tundra soils hold ~1,500 Pg of carbon, but the stock says nothing
  about this year's flux. A net-source claim needs flux measurement
  (chambers, eddy covariance), not a stock figure, and a stock figure
  is never presented as an emission.
- It does **not use caribou as a single-species verdict on the whole
  tundra**. Caribou are a keystone herbivore and a food-security
  indicator, but herds also cycle naturally and respond to hunting,
  roads and mines as well as to climate. The twin carries the lemming
  cycle, the bird breeding panel and the vegetation panel alongside the
  herd, and never reads one species alone.

Scope boundary: this section is a Conditional module, included only when the object contains tundra — with interface discipline built in: the twin ingests external monitoring frameworks (CAFF CBMP monitoring, GTN-P/CALM permafrost data, NOAA Arctic Report Card indicators, national herd censuses), never claims to set the herd size or the hunting quota itself, and records every handoff. The decision is recorded in the Object Passport at Phase 1.

Worked example (Toolik Lake tundra): published values now carried (see worked example): deciduous shrub cover 13.6% (1990) → 31.7% (2023), +132.3% (Betway-May et al. 2025, Glob. Change Biol. 31:e70155, DOI 10.1111/gcb.70155); mean maximum active-layer thickness 28–52 cm with no significant trend, permafrost temperature at 20 m +0.8 °C (Hobbie et al. 2017, Ambio 46(Suppl. 1):160–173, DOI 10.1007/s13280-016-0870-x); Central Arctic Herd 26,600 (photocensus 5 July 2025), down from 34,600 (2022) (ADF&G release 7 Jan 2026); SOC stock 5–25 kg C m⁻² in the flux footprint (Howard et al. 2020, Biogeosciences 17:4025–4042, DOI 10.5194/bg-17-4025-2020); CO₂/CH₄ fluxes Year 1 CH₄ 4.9, CO₂ 485 g C m⁻² yr⁻¹; Year 2 CH₄ 3.7, CO₂ 89 g C m⁻² yr⁻¹ (Howard et al. 2020). Remaining [NEXT DATA] gap: lemming densities at Toolik — not invented.

## 30. Forest

Include this section when the object is a forest stand, a management unit or a
forest landscape — boreal/taiga, temperate or tropical rainforest — or a mosaic
in which forest is a named component. For all other objects the passport records
"not applicable: no forest in the object" and the section is not carried. Forest
is the largest terrestrial ecosystem by area and by carbon stock, and it was the
last of the major biomes without its own module: before this section the twin
covered forest only through the shared rows — canopy cover, stand structure and
deadwood volume in §10, tree and shrub health in §11 — plus three gallery
teaching miniatures (forest-carbon, forest-fire, forest-logging, all synthetic,
on a Prince Albert Forest Management Area landscape). The numbers that make the
case: forest covers 4.14 billion ha — 32% of the land area — and holds 714 Gt of
carbon (FAO, Global Forest Resources Assessment 2025, published 21 October
2025). The net loss has slowed but not stopped: 4.12 M ha/yr in 2015–2025
against 4.7 M ha/yr in 2010–2020, with deforestation still 10.9 M ha/yr.
Primary forest is 1.18 B ha and its loss rate has halved since the early 2000s,
but the loss continues. One module covers the three forest biomes because the
indicator logic is the same (extent, structure, carbon, disturbance,
regeneration); the anchors and the reference values differ by biome and are set
from the object's own inventory and jurisdiction. Boundaries: forest-steppe
ecotones belong to the §22 fire and grazing rows where the question is the
steppe; forested peatlands belong to §24 for water-table and peat-carbon rows;
mangrove extent and canopy condition stay in §25; agroforestry and
silvopasture are farm systems and stay in §23; urban trees and urban canopy
equity stay in §26; a planted forest is forest (FRA 2025 counts 312 M ha of
planted forest, 8% of the total) and is covered here, with the natural-versus-
planted split recorded in the type row.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Forest extent and net area change, ha and ha/yr | Whether the forest is gaining or losing ground — the first number any forest twin reports | Core | FAO definition: land >0.5 ha, trees >5 m, canopy >10% (FRA 2025). Global reference: 4.14 B ha, 32% of land; net loss 4.12 M ha/yr 2015–2025 (down from 4.7 M ha/yr 2010–2020, FRA 2020); deforestation 10.9 M ha/yr; expansion 6.78 M ha/yr. Policy anchor: UN Strategic Plan for Forests, Global Forest Goal 1 — increase forest area by 3% worldwide by 2030 (120 M ha). Object baseline from national forest inventory / remote-sensing time series |
| Forest type and biome composition: boreal / temperate / tropical / subtropical share; natural vs planted | What kind of forest it is — a natural tropical rainforest and a planted boreal stand are different ecosystems with different values | Core | FRA 2025: naturally regenerating forest ~92% of the total (3.83 B ha), planted forest 8% (312 M ha). Domain shares (FRA 2020): tropical 45%, boreal 27%, temperate 16%, subtropical 11%. Object classification from inventory / remote sensing |
| Primary and old-growth forest area and share | How much of the forest has never been cleared — the irreplaceable core for biodiversity and carbon | Core | FRA 2025: 1.18 B ha of primary forest, about one-third of the reported forest area; the rate of primary-forest loss has halved since the early 2000s but continues (FRA 2020: 1.11 B ha). Object baseline; no universal "how much primary is enough" threshold — the watch is the trend, and any loss of primary forest is at least amber |
| Stand age-class distribution | Whether the forest has all ages or is one even-aged cohort — a single-age forest is one disturbance away from a gap | Core | National forest inventory practice; object baseline. No universal standard: the watch is a missing age class (no regeneration cohort, or no old stands) |
| Basal area and stem density by diameter class, m²/ha and stems/ha | The standing stock — the physical structure that carries timber, carbon and habitat | Core | National forest inventory practice; object baseline. Case values, not thresholds: European average growing stock 171.5 m³/ha in 2025 (169 m³/ha in 2020) — Forest Europe, State of Europe's Forests 2025; Harvard Forest pretreatment basal area 29.6–53.0 m²/ha across eight experimental plots (Ellison et al. 2010) |
| Aboveground biomass carbon stock, t C/ha | The carbon the forest holds in living wood — the stock the climate accounts count | Core | IPCC 2006/2019 guidelines: five carbon pools (aboveground and belowground biomass, deadwood, litter, soil organic carbon). Global reference: total forest carbon 714 Gt in 2025, up from 662 Gt in 2020 (FRA 2025; FRA 2020). Pan et al. 2011 (Science 333:988–993, DOI 10.1126/science.1201609): established forests took up 2.4 ± 0.4 Pg C/yr in 1990–2007; net global forest sink 1.1 ± 0.8 Pg C/yr. Object inventory; gallery forest-carbon miniature uses 52.00 t C/ha (2015) — synthetic teaching value, flagged as such |
| Forest soil organic carbon stock, t C/ha | The carbon under the forest — often as large as the biomass pool, and slower to recover when lost | Core | IPCC five-pool accounting; object inventory (soil sampling to a fixed depth, recorded). Case values, not thresholds: at Harvard Forest, soil to 45 cm holds ~45% of ecosystem carbon, live biomass ~50%, woody debris ~5% (Finzi et al. 2020). No universal soil-carbon threshold — the watch is the trend after disturbance |
| Net carbon flux: NEE / NEP, Mg C/ha/yr | Whether the forest is currently a sink or a source — the number that decides whether the carbon stock is growing | Conditional | Eddy-covariance flux towers; object baseline. Case values, not thresholds: Harvard Forest net uptake 2.0 ± 0.4 Mg C/ha/yr in 1993–2000 (biometry 1.6 ± 0.4; Barford et al. 2001, Science 294:1688–1691, DOI 10.1126/science.1062962); NEP ~300 g C/m²/yr in hardwood stands and ~450 g C/m²/yr in hemlock stands until the woolly adelgid arrived — hemlock stands turned into a net carbon source after 2014 (Finzi et al. 2020). A sink that flips to a source is red |
| Harvested area and volume against the allowable annual cut (AAC), ha/yr and m³/yr | Whether logging stays within what the forest can regrow — the sustainability test for any managed forest | Core where logging is present | National or provincial AAC determination; object management plan. Case values, not thresholds: British Columbia Prince George Timber Supply Area AAC 12.5 M m³/yr (2011 chief forester determination); BC total harvest 38.9 M m³ in 2023. Gallery forest-logging miniature (Prince Albert FMA, Saskatchewan): harvest 17,900 → 30,600 ha/yr in 2015–2025, 51.56 M m³ total — synthetic teaching data, flagged as such. Harvest above AAC, sustained, is red |
| Forest loss by driver: commodity / forestry / shifting agriculture / wildfire / urbanisation, ha/yr and share | What is actually removing the forest — permanent conversion and temporary loss need different answers | Conditional | Curtis et al. 2018 (Science 361:1108–1111, DOI 10.1126/science.aau3445): of global forest loss in 2001–2015, commodity-driven deforestation 27%, forestry 26%, shifting agriculture 24%, wildfire 23%, urbanisation <1%. Annual loss from Global Forest Watch / UMD GLAD; tropical primary forest loss 3.7 M ha in 2023, 6.7 M ha in 2024 (record) and 4.3 M ha in 2025 (Global Forest Watch / UMD GLAD, via World Resources Institute). Object attribution from remote sensing + management records |
| Pest and disease outbreak: area affected, mortality, host share | The biological disturbance — insects and pathogens can remove more timber than logging, and they change the forest's composition | Conditional | FRA 2025: pests, diseases and severe weather damaged 41 M ha of forest in 2020; fires affected ~261 M ha of land per year (about half of it forest). Case values, not thresholds: British Columbia mountain pine beetle — >18.3 M ha infested 1995–2015, 731 M m³ of pine killed (54% of merchantable pine volume), $57B GDP loss (Canadian Council of Forest Ministers). Harvard Forest: hemlock woolly adelgid arrived ~2009; hemlock ~25% of the forest; functional disappearance of hemlock expected by ~2025 (Ellison et al. 2010; Finzi et al. 2020). Object monitoring; any outbreak that kills a foundation species is at least amber |
| Forest fragmentation: core area, edge density, patch size | Whether the forest is one connected habitat or a scatter of fragments — fragmentation decides what species can live there | Core | §10 landscape metrics (patch size, edge, connectivity); object baseline from remote sensing. No universal fragmentation threshold — the watch is the trend in core area and in the largest patch |
| Regeneration: seedling and sapling density, natural-regeneration share | Whether the forest replaces itself — without regeneration the stand is a museum, not a living forest | Core | FRA 2025: 92% of the world's forests are naturally regenerating. National forest inventory regeneration surveys; object baseline. Harvard Forest Hemlock Removal Experiment: regeneration density differs between girdled plots (standing dead trees, slow disintegration) and logged plots (boles removed, soil compacted) — the disturbance type decides the next forest (Ellison et al. 2010) |
| Understory condition: shrub and herb layer cover, browse pressure | The layer where the next canopy grows — heavy browsing can stop regeneration for decades | Conditional | Field protocol; object baseline. Harvard Forest: ungulate browsers forage differently in adelgid-killed and logged stands, so the disturbance type changes the top-down control of regeneration (Faison et al. 2016, For. Ecol. Manage. 360:192–200, DOI 10.1016/j.foreco.2015.10.032). No universal browse threshold — set from the object's own baseline |
| Protected-area share and certified-forest share, % | How much of the forest is formally protected, and how much is managed under a certified scheme | Conditional | FRA 2025: 813 M ha of forest in protected areas (20% of the total), +251 M ha since 1990; 2.13 B ha (55%) under long-term management plans. Certification share (FSC / PEFC) from national registers; object baseline. No universal "enough protection" threshold |
| Canopy cover, stand structure, deadwood volume | Forest habitat quality and carbon storage — the shared structural row, not duplicated here | Cross-reference — see §10 | §10 row: canopy cover, stand structure, deadwood volume (Conditional — forests; national forest inventory practice). Case values for deadwood, not thresholds: European average 11.5 m³/ha, equal to 7.1% of the average growing stock (Forest Europe, State of Europe's Forests 2020, via EFI); 20–50 m³/ha is the threshold range to maintain the majority of saproxylic species, >100 m³/ha for the most demanding species (Müller & Bütler 2010, Biol. Conserv. 143:1733–1744); old-growth boreal forest in Finland 85.0 ± 27.8 m³/ha (De Meo et al. 2024) |
| Tree and shrub health: defoliation, dieback, regeneration | Forest condition and recruitment — the shared health row, not duplicated here | Cross-reference — see §11 | §11 row: tree and shrub health (Conditional — woody systems; forest inventory / health protocols). ICP Forests Level I/II crown-condition surveys where applicable |
| Forest soil condition: compaction, erosion, nutrient status | The ground the forest stands on — compaction and erosion outlast the harvest that caused them | Cross-reference — see §9 | §9 soil rows (compaction, erosion, nutrient status); forest-specific sampling by horizon |
| Forest-dependent fauna: presence, abundance, breeding success | Whether the animals that need the forest are still there — the fauna test of the forest's condition | Cross-reference — see §15 | §15 fauna rows; forest specialists (woodpeckers, cavity nesters, large carnivores, forest birds) as the diagnostic group |
| Forest fire regime: burned area, severity, return interval | The disturbance regime — too frequent fire and too rare fire are both degradation | Cross-reference — see §10 | §10 row: fire regime (Conditional — fire systems; remote-sensing fire products, management records). Global context: global burned area fell 24.3 ± 8.8% in 1998–2015 (Andela et al. 2017, Science 356:1356–1362, DOI 10.1126/science.aal4108); fires affected ~261 M ha of land per year, about half of it forest (FRA 2025); Canada burned a record 18.5 M ha in 2023 (CIFFC). Gallery forest-fire miniature (Prince Albert FMA): fire seasons 2019–2025 — synthetic teaching data, flagged as such |
| Mast yield index: cedar (Siberian pine) nut and berry crops — the bear forage base | The earliest warning signal for the taiga edge: a mast failure precedes the exits by weeks | Research — where large omnivores range near settlements; see §15/§17 | Forestry mast surveys or a mast index from the forest service; no published quantitative mast index for Buryatia for 2026 was found — [NEXT DATA]. Qualitative case values (2026): cedar nut "in many districts simply absent", berries down (Burprirodnadzor) |

### How §20 watch levels apply here

Forest rows use the same §20 rule as the rest of the catalogue: amber and red bands
are set from the anchor (law, standard, literature, or the object's own baseline
statistic); a breach alerts only when sustained (window,
`scripts/alert_bands.py --window-hours`); a single spike never alerts. Two
forest-specific notes:

- **Any loss of primary forest is at least amber.** There is no threshold at which
  clearing primary forest becomes acceptable; the watch is the trend, and the
  trend must be zero or negative.
- **A sink that flips to a source is red.** The carbon-flux row is the only row in
  this section where a sign change, not a level, is the red band — because a forest
  that has become a net source is no longer doing the job the climate accounts
  assume.

- **Taiga edge — human–bear conflict watch levels.** For a taiga-edge object the conflict-report series (§17) is the watched indicator and the mast index (§30, Research) is supporting context: a mast failure raises the watch, but the alert fires on the report series, because a Research-grade indicator never becomes an alert. Green is a normal mast year with isolated reports, of the order of the 2025 baseline (fewer than 1–2 a week across the republic); yellow is a mast failure with reports rising to several a week per district and the first exits of 2–3-year-old animals — warn residents, close trails, remove attractants, step up patrols; red is a repeat exit by the same animal, an attack on a person or livestock, or a bear inside a settlement, near a school or a tourist base — dispatch a brigade, regulate numbers, move schools to distance learning, as in Zakamensk in September 2026. The sustained-breach rule governs: one visit to a dump is an event; three visits in a week in one village is the sustained signal. (Case: Barguzinsky Reserve and the Buryatia taiga edge, autumn 2026 — second worked example under §30.)

### What this section does NOT do

- It does **not replace a forest inventory or a management plan**: it is a watch
  list, not a silvicultural prescription. Harvest levels, thinning regimes and
  species choice stay with the forester.
- It does **not set a universal "enough forest" threshold**: the 3% area increase
  is a UN global goal, not an object-level standard; the object-level watch is
  the trend against the object's own baseline.
- It does **not cover urban trees (§26), mangroves (§25), forested peatlands
  (§24 water-table rows) or agroforestry (§23)** — see the boundaries above.
- It does **not price carbon or timber**: no monetary valuation layer exists in
  the skill (see §16–§17); the carbon rows are physical units only.

Scope boundary: this section is a Conditional module, included only when the object
contains forest — with interface discipline built in: the twin ingests national
forest inventory data, remote-sensing time series (Hansen / Global Forest Watch
annual loss, FRA country reports) and the object's management plan, never claims
to set the allowable annual cut or the harvest schedule itself, and records every
handoff. The decision is recorded in the Object Passport at Phase 1.

Worked example (Harvard Forest, Petersham, Massachusetts): published values now
carried (see worked example): temperate mixed forest, ~1,500 ha, LTER since 1988;
hemlock ~25% of the forest; pretreatment basal area 29.6–53.0 m²/ha across the
eight Hemlock Removal Experiment plots (Ellison et al. 2010, Methods Ecol. Evol.
1:168–179); net uptake 2.0 ± 0.4 Mg C/ha/yr in 1993–2000 (Barford et al. 2001,
Science 294:1688–1691, DOI 10.1126/science.1062962); NEP ~300 g C/m²/yr in
hardwood stands and ~450 g C/m²/yr in hemlock stands, NEP +93% over 1992–2015,
hemlock stands net carbon source after 2014 (Finzi et al. 2020, Ecol. Monogr.
90(4), e01423, DOI 10.1002/ecm.1423); hemlock woolly adelgid arrived ~2009,
functional disappearance of hemlock expected by ~2025; girdled hemlocks died
within 30 months, logged plots lost 60–70% of basal area. Remaining [NEXT DATA]
gaps: current canopy-cover percentage, current deadwood volume, current
aboveground biomass stock (t C/ha), current regeneration density, landscape
fragmentation metrics — named, not invented.

## 31. Cropland

Include this section when the object is arable land — rainfed or irrigated annual
cropland, perennial cropland (orchards, vineyards, plantation crops where the rows
apply), or rice paddies — or a mosaic in which cropland is a named component. For
all other objects the passport records "not applicable: no cropland in the object"
and the section is not carried. Cropland is where the twin meets food: the most
intensively managed land on Earth, and the land where the twin's oldest shared rows
— soil carbon, nutrients and erosion in §9, the Agriculture quick set in §18 — were
doing the work of a module without being one. The numbers that make the case:
agriculture covers 4.8 billion ha — one-third of the world's land — and takes 72%
of global freshwater withdrawals (FAO, The State of the World's Land and Water
Resources 2025, SOLAW 2025). Irrigated land is only 22.5% of croplands but produces
48% of crop value, and irrigated yields run 76% above rainfed (SOLAW 2025). The
pressure side is just as large: 1.6 billion ha of land is degraded, 60% of it
agricultural (SOLAW 2025); 1,381 million ha of soils are salt-affected, including
10% of irrigated and 10% of rainfed cropland (FAO, Global Status of Salt-Affected
Soils 2024); cropland loses soil by water erosion at 12.7 t/ha/yr on average — over
four times the global mean of 2.8 t/ha/yr — some 17 Pg/yr from 1.43 billion ha of
cropland (Borrelli et al. 2017, Nature Communications 8:2013, DOI
10.1038/s41467-017-00232-0). Inorganic fertiliser use reached 185 Mt of nutrients
in 2022 — 108 Mt of nitrogen, 42 Mt of phosphorus, 35 Mt of potassium (FAO, FAOSTAT
Analytical Brief 90) — and pesticide use 3.54 Mt of active ingredients in 2021,
2.26 kg/ha of cropland, double the 1990 level (FAO, FAOSTAT Analytical Brief 70).
The counter-evidence is that management changes the outcome: more diverse crop
rotations raised maize yields by 28.1% on average across 347 site-years and cut
drought-year yield losses by 14.0–89.9% (Bowles et al. 2020, One Earth 2:284–293,
DOI 10.1016/j.oneear.2020.02.007). One module covers rainfed, irrigated and paddy
cropland because the indicator logic is the same (extent, rotation, soil, water,
nutrients, yield, margins); the anchors and the reference values differ by crop,
climate and jurisdiction and are set from the object's own records and standards.
A paddy is cropland with a water regime: the rice row below is the only row that
applies to paddies alone. Boundaries: natural grassland converted to cropland is
recorded here as a conversion in the extent row and in §22 as virgin-steppe loss —
the same event seen from two sides; the farm nutrient balance lives in §23 where
the question is the farm, and this section carries the field-level fertiliser
balance (manure applied to a field is recorded in both, with the same numbers);
cropland on drained peat belongs to §24 for water-table and peat-carbon rows;
salinisation under irrigation is carried here at field scale and in §28 at
landscape scale, agreeing on the ECe method; urban and peri-urban agriculture uses
this module for the field rows and §26 for the urban-system rows. Russian material
appears only as published-data anchors in the rows — Kursk chernozem SOC stocks
(Mikhailova & Post 2006) and erosion-linked SOC loss (Plotnikova et al. 2024) — and
in the FAO salt-affected-soils finding; there is no Russian worked example, pilot
or showcase case in this module.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Cropland extent and net area change, ha and ha/yr | Whether the arable base is gaining or losing ground — the first number any cropland twin reports | Core | Land-cover time series / farm records; object baseline. Global context: agriculture covers 4.8 B ha, one-third of the world's land (FAO, SOLAW 2025); cropland base 1.43 B ha in the global erosion assessment (Borrelli et al. 2017). Between 1964 and 2023 agricultural production tripled while agricultural land expanded only 8% — growth came from intensification, not expansion (SOLAW 2025). No universal "enough cropland" threshold — the watch is the trend and the conversion source (forest, steppe, wetland) |
| Crop type and cropping-system composition; cropping intensity | What grows, where, and how many crops a year the land carries — the system the rest of the rows describe | Core | Farm records / remote-sensing crop maps; cropping intensity = harvested area / physical area. Global context: in 2023, 22.5% of all croplands were equipped for irrigation and produced 48% of all crops in value terms; irrigated land is 3.2 times more productive than rainfed in value terms, and irrigated yields average 76% above rainfed (FAO, SOLAW 2025). Object baseline; no universal composition threshold |
| Crop rotation diversity and fallow share, % of arable area | Whether the rotation breaks pest and disease cycles, spreads risk and feeds the soil — the resilience row | Core | Rotation record: number of crops in the rotation, rotation diversity (Shannon index over crops), fallow share % of arable. Anchor: more diverse rotations raised maize yields by 28.1% on average across all growing conditions (22.6% in favourable conditions) and cut drought-year yield losses by 14.0–89.9% — 347 site-years, 11 long-term experiments, North America (Bowles et al. 2020, One Earth 2:284–293, DOI 10.1016/j.oneear.2020.02.007). No universal diversity number — the watch is a rotation shortening toward monoculture and a fallow share falling to zero |
| Tillage system: conventional / reduced / no-till share, % of arable area | How much the soil is disturbed — the management choice behind the SOC, erosion and compaction rows | Core | Farm records; object baseline. No universal share target: the right system depends on soil, climate and crop, and the SOC row below is the check on whether the chosen system is working |
| Soil organic carbon stock under tillage, t C/ha (0–30 cm), and trend | The carbon the field holds — the slow variable that decides whether the soil is being mined or built | Core | Soil sampling to a fixed depth (0–30 cm, recorded), repeated on a 3–5 year cycle; object baseline, trend over years. Case values, not thresholds: a global meta-analysis of 69 paired experiments found conversion from conventional to no-till did NOT increase total SOC to 40 cm — surface 0–10 cm gained 3.15 ± 2.42 t/ha while 20–40 cm lost 3.30 ± 1.61 t/ha — and cultivation of natural soils for >5 years lost >20 t/ha on average (Luo et al. 2010, Agric. Ecosyst. Environ. 139:224–231, DOI 10.1016/j.agee.2010.08.017). Published values, Kursk Haplic Chernozem (Russia): SOC in the top 2 m — native grassland 462 t/ha, yearly-cut meadow 451 t/ha, arable field 387 t/ha, continuous fallow 349 t/ha; 18–26% of the stock sits at 1–2 m (Mikhailova & Post 2006, Eur. J. Soil Sci. 57:330–336, DOI 10.1111/j.1365-2389.2005.00741.x); cultivation losses of 20–30% of the initial stock (Kogut 1998; Mikhailova & Post 2006). No universal SOC threshold — the watch is the trend |
| Irrigation water use and efficiency | Whether the water the field takes becomes crop or loss — the row that decides if irrigation is sustainable | Core where irrigated | Water metering / AQUASTAT method; irrigation water productivity kg/m³ (yield per m³ applied); application efficiency = beneficial use / withdrawal. Global context: agriculture accounts for 72% of global freshwater withdrawals (FAO, SOLAW 2025; AQUASTAT 2025). Case values, not thresholds: irrigation withdrawals run typically 1.6–2.5 times consumptive use, i.e. efficiency around 40–60% (Thenkabail et al. 2010, ISPRS Archives XXXVIII-8/W3). Object baseline; the watch is water use per tonne of yield rising while yield is flat, and a falling water table under the field (§8) |
| Soil salinisation: ECe trend and salt-affected share, % of cropland | Whether irrigation is salting the field it waters — the slow failure mode of irrigated agriculture | Core where irrigated, arid or coastal | Soil ECe (dS/m, saturated paste) and exchangeable sodium percentage; object baseline and trend. Global context: 1,381 Mha of soils are salt-affected (10.7% of global land); 10% of irrigated cropland and 10% of rainfed cropland are affected, with high uncertainty from limited data; salinity stress can cut yields of sensitive crops such as rice or beans by up to 70%; ten countries — including the Russian Federation — hold 70% of the world's salt-affected soils (FAO, Global Status of Salt-Affected Soils 2024). Crop anchor: rice threshold ECe 3.0 dS/m, yield falling 12% per dS/m beyond it (FAO Irrigation and Drainage Paper 29, Ayers & Westcot). A rising ECe trend on irrigated land is at least amber |
| Fertiliser N/P balance, nitrogen-use efficiency and runoff, kg/ha/yr | Whether nutrients feed the crop or leak to water and air — the balance the field must close every season | Core | Farm input records + harvested-product removal: N/P balance = inputs − removals; NUE = N in harvested product / N applied. Global context: inorganic fertiliser use in 2022 was 185 Mt of nutrients — N 108 Mt, P 42 Mt, K 35 Mt (FAO, FAOSTAT Analytical Brief 90). Nitrate in field drains and receiving water per §5/§8 rows. No universal surplus threshold — the watch is a persistent surplus on the same field and nitrate rising in the drain; a balance that never closes is at least amber |
| Direct N₂O emissions from fertilised soil, kg N₂O-N/ha/yr | The greenhouse-gas cost of the nitrogen the crop does not take up — the field's climate row | Conditional | IPCC Tier 1: direct emissions = 1% of N applied, as N₂O-N (EF1 = 0.01 kg N₂O-N per kg N applied; IPCC 2006 Guidelines, Vol. 4, Ch. 11, retained in the 2019 Refinement). Tier 2/3 from chamber or model estimates where available; object baseline. No universal threshold — the watch is emissions per tonne of yield rising while NUE falls |
| Pesticide pressure: use intensity and risk, kg a.i./ha/yr | How much chemical pressure the field, its margins and its water carry — and whether it is rising | Core | Farm spray records by class (herbicide / fungicide / insecticide), kg active ingredient per ha; risk-weighted where the jurisdiction runs a risk indicator. Global context: total pesticide use in agriculture in 2021 was 3.54 Mt of active ingredients, 2.26 kg/ha of cropland — up 4% on 2020, 11% in a decade, double the 1990 level (FAO, FAOSTAT Analytical Brief 70); an estimated 64% of agricultural land is at risk of pesticide pollution (FAO, SOLAW 2025). No universal intensity threshold — the watch is the trend by class and any use of a substance banned in the object's jurisdiction, which is red |
| Yield and yield stability, t/ha; coefficient of variation over ≥5 seasons | Whether the field produces, and whether it produces reliably — the outcome the other rows explain | Core | Harvest records / crop-cut surveys; mean yield and CV over at least 5 seasons, by crop and season. Case values, not thresholds: Sri Lanka paddy — national average yield, all schemes: 2022/23 Maha 3,731 kg/ha; 2023 Yala 4,128 kg/ha (Department of Census and Statistics, Paddy Statistics, revised series); paddy evapotranspiration Maha 470 mm, Yala 677 mm (Wanasinghe et al. 2023, Trop. Agric. Res. 34(2):148–161, DOI 10.4038/tar.v34i2.8626). The GEPIS Japonica target of 5.5–6.2 t/ha is a project target, not an observed yield (see worked example). A falling 5-year mean or a rising CV is at least amber |
| Soil erosion on arable land, t/ha/yr | Whether the field is losing the soil it stands on — the irreversible row: soil forms slower than it erodes | Core | RUSLE-family model + field evidence (rills, gullies, deposition); object baseline. Global anchor: cropland soil loss by water averages 12.7 t/ha/yr against a global mean of 2.8 t/ha/yr — over four times higher — some 17 Pg/yr from 1.43 B ha of cropland (Borrelli et al. 2017, Nat. Commun. 8:2013, DOI 10.1038/s41467-017-00232-0). Published values, Kursk arable Haplic Chernozems (Russia): SOC content falls significantly as the degree of water erosion rises, and the humus state deteriorates at the micro-level (Plotnikova et al. 2024, Agronomy 14(8):1607, DOI 10.3390/agronomy14081607). No universal tolerable-loss threshold — the watch is the rate against the object's own baseline and any gully initiation, which is red |
| Field-margin and biodiversity-strip share and condition, % of field boundary / field area | Whether the field keeps the strips that carry pollinators and pest enemies — the farm's own biodiversity infrastructure | Core | Field survey / remote sensing: margin share, strip width, flowering-plant diversity, perennial vs annual. Anchor: flower strips — but not hedgerows — enhanced pest-control services in adjacent fields by 16% on average (18 studies); pollination services declined exponentially with distance from plantings, and perennial, older, more diverse strips enhanced pollination more effectively (Albrecht et al. 2020, Ecol. Lett. 23:1488–1498, DOI 10.1111/ele.13576). No universal share threshold — the watch is margin loss and strips that exist on paper but carry no flowering plants |
| Crop residue fate and open-burning share, % of residue | Whether straw feeds the soil or goes up in smoke — the row that links SOC, air quality and the paddy methane row | Conditional | Farm records + satellite fire detections; share burned / incorporated / removed. No global anchor number — the watch is the burned share rising and any burning where incorporation is the stated practice; smoke and black-carbon exposure stay in §2 |
| Rice-paddy water regime and methane, kg CH₄/ha/season; flooding days | Whether the paddy's water regime is flooding the field — and the atmosphere — longer than the crop needs | Conditional — paddies only | Water-level log / irrigation records: continuous flooding vs single/multiple drainage (AWD); CH₄ by IPCC Tier 1 with the water-regime scaling factors, Tier 2/3 from chamber flux where available. Anchors: IPCC 2019 Refinement scaling factors — single drainage during the season 0.71, multiple drainage 0.55, relative to continuously flooded fields (IPCC 2006: single aeration 0.60, multiple 0.52); midseason drawdown cuts CH₄ by ~40% and AWD by ~50% on IPCC estimates (WRI working paper); US field studies found a single drain cut CH₄ by 39% and multiple drains by 83% (Linquist et al., via Field to Market 2017). Trade-off, recorded in the same row: draining raises N₂O — reported increases from 28.8% to more than 16-fold — so the paddy GHG row is CH₄ + N₂O together, never CH₄ alone. No measured CH₄ flux exists yet for the GEPIS site (see worked example) |
| Receiving-water nutrients and sediment | What the field sends downstream — the shared water-quality row, not duplicated here | Cross-reference — see §5 | §5 rows: nutrient forms and loads, sediment delivery; nitrate in drains from the fertiliser row above is read against §5 |
| Soil condition: nutrients, pH, compaction, contaminants | The ground the crop stands on — the shared soil rows, not duplicated here | Cross-reference — see §9 | §9 rows: SOC trend, moisture, texture/bulk density/compaction/infiltration, pH/ECe/salinity/sodicity, N/P/K, microbial biomass, erosion risk, ground cover, soil contaminants (metals, PAHs, pesticides, PFAS) |
| Landscape structure: field size, patch, connectivity, riparian buffers | Whether the arable landscape is a connected mosaic or a single bare block — the shared landscape rows | Cross-reference — see §10 | §10 rows: habitat extent and change, patch size / edge / core area, connectivity and corridors, riparian buffer width and condition; field size itself from the land-cover time series |
| Flora: weeds, crop wild relatives, red-list plants in margins | What grows that was not planted — the shared flora rows, not duplicated here | Cross-reference — see §11 | §11 rows: species richness, native vs alien composition, red-list plant populations, vegetation cover, phenology; crop wild relatives as the diagnostic group on arable land |
| Pollinators and soil invertebrates | The animals that pollinate the crop and build its soil — the shared invertebrate rows | Cross-reference — see §14 | §14 rows: pollinator activity and diversity, soil mesofauna; read with the field-margin row above (Albrecht et al. 2020) |
| Farmland birds and mammals | Whether the animals that need open farmland are still there — the fauna test of the field's condition | Cross-reference — see §15 | §15 rows: bird abundance, territory occupancy and breeding success; mammal occupancy; farmland specialists (skylark, lapwing, hares) as the diagnostic group |

### How §20 watch levels apply here

Cropland rows use the same §20 rule as the rest of the catalogue: amber and red bands
are set from the anchor (law, standard, literature, or the object's own baseline
statistic); a breach alerts only when sustained (window,
`scripts/alert_bands.py --window-hours`); a single spike never alerts. Three
cropland-specific notes:

- **A rising ECe trend on irrigated land is at least amber.** Salinisation is slow,
  nearly invisible season to season, and expensive to reverse; the watch is the trend,
  not a single reading.
- **A fertiliser balance that never closes is at least amber.** A persistent N or P
  surplus on the same field is a leak to water or air that has not happened yet in the
  records — it is already happening in the drain.
- **A paddy GHG row is CH₄ + N₂O together, never CH₄ alone.** Draining a paddy cuts
  methane and raises nitrous oxide; a twin that reports only the methane saving is
  reporting a saving that may not exist.

### What this section does NOT do

- It does **not replace an agronomic prescription**: it is a watch list, not a
  fertiliser recommendation, an irrigation schedule or a variety choice. Rates, timing
  and varieties stay with the agronomist.
- It does **not set a universal "enough yield" or "enough SOC" threshold**: the
  object-level watch is the trend against the object's own baseline and the published
  case values above.
- It does **not cover pasture and livestock (§23), natural grassland (§22), peat
  cropland water-table rows (§24) or urban agriculture's system rows (§26)** — see the
  boundaries above.
- It does **not price crops, water or carbon**: no monetary valuation layer exists in
  the skill (see §16–§17); the yield and water rows are physical units only, except
  where the worked example quotes a project price as a project fact.

Scope boundary: this section is a Conditional module, included only when the object contains
arable land — with interface discipline built in: the twin ingests farm records,
land-cover time series, soil surveys, water metering and the object's nutrient and
spray records, never claims to set fertiliser rates or irrigation schedules itself,
and records every handoff. The decision is recorded in the Object Passport at Phase 1.

Worked example (Rice paddies in Sri Lanka — the GEPIS site, Hambantota): published
values now carried (see worked example): starter area about 40 acres (about 16 ha)
at Mayurapura, growing premium Japonica rice on weathered soils structured with
tanakura clay and organic amendments, under regular agrochemical and toxicological
control; project target yield 5.5–6.2 t/ha at 450–600 LKR/kg — targets, not observed
yields (Baldanova et al., article v9.2); national paddy context — 2022/23 Maha 3,731 kg/ha, 2023 Yala 4,128 kg/ha (Department of Census and Statistics, Paddy Statistics, revised series);
paddy evapotranspiration Maha 470 mm, Yala 677 mm (Wanasinghe et al. 2023, Trop.
Agric. Res. 34(2):148–161, DOI 10.4038/tar.v34i2.8626); Sri Lanka's 2021 chemical-
fertiliser ban, the yield collapse that followed, and its reversal. Remaining
[NEXT DATA] gaps: measured yield, water applied per season and irrigation
efficiency at the GEPIS site; measured CH₄ flux and N₂O alongside it; SOC stock
(0–30 cm), ECe and fertiliser N/P rates at the site; field-margin share and
condition; erosion rate on the site — named, not invented. The USDA 2025/26 record
figures (3.7 Mt milled, 1.2 M ha, 4.62 t/ha rough) are the September 2026 USDA estimate. The record 3.7 Mt milled is confirmed by the USDA ERS Rice Outlook RCS-26H (15 September 2026), which also reports a higher harvested area and a 10% yield increase without giving the area or yield figures. The 1.2 M ha and 4.62 t/ha rough figures come from the trade press citing USDA (15 September 2026) and are not yet read from a USDA document; they are consistent arithmetically (1.2 M ha × 4.62 t/ha rough ≈ 5.5 Mt rough ≈ 3.7 Mt milled).

## 32. Non-peat wetlands and marshes

Include this section when the object is a freshwater marsh, a brackish
marsh, a salt marsh, a tidal freshwater marsh, a floodplain marsh, a reed
bed or a sedge meadow — or a mosaic in which a marsh is a named component.
For all other objects the passport records "not applicable: no non-peat
wetland in the object" and the section is not carried. Wetlands are the
fastest-disappearing ecosystem on Earth and the one the twin covered
least: before this section the catalogue held only the shared rows — water
level and water chemistry in §§3–4, nutrients in §5, macrophytes in §11,
fauna in §15 — plus one gallery teaching miniature (a synthetic wetland
prototype). There was no wetland extent, no hydroperiod, no salinity
regime, no sediment-accretion watch against sea-level rise, no
nutrient-retention account, no waterbird or fish-nursery test, no
invasive-reed watch and no drainage-pressure row. The numbers that make
the case: inland and coastal wetlands cover more than 12.1 million km² —
54% permanently inundated, 46% seasonally — and about 35% of the world's
natural wetlands were lost between 1970 and 2015, three times the rate of
forest loss (Ramsar Convention, Global Wetland Outlook 2018); the longer
view is worse: wetland loss since 1900 is estimated at 64–71% (Davidson 2014, Mar. Freshw. Res.
65:934, DOI 10.1071/MF14173), contested at ~21% net loss since 1700 (Fluet-Chouinard et al. 2023, Nature 614:281–286, CI 16–23%) — present as a range of estimates. One module covers the marsh types because
the indicator logic is the same (extent, water, vegetation, accretion,
retention, birds, fish, invaders, drainage); the anchors and the reference
values differ by type and jurisdiction and are set from the object's own
inventory and monitoring. Boundaries: peat-forming wetlands belong to §24
for water-table, peat-carbon and GHG rows — where a marsh sits on peat
(the Everglades sloughs and ridges are underlain by peat soils), the peat
rows are §24 and are not repeated here; mangrove extent and canopy
condition, seagrass extent and coral rows stay in §25 (salt marsh is §32;
the estuarine salinity gradient it shares with §25 is cross-referenced,
not duplicated); a rice paddy is a human-made wetland and stays in §31 —
a natural marsh farmed in the dry season is recorded in both, with the
§32 rows carrying the natural state and the §31 rows the production
state; the water-gauge panel and the chemical rows stay in §§3–4, and
§32 carries only the wetland-specific reading of them (hydroperiod,
phosphorus against the marsh criterion). No Russian worked example, pilot
or showcase case appears in this module; the regional case is Mongol Daguur, Mongolia.

| Indicator | What it tells | Tier | Typical anchor |
|---|---|---|---|
| Wetland extent and net area change, ha and ha/yr | Whether the marsh is gaining or losing ground — the first number any wetland twin reports | Core | Ramsar definition (Convention on Wetlands, Art. 1.1, 1971): areas of marsh, fen, peatland or water, natural or artificial, permanent or temporary, static or flowing, fresh, brackish or salt, including marine water under 6 m deep at low tide. Global reference: inland and coastal wetlands cover more than 12.1 M km², 54% permanently and 46% seasonally inundated; about 35% of natural wetlands lost 1970–2015, three times the rate of forest loss (Ramsar, Global Wetland Outlook 2018); 64–71% lost since 1900 (Davidson 2014, Mar. Freshw. Res. 65:934, DOI 10.1071/MF14173), contested at ~21% net loss since 1700 (Fluet-Chouinard et al. 2023, Nature 614:281–286) — present as a range of estimates. Object baseline from national wetland inventory / remote-sensing time series |
| Wetland type composition: freshwater marsh / brackish marsh / salt marsh / tidal freshwater marsh / floodplain marsh / reed bed / sedge meadow share | What kind of wetland it is — a salt marsh and a freshwater reed bed are different ecosystems with different values and different threats | Core | Ramsar wetland types (42 types, marine/coastal, inland, human-made); object classification from inventory / remote sensing. Case value, not a threshold: the Danube Delta holds the world's largest reed-bed expanse (UNESCO MAB; Ramsar site 521, 647,000 ha) |
| Hydroperiod: flooded duration (days/yr), timing of flooding and drying, flood depth | The master variable of a marsh — hydroperiod decides which plants grow, whether fish can reach the marsh, and whether birds can feed | Core | Object baseline from the water-gauge record (§3). Case values, not thresholds: Everglades landscape classes — long-hydroperiod sloughs flooded 11+ months a year, intermediate-hydroperiod sawgrass ridges 9–10 months, short-hydroperiod mixed-herb marshes 3–7 months (Davis & Ogden 1994, The Everglades: The Ecosystem and Its Restoration). A hydroperiod shortened by drainage or lengthened by impoundment is at least amber — the direction of change is the watch |
| Water-level regime: stage, amplitude, rate of change, connectivity to river, lake or sea | Whether the water arrives when the marsh needs it — a marsh fed by a dam release on a different calendar is a different marsh | Core | Object baseline from gauges and structure records (§3); Ramsar "wise use" and ecological-character reporting. Case value: the Everglades slopes southward at less than two inches per mile (≈3 cm/km; Florida Museum — the Davis & Ogden 1994 overview gives ~2.5 inches per mile, so state the slope as about 2 inches per mile or less) from Lake Okeechobee, and the sheet flow crosses ~100 miles (161 km) to Florida Bay (Florida Museum). Compartmentalisation by levees and canals — about half the historic Everglades lost, the rest broken into impoundments — is the red pattern |
| Salinity regime (coastal and brackish marshes): salinity, seasonal range, saltwater-intrusion events | Whether the marsh stays fresh, brackish or salt — salinity decides the plant community, and intrusion is the sea's first claim on the marsh | Conditional — coastal and brackish marshes | Object baseline from conductivity/salinity monitoring (§4); estuarine gradient per §25. No universal salinity threshold — the watch is the trend and the intrusion event: a freshwater marsh that turns brackish is at least amber |
| Vegetation composition: reed, sedge and salt-marsh grass shares and zonation; dominant species cover | What grows in the marsh — the plant community is the marsh's own record of its water and salt | Core | Field survey / remote sensing; object baseline. Case values, not thresholds: Danube Delta — 9,581 species recorded in the 2017 biodiversity census of the Danube Delta Biosphere Reserve, up from about 7,440 in the 2008 census (Danube Delta National Institute, presented by M. Doroftei, via Agerpres; older summaries give over 5,500, Claudino-Sales 2018); 312 bird species and about 90 fish species (UNESCO MAB), of which 45 freshwater fish species (UNESCO World Heritage documentation); the world's largest reed beds. Everglades — sawgrass (Cladium jamaicense) dominant in the historic freshwater marsh, cattail (Typha domingensis) a minor species before enrichment (Brix et al. 2010, BMC Ecology 10:23). A dominant-species flip (sawgrass → cattail, sedge → reed) is at least amber |
| Sediment accretion and surface-elevation change against local sea-level rise, mm/yr | Whether the marsh can keep its head above the sea — accretion below sea-level rise is a drowning marsh, however healthy it looks today | Core where the marsh meets the sea; Conditional inland | Marker horizons / surface-elevation tables (SET); local tide-gauge sea-level trend. Case values, not thresholds: refractory organic matter can contribute at most ~3 mm/yr to accretion (Morris et al. 2016, Earth's Future — the abstract gives a maximum steady-state accretion from refractory organic matter of 0.3 cm/yr); a Georgia salt marsh accreted 1.55 mm/yr against 3.25 mm/yr of sea-level rise 1935–2018 and is projected to keep only 12% of its area by 2160 (Langston et al. 2021, Estuar. Coast. Shelf Sci. 249); Plum Island high marsh accretes ~2.5 mm/yr against ~2.6 mm/yr of local sea-level rise — dynamic equilibrium (PIE-LTER). Accretion persistently below local sea-level rise is red |
| Nutrient retention: inflow–outflow nitrogen and phosphorus retention, % and kg/ha/yr | Whether the marsh is still the kidney it is credited with being — a marsh that exports nutrients is a marsh that has stopped filtering | Conditional — where the marsh receives agricultural or urban runoff | Inflow–outflow mass balance at the marsh boundary; object baseline. Case values, not thresholds: the Olentangy River created wetland (Ohio) reduced phosphorus by nearly 60% and nitrate by 40% over two years of monitoring (Fink & Mitsch, Ecol. Eng., via Ohio State University News, 7 March 2005). A retention that falls to zero or turns negative (net export) is red |
| Soil carbon stock and GHG flux in mineral-soil marsh, t C/ha and g C/m²/yr | The carbon a non-peat marsh holds and whether it is a sink or a source — salt-marsh soils are a blue-carbon stock, and drainage turns them into a source | Conditional — where carbon is in scope | IPCC 2013 Wetlands Supplement: Tier 1 emission factors for rewetted, drained and flooded land; object soil sampling to a fixed depth. Case value, not a threshold: marshes that developed under rapid sea-level rise store more soil carbon than marshes that developed under stable sea level, because sea-level rise creates accommodation space (Rogers et al. 2019, via the NSF salt-marsh dynamics review). Peat carbon and peat GHG flux stay in §24 |
| Waterbird use: breeding pairs, staging counts, moulting counts, Ramsar Criterion 5/6 status | Whether the birds that depend on the marsh are still there — waterbirds are the marsh's most legible indicator, counted by thousands | Core where birds are a stated value of the site | Standard waterbird census (aerial + ground counts); Ramsar Criteria 5 (regularly supports ≥20,000 waterbirds) and 6 (≥1% of a biogeographic population). Case values, not thresholds: Everglades — 138,834 wading-bird nests across South Florida in the 2018 season (122,571 in the Everglades), white ibis 100,784 nests, the strongest season since the 1930s; white ibis then fell to 31,848 nests in 2022 and 22,003 in 2023 (−5% and −38% against the 10-year average); the 2025 drought season counted ~3,500 nests, the lowest in 30 years against a 10-year average above 47,000 (SFWMD South Florida Wading Bird Reports, via Audubon and the Palm Beach Post); nesting populations of five wading-bird species fell by as much as 90% from the 1930s to the 1980s (Ogden 1994). Mongol Daguur, Mongolia — staging counts of 2,000 geese, 4,000 shelducks, 20,000 ducks, 7,000 coots and over 10,000 gulls (Ramsar Information Sheet 1997). A breeding or staging count that falls below its 1% flyway threshold is red |
| Fish nursery function: juvenile density, growth and survival in the marsh and at the marsh edge | Whether the marsh raises the fish — a marsh that juveniles do not use is a marsh that has lost its nursery | Conditional — coastal and floodplain marshes with a fishery | Drop traps, fyke/pop nets, tethering survival experiments; object baseline against unvegetated reference habitat. Anchor: a habitat is a nursery if juveniles occur at higher density, survive better, or grow faster there than elsewhere, and it contributes more recruits to the adult population (Beck et al. 2001, BioScience 51:633–641, DOI 10.1641/0006-3568(2001)051[0633:TICAMO]2.0.CO;2); salt-marsh nursery value for nekton confirmed by meta-analysis (Minello et al. 2003, Mar. Ecol. Prog. Ser. 246:39). Case value: Har Us Nuur, Mongolia — endemic fish of Western Mongolia (Ramsar Information Sheet MN976RIS, which is internally inconsistent: three endemic species in its overview, five listed as endemic in its fauna section and under Criterion 4a — carry "three to five" until the site's current fish survey settles it). No universal juvenile-density threshold — the watch is the marsh-versus-reference comparison |
| Invasive species: reed/cattail expansion and other invaders, area and share | Whether the invader is taking the marsh — one grass can turn a diverse marsh into a monoculture | Conditional — where an invader is present or the marsh is connected to an invaded system | Field survey / remote sensing; object baseline. Case values, not thresholds: introduced Phragmites australis haplotype M arrived in North America in the 19th century (probably in ballast) and displaced the native haplotypes, which have disappeared from New England; it now dominates Atlantic-coast and Great Lakes marshes (Saltonstall 2002, PNAS 99(4):2445–2449, DOI 10.1073/pnas.032477999); in the Everglades, cattail expanded from the 1970s in nutrient-enriched zones of Water Conservation Area 3A, replacing sawgrass marsh (Belanger et al. 2009; Entry & Gottlieb 2014). A native dominant replaced over a growing share is at least amber; a native haplotype lost is red |
| Drainage and reclamation pressure: drained share, ditch/canal density, conversion rate, ha/yr | What is removing the marsh — drainage is the oldest and still the largest cause of wetland loss | Core | Object land-use and drainage records; remote-sensing time series. Global reference: wetland loss since 1900 estimated 64–71% (Davidson 2014), contested at ~21% net loss since 1700 (Fluet-Chouinard et al. 2023, Nature 614:281–286, CI 16–23%) — present as a range of estimates; about 35% lost 1970–2015, with the loss rate accelerating after 2000 (Ramsar GWO 2018). Case value: the historic Everglades covered ~4,000 sq mi (10,360 km²) before drainage began in the 1880s; about half remains — "less than half" per the Florida Museum, "just over half" per the Davis & Ogden 1994 overview, so carry it as about half — mostly broken into levee-and-canal impoundments. Any net loss of natural marsh is at least amber |
| Restoration state (non-peat): restored area and share, hydrology restored, vegetation recovery | Whether the marsh is coming back — restoration without a hydroperiod is gardening, not recovery | Conditional — where restoration is under way or planned | Management records; object baseline. No universal restoration threshold — the watch is the hydroperiod first (restored water regime), then the vegetation, then the birds. Peat rewetting stays in §24 |
| Surface-water quality in the marsh: total phosphorus, nitrogen forms, dissolved oxygen, turbidity | The water the marsh lives in — for an oligotrophic marsh, a few micrograms of phosphorus change everything | Cross-reference — see §4 | §4 water-quality rows. Case value, not a transferable threshold: in the Everglades, the long-term geometric mean total-phosphorus criterion is 10 µg/L (10 ppb) — flora and fauna begin to change just above it (Everglades Forever Act 1994; FDEP; Sklar et al. 2005, Front. Ecol. Environ. 3(3):161–169). The 10 µg/L number is an Everglades criterion, not a general marsh standard |
| Wetland soil condition: hydric soil, redox, salinity of the soil, compaction | The ground the marsh stands on — a drained marsh soil oxidises, subsides and does not come back | Cross-reference — see §9 | §9 soil rows (hydric-soil indicators, redox, salinity, compaction); marsh-specific sampling by horizon. Peat subsidence stays in §24 |
| Wetland patch structure: patch size, connectivity, edge, fragmentation | Whether the marsh is one connected wetland or a scatter of fragments — fragmentation decides what birds and fish can reach | Cross-reference — see §10 | §10 landscape metrics (patch size, edge, connectivity); object baseline from remote sensing |
| Macrophyte and wetland-plant health: indicator species presence, red-list wetland plants, dieback | The plant test of the marsh's condition — the shared flora row, not duplicated here | Cross-reference — see §11 | §11 flora rows; wetland indicator species and red-list plants as the diagnostic group |
| Wetland-dependent fauna beyond birds and fish: amphibians, mammals, reptiles — presence, abundance, breeding success | Whether the animals that need the marsh are still there — the fauna test of the marsh's condition | Cross-reference — see §15 | §15 fauna rows; marsh specialists (e.g. European mink in the Danube Delta; wild boar in the Hovd Gol delta, Har Us Nuur, Mongolia — 40–60 animals in the 1997 survey, Ramsar Information Sheet MN976RIS) as the diagnostic group |

### How §20 watch levels apply here

Wetland rows use the same §20 rule as the rest of the catalogue: amber and red
bands are set from the anchor (law, standard, literature, or the object's own
baseline statistic); a breach alerts only when sustained (window,
`scripts/alert_bands.py --window-hours`); a single spike never alerts. Two
wetland-specific notes:

- **Any net loss of natural marsh is at least amber.** There is no threshold
  at which draining a natural marsh becomes acceptable; the watch is the
  trend, and the trend must be zero or negative — the same rule the forest
  module applies to primary forest.
- **A hydroperiod that leaves its historic band is red when it stays
  there.** The hydroperiod row is the marsh's master variable: a slough
  that stops flooding for a season, or a ridge that stops drying, changes
  the plant community, the fish access and the bird feeding in the same
  year — the 2025 Everglades drought season (3,500 nests, the lowest in 30
  years) is what a broken hydroperiod looks like.

### What this section does NOT do

- It does **not replace a wetland inventory, a hydrological model or a
  management plan**: it is a watch list, not an engineering prescription.
  Water releases, ditch blocking and species choice stay with the
  hydrologist and the manager.
- It does **not set a universal "enough wetland" threshold**: the 35%
  global loss is a warning, not an object-level standard; the
  object-level watch is the trend against the object's own baseline.
- It does **not cover peatlands (§24 water-table and peat-carbon rows),
  mangroves and seagrass (§25), rice paddies (§31), or urban blue space
  (§26)** — see the boundaries above.
- It does **not price wetland services**: no monetary valuation layer
  exists in the skill (see §16–§17); the nutrient, carbon and fish rows
  are physical units only.
- It does **not use a Russian worked example, pilot or showcase case**. The regional case is Mongol
  Daguur, Mongolia.

Scope boundary: this section is a Conditional module, included only when the object
contains a non-peat wetland or marsh — with interface discipline built in:
the twin ingests the national wetland inventory, remote-sensing time series
(Ramsar Sites Information Service, Global Wetland Outlook country data)
and the object's gauge and census records, never claims to set water
releases or drainage schedules itself, and records every handoff. The
decision is recorded in the Object Passport at Phase 1.

Worked example (Everglades, Florida, USA; regional case Mongol Daguur,
Mongolia): published values now carried (see worked example): historic
Everglades ~4,000 sq mi (10,360 km²), about half remains (sources
differ: "less than half", Florida Museum; "just over half", Davis & Ogden
1994 overview), compartmentalised by levees and canals; hydroperiod classes — sloughs
flooded 11+ months a year, sawgrass ridges 9–10 months, short-hydroperiod
marshes 3–7 months (Davis & Ogden 1994); long-term geometric mean
total-phosphorus criterion 10 µg/L (Everglades Forever Act 1994; Sklar et
al. 2005, Front. Ecol. Environ. 3(3):161–169); cattail expansion from the
1970s in nutrient-enriched zones of Water Conservation Area 3A, replacing
sawgrass (Belanger et al. 2009; Entry & Gottlieb 2014); wading-bird
nesting — 138,834 nests across South Florida in the 2018 season (122,571
in the Everglades), white ibis 100,784, the strongest season since the
1930s; white ibis 31,848 nests in 2022 and 22,003 in 2023; the 2025
drought season counted ~3,500 nests, the lowest in 30 years (SFWMD South
Florida Wading Bird Reports); five wading-bird species down as much as
90% from the 1930s to the 1980s (Ogden 1994). Mongol Daguur, Mongolia —
Ramsar site 210,000 ha; staging counts of 2,000 geese, 4,000 shelducks,
20,000 ducks, 7,000 coots and over 10,000 gulls (Ramsar Information Sheet
1997); six crane species; Ogii Lake swan goose 845–2,985 (Tsegmid &
Uuganbayar 2006), 2,706 counted in the avifaunal survey. Remaining [NEXT
DATA] gaps: Everglades current sediment-accretion rate, current
fish-nursery densities, current saltwater-intrusion extent, current
EPA-wide nutrient-retention balance, current sawgrass-versus-cattail area
shares; Mongol Daguur hydroperiod and water-level series, sediment
accretion, nutrient retention, reed-bed area, fish-nursery densities and
a current waterbird count — named, not invented.
