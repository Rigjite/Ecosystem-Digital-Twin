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
  --prewhiten auto   trend-free pre-whitening (Yue et al. 2002) when the lag-1
                     autocorrelation of the detrended series is significant
                     and sampling is regular; otherwise stated as uncorrected.
Slopes are per year; time is converted to decimal years, so irregular
sampling is handled by Sen's slope. Confidence interval of the slope follows
Gilbert (1987). Fewer than --min-n values in a segment: no test, stated.

Usage:
  python3 trend_test.py chl.csv --value-col chl --breaks 2009-01-01
  python3 trend_test.py tp.csv --value-col tp --seasonal month --breaks-file bias_register.csv

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


def lag1(xs):
    n = len(xs)
    if n < 3:
        return None
    m = sum(xs) / n
    den = sum((x - m) ** 2 for x in xs)
    if den == 0:
        return None
    return sum((xs[i] - m) * (xs[i + 1] - m) for i in range(n - 1)) / den


def regular(times):
    steps = [b - a for a, b in zip(times, times[1:])]
    if len(steps) < 2:
        return False
    m = sum(steps) / len(steps)
    if m <= 0:
        return False
    sd = math.sqrt(sum((s - m) ** 2 for s in steps) / len(steps))
    return sd / m <= 0.5


def test_segment(times, values, alpha, prewhiten, seasonal, months):
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
    else:
        s_val, var = mk_s_var(values)
        slopes = pair_slopes(times, values)
        res["test"] = "Mann-Kendall"
        slope0 = median(slopes) if slopes else 0.0
        detr = [v - slope0 * t for t, v in zip(times, values)]
        r1 = lag1(detr)
        res["lag1_autocorrelation_detrended"] = r1
        bound = ND.inv_cdf(1 - alpha / 2) / math.sqrt(n)
        significant = r1 is not None and abs(r1) > bound
        apply = prewhiten == "tfpw" or (prewhiten == "auto" and significant)
        if apply and not regular(times):
            res["warnings"].append("serial correlation not corrected: sampling is irregular, "
                                   "pre-whitening needs a near-regular series")
            apply = False
        elif significant and not apply:
            res["warnings"].append("significant lag-1 autocorrelation left uncorrected: p-value is optimistic")
        if apply and r1 is not None:
            yp = [detr[i] - r1 * detr[i - 1] for i in range(1, n)]
            blended = [y + slope0 * t for y, t in zip(yp, times[1:])]
            s_val, var = mk_s_var(blended)
            n_tested = len(blended)
            res["prewhitening"] = "trend-free pre-whitening (Yue et al. 2002)"
        else:
            res["prewhitening"] = "none"
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--time-col", default="time")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--breaks", help="comma list of ISO dates where a registered break starts a new segment")
    ap.add_argument("--breaks-file", help="CSV bias and breaks register")
    ap.add_argument("--breaks-date-col", default="date")
    ap.add_argument("--seasonal", choices=["none", "month"], default="none")
    ap.add_argument("--prewhiten", choices=["auto", "tfpw", "none"], default="auto")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--min-n", type=int, default=8)
    a = ap.parse_args(argv)
    try:
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
    except (ValueError, OSError) as exc:
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
        res = test_segment(times, values, a.alpha, a.prewhiten, a.seasonal == "month", months)
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
