#!/usr/bin/env python3
"""
Calibration and verification scores (Phases 3-4, ecosystem-digital-twin skill).

Three subcommands, each reading one CSV and printing JSON:

  continuous  observed vs simulated series. Scores the hold-out period only
              (rows after --train-end). Naive baselines are built without
              looking at the hold-out: persistence and climatology
              (training-period mean per month, or per day of year, or
              overall). Persistence must match the forecast horizon:
              --persistence rolling (default) repeats the previous
              observation, the fair baseline for one-step-ahead forecasts;
              --persistence fixed repeats the last training observation, the
              fair baseline for forecasts all issued at the end of training. Reports bias, PBIAS, MAE, RMSE, NSE, KGE (Gupta et
              al. 2009) and the skill score 1 - MSE_model / MSE_baseline.
              Declared thresholds (--thresholds "NSE>=0.5,KGE>=0.3") and the
              rule "must beat every naive baseline" decide pass or fail.
  events      binary observed vs forecast events: hits, misses, false alarms,
              correct negatives, POD, FAR (false-alarm ratio), CSI, frequency
              bias; optional lead-time distribution of hits.
  brier       probabilistic event forecasts: Brier score, Brier skill score
              against a climatological probability, reliability table and the
              Murphy (1973) decomposition reliability - resolution + uncertainty.

Exit codes: 0 pass or no thresholds declared; 2 input error; 3 gate failed.
Scoring on the calibration data itself is refused unless --no-holdout is
given, and the output is then labeled "in-sample fit, not forecast skill".

Examples:
  python3 skill_scores.py continuous flows.csv --obs-col q_obs --sim-col q_sim \
      --train-end 2019-12-31 --thresholds "NSE>=0.5"
  python3 skill_scores.py events hindcast.csv --obs-col bloom --fcst-col warn --lead-col lead_h
  python3 skill_scores.py brier hindcast.csv --obs-col bloom --prob-col p --clim-prob 0.12
"""

import argparse
import csv
import json
import math
import re
import sys
from datetime import datetime, timezone

MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}
TRUE = {"1", "true", "yes", "y", "t"}
FALSE = {"0", "false", "no", "n", "f"}


