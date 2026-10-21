#!/usr/bin/env python3
"""
Reproduces the open-series demonstration of the computational core
(Nile flow at Aswan 1871-1970; Lake Huron level 1875-1972; Mauna Loa CO2
1958-2001). The skill's scripts need only the standard library; this demo
also needs `statsmodels` (pip install statsmodels) to fetch the three public
datasets, and network access for the Lake Huron series (Rdatasets).

Usage (from the skill root):
    python3 examples/open_series_demo.py --out demo_out

Writes the input CSVs, every script's JSON output, and summary.json with the
numbers reported in examples/open-series-demo.md.
"""

import argparse
import csv
import json
import os
import statistics as st
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
FT = 0.3048  # metres per foot


def run(out, script, *args):
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, timeout=600)
    if res.returncode not in (0, 3):
        raise SystemExit(f"{script} failed ({res.returncode}): {res.stderr.strip()}")
    data = json.loads(res.stdout)
    data["_exit_code"] = res.returncode
    return data


def write_series(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["time", "value"])
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="demo_out")
    a = ap.parse_args()
    try:
        import statsmodels.api as sm
        from statsmodels.datasets import co2, nile
    except ImportError:
        raise SystemExit("this demo needs statsmodels: pip install statsmodels")
    os.makedirs(a.out, exist_ok=True)
    p = lambda name: os.path.join(a.out, name)

    n = nile.load_pandas().data
    write_series(p("nile.csv"), [[f"{int(y)}-07-01", v] for y, v in zip(n.year, n.volume)])
    lh = sm.datasets.get_rdataset("LakeHuron").data
    huron = [(int(y), float(v)) for y, v in zip(lh.time, lh.value)]
    write_series(p("huron.csv"), [[f"{y}-07-01", v] for y, v in huron])
    c = co2.load_pandas().data
    write_series(p("co2.csv"), [[t.date().isoformat(), "" if v != v else v] for t, v in zip(c.index, c.co2)])

    r = {}
    r["nile_qc"] = run(a.out, "qc_series.py", p("nile.csv"), "--min", "0", "--max", "3000")
    r["nile_trend_whole"] = run(a.out, "trend_test.py", p("nile.csv"))
    r["nile_trend_split"] = run(a.out, "trend_test.py", p("nile.csv"), "--breaks", "1899-01-01")
    r["huron_qc"] = run(a.out, "qc_series.py", p("huron.csv"), "--min", "570", "--max", "590")
    for mode in ("hamed-rao", "none", "tfpw"):
        r[f"huron_trend_{mode}"] = run(a.out, "trend_test.py", p("huron.csv"), "--autocorr", mode)

    train = [(y, v) for y, v in huron if y <= 1950]
    xs, ys = [y for y, _ in train], [v for _, v in train]
    mx, my = st.mean(xs), st.mean(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    icpt = my - slope * mx
    dev = [v - my for v in ys]
    phi = sum(dev[i] * dev[i - 1] for i in range(1, len(dev))) / sum(d * d for d in dev[:-1])
    models = {"trend": lambda y, prev: icpt + slope * y, "ar1": lambda y, prev: my + phi * (prev - my)}
    for name, f in models.items():
        with open(p(f"huron_{name}.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["time", "obs", "sim"])
            prev = None
            for y, v in huron:
                w.writerow([f"{y}-07-01", v, "" if prev is None else round(f(y, prev), 4)])
                prev = v
    r["huron_skill_trend"] = run(a.out, "skill_scores.py", "continuous", p("huron_trend.csv"), "--train-end",
                                 "1950-12-31", "--season", "none", "--persistence", "fixed", "--thresholds", "NSE>=0.5")
    r["huron_skill_ar1"] = run(a.out, "skill_scores.py", "continuous", p("huron_ar1.csv"), "--train-end",
                               "1950-12-31", "--season", "none", "--persistence", "rolling", "--thresholds", "NSE>=0.5")
    r["co2_qc"] = run(a.out, "qc_series.py", p("co2.csv"), "--min", "300", "--max", "400", "--max-rate", "0.2",
                      "--max-gap-hours", "192")
    r["co2_trend"] = run(a.out, "trend_test.py", p("co2.csv"), "--seasonal", "month")
    r["co2_trend_decades"] = run(a.out, "trend_test.py", p("co2.csv"), "--seasonal", "month", "--breaks",
                                 "1970-01-01,1980-01-01,1990-01-01")
    for key, val in r.items():
        with open(p(f"{key}.json"), "w", encoding="utf-8") as fh:
            json.dump(val, fh, indent=2)

    seg = lambda k, i=0: r[k]["segments"][i]
    nile_vals = [(int(row[0][:4]), float(row[1])) for row in csv.reader(open(p("nile.csv"))) if row[0] != "time"]
    before = st.mean(v for y, v in nile_vals if y <= 1898)
    after = st.mean(v for y, v in nile_vals if y >= 1899)
    hr = seg("huron_trend_hamed-rao")
    summary = {
        "nile": {"pettitt_last_before_break": r["nile_qc"]["change_point"]["last_value_before_break"],
                 "mean_before": round(before, 1), "mean_after": round(after, 1),
                 "drop_percent": round(100 * (1 - after / before), 1),
                 "whole_Z": round(seg("nile_trend_whole")["Z"], 2), "whole_p": round(seg("nile_trend_whole")["p_value"], 4),
                 "whole_sen": round(seg("nile_trend_whole")["sen_slope_per_year"], 2),
                 "segment_p": [round(s["p_value"], 2) for s in r["nile_trend_split"]["segments"]]},
        "huron": {"pettitt_last_before_break": r["huron_qc"]["change_point"]["last_value_before_break"],
                  "lag1_r": round(hr["lag1_autocorrelation_detrended"], 2),
                  "Z_none_tfpw_hamedrao": [round(seg(f"huron_trend_{m}")["Z"], 2) for m in ("none", "tfpw", "hamed-rao")],
                  "n_over_neff": round(hr["variance_factor_n_over_n_eff"], 2),
                  "sen_mm_per_year": round(hr["sen_slope_per_year"] * FT * 1000, 1),
                  "sen_ci_mm_per_year": [round(x * FT * 1000, 1) for x in hr["slope_ci"]],
                  "train_slope_mm_per_year": round(slope * FT * 1000, 1), "ar1_phi": round(phi, 3)},
        "co2": {"rows": r["co2_qc"]["rows"], "missing": r["co2_qc"]["flag_counts"].get("missing", 0),
                "seasonal_kendall_ppm_per_year": round(seg("co2_trend")["sen_slope_per_year"], 3),
                "ci": [round(x, 3) for x in seg("co2_trend")["slope_ci"]],
                "by_decade": [round(s["sen_slope_per_year"], 2) for s in r["co2_trend_decades"]["segments"]],
                "pettitt_last_before_break": r["co2_qc"]["change_point"]["last_value_before_break"]},
    }
    for name in ("trend", "ar1"):
        m = r[f"huron_skill_{name}"]["metrics"]
        summary["huron"][f"forecast_{name}"] = {
            "gate": r[f"huron_skill_{name}"]["gate"], "nse": round(m["nse"], 2), "kge": round(m["kge"], 2),
            "rmse_m": round(m["rmse"] * FT, 2), "bias_m": round(m["bias"] * FT, 2),
            "ss_persistence": round(m["skill_vs_persistence"], 2), "ss_climatology": round(m["skill_vs_climatology"], 2)}
    with open(p("summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
