#!/usr/bin/env python3
"""
Worked example — Beira Lake (Colombo, Sri Lanka), published data only.

What it shows, in the order of the skill's phases:
  1. State against declared thresholds (passport → indicators), with the
     sample spread kept visible instead of averaged away.
  2. A consistency check of the source itself (Gate B style): the published
     mean phosphorus index is compared with the published maximum.
  3. A decision question answered with arithmetic, not a model: can a
     constructed wetland alone take the lake out of the hypertrophic class?
  4. The value of information of a sludge analysis before choosing between
     safe disposal and use of processed sludge on fields (relative costs).
  5. The data gaps that stop this twin at maturity 2 (Descriptive).

Inputs are only published numbers, each with its source:
  [P24] Prasad S., Wei Y., Chaminda T. et al. Spatiotemporal assessment of
        water pollution for Beira Lake, Sri Lanka. Water 2024, 16(11), 1616.
        doi:10.3390/w16111616 — Table 1 (mean ± SD per season, 80 samples,
        2022–2023) and the class thresholds the authors use.
  [C77] Carlson R.E. A trophic state index for lakes. Limnology and
        Oceanography 1977, 22(2), 361–369. doi:10.4319/lo.1977.22.2.0361 —
        TSI(TP) = 14.42 ln(TP, µg/L) + 4.15.
  [L16] Land M. et al. How effective are created or restored freshwater
        wetlands for nitrogen and phosphorus removal? Environmental Evidence
        2016, 5, 9. doi:10.1186/s13750-016-0060-0 — median TP removal 46 %.
  [J05] Jeppesen E. et al. Freshwater Biology 2005, 50(10), 1747–1771.
        doi:10.1111/j.1365-2427.2005.01415.x — new in-lake TP equilibrium
        typically after 10–15 years of reduced loading.
  [P25] Perera K.A.B.P., Perera H.A.C.C. A comparative assessment of water
        pollution in Beira Lake and Ihalagama Lake. 29th International Forestry
        and Environment Symposium, University of Sri Jayewardenepura, 2025
        (abstract) — monthly samples Sep 2023 – Feb 2024, two sites: WPI 1.856.
  [D24] Dharmarathna D. et al. Assessment of pollution state of Beira Lake in
        Sri Lanka using water quality index, trophic status, and principal
        component analysis. Aquatic Ecology 2024, 58, 159–174.
        doi:10.1007/s10452-023-10052-8 — 39 grid sites: more than 93 % of the
        surface area in poor condition; hypereutrophic.
  [A26] Arachchi G.J.B. et al. Morphological and molecular characterization of
        microcystin-LR producing cyanobacteria in Beira and Boralesgamuwa lakes.
        2026. doi:10.31357/fesympo.v30.8999 — the toxin gene mcyA in every
        Beira sample; no toxin concentrations reported.
Nothing here comes from unpublished or company documents. Costs in step 4
are relative units (disposal = 1), not money.

Usage:  python3 beira_twin.py [--json]
Standard library only.
"""
import json
import math
import sys

# ---- 1. Published state (P24, Table 1): mean, SD per season ----------------
STATE = {
    "WPI":     {"dry": (2.53, 1.32),   "wet": (2.38, 0.92)},
    "TSI(TN)": {"dry": (88.61, 17.58), "wet": (99.07, 3.95)},
    "TSI(TP)": {"dry": (79.41, 7.61),  "wet": (129.09, 2.79)},
    "TSI(SD)": {"dry": (82.89, 4.11),  "wet": (77.64, 1.44)},
    "HPI":     {"dry": (38.37, 5.62),  "wet": (133.86, 2.55)},
}
# Thresholds as used by the authors (P24); anchor recorded for every band.
THRESHOLDS = {
    "WPI": [(1.0, "highly polluted")],
    "TSI(TN)": [(60.0, "eutrophic"), (80.0, "hypertrophic")],
    "TSI(TP)": [(60.0, "eutrophic"), (80.0, "hypertrophic")],
    "TSI(SD)": [(60.0, "eutrophic"), (80.0, "hypertrophic")],
    "HPI": [(100.0, "unsuitable for drinking")],
}
# Independent studies used as a cross-check of the state (not as calibration data)
CROSS_CHECK = [
    ("P25", "Sep 2023 – Feb 2024, 2 sites", "WPI 1.856", "highly polluted (WPI > 1)"),
    ("D24", "39 grid sites", "> 93 % of surface area in poor WQI condition", "hypereutrophic"),
    ("A26", "2026, triplicate surface samples", "mcyA toxin gene in all samples", "toxin-producing potential present"),
]
TP_WET_MIN_MG_L = 0.4    # P24: wet-season TP above 0.4 mg/L at every point
TP_WET_MAX_MG_L = 5.84   # P24: highest wet-season TP
WETLAND_TP_REMOVAL = 0.46  # L16: median


