# Indicators and threshold anchors

## Contents
1 Climate and weather drivers · 2 Air quality and deposition · 3 Hydrology
and hydrometry · 4 Surface-water physical and chemical quality · 5 Nutrients
and eutrophication · 6 Contaminants · 7 Sediments · 8 Groundwater · 9 Soil and
land · 10 Landscape and disturbance · 11 Flora · 12 Microalgae and
phytoplankton · 13 Microbiology · 14 Invertebrates · 15 Fish and wildlife ·
16 Ecosystem functions · 17 Pressures and management response · **18 Domain
quick sets (start here)** · 19 Indicator metadata and quality requirements ·
20 Watch levels and alert rules

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

## 20. Watch levels and alert rules

A watch level is an amber or red band on an indicator, set per object from
its anchor (law, standard, literature, or the object's own baseline
statistic). A breach becomes an alert only when it is sustained — the
indicator stays in the band for at least the window (`scripts/alert_bands.py`
`--window-hours`); a single spike never alerts. An observation gap longer
than the maximum gap ends the episode. Every band carries its anchor; a
band without one is refused by the script.

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
