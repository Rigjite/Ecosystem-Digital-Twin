#!/usr/bin/env python3
"""
Trend tests for the pattern memo (ecosystem-digital-twin skill).

Mann-Kendall test with Sen's slope, run separately on every segment between
registered breaks (method changes, moved stations, revised detection limits
from the bias and breaks register). A single trend across a registered break
is never reported as the result.

  --seasonal month   seasonal Kendall test (Hirsch, Slack & Smith 1982) for
                     monthly or irregular water-quality data: S and its
                     variance summed over months, slope = median of
                     within-month slopes. Covariance between seasons is not
                     corrected (Hirsch & Slack 1984); this is stated in output.
  --autocorr hamed-rao (default)  variance correction for serial correlation
                     (Hamed & Rao 1998, J. Hydrol. 204: 182-196): the
                     series is detrended by Sen's slope, the autocorrelation
                     of its ranks is computed, and only significant lags
                     inflate (or deflate) var(S). The slope is unchanged;
                     the p-value and the slope interval widen honestly.
  --autocorr tfpw    trend-free pre-whitening (Yue et al. 2002). For strongly
                     autocorrelated series it can make a trend look more
                     significant than the uncorrected test does (seen on
                     Lake Huron levels, lag-1 r = 0.76); kept for
                     comparison, not as the default.
  --autocorr none    no correction; a significant lag-1 autocorrelation is
                     then reported as a warning (the p-value is optimistic).
  Corrections need near-regular sampling; otherwise the result is stated
  as uncorrected.
Slopes are per year; time is converted to decimal years, so irregular
sampling is handled by Sen's slope. Confidence interval of the slope follows
Gilbert (1987). Fewer than --min-n values in a segment: no test, stated.

Usage:
  python3 trend_test.py chl.csv --value-col chl --breaks 2009-01-01
  python3 trend_test.py tp.csv --value-col tp --seasonal month --breaks-file bias_register.csv

JSON input (trend mode): a .json file {"values": [float], "timestamps":
[ISO date or decimal year], "alpha": 0.05} prints one result with the
spec keys s_stat, var_s_raw, hamed_rao_factor, z_corrected, p_value,
theil_sen_slope, trend ("increasing" | "decreasing" | "no trend").

Index modes (--mode wpi | tsi | hpi | hq) take a JSON file and compute the
water-quality indices of the skill's Core Mathematical Specifications:
  wpi  {"indicators": [{"name": str, "concentration": float, "mac": float,
       "dissolved_oxygen": bool}]} — WPI = mean(C/MAC); for dissolved
       oxygen the ratio is MAC/C when C < MAC, and 1.0 at or above the
       standard. Classes follow the standard Russian ИЗВ scale.
  tsi  {"sd_m": float, "chl_ug_l": float, "tp_ug_l": float} (any subset) —
       Carlson (1977) TSI per component; composite is the mean of the
       available components.
  hpi  {"metals": [{"name": str, "measured": float, "standard": float,
       "ideal": float}]} — HPI = sum(W*Q)/sum(W), W = 1/S,
       Q = 100*|M - I|/(S - I); critical when HPI > 100.
  hq   {"stressors": [{"name": str, "exposure": float, "reference": float,
       "duration": "acute" | "chronic", "target": str}]} — HQ = exposure /
       reference per stressor; HI = sum of HQs, split acute/chronic;
       unsafe when HI > 1 (the safety line). Same quotient family as HPI,
       but HPI covers only metals in water on a 100-scale; HQ/HI covers
       any stressor on a 1-scale.

Drift mode (--mode drift) checks a new batch against its calibration
baseline for the recalibration trigger: --baseline CAL.csv gives the
calibration series; the input file is the new batch (QC-passed; rows
with qc_flag != "ok" are excluded when the column exists). Level drift
is |mean(new) - mean(calibration)| / sd(calibration), firing at
--drift-threshold (default 2.0, declared per indicator in the Object
Passport); trend drift fires when the new batch's Sen slope falls
outside the calibration slope's Gilbert confidence interval (needs
--min-n new values, default 8). Output JSON carries `trigger` and
`action` ("recalibrate" | "no action"); exit 0 is a report, 2 an input
error. A fired trigger is a normal event, not a failure.

Output: JSON with one result per segment. Exit 0 on success, 2 input error.
"""

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from statistics import NormalDist

MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}
ND = NormalDist()


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


def ftime(text):
    if text is None or not text.strip():
        return None
    try:
        t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def decimal_year(t):
    start = datetime(t.year, 1, 1, tzinfo=t.tzinfo)
    end = datetime(t.year + 1, 1, 1, tzinfo=t.tzinfo)
    return t.year + (t - start).total_seconds() / (end - start).total_seconds()


def sign(x):
    return (x > 0) - (x < 0)


def mk_s_var(values):
    n = len(values)
    s = 0
    for i in range(n - 1):
        vi = values[i]
        for j in range(i + 1, n):
            s += sign(values[j] - vi)
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    ties = sum(t * (t - 1) * (2 * t + 5) for t in counts.values() if t > 1)
    var = (n * (n - 1) * (2 * n + 5) - ties) / 18.0
    return s, var


def z_from(s, var):
    if var <= 0:
        return 0.0
    if s > 0:
        return (s - 1) / math.sqrt(var)
    if s < 0:
        return (s + 1) / math.sqrt(var)
    return 0.0


def pair_slopes(times, values):
    out = []
    for i in range(len(values) - 1):
        for j in range(i + 1, len(values)):
            dt = times[j] - times[i]
            if dt > 0:
                out.append((values[j] - values[i]) / dt)
    return out


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def sen_ci(slopes, var, alpha):
    """Gilbert (1987) confidence interval from order statistics of the slopes."""
    n = len(slopes)
    if n == 0 or var <= 0:
        return None, None
    s = sorted(slopes)
    c = ND.inv_cdf(1 - alpha / 2) * math.sqrt(var)
    m1 = (n - c) / 2.0
    m2 = (n + c) / 2.0 + 1
    lo = int(round(m1)) - 1
    hi = int(round(m2)) - 1
    if lo < 0 or hi >= n:
        return None, None
    return s[lo], s[hi]


def average_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def hamed_rao_factor(detrended, alpha):
    """n/n* of Hamed & Rao (1998) from significant rank autocorrelations."""
    n = len(detrended)
    r = average_ranks(detrended)
    m = sum(r) / n
    den = sum((x - m) ** 2 for x in r)
    if n < 4 or den == 0:
        return 1.0, []
    bound = ND.inv_cdf(1 - alpha / 2) / math.sqrt(n)
    acc, lags = 0.0, []
    for k in range(1, n - 2):
        rho = sum((r[i] - m) * (r[i + k] - m) for i in range(n - k)) / den
        if abs(rho) > bound:
            acc += (n - k) * (n - k - 1) * (n - k - 2) * rho
            lags.append(k)
    return 1.0 + 2.0 * acc / (n * (n - 1) * (n - 2)), lags


def lag1(xs):
    n = len(xs)
    if n < 3:
        return None
    m = sum(xs) / n
    den = sum((x - m) ** 2 for x in xs)
    if den == 0:
        return None
    return sum((xs[i] - m) * (xs[i + 1] - m) for i in range(n - 1)) / den


# --- Water-quality indices (skill v2.3, Core Mathematical Specifications) ---

def wpi_class(wpi):
    """Standard Russian ИЗВ (water pollution index) classes."""
    if wpi < 0.3:
        return "very clean (I)"
    if wpi < 1.0:
        return "clean (II)"
    if wpi < 2.5:
        return "moderately polluted (III)"
    if wpi < 4.0:
        return "polluted (IV)"
    if wpi < 6.0:
        return "dirty (V)"
    if wpi < 10.0:
        return "very dirty (VI)"
    return "extremely dirty (VII)"


