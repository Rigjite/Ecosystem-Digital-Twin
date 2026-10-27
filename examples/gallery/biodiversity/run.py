#!/usr/bin/env python3
"""Gallery entry — biodiversity site: Khubsugul lakeshore birds (synthetic data).

Management question: what birds are recorded at this site, and in what
form can the records be shared?

Data are SYNTHETIC: 20 records, deterministic formulas (four shore
points on the southern / central shore of Lake Khubsugul (Khövsgöl),
Mongolia, approx 51.0 N, 100.5 E, with a small deterministic jitter),
datasetKey "synthetic". No real records are used: a real GBIF
occurrence-search pull for this site was attempted 2026-10-26 and
BLOCKED — the GBIF API returned HTTP 403 from this environment and
must not be retried or bypassed. A real-data version of this entry is
possible later via a live-browser GBIF pull. One record is
unidentified ("Aves sp.").

Design anchors (not data): the published bird community of Lake
Khubsugul — the eBird hotspot checklist for Khatgal (the town at the
southern end of the lake; 68 species) and the lake's best-known birds
(Baikal teal, bar-headed goose, black stork, Altai snowcock). The
sensitivity categories are the real IUCN Red List statuses of those
species (see the README).

Sensitivity (Non-Negotiable 3): the sample contains one record of
Emberiza aureola (yellow-breasted bunting, IUCN Critically Endangered),
published here with coordinates WITHHELD (blank) — the skill withholds
extreme-sensitivity coordinates rather than rounding them. One record
of Aythya ferina (common pochard, IUCN Vulnerable, breeding season)
is pre-rounded to the 0.1-degree grid in this file. All other records
are Near Threatened or Least Concern species; the runner generalizes
them to the 0.1-degree grid for the shared output anyway. The category
is per record, not per species: the second common pochard record
(August, passage) is low.

Run (from the skill root): python3 examples/gallery/biodiversity/run.py [--out DIR]
Prints the summary JSON to stdout; --out also writes the intermediates
and summary.json there. Standard library only.
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCRIPTS = os.path.join(ROOT, "scripts")


def run(script, *args):
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, timeout=120)
    if res.returncode not in (0, 3):
        raise SystemExit(f"{script} failed ({res.returncode}): {res.stderr.strip()}")
    return res.returncode, json.loads(res.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write intermediates and summary.json here")
    a = ap.parse_args()
    work = a.out or tempfile.mkdtemp(prefix="biodiversity_gallery_")
    os.makedirs(work, exist_ok=True)
    data = os.path.join(HERE, "occurrences.csv")
    with open(data, newline="") as fh:
        rows = list(csv.DictReader(fh))

    generalized = os.path.join(work, "generalized.csv")
    _, gen = run("generalize_coords.py", data,
                 "--category-col", "category", "--out", generalized)
    _, check = run("generalize_coords.py", "--check", generalized,
                   "--category-col", "category")
    with open(generalized, newline="") as fh:
        out_rows = list(csv.DictReader(fh))
    cells = {}
    for r in out_rows:
        if r["decimalLatitude"]:
            cells.setdefault((r["decimalLatitude"], r["decimalLongitude"]), set()).add(r["species"])
    counts = {}
    for r in rows:
        counts[r["species"]] = counts.get(r["species"], 0) + 1
    counts_csv = os.path.join(work, "counts.csv")
    with open(counts_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["species", "count"])
        for sp in sorted(counts):
            w.writerow([sp, counts[sp]])
    _, div = run("diversity.py", "indices", counts_csv,
                 "--taxonomy", os.path.join(HERE, "taxonomy.csv"))
    summary = {
        "entry": "biodiversity",
        "question": "What birds are recorded at this site, and in what form can the records be shared?",
        "data": "synthetic: deterministic formulas; Khubsugul lakeshore, Mongolia, approx 51.0 N 100.5 E, 20 records; GBIF pull blocked (HTTP 403)",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "records": len(rows),
        "species": len(set(r["species"] for r in rows)),
        "generalized": gen["generalized"],
        "withheld": gen["withheld"],
        "check": {"gate": check["gate"], "violations": check["violations"]},
        "cells_0_1_degree": len(cells),
        "max_species_per_cell": max(len(v) for v in cells.values()),
        "diversity": {"shannon": div["shannon"], "pielou": div["pielou"],
                      "delta_plus": div["delta_plus"],
                      "note": "counts are records per species (presence-only proxy, never "
                              "abundance); Delta+ from taxonomy.csv; the unidentified record "
                              "(Aves sp.) is known only to class and contributes at distance 4"},
        "gaps": ["[НЕТ ДАННЫХ] synthetic records — no real observations; illustrative only",
                 "[НЕТ ДАННЫХ] presence-only records (no abundance, no effort data)",
                 "[НЕТ ДАННЫХ] one record unidentified (Aves sp.)",
                 "[НЕТ ДАННЫХ] no systematic survey (observer bias toward roads and the lakeshore)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
