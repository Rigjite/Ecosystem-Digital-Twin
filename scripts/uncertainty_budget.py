#!/usr/bin/env python3
"""
Uncertainty budget for headline outputs (Phase 3, ecosystem-digital-twin skill).

The twin's model is run as ensembles; this script turns the ensemble results
into the budget every headline number ships with. Input CSV, one row per
ensemble member:

  output,source,member,value
  summer_chl,parameter,1,21.4
  summer_chl,forcing,1,19.8
  summer_chl,all,1,23.1
  ...

source is one of: measurement, forcing, parameter, structural, scenario
(one-at-a-time ensembles: only that source varies) and all (a joint ensemble
where every source varies together). For each output the script reports:

  - variance and standard deviation per source, and its share of the summed
    one-at-a-time variances;
  - from the joint ensemble: median and percentile interval (--interval),
    and the interaction term var(all) - sum(var per source). A large
    interaction means the one-at-a-time shares are only indicative; move to
    variance-based sensitivity analysis (Sobol) for that output.
  - which share is reducible (measurement, forcing, parameter, structural)
    and which lies in the future itself (scenario).

Without a joint ensemble no interval is produced: an interval is computed or
it is absent, never assumed. Exit 0 on success, 2 on input error.

Usage:
  python3 uncertainty_budget.py ensemble.csv --interval 90
"""

import argparse
import csv
import json
import math
import sys

SOURCES = ("measurement", "forcing", "parameter", "structural", "scenario")
REDUCIBLE = {"measurement", "forcing", "parameter", "structural"}


def sniff_delimiter(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in (",", ";", "\t")}
    best = max(counts, key=counts.get)
    return best if counts[best] else ","


def to_number(text):
    s = (text or "").strip()
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    v = float(s)
    if not math.isfinite(v):
        raise ValueError("not finite")
    return v


def variance(xs):
    n = len(xs)
    if n < 2:
        return None
    m = sum(xs) / n
    return sum((x - m) ** 2 for x in xs) / (n - 1)


