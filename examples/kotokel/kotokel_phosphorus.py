"""Scenario analysis for a water body with the morphometry of Lake Kotokel.

Reproduces Table 2 of Baldanova & Suzuki (2026), "Ecosystem digital twins as a
tool for forecasting and prior assessment of anthropogenic impacts".

Two-compartment total-phosphorus (TP) balance, simplified from Chapra & Canale
(1991), Water Research 25(6): 707-715:

    dPw/dt = L + kr*Ps - (vs/z)*Pw - Pw/tau
    dPs/dt = (vs/z)*Pw - (kr + kb)*Ps

Pw - TP mass in the water column, t; Ps - mobile P pool of the upper sediment, t.
This is an ILLUSTRATIVE scenario model, not a calibrated forecast: the initial
TP is measured (80 ug/L), but internal loading of Lake Kotokel has not been
measured and no TP time series exists, so vs, kb and kr are assumed and explored
over a 27-combination grid. For each combination the external load is
set so that the initial equilibrium gives the same TP concentration; because the
model is linear, results are reported as % change from that initial level.

Standard library only (Python 3.9+). Usage:  python kotokel_phosphorus.py
"""
import itertools
import json

AREA = 68.9e6   # m2, Shiretorova et al. 2025, Water 17(4): 545
ZMEAN = 3.5     # m, Semernoy et al. 2010
TAU = 6.0       # yr, nominal water renewal time, Shiretorova et al. 2025
TP0 = 80.0      # ug/L, mean TP of 86 surface samples, May 2024 - Mar 2025
                # (Shiretorova et al. 2025, Limnol. Freshw. Biol. 4: 1062-1082, Table 1);
                # results here are relative, so it only sets the absolute scale
V = AREA * ZMEAN

BASE = (0.10, 10.0, 0.03)  # kr (1/yr), vs (m/yr), kb (1/yr)
GRID = list(itertools.product([0.05, 0.10, 0.20], [5.0, 10.0, 20.0], [0.01, 0.03, 0.05]))

# scenario: (external-load factor, one-off fraction of mobile sediment P removed)
SCENARIOS = {
    "S1 shore development without treatment (+30% external load)": (1.30, 0.0),
    "S2 wetlands on inflows (-46% external load; Land et al. 2016 median)": (0.54, 0.0),
    "S3 one-off sediment remediation (-50% mobile sediment P)": (1.00, 0.5),
    "S4 S2 + S3 combined": (0.54, 0.5),
}
HORIZONS = (3, 5, 10, 50)


def simulate(kr, vs, kb, load_factor, sed_cut, years=50.0, dt=0.002):
    """Return {year: % change of TP} and the trajectory [(t, %), ...]."""
    sig, rho = vs / ZMEAN, 1.0 / TAU
    pw = TP0 * 1e-9 * V                       # t
    ps = sig * pw / (kr + kb)                 # equilibrium sediment pool
    load0 = pw * (rho + sig * kb / (kr + kb))  # external load giving that equilibrium
    ps *= 1.0 - sed_cut
    load = load0 * load_factor
    out, traj = {}, []
    for i in range(1, int(round(years / dt)) + 1):
        dpw = load + kr * ps - sig * pw - rho * pw
        dps = sig * pw - (kr + kb) * ps
        pw += dpw * dt
        ps += dps * dt
        t = i * dt
        rel = pw / V * 1e9 / TP0 * 100.0 - 100.0
        traj.append((t, rel))
        for y in HORIZONS:
            if abs(t - y) < dt / 2:
                out[y] = rel
    return out, traj


def internal_share(kr, vs, kb):
    sig, rho = vs / ZMEAN, 1.0 / TAU
    pw = TP0 * 1e-9 * V
    ps = sig * pw / (kr + kb)
    load0 = pw * (rho + sig * kb / (kr + kb))
    return kr * ps / (kr * ps + load0)


def main():
    report = {"internal_share_pct": [round(100 * min(internal_share(*g) for g in GRID)),
                                     round(100 * max(internal_share(*g) for g in GRID))]}
    for name, (lf, cut) in SCENARIOS.items():
        base, traj = simulate(*BASE, lf, cut)
        grid = [simulate(*g, lf, cut) for g in GRID]
        row = {}
        for y in HORIZONS:
            vals = [o[y] for o, _ in grid]
            row[f"{y} yr"] = {"base": round(base[y]), "min": round(min(vals)), "max": round(max(vals))}
        if lf > 1:
            # time to half of the change reached at 50 yr, and share of it present at 3 yr
            t50 = [next(t for t, r in tr if r >= tr[-1][1] / 2) for _, tr in grid]
            share3 = [o[3] / tr[-1][1] for o, tr in grid]
            row["t50_yr"] = {"base": round(next(t for t, r in traj if r >= traj[-1][1] / 2), 1),
                             "min": round(min(t50), 1), "max": round(max(t50), 1)}
            row["share_of_50yr_change_at_3yr_pct"] = {"base": round(100 * base[3] / traj[-1][1]),
                                                      "min": round(100 * min(share3)),
                                                      "max": round(100 * max(share3))}
        report[name] = row
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
