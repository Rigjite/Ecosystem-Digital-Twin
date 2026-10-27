#!/usr/bin/env python3
"""
Append-only forecast registry (Phases 3-4, ecosystem-digital-twin skill).

Predictive claims are earned in advance: a forecast counts only if it was
registered before its outcome could be known, and it is scored exactly as
registered. The registry is a JSON-lines file in which every record carries
the SHA-256 hash of the previous record, so any later edit, deletion, or
reordering is detectable with `verify`. The issue time is always the clock
time of registration (no back-dating option). The chain proves that nothing
was edited later; to prove *when* it was written, anchor the latest hash
outside the build (a git commit, or an email to the owner) at each issue.
A forecast record also carries its refresh cadence (daily, weekly,
seasonal, or event-driven) and the usable warning lead time for the
decision (lead_time value + unit); both are validated on issue and on
verify. Records issued before v2.4 carry neither field and still verify.

Commands:
  issue    register a forecast. Refused if the id exists, if the horizon end
           is not after the issue time, if no input manifest ids are given,
           or if values are malformed. --supersedes OLD registers a correction
           as a new record; the old forecast stays in the registry and in
           the scores. Optional --cadence and --lead-time (with
           --lead-time-unit, default days) record the refresh rhythm and
           the usable warning lead time for the decision.
  resolve  record the observed outcome as a new record. Refused before the
           horizon closes, except a probability forecast whose event has
           already occurred (outcome 1). A second outcome for the same id
           needs --amend-reason and is shown as an amendment.
  replay   record a historical-event replay: the pipeline run on the data
           up to a past extreme, with whether and when the alert fired.
           Refused if the data cutoff is after the event date, if an alert
           that fired has no lead time, or if a miss claims one. A replay
           is a verification, not a forecast: it is hash-chained like every
           record, but it is never scored and carries no decision weight
           for a future event.
  promote  record a promotion: a model moves from exploratory to
           operational, signed — promoted by (name/role), on (the
           registration clock), evidence (benchmark + hold-out score). A
           model without a promotion record is exploratory by rule; its
           outputs are never presented as operational. Promotions are
           hash-chained like every record, but never scored.
  verify   recompute the hash chain; exit 3 if any record was altered.
  score    score every registered forecast as issued: Brier score for
           probabilities, absolute error and interval coverage for
           quantities. Superseded forecasts are scored too (a correction
           cannot remove a miss). Forecasts past their horizon without an
           outcome are listed as overdue; trial forecasts are reported apart.

Usage:
  python3 registry.py issue --registry reg.jsonl --id LP-F-001 --kind quantity \
      --target "Jul-Aug mean chlorophyll-a, deep station (mg/m3)" --value 18 \
      --lower 11 --upper 27 --horizon-end 2027-08-31 --model "TP-lag regression" \
      --model-version 0.2 --inputs ds-03,ds-05 --metric abs_error --trial \
      --cadence seasonal --lead-time 90 --lead-time-unit days
  python3 registry.py resolve --registry reg.jsonl --id LP-F-001 --outcome 21.4
  python3 registry.py promote --registry reg.jsonl --id PROM-001 --model "TP-lag regression" \
      --model-version 0.2 --promoted-by "R. Baldanova (lead modeler)" \
      --evidence "SS_RMSE 0.42 on hold-out 2026-01..06; alert trial PASS"
  python3 registry.py verify --registry reg.jsonl
  python3 registry.py score --registry reg.jsonl

score caps its per-forecast, overdue and pending lists with --max-items
(default 25; totals always reported) and writes the full record with
--full-json FILE.
"""

import argparse
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone

GENESIS = "0" * 64


CLOCK_ENV = "ECO_TWIN_CLOCK"  # test and replay clock only; every record notes when it was used


CADENCES = ("daily", "weekly", "seasonal", "event-driven")
LEAD_TIME_UNITS = ("hours", "days", "weeks")


def now_utc():
    override = os.environ.get(CLOCK_ENV)
    if override:
        return parse_time(override)
    return datetime.now(timezone.utc)


def clock_source():
    return "override" if os.environ.get(CLOCK_ENV) else "system"


def parse_time(text, end_of_day=False):
    t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    if len(text.strip()) == 10 and end_of_day:
        t = t.replace(hour=23, minute=59, second=59)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def digest(record):
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def append(path, record, records):
    record["prev_hash"] = records[-1]["hash"] if records else GENESIS
    record["hash"] = digest(record)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record


