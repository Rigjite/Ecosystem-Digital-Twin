#!/usr/bin/env python3
"""Gallery entry — forest fire: Prince Albert FMA fire seasons (synthetic).

Management question: are forest fires becoming more frequent or larger
in this landscape, and when does the fire season cross watch levels?

Data are SYNTHETIC — a teaching miniature. Every number below is invented
by deterministic formulas to the scale and pattern of the published
Canadian record; it is not a measurement and must never be cited
as data. Design anchors (NOT data):
- Canada 2023: 18,496,051 ha burned, the national record (CIFFC) —
  about 250% above the previous record (1995: 7,105,998 ha) and about
  8 times the national average of ~2.5 million ha/yr. 2025 passed
  7.5 million ha by mid-August (CIFFC).
- Saskatchewan 2023: 494 fires, about 1.9 million ha burned
  (Saskatchewan Public Safety Agency) — about five times the size of
  Prince Albert National Park (387,500 ha), and more than in 2015.
- The landscape is the Prince Albert Forest Management Agreement
  (PA FMA) area, Saskatchewan: 3,354,418 ha total, 2.7 million ha
  forested (Sakaw Askiy Management Inc., Forest Management Plan
  2018-2038). The miniature's seasons (65,400-128,830 ha) burn
  2.4-4.8% of the forested area each year — a small share of the
  provincial record — and its 2025 season (128,830 ha) is a new
  record, the endpoint of the rising trend.

Real data were checked first and found unusable for this miniature:
- NASA FIRMS Area API (the only route to a filtered multi-year series
  for a bounding box) requires a free MAP_KEY (registration); no key is
  available in this environment.
- FIRMS public NRT CSVs (VIIRS/MODIS, 24 h / 48 h / 7 d) are free and
  keyless, but they are global files covering only the last 7 days —
  too short for a trend and too large to filter by hand.
- FIRMS archive download and the yearly summary by country need a login
  code / interactive form; the summary is country-level only, not a
  landscape.
- GFED5 (NetCDF), Global Fire Atlas (shapefiles / GeoTIFF) and Copernicus
  Burnt Area (raster) are gridded products; extracting a series needs
  raster processing, outside the stdlib-only skill.
- No published annual fire series exists for the PA FMA itself; the
  provincial and national totals above are the anchors, not a series.

Formulas (no RNG): fire seasons April-October, 2019-2025 (49 months).
Monthly fire counts = base (Apr 2, May 8, Jun 7, Jul 9, Aug 10, Sep 5,
Oct 2) x year multiplier (2019: 1.25, 2020: 1.00, 2021: 1.30, 2022: 1.15,
2023: 1.20, 2024: 1.30, 2025: 1.45) + deterministic wobble
((year - 2019) + month_index + 1) % 3 - 1.
Monthly burned area = counts x mean fire size (Apr 400, May 2200,
Jun 1200, Jul 1800, Aug 2000, Sep 700, Oct 300 ha) x size multiplier
(2019: 1.20, 2020: 1.00, 2021: 1.05, 2022: 1.05, 2023: 1.10,
2024: 1.20, 2025: 1.30).

Run (from the skill root): python3 examples/gallery/forest-fire/run.py [--out DIR]
Prints the summary JSON to stdout; --out also writes the intermediates
and summary.json there. Standard library only.
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCRIPTS = os.path.join(ROOT, "scripts")
# Fire-count bands: declared watch levels for this miniature, amber 11
# sits below p90 of the 2019-2025 monthly window (13.0 fires/month);
# red 13 sits at p90/p95 (13.0 fires/month).
FIRES_AMBER = 11
FIRES_RED = 13
FIRES_ANCHOR = ("declared watch levels for this miniature, amber 11 sits "
                "below p90 of the 2019-2025 monthly window (13.0 "
                "fires/month); red 13 sits at p90/p95 (13.0 fires/month)")
# Burned-area bands: declared watch levels for this miniature; red is
# approximately p90 of the 2019-2025 monthly window (29,316 ha/month).
AREA_AMBER = 20000
AREA_RED = 30000
AREA_ANCHOR = ("declared watch levels for this miniature; red 30,000 "
               "ha/month is approximately p90 of the 2019-2025 monthly "
               "window (29,316 ha/month)")


def run(script, *args):
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, timeout=120)
    if res.returncode not in (0, 3):
        raise SystemExit(f"{script} failed ({res.returncode}): {res.stderr.strip()}")
    return res.returncode, json.loads(res.stdout)


def read_rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write intermediates and summary.json here")
    a = ap.parse_args()
    work = a.out or tempfile.mkdtemp(prefix="forest_fire_gallery_")
    os.makedirs(work, exist_ok=True)

    rows = read_rows(os.path.join(HERE, "fires.csv"))
    fires = [int(r["fires"]) for r in rows]
    area = [int(r["burned_ha"]) for r in rows]

    fires_csv = os.path.join(work, "fires.csv")
    write_csv(fires_csv, ["time", "value"],
              [[r["time"], r["fires"]] for r in rows])
    area_csv = os.path.join(work, "area.csv")
    write_csv(area_csv, ["time", "value"],
              [[r["time"], r["burned_ha"]] for r in rows])

    _, qc_fires = run("qc_series.py", fires_csv, "--min", "0")
    _, qc_area = run("qc_series.py", area_csv, "--min", "0")
    _, fires_trend = run("trend_test.py", "--seasonal", "month", fires_csv)
    _, area_trend = run("trend_test.py", "--seasonal", "month", area_csv)
    _, fires_alerts = run("alert_bands.py", "--indicator", "fires per month",
                          "--amber", f">={FIRES_AMBER}", "--red", f">={FIRES_RED}",
                          "--window-hours", "720", "--anchor", FIRES_ANCHOR,
                          "--human-check", "check the FIRMS detections and the forestry fire record",
                          fires_csv)
    _, area_alerts = run("alert_bands.py", "--indicator", "burned area, ha per month",
                         "--amber", f">={AREA_AMBER}", "--red", f">={AREA_RED}",
                         "--window-hours", "720", "--anchor", AREA_ANCHOR,
                         "--human-check", "check the FIRMS detections and the forestry fire record",
                         area_csv)
    fires_seg = fires_trend["segments"][0]
    area_seg = area_trend["segments"][0]
    annual = []
    for year in range(2019, 2026):
        ys = [r for r in rows if r["time"].startswith(str(year))]
        annual.append({"year": year,
                       "fires": sum(int(r["fires"]) for r in ys),
                       "burned_ha": sum(int(r["burned_ha"]) for r in ys)})
    biggest = max(annual, key=lambda y: y["burned_ha"])
    summary = {
        "entry": "forest-fire",
        "question": "Are forest fires becoming more frequent or larger in this landscape, and when does the fire season cross watch levels?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"fires_rows": qc_fires["rows"], "fires_flagged": qc_fires["rows_flagged"],
               "area_rows": qc_area["rows"], "area_flagged": qc_area["rows_flagged"]},
        "fires_trend": {"direction": fires_seg["direction"], "p_value": fires_seg["p_value"],
                        "sen_slope_per_year": fires_seg["sen_slope_per_year"]},
        "area_trend": {"direction": area_seg["direction"], "p_value": area_seg["p_value"],
                       "sen_slope_per_year": area_seg["sen_slope_per_year"]},
        "annual": annual,
        "biggest_season": biggest,
        "months_above_amber_fires": sum(1 for v in fires if v >= FIRES_AMBER),
        "months_above_red_fires": sum(1 for v in fires if v >= FIRES_RED),
        "months_above_amber_area": sum(1 for v in area if v >= AREA_AMBER),
        "months_above_red_area": sum(1 for v in area if v >= AREA_RED),
        "fires_alerts": {"status": fires_alerts["status"], "n_alerts": len(fires_alerts["alerts"]),
                         "amber": sum(1 for x in fires_alerts["alerts"] if x["band"] == "amber"),
                         "red": sum(1 for x in fires_alerts["alerts"] if x["band"] == "red")},
        "area_alerts": {"status": area_alerts["status"], "n_alerts": len(area_alerts["alerts"]),
                        "amber": sum(1 for x in area_alerts["alerts"] if x["band"] == "amber"),
                        "red": sum(1 for x in area_alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no measured fire series for this FMA (FIRMS Area API needs a MAP_KEY; public NRT files cover 7 days only; GFED/Global Fire Atlas/Copernicus are gridded products)",
                 "[НЕТ ДАННЫХ] no ignition causes (lightning vs human) in this miniature",
                 "[НЕТ ДАННЫХ] no fuel moisture or fire-weather series (the trend is counts and area only, not cause)",
                 "[НЕТ ДАННЫХ] no post-fire recovery series (burn-scar revegetation is not tracked here)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
