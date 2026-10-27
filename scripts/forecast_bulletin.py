#!/usr/bin/env python3
"""
Daily forecast bulletin (Round 2 of the v2.7 program, Gironde).

The registry is for the builder; the bulletin is for the client. This
renderer reads one forecast registry entry and the latest observation CSV
and writes a one-page dated Markdown bulletin: the observed value today,
the forecast values for the lead window, the watch status, and the date
the forecast will be scored. It changes no numbers — it renders the
registry entry and the latest observation into the thing a client
actually reads.

Usage:
  python3 forecast_bulletin.py --registry examples/beira/registry.jsonl \
      --id BEIRA-F-001 --observations latest.csv --output bulletin.md
  python3 forecast_bulletin.py --registry r.jsonl --id F-001 \
      --observations latest.csv --amber ">=25" --red ">=50"

--observations is a CSV with time and value columns (decimal commas
accepted); the latest row by time is the observed value today. --amber /
--red (same band syntax as alert_bands.py, e.g. ">=25") are optional: with
them, the bulletin states the watch status of the latest observation and
of the forecast value; without them the status is "not stated (no bands
given)". --output writes the bulletin to a file; without it the bulletin
goes to stdout.

Exit 0 when written; 2 on input error (missing file, unknown forecast id,
a record that is not a forecast, missing time/value columns, no
observations, a band spec that does not parse, bands pointing different
ways, or a red band inside the amber band).

The bulletin names the scoring date (the forecast's horizon end) and the
verification metric declared in the registry entry, so the client can see
when and how the forecast will be judged.
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


def parse_band(spec, name):
    m = BAND.match(spec or "")
    if not m:
        raise ValueError(f"--{name} must look like '<5' or '>=25', got {spec!r}")
    op, thr = m.group(1), to_number(m.group(2))
    test = {"<": lambda v: v < thr, "<=": lambda v: v <= thr,
            ">": lambda v: v > thr, ">=": lambda v: v >= thr}[op]
    return op, thr, test


def band_of(value, amber, red):
    if red is not None and red[2](value):
        return "red"
    if amber[2](value):
        return "amber"
    return "green"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registry", required=True, help="JSONL registry file")
    ap.add_argument("--id", required=True, help="forecast id in the registry")
    ap.add_argument("--observations", required=True, help="latest observations CSV: time, value")
    ap.add_argument("--value-col", default="value", help="value column of the observations (default value)")
    ap.add_argument("--time-col", default="time", help="time column of the observations (default time)")
    ap.add_argument("--amber", help="amber band for the watch status, e.g. '>=25'")
    ap.add_argument("--red", help="red band for the watch status, e.g. '>=50'")
    ap.add_argument("--output", help="write the bulletin to this file (default: stdout)")
    a = ap.parse_args(argv)
    try:
        amber = red = None
        if a.amber:
            amber = parse_band(a.amber, "amber")
        if a.red:
            red = parse_band(a.red, "red")
        if amber is not None and red is not None:
            if (amber[0][0] == "<") != (red[0][0] == "<"):
                raise ValueError("amber and red must point the same way (both '<' or both '>')")
            if (amber[0][0] == "<" and red[1] > amber[1]) or (amber[0][0] == ">" and red[1] < amber[1]):
                raise ValueError("the red band must be beyond the amber band")
        with open(a.registry, encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]
        entry = next((r for r in records if r.get("id") == a.id), None)
        if entry is None:
            raise ValueError(f"forecast id '{a.id}' is not in the registry")
        if entry.get("type") != "forecast":
            raise ValueError(f"record '{a.id}' is a {entry.get('type')}, not a forecast")
        with open(a.observations, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, delimiter=sniff_delimiter(a.observations))
            for col in (a.time_col, a.value_col):
                if col not in (reader.fieldnames or []):
                    raise ValueError(f"column '{col}' not found in {a.observations}")
            rows = []
            for r in reader:
                t, v = ftime(r[a.time_col]), fnum(r[a.value_col])
                if t is None or v is None:
                    continue
                rows.append((t, v))
        if not rows:
            raise ValueError("no usable observations in the observations file")
        rows.sort(key=lambda x: x[0])
        obs_t, obs_v = rows[-1]
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    unit = entry.get("unit") or ""
    unit = f" {unit}" if unit else ""
    value = entry.get("value")
    interval = ""
    if entry.get("lower") is not None and entry.get("upper") is not None:
        interval = f" (interval {entry['lower']}–{entry['upper']}{unit}"
        if entry.get("interval_method"):
            interval += f", {entry['interval_method']}"
        interval += ")"
    if amber is not None:
        obs_status = band_of(obs_v, amber, red)
        fc_status = band_of(value, amber, red) if isinstance(value, (int, float)) else "not stated"
        status = (f"latest observation {obs_status} "
                  f"(amber {a.amber}" + (f", red {a.red}" if a.red else "") + "); "
                  f"forecast value {fc_status}")
    else:
        status = "not stated (no bands given)"
    trial = entry.get("trial")
    lines = [f"# Forecast bulletin — {entry['id']}",
             "",
             f"Target: {entry.get('target')}",
             f"Issued at: {entry.get('issued_at')}",
             f"Model: {entry.get('model')} {entry.get('model_version') or ''}".rstrip(),
             f"Refresh cadence: {entry.get('cadence') or 'not stated'}; "
             f"usable warning lead time: "
             f"{entry.get('lead_time', {}).get('value') if isinstance(entry.get('lead_time'), dict) else 'not stated'} "
             f"{entry.get('lead_time', {}).get('unit') if isinstance(entry.get('lead_time'), dict) else ''}".rstrip(),
             "",
             f"Observed value today: {obs_v}{unit} (latest observation, {obs_t.date().isoformat()})",
             f"Forecast: {value}{unit}{interval}",
             f"Watch status: {status}",
             "",
             f"This forecast will be scored on {entry.get('horizon_end')} "
             f"against the {entry.get('metric')} metric, exactly as issued.",
             ]
    if trial:
        lines.append("Trial forecast — no decision weight.")
    lines.append("")
    lines.append("Source: the forecast registry entry and the latest observation "
                 "CSV; this bulletin renders them, it changes no numbers.")
    text = "\n".join(lines) + "\n"
    if a.output:
        with open(a.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"bulletin written to {a.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
