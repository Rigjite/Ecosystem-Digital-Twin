#!/usr/bin/env python3
"""
Trait-environment matching / extreme-condition screening (Round 3 of
the v2.7 program, BioDT).

Screen a taxon list against published environmental-tolerance tables
(temperature, soil acidity, salinity, drought) and return which taxa fit
the site's extremes — the deterministic core of BioDT's crop wild
relatives prototype (ModGP workflow). It answers the client's direct
question: which wild relatives / resilient varieties suit this site.

Input: a trait table CSV (taxon + trait columns, e.g. Ellenberg
indicator values T, F, R, N, S) and a conditions JSON file mapping each
trait to a rule:

  {"S": {"mode": "at_least", "value": 8},
   "T": {"mode": "within", "value": 6, "window": 1}}

A cell holding "x" means the source table is indifferent for that trait
(Ellenberg's "x": the taxon shows no preference) — such a taxon is NOT
excluded by a condition on that trait, and the output names it as
indifferent. A cell that is neither a number nor "x" is malformed and
refused (exit 2).

Modes: "at_least" — the taxon's value must reach the site's value
(a tolerance: salinity, drought); "within" — the taxon's value must fall
within the declared window around the site's value (an optimum:
temperature, pH). A taxon fits only when EVERY stated condition is met;
the output names, for each failing taxon, the condition it failed and the
values on both sides. The answer is the list that fits, not a ranking.

The trait table is published per object (Ellenberg indicator values for
the worked example shipped with the field gallery entry,
examples/gallery/field/trait_table.csv). Source of the shipped values:
the Ellenberg column in Tichý et al. 2023, "Ellenberg-type indicator
values for European vascular plant species", Zenodo record 7427088,
whose Germany source is Ellenberg & Leuschner (2010) — the revised
edition of Ellenberg et al. 1991 (Scripta Geobotanica 18). Verified
against that transcription 2026-10-26; Salicornia values are ssp.
europaea. A table transcribed for a build is verified against the
published source before client use.

Exit 0 on success; 2 on input error (missing trait column, unknown
mode, empty table, malformed conditions, a trait cell that is neither
a number nor "x").

Usage:
  python3 trait_match.py traits.csv --conditions conditions.json
"""

import argparse
import csv
import json
import math
import sys

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


def check_condition(value, rule):
    """One trait against one rule. Returns (fits, reason)."""
    mode = rule.get("mode")
    target = rule.get("value")
    if mode == "at_least":
        ok = value >= target
        reason = f"{value} >= {target}" if ok else f"{value} < {target} (needs >= {target})"
    elif mode == "within":
        window = rule.get("window")
        if window is None:
            raise ValueError("a 'within' rule needs a 'window'")
        ok = abs(value - target) <= window
        reason = (f"{value} within {target} ± {window}" if ok
                  else f"{value} outside {target} ± {window}")
    else:
        raise ValueError(f"unknown mode {mode!r} (use 'at_least' or 'within')")
    return ok, reason


def trait_match(taxa, conditions):
    """taxa: list of {taxon, trait: value | "x"}. conditions: {trait: rule}.

    Returns (fits, fails, indifferent) where fails maps taxon -> list of
    failed condition descriptions, and indifferent lists the
    (taxon, trait) pairs the source table marks indifferent ("x") for a
    trait a condition was stated on: such a taxon is NOT excluded by
    that condition, because the source assigns it no value there."""
    fits, fails, indifferent = [], {}, []
    for taxon in taxa:
        name = taxon["taxon"]
        failed = []
        for trait, rule in conditions.items():
            if trait not in taxon:
                raise ValueError(f"trait {trait!r} not in the table for {name!r}")
            value = taxon[trait]
            if value == "x":
                indifferent.append({"taxon": name, "trait": trait,
                                    "note": "indifferent in the source table: "
                                            "the condition on this trait does "
                                            "not exclude the taxon"})
                continue
            ok, reason = check_condition(value, rule)
            if not ok:
                failed.append(f"{trait}: {reason}")
        if failed:
            fails[name] = failed
        else:
            fits.append(name)
    return fits, fails, indifferent


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="trait table CSV: taxon + numeric trait columns")
    ap.add_argument("--conditions", required=True, help="JSON file: {trait: {mode, value, window?}}")
    a = ap.parse_args(argv)
    try:
        with open(a.conditions, encoding="utf-8") as fh:
            conditions = json.load(fh)
        if not isinstance(conditions, dict) or not conditions:
            raise ValueError("the conditions file needs at least one trait rule")
        for trait, rule in conditions.items():
            if not isinstance(rule, dict) or "mode" not in rule or "value" not in rule:
                raise ValueError(f"rule for {trait!r} needs 'mode' and 'value'")
            if rule["mode"] not in ("at_least", "within"):
                raise ValueError(f"unknown mode {rule['mode']!r} for {trait!r}")
            float(rule["value"])
            if rule["mode"] == "within":
                if rule.get("window") is None:
                    raise ValueError(f"rule for {trait!r} ('within') needs a 'window'")
                float(rule["window"])
        rows = read_csv(a.input, ["taxon"] + list(conditions))
        taxa = []
        for r in rows:
            name = (r.get("taxon") or "").strip()
            if not name:
                raise ValueError("a trait row has no taxon name")
            entry = {"taxon": name}
            for trait in conditions:
                cell = (r[trait] or "").strip()
                if cell.lower() == "x":
                    entry[trait] = "x"  # indifferent in the source table
                    continue
                try:
                    v = float(cell)
                except (TypeError, ValueError):
                    raise ValueError(f"trait {trait!r} for {name!r} is not a number "
                                     f"and not 'x' (indifferent)")
                if not math.isfinite(v):
                    raise ValueError(f"trait {trait!r} for {name!r} is not finite")
                entry[trait] = v
            taxa.append(entry)
        if not taxa:
            raise ValueError("the trait table is empty")
        fits, fails, indifferent = trait_match(taxa, conditions)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"mode": "trait_match", "input": a.input, "conditions": conditions,
                      "fits": fits,
                      "fails": [{"taxon": name, "failed": reasons} for name, reasons in fails.items()],
                      "indifferent": indifferent,
                      "note": "a taxon fits only when EVERY stated condition is met; the list that "
                              "fits is the answer, not a ranking; a taxon marked indifferent ('x') "
                              "for a trait is not excluded by a condition on that trait"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
