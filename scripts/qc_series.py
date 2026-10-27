#!/usr/bin/env python3
"""
Data quality gate for one time series (Phase 1, ecosystem-digital-twin skill).

Flags, never edits: every input row is written back unchanged, with a
qc_flag column added, so quarantined values stay visible downstream.

Checks:
  missing         value empty or non-numeric (always on)
  duplicate_time  the same timestamp appears more than once (always on)
  range           value outside --min / --max (physical or method limits)
  rate            |change| per hour above --max-rate, against the previous
                  value that passed missing/range (needs timestamps)
  stuck           the same value repeated --stuck-run times or more in a row
  neighbor        difference to a reference station is a robust outlier:
                  |d - median(d)| > --neighbor-k * 1.4826 * MAD(d)
Summary-only diagnostics:
  gaps            time steps longer than --max-gap-hours
  change point    Pettitt test on values that passed every row check; a
                  significant break must be explained in the bias and breaks
                  register before any trend is computed across it

File zones: a series that passes this gate moves from the twin
workspace's `landing/` zone (as received, never edited) to `trusted/`;
domain-converted files ready for the model live in `refined/`. The zones
are a file convention (SKILL.md Stage 2) — this script flags rows, it
never moves or edits files.

Usage:
  python3 qc_series.py do.csv --value-col do_mgl --min 0 --max 20 \
      --max-rate 3 --stuck-run 6 --max-gap-hours 3 --out do_qc.csv

Prints the summary JSON to stdout. Exit codes: 0 run completed; 2 input
error; 3 a flag named in --fail-on occurred (use it to make a gate fatal).
Long lists in the printed summary are capped by --max-items (default 25):
the summary keeps the first items plus the total count and a "truncated"
flag, so it stays small enough to hand to other models; --full-json FILE
writes the untruncated record.
"""

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone

MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}


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


def parse_float(text):
    if text is None or text.strip().lower() in MISSING:
        return None
    try:
        value = to_number(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def parse_time(text):
    if text is None or not text.strip():
        return None
    s = text.strip().replace("Z", "+00:00")
    try:
        t = datetime.fromisoformat(s)
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)  # naive stamps are compared as-is
    return t


def median(values):
    s = sorted(values)
    n = len(s)
    if n == 0:
        return None
    mid = n // 2
    return s[mid] if n % 2 else 0.5 * (s[mid - 1] + s[mid])


def average_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pettitt(values):
    """Pettitt (1979) change-point test. Returns (index_of_last_point_before_break, K, p)."""
    n = len(values)
    if n < 10:
        return None
    ranks = average_ranks(values)
    best_t, best_k, cum = None, -1.0, 0.0
    for t in range(1, n):  # break after position t (t points in first segment)
        cum += ranks[t - 1]
        u = abs(2.0 * cum - t * (n + 1))
        if u > best_k:
            best_k, best_t = u, t
    p = min(1.0, 2.0 * math.exp(-6.0 * best_k ** 2 / (n ** 3 + n ** 2)))
    return best_t - 1, best_k, p