def tsi_tp(tp_ug_l):
    """Carlson (1977) trophic state index from total phosphorus, µg/L."""
    return 14.42 * math.log(tp_ug_l) + 4.15


def tp_from_tsi(tsi):
    """Inverse of tsi_tp, µg/L."""
    return math.exp((tsi - 4.15) / 14.42)


def classify(indicator, value):
    label = "below all thresholds"
    for limit, name in THRESHOLDS[indicator]:
        if value > limit:
            label = name
    return label


def step1_state():
    rows = []
    for ind, seasons in STATE.items():
        top = THRESHOLDS[ind][-1][0]
        for season, (mean, sd) in seasons.items():
            rows.append({
                "indicator": ind, "season": season, "mean": mean, "sd": sd,
                "class": classify(ind, mean),
                # spread check: does the mean ± 1 SD band sit entirely above the top threshold?
                "whole_band_above_top_threshold": mean - sd > top,
                "band_straddles_top_threshold": mean - sd <= top < mean + sd,
            })
    return rows


def step2_source_check():
    tp_at_mean = tp_from_tsi(STATE["TSI(TP)"]["wet"][0]) / 1000.0
    tsi_at_max = tsi_tp(TP_WET_MAX_MG_L * 1000.0)
    return {
        "wet_mean_TSI_TP": STATE["TSI(TP)"]["wet"][0],
        "TP_implied_by_mean_TSI_mg_L": round(tp_at_mean, 2),
        "TSI_of_reported_max_TP": round(tsi_at_max, 2),
        "finding": ("The mean wet-season TSI(TP) corresponds to the reported maximum TP. "
                    "The aggregation of station TSI values should be confirmed with the authors "
                    "before the mean is used as a calibration target (open question, not an error claim)."),
    }


def step3_wetland_alone():
    tp_hyper = tp_from_tsi(80.0)   # µg/L at the hypertrophic boundary
    tp_eutro = tp_from_tsi(60.0)
    out = {"TP_at_TSI80_ug_L": round(tp_hyper), "TP_at_TSI60_ug_L": round(tp_eutro), "cases": []}
    for name, tp_mg in (("least polluted point (0.4 mg/L)", TP_WET_MIN_MG_L),
                        ("most polluted point (5.84 mg/L)", TP_WET_MAX_MG_L)):
        tp = tp_mg * 1000.0
        after = tp * (1 - WETLAND_TP_REMOVAL)
        out["cases"].append({
            "case": name,
            "TSI_now": round(tsi_tp(tp), 1),
            "TSI_after_46pct_cut": round(tsi_tp(after), 1),
            "class_after": classify("TSI(TP)", tsi_tp(after)),
            "reduction_needed_to_leave_hypertrophic_pct": round(100 * (1 - tp_hyper / tp), 1),
        })
    out["assumption"] = ("Optimistic bound: in-lake TP falls in proportion to the external load cut. "
                         "Internal loading from sediments delays this; a new equilibrium typically "
                         "takes 10–15 years [J05].")
    return out


