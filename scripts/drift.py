#!/usr/bin/env python3
"""
Deterministic drift / connectivity (Round 2 of the v2.7 program, EDITO).

Passive particles are advected by a published current field — displacement
= current velocity x time, plus a wind-leeway factor — and the module
reports, per target zone, the connectivity (fraction of released particles
arriving in the zone) and the median travel time (hours) of the arrivals.
That is the Turtle Drift Tracker's connectivity and the Plastic Pollution
Tracker's travel time, in deterministic form: one trajectory per release
point, no ensemble, no RNG.

Inputs (all CSV, comma/semicolon/tab; decimal commas accepted):
  --release  release points: id, lat, lon
  --currents current field: time, u, v — u eastward, v northward, m/s.
             One row is a constant field; several rows are a time-varying
             field (the row with the latest time at or before the step is
             used, the last row held after the table ends). The vectors
             are transcribed as a table from a published current rose or
             Copernicus Marine values — the source is recorded by the
             builder in the passport, never invented here.
  --targets  target zones: zone, lat_min, lat_max, lon_min, lon_max

A particle arrives in a zone at the first step its position is inside the
zone's box (a release point inside a zone arrives at 0 hours). A particle
that never arrives within --max-hours is reported with arrived_zone null
and no travel time. 1 degree latitude = 111,320 m; 1 degree longitude =
111,320 x cos(lat) m, evaluated at the particle's latitude each step.

Wind leeway: --wind-u / --wind-v (m/s, default 0) add leeway x wind to the
current at every step; --leeway 0 (the default) is current only.

Usage:
  python3 drift.py --release release.csv --currents currents.csv \
      --targets targets.csv --step-hours 1 --max-hours 240

Exit 0 when evaluated; 2 on input error (missing file or column, no
release points, no targets, no current rows, --step-hours or --max-hours
not positive, --leeway negative).

The output is a model result, not data: connectivity and travel time are
computed from the transcribed field and the declared leeway, and the
method is printed with the result so a reader can reproduce it.
"""

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone

MISSING = {"", "na", "nan", "null", "none", "-", "n/a"}
METRES_PER_DEG_LAT = 111320.0


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


def read_csv(path, required):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh, delimiter=sniff_delimiter(path))
        for col in required:
            if col not in (reader.fieldnames or []):
                raise ValueError(f"column '{col}' not found in {path}")
        return list(reader)


def median(values):
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release", required=True, help="release points CSV: id, lat, lon")
    ap.add_argument("--currents", required=True, help="current field CSV: time, u, v (m/s)")
    ap.add_argument("--targets", required=True, help="target zones CSV: zone, lat_min, lat_max, lon_min, lon_max")
    ap.add_argument("--step-hours", type=float, default=1.0, help="advection step in hours (default 1)")
    ap.add_argument("--max-hours", type=float, default=240.0, help="longest travel time tracked (default 240)")
    ap.add_argument("--leeway", type=float, default=0.0, help="wind-leeway factor, fraction of the wind vector (default 0)")
    ap.add_argument("--wind-u", type=float, default=0.0, help="wind eastward component, m/s (default 0)")
    ap.add_argument("--wind-v", type=float, default=0.0, help="wind northward component, m/s (default 0)")
    a = ap.parse_args(argv)
    try:
        if a.step_hours <= 0:
            raise ValueError("--step-hours must be positive")
        if a.max_hours <= 0:
            raise ValueError("--max-hours must be positive")
        if a.leeway < 0:
            raise ValueError("--leeway must not be negative")
        releases = read_csv(a.release, ["id", "lat", "lon"])
        if not releases:
            raise ValueError("no release points in the release file")
        pts = []
        for r in releases:
            lat, lon = fnum(r["lat"]), fnum(r["lon"])
            if lat is None or lon is None:
                raise ValueError(f"release point '{r.get('id')}' needs numeric lat and lon")
            pts.append((r["id"], lat, lon))
        cur = read_csv(a.currents, ["time", "u", "v"])
        if not cur:
            raise ValueError("no current rows in the currents file")
        field = []
        for r in cur:
            t, u, v = ftime(r["time"]), fnum(r["u"]), fnum(r["v"])
            if t is None or u is None or v is None:
                raise ValueError("each currents row needs a time and numeric u, v")
            field.append((t, u, v))
        field.sort(key=lambda x: x[0])
        targets = read_csv(a.targets, ["zone", "lat_min", "lat_max", "lon_min", "lon_max"])
        if not targets:
            raise ValueError("no target zones in the targets file")
        zones = []
        for r in targets:
            vals = [fnum(r[c]) for c in ("lat_min", "lat_max", "lon_min", "lon_max")]
            if any(v is None for v in vals):
                raise ValueError(f"target zone '{r.get('zone')}' needs numeric bounds")
            if vals[0] > vals[1] or vals[2] > vals[3]:
                raise ValueError(f"target zone '{r.get('zone')}' has an inverted bound")
            zones.append((r["zone"], vals[0], vals[1], vals[2], vals[3]))
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    t0 = field[0][0]
    steps = int(a.max_hours / a.step_hours)
    particles = []
    for rid, lat, lon in pts:
        arrived, travel = None, None
        for zone, la_min, la_max, lo_min, lo_max in zones:
            if la_min <= lat <= la_max and lo_min <= lon <= lo_max:
                arrived, travel = zone, 0.0
                break
        if arrived is None:
            clat, clon = lat, lon
            for k in range(1, steps + 1):
                t = t0.timestamp() + k * a.step_hours * 3600.0
                u, v = field[0][1], field[0][2]
                for ft, fu, fv in field:
                    if ft.timestamp() <= t:
                        u, v = fu, fv
                    else:
                        break
                dt = a.step_hours * 3600.0
                dlat = (v + a.leeway * a.wind_v) * dt / METRES_PER_DEG_LAT
                dlon = (u + a.leeway * a.wind_u) * dt / (METRES_PER_DEG_LAT * math.cos(math.radians(clat)))
                clat += dlat
                clon += dlon
                for zone, la_min, la_max, lo_min, lo_max in zones:
                    if la_min <= clat <= la_max and lo_min <= clon <= lo_max:
                        arrived, travel = zone, round(k * a.step_hours, 6)
                        break
                if arrived is not None:
                    break
        particles.append({"id": rid, "arrived_zone": arrived, "travel_hours": travel})
    out_zones = []
    for zone, _, _, _, _ in zones:
        arrivals = [p["travel_hours"] for p in particles if p["arrived_zone"] == zone]
        out_zones.append({"zone": zone, "arrivals": len(arrivals),
                          "connectivity": round(len(arrivals) / len(particles), 6),
                          "median_travel_hours": median(arrivals) if arrivals else None})
    out = {"released": len(particles), "step_hours": a.step_hours, "max_hours": a.max_hours,
           "leeway": a.leeway, "wind": {"u": a.wind_u, "v": a.wind_v},
           "zones": out_zones, "particles": particles,
           "method": "deterministic advection: displacement = (current + leeway x wind) x dt; "
                     "1 deg lat = 111320 m; 1 deg lon = 111320 x cos(lat) m; "
                     "arrival = first step inside a target zone"}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
