# Evidence sources — literature platforms

Literature is the twin's **evidence layer**, not a measurement layer. It never
substitutes for observations of the object. It justifies: which indicators to
select, which thresholds and methods are defensible, what effect a scenario
can plausibly have, and where published twins or monitoring programs have
already failed. Measurement data lives in `references/data-sources.md`;
published evidence lives here.

## Platform routing

No single platform covers an ecosystem twin. Route by question:

| Platform | Best for | Access | Endpoint / contract |
|---|---|---|---|
| **PubMed / PMC** (NCBI E-utilities) | Microbiology and sanitary indicators, pathogens, antimicrobial resistance, cyanotoxins and health risk, ecotoxicology, wildlife disease, molecular methods (eDNA, qPCR, source tracking) | Open; no key for small requests. Send `tool` and a real contact `email`; optional API key raises the shared limit from 3 to 10 requests/s | `esearch.fcgi` / `efetch.fcgi` on `eutils.ncbi.nlm.nih.gov/entrez/eutils/`; JSON IDs + XML records. Paging works within the first 10,000 matches — partition larger searches |
| **Europe PMC** | Life-sciences breadth beyond PubMed, open-access full text (JATS XML), preprints, methods detail | Open; no key | `https://www.ebi.ac.uk/europepmc/webservices/rest/search` with `format=json`, `resultType=core`; cursor pagination via `cursorMark`, up to 1,000 per page; full text at `/{PMCID}/fullTextXML` |
| **OpenAlex** | Cross-disciplinary discovery where PubMed is weak: hydrology, remote sensing, soil science, geomorphology, climate impacts; topic and citation mapping | Keyless casual reads; free key raises budget | `https://api.openalex.org/works` with `search`, `filter`, `per_page` ≤ 100; cursor paging via `meta.next_cursor` |
| **Crossref** | DOI and metadata verification — the identity layer for every citation the twin relies on | Open; `mailto` gives polite-pool rates | `https://api.crossref.org/works/{doi}` for a record; `/works?query=` for search. A Crossref 404 does not prove a DOI from another agency invalid |
| **Semantic Scholar** (Graph API) | Citation-graph expansion from a known seed paper; supplementary discovery | Open shared pool, throttled; key raises quota | `graph/v1/paper/search`; relevance search returns at most 1,000 records — discovery, never an exhaustive export |
| **AGRIS** (FAO) | Agriculture, fisheries, forestry, land and water management literature, including regional reports | Web discovery; no stable public bulk API is assumed | Search the web interface; record query and date like any other source |
| **Regional and national literature** (e.g. CyberLeninka — open; eLibrary — subscription, for Russian objects) | Local monitoring studies, regional species and water-body literature that English-language indexes miss | Web; subscription only where access actually exists | Mandatory for objects whose science is published mainly in the local language — for example, much Russian-language limnology is invisible to a PubMed-only search |
| **Scopus / Web of Science / CAB Abstracts** | Broad environmental and agricultural coverage | **Only with institutional access that actually exists** — never promise them in a plan without it | Export through the licensed interface; record the same provenance as open sources |
| **Google Scholar** | Last-resort discovery of a known title | No supported bulk API | Manual lookup only; stop on access blocks; never a pipeline source |

The bundled helper `scripts/evidence_search.py` queries PubMed, Europe PMC,
OpenAlex, and Crossref and emits normalized JSON that the **literature-review**
skill's search_databases.py helper (part of that skill, when installed) can
deduplicate and format. A throttled or failed platform is reported, skipped,
and recorded as a search limitation. Other platforms are searched through
their interfaces with the same provenance record.

## When the evidence layer runs

- **Phase 1 (with the data inventory):** an evidence inventory next to the
  data inventory — prior studies of this object or its analogues, published
  monitoring programs, known baselines.
- **Phase 2 (indicator selection):** every core indicator and every threshold
  anchor carries at least one evidence pointer (standard, guideline, or
  peer-reviewed method) beyond the catalogue's anchor column.
- **Phase 3 (calibration):** benchmark studies — published model performance
  for comparable objects — set realistic expectations before fitting.
- **Phase 5 (scenarios):** expected effect directions in `scenarios.md` are
  hypotheses; the evidence search supplies the published effect sizes and
  failure cases for the object's own context before a recommendation.
- **Before delivery:** re-run the key queries; literature that appeared after
  the build started can change a threshold or a method.

## Query protocol

1. Frame each search as a question: object or analogue + indicator/pressure +
   method or outcome. Synonym groups with OR, concepts combined with AND.
2. Translate the query per platform. Field syntax is not portable: PubMed
   `[MeSH]` tags, Europe PMC field syntax, and OpenAlex filters are different
   languages — record the actual translated query, not just keywords.
3. Search in English **and** the object's scientific language (for Russian
   objects: Russian terms in regional sources). A monolingual search is a
   stated limitation.
4. Record for every search: platform, exact query, date, filters, reported
   total, retrieved count, and any failure or cap. A capped retrieval is
   marked incomplete before screening.
5. Deduplicate across platforms by DOI, then by title (the literature-review
   helper does this); merge reports of the same study, keep every version.

## Evidence discipline

- **Hierarchy:** law and standards → international guidelines (WHO, OECD,
  CLRTAP, WFD-type frameworks) → systematic reviews and meta-analyses →
  multi-site monitoring studies → local studies of the object → single-site
  or analogue studies → expert judgment. A lower tier never silently
  overrides a higher one.
- **Abstracts screen; full text decides.** A numeric threshold, a method
  parameter, or an effect size enters the twin only from the full text or
  the standard itself — never from an abstract, a snippet, or a citing paper.
- **Transferability is checked, not assumed.** Before a published value moves
  to this object, record: water/land type, climate zone, jurisdiction,
  method compatibility, and the date of the evidence. Analogues from other
  countries are used comparatively — pattern first, transfer conditions
  stated — exactly as with analogue twins in `world-practice.md`.
- **Citation counts are discovery aids, not quality scores.** Screening is by
  protocol fit and method, not by venue or citation volume.
- **Retractions and corrections are checked** for any source a deliverable
  leans on (Crossref metadata and the platform record show update status).
- Every evidence item used in a deliverable enters the provenance package
  with: authors, year, title, platform, PMID/PMCID/DOI as available, the
  query that found it, retrieval date, evidence tier, and the twin element
  it supports (indicator, threshold, method, scenario expectation).
