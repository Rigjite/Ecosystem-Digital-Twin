#!/usr/bin/env python3
"""
Alert bands with sustained-breach windows (Phase 4, ecosystem-digital-twin skill).

Evaluates one monitored series against amber and red bands. A breach becomes
an alert only when it is sustained: consecutive valid observations stay in
the band for at least --window-hours (a single spike never alerts). An
observation gap longer than --max-gap-hours ends an episode, because a
breach cannot be assumed to persist through missing data. --tolerate N lets
up to N isolated in-between readings (sensor noise) sit inside an episode
without ending it; the default 0 is strictest.

Quality flags from qc_series.py --out: values flagged as invalid (missing,
range, stuck, duplicate_time — see --ignore-flags) are ignored. Values
flagged only as suspect (rate, neighbor) are kept, because a real crash can
look like a rate jump; alerts that contain them say so, and the human check
decides.

Every band needs its anchor (--anchor: regulation, standard, or the
object's baseline statistic); without one the script refuses to run.

Bands are written as an operator and a threshold, high-is-bad or low-is-bad:
  dissolved oxygen   --amber "<5"  --red "<2"   --window-hours 6
  chlorophyll-a      --amber ">=25" --red ">=50" --window-hours 168

Alert record (as the skill's Phase 4 requires): indicator, band, observed
peak (or trough), start timestamp, end timestamp or "ongoing", elapsed hours,
number of observations, anchor, and the recommended human check. Likely
drivers are added by the analyst from the pattern memo, not guessed here.

Usage:
  python3 alert_bands.py do_qc.csv --indicator "DO bottom, mg/L" --value-col do \
      --amber "<5" --red "<2" --window-hours 6 --max-gap-hours 2 \
      --anchor "national standard for fishery waters" --human-check "profile with handheld sonde"

A breach is logged as "explained" (not alerted) with --explained-by: when
the driver series (rainfall, flow, temperature — from the same window) is
itself beyond its own watch level in a sustained episode overlapping the
breach, the breach goes to explained_breaches and does not alert, does not
set the status, and does not count for --fail-on. Only unexplained breaches
alert. The driver's own episode must be sustained for the same window — a
brief driver spike explains nothing. (Round 1 of the v2.7 program,
Southern Water: Stormharvester silences wet-weather alarms by learning
"normal behaviour" — this is the deterministic version: a band check on a
named driver, no ML.)

A threshold table per decision-maker class is read with --class-thresholds:
a CSV with columns class, limit (the operational limit in the indicator's
units, same direction as the bands). The output gains a class_thresholds
block: per class, the limit and whether the latest observed value and the
episode peak are within it — can_operate is yes only when the class can
operate now (latest value within its limit) and could operate at the event's
worst moment (peak within its limit); when there was no alert episode the
peak check is vacuous and only the latest value decides. (Round 2 of the
v2.7 program, Patos: one forecast value maps to one verdict per
decision-maker class — who can do what, distinct from the per-asset
clearance in scripts/registry.py.)

Exit 0 when evaluated (alerts or not); 3 when --fail-on red and a red alert
exists; 2 on input error.

No language model belongs in this path: the alert comes from this
deterministic rule and goes to a named human. A model may explain an alert
afterwards; it never triggers, delays, or suppresses one.
Long lists in the printed summary are capped by --max-items (default 25):
the summary keeps the first items plus the total count and a "truncated"
flag, so it stays small enough to hand to other models; --full-json FILE
writes the untruncated record.
"""

import argparse
import csv
import json
import math
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


def cap(summary, key, max_items):
    """Keep at most max_items of summary[key]; record the total and whether it was cut."""
    items = summary.get(key) or []
    summary[key + "_total"] = len(items)
    summary[key + "_truncated"] = len(items) > max_items
    summary[key] = items[:max_items]


def parse_band(spec, name):
    m = BAND.match(spec or "")
    if not m:
        raise ValueError(f"--{name} must look like '<5' or '>=25', got {spec!r}")
    op, thr = m.group(1), to_number(m.group(2))
    test = {"<": lambda v: v < thr, "<=": lambda v: v <= thr,
            ">": lambda v: v > thr, ">=": lambda v: v >= thr}[op]
    return op, thr, test