def water_pollution_index(indicators):
    """WPI = mean(C_i / MAC_i) over the given indicators.

    Each indicator is {"name", "concentration", "mac", "dissolved_oxygen"}.
    For dissolved oxygen the ratio is MAC/C when C < MAC (higher oxygen is
    better); at or above the standard the term is 1.0 — no pollution
    contribution. MAC must be > 0, concentrations >= 0.
    """
    if not indicators:
        raise ValueError("WPI needs at least one indicator")
    terms = []
    for ind in indicators:
        try:
            c = float(ind["concentration"])
            mac = float(ind["mac"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"indicator {ind!r} needs numeric 'concentration' and 'mac'")
        if mac <= 0:
            raise ValueError(f"indicator {ind.get('name', '?')}: MAC must be > 0")
        if c < 0:
            raise ValueError(f"indicator {ind.get('name', '?')}: concentration must be >= 0")
        if ind.get("dissolved_oxygen"):
            ratio = mac / c if 0 < c < mac else 1.0
        else:
            ratio = c / mac
        terms.append({"name": ind.get("name", "?"), "ratio": ratio,
                      "dissolved_oxygen": bool(ind.get("dissolved_oxygen", False))})
    wpi = sum(t["ratio"] for t in terms) / len(terms)
    return {"wpi": wpi, "n": len(terms), "class": wpi_class(wpi), "terms": terms}


def tsi_class(tsi):
    """Carlson trophic bands: <40 oligotrophic, 40–50 mesotrophic,
    50–70 eutrophic, >70 hypereutrophic (boundary values take the higher band)."""
    if tsi < 40:
        return "oligotrophic"
    if tsi < 50:
        return "mesotrophic"
    if tsi < 70:
        return "eutrophic"
    return "hypereutrophic"


def carlson_tsi(sd_m=None, chl_ug_l=None, tp_ug_l=None):
    """Carlson (1977) trophic state index per component; composite is the
    arithmetic mean of the available components. Each input must be > 0
    (logarithms); at least one component is required."""
    comps = {}
    if sd_m is not None:
        if sd_m <= 0:
            raise ValueError("Secchi depth must be > 0")
        comps["tsi_sd"] = 60 - 14.41 * math.log(sd_m)
    if chl_ug_l is not None:
        if chl_ug_l <= 0:
            raise ValueError("chlorophyll-a must be > 0")
        comps["tsi_chl"] = 9.81 * math.log(chl_ug_l) + 30.6
    if tp_ug_l is not None:
        if tp_ug_l <= 0:
            raise ValueError("total phosphorus must be > 0")
        comps["tsi_tp"] = 14.42 * math.log(tp_ug_l) + 4.15
    if not comps:
        raise ValueError("TSI needs at least one of sd_m, chl_ug_l, tp_ug_l")
    vals = list(comps.values())
    comp = sum(vals) / len(vals)
    out = {"tsi_sd": comps.get("tsi_sd"), "tsi_chl": comps.get("tsi_chl"),
           "tsi_tp": comps.get("tsi_tp"), "tsi_composite": comp,
           "class": tsi_class(comp)}
    return out


def heavy_metal_pollution_index(metals):
    """HPI = sum(W_i * Q_i) / sum(W_i), W_i = 1/S_i,
    Q_i = 100 * |M_i - I_i| / (S_i - I_i). 'ideal' defaults to 0 (strictly
    toxic). Standards must be > 0 and differ from the ideal value;
    measured concentrations must be >= 0. Critical when HPI > 100."""
    if not metals:
        raise ValueError("HPI needs at least one metal")
    terms, num, den = [], 0.0, 0.0
    for met in metals:
        try:
            m = float(met["measured"])
            s = float(met["standard"])
            ideal = float(met.get("ideal", 0.0))
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"metal {met!r} needs numeric 'measured', 'standard' and 'ideal'")
        if s <= 0:
            raise ValueError(f"metal {met.get('name', '?')}: standard must be > 0")
        if s == ideal:
            raise ValueError(f"metal {met.get('name', '?')}: standard must differ from the ideal value")
        if m < 0:
            raise ValueError(f"metal {met.get('name', '?')}: measured concentration must be >= 0")
        w = 1.0 / s
        q = 100.0 * abs(m - ideal) / (s - ideal)
        terms.append({"name": met.get("name", "?"), "w": w, "q": q})
        num += w * q
        den += w
    hpi = num / den
    return {"hpi": hpi, "critical": hpi > 100, "threshold": 100, "terms": terms}


