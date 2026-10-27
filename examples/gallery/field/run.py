#!/usr/bin/env python3
"""Gallery entry — agricultural field: soil-moisture watch (synthetic).

Management question: is the field drying toward the irrigation trigger,
and when does soil moisture cross the declared watch levels?

Data are SYNTHETIC (deterministic formulas, no RNG): daily soil moisture
(%), 2026-04-01..2026-06-29, a drying trend with three rain events that
wet the soil and drain exponentially. They are not measurements and must
never be cited as data. The watch levels are declared for this miniature
(loam, cereal crop), not measured field capacity or wilting point.

Run (from the skill root): python3 examples/gallery/field/run.py [--out DIR]
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
AMBER = 18.0  # declared watch level: irrigation should be planned
RED = 12.0    # declared watch level: crop water stress


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
    work = a.out or tempfile.mkdtemp(prefix="field_gallery_")
    os.makedirs(work, exist_ok=True)
    data = os.path.join(HERE, "data.csv")
    with open(data, newline="") as fh:
        rows = list(csv.DictReader(fh))
    values = [float(r["value"]) for r in rows]

    _, qc = run("qc_series.py", data, "--min", "0", "--max", "60")
    _, trend = run("trend_test.py", data)
    _, alerts = run("alert_bands.py", "--indicator", "soil-moisture",
                    "--amber", f"<{AMBER:g}", "--red", f"<{RED:g}",
                    "--window-hours", "24", "--anchor", "2026-06-29", data)
    seg = trend["segments"][0]
    _, pft = run("diversity.py", "pft", os.path.join(HERE, "pft_cover.csv"),
                 "--pft-table", os.path.join(HERE, "pft_table.csv"))
    summary = {
        "entry": "field",
        "question": "Is the field drying toward the irrigation trigger?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"rows": qc["rows"], "rows_flagged": qc["rows_flagged"]},
        "moisture_trend": {"direction": seg["direction"], "p_value": seg["p_value"],
                           "sen_slope_per_year": seg["sen_slope_per_year"]},
        "days_below_amber": sum(1 for v in values if v < AMBER),
        "days_below_red": sum(1 for v in values if v < RED),
        "pft_shares": {"by_pft": pft["shares_by_pft"],
                       "by_pathway": pft["shares_by_pathway"],
                       "note": "one season: shares only, no trend (a trend needs repeat surveys)"},
        "alerts": {"status": alerts["status"], "n_alerts": len(alerts["alerts"]),
                   "amber": sum(1 for x in alerts["alerts"] if x["band"] == "amber"),
                   "red": sum(1 for x in alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no measured field capacity or wilting point",
                 "[НЕТ ДАННЫХ] no rain gauge (rainfall is part of the synthetic design)",
                 "[НЕТ ДАННЫХ] one season only, no multi-year baseline"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
