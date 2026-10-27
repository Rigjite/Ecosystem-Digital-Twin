#!/usr/bin/env python3
"""
Diversity indices (Round 3 of the v2.7 program, BioDT).

The skill had zero diversity indices: the gallery biodiversity entry
reported only richness (18 species) and cells. Richness alone misleads a
client — a falling Shannon or taxonomic distinctness is the real signal
of biodiversity loss, and it is the metric conservation clients and
IPBES-style reporting ask for.

Subcommands:

  indices   Shannon H' and Pielou evenness from counts, plus Clarke-Warwick
            taxonomic distinctness (Delta+) from the Linnaean hierarchy.
            The stdlib-feasible cousin of BioDT's phylogenetic-diversity
            prototype (Faith's PD needs a phylogeny; Delta+ needs only the
            taxonomic tree the skill already uses via the GBIF backbone).
  pft       plant functional type shares (see the pft subcommand help).

Indices (natural logarithm throughout):

  Shannon H' = -sum(p_i * ln p_i), p_i = count_i / N.
  Pielou J' = H' / ln(S), S = number of species with count > 0.
  Delta+ = mean taxonomic distance over all pairs of species present.
    Distance weights (Clarke-Warwick, equal step lengths): same genus 1,
    same family 2, same order 3, same class 4, same phylum 5, different
    phylum 6. A pair agrees at the deepest rank where both taxa are known
    and equal; a rank unknown for either taxon cannot agree, so the pair
    is judged at the next coarser rank (an unidentified record known only
    to class contributes at distance 4 against every bird).

Input: a counts CSV (species, count). With --taxonomy, a taxonomy CSV
(species, genus, family, order, class, phylum) for Delta+. Counts from
presence-only records are records per species — a proxy, stated as such
in the output; Delta+ needs presence, not abundance. Species in the
counts file but missing from the taxonomy are excluded from Delta+ and
named in the warnings.

Exit 0 on success; 2 on input error (missing columns, no species, a
negative count, a taxonomy with no usable ranks).

Usage:
  python3 diversity.py indices counts.csv --taxonomy taxonomy.csv
  python3 diversity.py pft cover.csv --pft-table pft.csv
"""

import argparse
import csv
import json
import math
import sys

RANKS = ("genus", "family", "order", "class", "phylum")
WEIGHTS = {"genus": 1, "family": 2, "order": 3, "class": 4, "phylum": 5}
MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}


def sniff_delimiter(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in (",", ";", "\t")}
    best = max(counts, key=counts.get)
    return best if counts[best] else ","


def read_csv(path, needed):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        missing = [c for c in needed if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"columns not found in {path}: {missing}")
        return list(reader)


def shannon(counts):
    """Shannon H' (natural log) from a list of counts > 0."""
    n = sum(counts)
    if n <= 0:
        raise ValueError("no counts: Shannon is undefined")
    return -sum((c / n) * math.log(c / n) for c in counts if c > 0)


def pielou(h, s):
    """Pielou evenness J' = H' / ln(S); None when S < 2."""
    if s < 2:
        return None
    return h / math.log(s)


def taxon_distance(a, b):
    """Clarke-Warwick distance between two taxa (dicts of rank -> name).

    The deepest rank where both are known and equal decides; a rank
    unknown for either cannot agree, so the pair falls through to the
    next coarser rank. No shared rank at all -> 6 (different phylum)."""
    for rank in RANKS:
        va = (a.get(rank) or "").strip()
        vb = (b.get(rank) or "").strip()
        if va and vb:
            if va == vb:
                return WEIGHTS[rank]
    return 6


def taxonomic_distinctness(taxa):
    """Delta+ = mean pairwise taxonomic distance over the taxa present.

    taxa is a list of rank dicts. Returns None with fewer than two taxa."""
    if len(taxa) < 2:
        return None
    total, pairs = 0, 0
    for i in range(len(taxa)):
        for j in range(i + 1, len(taxa)):
            total += taxon_distance(taxa[i], taxa[j])
            pairs += 1
    return total / pairs


