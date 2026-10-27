#!/usr/bin/env python3
"""Gallery entry — river reach: Potomac River at Little Falls (real data).

Management question: are high-flow days increasing in this reach, and when
does flow cross the declared watch levels?

Data are REAL: USGS National Water Information System, site 01646500
(Potomac River near Washington, DC, Little Falls pump station), parameter
00060 (discharge), daily values 2026-08-01..2026-10-20, converted from
ft3/s to m3/s (x 0.0283168). USGS data are public domain. Fetched
2026-10-26; values are provisional (qualifier P). No water chemistry was
fetched, so this entry has no WPI — that is a stated gap, not an omission.

Run (from the skill root): python3 examples/gallery/river/run.py [--out DIR]
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
# Declared watch levels: the 90th and 95th percentiles of this 81-day
# window, rounded. They are watch levels for this miniature, not a
# regulatory standard and not a flood stage.
AMBER = 155.0
RED = 280.0


def run(script, *args):
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, timeout=120)
    if res.returncode not in (0, 3):
        raise SystemExit(f"{script} failed ({res.returncode}): {res.stderr.strip()}")
    return res.returncode, json.loads(res.stdout)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write intermediates and summary.json here")
    a = ap.parse_args()
    work = a.out or tempfile.mkdtemp(prefix="river_gallery_")
    os.makedirs(work, exist_ok=True)
    data = os.path.join(HERE, "data.csv")
    with open(data, newline="") as fh:
        rows = list(csv.DictReader(fh))
    values = [float(r["value"]) for r in rows]

    _, qc = run("qc_series.py", data, "--min", "0")
    _, trend = run("trend_test.py", data)
    _, alerts = run("alert_bands.py", "--indicator", "flow",
                    "--amber", f">={AMBER:g}", "--red", f">={RED:g}",
                    "--window-hours", "24", "--anchor", "2026-10-20", data)
    seg = trend["segments"][0]
    summary = {
        "entry": "river",
        "question": "Are high-flow days increasing in this reach, and when does flow cross the watch levels?",
        "data": "real: USGS NWIS site 01646500, parameter 00060, daily discharge 2026-08-01..2026-10-20, public domain",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"rows": qc["rows"], "rows_flagged": qc["rows_flagged"]},
        "flow_trend": {"direction": seg["direction"], "p_value": seg["p_value"],
                       "sen_slope_per_year": seg["sen_slope_per_year"]},
        "flow_max_m3_s": max(values),
        "days_above_amber": sum(1 for v in values if v >= AMBER),
        "days_above_red": sum(1 for v in values if v >= RED),
        "alerts": {"status": alerts["status"], "n_alerts": len(alerts["alerts"]),
                   "amber": sum(1 for x in alerts["alerts"] if x["band"] == "amber"),
                   "red": sum(1 for x in alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no water chemistry for this reach (no WPI)",
                 "[НЕТ ДАННЫХ] 81 days is too short for a trend claim",
                 "[НЕТ ДАННЫХ] no rating curve to a flood stage"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