def hazard_quotient_index(stressors):
    """HQ = exposure / reference per stressor; HI = sum of HQs, split by
    duration (acute / chronic). The safety line is 1: HI above 1 is
    unsafe. Same quotient family as HPI, but HPI covers only metals in
    water on a 100-scale; HQ/HI covers any stressor (air, water, smoke,
    chemicals) on a 1-scale, with the acute/chronic split. References
    must be > 0, exposures >= 0; duration defaults to "chronic" when not
    stated. Each term records its target (e.g. respiratory) where known;
    the published HI is often reported per target organ — this function
    sums by duration and keeps the target on the term, so a per-target
    HI is read off the terms."""
    if not stressors:
        raise ValueError("HQ/HI needs at least one stressor")
    terms, hi_acute, hi_chronic = [], 0.0, 0.0
    for st in stressors:
        try:
            e = float(st["exposure"])
            ref = float(st["reference"])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"stressor {st!r} needs numeric 'exposure' and 'reference'")
        if ref <= 0:
            raise ValueError(f"stressor {st.get('name', '?')}: reference must be > 0")
        if e < 0:
            raise ValueError(f"stressor {st.get('name', '?')}: exposure must be >= 0")
        duration = str(st.get("duration", "chronic")).lower()
        if duration not in ("acute", "chronic"):
            raise ValueError(f"stressor {st.get('name', '?')}: duration must be 'acute' or 'chronic'")
        hq = e / ref
        terms.append({"name": st.get("name", "?"), "hq": hq, "duration": duration,
                      "target": st.get("target")})
        if duration == "acute":
            hi_acute += hq
        else:
            hi_chronic += hq
    hi = hi_acute + hi_chronic
    return {"hi": hi, "hi_acute": hi_acute, "hi_chronic": hi_chronic,
            "unsafe": hi > 1, "unsafe_acute": hi_acute > 1,
            "unsafe_chronic": hi_chronic > 1, "threshold": 1, "terms": terms}


def regular(times):
    steps = [b - a for a, b in zip(times, times[1:])]
    if len(steps) < 2:
        return False
    m = sum(steps) / len(steps)
    if m <= 0:
        return False
    sd = math.sqrt(sum((s - m) ** 2 for s in steps) / len(steps))
    return sd / m <= 0.5


def test_segment(times, values, alpha, autocorr, seasonal, months):
    n = len(values)
    n_tested = n
    res = {"n": n, "warnings": []}
    if seasonal:
        S = V = 0.0
        slopes = []
        used = 0
        for mth in sorted(set(months)):
            idx = [i for i in range(n) if months[i] == mth]
            if len(idx) < 2:
                continue
            used += 1
            s_k, v_k = mk_s_var([values[i] for i in idx])
            S += s_k
            V += v_k
            slopes += pair_slopes([times[i] for i in idx], [values[i] for i in idx])
        res["test"] = "seasonal Kendall (by month)"
        res["seasons_used"] = used
        res["warnings"].append("covariance between seasons not corrected (Hirsch & Slack 1984); "
                               "serial correlation within seasons assumed negligible")
        s_val, var = S, V
        res["var_s_raw"] = var
    else:
        s_val, var = mk_s_var(values)
        res["var_s_raw"] = var
        slopes = pair_slopes(times, values)
        res["test"] = "Mann-Kendall"
        slope0 = median(slopes) if slopes else 0.0
        detr = [v - slope0 * t for t, v in zip(times, values)]
        r1 = lag1(detr)
        res["lag1_autocorrelation_detrended"] = r1
        bound = ND.inv_cdf(1 - alpha / 2) / math.sqrt(n)
        significant = r1 is not None and abs(r1) > bound
        res["serial_correction"] = "none"
        if autocorr != "none" and not regular(times):
            if significant:
                res["warnings"].append("serial correlation not corrected: sampling is irregular, "
                                       "the corrections need a near-regular series")
        elif autocorr == "hamed-rao":
            factor, lags = hamed_rao_factor(detr, alpha)
            if factor > 0:
                var = var * factor
                res["serial_correction"] = "variance correction (Hamed & Rao 1998)"
                res["variance_factor_n_over_n_eff"] = factor
                res["significant_rank_lags"] = len(lags)
            else:
                res["warnings"].append("Hamed-Rao factor not positive: correction skipped, p-value uncertain")
        elif autocorr == "tfpw" and r1 is not None:
            yp = [detr[i] - r1 * detr[i - 1] for i in range(1, n)]
            blended = [y + slope0 * t for y, t in zip(yp, times[1:])]
            s_val, var = mk_s_var(blended)
            n_tested = len(blended)
            res["serial_correction"] = "trend-free pre-whitening (Yue et al. 2002)"
            if significant:
                res["warnings"].append("TFPW on a strongly autocorrelated series can overstate significance; "
                                       "compare with --autocorr hamed-rao")
        elif significant:
            res["warnings"].append("significant lag-1 autocorrelation left uncorrected: p-value is optimistic")
    z = z_from(s_val, var)
    p = 2 * (1 - ND.cdf(abs(z)))
    slope = median(slopes) if slopes else None
    lo, hi = sen_ci(slopes, var, alpha)
    res.update({
        "S": s_val, "var_S": var, "Z": z, "p_value": p,
        "kendall_tau": (s_val / (n_tested * (n_tested - 1) / 2.0)) if (not seasonal and n_tested > 1) else None,
        "sen_slope_per_year": slope, "slope_ci": [lo, hi], "ci_level": 1 - alpha,
        "direction": ("increasing" if z > 0 else "decreasing") if p < alpha else "no significant trend",
    })
    return res


