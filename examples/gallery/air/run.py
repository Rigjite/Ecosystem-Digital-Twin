#!/usr/bin/env python3
"""Gallery entry — air basin: Prince George winter PM2.5 watch (synthetic).

Management question: how many days in the winter window exceed the WHO
2021 daily PM2.5 guideline (45 ug/m3), and when do smog episodes start?

Data are SYNTHETIC (deterministic formulas, no RNG): daily PM2.5,
2026-01-05..2026-02-28, three planted wood-smoke inversion episodes.
They are not measurements and must never be cited as data. Real data
were checked first: the CAMS model (Open-Meteo) for Prince George over
2026-01-05..2026-02-28 returns hourly values, but the model grid is too
coarse to resolve the valley inversion, so no model series was
substituted; the BC station network publishes 24-hour averages
(Prince George 33 ug/m3 on 2026-01-25, above the provincial objective
25 ug/m3), and the full hourly station series for the window was not
pulled into a CSV for this teaching build. The synthetic series shows
what the twin does once measurements exist.

Run (from the skill root): python3 examples/gallery/air/run.py [--out DIR]
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
AMBER = 45.0  # WHO 2021 daily guideline for PM2.5
RED = 75.0    # WHO 2021 interim target 1 (daily) for PM2.5


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
    work = a.out or tempfile.mkdtemp(prefix="air_gallery_")
    os.makedirs(work, exist_ok=True)
    data = os.path.join(HERE, "data.csv")
    with open(data, newline="") as fh:
        rows = list(csv.DictReader(fh))
    values = [float(r["value"]) for r in rows]

    _, qc = run("qc_series.py", data, "--min", "0", "--max", "500")
    _, trend = run("trend_test.py", data)
    _, alerts = run("alert_bands.py", "--indicator", "pm2.5",
                    "--amber", f">={AMBER:g}", "--red", f">={RED:g}",
                    "--window-hours", "24", "--anchor", "2026-02-28", data)
    seg = trend["segments"][0]
    summary = {
        "entry": "air",
        "question": "How many winter days exceed the WHO daily PM2.5 guideline, and when do smog episodes start?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"rows": qc["rows"], "rows_flagged": qc["rows_flagged"]},
        "pm25_trend": {"direction": seg["direction"], "p_value": seg["p_value"],
                       "sen_slope_per_year": seg["sen_slope_per_year"]},
        "days_above_amber": sum(1 for v in values if v >= AMBER),
        "days_above_red": sum(1 for v in values if v >= RED),
        "alerts": {"status": alerts["status"], "n_alerts": len(alerts["alerts"]),
                   "amber": sum(1 for x in alerts["alerts"] if x["band"] == "amber"),
                   "red": sum(1 for x in alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no hourly station series pulled for the window (BC network publishes 24-hour averages; Prince George 33 ug/m3 on 2026-01-25, above the provincial objective 25 ug/m3)",
                 "[НЕТ ДАННЫХ] no wind or inversion-height data (episode cause not attributed)",
                 "[НЕТ ДАННЫХ] one winter window only, no multi-year baseline"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
