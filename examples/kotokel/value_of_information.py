"""Which unknown parameter drives the scenario uncertainty, and how much would
measuring the internal (sediment) phosphorus load narrow it?

Uses the same model and 27-combination grid as kotokel_phosphorus.py.
1) First-order variance shares of kr, vs, kb (full-factorial main effects).
2) R^2 of each scenario effect on the internal-load share, a quantity that a
   sediment-flux measurement determines.
3) Range of the effect when kr is known (each level) versus unknown.
Standard library only.
"""
import json
import statistics as st

from kotokel_phosphorus import GRID, SCENARIOS, internal_share, simulate

YEARS = (5, 10, 50)


def main():
    rows = {}
    for name, (lf, cut) in SCENARIOS.items():
        key = name.split()[0]
        res = {g: simulate(*g, lf, cut)[0] for g in GRID}
        out = {}
        for y in YEARS:
            ys = {g: res[g][y] for g in GRID}
            tot = st.pvariance(ys.values())
            shares = {}
            for i, p in enumerate(("kr", "vs", "kb")):
                levels = sorted({g[i] for g in GRID})
                means = [st.mean(v for g, v in ys.items() if g[i] == lv) for lv in levels]
                shares[p] = round(100 * st.pvariance(means) / tot)
            sh = [internal_share(*g) for g in GRID]
            vals = [ys[g] for g in GRID]
            r = st.correlation(sh, vals)
            full = max(vals) - min(vals)
            by_kr = []
            for lv in sorted({g[0] for g in GRID}):
                sub = [v for g, v in ys.items() if g[0] == lv]
                by_kr.append(max(sub) - min(sub))
            out[f"{y} yr"] = {
                "variance_share_pct": shares,
                "R2_on_internal_share_pct": round(100 * r * r),
                "range_pp_unknown": round(full, 1),
                "range_pp_kr_known_mean": round(st.mean(by_kr), 1),
                "range_reduction_pct": round(100 * (1 - st.mean(by_kr) / full)),
            }
        rows[key] = out
    print(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
