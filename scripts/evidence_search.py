#!/usr/bin/env python3
"""
Evidence search for the ecosystem-digital-twin skill.

Queries the open literature platforms routed in references/evidence-sources.md
(PubMed, Europe PMC, OpenAlex, Crossref) and emits one normalized JSON array
that the literature-review skill's scripts/search_databases.py can
deduplicate, filter, rank, and format.

Normalized record fields: title, authors ("A and B" string), first_author,
year (int or null), source, doi, url, citations (int or null), abstract,
journal, plus provider ids (pmid, pmcid, openalex_id) as extra fields.

No API key is required. Pass --email with a real contact address: NCBI asks
for it, and Crossref/OpenAlex give polite-pool rates for identified traffic.
Requests are sequential with a delay; respect 429 responses by stopping the
affected source, never by hammering it.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "ecosystem-digital-twin/2.0 evidence-search"
TIMEOUT = 25


def fetch(url, params, accept="application/json"):
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    req = urllib.request.Request(f"{url}?{qs}", headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def clean(text):
    return re.sub(r"\s+", " ", (text or "")).strip()


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def year_of(value):
    if value is None:
        return None
    m = re.search(r"(1[5-9]\d{2}|20\d{2})", str(value))
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- PubMed
def search_pubmed(query, limit, email):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    common = {"tool": "ecosystem_digital_twin", "email": email}
    raw = fetch(f"{base}/esearch.fcgi", {**common, "db": "pubmed", "term": query,
                                         "retmode": "json", "retmax": limit, "sort": "relevance"})
    ids = json.loads(raw).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    time.sleep(0.4)
    xml_text = fetch(f"{base}/efetch.fcgi", {**common, "db": "pubmed", "id": ",".join(ids),
                                             "retmode": "xml"}, accept="application/xml")
    root = ET.fromstring(xml_text)
    records = []
    for art in root.iter("PubmedArticle"):
        title_el = art.find(".//ArticleTitle")
        title = clean("".join(title_el.itertext())) if title_el is not None else ""
        abstract = clean(" ".join("".join(a.itertext())
                                  for a in art.findall(".//Abstract/AbstractText")))
        authors, first_author = [], None
        for au in art.findall(".//AuthorList/Author"):
            last = clean(au.findtext("LastName") or "")
            initials = clean(au.findtext("Initials") or "")
            if last:
                authors.append(f"{last}, {initials}".strip(", "))
                if first_author is None:
                    first_author = last
        doi = None
        for el in art.findall(".//ELocationID"):
            if el.get("EIdType") == "doi":
                doi = clean(el.text)
        if not doi:
            for el in art.findall(".//ArticleId"):
                if el.get("IdType") == "doi":
                    doi = clean(el.text)
        pmid = clean(art.findtext(".//MedlineCitation/PMID") or "")
        year = year_of(art.findtext(".//JournalIssue/PubDate/Year")
                       or art.findtext(".//ArticleDate/Year")
                       or art.findtext(".//JournalIssue/PubDate/MedlineDate"))
        records.append({
            "title": title, "authors": " and ".join(authors), "first_author": first_author,
            "year": year, "source": "PubMed", "doi": doi or None,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
            "citations": None, "abstract": abstract or None,
            "journal": clean(art.findtext(".//Journal/Title") or "") or None,
            "pmid": pmid or None,
        })
    return records


# ---------------------------------------------------------------- Europe PMC
def search_europepmc(query, limit, email):
    raw = fetch("https://www.ebi.ac.uk/europepmc/webservices/rest/search",
                {"query": query, "format": "json", "resultType": "core",
                 "pageSize": limit, "email": email})
    results = json.loads(raw).get("resultList", {}).get("result", [])
    records = []
    for r in results:
        author_str = clean(r.get("authorString") or "")
        authors = author_str.rstrip(".")
        first = authors.split(",")[0].strip()
        parts = first.split()
        if len(parts) > 1 and parts[-1].isupper() and len(parts[-1]) <= 3:
            first = " ".join(parts[:-1])  # "Smith JA" -> "Smith", as the other sources report it
        first_author = first or None
        pmid = r.get("pmid")
        records.append({
            "title": clean(r.get("title") or ""), "authors": authors,
            "first_author": first_author, "year": to_int(r.get("pubYear")),
            "source": "Europe PMC", "doi": r.get("doi") or None,
            "url": (f"https://europepmc.org/article/MED/{pmid}" if pmid
                    else (f"https://doi.org/{r['doi']}" if r.get("doi") else None)),
            "citations": to_int(r.get("citedByCount")),
            "abstract": clean(r.get("abstractText") or "") or None,
            "journal": ((r.get("journalInfo") or {}).get("journal") or {}).get("title"),
            "pmid": pmid, "pmcid": r.get("pmcid"),
        })
    return records


# ---------------------------------------------------------------- OpenAlex
def search_openalex(query, limit, email):
    raw = fetch("https://api.openalex.org/works",
                {"search": query, "per_page": limit, "mailto": email})
    records = []
    for w in json.loads(raw).get("results", []):
        names = [clean((a.get("author") or {}).get("display_name") or "")
                 for a in w.get("authorships", [])]
        names = [n for n in names if n]
        abstract = None
        inv = w.get("abstract_inverted_index")
        if inv:
            words = {}
            for word, positions in inv.items():
                for pos in positions:
                    words[pos] = word
            abstract = clean(" ".join(words[i] for i in sorted(words))) or None
        doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
        records.append({
            "title": clean(w.get("title") or w.get("display_name") or ""),
            "authors": " and ".join(names),
            "first_author": (names[0].split()[-1] if names else None),
            "year": to_int(w.get("publication_year")), "source": "OpenAlex",
            "doi": doi, "url": f"https://doi.org/{doi}" if doi else w.get("id"),
            "citations": to_int(w.get("cited_by_count")), "abstract": abstract,
            "journal": (((w.get("primary_location") or {}).get("source") or {})
                        .get("display_name")),
            "openalex_id": w.get("id"),
        })
    return records


# ---------------------------------------------------------------- Crossref
def search_crossref(query, limit, email):
    raw = fetch("https://api.crossref.org/works",
                {"query": query, "rows": limit, "mailto": email})
    records = []
    for it in json.loads(raw).get("message", {}).get("items", []):
        names, first_author = [], None
        for a in it.get("author", []):
            family = clean(a.get("family") or "")
            given = clean(a.get("given") or "")
            if family:
                names.append(f"{family}, {given[0]}.".strip(", ") if given else family)
                if first_author is None:
                    first_author = family
        year = None
        for key in ("published-print", "published-online", "issued", "created"):
            parts = ((it.get(key) or {}).get("date-parts") or [[None]])[0]
            if parts and parts[0]:
                year = to_int(parts[0])
                break
        doi = it.get("DOI")
        records.append({
            "title": clean((it.get("title") or [""])[0]), "authors": " and ".join(names),
            "first_author": first_author, "year": year, "source": "Crossref",
            "doi": doi or None, "url": f"https://doi.org/{doi}" if doi else it.get("URL"),
            "citations": to_int(it.get("is-referenced-by-count")), "abstract": None,
            "journal": (it.get("container-title") or [None])[0],
        })
    return records


SOURCES = {"pubmed": search_pubmed, "europepmc": search_europepmc,
           "openalex": search_openalex, "crossref": search_crossref}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="search query (translated per platform by the caller)")
    parser.add_argument("--sources", default="pubmed,europepmc,openalex,crossref",
                        help="comma-separated subset of: " + ", ".join(SOURCES))
    parser.add_argument("--limit", type=int, default=10, help="max records per source")
    parser.add_argument("--email", default="", help="real contact email for polite API use")
    parser.add_argument("--output", help="write JSON array here instead of stdout")
    parser.add_argument("--delay", type=float, default=0.4, help="seconds between requests")
    args = parser.parse_args()

    if not args.email:
        print("[warn] no --email given: NCBI asks for a contact address, and Crossref/OpenAlex "
              "polite pools need one", file=sys.stderr)
    wanted = [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in wanted if s not in SOURCES]
    if unknown:
        parser.error(f"unknown sources: {unknown}; choose from {list(SOURCES)}")

    all_records, failures = [], []
    for i, name in enumerate(wanted):
        if i:
            time.sleep(args.delay)
        try:
            found = SOURCES[name](args.query, args.limit, args.email)
            print(f"[{name}] {len(found)} records", file=sys.stderr)
            all_records.extend(found)
        except urllib.error.HTTPError as exc:
            failures.append(name)
            if exc.code == 429:
                print(f"[{name}] THROTTLED (HTTP 429): source skipped, not retried; "
                      "add an API key or retry later", file=sys.stderr)
            else:
                print(f"[{name}] FAILED: HTTP {exc.code}", file=sys.stderr)
        except Exception as exc:  # one dead platform must not kill the search
            failures.append(name)
            print(f"[{name}] FAILED: {exc}", file=sys.stderr)

    payload = json.dumps(all_records, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
        print(f"[ok] {len(all_records)} records -> {args.output}", file=sys.stderr)
    else:
        print(payload)
    if failures:
        print(f"[summary] failed or skipped sources: {', '.join(failures)} - record this as a search "
              "limitation in the evidence log", file=sys.stderr)
    if failures and len(failures) == len(wanted):
        return 2
    return 0 if all_records else 1


if __name__ == "__main__":
    sys.exit(main())