def cmd_indices(a):
    rows = read_csv(a.input, ["species", "count"])
    counts = {}
    for r in rows:
        name = (r.get("species") or "").strip()
        if not name:
            raise ValueError("a counts row has no species name")
        try:
            c = float(r["count"])
        except (TypeError, ValueError):
            raise ValueError(f"count for {name!r} is not a number")
        if c < 0 or not math.isfinite(c):
            raise ValueError(f"count for {name!r} is negative or not finite")
        counts[name] = counts.get(name, 0.0) + c
    counts = {k: v for k, v in counts.items() if v > 0}
    if not counts:
        raise ValueError("no species with a count above zero")
    n = sum(counts.values())
    s = len(counts)
    h = shannon(list(counts.values()))
    warnings = []
    delta = None
    if a.taxonomy:
        trows = read_csv(a.taxonomy, ["species"] + list(RANKS))
        tax = {}
        for r in trows:
            name = (r.get("species") or "").strip()
            if name:
                tax[name] = {rank: (r.get(rank) or "").strip() for rank in RANKS}
        missing = [sp for sp in counts if sp not in tax]
        if missing:
            warnings.append(f"species missing from the taxonomy, excluded from Delta+: {missing}")
        usable = [tax[sp] for sp in counts if sp in tax]
        if len(usable) < 2:
            warnings.append("fewer than two species with taxonomy: Delta+ is not computed")
        else:
            delta = taxonomic_distinctness(usable)
            class_only = [sp for sp in counts if sp in tax
                          and not tax[sp]["genus"] and not tax[sp]["family"] and not tax[sp]["order"]]
            if class_only:
                warnings.append(f"species known only to class, contributing at distance 4: {class_only}")
    out = {"mode": "indices", "input": a.input, "taxonomy": a.taxonomy,
           "richness": s, "total": n, "shannon": h, "pielou": pielou(h, s),
           "delta_plus": delta,
           "per_species": [{"species": sp, "count": counts[sp],
                            "share": counts[sp] / n} for sp in sorted(counts)],
           "note": "Shannon and Pielou use the natural logarithm; Delta+ is the Clarke-Warwick "
                   "mean pairwise taxonomic distance (same genus 1, family 2, order 3, class 4, "
                   "phylum 5, different phylum 6). Counts from presence-only records are records "
                   "per species, a proxy — stated here, never silently treated as abundance.",
           "warnings": warnings}
    return out, False


def cmd_pft(a):
    """Plant functional type shares (Round 3 of the v2.7 program, BioDT).

    Input: a cover/count CSV (species, cover) and a PFT assignment table
    (--pft-table: species, pft, pathway, source). Shares are computed
    from one quantity only — cover or counts, never mixed — and reported
    per PFT (growth form) and per photosynthetic pathway. The assignment
    table is published per site (literature / TRY); a species missing
    from it is excluded from the shares and named. A trend needs repeat
    surveys; one survey reports shares only."""
    rows = read_csv(a.input, ["species", "cover"])
    cover = {}
    for r in rows:
        name = (r.get("species") or "").strip()
        if not name:
            raise ValueError("a cover row has no species name")
        try:
            c = float(r["cover"])
        except (TypeError, ValueError):
            raise ValueError(f"cover for {name!r} is not a number")
        if c < 0 or not math.isfinite(c):
            raise ValueError(f"cover for {name!r} is negative or not finite")
        cover[name] = cover.get(name, 0.0) + c
    cover = {k: v for k, v in cover.items() if v > 0}
    if not cover:
        raise ValueError("no species with cover above zero")
    trows = read_csv(a.pft_table, ["species", "pft", "pathway"])
    assign = {}
    for r in trows:
        name = (r.get("species") or "").strip()
        if name:
            assign[name] = {"pft": (r.get("pft") or "").strip(),
                            "pathway": (r.get("pathway") or "").strip()}
    total = sum(cover.values())
    warnings = []
    missing = [sp for sp in cover if sp not in assign]
    if missing:
        warnings.append(f"species missing from the PFT table, excluded from the shares: {missing}")
    by_pft, by_pathway = {}, {}
    for sp, c in cover.items():
        if sp not in assign:
            continue
        by_pft[assign[sp]["pft"]] = by_pft.get(assign[sp]["pft"], 0.0) + c
        by_pathway[assign[sp]["pathway"]] = by_pathway.get(assign[sp]["pathway"], 0.0) + c
    out = {"mode": "pft", "input": a.input, "pft_table": a.pft_table,
           "total": total, "n_species": len(cover),
           "shares_by_pft": {k: v / total for k, v in sorted(by_pft.items())},
           "shares_by_pathway": {k: v / total for k, v in sorted(by_pathway.items())},
           "note": "shares from one quantity only (cover here, or counts — never mixed); "
                   "the PFT assignment table is published per site; a trend needs repeat surveys, "
                   "one survey reports shares only",
           "warnings": warnings}
    return out, False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("indices", help="Shannon, Pielou and taxonomic distinctness from counts")
    i.add_argument("input", help="counts CSV: species, count")
    i.add_argument("--taxonomy", help="taxonomy CSV: species, genus, family, order, class, phylum")
    p = sub.add_parser("pft", help="plant functional type shares from cover/counts + a PFT table")
    p.add_argument("input", help="cover/count CSV: species, cover")
    p.add_argument("--pft-table", required=True, help="PFT assignment CSV: species, pft, pathway, source")
    a = ap.parse_args(argv)
    try:
        out, failed = {"indices": cmd_indices, "pft": cmd_pft}[a.cmd](a)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