def cap(summary, key, max_items):
    """Keep at most max_items of summary[key]; record the total and whether it was cut."""
    items = summary.get(key) or []
    summary[key + "_total"] = len(items)
    summary[key + "_truncated"] = len(items) > max_items
    summary[key] = items[:max_items]


def forecasts(records):
    return {r["id"]: r for r in records if r.get("type") == "forecast"}


def validate_forecast_fields(record):
    """Validate the v2.4 forecast fields of one registry record.

    Returns an error string, or None. Records issued before v2.4 carry
    neither field and always pass: absence is not an error.
    """
    cadence = record.get("cadence")
    if cadence is not None and cadence not in CADENCES:
        return f"cadence '{cadence}' is not one of {', '.join(CADENCES)}"
    lead = record.get("lead_time")
    if lead is not None:
        if not isinstance(lead, dict):
            return "lead_time must be an object with value and unit"
        value, unit = lead.get("value"), lead.get("unit")
        if (not isinstance(value, (int, float)) or isinstance(value, bool)
                or not math.isfinite(value) or value <= 0):
            return "lead_time.value must be a positive number"
        if unit not in LEAD_TIME_UNITS:
            return f"lead_time.unit '{unit}' is not one of {', '.join(LEAD_TIME_UNITS)}"
    clearance = record.get("clearance")
    if clearance is not None:
        if not isinstance(clearance, list):
            return "clearance must be a list of {asset, threshold, clearance}"
        value = record.get("value")
        for entry in clearance:
            if not isinstance(entry, dict):
                return "each clearance entry must be an object with asset, threshold, clearance"
            thr, clr = entry.get("threshold"), entry.get("clearance")
            if (not isinstance(entry.get("asset"), str) or not entry["asset"].strip()
                    or not isinstance(thr, (int, float)) or isinstance(thr, bool)
                    or not math.isfinite(thr)
                    or not isinstance(clr, (int, float)) or isinstance(clr, bool)
                    or not math.isfinite(clr)):
                return "each clearance entry needs a named asset and finite threshold and clearance"
            if (not isinstance(value, (int, float)) or isinstance(value, bool)
                    or abs(clr - (thr - value)) > 1e-6):
                return "clearance must equal threshold - forecast value"
    return None


def cmd_issue(a, records):
    fc = forecasts(records)
    if a.id in fc:
        raise ValueError(f"forecast id '{a.id}' already registered; register a correction with a new id and --supersedes")
    if a.supersedes and a.supersedes not in fc:
        raise ValueError(f"--supersedes '{a.supersedes}' is not a registered forecast")
    issued = now_utc()
    horizon = parse_time(a.horizon_end, end_of_day=True)
    if horizon <= issued:
        raise ValueError("horizon end must be after the issue time: the outcome must still be unknown")
    inputs = [x.strip() for x in (a.inputs or "").split(",") if x.strip()]
    if not inputs:
        raise ValueError("--inputs must list the manifest ids of the input data")
    if a.kind == "probability":
        if a.value is None or not 0.0 <= a.value <= 1.0:
            raise ValueError("a probability forecast needs --value in [0, 1]")
    else:
        if a.value is None:
            raise ValueError("a quantity forecast needs --value")
    if (a.lower is None) != (a.upper is None):
        raise ValueError("give both --lower and --upper, or neither")
    if a.lower is not None and not a.lower <= a.value <= a.upper:
        raise ValueError("the interval must contain the forecast value")
    if a.lower is not None and not a.interval_method:
        raise ValueError("an interval needs --interval-method (how it was computed); decorative intervals are refused")
    if a.lead_time is None and a.lead_time_unit is not None:
        raise ValueError("--lead-time-unit needs --lead-time")
    if a.lead_time is not None and (not math.isfinite(a.lead_time) or a.lead_time <= 0):
        raise ValueError("--lead-time must be a positive number of --lead-time-unit")
    clearance = None
    if a.clearance:
        clearance = []
        for pair in a.clearance.split(","):
            if ":" not in pair:
                raise ValueError(f"--clearance pair '{pair}' must look like 'asset:threshold'")
            name, thr = pair.split(":", 1)
            name = name.strip()
            try:
                thr = float(thr)
            except ValueError:
                raise ValueError(f"--clearance threshold for '{name}' must be a number, got '{thr}'")
            if not name or not math.isfinite(thr):
                raise ValueError("--clearance needs a named asset and a finite threshold per pair")
            clearance.append({"asset": name, "threshold": thr,
                              "clearance": round(thr - a.value, 9)})
    metric = a.metric or ("brier" if a.kind == "probability" else "abs_error")
    rec = {"type": "forecast", "id": a.id, "issued_at": issued.isoformat(), "horizon_end": horizon.isoformat(),
           "target": a.target, "kind": a.kind, "value": a.value, "lower": a.lower, "upper": a.upper,
           "interval_method": a.interval_method, "unit": a.unit, "model": a.model,
           "model_version": a.model_version, "inputs": inputs, "metric": metric,
           "trial": bool(a.trial), "supersedes": a.supersedes, "clock": clock_source(),
           "cadence": a.cadence,
           "lead_time": ({"value": a.lead_time, "unit": a.lead_time_unit or "days"}
                         if a.lead_time is not None else None),
           "clearance": clearance}
    return append(a.registry, rec, records)