def load_breaks(arg_breaks, breaks_file, date_col):
    out = []
    if arg_breaks:
        for part in arg_breaks.split(","):
            t = ftime(part)
            if t is None:
                raise ValueError(f"break '{part}' is not an ISO date")
            out.append(t)
    if breaks_file:
        with open(breaks_file, newline="", encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh, delimiter=sniff_delimiter(breaks_file)):
                t = ftime(r.get(date_col))
                if t is not None:
                    out.append(t)
    return sorted(set(out))


def run_json_trend(data, alpha, autocorr, min_n):
    """Trend test from a JSON payload {"values": [...], "timestamps": [...]}.

    Timestamps are ISO dates or decimal years (numbers are used as decimal
    years directly). Returns the spec-keyed result dict.
    """
    values = data.get("values")
    stamps = data.get("timestamps")
    if not isinstance(values, list) or not values:
        raise ValueError("JSON trend input needs a non-empty 'values' list")
    if stamps is not None and len(stamps) != len(values):
        raise ValueError("'timestamps' must match 'values' in length")
    if data.get("alpha") is not None:
        alpha = float(data["alpha"])
    times, months = [], []
    for i, v in enumerate(values):
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"value {i} is not a finite number")
        stamp = stamps[i] if stamps is not None else i
        if isinstance(stamp, (int, float)):
            times.append(float(stamp))
            months.append(1)
        else:
            t = ftime(str(stamp))
            if t is None:
                raise ValueError(f"timestamp {stamp!r} is not an ISO date or a number")
            times.append(decimal_year(t))
            months.append(t.month)
    if len(values) < min_n:
        return {"mode": "trend", "n": len(values), "result": None,
                "warnings": [f"fewer than {min_n} values: no trend test"]}
    res = test_segment(times, values, alpha, autocorr, False, months)
    trend = {"increasing": "increasing", "decreasing": "decreasing"}.get(res["direction"], "no trend")
    return {
        "mode": "trend", "n": len(values), "alpha": alpha,
        "s_stat": res["S"], "var_s_raw": res["var_s_raw"],
        "hamed_rao_factor": res.get("variance_factor_n_over_n_eff", 1.0),
        "z_corrected": res["Z"], "p_value": res["p_value"],
        "theil_sen_slope": res["sen_slope_per_year"], "trend": trend,
        "serial_correction": res.get("serial_correction"),
        "warnings": res.get("warnings", []),
    }


def run_index_mode(mode, data):
    """WPI / TSI / HPI from a JSON payload; returns the spec-keyed result."""
    if mode == "wpi":
        if not isinstance(data.get("indicators"), list):
            raise ValueError("WPI mode needs an 'indicators' list")
        return {"mode": "wpi", **water_pollution_index(data["indicators"])}
    if mode == "tsi":
        return {"mode": "tsi", **carlson_tsi(data.get("sd_m"), data.get("chl_ug_l"), data.get("tp_ug_l"))}
    if mode == "hpi":
        if not isinstance(data.get("metals"), list):
            raise ValueError("HPI mode needs a 'metals' list")
        return {"mode": "hpi", **heavy_metal_pollution_index(data["metals"])}
    if mode == "hq":
        if not isinstance(data.get("stressors"), list):
            raise ValueError("HQ/HI mode needs a 'stressors' list")
        return {"mode": "hq", **hazard_quotient_index(data["stressors"])}
    raise ValueError(f"unknown mode '{mode}'")


