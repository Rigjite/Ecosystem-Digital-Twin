# Gallery entry — biodiversity site: Khubsugul lakeshore birds (synthetic data)

## Management question

What birds are recorded at this site, and in what form can the records
be shared?

## Site

Lake Khubsugul (Khövsgöl), Mongolia, southern / central shore,
approx 51.0 N, 100.5 E. Mongolia's largest freshwater lake — it holds
about 70% of the country's freshwater — and an Important Bird Area
(BirdLife International); the lake and its taiga shore are protected
as Khubsugul National Park (1992). It drains south through the Egiin
Gol into the Selenga and on to Lake Baikal. About 291 bird species
are recorded around the lake, 258 of them migratory.

## Data

SYNTHETIC: 20 records (`occurrences.csv`), deterministic formulas —
four shore points with a small deterministic jitter, observation dates
May–September 2026, datasetKey "synthetic". 18 species. One record is
unidentified ("Aves sp."). These numbers must never be cited as data.

No real records are used. A real GBIF occurrence-search pull for this
site was attempted on 2026-10-26 and BLOCKED: the GBIF API returned
HTTP 403 from this environment, and the request must not be retried or
bypassed. A real-data version of this entry is possible later via a
live-browser GBIF pull.

Design anchors (not data): the published bird community of Lake
Khubsugul — the eBird hotspot checklist for Khatgal, the town at the
southern end of the lake (68 species), and the lake's best-known birds
(Baikal teal, bar-headed goose, black stork, Altai snowcock). The
sensitivity categories are the real IUCN Red List statuses of those
species (table below).

## Sensitivity

| Species | Common name | IUCN Red List | Category |
|---|---|---|---|
| *Emberiza aureola* | Yellow-breasted Bunting | Critically Endangered | extreme |
| *Aythya ferina* | Common Pochard | Vulnerable | high (record 1); low (record 18) |
| *Aegypius monachus* | Cinereous Vulture | Near Threatened | low |
| *Sibirionetta formosa* | Baikal Teal | Least Concern | low |
| *Anser indicus* | Bar-headed Goose | Least Concern | low |
| *Ciconia nigra* | Black Stork | Least Concern | low |
| *Tetraogallus altaicus* | Altai Snowcock | Least Concern | low |
| *Cygnus cygnus* | Whooper Swan | Least Concern | low |
| *Tadorna ferruginea* | Ruddy Shelduck | Least Concern | low |
| *Bucephala clangula* | Common Goldeneye | Least Concern | low |
| *Aythya fuligula* | Tufted Duck | Least Concern | low |
| *Mergus merganser* | Common Merganser | Least Concern | low |
| *Larus mongolicus* | Mongolian Gull | Least Concern | low |
| *Phalacrocorax carbo* | Great Cormorant | Least Concern | low |
| *Ardea cinerea* | Gray Heron | Least Concern | low |
| *Aquila chrysaetos* | Golden Eagle | Least Concern | low |
| *Spatula querquedula* | Garganey | Least Concern | low |

The sample contains one record of *Emberiza aureola* (yellow-breasted
bunting, IUCN Critically Endangered), published here with coordinates
WITHHELD (blank) — the skill withholds extreme-sensitivity coordinates
rather than rounding them. One record of *Aythya ferina* (common
pochard, IUCN Vulnerable, breeding season) is pre-rounded to the
0.1-degree grid in this file. All other records are Near Threatened or
Least Concern species; the runner generalizes them to the 0.1-degree
grid for the shared output anyway.

The category is per record, not per species: the second common pochard
record (August, passage) is low, while the June breeding-season record
is high.

Honest limit on the extreme record: the yellow-breasted bunting is a
Critically Endangered breeder of the Mongolian Khangai region — the
mountain system of the Khubsugul basin — but it is not a confirmed
record at this exact shore. It is included to demonstrate the withhold
rule, and the record itself is synthetic; no real observation at this
shore is claimed.

## What the run shows

Run: `python3 run.py` (from the skill root:
`python3 examples/gallery/biodiversity/run.py`). Standard library only.

| Step | Result |
|---|---|
| Generalize (`generalize_coords.py`) | 20 records: 19 generalized to the 0.1° grid, 1 withheld (the *Emberiza* record) |
| Check (`generalize_coords.py --check`) | Gate pass, 0 violations |
| Richness | 18 species in 4 cells of 0.1°, at most 7 species in one cell |
| Diversity (`diversity.py indices`) | Shannon H′ 2.86, Pielou J′ 0.99, taxonomic distinctness Δ+ 3.51 — counts are records per species (presence-only proxy, never abundance); Δ+ from `taxonomy.csv` (the Linnaean hierarchy of the lake's birds; the unidentified record, *Aves sp.*, is known only to class and contributes at distance 4) |

## Maturity

2 (Descriptive): what is recorded and how it may be shared — no
abundance, no trend, no forecast.

## Gaps

- [НЕТ ДАННЫХ] synthetic records — no real observations; illustrative only
- [НЕТ ДАННЫХ] presence-only records (no abundance, no effort data)
- [НЕТ ДАННЫХ] one record unidentified (Aves sp.)
- [НЕТ ДАННЫХ] no systematic survey (observer bias toward roads and the lakeshore)
