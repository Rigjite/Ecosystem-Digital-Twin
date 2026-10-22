"""The update step of the Lake Kotokel twin: a new measurement prunes the
ensemble of parameter combinations and narrows the scenario forecast.

Same model and 27-combination grid as kotokel_phosphorus.py.

Procedure (rejection of incompatible ensemble members):
  each of the 27 combinations is taken in turn as the "true" lake;
  a sediment-flux campaign measures its internal-load share with an error of
  +/- TOL percentage points; every combination whose internal-load share differs
  from the measured one by more than TOL is rejected; the scenario forecast is
  recomputed from the members that remain.
Reported: median number of remaining members and median width (max - min,
percentage points of initial TP) of each scenario forecast, before and after
the update, at 5, 10 and 50 yr.

Also checks why routine TP monitoring alone does not update this twin: with an
unchanged load every member stays at the measured initial TP, so TP
observations cannot tell the members apart.

Standard library only.  Usage:  python twin_update.py
"""
import json
import statistics as st

from kotokel_phosphorus import GRID, SCENARIOS, internal_share, simulate

YEARS = (5, 10, 50)
TOLS = (5, 10, 15)  # measurement error of the internal-load share, p.p.


def main():
    share = {g: 100 * internal_share(*g) for g in GRID}
    res = {name.split()[0]: {g: simulate(*g, lf, cut)[0] for g in GRID}
           for name, (lf, cut) in SCENARIOS.items()}

    report = {}
    for tol in TOLS:
        kept_n = []
        widths = {s: {y: [] for y in YEARS} for s in res}
        for truth in GRID:
            kept = [g for g in GRID if abs(share[g] - share[truth]) <= tol]
            kept_n.append(len(kept))
            for s in res:
                for y in YEARS:
                    v = [res[s][g][y] for g in kept]
                    widths[s][y].append(max(v) - min(v))
        block = {"median_members_kept_of_27": st.median(kept_n)}
        for s in res:
            row = {}
            for y in YEARS:
                full = max(res[s][g][y] for g in GRID) - min(res[s][g][y] for g in GRID)
                after = st.median(widths[s][y])
                row[f"{y} yr"] = {"width_before_pp": round(full, 1),
                                  "width_after_pp_median": round(after, 1),
                                  "narrowing_pct": round(100 * (1 - after / full))}
            block[s] = row
        report[f"tolerance +/-{tol} p.p."] = block

    # routine monitoring under unchanged load: does TP differ between members?
    s0 = [simulate(*g, 1.0, 0.0)[0] for g in GRID]
    spread = max(max(abs(o[y]) for y in YEARS) for o in s0)
    report["no-measures run: max |TP change| over members, %"] = round(spread, 6)
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