def percentile(sorted_xs, p):
    k = (len(sorted_xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * (k - lo)


def budget(groups, interval):
    out = {"sources": {}, "warnings": []}
    unknown = [g for g in groups if g not in SOURCES and g != "all"]
    if unknown:
        raise ValueError(f"unknown source(s) {unknown}; use {', '.join(SOURCES)} or all")
    total_oat = 0.0
    for src in SOURCES:
        xs = groups.get(src)
        if not xs:
            out["sources"][src] = {"members": 0, "variance": None, "note": "not run - state why in the report"}
            continue
        v = variance(xs)
        if v is None:
            out["warnings"].append(f"{src}: one member only, no variance")
            out["sources"][src] = {"members": len(xs), "variance": None}
            continue
        total_oat += v
        out["sources"][src] = {"members": len(xs), "variance": v, "sd": math.sqrt(v),
                               "reducible": src in REDUCIBLE}
        if src == "structural" and len(xs) < 5:
            out["warnings"].append("structural spread comes from few model structures: name them in the report")
        elif len(xs) < 30 and src != "structural":
            out["warnings"].append(f"{src}: {len(xs)} members; shares are rough below ~30")
    for src, rec in out["sources"].items():
        if rec.get("variance") is not None and total_oat > 0:
            rec["share_of_one_at_a_time_sum"] = rec["variance"] / total_oat
    reducible = sum(r["variance"] for s, r in out["sources"].items()
                    if r.get("variance") is not None and s in REDUCIBLE)
    out["one_at_a_time_variance_sum"] = total_oat
    out["reducible_share"] = reducible / total_oat if total_oat > 0 else None
    joint = groups.get("all")
    if joint and len(joint) >= 2:
        s = sorted(joint)
        lo_p = (1 - interval / 100.0) / 2
        v_all = variance(joint)
        out["joint"] = {
            "members": len(joint), "median": percentile(s, 0.5), "variance": v_all, "sd": math.sqrt(v_all),
            "interval_level": interval, "interval": [percentile(s, lo_p), percentile(s, 1 - lo_p)],
            "interaction": v_all - total_oat,
        }
        if v_all > 0 and abs(v_all - total_oat) / v_all > 0.2:
            out["warnings"].append("sources interact (|interaction| > 20% of joint variance): one-at-a-time "
                                   "shares are indicative; use variance-based (Sobol) sensitivity analysis")
        if len(joint) < 100:
            out["warnings"].append(f"joint ensemble has {len(joint)} members; percentile interval is rough below ~100")
    else:
        out["joint"] = None
        out["warnings"].append("no joint ensemble ('all'): no interval is reported - run one before publishing an interval")
    return out


def sampling_priority(targets):
    """Spread-informed sampling priority (Round 3 of the v2.7 program,
    lake platforms). targets: list of (target, value_a, value_b) —
    the admitted model's value and the naive benchmark's, or two
    candidate models' values. Disagreement is |a - b|; the ranking is
    descending by disagreement, ties broken by input order (deterministic,
    stated). The top target is where the next sample goes: where the
    models disagree most, a measurement decides between them. Returns
    (ranked, sample_next)."""
    ranked = sorted(((abs(a - b), i, t, a, b) for i, (t, a, b) in enumerate(targets)),
                    key=lambda x: (-x[0], x[1]))
    out = [{"rank": k + 1, "target": t, "disagreement": d,
            "value_a": a, "value_b": b} for k, (d, _, t, a, b) in enumerate(ranked)]
    return out, out[0]["target"] if out else None


def cmd_sampling_priority(a):
    """Rank the next sampling targets by model disagreement. Input CSV:
    target + (model, naive) — the admitted model vs the naive benchmark —
    or (model_a, model_b) — two candidate models. Plugs into the VoI/EVSI
    machinery: it turns 'information has value' into 'sample here next'.
    Exit 0; 2 on input error."""
    with open(a.input, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.input))
        fields = reader.fieldnames or []
        if "target" not in fields:
            raise ValueError(f"column 'target' not found in {a.input}")
        if "model" in fields and "naive" in fields:
            cols, basis = ("model", "naive"), "admitted model vs naive benchmark"
        elif "model_a" in fields and "model_b" in fields:
            cols, basis = ("model_a", "model_b"), "candidate model A vs candidate model B"
        else:
            raise ValueError("need value columns 'model' + 'naive' or 'model_a' + 'model_b'")
        targets, bad = [], 0
        for r in reader:
            name = (r.get("target") or "").strip()
            if not name:
                bad += 1
                continue
            try:
                va, vb = to_number(r[cols[0]]), to_number(r[cols[1]])
            except ValueError:
                bad += 1
                continue
            targets.append((name, va, vb))
    if not targets:
        raise ValueError("no usable targets: need at least one target with two numeric values")
    ranked, sample_next = sampling_priority(targets)
    out = {"mode": "sampling-priority", "input": a.input, "basis": basis,
           "ranked": ranked, "sample_next": sample_next,
           "rule": "rank by |model - naive| (or |model A - model B|) descending; ties by input "
                   "order; sample the top target next — where the models disagree most, a "
                   "measurement decides between them",
           "warnings": ([f"{bad} row(s) lack a target or numeric values and were skipped"]
                        if bad else [])}
    return out, False


def main(argv=None):
    argv = list(sys.argv[1:]) if argv is None else list(argv)
    if argv and argv[0] == "sampling-priority":
        ap = argparse.ArgumentParser(description="Rank the next sampling targets by model disagreement "
                                                "(Round 3 of the v2.7 program, lake platforms).",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
        ap.add_argument("input", help="targets CSV: target + model/naive or model_a/model_b")
        a = ap.parse_args(argv[1:])
        try:
            out, failed = cmd_sampling_priority(a)
        except (ValueError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 3 if failed else 0
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--output-col", default="output")
    ap.add_argument("--source-col", default="source")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--interval", type=float, default=90.0, help="central interval level in percent")
    a = ap.parse_args(argv)
    if not 0 < a.interval < 100:
        print("error: --interval must be between 0 and 100", file=sys.stderr)
        return 2
    try:
        with open(a.input, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.input))
            needed = [a.source_col, a.value_col]
            missing = [c for c in needed if c not in (reader.fieldnames or [])]
            if missing:
                raise ValueError(f"columns not found: {missing}")
            data, bad = {}, 0
            for r in reader:
                try:
                    v = to_number(r[a.value_col])
                except ValueError:
                    bad += 1
                    continue
                out_name = r.get(a.output_col) or "output"
                data.setdefault(out_name, {}).setdefault(r[a.source_col].strip().lower(), []).append(v)
        results = {name: budget(groups, a.interval) for name, groups in data.items()}
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"input": a.input, "unparseable_rows": bad, "outputs": results,
                      "rule": "an interval is computed from the joint ensemble or not reported"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
