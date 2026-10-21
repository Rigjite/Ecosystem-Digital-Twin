#!/usr/bin/env python3
"""
Generalize sensitive species occurrence coordinates before any shared output
(conservation safeguard, ecosystem-digital-twin skill).

Follows GBIF best practice (Chapman 2020, "Current Best Practices for
Generalizing Sensitive Species Occurrence Data", GBIF Secretariat):
coordinates are rounded on a decimal-degree grid chosen by sensitivity
category. This skill sets a floor of 0.1 degree for every listed species:

  category   GBIF guidance                 this skill (default)
  extreme    withhold, or 1 degree         withhold (coordinates blanked);
                                           --extreme-grid 1 rounds to 1 degree
  high       0.1 degree (~11 km)           0.1 degree
  medium     0.01 degree (~1 km)           0.1 degree (floor)
  low        0.001 degree (~100 m)         0.1 degree (floor)
  none       unrestricted                  unchanged

--allow-gbif-finer applies GBIF's finer medium/low grids instead of the
floor; use it only with the reason recorded in the object passport.

For every generalized row the Darwin Core fields coordinateUncertaintyInMeters
(distance from the rounded point to the farthest cell corner),
coordinatePrecision, dataGeneralizations and informationWithheld are set, and
free-text or verbatim location fields that can re-identify the site are
blanked (see --blank-cols).

--check FILE verifies a file that is about to be shared: every sensitive row
must sit on its category grid and carry no site-identifying text. Exit 3 on
any violation. The report names row numbers only, never coordinates.

Usage:
  python3 generalize_coords.py occurrences.csv --category-col sensitivity --out shared.csv
  python3 generalize_coords.py occurrences.csv --category high --out shared.csv
  python3 generalize_coords.py --check shared.csv --category-col sensitivity
"""

import argparse
import csv
import json
import math
import sys

GBIF_GRID = {"extreme": 1.0, "high": 0.1, "medium": 0.01, "low": 0.001}
FLOOR = 0.1
DEFAULT_BLANK = ["locality", "verbatimLocality", "verbatimCoordinates", "verbatimLatitude",
                 "verbatimLongitude", "footprintWKT", "georeferenceRemarks", "locationRemarks",
                 "verbatimElevation", "verbatimDepth"]
EARTH_R = 6371008.8


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


def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_R * math.asin(min(1.0, math.sqrt(h)))


def decimals(grid):
    return max(0, -int(math.floor(math.log10(grid) + 1e-9)))


def round_to(x, grid):
    return math.floor(x / grid + 0.5) * grid


def generalize(lat, lon, grid):
    d = decimals(grid)
    rlat = max(-90.0, min(90.0, round(round_to(lat, grid), d)))
    rlon = round(round_to(lon, grid), d)
    if rlon > 180:
        rlon -= 360
    if rlon <= -180:
        rlon += 360
    half = grid / 2.0
    corners = [(max(-90.0, min(90.0, rlat + dy)), rlon + dx) for dy in (-half, half) for dx in (-half, half)]
    unc = max(haversine(rlat, rlon, cy, cx) for cy, cx in corners)
    return rlat, rlon, int(math.ceil(unc))


def grid_for(category, args):
    c = (category or "").strip().lower()
    if c in ("", "none", "not sensitive", "no"):
        return None
    if c not in GBIF_GRID:
        raise ValueError(f"unknown sensitivity category '{category}' (use extreme, high, medium, low, none)")
    if c == "extreme":
        return "withhold" if args.extreme_grid is None else max(args.extreme_grid, 1.0)
    g = GBIF_GRID[c]
    return g if args.allow_gbif_finer else max(g, FLOOR)


def on_grid(value, grid):
    k = value / grid
    return abs(k - round(k)) < 1e-6


def row_category(row, args):
    if args.category_col:
        return row.get(args.category_col)
    return args.category


