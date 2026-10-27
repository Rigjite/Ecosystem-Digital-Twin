# Prototype gallery — one small working twin per task type

Each entry is a runnable miniature: a small data file, a `run.py` that
reuses the skill's scripts, and a README stating the management
question, the maturity label, and the expected outputs. Run any entry
from the skill root, e.g. `python3 examples/gallery/pond/run.py`.
Every runner prints its summary JSON to stdout; `--out DIR` also writes
the intermediates and `summary.json` there. Standard library only.

Lakes are already covered by `examples/beira/` (real published data)
and `examples/lake-example.md` (teaching miniature), and the
linked-cascade shape by the v2.3 dry-run cascade — the gallery does not
duplicate them.

| Entry | Management question | Data | Maturity |
|---|---|---|---|
| `pond/` | Will summer chlorophyll exceed the bathing advisory watch levels? | Synthetic (deterministic formulas) | 3 Informative |
| `river/` | Are high-flow days increasing in this reach? | Real: USGS NWIS, Potomac at Little Falls, 81 daily values | 2 Descriptive |
| `field/` | Is the field drying toward the irrigation trigger? | Synthetic (deterministic formulas) | 2 Descriptive |
| `air/` | How many winter days exceed the WHO daily PM2.5 guideline? | Synthetic (deterministic formulas) | 2 Descriptive |
| `biodiversity/` | What birds are recorded here, and in what form may the records be shared? | Synthetic (deterministic formulas); anchors: published Khubsugul bird records, IUCN statuses | 2 Descriptive |
| `wetland/` | Is the treatment wetland still removing nutrients, and is the marsh drying? | Real: SFWMD STA-1W monthly TP 2008–09; USGS EDEN 10 daily level 2025–26 | 2 Descriptive |
| `forest-fire/` | Are forest fires becoming more frequent or larger in this landscape? | Synthetic (deterministic formulas); anchors: CIFFC 2023 record, Saskatchewan 2023, Prince Albert FMA | 2 Descriptive |
| `forest-logging/` | Where and how much forest is being lost to logging, and is the loss accelerating? | Synthetic (deterministic formulas); anchors: BC harvest totals, Prince George / Quesnel / Mackenzie AAC | 2 Descriptive |
| `forest-carbon/` | How much carbon does this forest store and accumulate, and is the stock growing or shrinking? | Synthetic (deterministic formulas); anchors: UNEP boreal biomass, Alberta sequestration, fire-entry burned areas | 2 Descriptive |

Synthetic entries are labelled synthetic in their READMEs and in the
runner summaries; their numbers must never be cited as data. Real
entries state the source, the fetch date, and the licence in their
READMEs. Every entry states its [НЕТ ДАННЫХ] gaps instead of filling
them.