def cmd_resolve(a, records):
    fc = forecasts(records)
    if a.id not in fc:
        raise ValueError(f"'{a.id}' is not registered: an unregistered forecast earns no verification credit")
    f = fc[a.id]
    current = now_utc()
    observed = parse_time(a.observed_at) if a.observed_at else current
    if observed > current:
        raise ValueError("an outcome cannot be observed in the future")
    if observed < parse_time(f["issued_at"]):
        raise ValueError("an outcome cannot be observed before the forecast was issued")
    early = observed < parse_time(f["horizon_end"])
    if f["kind"] == "probability":
        if a.outcome not in (0.0, 1.0):
            raise ValueError("a probability forecast resolves to 0 or 1")
        if early and a.outcome == 0.0:
            raise ValueError("'did not occur' cannot be recorded before the horizon closes")
    elif early:
        raise ValueError("a quantity outcome cannot be known before the horizon closes")
    prior = [r for r in records if r.get("type") == "outcome" and r["id"] == a.id]
    if prior and not a.amend_reason:
        raise ValueError("an outcome is already recorded; pass --amend-reason to append an amendment")
    rec = {"type": "outcome", "id": a.id, "observed_at": observed.isoformat(), "outcome": a.outcome,
           "source": a.source, "amend_reason": a.amend_reason, "recorded_at": current.isoformat(),
           "clock": clock_source()}
    return append(a.registry, rec, records)


def cmd_replay(a, records):
    """Record a historical-event replay (Round 1 of the v2.7 program).

    A replay runs the existing QC/trend/alert pipeline on the data up to
    a historical extreme and records whether and when the alert fired.
    The data cutoff is the last observation before the event: the pipeline
    sees only data up to the cutoff, never the event itself. A replay
    whose alert did not fire records lead_time_days null — a miss is a
    finding, not a failure to report. Replays are verifications, not
    forecasts: they are hash-chained like every record, but `score`
    ignores them and they carry no decision weight for a future event.
    The measured lead time feeds the lead-time register with a measured,
    not claimed, value.
    """
    existing = {r["id"] for r in records if r.get("type") == "replay"}
    if a.id in existing:
        raise ValueError(f"replay id '{a.id}' already registered")
    event = parse_time(a.event_date)
    cutoff = parse_time(a.data_cutoff)
    if cutoff > event:
        raise ValueError("the data cutoff must be on or before the event date: "
                         "the pipeline must not see the event")
    fired = a.alert_fired == "yes"
    if fired and (a.lead_time_days is None or a.lead_time_days < 0):
        raise ValueError("an alert that fired needs --lead-time-days >= 0 (days from the alert to the event)")
    if not fired and a.lead_time_days is not None:
        raise ValueError("a replay whose alert did not fire has no lead time: omit --lead-time-days")
    inputs = [x.strip() for x in (a.inputs or "").split(",") if x.strip()]
    if not inputs:
        raise ValueError("--inputs must list the manifest ids of the data up to the cutoff")
    rec = {"type": "replay", "id": a.id, "event": a.event,
           "event_date": event.isoformat(), "data_cutoff": cutoff.isoformat(),
           "alert_fired": fired, "lead_time_days": a.lead_time_days,
           "method": a.method, "inputs": inputs, "model": a.model,
           "model_version": a.model_version, "issued_at": now_utc().isoformat(),
           "clock": clock_source()}
    return append(a.registry, rec, records)


