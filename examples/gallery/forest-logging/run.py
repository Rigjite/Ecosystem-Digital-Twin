#!/usr/bin/env python3
"""Gallery entry — forest logging: British Columbia timber supply areas (synthetic).

Management question: where and how much forest is being lost to logging
in this landscape, and is the loss accelerating?

Data are SYNTHETIC — a teaching miniature. Every number below is invented
by deterministic formulas to the scale and pattern of the published
record for British Columbia; it is not a measurement and must never be
cited as data. Design anchors (NOT data):
- BC timber harvest: 38.9 million m3 (2023), 39.0 (2024), 37.7 (2025);
  Interior 26.9 million m3 in 2023 (BC Harvest Billing System, "2025
  Economic State of British Columbia's Forestry Sector"). The
  miniature's three-TSA total (3.4-6.4 million m3/yr) is a small share
  of the provincial harvest, as actual harvest runs well below the
  allowable cut.
- Prince George Timber Supply Area: allowable annual cut (AAC)
  12.5 million m3 (2011, reduced from a 14.9 peak; pre-beetle 9.3);
  base-case forecast initial harvest 10.1 million m3 for 10 years.
- Quesnel Timber Supply Area: AAC 4.0 million m3 (pre-beetle 2.34);
  mid-term timber supply projection 1.15 million m3/yr.
- Mackenzie Timber Supply Area: AACs cut 18.4% in 2024 to align
  harvest with the Chief Forester's May 2023 AAC determination.
- Minimum harvest volume 140 m3/ha (BC Mid-Term Timber Supply
  Project); the miniature's yields (192-210 m3/ha) sit above that
  merchantability threshold, as interior mature stands run higher.
The miniature covers three real BC timber supply areas (Prince George,
Quesnel, Mackenzie); its annual totals (17,900 ha in 2015 rising to
30,600 ha in 2025, harvest 3.4-6.4 million m3) echo the provincial
scale above without reproducing any measured series.

Real data were checked first and found unusable for this miniature:
- Global Forest Watch data API (the only route to an annual series for
  an administrative unit) requires a free API key (registration); no key
  is available in this environment.
- GFW dashboard and map pages are JavaScript-driven; the annual
  tree-cover-loss series is not in the fetchable page text.
- Hansen / GLAD gridded data are raster products; extracting a series
  needs raster processing, outside the stdlib-only skill.
- BC publishes harvest totals by region in the Economic State of the
  Forest Sector and the Harvest Billing System, not an open annual
  series by timber supply area; published aggregates give no clean
  annual series for three TSAs.

Formulas (no RNG): annual rows, 2015-2025 (11 rows). Logged area per
timber supply area rises with one shared dip in 2020 (slowdown year);
harvest volume = logged area x mean yield (192-210 m3/ha, deterministic
wobble), so volume follows area with its own texture.

Run (from the skill root): python3 examples/gallery/forest-logging/run.py [--out DIR]
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
DISTRICTS = ("prince_george_ha", "quesnel_ha", "mackenzie_ha")
DISTRICT_NAMES = {"prince_george_ha": "Prince George", "quesnel_ha": "Quesnel",
                  "mackenzie_ha": "Mackenzie"}
# Logged-area bands: declared watch levels for this miniature. Amber
# 24,500 ha/yr sits between the 2015-2021 maximum (23,800) and the 2022
# value (25,400); red 28,000 ha/yr sits between the 2023 value (26,900)
# and the 2024 value (28,700).
AREA_AMBER = 24500
AREA_RED = 28000
AREA_ANCHOR = ("declared watch levels for this miniature: amber 24,500 "
               "ha/yr sits between the 2015-2021 maximum (23,800 ha/yr) "
               "and the 2022 value (25,400 ha/yr); red 28,000 ha/yr sits "
               "between the 2023 value (26,900 ha/yr) and the 2024 value "
               "(28,700 ha/yr)")
# Harvest-volume bands: declared watch levels for this miniature. Amber
# 5.0 million m3/yr sits between the 2021 value (4.81) and the 2022
# value (5.21); red 5.7 million m3/yr sits between the 2023 value (5.35)
# and the 2024 value (5.94).
VOLUME_AMBER = 5000000
VOLUME_RED = 5700000
VOLUME_ANCHOR = ("declared watch levels for this miniature: amber "
                 "5.0 million m3/yr sits between the 2021 value (4.81) "
                 "and the 2022 value (5.21); red 5.7 million m3/yr sits "
                 "between the 2023 value (5.35) and the 2024 value (5.94)")
# Annual observations: a breach must be sustained for one year to alert.
WINDOW_HOURS = 8760


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
    work = a.out or tempfile.mkdtemp(prefix="forest_logging_gallery_")
    os.makedirs(work, exist_ok=True)

    rows = read_rows(os.path.join(HERE, "logging.csv"))
    totals = [sum(int(r[d]) for d in DISTRICTS) for r in rows]
    volumes = [int(r["harvest_m3"]) for r in rows]

    total_csv = os.path.join(work, "total.csv")
    write_csv(total_csv, ["time", "value"],
              [[r["time"], t] for r, t in zip(rows, totals)])
    volume_csv = os.path.join(work, "volume.csv")
    write_csv(volume_csv, ["time", "value"],
              [[r["time"], v] for r, v in zip(rows, volumes)])

    _, qc_area = run("qc_series.py", total_csv, "--min", "0")
    _, qc_volume = run("qc_series.py", volume_csv, "--min", "0")
    _, area_trend = run("trend_test.py", total_csv)
    _, volume_trend = run("trend_test.py", volume_csv)
    _, area_alerts = run("alert_bands.py", "--indicator", "logged area, ha per year",
                         "--amber", f">={AREA_AMBER}", "--red", f">={AREA_RED}",
                         "--window-hours", str(WINDOW_HOURS), "--anchor", AREA_ANCHOR,
                         "--human-check", "check the BC Harvest Billing System record and the GFW tree-cover-loss series for British Columbia",
                         total_csv)
    _, volume_alerts = run("alert_bands.py", "--indicator", "harvest volume, m3 per year",
                           "--amber", f">={VOLUME_AMBER}", "--red", f">={VOLUME_RED}",
                           "--window-hours", str(WINDOW_HOURS), "--anchor", VOLUME_ANCHOR,
                           "--human-check", "check the BC Harvest Billing System record and the GFW tree-cover-loss series for British Columbia",
                           volume_csv)
    area_seg = area_trend["segments"][0]
    volume_seg = volume_trend["segments"][0]
    annual = []
    for r, t in zip(rows, totals):
        annual.append({"year": int(r["time"][:4]),
                       "prince_george_ha": int(r["prince_george_ha"]),
                       "quesnel_ha": int(r["quesnel_ha"]),
                       "mackenzie_ha": int(r["mackenzie_ha"]),
                       "logged_ha": t,
                       "harvest_m3": int(r["harvest_m3"])})
    biggest = max(annual, key=lambda y: y["logged_ha"])
    district_totals = {d: sum(int(r[d]) for r in rows) for d in DISTRICTS}
    grand = sum(district_totals.values())
    shares = {DISTRICT_NAMES[d]: round(district_totals[d] / grand, 3)
              for d in DISTRICTS}
    largest = max(DISTRICT_NAMES.values(),
                  key=lambda n: shares[n])
    summary = {
        "entry": "forest-logging",
        "question": "Where and how much forest is being lost to logging in this landscape, and is the loss accelerating?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"area_rows": qc_area["rows"], "area_flagged": qc_area["rows_flagged"],
               "volume_rows": qc_volume["rows"], "volume_flagged": qc_volume["rows_flagged"]},
        "area_trend": {"direction": area_seg["direction"], "p_value": area_seg["p_value"],
                       "sen_slope_per_year": area_seg["sen_slope_per_year"]},
        "volume_trend": {"direction": volume_seg["direction"], "p_value": volume_seg["p_value"],
                         "sen_slope_per_year": volume_seg["sen_slope_per_year"]},
        "annual": annual,
        "biggest_year": biggest,
        "district_shares_2015_2025": shares,
        "largest_district": largest,
        "years_above_amber_area": sum(1 for v in totals if v >= AREA_AMBER),
        "years_above_red_area": sum(1 for v in totals if v >= AREA_RED),
        "years_above_amber_volume": sum(1 for v in volumes if v >= VOLUME_AMBER),
        "years_above_red_volume": sum(1 for v in volumes if v >= VOLUME_RED),
        "area_alerts": {"status": area_alerts["status"], "n_alerts": len(area_alerts["alerts"]),
                        "amber": sum(1 for x in area_alerts["alerts"] if x["band"] == "amber"),
                        "red": sum(1 for x in area_alerts["alerts"] if x["band"] == "red")},
        "volume_alerts": {"status": volume_alerts["status"], "n_alerts": len(volume_alerts["alerts"]),
                          "amber": sum(1 for x in volume_alerts["alerts"] if x["band"] == "amber"),
                          "red": sum(1 for x in volume_alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no measured logging series for these timber supply areas (GFW data API needs a key; dashboard and map pages are JavaScript-driven; Hansen/GLAD rasters need raster processing; BC publishes regional harvest totals, not an open annual series by timber supply area)",
                 "[НЕТ ДАННЫХ] no split of loss by driver in this miniature (the GFW total-loss anchors mix logging, fire, and other disturbances; the miniature's series is logging only, by design)",
                 "[НЕТ ДАННЫХ] no regeneration or reforestation series (net change is not tracked here)",
                 "[НЕТ ДАННЫХ] no illegal-logging estimate (official harvest only, by design)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
