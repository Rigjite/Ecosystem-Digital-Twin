#!/usr/bin/env python3
"""
Sensitivity screen (Stage 3, ecosystem-digital-twin skill).

Before calibrating, rank the model parameters: perturb each one, one at
a time, and record how much the output metric moves. Calibrate only the
influential parameters; leave the rest at literature values — the screen
is what makes that choice defensible, instead of tuning every knob on
little data. (Gironde's TELEMAC work runs a sensitivity analysis before
calibrating, to "quickly reveal the most influential parameters which
can then be optimally calibrated".)

The model is the object's own deterministic model, supplied as a Python
file defining `run(params: dict) -> float` — the script never invents
the model, it only perturbs and records. Parameters come from a JSON
file: {"parameters": [{"name": ..., "value": ..., "perturb": 0.1}]}
where "perturb" is a fraction (0.1 = +/-10%), or {"range": [lo, hi]}
for absolute endpoints instead of a fraction. The output metric is
named with --metric (default "output").

Honest limit, stated here and in SKILL.md Stage 3: one-at-a-time
misses interactions, unlike Sobol indices. The screen ranks parameters;
it does not prove independence, and it never replaces a full
sensitivity analysis where the stakes demand one.

Boundary — screen vs driver-perturbation table: the screen perturbs
MODEL parameters (the calibration knobs — which parameter matters for
the fit); the driver-perturbation table (`references/scenarios.md`)
perturbs INPUT drivers (rainfall, nutrient load, abstraction, land use
— which external driver moves the indicator). Different questions,
different tables, never merged.

Usage:
  python3 sensitivity_screen.py model.py --params params.json [--metric tp]
  python3 sensitivity_screen.py model.py --params params.json --out screen.json
"""

import argparse
import importlib.util
import json
import math
import os
import sys


def load_model(path):
    if not os.path.exists(path):
        raise ValueError(f"model file '{path}' does not exist")
    spec = importlib.util.spec_from_file_location("screened_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not callable(getattr(mod, "run", None)):
        raise ValueError(f"model file '{path}' must define run(params) -> float")
    return mod


def load_params(path):
    with open(path, encoding="utf-8") as fh:
        spec = json.load(fh)
    params = spec.get("parameters")
    if not isinstance(params, list) or not params:
        raise ValueError("params file needs a non-empty 'parameters' list")
    out = []
    for p in params:
        if not isinstance(p, dict) or not isinstance(p.get("name"), str) or not p["name"].strip():
            raise ValueError("each parameter needs a non-empty 'name'")
        value = p.get("value")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise ValueError(f"parameter '{p['name']}': 'value' must be a finite number")
        if "perturb" in p and "range" in p:
            raise ValueError(f"parameter '{p['name']}': give 'perturb' or 'range', not both")
        if "perturb" in p:
            frac = p["perturb"]
            if not isinstance(frac, (int, float)) or isinstance(frac, bool) or not math.isfinite(frac) \
                    or not 0 < frac < 1:
                raise ValueError(f"parameter '{p['name']}': 'perturb' must be a fraction in (0, 1)")
            points = [value * (1 - frac), value * (1 + frac)]
        elif "range" in p:
            lo, hi = p["range"]
            if (not isinstance(lo, (int, float)) or isinstance(lo, bool)
                    or not isinstance(hi, (int, float)) or isinstance(hi, bool)
                    or not math.isfinite(lo) or not math.isfinite(hi) or not lo < hi):
                raise ValueError(f"parameter '{p['name']}': 'range' must be [lo, hi] with lo < hi, finite")
            points = [lo, hi]
        else:
            raise ValueError(f"parameter '{p['name']}': give 'perturb' (fraction) or 'range' ([lo, hi])")
        out.append({"name": p["name"], "value": value, "points": points})
    names = [p["name"] for p in out]
    if len(set(names)) != len(names):
        raise ValueError("parameter names must be unique")
    return out


def evaluate(model, values):
    result = model.run(dict(values))
    if not isinstance(result, (int, float)) or isinstance(result, bool) or not math.isfinite(result):
        raise ValueError("model run(params) must return a finite number")
    return float(result)


def screen(model, params, metric):
    base_values = {p["name"]: p["value"] for p in params}
    baseline = evaluate(model, base_values)
    rows = []
    for p in params:
        outs = []
        for point in p["points"]:
            trial = dict(base_values)
            trial[p["name"]] = point
            outs.append(evaluate(model, trial))
        changes = [o - baseline for o in outs]
        abs_change = max(abs(c) for c in changes)
        rel_change = (abs_change / abs(baseline)) if baseline != 0 else None
        rows.append({"parameter": p["name"], "value": p["value"],
                     "perturbed_values": p["points"], "outputs": outs,
                     "abs_change": abs_change, "rel_change": rel_change})
    # Rank by relative change; when the baseline is 0, relative change is
    # undefined, so those rows rank by absolute change below the ranked ones.
    ranked = sorted(rows, key=lambda r: (r["rel_change"] is None,
                                         -(r["rel_change"] if r["rel_change"] is not None else r["abs_change"])))
    for n, row in enumerate(ranked, start=1):
        row["rank"] = n
    return {"metric": metric, "baseline": baseline, "parameters": ranked,
            "rule": "calibrate only the influential parameters; the rest stay at literature values",
            "limit": "one-at-a-time misses interactions, unlike Sobol indices; the screen ranks, it does not prove independence"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model", help="Python file defining run(params: dict) -> float (the object's own deterministic model)")
    ap.add_argument("--params", required=True, help="JSON file: {\"parameters\": [{\"name\", \"value\", \"perturb\" | \"range\"}]}")
    ap.add_argument("--metric", default="output", help="name of the output metric (default 'output')")
    ap.add_argument("--out", help="write the ranked table as JSON here (in addition to stdout)")
    a = ap.parse_args(argv)
    try:
        model = load_model(a.model)
        params = load_params(a.params)
        result = screen(model, params, a.metric)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
