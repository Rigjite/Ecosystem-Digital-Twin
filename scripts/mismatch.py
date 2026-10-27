#!/usr/bin/env python3
"""
Mismatch register (calibration/audit step, ecosystem-digital-twin skill).

Learning from the pattern of the error: where the model missed, the
disagreement itself becomes a finding. For a spatial or categorical
prediction (e.g. which cells flood), compare the observed table against
the modeled table and score the *extent* — the fraction of observed
flooded cells the model correctly predicted — alongside the level score.
Then state the inferred hidden cause as a [ГИПОТЕЗА]/[НЕТ ДАННЫХ] item
and name the measurement that would confirm it. (Patos Lagoon: where
the flood model missed flooding, the team inferred a hidden pathway —
an underground drainage network without backflow control — from the
pattern of the disagreement itself.)

The register is the learning log, not a gate: the alert trial and the
hindcast reproduction gate are pass/fail (a failed gate revokes
admission); the mismatch register explains *why* a validation was bad
and turns the failure into the next data requirement. A failed
validation with no register entry is a score with no lesson.

Inputs are two CSVs with columns (cell, value) where value is 0/1
(flooded / not flooded, or the category under test): --observed the
measured table, --modeled the model's table. Both must list the same
cells; a cell in one table but not the other is an input error, not a
mismatch. With --register FILE the entry is appended to a JSON-lines
register (append-only, like the forecast registry but without the hash
chain — the register is a learning log, not a forecast record); --cause
and --confirm-measurement are required then, and may be the literal
"[НЕТ ДАННЫХ]" when no cause is yet inferred.

Usage:
  python3 mismatch.py --observed obs.csv --modeled mod.csv
  python3 mismatch.py --observed obs.csv --modeled mod.csv --register mismatches.jsonl \
      --id FLOOD-M-001 --cause "suspected underground drainage without backflow control [ГИПОТЕЗА]" \
      --confirm-measurement "drainage network survey of the missed cells" \
      --model "region-growing flood model" --model-version 1
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone


def sniff_delimiter(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in (",", ";", "\t")}
    best = max(counts, key=counts.get)
    return best if counts[best] else ","


def read_table(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        for col in ("cell", "value"):
            if col not in (reader.fieldnames or []):
                raise ValueError(f"column '{col}' not found in {path}")
        rows = list(reader)
    out = {}
    for row in rows:
        cell = (row.get("cell") or "").strip()
        if not cell:
            raise ValueError(f"{path}: a row has an empty cell id")
        if cell in out:
            raise ValueError(f"{path}: duplicate cell id '{cell}'")
        raw = (row.get("value") or "").strip()
        if raw not in ("0", "1"):
            raise ValueError(f"{path}: cell '{cell}' has value '{raw}', expected 0 or 1")
        out[cell] = int(raw)
    if not out:
        raise ValueError(f"{path}: no rows")
    return out


def compare(observed, modeled):
    if set(observed) != set(modeled):
        only_obs = sorted(set(observed) - set(modeled))
        only_mod = sorted(set(modeled) - set(observed))
        raise ValueError("cell sets differ: only in observed " + str(only_obs) +
                         "; only in modeled " + str(only_mod))
    obs_pos = {c for c, v in observed.items() if v == 1}
    mod_pos = {c for c, v in modeled.items() if v == 1}
    hits = sorted(obs_pos & mod_pos)
    misses = sorted(obs_pos - mod_pos)
    false_alarms = sorted(mod_pos - obs_pos)
    extent = (len(hits) / len(obs_pos)) if obs_pos else None
    return {"n_cells": len(observed), "n_observed": len(obs_pos), "n_modeled": len(mod_pos),
            "extent": extent, "hits": hits, "misses": misses, "false_alarms": false_alarms}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--observed", required=True, help="observed table CSV: cell, value (0/1)")
    ap.add_argument("--modeled", required=True, help="modeled table CSV: cell, value (0/1)")
    ap.add_argument("--register", help="JSON-lines register file to append the entry to")
    ap.add_argument("--id", help="mismatch entry id, e.g. FLOOD-M-001 (required with --register)")
    ap.add_argument("--cause", help="inferred hidden cause, a [ГИПОТЕЗА]/[НЕТ ДАННЫХ] item (required with --register)")
    ap.add_argument("--confirm-measurement", help="the measurement that would confirm the cause (required with --register)")
    ap.add_argument("--model", help="model name (recorded with --register)")
    ap.add_argument("--model-version", help="model version (recorded with --register)")
    a = ap.parse_args(argv)
    try:
        if a.register:
            for field in ("id", "cause", "confirm_measurement"):
                if not getattr(a, field):
                    raise ValueError(f"--{field.replace('_', '-')} is required with --register")
        observed = read_table(a.observed)
        modeled = read_table(a.modeled)
        result = compare(observed, modeled)
        result["rule"] = ("extent is the fraction of observed positives correctly predicted; "
                          "a miss is a finding, recorded with its inferred cause and the "
                          "measurement that would confirm it")
        if a.register:
            entry = {"type": "mismatch", "id": a.id,
                     "recorded_at": datetime.now(timezone.utc).isoformat(),
                     "model": a.model, "model_version": a.model_version,
                     "cause": a.cause, "confirm_measurement": a.confirm_measurement,
                     **{k: result[k] for k in ("n_cells", "n_observed", "n_modeled", "extent",
                                               "hits", "misses", "false_alarms")}}
            with open(a.register, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
            result["registered"] = entry
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
