#!/usr/bin/env python3
"""
Seeded scenario generator (Round 1 of the v2.7 program, Digital Baikal).

Fits an AR(1) process to a driver series from the object's own data
(mean, sample SD, lag-1 autocorrelation) and generates N seeded scenario
series of the same length. Every generated value is a SCENARIO DRAW,
never a measurement: the output CSV and the JSON summary both say so, and
a generated series must never be cited as observed data. The scenarios
feed the existing pipeline — one generated column at a time into
trend_test.py / alert_bands.py — so a What-if scenario reports a
distribution ("in k of N seeded series the watch turns red") instead of
a single path.

Method: x_0 = mean + sd * z_0; x_t = mean + rho * (x_{t-1} - mean) + eps_t,
eps_t ~ Normal(0, sd * sqrt(1 - rho^2)), all draws from one
random.Random(seed). rho is clamped to [-0.99, 0.99] for stability; a
constant input series (sd 0) generates the mean on every step. The seed
is recorded in the output, so a run is reproducible from its summary
alone. The fitted distribution comes from the input series itself — no
external parameters are smuggled in.

With --watch (same band syntax as alert_bands.py, e.g. ">=25"), the
summary also reports how many of the N series breach the band at least
once. That is a breach count, not a sustained alert: sustained alerts
come from feeding a generated column to alert_bands.py.

Usage:
  python3 scenario_generate.py driver.csv --value-col rain --n 100 --seed 42 \
      --out scenarios.csv --watch ">=25"

Exit 0 on success, 2 on input error.
"""

import argparse
import csv
import json
import math
import random
import re
import sys
from datetime import datetime, timezone

MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}
BAND = re.compile(r"^\s*(<=|>=|<|>)\s*(-?[\d.,]+)\s*$")


def sniff_delimiter(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in (",", ";", "\t")}
    best = max(counts, key=counts.get)
    return best if counts[best] else ","


def to_number(text):
    s = text.strip()
    if s.count(",") == 1 and "." not in s:
        s = s.replace(",", ".")
    return float(s)


def fnum(text):
    if text is None or text.strip().lower() in MISSING:
        return None
    try:
        v = to_number(text)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def ftime(text):
    if text is None or not text.strip():
        return None
    try:
        t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def parse_band(spec):
    m = BAND.match(spec or "")
    if not m:
        raise ValueError(f"--watch must look like '<5' or '>=25', got {spec!r}")
    op, thr = m.group(1), to_number(m.group(2))
    test = {"<": lambda v: v < thr, "<=": lambda v: v <= thr,
            ">": lambda v: v > thr, ">=": lambda v: v >= thr}[op]
    return op, thr, test


def fit_ar1(values):
    """Mean, sample SD and lag-1 autocorrelation of the input series."""
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    sd = math.sqrt(var)
    den = sum((v - mean) ** 2 for v in values)
    if den == 0:
        return mean, sd, 0.0
    rho = sum((values[i] - mean) * (values[i + 1] - mean) for i in range(n - 1)) / den
    return mean, sd, max(-0.99, min(0.99, rho))


def generate(values_len, mean, sd, rho, n_series, seed):
    """N seeded AR(1) series, each as long as the input. Deterministic
    given the seed: one random.Random(seed), scenarios in order."""
    rng = random.Random(seed)
    innov = sd * math.sqrt(max(0.0, 1 - rho * rho)) if sd > 0 else 0.0
    out = []
    for _ in range(n_series):
        if sd == 0:
            out.append([mean] * values_len)
            continue
        series = [mean + sd * rng.gauss(0, 1)]
        for _ in range(1, values_len):
            series.append(mean + rho * (series[-1] - mean) + rng.gauss(0, innov))
        out.append(series)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="driver series CSV (time + value columns)")
    ap.add_argument("--time-col", default="time")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--n", type=int, default=100, help="number of seeded scenario series (default 100)")
    ap.add_argument("--seed", type=int, default=42, help="fixed seed; recorded in the output (default 42)")
    ap.add_argument("--out", required=True, help="output CSV: time + scenario_1..scenario_N columns")
    ap.add_argument("--watch", help="band, e.g. '>=25': report how many series breach it at least once")
    a = ap.parse_args(argv)
    try:
        if a.n < 1:
            raise ValueError("--n must be at least 1")
        watch = parse_band(a.watch) if a.watch else None
        with open(a.input, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.input))
            fields = reader.fieldnames or []
            for col in (a.time_col, a.value_col):
                if col not in fields:
                    raise ValueError(f"column '{col}' not found in {a.input}")
            has_qc = "qc_flag" in fields
            times, values, excluded = [], [], 0
            for r in reader:
                if has_qc and (r.get("qc_flag") or "").strip() not in ("ok", ""):
                    excluded += 1
                    continue
                t, v = ftime(r[a.time_col]), fnum(r[a.value_col])
                if t is not None and v is not None:
                    times.append(r[a.time_col])
                    values.append(v)
        if len(values) < 3:
            raise ValueError(f"only {len(values)} usable values; need at least 3 to fit the distribution")
        mean, sd, rho = fit_ar1(values)
        series = generate(len(values), mean, sd, rho, a.n, a.seed)
        cols = ["scenario_%d" % (k + 1) for k in range(a.n)]
        with open(a.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow([a.time_col] + cols)
            for i, t in enumerate(times):
                w.writerow([t] + [round(s[i], 6) for s in series])
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = {"mode": "scenario_generate", "input": a.input, "n_series": a.n,
           "n": len(values), "seed": a.seed,
           "fitted": {"mean": mean, "sd": sd, "lag1_rho": rho},
           "rows_excluded_qc": excluded, "out": a.out,
           "kind": "scenario draw, not a measurement",
           "rule": "generated values are scenario draws from the fitted distribution; "
                   "they are never cited as observed data"}
    if watch:
        op, thr, test = watch
        breaching = sum(1 for s in series if any(test(v) for v in s))
        out["watch"] = {"band": f"{op}{thr}", "scenarios_breaching": breaching,
                        "share": breaching / a.n,
                        "interpretation": f"in {breaching} of {a.n} seeded series the watch turns red "
                                          f"(at least one breach of {op}{thr})"}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