def sniff_delimiter(path):
    """Comma, semicolon (common in European and Russian exports) or tab, from the header line."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        head = fh.readline()
    counts = {d: head.count(d) for d in (",", ";", "\t")}
    best = max(counts, key=counts.get)
    return best if counts[best] else ","


def to_number(text):
    """Parse a number; accepts a decimal comma ("3,5") as written in semicolon-separated exports."""
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


def fbool(text):
    if text is None:
        return None
    s = text.strip().lower()
    if s in TRUE:
        return 1
    if s in FALSE:
        return 0
    return None


def ftime(text):
    if text is None or not text.strip():
        return None
    try:
        t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def read_csv(path, needed):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        missing = [c for c in needed if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"columns not found in {path}: {missing}")
        return list(reader)


def mean(xs):
    return sum(xs) / len(xs)


def continuous_metrics(obs, sim):
    n = len(obs)
    mo, ms = mean(obs), mean(sim)
    err = [s - o for o, s in zip(obs, sim)]
    mse = sum(e * e for e in err) / n
    sso = sum((o - mo) ** 2 for o in obs)
    so = math.sqrt(sso / n)
    ss = math.sqrt(sum((s - ms) ** 2 for s in sim) / n)
    cov = sum((o - mo) * (s - ms) for o, s in zip(obs, sim)) / n
    r = cov / (so * ss) if so > 0 and ss > 0 else None
    alpha = ss / so if so > 0 else None
    beta = ms / mo if mo != 0 else None
    kge = None
    if r is not None and alpha is not None and beta is not None:
        kge = 1 - math.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
    return {
        "n": n, "mean_obs": mo, "mean_sim": ms,
        "bias": mean(err),
        "pbias": 100.0 * sum(err) / sum(obs) if sum(obs) != 0 else None,
        "mae": mean([abs(e) for e in err]),
        "rmse": math.sqrt(mse), "mse": mse,
        "nse": 1 - sum(e * e for e in err) / sso if sso > 0 else None,
        "kge": kge, "kge_r": r, "kge_alpha": alpha, "kge_beta": beta,
    }


THRESH = re.compile(r"^\s*(abs_)?([a-z_]+)\s*(>=|<=|>|<)\s*(-?[\d.]+)\s*$", re.I)


def check_thresholds(spec, metrics):
    results = []
    for part in [p for p in spec.split(",") if p.strip()]:
        m = THRESH.match(part)
        if not m:
            raise ValueError(f"cannot parse threshold '{part}' (use e.g. NSE>=0.5 or abs_pbias<=25)")
        use_abs, name, op, limit = bool(m.group(1)), m.group(2).lower(), m.group(3), float(m.group(4))
        value = metrics.get(name)
        if value is None:
            results.append({"threshold": part.strip(), "value": None, "pass": False,
                            "reason": f"metric '{name}' unavailable"})
            continue
        v = abs(value) if use_abs else value
        ok = {">=": v >= limit, "<=": v <= limit, ">": v > limit, "<": v < limit}[op]
        results.append({"threshold": part.strip(), "value": v, "pass": ok})
    return results


def cmd_continuous(a):
    rows = read_csv(a.input, [a.time_col, a.obs_col, a.sim_col])
    recs, bad_time = [], 0
    for r in rows:
        t, o, s = ftime(r[a.time_col]), fnum(r[a.obs_col]), fnum(r[a.sim_col])
        if t is not None:
            recs.append((t, o, s))
        else:
            bad_time += 1
    recs.sort(key=lambda x: x[0])
    if a.train_end is None and not a.no_holdout:
        raise ValueError("declare the hold-out split with --train-end (fixed before fitting), "
                         "or pass --no-holdout to score in-sample fit explicitly")
    cut = ftime(a.train_end) if a.train_end else None
    if a.train_end and cut is None:
        raise ValueError(f"--train-end '{a.train_end}' is not an ISO date")
    train = [x for x in recs if cut is not None and x[0] <= cut]
    test = [x for x in recs if cut is None or x[0] > cut]
    train_obs = [(t, o) for t, o, _ in (train if cut else recs) if o is not None]
    if len(train_obs) < 2:
        raise ValueError("need at least two observed training values to build baselines")

    def key(t):
        return t.month if a.season == "month" else (t.timetuple().tm_yday if a.season == "doy" else 0)

    groups = {}
    for t, o in train_obs:
        groups.setdefault(key(t), []).append(o)
    overall = mean([o for _, o in train_obs])
    clim = {k: mean(v) for k, v in groups.items()}

    last_obs = train_obs[-1][1] if cut else None
    pairs, pers, climv = [], [], []
    for t, o, s in test:
        if o is not None and s is not None and last_obs is not None:
            pairs.append((o, s))
            pers.append(last_obs)
            climv.append(clim.get(key(t), overall))
        if o is not None and a.persistence == "rolling":
            last_obs = o
    if len(pairs) < 3:
        raise ValueError(f"only {len(pairs)} scorable hold-out pairs; need at least 3")
    obs = [p[0] for p in pairs]
    sim = [p[1] for p in pairs]
    m = continuous_metrics(obs, sim)
    mse_pers = mean([(o - b) ** 2 for o, b in zip(obs, pers)])
    mse_clim = mean([(o - b) ** 2 for o, b in zip(obs, climv)])
    m["skill_vs_persistence"] = 1 - m["mse"] / mse_pers if mse_pers > 0 else None
    m["skill_vs_climatology"] = 1 - m["mse"] / mse_clim if mse_clim > 0 else None
    baseline_checks = [
        {"baseline": "persistence (" + ("previous observation" if a.persistence == "rolling"
                                         else "last training observation") + ")", "mse_baseline": mse_pers,
         "pass": m["skill_vs_persistence"] is not None and m["skill_vs_persistence"] > 0},
        {"baseline": f"climatology ({a.season}, training period only)", "mse_baseline": mse_clim,
         "pass": m["skill_vs_climatology"] is not None and m["skill_vs_climatology"] > 0},
    ]
    thresholds = check_thresholds(a.thresholds or "", m)
    warnings = []
    if len(pairs) < 20:
        warnings.append(f"only {len(pairs)} hold-out pairs: scores are fragile, report them with this count")
    if a.no_holdout:
        warnings.append("in-sample fit, not forecast skill: no hold-out was declared")
    failed = [t for t in thresholds if not t["pass"]] + [b for b in baseline_checks if not b["pass"]]
    unpaired = sum(1 for _, o, s in test if o is None or s is None)
    if unpaired:
        warnings.append(f"{unpaired} hold-out rows lack a valid observation or simulation and were not scored")
    if bad_time:
        warnings.append(f"{bad_time} rows have no valid timestamp and were ignored")
    out = {
        "mode": "continuous", "label": "in-sample fit, not forecast skill" if a.no_holdout else "hold-out skill",
        "train_end": a.train_end, "n_train_obs": len(train_obs), "metrics": m,
        "baselines": baseline_checks, "thresholds": thresholds,
        "gate": "fail" if failed else ("pass" if thresholds else "pass (baselines only; no thresholds declared)"),
        "warnings": warnings,
    }
    return out, bool(failed)


def cmd_events(a):
    cols = [a.obs_col, a.fcst_col] + ([a.lead_col] if a.lead_col else [])
    rows = read_csv(a.input, cols)
    h = m = f = c = 0
    leads, skipped = [], 0
    for r in rows:
        o, p = fbool(r[a.obs_col]), fbool(r[a.fcst_col])
        if o is None or p is None:
            skipped += 1
            continue
        if o and p:
            h += 1
            if a.lead_col:
                lv = fnum(r[a.lead_col])
                if lv is not None:
                    leads.append(lv)
        elif o and not p:
            m += 1
        elif p and not o:
            f += 1
        else:
            c += 1
    n = h + m + f + c
    if n == 0:
        raise ValueError("no rows with valid 0/1 values")

    def ratio(x, y):
        return x / y if y else None

    out = {
        "mode": "events", "n": n, "skipped_rows": skipped,
        "hits": h, "misses": m, "false_alarms": f, "correct_negatives": c,
        "observed_events": h + m, "base_rate": (h + m) / n,
        "pod": ratio(h, h + m), "far": ratio(f, h + f), "csi": ratio(h, h + m + f),
        "frequency_bias": ratio(h + f, h + m), "warnings": [],
    }
    if leads:
        s = sorted(leads)

        def q(p):
            k = (len(s) - 1) * p
            lo, hi = math.floor(k), math.ceil(k)
            return s[lo] + (s[hi] - s[lo]) * (k - lo)

        out["lead_time_of_hits"] = {"n": len(s), "min": s[0], "q25": q(0.25), "median": q(0.5),
                                    "q75": q(0.75), "max": s[-1]}
    if h + m < 5:
        out["warnings"].append(f"only {h + m} observed events: descriptive counts, not a statistical track record")
    return out, False


def cmd_brier(a):
    rows = read_csv(a.input, [a.obs_col, a.prob_col])
    pairs = []
    for r in rows:
        o, p = fbool(r[a.obs_col]), fnum(r[a.prob_col])
        if o is None or p is None:
            continue
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"probability {p} outside [0, 1]")
        pairs.append((p, o))
    n = len(pairs)
    if n == 0:
        raise ValueError("no rows with a valid probability and 0/1 outcome")
    obar = mean([o for _, o in pairs])
    bs = mean([(p - o) ** 2 for p, o in pairs])
    warnings = []
    if a.clim_prob is not None:
        clim, clim_label = a.clim_prob, "declared climatological probability"
    else:
        clim, clim_label = obar, "sample base rate (in-sample; declare --clim-prob from training data)"
        warnings.append("reference probability taken from the scored sample itself")
    bs_ref = mean([(clim - o) ** 2 for _, o in pairs])
    bins = []
    for k in range(a.bins):
        lo, hi = k / a.bins, (k + 1) / a.bins
        members = [(p, o) for p, o in pairs if (lo <= p < hi) or (k == a.bins - 1 and p == 1.0)]
        if members:
            bins.append({"bin": f"[{lo:.2f}, {hi:.2f}{']' if k == a.bins - 1 else ')'}",
                         "n": len(members), "mean_forecast": mean([p for p, _ in members]),
                         "observed_frequency": mean([o for _, o in members])})
    rel = sum(b["n"] * (b["mean_forecast"] - b["observed_frequency"]) ** 2 for b in bins) / n
    res = sum(b["n"] * (b["observed_frequency"] - obar) ** 2 for b in bins) / n
    unc = obar * (1 - obar)
    if n < 30:
        warnings.append(f"only {n} forecasts: reliability table is indicative only")
    if sum(o for _, o in pairs) < 5:
        warnings.append("fewer than 5 observed events: Brier skill is not yet a track record")
    out = {
        "mode": "brier", "n": n, "observed_frequency": obar, "brier_score": bs,
        "reference": clim_label, "reference_probability": clim, "brier_reference": bs_ref,
        "brier_skill_score": 1 - bs / bs_ref if bs_ref > 0 else None,
        "decomposition": {"reliability": rel, "resolution": res, "uncertainty": unc,
                          "note": "BS ~= reliability - resolution + uncertainty (exact when forecasts within a bin are equal)"},
        "reliability_table": bins, "warnings": warnings,
    }
    return out, False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("continuous", help="observed vs simulated series")
    c.add_argument("input")
    c.add_argument("--time-col", default="time")
    c.add_argument("--obs-col", default="obs")
    c.add_argument("--sim-col", default="sim")
    c.add_argument("--train-end", help="last timestamp of the calibration period (ISO date)")
    c.add_argument("--no-holdout", action="store_true", help="score in-sample fit (labeled as such)")
    c.add_argument("--season", choices=["month", "doy", "none"], default="month")
    c.add_argument("--persistence", choices=["rolling", "fixed"], default="rolling",
                   help="rolling: one-step forecasts; fixed: forecasts issued at the end of training")
    c.add_argument("--thresholds", help='declared pass rules, e.g. "NSE>=0.5,abs_pbias<=25"')
    e = sub.add_parser("events", help="binary event forecasts")
    e.add_argument("input")
    e.add_argument("--obs-col", default="obs")
    e.add_argument("--fcst-col", default="fcst")
    e.add_argument("--lead-col")
    b = sub.add_parser("brier", help="probabilistic event forecasts")
    b.add_argument("input")
    b.add_argument("--obs-col", default="obs")
    b.add_argument("--prob-col", default="prob")
    b.add_argument("--clim-prob", type=float, help="climatological probability from the training period")
    b.add_argument("--bins", type=int, default=10)
    a = ap.parse_args(argv)
    try:
        out, failed = {"continuous": cmd_continuous, "events": cmd_events, "brier": cmd_brier}[a.cmd](a)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