def cmd_promote(a, records):
    """Record a promotion (Round 4 of the v2.7 program, Gironde).

    A model moves from exploratory to operational, signed: who approved
    (name/role), when (the registration clock), and the evidence
    (benchmark + hold-out score). A model without a promotion record is
    exploratory by rule; its outputs are never presented as operational.
    Promotions are hash-chained like every record, but `score` ignores
    them — a promotion is governance, not a forecast.
    """
    existing = {r["id"] for r in records if r.get("type") == "promotion"}
    if a.id in existing:
        raise ValueError(f"promotion id '{a.id}' already registered")
    if not (a.promoted_by or "").strip():
        raise ValueError("--promoted-by (name/role) is required: a promotion is signed")
    if not (a.evidence or "").strip():
        raise ValueError("--evidence (benchmark + hold-out score) is required: a promotion needs its evidence")
    rec = {"type": "promotion", "id": a.id, "status": "operational",
           "model": a.model, "model_version": a.model_version,
           "promoted_by": a.promoted_by, "evidence": a.evidence,
           "issued_at": now_utc().isoformat(), "clock": clock_source()}
    return append(a.registry, rec, records)


def verify(records):
    prev = GENESIS
    for n, r in enumerate(records, start=1):
        if r.get("prev_hash") != prev:
            return {"ok": False, "line": n, "problem": "chain broken: record removed, inserted, or reordered"}
        if digest(r) != r.get("hash"):
            return {"ok": False, "line": n, "problem": "record content altered after registration"}
        if r.get("type") == "forecast":
            problem = validate_forecast_fields(r)
            if problem:
                return {"ok": False, "line": n, "problem": problem}
        prev = r["hash"]
    return {"ok": True, "records": len(records)}


