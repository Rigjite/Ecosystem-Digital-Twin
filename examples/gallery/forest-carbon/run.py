#!/usr/bin/env python3
"""Gallery entry — forest carbon: Prince Albert FMA carbon stock (synthetic).

Management question: how much carbon does this forest store and
accumulate, and is the stock growing or shrinking?

Data are SYNTHETIC — a teaching miniature. Every number below is invented
by deterministic formulas to the scale and pattern of the published
record for Canadian boreal forests; it is not a measurement and must
never be cited as data. Design anchors (NOT data):
- Boreal plant biomass: roughly 60-100 t C/ha, of which around 80% is
  in the above-ground biomass (Mahli et al. 1999; Luyssaert et al.
  2007, via UNEP) — so aboveground living biomass runs about 48-80
  t C/ha. The miniature's starting stock (52.0 t C/ha, 2015) sits at
  the low end of that range.
- Boreal sequestration: a single hectare of healthy boreal forest can
  sequester between 0.5 and 2 t C/yr (Alberta studies). The miniature's
  gross growth (+0.55 t C/ha/yr) sits at the low end of that range.
- The landscape is the Prince Albert Forest Management Agreement (PA
  FMA) area, Saskatchewan — the same landscape as the forest-fire
  entry, so the three forest entries share one landscape and consistent
  disturbance years. Total area 3,354,418 ha, 2.7 million ha forested
  (Sakaw Askiy Management Inc.); sustainable harvest rate recalculated
  to 1.92 million m3/yr after disturbance exceeded FMP thresholds.
- Fire losses use the forest-fire entry's annual burned areas for this
  same FMA (2019-2025: 101,400 / 65,400 / 90,405 / 83,265 / 87,230 /
  103,320 / 128,830 ha) and stated interpolation for 2015-2018
  (88,000 / 74,000 / 82,000 / 91,000 ha, rising toward 2019). Loss per
  year = burned share of the forested area x standing density x 0.20
  (the share of the standing carbon lost to combustion and post-fire
  mortality on burned ground — a stated assumption, not a measured
  factor).
- Canada 2023 burned 18,496,051 ha, the national record (CIFFC);
  Saskatchewan 2023 burned about 1.9 million ha in 494 fires
  (Saskatchewan Public Safety Agency). The miniature's seasons
  (65,400-128,830 ha) are a small share of the provincial record.

Real data were checked first and found unusable for this miniature:
- ESA CCI Biomass (global AGB maps, 100 m, annual 2007/2010/2015-2024,
  CC BY 4.0, DOI 10.5285/95913ffb6467447ca72c4e9d8cf30501) is a raster
  product (NetCDF/GeoTIFF); extracting a series needs raster
  processing, outside the stdlib-only skill — the same raster problem
  as the JRC and GFED products in the wetland and forest-fire entries.
- Global Forest Watch data API (the only route to an annual series for
  an administrative unit) requires a free API key (registration); the
  dashboard and map pages are JavaScript-driven — the same key problem
  as the forest-logging entry.
- US Forest Service FIA DataMart offers CSV downloads without login,
  but building a clean annual carbon-stock series means joining
  PLOT/TREE/COND tables across remeasurement cycles (heavy
  harmonisation), and it is US data — off-story for a Saskatchewan
  landscape.
- Canada's National Forest Inventory publishes national and provincial
  totals, not an open annual series for one forest management area.

HONEST BOUNDARY: this entry watches carbon stock and its change. It is
NOT a carbon-credit methodology and claims no compliance with any
credit standard (Verra, Gold Standard, or other). Credit accounting
has its own verification rules — additionality, permanence, leakage,
third-party verification — that this miniature does not implement.

Formulas (no RNG): annual rows, 2015-2025 (11 rows). Starting density
52.00 t C/ha (2015); each following year density = previous density
+ 0.55 (gross growth, at the low end of the published 0.5-2
sequestration range) - fire loss, where fire loss = burned_ha /
2,700,000 x density x 0.20. Total stock = density x 2,700,000 ha. Net
change is the year-to-year difference of the density series (plain
arithmetic in the runner).

Run (from the skill root): python3 examples/gallery/forest-carbon/run.py [--out DIR]
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
FOREST_HA = 2700000
# Net-change bands: declared watch levels for this miniature. Amber
# +0.15 t C/ha/yr is a year when growth nearly stalled — the fire loss
# ate almost all of the year's growth; red 0.0 t C/ha/yr is a year when
# the stock shrank. The density series rises through the window, so
# there is no low-density watch: the decision-relevant signal is the
# net change, not the level.
CHANGE_AMBER = 0.15
CHANGE_RED = 0.0
CHANGE_ANCHOR = ("declared watch levels for this miniature: amber "
                 "+0.15 t C/ha/yr is a year when growth nearly stalled "
                 "(the fire loss ate almost all of the year's growth); "
                 "red 0.0 t C/ha/yr is a year when the stock shrank")
HUMAN_CHECK = ("check the ESA CCI Biomass map and the National Forest "
               "Inventory carbon stock for this FMA; a rising stock with "
               "rising fire area points to growth still outpacing fire "
               "loss, not a measurement artefact")
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
    work = a.out or tempfile.mkdtemp(prefix="forest_carbon_gallery_")
    os.makedirs(work, exist_ok=True)

    rows = read_rows(os.path.join(HERE, "carbon.csv"))
    densities = [float(r["carbon_density_t_ha"]) for r in rows]
    years = [int(r["time"][:4]) for r in rows]

    density_csv = os.path.join(work, "density.csv")
    write_csv(density_csv, ["time", "value"],
              [[r["time"], v] for r, v in zip(rows, densities)])
    changes = [round(densities[i] - densities[i - 1], 2) for i in range(1, len(densities))]
    change_csv = os.path.join(work, "change.csv")
    write_csv(change_csv, ["time", "value"],
              [[rows[i]["time"], c] for i, c in enumerate(changes, start=1)])

    _, qc_density = run("qc_series.py", density_csv, "--min", "0")
    _, density_trend = run("trend_test.py", density_csv)
    _, change_trend = run("trend_test.py", change_csv)
    _, change_alerts = run("alert_bands.py", "--indicator", "net carbon change, t C per ha per year",
                           "--amber", f"<={CHANGE_AMBER:g}", "--red", f"<={CHANGE_RED:g}",
                           "--window-hours", str(WINDOW_HOURS), "--anchor", CHANGE_ANCHOR,
                           "--human-check", HUMAN_CHECK,
                           change_csv)
    density_seg = density_trend["segments"][0]
    change_seg = change_trend["segments"][0]
    annual = []
    for i, (r, v) in enumerate(zip(rows, densities)):
        annual.append({"year": years[i],
                       "carbon_density_t_ha": v,
                       "total_stock_mt_c": round(v * FOREST_HA / 1e6, 2),
                       "net_change_t_ha_yr": None if i == 0 else changes[i - 1]})
    start_stock = annual[0]["total_stock_mt_c"]
    end_stock = annual[-1]["total_stock_mt_c"]
    summary = {
        "entry": "forest-carbon",
        "question": "How much carbon does this forest store and accumulate, and is the stock growing or shrinking?",
        "data": "synthetic teaching miniature (deterministic formulas); must never be cited as data",
        "maturity": 2,
        "maturity_label": "Descriptive",
        "qc": {"density_rows": qc_density["rows"], "density_flagged": qc_density["rows_flagged"]},
        "density_trend": {"direction": density_seg["direction"], "p_value": density_seg["p_value"],
                          "sen_slope_per_year": density_seg["sen_slope_per_year"]},
        "change_trend": {"direction": change_seg["direction"], "p_value": change_seg["p_value"],
                         "sen_slope_per_year": change_seg["sen_slope_per_year"]},
        "annual": annual,
        "start_density_t_ha": densities[0],
        "end_density_t_ha": densities[-1],
        "start_stock_mt_c": start_stock,
        "end_stock_mt_c": end_stock,
        "stock_change_mt_c": round(end_stock - start_stock, 2),
        "stock_change_pct": round(100.0 * (end_stock - start_stock) / start_stock, 1),
        "years_below_amber_change": sum(1 for c in changes if c <= CHANGE_AMBER),
        "years_below_red_change": sum(1 for c in changes if c <= CHANGE_RED),
        "change_alerts": {"status": change_alerts["status"], "n_alerts": len(change_alerts["alerts"]),
                          "amber": sum(1 for x in change_alerts["alerts"] if x["band"] == "amber"),
                          "red": sum(1 for x in change_alerts["alerts"] if x["band"] == "red")},
        "gaps": ["[НЕТ ДАННЫХ] no measured carbon series for this FMA (ESA CCI Biomass is a raster product; GFW data API needs a key; FIA is US data and needs multi-table harmonisation; the National Forest Inventory publishes national and provincial totals, not an open annual series for one forest management area)",
                 "[НЕТ ДАННЫХ] no logging-removal term for this FMA (losses here are fire only; the forest-logging entry covers British Columbia timber supply areas)",
                 "[НЕТ ДАННЫХ] no soil carbon series (this miniature tracks living biomass carbon only)",
                 "[НЕТ ДАННЫХ] no belowground split (roots are inside the living-biomass total, not measured separately)",
                 "[НЕТ ДАННЫХ] this entry is not a carbon-credit methodology and claims no compliance with any credit standard (Verra, Gold Standard, or other)"],
    }
    if a.out:
        with open(os.path.join(work, "summary.json"), "w") as fh:
            json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