def find_episodes(pts, amber, red, window_hours, max_gap_hours, tolerate):
    """Sustained episodes per band, plus the count of unsustained (spike)
    runs at the amber band. Each episode is {"band", "start", "end",
    "hours", "run"}. Amber episodes already covered by a red episode are
    dropped. With red None, only the amber band is checked."""
    out, spikes = [], 0
    red_spans = []
    bands = (("red", red), ("amber", amber)) if red is not None else (("amber", amber),)
    for band, test in bands:
        for run in episodes(pts, test, max_gap_hours, tolerate):
            start, end = run[0][0], run[-1][0]
            hours = (end - start).total_seconds() / 3600.0
            if hours < window_hours or len(run) < 2:
                if band == "amber":
                    spikes += 1
                continue
            if band == "amber" and any(rs <= start and end <= re_ for rs, re_ in red_spans):
                continue
            if band == "red":
                red_spans.append((start, end))
            out.append({"band": band, "start": start, "end": end, "hours": hours, "run": run})
    out.sort(key=lambda x: (x["start"], x["band"] != "red"))
    return out, spikes


def episodes(points, in_band, max_gap_h, tolerate=0):
    """Runs of in-band points, ended by a long gap or by more than `tolerate`
    consecutive out-of-band points. Points are (time, value, suspect)."""
    runs, cur, pending, prev_t = [], [], [], None
    for p in points:
        t, v = p[0], p[1]
        gap = prev_t is not None and (t - prev_t).total_seconds() / 3600.0 > max_gap_h
        prev_t = t
        if gap:
            if cur:
                runs.append(cur)
            cur, pending = ([p] if in_band(v) else []), []
            continue
        if in_band(v):
            cur.append(p)
            pending = []
        elif cur:
            pending.append(p)
            if len(pending) > tolerate:
                runs.append(cur)
                cur, pending = [], []
    if cur:
        runs.append(cur)
    return runs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("--indicator", required=True, help="name, unit and location of the indicator")
    ap.add_argument("--time-col", default="time")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--qc-col", default="qc_flag", help="quality flag column, if present")
    ap.add_argument("--amber", required=True)
    ap.add_argument("--red", required=True)
    ap.add_argument("--window-hours", type=float, required=True, help="minimum sustained duration of a breach")
    ap.add_argument("--max-gap-hours", type=float, default=float("inf"), help="longer gaps end an episode")
    ap.add_argument("--anchor", required=True, help="regulation, standard, or baseline the bands come from")
    ap.add_argument("--human-check", default="", help="the recommended human check for an alert")
    ap.add_argument("--tolerate", type=int, default=0, help="isolated in-between readings allowed inside an episode")
    ap.add_argument("--ignore-flags", default="missing,range,stuck,duplicate_time",
                    help="qc flags that make a value invalid (others are kept as suspect)")
    ap.add_argument("--fail-on", choices=["none", "amber", "red"], default="none")
    ap.add_argument("--max-items", type=int, default=25, help="cap on listed alerts in the printed summary")
    ap.add_argument("--full-json", help="write the untruncated record here")
    ap.add_argument("--explained-by", help="driver series CSV: a breach is logged as explained, not alerted, "
                                           "when this series is itself beyond its own watch level in the same window")
    ap.add_argument("--driver-col", default="value", help="value column of the driver series (default value)")
    ap.add_argument("--driver-time-col", default="time", help="time column of the driver series (default time)")
    ap.add_argument("--driver-amber", help="the driver's own amber band, e.g. '>=25'")
    ap.add_argument("--driver-red", help="the driver's own red band, e.g. '>=50'")
    ap.add_argument("--class-thresholds", help="per-class operational limits CSV: columns class, limit "
                                               "(in the indicator's units, same direction as the bands)")
    a = ap.parse_args(argv)
    try:
        if not a.anchor.strip():
            raise ValueError("--anchor must name the regulation, standard, or baseline behind the bands")
        a_op, a_thr, amber = parse_band(a.amber, "amber")
        r_op, r_thr, red = parse_band(a.red, "red")
        if (a_op[0] == "<") != (r_op[0] == "<"):
            raise ValueError("amber and red must point the same way (both '<' or both '>')")
        if (a_op[0] == "<" and r_thr > a_thr) or (a_op[0] == ">" and r_thr < a_thr):
            raise ValueError("the red band must be beyond the amber band")
        with open(a.input, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.input))
            for col in (a.time_col, a.value_col):
                if col not in (reader.fieldnames or []):
                    raise ValueError(f"column '{col}' not found")
            has_qc = a.qc_col in (reader.fieldnames or [])
            invalid = {f.strip() for f in a.ignore_flags.split(",") if f.strip()}
            pts, ignored = [], 0
            for r in reader:
                t, v = ftime(r[a.time_col]), fnum(r[a.value_col])
                flags = set() if not has_qc else {f for f in (r.get(a.qc_col) or "ok").split("|") if f != "ok"}
                if t is None or v is None or flags & invalid:
                    ignored += 1
                    continue
                pts.append((t, v, sorted(flags)))
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    pts.sort(key=lambda x: x[0])
    low_bad = a_op[0] == "<"
    last_t = pts[-1][0] if pts else None
    found, spikes = find_episodes(pts, amber, red, a.window_hours, a.max_gap_hours, a.tolerate)
    explained = []
    if a.explained_by:
        if not a.driver_amber:
            print("error: --explained-by needs --driver-amber (the driver's own watch level)", file=sys.stderr)
            return 2
        try:
            d_op, d_thr, d_amber = parse_band(a.driver_amber, "driver-amber")
            d_red = None
            if a.driver_red:
                d_r_op, d_r_thr, d_red = parse_band(a.driver_red, "driver-red")
                if (d_op[0] == "<") != (d_r_op[0] == "<"):
                    raise ValueError("driver-amber and driver-red must point the same way (both '<' or both '>')")
                if (d_op[0] == "<" and d_r_thr > d_thr) or (d_op[0] == ">" and d_r_thr < d_thr):
                    raise ValueError("the driver red band must be beyond the driver amber band")
            with open(a.explained_by, newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.explained_by))
                for col in (a.driver_time_col, a.driver_col):
                    if col not in (reader.fieldnames or []):
                        raise ValueError(f"driver column '{col}' not found in {a.explained_by}")
                d_has_qc = a.qc_col in (reader.fieldnames or [])
                d_invalid = {f.strip() for f in a.ignore_flags.split(",") if f.strip()}
                dpts = []
                for r in reader:
                    t, v = ftime(r[a.driver_time_col]), fnum(r[a.driver_col])
                    flags = set() if not d_has_qc else {f for f in (r.get(a.qc_col) or "ok").split("|") if f != "ok"}
                    if t is None or v is None or flags & d_invalid:
                        continue
                    dpts.append((t, v, sorted(flags)))
        except (ValueError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        dpts.sort(key=lambda x: x[0])
        d_found, _ = find_episodes(dpts, d_amber, d_red, a.window_hours, a.max_gap_hours, a.tolerate)
        kept = []
        for ep in found:
            expl = next((d for d in d_found
                         if d["start"] <= ep["end"] and ep["start"] <= d["end"]), None)
            if expl is None:
                kept.append(ep)
                continue
            explained.append((ep, expl))
        found = kept
    classes = []
    if a.class_thresholds:
        try:
            with open(a.class_thresholds, newline="", encoding="utf-8-sig") as fh:
                reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.class_thresholds))
                for col in ("class", "limit"):
                    if col not in (reader.fieldnames or []):
                        raise ValueError(f"class-threshold column '{col}' not found in {a.class_thresholds}")
                seen = set()
                for r in reader:
                    name = (r.get("class") or "").strip()
                    limit = fnum(r.get("limit"))
                    if not name or limit is None:
                        raise ValueError("each class-threshold row needs a named class and a finite limit")
                    if name in seen:
                        raise ValueError(f"duplicate class '{name}' in {a.class_thresholds}")
                    seen.add(name)
                    classes.append((name, limit))
                if not classes:
                    raise ValueError(f"no class thresholds in {a.class_thresholds}")
        except (ValueError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    alerts = []
    for ep in found:
        band, start, end, run, hours = ep["band"], ep["start"], ep["end"], ep["run"], ep["hours"]
        peak = min(p[1] for p in run) if low_bad else max(p[1] for p in run)
        suspect = sorted({f for p in run for f in p[2]})
        alerts.append({
            "indicator": a.indicator, "band": band, "observed_extreme": peak,
            "threshold": f"{a_op if band == 'amber' else r_op}{a_thr if band == 'amber' else r_thr}",
            "start": start.isoformat(), "end": "ongoing" if end == last_t else end.isoformat(),
            "elapsed_hours": round(hours, 2), "observations": len(run),
            "red_band_observations": sum(1 for p in run if red(p[1])),
            "suspect_flags_inside": suspect,
            "anchor": a.anchor, "recommended_check": a.human_check or "(state the human check)",
            "likely_drivers": "(from the pattern memo and event catalogue)",
        })
    explained_breaches = []
    for ep, dep in explained:
        band, start, end, run, hours = ep["band"], ep["start"], ep["end"], ep["run"], ep["hours"]
        peak = min(p[1] for p in run) if low_bad else max(p[1] for p in run)
        explained_breaches.append({
            "indicator": a.indicator, "band": band, "observed_extreme": peak,
            "threshold": f"{a_op if band == 'amber' else r_op}{a_thr if band == 'amber' else r_thr}",
            "start": start.isoformat(), "end": "ongoing" if end == last_t else end.isoformat(),
            "elapsed_hours": round(hours, 2), "observations": len(run),
            "explained_by": {"driver": a.explained_by, "driver_indicator": a.driver_col,
                             "driver_band": dep["band"],
                             "driver_threshold": f"{d_op if dep['band'] == 'amber' else d_r_op}"
                                                 f"{d_thr if dep['band'] == 'amber' else d_r_thr}",
                             "driver_start": dep["start"].isoformat(),
                             "driver_end": dep["end"].isoformat()},
            "anchor": a.anchor,
            "rule": "breach explained by the driver; logged, not alerted",
        })
    status = "red" if any(x["band"] == "red" for x in alerts) else ("amber" if alerts else "green")
    rule = "a breach alerts only when sustained for the window; gaps end episodes; flagged values ignored"
    if a.explained_by:
        rule += "; a breach the driver explains is logged, not alerted"
    class_thresholds = []
    if classes:
        latest = pts[-1][1] if pts else None
        peak = None
        if alerts:
            peak = (max(x["observed_extreme"] for x in alerts) if not low_bad
                    else min(x["observed_extreme"] for x in alerts))

        def within(v, limit):
            return None if v is None else (v <= limit if not low_bad else v >= limit)

        for name, limit in classes:
            lw, pw = within(latest, limit), within(peak, limit)
            class_thresholds.append({
                "class": name, "limit": limit,
                "latest_value": latest, "latest_within": lw,
                "peak_value": peak, "peak_within": pw,
                "can_operate": (lw if pw is None else (lw and pw)) if lw is not None else None,
            })
        rule += "; class thresholds map the latest value and the episode peak to one verdict per decision-maker class"
    out = {"indicator": a.indicator, "observations_used": len(pts), "observations_ignored": ignored,
           "window_hours": a.window_hours, "max_gap_hours": a.max_gap_hours, "tolerate": a.tolerate,
           "status": status, "alerts": alerts, "explained_breaches": explained_breaches,
           "class_thresholds": class_thresholds,
           "unsustained_breaches": spikes, "rule": rule}
    if a.full_json:
        with open(a.full_json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
    cap(out, "alerts", a.max_items)
    cap(out, "explained_breaches", a.max_items)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if a.fail_on == "red" and status == "red":
        return 3
    if a.fail_on == "amber" and status in ("amber", "red"):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