def fnum(text):
    try:
        v = to_number(text)
    except (AttributeError, TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def run_generalize(args, fields, rows, blank_cols):
    out_fields = list(fields)
    for extra in ("coordinateUncertaintyInMeters", "coordinatePrecision", "dataGeneralizations",
                  "informationWithheld"):
        if extra not in out_fields:
            out_fields.append(extra)
    counts = {"generalized": 0, "withheld": 0, "unchanged": 0, "missing_coordinates": 0}
    out_rows = []
    for r in rows:
        r = dict(r)
        grid = grid_for(row_category(r, args), args)
        lat, lon = fnum(r.get(args.lat_col)), fnum(r.get(args.lon_col))
        if grid is None:
            counts["unchanged"] += 1
            out_rows.append(r)
            continue
        for col in blank_cols:
            if col in r:
                r[col] = ""
        if grid == "withhold":
            r[args.lat_col] = r[args.lon_col] = ""
            r["coordinateUncertaintyInMeters"] = r["coordinatePrecision"] = ""
            r["dataGeneralizations"] = "Coordinates withheld: extreme sensitivity (GBIF category 1)"
            r["informationWithheld"] = "Location withheld; available from the data owner under agreement"
            counts["withheld"] += 1
        elif lat is None or lon is None:
            counts["missing_coordinates"] += 1
        else:
            rlat, rlon, unc = generalize(lat, lon, grid)
            d = decimals(grid)
            r[args.lat_col] = f"{rlat:.{d}f}"
            r[args.lon_col] = f"{rlon:.{d}f}"
            r["coordinateUncertaintyInMeters"] = str(unc)
            r["coordinatePrecision"] = str(grid)
            r["dataGeneralizations"] = f"Coordinates rounded to a {grid}-degree grid (sensitive species)"
            r["informationWithheld"] = "Precise location withheld; available from the data owner under agreement"
            counts["generalized"] += 1
        out_rows.append(r)
    return out_fields, out_rows, counts


def run_check(args, rows, blank_cols):
    violations = []
    for i, r in enumerate(rows, start=2):  # row 1 is the header
        try:
            grid = grid_for(row_category(r, args), args)
        except ValueError as exc:
            violations.append({"row": i, "problem": str(exc)})
            continue
        if grid is None:
            continue
        lat, lon = fnum(r.get(args.lat_col)), fnum(r.get(args.lon_col))
        if grid == "withhold":
            if lat is not None or lon is not None:
                violations.append({"row": i, "problem": "extreme-sensitivity coordinates present"})
        elif lat is not None and lon is not None:
            if not (on_grid(lat, grid) and on_grid(lon, grid)):
                violations.append({"row": i, "problem": f"coordinates finer than the {grid}-degree grid"})
        leaked = [c for c in blank_cols if (r.get(c) or "").strip()]
        if leaked:
            violations.append({"row": i, "problem": f"site-identifying text in {leaked}"})
    return violations


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="occurrence CSV to generalize")
    ap.add_argument("--check", metavar="FILE", help="verify a file before sharing instead of generalizing")
    ap.add_argument("--lat-col", default="decimalLatitude")
    ap.add_argument("--lon-col", default="decimalLongitude")
    ap.add_argument("--category", help="one category for every row: extreme, high, medium, low, none")
    ap.add_argument("--category-col", help="column holding the category per row")
    ap.add_argument("--extreme-grid", type=float, help="round extreme rows to this grid (>= 1) instead of withholding")
    ap.add_argument("--allow-gbif-finer", action="store_true", help="use GBIF's finer medium/low grids (record why)")
    ap.add_argument("--blank-cols", help="comma list replacing the default site-identifying columns")
    ap.add_argument("--also-blank", default="", help="extra columns to blank in addition to the defaults")
    ap.add_argument("--out", help="output CSV (required unless --check)")
    args = ap.parse_args(argv)
    if not args.category and not args.category_col:
        print("error: give --category or --category-col", file=sys.stderr)
        return 2
    blank_cols = ([c.strip() for c in args.blank_cols.split(",") if c.strip()] if args.blank_cols
                  else list(DEFAULT_BLANK)) + [c.strip() for c in args.also_blank.split(",") if c.strip()]
    path = args.check or args.input
    if not path:
        print("error: give an input file or --check FILE", file=sys.stderr)
        return 2
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            delim = sniff_delimiter(path)
            reader = csv.DictReader(fh, delimiter=delim)
            fields = reader.fieldnames or []
            rows = list(reader)
        for col in (args.lat_col, args.lon_col) + ((args.category_col,) if args.category_col else ()):
            if col not in fields:
                raise ValueError(f"column '{col}' not found")
        if args.check:
            violations = run_check(args, rows, blank_cols)
            print(json.dumps({"mode": "check", "file": path, "rows": len(rows),
                              "violations": violations, "gate": "fail" if violations else "pass"}, indent=2))
            return 3 if violations else 0
        if not args.out:
            raise ValueError("--out is required when generalizing")
        out_fields, out_rows, counts = run_generalize(args, fields, rows, blank_cols)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore", delimiter=delim)
        writer.writeheader()
        writer.writerows(out_rows)
    print(json.dumps({"mode": "generalize", "input": path, "output": args.out, "rows": len(rows),
                      **counts, "floor_degrees": None if args.allow_gbif_finer else FLOOR,
                      "next_step": f"run --check {args.out} before sharing"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
