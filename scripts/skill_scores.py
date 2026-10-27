#!/usr/bin/env python3
"""
Calibration and verification scores (Phases 3-4, ecosystem-digital-twin skill).

Eight subcommands, each reading one CSV and printing JSON (the last two
are the forecast-quality subcommands of Round 3 of the v2.7 program):

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
              Version 2.3 also reports SS_RMSE = 1 - RMSE_model / RMSE_naive
              (against the persistence baseline, with SS_RMSE vs climatology
              alongside) and an admission verdict: ADMITTED if and only if
              SS_RMSE > 0 on the declared hold-out; in-sample fits get no
              verdict. The MSE-ratio skill scores are kept unchanged — the
              two metrics share the > 0 boundary but differ in value.
  events      binary observed vs forecast events: hits, misses, false alarms,
              correct negatives, POD, FAR (false-alarm ratio), CSI, frequency
              bias; optional lead-time distribution of hits.
  brier       probabilistic event forecasts: Brier score, Brier skill score
              against a climatological probability, reliability table and the
              Murphy (1973) decomposition reliability - resolution + uncertainty.
  revalidate  continuous revalidation of an admitted model on a new batch:
              the combined series (calibration + new batch) with the
              ORIGINAL --train-end split; baselines are built from training
              data only, so the new batch never trains its own baseline.
              Reports the new SS_RMSE and verdict plus the status
              transition against --previous-verdict: SS_RMSE <= 0 revokes
              ADMITTED (status NOT_ADMITTED, maturity_action "drop").
  alert-trial scores the ALERTS on a hold-out window — precision (relevant
              alerts / all alerts), miss rate (missed critical events / all
              critical events), alarm volume — with admission thresholds:
              precision >= 0.9 (default --min-precision), zero missed
              criticals (default --max-missed-criticals 0), alarm count
              capped (optional --max-alarms). A window with no alerts and
              no critical events is INCONCLUSIVE_QUIET_WINDOW, not a FAIL:
              nothing to score, so it neither admits nor rejects, and
              admission waits for a synthetic stress-test or a historical
              extreme replay. Critical events with no alerts still FAIL —
              the model stayed silent when it mattered. Distinct from
              admission (SS_RMSE > 0), which scores the model, not the
              alerts.
  admit       calibration plausibility gate: admission requires (a) the model
              beats the naive benchmark on every PRIMARY target variable
              declared in the Object Passport (SS_RMSE > 0 for each;
              secondary background variables are reported, not gated —
              when no variable in the dossier carries a "primary" flag,
              every variable is primary, the pre-2.7 behaviour) and (b)
              every fitted parameter inside its declared physical bounds
              (references/calibration-bounds.md). A parameter outside its
              bounds is REJECTED even when SS_RMSE > 0. One of two
              admission gates; the alert trial is the other — both must
              pass.
  skill_horizon
              skill vs lead time: per lead bin, SS_RMSE of the forecast
              against the naive baseline supplied per row; the skill
              horizon is the longest lead at which the forecast still beats
              persistence (SS_RMSE > 0) with every shorter lead also above
              zero. A forecast is not trusted beyond its horizon.
  nudge       observation-nudged forecast: shift a raw forecast value by
              the mean model-minus-observed residual over the last N
              QC-passed observation/model pairs (N declared in the Object
              Passport); the correction is recorded in the registry entry
              and the nudged forecast is scored per lead time by
              skill_horizon like any forecast.

Exit codes: 0 pass or no thresholds declared; 2 input error; 3 gate failed.
For revalidate, exit 3 also means the admission was revoked.
Scoring on the calibration data itself is refused unless --no-holdout is
given, and the output is then labeled "in-sample fit, not forecast skill".
Revalidation has no --no-holdout: a re-score without a hold-out is refused.

Examples:
  python3 skill_scores.py continuous flows.csv --obs-col q_obs --sim-col q_sim \
      --train-end 2019-12-31 --thresholds "NSE>=0.5"
  python3 skill_scores.py events hindcast.csv --obs-col bloom --fcst-col warn --lead-col lead_h
  python3 skill_scores.py brier hindcast.csv --obs-col bloom --prob-col p --clim-prob 0.12
  python3 skill_scores.py revalidate flows.csv --obs-col q_obs --sim-col q_sim \
      --train-end 2019-12-31 --previous-verdict ADMITTED --previous-ss-rmse 0.42
  python3 skill_scores.py alert-trial trial.csv --min-precision 0.9 --max-alarms 200
  python3 skill_scores.py admit dossier.json
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


def ss_rmse(rmse_model, rmse_naive):
    """Benchmark skill score SS_RMSE = 1 - RMSE_model / RMSE_naive (v2.3).

    Returns None when the naive baseline has zero error (the ratio is
    undefined); callers treat that as "no verdict". Note this differs from
    the MSE-ratio skill score 1 - MSE_model / MSE_baseline kept alongside
    it: SS_RMSE > 0 and the MSE-ratio skill > 0 mark the same boundary (the
    model beats the baseline), but their values differ.
    """
    if rmse_naive is None or rmse_naive <= 0:
        return None
    return 1 - rmse_model / rmse_naive


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
    # SS_RMSE (v2.3): 1 - RMSE_model / RMSE_naive. Kept alongside the
    # MSE-ratio skill scores above; same > 0 boundary, different value.
    m["ss_rmse"] = ss_rmse(m["rmse"], math.sqrt(mse_pers))
    m["ss_rmse_vs_climatology"] = ss_rmse(m["rmse"], math.sqrt(mse_clim))
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
    # Admission verdict (v2.3): ADMITTED if and only if SS_RMSE > 0 on the
    # declared hold-out, against the persistence (inertial) baseline. The
    # gate above additionally requires beating climatology; a model can
    # therefore be ADMITTED by this verdict yet fail the gate. No verdict
    # exists without out-of-sample data.
    if a.no_holdout:
        verdict = None
        warnings.append("no admission verdict: in-sample fit is not out-of-sample validation")
    elif m["ss_rmse"] is None:
        verdict = None
        warnings.append("no admission verdict: the naive baseline has zero error")
    else:
        verdict = "ADMITTED" if m["ss_rmse"] > 0 else "REJECTED_BELOW_BENCHMARK"
    unpaired = sum(1 for _, o, s in test if o is None or s is None)
    if unpaired:
        warnings.append(f"{unpaired} hold-out rows lack a valid observation or simulation and were not scored")
    if bad_time:
        warnings.append(f"{bad_time} rows have no valid timestamp and were ignored")
    out = {
        "mode": "continuous", "label": "in-sample fit, not forecast skill" if a.no_holdout else "hold-out skill",
        "train_end": a.train_end, "n_train_obs": len(train_obs), "metrics": m,
        "ss_rmse": m["ss_rmse"], "admission_verdict": verdict,
        "baselines": baseline_checks, "thresholds": thresholds,
        "gate": "fail" if failed else ("pass" if thresholds else "pass (baselines only; no thresholds declared)"),
        "warnings": warnings,
    }
    return out, bool(failed)


def cmd_revalidate(a):
    """Continuous revalidation (Round 2 of the v2.5 program).

    Re-scores the admitted model on a new batch: the input is the
    combined series (calibration + new batch) with the ORIGINAL
    --train-end split, so the new batch is the hold-out and the naive
    baselines are built from training data only. The scoring itself is
    cmd_continuous, reused whole — this wrapper only adds the status
    transition. SS_RMSE <= 0 revokes ADMITTED: the model loses its
    forecasting status and the twin's maturity label drops to the
    highest level the twin still meets, until a better model is
    admitted. A re-score without a hold-out is refused by design:
    there is no --no-holdout here.
    """
    if a.train_end is None:
        raise ValueError("--train-end is required for revalidation: the original calibration split")
    ns = argparse.Namespace(input=a.input, time_col=a.time_col, obs_col=a.obs_col,
                            sim_col=a.sim_col, train_end=a.train_end, no_holdout=False,
                            season=a.season, persistence=a.persistence, thresholds=a.thresholds)
    out, failed = cmd_continuous(ns)
    new_verdict = out.get("admission_verdict")
    new_ss = out.get("ss_rmse")
    prev = a.previous_verdict
    if new_verdict == "ADMITTED":
        status = "ADMITTED"
    elif new_verdict == "REJECTED_BELOW_BENCHMARK":
        status = "NOT_ADMITTED"
    else:
        status = None
    revoked = (prev == "ADMITTED" and status == "NOT_ADMITTED")
    transition = f"{prev} -> {status}" if prev and status else None
    maturity_action = "drop" if revoked else "keep"
    if revoked:
        maturity_note = ("lower the maturity label to the highest level the twin still meets "
                         "(forecasting levels require an ADMITTED model); record the drop in the "
                         "Object Passport; re-admit only after a better model passes revalidation")
    elif status == "NOT_ADMITTED":
        maturity_note = "model was not previously admitted: nothing to revoke"
    else:
        maturity_note = "no change"
    warnings = list(out.get("warnings", []))
    if prev is None:
        warnings.append("no previous verdict supplied: transition not stated; "
                        "pass --previous-verdict to record it")
    if a.previous_ss_rmse is not None and new_ss is not None:
        warnings.append(f"SS_RMSE moved {a.previous_ss_rmse} -> {new_ss} on the new hold-out")
    out["mode"] = "revalidate"
    out["revalidation"] = {
        "previous_verdict": prev, "previous_ss_rmse": a.previous_ss_rmse,
        "new_ss_rmse": new_ss, "new_verdict": new_verdict,
        "status": status, "transition": transition, "revoked": revoked,
        "maturity_action": maturity_action, "maturity_note": maturity_note,
    }
    out["warnings"] = warnings
    return out, bool(revoked or failed)


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


def cmd_admit(a):
    """Calibration plausibility gate (Round 1 of the v2.7 program, lake
    platforms). A fit can be good and still be wrong: admission requires
    (a) the model beats the naive benchmark on every PRIMARY target
    variable declared in the Object Passport (SS_RMSE > 0 for each), and
    (b) every fitted parameter inside its declared physical bounds
    (references/calibration-bounds.md). Secondary background variables
    (a buffered pH, a flat background index) are reported, not gated:
    a model is not blocked by one flat curve it was never built to
    predict. Each variable may carry a "primary" flag (true/false); when
    no variable in the dossier carries the flag at all, every variable
    is primary — the pre-2.7 behaviour, kept for backward
    compatibility. A parameter outside its bounds is REJECTED even when
    SS_RMSE > 0, and the verdict names the offending parameter or
    PRIMARY variable. Input is a JSON dossier: {"variables": [{"name",
    "ss_rmse", "primary": true}], "parameters": [{"name", "value",
    "bounds": [lo, hi], "source"}]}. This is one of two admission
    gates; the alert trial (alert-trial) is the other, on alert quality —
    both must pass."""
    with open(a.dossier, encoding="utf-8") as fh:
        data = json.load(fh)
    variables = data.get("variables")
    parameters = data.get("parameters")
    if not isinstance(variables, list) or not variables:
        raise ValueError("the dossier needs a non-empty 'variables' list")
    if not isinstance(parameters, list):
        raise ValueError("the dossier needs a 'parameters' list (possibly empty)")
    any_primary_flag = any(isinstance(v, dict) and "primary" in v for v in variables)
    failures = []
    echoed = []
    for v in variables:
        try:
            ss = float(v["ss_rmse"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"variable {v!r} needs a numeric 'ss_rmse'")
        # A variable is primary when its flag says so; with no flag on any
        # variable, every variable is primary (the pre-2.7 behaviour).
        primary = v.get("primary") in (True, 1) if any_primary_flag else True
        echoed.append({"name": v.get("name", "?"), "ss_rmse": ss, "primary": primary})
        if primary and not (ss > 0):
            failures.append(f"variable {v.get('name', '?')}: SS_RMSE {ss} does not beat "
                            "the naive benchmark (> 0)")
    for p in parameters:
        try:
            value = float(p["value"])
            lo, hi = float(p["bounds"][0]), float(p["bounds"][1])
        except (KeyError, TypeError, ValueError, IndexError):
            raise ValueError(f"parameter {p!r} needs a numeric 'value' and 'bounds' [lo, hi]")
        if lo > hi:
            raise ValueError(f"parameter {p.get('name', '?')}: bounds [{lo}, {hi}] are inverted")
        if not (lo <= value <= hi):
            failures.append(f"parameter {p.get('name', '?')}: {value} outside declared bounds "
                            f"[{lo}, {hi}] (source: {p.get('source', 'not stated')})")
    out = {"mode": "admit", "dossier": a.dossier,
           "variables": echoed,
           "parameters": [{"name": p.get("name", "?"), "value": float(p["value"]),
                           "bounds": [float(p["bounds"][0]), float(p["bounds"][1])],
                           "source": p.get("source")} for p in parameters],
           "verdict": "REJECTED" if failures else "ADMITTED", "failures": failures,
           "rule": "every PRIMARY target variable beats the naive benchmark (SS_RMSE > 0) "
                   "AND every fitted parameter inside its declared bounds; secondary "
                   "variables are reported, not gated; when no variable carries a "
                   "'primary' flag, every variable is primary; both admission gates "
                   "(this and the alert trial) must pass"}
    return out, bool(failures)


def skill_horizon_by_lead(pairs_by_lead):
    """Skill vs lead time (Round 3 of the v2.7 program, lake platforms).

    pairs_by_lead maps a lead value to a list of (obs, sim, naive) triples.
    Per lead: SS_RMSE = 1 - RMSE_model / RMSE_naive. The skill horizon is
    the longest lead at which the forecast still beats persistence
    (SS_RMSE > 0) with every shorter lead also above zero: walk from the
    shortest lead and stop at the first lead that does not beat the
    baseline. A longer lead that beats the baseline after a failure is a
    non-monotone recovery — noise, not skill — and is reported as a
    warning, not as horizon. Returns (per_lead, horizon, warnings)."""
    per_lead, warnings = [], []
    for lead in sorted(pairs_by_lead):
        pairs = pairs_by_lead[lead]
        rmse_m = math.sqrt(mean([(s - o) ** 2 for o, s, _ in pairs]))
        rmse_n = math.sqrt(mean([(b - o) ** 2 for o, _, b in pairs]))
        ss = ss_rmse(rmse_m, rmse_n)
        rec = {"lead": lead, "n": len(pairs), "rmse_model": rmse_m,
               "rmse_naive": rmse_n, "ss_rmse": ss,
               "beats_persistence": ss is not None and ss > 0}
        if len(pairs) < 3:
            warnings.append(f"lead {lead}: only {len(pairs)} pairs — SS_RMSE is fragile, report it with this count")
        if ss is None:
            warnings.append(f"lead {lead}: the naive baseline has zero error — no SS_RMSE")
        per_lead.append(rec)
    horizon = None
    for rec in per_lead:
        if rec["beats_persistence"]:
            horizon = rec["lead"]
        else:
            break
    if horizon is not None:
        recovered = [r["lead"] for r in per_lead if r["lead"] > horizon and r["beats_persistence"]]
        if recovered:
            warnings.append(f"non-monotone recovery at lead(s) {recovered}: skill returns after dying — "
                            "the horizon stops at the first failure, the recovery is not trusted")
    return per_lead, horizon, warnings


def cmd_skill_horizon(a):
    """Skill-vs-lead-time curve (Round 3 of the v2.7 program, lake
    platforms). Input CSV, one row per scored forecast pair: lead, obs,
    sim, naive — the naive column is the persistence (or climatology)
    baseline value for that pair, supplied by the caller from the same
    hold-out. The twin's report states the skill horizon: the longest
    lead where the forecast still beats persistence. A forecast is not
    trusted beyond its horizon. Exit 0 (a report, not a gate); 2 on
    input error."""
    rows = read_csv(a.input, [a.lead_col, a.obs_col, a.sim_col, a.naive_col])
    pairs_by_lead, skipped = {}, 0
    for r in rows:
        lead, o, s, b = (fnum(r[a.lead_col]), fnum(r[a.obs_col]),
                         fnum(r[a.sim_col]), fnum(r[a.naive_col]))
        if lead is None or o is None or s is None or b is None:
            skipped += 1
            continue
        pairs_by_lead.setdefault(lead, []).append((o, s, b))
    if not pairs_by_lead:
        raise ValueError("no rows with a numeric lead, observation, simulation and naive value")
    per_lead, horizon, warnings = skill_horizon_by_lead(pairs_by_lead)
    if skipped:
        warnings.append(f"{skipped} row(s) lack a valid lead, observation, simulation or naive value and were skipped")
    out = {"mode": "skill_horizon", "input": a.input, "lead_unit": a.lead_unit,
           "per_lead": per_lead, "skill_horizon": horizon,
           "skill_horizon_unit": a.lead_unit if horizon is not None else None,
           "rule": "the skill horizon is the longest lead with SS_RMSE > 0 and every shorter lead "
                   "also above zero; a forecast is not trusted beyond its horizon",
           "warnings": warnings}
    return out, False


def cmd_nudge(a):
    """Observation-nudged forecast (Round 3 of the v2.7 program, lake
    platforms). A deterministic bias correction, not a filter: shift a
    raw forecast value by the mean model-minus-observed residual over
    the last N QC-passed observation/model pairs (N declared in the
    Object Passport, default 5). residual = sim - obs; nudged =
    raw forecast - mean residual. The correction is recorded in the
    registry entry so it can be checked, and the nudged forecast is
    scored per lead time by skill_horizon like any forecast. Exit 0;
    2 on input error."""
    if a.n < 1:
        raise ValueError("--n must be at least 1")
    rows = read_csv(a.input, [a.time_col, a.obs_col, a.sim_col])
    recs, bad = [], 0
    for r in rows:
        t, o, s = ftime(r[a.time_col]), fnum(r[a.obs_col]), fnum(r[a.sim_col])
        if t is not None and o is not None and s is not None:
            recs.append((t, o, s))
        else:
            bad += 1
    recs.sort(key=lambda x: x[0])
    if len(recs) < 2:
        raise ValueError(f"only {len(recs)} usable observation/model pair(s); need at least 2")
    used = recs[-a.n:]
    residuals = [s - o for _, o, s in used]
    mean_residual = mean(residuals)
    warnings = []
    if len(used) < a.n:
        warnings.append(f"only {len(used)} of the declared {a.n} pairs available — the correction uses what exists")
    if bad:
        warnings.append(f"{bad} row(s) lack a valid time, observation or simulation and were skipped")
    out = {"mode": "nudge", "input": a.input, "n_declared": a.n, "n_used": len(used),
           "mean_residual": mean_residual, "raw_forecast": a.forecast,
           "nudged_forecast": a.forecast - mean_residual,
           "correction": -mean_residual,
           "rule": "nudged = raw forecast - mean(sim - obs) over the last N QC-passed pairs; "
                   "record the correction in the registry entry; score the nudged forecast per "
                   "lead time by skill_horizon like any forecast",
           "warnings": warnings}
    return out, False


def cmd_alert_trial(a):
    """Score the alerts on a hold-out window (Round 1 of the v2.7 program,
    Southern Water). This scores the ALERTS, not the model: a model can
    beat its benchmark (SS_RMSE > 0) and still cry wolf, or stay silent
    when it matters. Input CSV, one row per alert or critical event in the
    hold-out window: kind ("alert" | "critical_event"), relevant (1/0).
    For an alert, relevant 1 means a real event followed within the lead
    window; 0 is a false positive. For a critical event, relevant 1 means
    it was alerted in time; 0 means it was missed. Verdict PASS requires
    precision >= --min-precision (default 0.9), zero missed criticals
    (default --max-missed-criticals 0), and the alarm count within
    --max-alarms when given. A window with no alerts and no critical
    events is INCONCLUSIVE_QUIET_WINDOW (exit 0): nothing to score, so
    it neither admits nor rejects — admission waits for a synthetic
    stress-test or a historical extreme replay. Critical events with no
    alerts still FAIL: the model stayed silent when it mattered."""
    rows = read_csv(a.input, ["kind", "relevant"])
    if not rows:
        # A quiet window: no alerts and no critical events — nothing to
        # score. This is a report, not a failure (exit 0).
        return {"mode": "alert-trial", "input": a.input, "n_alerts": 0,
                "n_relevant": 0, "precision": None,
                "n_critical_events": 0, "n_missed_criticals": 0,
                "miss_rate": None, "alarm_volume": 0,
                "thresholds": {"min_precision": a.min_precision,
                               "max_missed_criticals": a.max_missed_criticals,
                               "max_alarms": a.max_alarms},
                "verdict": "INCONCLUSIVE_QUIET_WINDOW", "failures": [],
                "note": "no alerts and no critical events in the window: nothing to "
                        "score. This neither admits nor rejects; admission waits for a "
                        "synthetic stress-test or a historical extreme replay.",
                "rule": "precision >= minimum, zero missed criticals, alarm volume within "
                        "cap; a window with no alerts and no critical events is "
                        "INCONCLUSIVE_QUIET_WINDOW"}, False
    n_alerts = n_relevant = n_critical = n_missed = 0
    for r in rows:
        kind = (r.get("kind") or "").strip().lower()
        if kind not in ("alert", "critical_event"):
            raise ValueError(f"kind must be 'alert' or 'critical_event', got {r.get('kind')!r}")
        rel = fbool(r.get("relevant"))
        if rel is None:
            raise ValueError(f"relevant must be 0/1 (or true/false), got {r.get('relevant')!r}")
        if kind == "alert":
            n_alerts += 1
            n_relevant += rel
        else:
            n_critical += 1
            n_missed += 1 - rel
    precision = n_relevant / n_alerts if n_alerts else None
    miss_rate = n_missed / n_critical if n_critical else None
    failures = []
    if precision is None:
        failures.append("no alerts in the window: precision is undefined")
    elif precision < a.min_precision:
        failures.append(f"precision {precision:.3f} below the minimum {a.min_precision}")
    if n_missed > a.max_missed_criticals:
        failures.append(f"{n_missed} missed critical event(s), maximum {a.max_missed_criticals}")
    if a.max_alarms is not None and n_alerts > a.max_alarms:
        failures.append(f"alarm volume {n_alerts} above the cap {a.max_alarms}")
    out = {"mode": "alert-trial", "input": a.input, "n_alerts": n_alerts,
           "n_relevant": n_relevant, "precision": precision,
           "n_critical_events": n_critical, "n_missed_criticals": n_missed,
           "miss_rate": miss_rate, "alarm_volume": n_alerts,
           "thresholds": {"min_precision": a.min_precision,
                          "max_missed_criticals": a.max_missed_criticals,
                          "max_alarms": a.max_alarms},
           "verdict": "FAIL" if failures else "PASS", "failures": failures,
           "rule": "precision >= minimum, zero missed criticals, alarm volume within cap; "
                   "a window with no alerts and no critical events is INCONCLUSIVE_QUIET_WINDOW — "
                   "it neither admits nor rejects"}
    return out, bool(failures)


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
    r = sub.add_parser("revalidate", help="re-score an admitted model on a new batch")
    r.add_argument("input", help="combined series: calibration + new batch")
    r.add_argument("--time-col", default="time")
    r.add_argument("--obs-col", default="obs")
    r.add_argument("--sim-col", default="sim")
    r.add_argument("--train-end", required=True, help="original calibration split (ISO date)")
    r.add_argument("--season", choices=["month", "doy", "none"], default="month")
    r.add_argument("--persistence", choices=["rolling", "fixed"], default="rolling")
    r.add_argument("--thresholds", help='declared pass rules, e.g. "NSE>=0.5,abs_pbias<=25"')
    r.add_argument("--previous-verdict", choices=["ADMITTED", "REJECTED_BELOW_BENCHMARK"],
                   help="admission verdict from the previous validation round")
    r.add_argument("--previous-ss-rmse", type=float, help="SS_RMSE from the previous validation round")
    t = sub.add_parser("alert-trial", help="score the alerts on a hold-out window")
    t.add_argument("input", help="one row per alert or critical event: kind, relevant")
    t.add_argument("--min-precision", type=float, default=0.9)
    t.add_argument("--max-missed-criticals", type=int, default=0)
    t.add_argument("--max-alarms", type=int, help="optional cap on the alarm count")
    d = sub.add_parser("admit", help="calibration plausibility gate: SS_RMSE > 0 on every primary target variable "
                                     "and all parameters inside declared bounds")
    d.add_argument("dossier", help="JSON dossier: {variables: [{name, ss_rmse, primary (optional)}], "
                                   "parameters: [{name, value, bounds: [lo, hi], source}]}")
    h = sub.add_parser("skill-horizon", help="skill vs lead time: per-lead SS_RMSE and the skill horizon")
    h.add_argument("input", help="one row per scored forecast pair: lead, obs, sim, naive")
    h.add_argument("--lead-col", default="lead")
    h.add_argument("--obs-col", default="obs")
    h.add_argument("--sim-col", default="sim")
    h.add_argument("--naive-col", default="naive")
    h.add_argument("--lead-unit", default="days", help="unit of the lead values (e.g. hours, days)")
    n = sub.add_parser("nudge", help="observation-nudged forecast: shift a raw forecast by the mean recent residual")
    n.add_argument("input", help="recent QC-passed observation/model pairs: time, obs, sim")
    n.add_argument("--forecast", type=float, required=True, help="the raw forecast value to correct")
    n.add_argument("--n", type=int, default=5, help="number of last pairs for the mean residual (declared in the passport)")
    n.add_argument("--time-col", default="time")
    n.add_argument("--obs-col", default="obs")
    n.add_argument("--sim-col", default="sim")
    a = ap.parse_args(argv)
    try:
        out, failed = {"continuous": cmd_continuous, "events": cmd_events, "brier": cmd_brier,
                       "revalidate": cmd_revalidate, "alert-trial": cmd_alert_trial,
                       "admit": cmd_admit, "skill-horizon": cmd_skill_horizon,
                       "nudge": cmd_nudge}[a.cmd](a)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
