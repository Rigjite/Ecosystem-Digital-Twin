#!/usr/bin/env python3
"""Gallery entry — wetland: Everglades treatment wetland + marsh (real data).

Management question: is the treatment wetland still removing nutrients,
and is the marsh drying?

Data are REAL, from two published streams of the Everglades wetland system
(South Florida, USA), different cells and different periods. The entry
demonstrates the twin's two watches on the streams the system actually
publishes; a synchronous single-object record is [НЕТ ДАННЫХ]:
- nutrients: monthly influent/effluent total phosphorus (TP, ug/L) of the
  Algal Turf Scrubber mobile pilot unit (MPU) at the STA-1W discharge
  canal (Stormwater Treatment Area 1 West, a constructed wetland),
  Aug 2008..Aug 2009, South Florida Water Management District, public
  document. The MPU floway (1 ft x 1200 ft, 20 gpm) ran without
  microfiltration in this series; the document's stated means are 35 and
  24 ug/L and the stated TP reduction 33.3%.
- level: daily gage height (ft NAVD88) at EDEN 10 in Water Conservation
  Area 3-B (USGS NWIS site 254707080370201), 2025-12-01..2026-03-31.
  USGS data are public domain. Values from 2025-12-19 are provisional
  (qualifier P); 2025-12-01..18 are approved (qualifier A).

Run (from the skill root): python3 examples/gallery/wetland/run.py [--out DIR]
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
# Outflow TP bands are the STA water-quality-based effluent limit (WQBEL,
# SFWMD): the annual flow-weighted mean outflow TP shall not exceed 13 ug/L
# in more than 3 out of 5 water years, and shall not exceed 19 ug/L in any
# water year. They are applied here as MONTHLY watch levels; a monthly
# breach is not itself a WQBEL violation.
TP_AMBER = 13.0
TP_RED = 19.0
TP_ANCHOR = ("STA WQBEL (SFWMD): annual flow-weighted mean outflow TP "
             "<=13 ug/L in 3 of 5 water years, <=19 ug/L in any water year; "
             "applied here as monthly watch levels")
# Level bands are the 10th and 5th percentiles of this 121-day window,
# rounded. They are watch levels for this miniature, not a regulatory
# standard.
LV_AMBER = 5.37
LV_RED = 5.33
LV_ANCHOR = ("p10/p5 of the 2025-12-01..2026-03-31 window at EDEN 10 "
             "(declared watch levels)")
# Reference from the skill's own Beira case (examples/beira/): the wetland
# measure there uses the median published TP removal of 46%.
BEIRA_REFERENCE_REMOVAL_PCT = 46.0


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


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write intermediates and summary.json here")
    a = ap.parse_args()
    work = a.out or tempfile.mkdtemp(prefix="wetland_gallery_")
    os.makedirs(work, exist_ok=True)

    nutrients = read_rows(os.path.join(HERE, "nutrients.csv"))
    tp_in = [float(r["tp_in_ug_l"]) for r in nutrients]
    tp_out = [float(r["tp_out_ug_l"]) for r in nutrients]
    removal = [(i - o) / i * 100.0 for i, o in zip(tp_in, tp_out)]

    tp_out_csv = os.path.join(work, "tp_out.csv")
    write_csv(tp_out_csv, ["time", "value"],
              [[r["time"], r["tp_out_ug_l"]] for r in nutrients])
    removal_csv = os.path.join(work, "removal.csv")
    write_csv(removal_csv, ["time", "value"],
              [[r["time"], f"{v:.1f}"] for r, v in zip(nutrients, removal)])
    level_csv = os.path.join(HERE, "level.csv")
    level_rows = read_rows(level_csv)
    level = [float(r["value"]) for r in level_rows]

    _, qc_tp = run("qc_series.py", tp_out_csv, "--min", "0")
    _, qc_lv = run("qc_series.py", level_csv, "--min", "0")
    _, rem_trend = run("trend_test.py", removal_csv)
    _, lv_trend = run("trend_test.py", level_csv)
    _, tp_alerts = run("alert_bands.py", "--indicator", "outflow TP, ug/L",
                       "--amber", f">={TP_AMBER:g}", "--red", f">={TP_RED:g}",
                       "--window-hours", "720", "--anchor", TP_ANCHOR,
                       "--human-check", "resample outflow and check the flow record",
                       tp_out_csv)
    _, lv_alerts = run("alert_bands.py", "--indicator", "gage height, ft NAVD88",
                       "--amber", f"<={LV_AMBER:g}", "--red", f"<={LV_RED:g}",
                       "--window-hours", "24", "--anchor", LV_ANCHOR,
                       "--human-check", "check the EDEN gage and the rainfall record",
                       level_csv)
    rem_seg = rem_trend["segments"][0]
    lv_seg = lv_trend["segments"][0]
    summary = {
        "entry": "wetland",
        "question": "Is the treatment wetland still removing nutrients, and is the marsh drying?",
        "data": ("real: SFWMD STA-1W ATS pilot monthly influent/effluent TP "
                 "2008-08..2009-08 (public document); USGS NWIS EDEN 10 "
                 "254707080370201 daily gage height 2025-12-01..2026-03-31 "
                 "(public domain)"),
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"tp_out_rows": qc_tp["rows"], "tp_out_flagged": qc_tp["rows_flagged"],
               "level_rows": qc_lv["rows"], "level_flagged": qc_lv["rows_flagged"]},
        "removal": {"n_months": len(removal),
                    "median_pct": round(median(removal), 1),
                    "mean_pct": round(sum(removal) / len(removal), 1),
                    "document_mean_pct": 33.3,
                    "beira_reference_median_pct": BEIRA_REFERENCE_REMOVAL_PCT},
        "removal_trend": {"direction": rem_seg["direction"], "p_value": rem_seg["p_value"],
                          "sen_slope_per_year": rem_seg["sen_slope_per_year"]},
        "level_trend": {"direction": lv_seg["direction"], "p_value": lv_seg["p_value"],
                        "sen_slope_per_year": lv_seg["sen_slope_per_year"]},
        "level_start_ft": level[0],
        "level_min_ft": min(level),
        "level_end_ft": level[-1],
        "days_below_amber": sum(1 for v in level if v <= LV_AMBER),
        "days_below_red": sum(1 for v in level if v <= LV_RED),
        "tp_alerts": {"status": tp_alerts["status"], "n_alerts": len(tp_alerts["alerts"]),
                      "amber": sum(1 for x in tp_alerts["alerts"] if x["band"] == "amber"),
                      "red": sum(1 for x in tp_alerts["alerts"] if x["band"] == "red")},
        "level_alerts": {"status": lv_alerts["status"], "n_alerts": len(lv_alerts["alerts"]),
                         "amber": sum(1 for x in lv_alerts["alerts"] if x["band"] == "amber"),
                         "red": sum(1 for x in lv_alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no synchronous single-object record (nutrient cell 2008-09, marsh gage 2025-26)",
                 "[НЕТ ДАННЫХ] no water extent series (JRC Global Surface Water is raster tiles / Explorer; extent needs raster processing, outside the stdlib-only skill)",
                 "[НЕТ ДАННЫХ] no inflow/outflow flows for the pilot (loads not quantified)",
                 "[НЕТ ДАННЫХ] no nitrogen series for this cell (TP only)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
