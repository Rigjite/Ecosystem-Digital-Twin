#!/usr/bin/env python3
"""Gallery entry — pond: small-pond eutrophication miniature (synthetic).

Management question: will summer chlorophyll-a exceed the bathing advisory
watch levels, and is the eutrophication trend real?

Data are SYNTHETIC (deterministic formulas, no RNG): monthly total
phosphorus and chlorophyll-a, 2023-01..2025-12. They are not measurements
and must never be cited as data. The model form below is the form the
synthetic series were generated from, so the hold-out score is
near-perfect by construction — the entry demonstrates the workflow
(fit on declared training data, score on a declared hold-out, gate),
not a real model's skill.

Run (from the skill root): python3 examples/gallery/pond/run.py [--out DIR]
Prints the summary JSON to stdout; --out also writes the intermediates
and summary.json there. Standard library only.
"""
import argparse
import csv
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SCRIPTS = os.path.join(ROOT, "scripts")
TRAIN_END = "2024-12-31"  # declared before fitting; hold-out is 2025


def run(script, *args):
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, timeout=120)
    if res.returncode not in (0, 3):
        raise SystemExit(f"{script} failed ({res.returncode}): {res.stderr.strip()}")
    return res.returncode, json.loads(res.stdout)


def read_series(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def ols3(x_rows, y_values):
    """Least squares for y ~ 1 + x1 + x2 (3x3 normal equations)."""
    n = 3
    a = [[sum(r[i] * r[j] for r in x_rows) for j in range(n)] for i in range(n)]
    b = [sum(r[i] * y for r, y in zip(x_rows, y_values)) for i in range(n)]
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="write intermediates and summary.json here")
    a = ap.parse_args()
    work = a.out or tempfile.mkdtemp(prefix="pond_gallery_")
    os.makedirs(work, exist_ok=True)
    rows = read_series(os.path.join(HERE, "data.csv"))
    tp = [float(r["tp_ug_l"]) for r in rows]
    chl = [float(r["chl_ug_l"]) for r in rows]
    months = [int(r["time"][5:7]) for r in rows]

    chl_csv = os.path.join(work, "chl.csv")
    write_csv(chl_csv, ["time", "value"], [[r["time"], r["chl_ug_l"]] for r in rows])
    _, qc = run("qc_series.py", chl_csv, "--min", "0", "--max", "200")

    tp_csv = os.path.join(work, "tp.csv")
    write_csv(tp_csv, ["time", "value"], [[r["time"], r["tp_ug_l"]] for r in rows])
    _, trend = run("trend_test.py", tp_csv)

    tsi_json = os.path.join(work, "tsi.json")
    with open(tsi_json, "w") as fh:
        json.dump({"tp_ug_l": tp[-1], "chl_ug_l": chl[-1]}, fh)
    _, tsi = run("trend_test.py", "--mode", "tsi", tsi_json)

    # Model: chlorophyll ~ lagged TP + seasonal term, fitted on the declared
    # training period only (chl rows 1..23, i.e. 2023-02..2024-12).
    design, target = [], []
    for i in range(1, 24):
        design.append([1.0, tp[i - 1], math.sin(2 * math.pi * (months[i] - 6) / 12)])
        target.append(chl[i])
    beta = ols3(design, target)
    model_csv = os.path.join(work, "model.csv")
    with open(model_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["time", "obs", "sim"])
        for i, r in enumerate(rows):
            lag = tp[i - 1] if i > 0 else tp[0]
            sim = beta[0] + beta[1] * lag + beta[2] * math.sin(2 * math.pi * (months[i] - 6) / 12)
            w.writerow([r["time"], r["chl_ug_l"], round(sim, 1)])
    _, scores = run("skill_scores.py", "continuous", model_csv,
                    "--obs-col", "obs", "--sim-col", "sim",
                    "--train-end", TRAIN_END, "--thresholds", "NSE>=0.5")

    _, alerts = run("alert_bands.py", "--indicator", "chlorophyll-a",
                    "--amber", ">=40", "--red", ">=60", "--window-hours", "720",
                    "--anchor", "2026-01-01", chl_csv)
    seg = trend["segments"][0]
    summary = {
        "entry": "pond",
        "question": "Will summer chlorophyll-a exceed the bathing advisory watch levels?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 3,
        "maturity_label": "Informative",
        "qc": {"rows": qc["rows"], "rows_flagged": qc["rows_flagged"]},
        "tp_trend": {"direction": seg["direction"], "p_value": seg["p_value"],
                     "sen_slope_per_year": seg["sen_slope_per_year"]},
        "tsi_latest": {"tsi_composite": tsi["tsi_composite"], "class": tsi["class"]},
        "calibration": {"model": "chl ~ lagged TP + seasonal term (OLS, training data only)",
                        "gate": scores["gate"],
                        "admission_verdict": scores["admission_verdict"],
                        "ss_rmse": scores["ss_rmse"], "nse": scores["metrics"]["nse"]},
        "alerts": {"status": alerts["status"], "n_alerts": len(alerts["alerts"]),
                   "amber": sum(1 for x in alerts["alerts"] if x["band"] == "amber"),
                   "red": sum(1 for x in alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no winter under-ice oxygen data",
                 "[НЕТ ДАННЫХ] no sediment phosphorus release measurements",
                 "[НЕТ ДАННЫХ] no measured inflow discharge (load is not quantified)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