def cmd_score(a, records):
    fc = forecasts(records)
    outcomes = {}
    amended = set()
    for r in records:
        if r.get("type") == "outcome":
            if r["id"] in outcomes:
                amended.add(r["id"])
            outcomes[r["id"]] = r
    superseded = {f["supersedes"] for f in fc.values() if f.get("supersedes")}
    now = parse_time(a.now) if a.now else now_utc()
    rows, overdue, pending = [], [], []
    for fid, f in fc.items():
        o = outcomes.get(fid)
        if o is None:
            (overdue if parse_time(f["horizon_end"]) < now else pending).append(fid)
            continue
        y = o["outcome"]
        row = {"id": fid, "trial": f["trial"], "superseded": fid in superseded,
               "amended_outcome": fid in amended, "kind": f["kind"]}
        if f["kind"] == "probability":
            row["brier"] = (f["value"] - y) ** 2
        else:
            row["abs_error"] = abs(f["value"] - y)
            if f.get("lower") is not None:
                row["in_interval"] = f["lower"] <= y <= f["upper"]
        rows.append(row)

    def summarize(sel):
        out = {"n_scored": len(sel)}
        b = [r["brier"] for r in sel if "brier" in r]
        e = [r["abs_error"] for r in sel if "abs_error" in r]
        c = [r["in_interval"] for r in sel if "in_interval" in r]
        if b:
            out["mean_brier"] = sum(b) / len(b)
            out["n_probability"] = len(b)
        if e:
            out["mean_abs_error"] = sum(e) / len(e)
            out["n_quantity"] = len(e)
        if c:
            out["interval_coverage"] = sum(c) / len(c)
            out["n_intervals"] = len(c)
        return out

    chain = verify(records)
    return {
        "registry": a.registry, "chain": chain,
        "operational": summarize([r for r in rows if not r["trial"]]),
        "trial": summarize([r for r in rows if r["trial"]]),
        "forecasts": rows, "overdue_without_outcome": overdue, "pending": pending,
        "rule": "scored exactly as registered; superseded forecasts stay in the score",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("issue")
    i.add_argument("--registry", required=True)
    i.add_argument("--id", required=True)
    i.add_argument("--kind", choices=["probability", "quantity"], required=True)
    i.add_argument("--target", required=True, help="what is forecast, with unit and location")
    i.add_argument("--value", type=float)
    i.add_argument("--lower", type=float)
    i.add_argument("--upper", type=float)
    i.add_argument("--interval-method", help="how the interval was computed")
    i.add_argument("--unit")
    i.add_argument("--horizon-end", required=True, help="ISO date/time when the outcome becomes knowable")
    i.add_argument("--model", required=True)
    i.add_argument("--model-version", required=True)
    i.add_argument("--inputs", required=True, help="comma list of input manifest ids")
    i.add_argument("--metric", choices=["brier", "abs_error", "interval"])
    i.add_argument("--trial", action="store_true", help="trial forecast of a level-3 twin: no decision weight")
    i.add_argument("--cadence", choices=CADENCES,
                   help="forecast refresh rhythm: daily, weekly, seasonal, or event-driven")
    i.add_argument("--lead-time", type=float,
                   help="usable warning lead time for the decision, in --lead-time-unit")
    i.add_argument("--lead-time-unit", choices=LEAD_TIME_UNITS, default=None,
                   help="unit of --lead-time (default days)")
    i.add_argument("--clearance", help="per-asset clearance: 'asset:threshold,...' "
                                       "(threshold in the forecast's unit); the record carries "
                                       "clearance = threshold - forecast value per asset")
    i.add_argument("--supersedes")
    r = sub.add_parser("resolve")
    r.add_argument("--registry", required=True)
    r.add_argument("--id", required=True)
    r.add_argument("--outcome", type=float, required=True)
    r.add_argument("--observed-at")
    r.add_argument("--source", help="manifest id of the observation")
    r.add_argument("--amend-reason")
    p = sub.add_parser("replay")
    p.add_argument("--registry", required=True)
    p.add_argument("--id", required=True, help="replay record id, e.g. RIVER-R-001")
    p.add_argument("--event", required=True, help="the historical extreme, named (e.g. 'Potomac flood peak 2026-10-14')")
    p.add_argument("--event-date", required=True, help="ISO date/time of the event")
    p.add_argument("--data-cutoff", required=True, help="ISO date/time of the last observation before the event")
    p.add_argument("--alert-fired", choices=["yes", "no"], required=True,
                   help="did the pipeline's alert fire on the data up to the cutoff?")
    p.add_argument("--lead-time-days", type=float,
                   help="days from the alert to the event; required when the alert fired, forbidden when it did not")
    p.add_argument("--method", required=True, help="the pipeline run, e.g. 'alert_bands.py --amber ... --window-hours ...'")
    p.add_argument("--inputs", required=True, help="comma list of input manifest ids (data up to the cutoff)")
    p.add_argument("--model", required=True)
    p.add_argument("--model-version", required=True)
    p = sub.add_parser("promote")
    p.add_argument("--registry", required=True)
    p.add_argument("--id", required=True, help="promotion record id, e.g. PROM-001")
    p.add_argument("--model", required=True)
    p.add_argument("--model-version", required=True)
    p.add_argument("--promoted-by", required=True, help="who approved, name/role")
    p.add_argument("--evidence", required=True, help="benchmark + hold-out score the promotion rests on")
    v = sub.add_parser("verify")
    v.add_argument("--registry", required=True)
    s = sub.add_parser("score")
    s.add_argument("--registry", required=True)
    s.add_argument("--now", help="evaluation time (ISO); default now, UTC")
    s.add_argument("--max-items", type=int, default=25)
    s.add_argument("--full-json", help="write the untruncated score record here")
    a = ap.parse_args(argv)
    try:
        records = load(a.registry)
        if a.cmd in ("issue", "resolve", "replay", "promote"):
            check = verify(records)
            if not check["ok"]:
                raise ValueError(f"registry integrity check failed at line {check['line']}: {check['problem']}")
            rec = {"issue": cmd_issue, "resolve": cmd_resolve, "replay": cmd_replay,
                   "promote": cmd_promote}[a.cmd](a, records)
            print(json.dumps({"registered": rec}, ensure_ascii=False, indent=2))
            return 0
        if a.cmd == "verify":
            res = verify(records)
            print(json.dumps(res, indent=2))
            return 0 if res["ok"] else 3
        res = cmd_score(a, records)
        if a.full_json:
            with open(a.full_json, "w", encoding="utf-8") as fh:
                json.dump(res, fh, ensure_ascii=False, indent=2)
        for key in ("forecasts", "overdue_without_outcome", "pending"):
            cap(res, key, a.max_items)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["chain"]["ok"] else 3
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