def step4_value_of_information(p_values=(0.2, 0.5, 0.8), c_values=(0.5, 0.8), l_values=(2.0, 5.0)):
    """Relative costs: safe disposal = 1. Field route costs c if the processed
    sludge complies; if it does not and is used anyway, add loss L.
    Without analysis choose min(1, c + (1-p)·L); with a perfect analysis
    choose per outcome. VOI is the expected saving, in disposal units."""
    table = []
    for p in p_values:
        for c in c_values:
            for loss in l_values:
                no_info = min(1.0, c + (1 - p) * loss)
                perfect = p * min(1.0, c) + (1 - p) * 1.0
                table.append({"p_compliant": p, "field_route_cost": c, "loss_if_noncompliant": loss,
                              "choice_without_analysis": "field" if c + (1 - p) * loss < 1.0 else "disposal",
                              "VOI_disposal_units": round(no_info - perfect, 3)})
    return table


GAPS = [
    "[НЕТ ДАННЫХ] sample count per season and station-level values (only seasonal mean ± SD are published)",
    "[НЕТ ДАННЫХ] sediment chemistry: metals, nutrients and microcystin in the sludge (published data describe the water column only)",
    "[НЕТ ДАННЫХ] external loads by inflow and outfall (needed to calibrate any load-response model)",
    "[НЕТ ДАННЫХ] microcystin concentrations: toxin genes confirmed in 2026 [A26], but the last published concentrations are from 2013–2014",
    "[НЕТ ДАННЫХ] costs of dredging, transport, disposal and processing (step 4 uses relative units)",
]


def main(argv):
    result = {"state": step1_state(), "cross_check": [dict(zip(("source", "design", "finding", "verdict"), c)) for c in CROSS_CHECK],
              "source_check": step2_source_check(),
              "wetland_alone": step3_wetland_alone(), "value_of_information": step4_value_of_information(),
              "gaps": GAPS, "maturity": "2 (Descriptive): no time series, no calibrated model, no registered forecast resolved"}
    if "--json" in argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print("1. STATE vs thresholds [P24]")
    for r in result["state"]:
        spread = ("whole ±SD band above top threshold" if r["whole_band_above_top_threshold"]
                  else "±SD band straddles top threshold" if r["band_straddles_top_threshold"] else "")
        print(f"   {r['indicator']:8} {r['season']:3}  {r['mean']:7.2f} ± {r['sd']:<6.2f} → {r['class']:24} {spread}")
    print("\n   Cross-check with independent studies:")
    for c in result["cross_check"]:
        print(f"   [{c['source']}] {c['design']}: {c['finding']} → {c['verdict']}")
    s = result["source_check"]
    print("\n2. SOURCE CHECK (Gate B style)")
    print(f"   mean wet TSI(TP) {s['wet_mean_TSI_TP']} ⇒ TP ≈ {s['TP_implied_by_mean_TSI_mg_L']} mg/L; "
          f"TSI of reported max 5.84 mg/L = {s['TSI_of_reported_max_TP']}")
    print(f"   {s['finding']}")
    w = result["wetland_alone"]
    print(f"\n3. CAN A WETLAND ALONE END HYPERTROPHY? (TSI 80 ⇔ TP {w['TP_at_TSI80_ug_L']} µg/L [C77])")
    for c in w["cases"]:
        print(f"   {c['case']:32} TSI {c['TSI_now']} → {c['TSI_after_46pct_cut']} ({c['class_after']}); "
              f"cut needed to leave hypertrophic: {c['reduction_needed_to_leave_hypertrophic_pct']} %")
    print(f"   Assumption: {w['assumption']}")
    print("\n4. VALUE OF A SLUDGE ANALYSIS (relative units, disposal = 1)")
    print("   p(compliant)  field cost  loss if not  choice w/o analysis  VOI")
    for v in result["value_of_information"]:
        print(f"   {v['p_compliant']:12} {v['field_route_cost']:11} {v['loss_if_noncompliant']:11}"
              f"  {v['choice_without_analysis']:19} {v['VOI_disposal_units']}")
    print("\n5. GAPS → maturity " + result["maturity"])
    for g in GAPS:
        print("   " + g)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