def cap(summary, key, max_items):
    """Keep at most max_items of summary[key]; record the total and whether it was cut."""
    items = summary.get(key) or []
    summary[key + "_total"] = len(items)
    summary[key + "_truncated"] = len(items) > max_items
    summary[key] = items[:max_items]


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        if reader.fieldnames is None:
            raise SystemExit(f"error: {path} has no header row")
        return reader.fieldnames, list(reader)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="CSV with a header row")
    ap.add_argument("--time-col", default="time")
    ap.add_argument("--value-col", default="value")
    ap.add_argument("--min", type=float, help="lowest plausible value")
    ap.add_argument("--max", type=float, help="highest plausible value")
    ap.add_argument("--max-rate", type=float, help="largest plausible |change| per hour")
    ap.add_argument("--stuck-run", type=int, default=0, help="flag runs of N identical values (0 = off)")
    ap.add_argument("--max-gap-hours", type=float, help="report time steps longer than this")
    ap.add_argument("--reference", help="CSV of a neighboring station with the same time column")
    ap.add_argument("--ref-value-col", help="value column in --reference (default: --value-col)")
    ap.add_argument("--neighbor-k", type=float, default=4.0)
    ap.add_argument("--out", help="write flagged CSV here (default: no CSV output)")
    ap.add_argument("--fail-on", default="", help="comma list of flags that make the gate fail (exit 3)")
    ap.add_argument("--max-items", type=int, default=25, help="cap on listed gaps in the printed summary")
    ap.add_argument("--full-json", help="write the untruncated summary here")
    args = ap.parse_args(argv)

    fields, rows = read_rows(args.input)
    if args.value_col not in fields:
        print(f"error: value column '{args.value_col}' not in {fields}", file=sys.stderr)
        return 2
    has_time = args.time_col in fields
    n = len(rows)
    values = [parse_float(r.get(args.value_col)) for r in rows]
    times = [parse_time(r.get(args.time_col)) for r in rows] if has_time else [None] * n
    flags = [[] for _ in range(n)]
    notes = []
    if not has_time:
        notes.append(f"no '{args.time_col}' column: rate, gap, duplicate and neighbor checks skipped")

    for i, v in enumerate(values):
        if v is None:
            flags[i].append("missing")
        elif (args.min is not None and v < args.min) or (args.max is not None and v > args.max):
            flags[i].append("range")
    if has_time and any(t is None for t in times):
        bad = sum(1 for t in times if t is None)
        notes.append(f"{bad} rows have unparseable timestamps; they are excluded from time-based checks")

    order = sorted((i for i in range(n) if times[i] is not None), key=lambda i: times[i])
    if has_time:
        seen = {}
        for i in order:
            seen.setdefault(times[i], []).append(i)
        for idxs in seen.values():
            if len(idxs) > 1:
                for i in idxs:
                    flags[i].append("duplicate_time")

    if has_time and args.max_rate is not None:
        prev = None
        for i in order:
            if values[i] is None or "range" in flags[i]:
                continue
            if prev is not None:
                dt_h = (times[i] - times[prev]).total_seconds() / 3600.0
                if dt_h > 0 and abs(values[i] - values[prev]) / dt_h > args.max_rate:
                    flags[i].append("rate")
            prev = i

    if args.stuck_run and args.stuck_run > 1:
        seq = order if has_time else list(range(n))
        run = []
        for i in seq + [None]:
            if i is not None and values[i] is not None and run and values[i] == values[run[-1]]:
                run.append(i)
                continue
            if len(run) >= args.stuck_run:
                for j in run:
                    flags[j].append("stuck")
            run = [i] if i is not None and values[i] is not None else []

    neighbor_info = None
    if args.reference and has_time:
        ref_fields, ref_rows = read_rows(args.reference)
        ref_col = args.ref_value_col or args.value_col
        if ref_col not in ref_fields or args.time_col not in ref_fields:
            print(f"error: reference needs '{args.time_col}' and '{ref_col}'", file=sys.stderr)
            return 2
        ref = {}
        for r in ref_rows:
            t, v = parse_time(r.get(args.time_col)), parse_float(r.get(ref_col))
            if t is not None and v is not None:
                ref[t] = v
        pairs = [(i, values[i] - ref[times[i]]) for i in order
                 if values[i] is not None and "range" not in flags[i] and times[i] in ref]
        if len(pairs) >= 10:
            d = [p[1] for p in pairs]
            med = median(d)
            mad = median([abs(x - med) for x in d])
            scale = 1.4826 * mad
            if scale > 0:
                for i, di in pairs:
                    if abs(di - med) > args.neighbor_k * scale:
                        flags[i].append("neighbor")
            neighbor_info = {"matched": len(pairs), "median_difference": med, "robust_sd": scale}
        else:
            notes.append(f"neighbor check skipped: only {len(pairs)} matched timestamps (need >= 10)")

    gaps = []
    if has_time and args.max_gap_hours is not None:
        for a, b in zip(order, order[1:]):
            dt_h = (times[b] - times[a]).total_seconds() / 3600.0
            if dt_h > args.max_gap_hours:
                gaps.append({"after": rows[a][args.time_col], "before": rows[b][args.time_col], "hours": round(dt_h, 2)})

    clean_idx = [i for i in (order if has_time else range(n)) if not flags[i]]
    change_point = None
    pt = pettitt([values[i] for i in clean_idx])
    if pt is not None:
        idx, k_stat, p = pt
        change_point = {
            "last_value_before_break": rows[clean_idx[idx]].get(args.time_col, f"row {clean_idx[idx] + 2}"),
            "K": k_stat, "p_value": round(p, 6), "significant_at_0.05": p < 0.05,
        }
        if p < 0.05:
            notes.append("significant change point: record its cause in the bias and breaks register "
                         "before computing any trend across it (trend_test.py --breaks)")
    else:
        notes.append("change-point test skipped: fewer than 10 clean values")

    counts = {}
    for f in flags:
        for name in f:
            counts[name] = counts.get(name, 0) + 1
    flagged = sum(1 for f in flags if f)

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields + ["qc_flag"], delimiter=sniff_delimiter(args.input))
            writer.writeheader()
            for r, f in zip(rows, flags):
                out = dict(r)
                out["qc_flag"] = "|".join(f) if f else "ok"
                writer.writerow(out)

    fail_on = [s.strip() for s in args.fail_on.split(",") if s.strip()]
    failed = [name for name in fail_on if counts.get(name)]
    summary = {
        "input": args.input, "rows": n, "rows_flagged": flagged, "rows_ok": n - flagged,
        "flag_counts": counts, "gaps": gaps, "neighbor": neighbor_info,
        "change_point": change_point, "notes": notes,
        "gate": "fail" if failed else "pass", "failed_on": failed,
        "values_modified": False,
    }
    if args.full_json:
        with open(args.full_json, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=2)
    cap(summary, "gaps", args.max_items)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
