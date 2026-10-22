"""Scenario results in absolute TP concentrations and OECD trophic classes.

Companion to kotokel_phosphorus.py (same model, same 27-combination grid).

Initial state: TP0 = 80 ug/L, the mean of 86 surface samples taken from May 2024
to March 2025 (range 20-360 ug/L, SD 50 ug/L; Shiretorova et al. 2025,
Limnology and Freshwater Biology, no. 4, pp. 1062-1082, Table 1).

Trophic classes by mean total phosphorus (OECD 1982, as cited by CCME 2004):
ultra-oligotrophic < 4; oligotrophic 4-10; mesotrophic 10-35; eutrophic 35-100;
hypertrophic > 100 ug/L.  The Russian fishery limit used in the same paper is
200 ug/L.

Prints, for each scenario, TP (ug/L) at 5, 10 and 50 yr (base and min-max over
the grid), how many of the 27 combinations exceed 100 ug/L (hypertrophic) or
fall to 35 ug/L or below (mesotrophic) at 50 yr, and the external-load cut
needed to reach 35 ug/L at 50 yr (alone, and after the one-off sediment
removal S3).

Standard library only.  Usage:  python trophic_classes.py
"""
import json

import kotokel_phosphorus as kp

HYPER, MESO = 100.0, 35.0  # ug/L, class boundaries


def tp_ugl(rel_percent):
    return kp.TP0 * (1.0 + rel_percent / 100.0)


def tp50(params, load_factor, sed_cut):
    out, _ = kp.simulate(*params, load_factor, sed_cut)
    return tp_ugl(out[50])


def load_cut_for(params, sed_cut, target=MESO):
    """Smallest external-load cut (%) giving TP <= target at 50 yr, or None."""
    if tp50(params, 0.0, sed_cut) > target:
        return None
    lo, hi = 0.0, 1.0  # load factor: lo reaches the target, hi does not
    for _ in range(14):
        mid = (lo + hi) / 2
        if tp50(params, mid, sed_cut) <= target:
            lo = mid
        else:
            hi = mid
    return 100.0 * (1.0 - lo)


def main():
    report = {}
    for name, (lf, cut) in kp.SCENARIOS.items():
        base, _ = kp.simulate(*kp.BASE, lf, cut)
        grid = [kp.simulate(*g, lf, cut)[0] for g in kp.GRID]
        row = {}
        for y in (5, 10, 50):
            vals = [tp_ugl(o[y]) for o in grid]
            row[f"{y} yr"] = {"base": round(tp_ugl(base[y]), 1),
                              "min": round(min(vals), 1), "max": round(max(vals), 1)}
        v50 = [tp_ugl(o[50]) for o in grid]
        row["n_above_100_at_50yr"] = sum(v > HYPER for v in v50)
        row["n_at_or_below_35_at_50yr"] = sum(v <= MESO for v in v50)
        report[name] = row

    need = {}
    for label, cut in (("load cut only", 0.0), ("after S3 (-50% mobile sediment P)", 0.5)):
        r = [load_cut_for(g, cut) for g in kp.GRID]
        ok = [x for x in r if x is not None]
        b = load_cut_for(kp.BASE, cut)
        need[label] = {"base_pct": None if b is None else round(b),
                       "min_pct": round(min(ok)), "max_pct": round(max(ok)),
                       "n_unreachable_even_at_zero_load": len(r) - len(ok)}
    report["external_load_cut_needed_for_35ugL_at_50yr"] = need
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