def load_series(path, value_col, time_col):
    """Load one CSV series as (decimal-year times, values, qc-excluded rows, has-qc-column).

    Rows with a qc_flag column value other than "ok" (or empty) are
    excluded: only QC-passed observations count as data. Rows without a
    valid timestamp or value are dropped. Times are sorted.
    """
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        fields = reader.fieldnames or []
        if value_col not in fields:
            raise ValueError(f"column '{value_col}' not found in {path}")
        if time_col not in fields:
            raise ValueError(f"column '{time_col}' not found in {path}")
        has_qc = "qc_flag" in fields
        pairs, excluded = [], 0
        for r in reader:
            if has_qc and (r.get("qc_flag") or "").strip() not in ("ok", ""):
                excluded += 1
                continue
            t, v = ftime(r[time_col]), fnum(r.get(value_col))
            if t is not None and v is not None:
                pairs.append((decimal_year(t), v))
    pairs.sort(key=lambda x: x[0])
    return [p[0] for p in pairs], [p[1] for p in pairs], excluded, has_qc


def run_drift_mode(cal_path, new_path, threshold, min_n, value_col, time_col):
    """Recalibration trigger: drift of a new batch against its calibration baseline.

    Level drift is |mean(new) - mean(calibration)| / sd(calibration)
    (sample sd); it fires at the declared threshold. Trend drift fires
    when the new batch's Sen slope falls outside the calibration slope's
    Gilbert confidence interval (same test_segment machinery as the
    trend test; needs min_n new values). Either component fires the
    trigger. A fired trigger is a report (exit 0), not a failure: the
    runner recalibrates, recomputes alert bands, and revalidates.
    """
    cal_times, cal_values, cal_excl, cal_qc = load_series(cal_path, value_col, time_col)
    new_times, new_values, new_excl, new_qc = load_series(new_path, value_col, time_col)
    if len(cal_values) < 3:
        raise ValueError(f"calibration series has only {len(cal_values)} usable values; need at least 3")
    if len(new_values) < 3:
        raise ValueError(f"new batch has only {len(new_values)} usable values; need at least 3")
    warnings = []
    if not new_qc:
        warnings.append("new batch has no qc_flag column: QC was not applied; run qc_series.py --out first")
    if not cal_qc:
        warnings.append("calibration series has no qc_flag column")
    if cal_excl:
        warnings.append(f"{cal_excl} calibration rows excluded by qc_flag")
    if new_excl:
        warnings.append(f"{new_excl} new-batch rows excluded by qc_flag")
    mean_cal = sum(cal_values) / len(cal_values)
    sd_cal = math.sqrt(sum((v - mean_cal) ** 2 for v in cal_values) / (len(cal_values) - 1))
    mean_new = sum(new_values) / len(new_values)
    if sd_cal > 0:
        drift_level = abs(mean_new - mean_cal) / sd_cal
        level_fires = drift_level >= threshold
    else:
        drift_level = None
        level_fires = mean_new != mean_cal
        warnings.append("calibration series is constant (sd 0): level drift not measurable; "
                        "any mean shift fires the trigger")
    res_cal = test_segment(cal_times, cal_values, 0.05, "hamed-rao", False, [1] * len(cal_values))
    slope_cal = res_cal["sen_slope_per_year"]
    ci_cal = res_cal["slope_ci"]
    slope_new, trend_fires = None, None
    if len(new_values) >= min_n:
        res_new = test_segment(new_times, new_values, 0.05, "hamed-rao", False, [1] * len(new_values))
        slope_new = res_new["sen_slope_per_year"]
        if ci_cal[0] is not None and ci_cal[1] is not None:
            trend_fires = slope_new < ci_cal[0] or slope_new > ci_cal[1]
        else:
            warnings.append("calibration slope confidence interval unavailable: trend drift not assessed")
    else:
        warnings.append(f"new batch has {len(new_values)} values (< {min_n}): trend drift not assessed")
    trigger = bool(level_fires or trend_fires)
    return {
        "mode": "drift", "value_col": value_col, "threshold": threshold,
        "n_calibration": len(cal_values), "n_new": len(new_values),
        "rows_excluded_qc": new_excl, "calibration_rows_excluded_qc": cal_excl,
        "mean_calibration": mean_cal, "sd_calibration": sd_cal, "mean_new": mean_new,
        "drift_level": drift_level, "level_fires": level_fires,
        "slope_calibration": slope_cal, "slope_ci_calibration": ci_cal,
        "slope_new": slope_new, "trend_fires": trend_fires,
        "trigger": trigger,
        "action": "recalibrate" if trigger else "no action",
        "warnings": warnings,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--mode", choices=["trend", "wpi", "tsi", "hpi", "hq", "drift"], default="trend",
                    help="trend: Mann-Kendall test (default); wpi/tsi/hpi/hq: index from a JSON file; "
                         "drift: recalibration trigger, new batch vs --baseline calibration series")
    ap.add_argument("--time-col", default="time")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--breaks", help="comma list of ISO dates where a registered break starts a new segment")
    ap.add_argument("--breaks-file", help="CSV bias and breaks register")
    ap.add_argument("--breaks-date-col", default="date")
    ap.add_argument("--seasonal", choices=["none", "month"], default="none")
    ap.add_argument("--autocorr", choices=["hamed-rao", "tfpw", "none"], default="hamed-rao",
                    help="serial-correlation handling for the non-seasonal test")
    ap.add_argument("--prewhiten", choices=["auto", "tfpw", "none"], help=argparse.SUPPRESS)  # v2.0 alias
    ap.add_argument("--alpha", type=float, default=None)
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--baseline", help="calibration series CSV for --mode drift (the new batch is the input file)")
    ap.add_argument("--drift-threshold", type=float, default=2.0,
                    help="level-drift threshold in calibration SDs for --mode drift (default 2.0; "
                         "declare the per-indicator value in the Object Passport)")
    a = ap.parse_args(argv)
    alpha = a.alpha if a.alpha is not None else 0.05
    autocorr = {"auto": "hamed-rao", "tfpw": "tfpw", "none": "none"}.get(a.prewhiten, a.autocorr)
    try:
        if a.mode in ("wpi", "tsi", "hpi", "hq"):
            with open(a.input, encoding="utf-8") as fh:
                data = json.load(fh)
            out = run_index_mode(a.mode, data)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        if a.mode == "drift":
            if not a.baseline:
                raise ValueError("--mode drift needs --baseline <calibration series>")
            out = run_drift_mode(a.baseline, a.input, a.drift_threshold, a.min_n,
                                 a.value_col, a.time_col)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        if a.input.endswith(".json"):
            with open(a.input, encoding="utf-8") as fh:
                data = json.load(fh)
            out = run_json_trend(data, alpha, autocorr, a.min_n)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0
        with open(a.input, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.input))
            for col in (a.time_col, a.value_col):
                if col not in (reader.fieldnames or []):
                    raise ValueError(f"column '{col}' not found")
            recs, dropped = [], 0
            for r in reader:
                t, v = ftime(r[a.time_col]), fnum(r[a.value_col])
                if t is not None and v is not None:
                    recs.append((t, v))
                else:
                    dropped += 1
        breaks = load_breaks(a.breaks, a.breaks_file, a.breaks_date_col)
    except (ValueError, TypeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    recs.sort(key=lambda x: x[0])
    edges = [None] + breaks + [None]
    segments = []
    for lo, hi in zip(edges, edges[1:]):
        seg = [(t, v) for t, v in recs if (lo is None or t >= lo) and (hi is None or t < hi)]
        label = {"from": lo.date().isoformat() if lo else "start", "to_before": hi.date().isoformat() if hi else "end"}
        if len(seg) < a.min_n:
            segments.append({**label, "n": len(seg), "result": None,
                             "warnings": [f"fewer than {a.min_n} values: no trend test"]})
            continue
        times = [decimal_year(t) for t, _ in seg]
        values = [v for _, v in seg]
        months = [t.month for t, _ in seg]
        res = test_segment(times, values, alpha, autocorr, a.seasonal == "month", months)
        res.update(label)
        res["first"], res["last"] = seg[0][0].date().isoformat(), seg[-1][0].date().isoformat()
        segments.append(res)
    out = {
        "input": a.input, "value_col": a.value_col, "n_total": len(recs),
        "rows_without_valid_time_or_value": dropped,
        "registered_breaks": [b.date().isoformat() for b in breaks],
        "segments": segments,
        "rule": "trends are reported per segment; no single trend is reported across a registered break",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
