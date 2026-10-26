#!/usr/bin/env python3
"""
Unit tests for the bundled scripts. Standard library only; network not needed.

  python3 -m unittest discover -s tests -v      (from the skill root)

Formulas are checked against hand-computed values; CLIs are run as
subprocesses so exit codes and gate behavior are tested as an agent sees them.
"""

import csv
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPTS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(script, *args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    res = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                         capture_output=True, text=True, env=e, timeout=120)
    out = None
    if res.stdout.strip().startswith("{"):
        out = json.loads(res.stdout)
    return res.returncode, out, res.stderr


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def wtext(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def rtext(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class Tmp(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.d = self._td.name

    def tearDown(self):
        self._td.cleanup()

    def p(self, name):
        return os.path.join(self.d, name)


class TestSkillScores(Tmp):
    m = load("skill_scores")

    def test_perfect_simulation(self):
        r = self.m.continuous_metrics([1, 2, 3, 4], [1, 2, 3, 4])
        self.assertAlmostEqual(r["nse"], 1.0)
        self.assertAlmostEqual(r["kge"], 1.0)
        self.assertAlmostEqual(r["rmse"], 0.0)

    def test_nse_hand_value(self):
        r = self.m.continuous_metrics([1, 2, 3, 4, 5], [1.5, 2, 2.5, 4.5, 5])
        self.assertAlmostEqual(r["nse"], 1 - 0.75 / 10)  # SSE 0.75, SSO 10
        self.assertAlmostEqual(r["bias"], 0.1)

    def test_mean_prediction_has_zero_nse(self):
        r = self.m.continuous_metrics([1, 2, 3, 4, 5], [3, 3, 3, 3, 3])
        self.assertAlmostEqual(r["nse"], 0.0)

    def test_kge_hand_value(self):
        r = self.m.continuous_metrics([1, 2, 3, 4], [2, 4, 6, 8])  # r=1, alpha=2, beta=2
        self.assertAlmostEqual(r["kge"], 1 - math.sqrt(2))

    def _monthly(self, path, noise, shift=0.0):
        import random
        rng = random.Random(7)  # fixed seed: anomalies that climatology cannot know
        rows, d = [], date(2015, 1, 15)
        for k in range(72):
            obs = 10 + 5 * math.sin(2 * math.pi * (d.month - 1) / 12) + rng.gauss(0, 1.5)
            sim = obs + noise * (1 if k % 2 else -1) + shift
            rows.append([d.isoformat(), f"{obs:.4f}", f"{sim:.4f}"])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=15)
        write_csv(path, ["time", "obs", "sim"], rows)

    def test_holdout_required(self):
        self._monthly(self.p("s.csv"), 0.1)
        code, _, err = run("skill_scores.py", "continuous", self.p("s.csv"))
        self.assertEqual(code, 2)
        self.assertIn("--train-end", err)

    def test_good_model_passes_and_beats_baselines(self):
        self._monthly(self.p("s.csv"), 0.1)
        code, out, _ = run("skill_scores.py", "continuous", self.p("s.csv"),
                           "--train-end", "2018-12-31", "--thresholds", "NSE>=0.5,abs_pbias<=10")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["n_train_obs"], 48)
        self.assertEqual(out["metrics"]["n"], 24)
        self.assertGreater(out["metrics"]["skill_vs_climatology"], 0)
        self.assertGreater(out["metrics"]["skill_vs_persistence"], 0)

    def test_fixed_persistence_baseline(self):
        rows = [[f"{1900 + k}-07-01", 10 + k, 10 + k] for k in range(30)]  # obs rises 1/yr; sim perfect
        write_csv(self.p("f.csv"), ["time", "obs", "sim"], rows)
        _, roll, _ = run("skill_scores.py", "continuous", self.p("f.csv"), "--train-end", "1919-12-31", "--season", "none")
        _, fix, _ = run("skill_scores.py", "continuous", self.p("f.csv"), "--train-end", "1919-12-31", "--season", "none",
                        "--persistence", "fixed")
        self.assertAlmostEqual(roll["baselines"][0]["mse_baseline"], 1.0)  # previous year is always 1 off
        self.assertAlmostEqual(fix["baselines"][0]["mse_baseline"], sum(k * k for k in range(1, 11)) / 10)
        self.assertIn("last training", fix["baselines"][0]["baseline"])

    def test_biased_model_fails_gate(self):
        self._monthly(self.p("s.csv"), 0.1, shift=6.0)
        code, out, _ = run("skill_scores.py", "continuous", self.p("s.csv"),
                           "--train-end", "2018-12-31", "--thresholds", "NSE>=0.5")
        self.assertEqual(code, 3)
        self.assertEqual(out["gate"], "fail")

    def test_events_contingency(self):
        write_csv(self.p("e.csv"), ["obs", "fcst", "lead"],
                  [[1, 1, 48], [1, 0, ""], [1, 1, 24], [0, 1, ""], [0, 0, ""], [0, 0, ""], [1, 1, 72], [0, 0, ""]])
        code, out, _ = run("skill_scores.py", "events", self.p("e.csv"), "--lead-col", "lead")
        self.assertEqual(code, 0)
        self.assertEqual((out["hits"], out["misses"], out["false_alarms"], out["correct_negatives"]), (3, 1, 1, 3))
        self.assertAlmostEqual(out["pod"], 0.75)
        self.assertAlmostEqual(out["far"], 0.25)
        self.assertAlmostEqual(out["csi"], 0.6)
        self.assertAlmostEqual(out["lead_time_of_hits"]["median"], 48)
        self.assertTrue(out["warnings"])  # 4 events < 5

    def test_brier_climatology_has_zero_skill(self):
        rows = [[1 if k % 4 == 0 else 0, 0.25] for k in range(40)]
        write_csv(self.p("b.csv"), ["obs", "prob"], rows)
        code, out, _ = run("skill_scores.py", "brier", self.p("b.csv"), "--clim-prob", "0.25")
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["brier_score"], 0.1875)
        self.assertAlmostEqual(out["brier_skill_score"], 0.0)
        d = out["decomposition"]
        self.assertAlmostEqual(d["reliability"] - d["resolution"] + d["uncertainty"], out["brier_score"])


class TestTrend(Tmp):
    m = load("trend_test")

    def test_s_and_variance_with_ties(self):
        s, var = self.m.mk_s_var([1, 1, 2])
        self.assertEqual(s, 2)
        self.assertAlmostEqual(var, (3 * 2 * 11 - 2 * 1 * 9) / 18)

    def test_monotonic_series(self):
        write_csv(self.p("t.csv"), ["time", "value"], [[f"{2000 + k}-07-01", k] for k in range(20)])
        code, out, _ = run("trend_test.py", self.p("t.csv"))
        self.assertEqual(code, 0)
        seg = out["segments"][0]
        self.assertEqual(seg["S"], 190)
        self.assertEqual(seg["direction"], "increasing")
        self.assertAlmostEqual(seg["sen_slope_per_year"], 1.0, places=2)

    def test_breaks_split_segments(self):
        rows = [[f"{1990 + k}-07-01", k] for k in range(19)] + [[f"{2009 + k}-07-01", 50 - k] for k in range(12)]
        write_csv(self.p("t.csv"), ["time", "value"], rows)
        code, out, _ = run("trend_test.py", self.p("t.csv"), "--breaks", "2009-01-01")
        self.assertEqual(code, 0)
        self.assertEqual(len(out["segments"]), 2)
        self.assertEqual(out["segments"][0]["direction"], "increasing")
        self.assertEqual(out["segments"][1]["direction"], "decreasing")

    def test_short_segment_not_tested(self):
        write_csv(self.p("t.csv"), ["time", "value"], [[f"{2000 + k}-07-01", k] for k in range(5)])
        _, out, _ = run("trend_test.py", self.p("t.csv"))
        self.assertIsNone(out["segments"][0]["result"])

    def test_seasonal_kendall_recovers_trend(self):
        rows = []
        for y in range(2010, 2020):
            for mth in range(1, 13):
                v = 0.5 * (y - 2010) + 4 * math.sin(2 * math.pi * mth / 12) + (0.3 if (y + mth) % 3 else -0.4)
                rows.append([f"{y}-{mth:02d}-15", round(v, 3)])
        write_csv(self.p("t.csv"), ["time", "value"], rows)
        _, out, _ = run("trend_test.py", self.p("t.csv"), "--seasonal", "month")
        seg = out["segments"][0]
        self.assertEqual(seg["direction"], "increasing")
        self.assertAlmostEqual(seg["sen_slope_per_year"], 0.5, delta=0.1)
        lo, hi = seg["slope_ci"]
        self.assertTrue(lo <= 0.5 <= hi)


class TestQC(Tmp):
    m = load("qc_series")

    def test_flags_without_editing(self):
        vals = [5.0, 5.2, 5.1, "", 99.0, 5.3, 12.0, 5.2, 5.4, 5.4, 5.4, 5.4, 5.4, 5.4, 5.5, 5.3]
        rows = []
        for h, v in enumerate(vals):
            rows.append([f"2027-07-01T{h:02d}:00:00", v])
        rows.append(["2027-07-01T15:00:00", 5.3])  # duplicate timestamp
        write_csv(self.p("q.csv"), ["time", "value"], rows)
        code, out, _ = run("qc_series.py", self.p("q.csv"), "--min", "0", "--max", "20",
                           "--max-rate", "3", "--stuck-run", "6", "--out", self.p("o.csv"),
                           "--fail-on", "range")
        self.assertEqual(code, 3)
        flagged = read_csv(self.p("o.csv"))
        by_row = [r["qc_flag"] for r in flagged]
        self.assertEqual(by_row[3], "missing")
        self.assertEqual(by_row[4], "range")
        self.assertIn("rate", by_row[6])
        self.assertTrue(all("stuck" in by_row[k] for k in range(8, 14)))
        self.assertIn("duplicate_time", by_row[15])
        self.assertEqual([r["value"] for r in flagged], [str(r[1]) for r in rows])  # untouched
        self.assertFalse(out["values_modified"])

    def test_pettitt_finds_step(self):
        series = [1 + 0.01 * (k % 3) for k in range(20)] + [5 + 0.01 * (k % 3) for k in range(20)]
        idx, k_stat, p = self.m.pettitt(series)
        self.assertEqual(idx, 19)
        self.assertLess(p, 0.001)


class TestCoordinates(Tmp):
    m = load("generalize_coords")

    def test_rounding_and_uncertainty(self):
        lat, lon, unc = self.m.generalize(52.3456, 104.2789, 0.1)
        self.assertEqual((lat, lon), (52.3, 104.3))
        self.assertTrue(6000 < unc < 7200, unc)
        _, _, unc_eq = self.m.generalize(0.01, 0.01, 0.1)
        self.assertTrue(7800 < unc_eq < 7900, unc_eq)

    def test_categories_and_check(self):
        header = ["scientificName", "decimalLatitude", "decimalLongitude", "locality", "sensitivity"]
        rows = [["A", "52.34567", "104.27891", "north cliff nest", "extreme"],
                ["B", "52.34567", "104.27891", "bay", "high"],
                ["C", "52.34567", "104.27891", "pond", "medium"],
                ["D", "52.34567", "104.27891", "field", "none"]]
        write_csv(self.p("occ.csv"), header, rows)
        code, raw_check, _ = run("generalize_coords.py", "--check", self.p("occ.csv"), "--category-col", "sensitivity")
        self.assertEqual(code, 3)
        self.assertNotIn("52.34", json.dumps(raw_check))  # the report never prints coordinates
        code, out, _ = run("generalize_coords.py", self.p("occ.csv"), "--category-col", "sensitivity",
                           "--out", self.p("shared.csv"))
        self.assertEqual(code, 0)
        self.assertEqual((out["withheld"], out["generalized"], out["unchanged"]), (1, 2, 1))
        shared = read_csv(self.p("shared.csv"))
        self.assertEqual(shared[0]["decimalLatitude"], "")
        self.assertEqual(shared[1]["decimalLatitude"], "52.3")
        self.assertEqual(shared[2]["decimalLatitude"], "52.3")  # medium lifted to the 0.1 floor
        self.assertEqual(shared[1]["locality"], "")
        self.assertEqual(shared[3]["decimalLatitude"], "52.34567")
        code, ok, _ = run("generalize_coords.py", "--check", self.p("shared.csv"), "--category-col", "sensitivity")
        self.assertEqual(code, 0, ok)

    def test_gbif_finer_option(self):
        write_csv(self.p("o.csv"), ["decimalLatitude", "decimalLongitude"], [["52.34567", "104.27891"]])
        run("generalize_coords.py", self.p("o.csv"), "--category", "medium", "--allow-gbif-finer",
            "--out", self.p("s.csv"))
        self.assertEqual(read_csv(self.p("s.csv"))[0]["decimalLatitude"], "52.35")


class TestManifest(Tmp):
    def index(self, **over):
        idx = {
            "name": "Lake test package", "description": "Unit-test package",
            "license": "https://creativecommons.org/licenses/by/4.0/", "datePublished": "2027-10-01",
            "datasets": [{"id": "ds-01", "name": "Sentinel-2 L2A", "url": "https://example.org/s2",
                          "version": "L2A", "retrieved": "2027-09-01", "license": "CC-BY-4.0"},
                         {"id": "ds-02", "name": "Lab chemistry", "path": "data/lab.csv", "version": "v3",
                          "license": "client"}],
            "models": [{"id": "m-01", "name": "TP-lag regression", "version": "0.2"}],
            "steps": [{"id": "st-01", "name": "Fit and hindcast", "instrument": "m-01",
                       "inputs": ["ds-01", "ds-02"], "parameters": "lag 3 weeks"}],
            "outputs": [{"id": "out-01", "name": "Summer mean chlorophyll-a", "value": 18.2,
                         "unit": "mg/m3", "produced_by": "st-01", "headline": True}],
        }
        idx.update(over)
        os.makedirs(self.p("pkg/data"), exist_ok=True)
        wtext(self.p("pkg/data/lab.csv"), "time,tp\n")
        with open(self.p("build.json"), "w") as fh:
            json.dump(idx, fh)
        return self.p("build.json")

    def test_valid_crate(self):
        code, out, _ = run("build_manifest.py", self.index(), "--out-dir", self.p("pkg"))
        self.assertEqual(code, 0, out)
        crate = json.loads(rtext(self.p("pkg/ro-crate-metadata.json")))
        self.assertEqual(crate["@context"], "https://w3id.org/ro/crate/1.1/context")
        g = {e["@id"]: e for e in crate["@graph"]}
        self.assertEqual(g["ro-crate-metadata.json"]["conformsTo"]["@id"], "https://w3id.org/ro/crate/1.1")
        root = g["./"]
        for key in ("name", "description", "datePublished", "license"):
            self.assertIn(key, root)
        self.assertEqual(g["https://example.org/s2"]["sdDatePublished"], "2027-09-01")
        self.assertEqual(g["data/lab.csv"]["@type"], "File")
        act = g["#st-01"]
        self.assertEqual(act["@type"], "CreateAction")
        self.assertEqual(act["result"], [{"@id": "#out-01"}])
        self.assertEqual(g["#out-01"]["@type"], "PropertyValue")
        try:
            from rocrate.rocrate import ROCrate  # optional third-party validator
        except ImportError:
            return
        rc = ROCrate(self.p("pkg"))
        self.assertEqual(rc.name, "Lake test package")
        self.assertIsNotNone(rc.dereference("#st-01"))

    def test_missing_retrieval_date_fails(self):
        bad = [{"id": "ds-01", "name": "x", "url": "https://example.org/x", "version": "1"}]
        code, out, _ = run("build_manifest.py", self.index(datasets=bad), "--check")
        self.assertEqual(code, 3)
        self.assertTrue(any("retrieved" in e for e in out["errors"]))

    def test_unknown_model_and_orphan_output_fail(self):
        steps = [{"id": "st-01", "name": "s", "instrument": "m-99", "inputs": ["ds-01"]}]
        outputs = [{"id": "out-01", "name": "x", "value": 1, "produced_by": "st-09"}]
        code, out, _ = run("build_manifest.py", self.index(steps=steps, outputs=outputs), "--check")
        self.assertEqual(code, 3)
        joined = " ".join(out["errors"])
        self.assertIn("m-99", joined)
        self.assertIn("st-09", joined)

    def test_report_citations(self):
        idx = self.index()
        wtext(self.p("r1.md"), "Summer chlorophyll was 18.2 mg/m3 [out-01].\n")
        code, _, _ = run("build_manifest.py", idx, "--check", "--report", self.p("r1.md"))
        self.assertEqual(code, 0)
        wtext(self.p("r2.md"), "Summer chlorophyll was 18.2 mg/m3, see [out-07].\n")
        code, out, _ = run("build_manifest.py", idx, "--check", "--report", self.p("r2.md"))
        self.assertEqual(code, 3)
        self.assertTrue(any("out-07" in e for e in out["errors"]))
        self.assertTrue(any("out-01" in e for e in out["errors"]))


class TestRegistry(Tmp):
    def clock(self, t):
        return {"ECO_TWIN_CLOCK": t}

    def issue(self, fid, *extra, at="2027-05-01T08:00:00Z", horizon="2027-08-31"):
        return run("registry.py", "issue", "--registry", self.p("reg.jsonl"), "--id", fid,
                   "--kind", "quantity", "--target", "Jul-Aug mean chl-a (mg/m3)", "--value", "18",
                   "--lower", "11", "--upper", "27", "--interval-method", "regression prediction interval",
                   "--horizon-end", horizon, "--model", "TP-lag", "--model-version", "0.2",
                   "--inputs", "ds-03,ds-05", *extra, env=self.clock(at))

    def test_lifecycle_and_scoring(self):
        code, _, err = self.issue("F1", "--trial")
        self.assertEqual(code, 0, err)
        code, _, err = run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", "F1",
                           "--outcome", "21.5", env=self.clock("2027-09-03T10:00:00Z"))
        self.assertEqual(code, 0, err)
        code, out, _ = run("registry.py", "score", "--registry", self.p("reg.jsonl"), "--now", "2027-09-04")
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["trial"]["mean_abs_error"], 3.5)
        self.assertEqual(out["trial"]["interval_coverage"], 1.0)
        self.assertEqual(out["operational"]["n_scored"], 0)

    def test_refusals(self):
        self.assertEqual(self.issue("F1")[0], 0)
        self.assertEqual(self.issue("F1")[0], 2)  # duplicate id
        self.assertEqual(self.issue("F2", horizon="2027-04-01")[0], 2)  # outcome already knowable
        code, _, err = run("registry.py", "issue", "--registry", self.p("reg.jsonl"), "--id", "F3",
                           "--kind", "quantity", "--target", "x", "--value", "1", "--lower", "0", "--upper", "2",
                           "--horizon-end", "2027-09-01", "--model", "m", "--model-version", "1",
                           "--inputs", "ds-01", env=self.clock("2027-05-01T00:00:00Z"))
        self.assertEqual(code, 2)
        self.assertIn("interval-method", err)
        code, _, _ = run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", "F1",
                         "--outcome", "20", env=self.clock("2027-07-01T00:00:00Z"))
        self.assertEqual(code, 2)  # quantity outcome before the horizon closes
        code, _, _ = run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", "NOPE",
                         "--outcome", "1", env=self.clock("2027-09-05T00:00:00Z"))
        self.assertEqual(code, 2)  # unregistered forecast earns nothing

    def test_probability_early_resolution(self):
        args = ["--registry", self.p("reg.jsonl"), "--id", "P1", "--kind", "probability", "--target",
                "amber bloom trigger fires this season", "--value", "0.6", "--horizon-end", "2027-09-30",
                "--model", "watch", "--model-version", "1", "--inputs", "ds-01"]
        self.assertEqual(run("registry.py", "issue", *args, env=self.clock("2027-05-01T00:00:00Z"))[0], 0)
        no = run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", "P1", "--outcome", "0",
                 env=self.clock("2027-07-01T00:00:00Z"))
        self.assertEqual(no[0], 2)
        yes = run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", "P1", "--outcome", "1",
                  env=self.clock("2027-07-01T00:00:00Z"))
        self.assertEqual(yes[0], 0)
        _, out, _ = run("registry.py", "score", "--registry", self.p("reg.jsonl"))
        self.assertAlmostEqual(out["operational"]["mean_brier"], 0.16)

    def test_tamper_detection_and_superseded_scoring(self):
        self.issue("F1")
        self.issue("F2", "--supersedes", "F1", at="2027-05-02T08:00:00Z")
        for fid in ("F1", "F2"):
            run("registry.py", "resolve", "--registry", self.p("reg.jsonl"), "--id", fid, "--outcome", "30",
                env=self.clock("2027-09-05T00:00:00Z"))
        _, out, _ = run("registry.py", "score", "--registry", self.p("reg.jsonl"))
        self.assertEqual(out["operational"]["n_scored"], 2)  # the superseded forecast still counts
        self.assertEqual(run("registry.py", "verify", "--registry", self.p("reg.jsonl"))[0], 0)
        lines = rtext(self.p("reg.jsonl")).splitlines()
        lines[0] = lines[0].replace('"value": 18.0', '"value": 29.0')
        wtext(self.p("reg.jsonl"), "\n".join(lines) + "\n")
        code, out, _ = run("registry.py", "verify", "--registry", self.p("reg.jsonl"))
        self.assertEqual(code, 3)
        self.assertEqual(out["line"], 1)

    def test_overdue_listed(self):
        self.issue("F1")
        _, out, _ = run("registry.py", "score", "--registry", self.p("reg.jsonl"), "--now", "2027-12-01")
        self.assertEqual(out["overdue_without_outcome"], ["F1"])


class TestRobustInput(Tmp):
    def test_semicolon_and_decimal_comma(self):
        with open(self.p("eu.csv"), "w", encoding="utf-8") as fh:
            fh.write("time;value\n")
            for h in range(12):
                fh.write(f"2027-07-01T{h:02d}:00:00;{5 + h % 2},{h % 10}\n")
        code, out, _ = run("qc_series.py", self.p("eu.csv"), "--min", "0", "--max", "20", "--out", self.p("o.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["flag_counts"], {})  # decimal commas parsed, not counted as missing
        with open(self.p("o.csv"), encoding="utf-8") as fh:
            self.assertIn(";", fh.readline())  # output keeps the input delimiter

    def test_prewhitening_triggers_on_autocorrelated_series(self):
        import random
        rng = random.Random(3)
        e, rows = 0.0, []
        for k in range(120):
            e = 0.8 * e + rng.gauss(0, 1)
            d = date(2010, 1, 1) + timedelta(days=30 * k)
            rows.append([d.isoformat(), round(0.05 * k + e, 4)])
        write_csv(self.p("ar.csv"), ["time", "value"], rows)
        _, out, _ = run("trend_test.py", self.p("ar.csv"))
        seg = out["segments"][0]
        self.assertGreater(seg["lag1_autocorrelation_detrended"], 0.3)
        self.assertIn("Hamed", seg["serial_correction"])
        self.assertAlmostEqual(seg["Z"], 4.0455, places=3)  # reference: pymannkendall 1.4.3 hamed_rao_modification_test
        self.assertGreater(seg["variance_factor_n_over_n_eff"], 1.5)  # positive autocorrelation inflates var(S)
        _, raw, _ = run("trend_test.py", self.p("ar.csv"), "--autocorr", "none")
        self.assertLess(abs(seg["Z"]), abs(raw["segments"][0]["Z"]))  # correction lowers |Z|
        _, tf, _ = run("trend_test.py", self.p("ar.csv"), "--autocorr", "tfpw")
        self.assertIn("Yue", tf["segments"][0]["serial_correction"])
        self.assertTrue(any("overstate" in w for w in tf["segments"][0]["warnings"]))


class TestOutputCaps(Tmp):
    """Summaries stay small enough to hand to other models; totals are never lost."""

    def test_qc_gaps_capped_with_full_record(self):
        rows = [[f"2027-07-{1 + k // 4:02d}T{(k % 4) * 6:02d}:00:00", 5] for k in range(0, 120, 2)]
        write_csv(self.p("g.csv"), ["time", "value"], rows)
        code, out, _ = run("qc_series.py", self.p("g.csv"), "--max-gap-hours", "1", "--max-items", "5",
                           "--full-json", self.p("full.json"))
        self.assertEqual(code, 0)
        self.assertEqual(len(out["gaps"]), 5)
        self.assertTrue(out["gaps_truncated"])
        full = json.loads(rtext(self.p("full.json")))
        self.assertEqual(out["gaps_total"], len(full["gaps"]))
        self.assertGreater(out["gaps_total"], 5)

    def test_alerts_capped(self):
        rows, h = [], 0
        for episode in range(8):  # eight separate 8-hour red episodes
            for k in range(9):
                rows.append([f"2027-07-{1 + h // 24:02d}T{h % 24:02d}:00:00", 1.0])
                h += 1
            for k in range(3):
                rows.append([f"2027-07-{1 + h // 24:02d}T{h % 24:02d}:00:00", 8.0])
                h += 1
        write_csv(self.p("a.csv"), ["time", "value"], rows)
        _, out, _ = run("alert_bands.py", self.p("a.csv"), "--indicator", "DO", "--amber", "<5", "--red", "<2",
                        "--window-hours", "6", "--anchor", "test", "--max-items", "3")
        self.assertEqual(out["alerts_total"], 8)
        self.assertEqual(len(out["alerts"]), 3)
        self.assertTrue(out["alerts_truncated"])
        self.assertEqual(out["status"], "red")


class TestAlerts(Tmp):
    def series(self, values, flags=None, start_hour=0, step=1):
        rows = []
        for k, v in enumerate(values):
            h = start_hour + k * step
            row = [f"2027-07-{1 + h // 24:02d}T{h % 24:02d}:00:00", v]
            if flags is not None:
                row.append(flags[k])
            rows.append(row)
        header = ["time", "value"] + (["qc_flag"] if flags is not None else [])
        write_csv(self.p("s.csv"), header, rows)
        return self.p("s.csv")

    def alert(self, path, *extra):
        return run("alert_bands.py", path, "--indicator", "DO bottom (mg/L)", "--amber", "<5", "--red", "<2",
                   "--window-hours", "6", "--max-gap-hours", "2", "--anchor", "national standard (test)", *extra)

    def test_sustained_red_alert_and_spike(self):
        vals = [7, 7, 1.5, 7, 7] + [4] * 3 + [1.8] * 8 + [6, 6]
        code, out, _ = self.alert(self.series(vals))
        self.assertEqual(code, 0)
        self.assertEqual(out["status"], "red")
        red = [x for x in out["alerts"] if x["band"] == "red"]
        self.assertEqual(len(red), 1)
        self.assertEqual(red[0]["elapsed_hours"], 7.0)
        self.assertAlmostEqual(red[0]["observed_extreme"], 1.8)
        self.assertGreaterEqual(out["unsustained_breaches"], 1)  # the single 1.5 spike

    def test_gap_breaks_episode_and_flags_ignored(self):
        vals = [3] * 4 + [3] * 4
        path = self.series(vals[:4], start_hour=0)
        rows = list(csv.reader(rtext(path).splitlines()))
        rows += [[f"2027-07-01T{h:02d}:00:00", 3] for h in range(10, 14)]  # 7-hour gap before these
        write_csv(path, rows[0], rows[1:])
        _, out, _ = self.alert(path)
        self.assertEqual(out["status"], "green")
        code, out, _ = self.alert(self.series([1] * 10, flags=["stuck"] * 10), "--fail-on", "red")
        self.assertEqual((code, out["status"], out["observations_ignored"]), (0, "green", 10))

    def test_suspect_values_kept_and_noise_tolerance(self):
        vals = [7, 1.5, 1.6, 1.7, 3.2, 1.8, 1.7, 1.6, 1.5, 7, 7]
        flags = ["ok", "rate"] + ["ok"] * 9
        path = self.series(vals, flags=flags)
        _, strict, _ = self.alert(path)
        self.assertEqual(strict["status"], "amber")  # the 3.2 reading splits the red run
        _, tol, _ = self.alert(path, "--tolerate", "1")
        self.assertEqual(tol["status"], "red")
        red = [x for x in tol["alerts"] if x["band"] == "red"][0]
        self.assertEqual(red["suspect_flags_inside"], ["rate"])  # the crash onset is kept, marked suspect

    def test_anchor_required_and_fail_on(self):
        path = self.series([1] * 10)
        code, _, _ = run("alert_bands.py", path, "--indicator", "DO", "--amber", "<5", "--red", "<2",
                         "--window-hours", "6", "--anchor", "  ")
        self.assertEqual(code, 2)
        code, out, _ = self.alert(path, "--fail-on", "red")
        self.assertEqual(code, 3)
        self.assertEqual(out["alerts"][0]["end"], "ongoing")


class TestCatalogue(unittest.TestCase):
    def test_indicator_groups_present(self):  # T8, automated
        text = rtext(os.path.join(ROOT, "references", "indicators.md")).lower()
        groups = ["dissolved oxygen", "nutrient", "phytoplankton", "escherichia coli", "discharge",
                  "sediment", "groundwater", "soil", "flora", "fish", "bird", "amphibian", "deposition",
                  "ecosystem functions", "pressures", "tier"]
        missing = [g for g in groups if g not in text]
        self.assertEqual(missing, [])


class TestUncertaintyBudget(Tmp):
    def rows(self, with_joint=True):
        rows = []
        for k in range(40):
            z = (k - 19.5) / 11.69  # deterministic spread with sd ~ 1
            rows.append(["chl", "parameter", k, 20 + 2 * z])
            rows.append(["chl", "forcing", k, 20 + 1 * z])
        for k in range(3):
            rows.append(["chl", "structural", k, [19.0, 20.0, 21.0][k]])
        if with_joint:
            for k in range(200):
                z = (k - 99.5) / 57.88
                rows.append(["chl", "all", k, 20 + 2.3 * z])
        return rows

    def test_shares_and_interval(self):
        write_csv(self.p("ens.csv"), ["output", "source", "member", "value"], self.rows())
        code, out, _ = run("uncertainty_budget.py", self.p("ens.csv"), "--interval", "90")
        self.assertEqual(code, 0)
        b = out["outputs"]["chl"]
        shares = {k: v.get("share_of_one_at_a_time_sum") for k, v in b["sources"].items()}
        self.assertGreater(shares["parameter"], shares["forcing"])
        self.assertAlmostEqual(sum(x for x in shares.values() if x), 1.0)
        lo, hi = b["joint"]["interval"]
        self.assertTrue(lo < 20 < hi)
        self.assertEqual(b["sources"]["scenario"]["members"], 0)

    def test_no_joint_no_interval(self):
        write_csv(self.p("ens.csv"), ["output", "source", "member", "value"], self.rows(with_joint=False))
        _, out, _ = run("uncertainty_budget.py", self.p("ens.csv"))
        b = out["outputs"]["chl"]
        self.assertIsNone(b["joint"])
        self.assertTrue(any("no interval" in w for w in b["warnings"]))

    def test_unknown_source_rejected(self):
        write_csv(self.p("ens.csv"), ["output", "source", "member", "value"], [["chl", "vibes", 1, 3], ["chl", "vibes", 2, 4]])
        self.assertEqual(run("uncertainty_budget.py", self.p("ens.csv"))[0], 2)


class TestEndToEnd(Tmp):
    """A miniature lake build carried through every script, as an agent would run it."""

    def test_lake_build(self):
        import random
        rng = random.Random(11)
        rows, d = [], date(2021, 1, 15)
        for k in range(60):
            season = 12 + 8 * math.sin(2 * math.pi * (d.month - 4) / 12)
            obs = season + rng.gauss(0, 2.0)
            sim = obs + rng.gauss(0, 0.8)
            rows.append([d.isoformat(), round(obs, 3), round(sim, 3)])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=15)
        write_csv(self.p("chl.csv"), ["time", "obs", "sim"], rows)
        code, qc, _ = run("qc_series.py", self.p("chl.csv"), "--value-col", "obs", "--min", "0", "--max", "300")
        self.assertEqual(code, 0)
        self.assertEqual(qc["rows_flagged"], 0)
        code, tr, _ = run("trend_test.py", self.p("chl.csv"), "--value-col", "obs", "--seasonal", "month")
        self.assertEqual(code, 0)
        code, sk, _ = run("skill_scores.py", "continuous", self.p("chl.csv"), "--train-end", "2023-12-31",
                          "--thresholds", "NSE>=0.5")
        self.assertEqual(code, 0, sk)
        reg = self.p("reg.jsonl")
        clock = {"ECO_TWIN_CLOCK": "2026-05-04T09:00:00Z"}
        code, _, err = run("registry.py", "issue", "--registry", reg, "--id", "LP-F-001", "--kind", "quantity",
                           "--target", "Jul-Aug 2026 mean chl-a, deep station (mg/m3)", "--value", "22",
                           "--lower", "14", "--upper", "31", "--interval-method", "95% regression prediction interval",
                           "--horizon-end", "2026-08-31", "--model", "TP-lag regression", "--model-version", "0.2",
                           "--inputs", "ds-03,ds-05", "--trial", env=clock)
        self.assertEqual(code, 0, err)
        index = {"name": "Lake Primernoe package", "description": "Test build",
                 "license": "https://creativecommons.org/licenses/by/4.0/",
                 "datasets": [{"id": "ds-03", "name": "Lab chemistry", "url": "https://example.org/lab",
                               "version": "2026-04", "retrieved": "2026-04-30", "license": "client"},
                              {"id": "ds-05", "name": "Inflow load", "url": "https://example.org/load",
                               "version": "v1", "retrieved": "2026-04-30", "license": "client"}],
                 "models": [{"id": "m-01", "name": "TP-lag regression", "version": "0.2"}],
                 "steps": [{"id": "st-01", "name": "Hold-out scoring", "instrument": "m-01",
                            "inputs": ["ds-03", "ds-05"], "parameters": "train 2021-2023, hold-out 2024-2025"}],
                 "outputs": [{"id": "out-01", "name": "Hold-out NSE", "value": round(sk["metrics"]["nse"], 3),
                              "produced_by": "st-01", "headline": True}]}
        with open(self.p("build.json"), "w") as fh:
            json.dump(index, fh)
        with open(self.p("report.md"), "w") as fh:
            fh.write(f"Hold-out NSE was {index['outputs'][0]['value']} [out-01]. Forecast LP-F-001 is a trial.\n")
        code, mf, _ = run("build_manifest.py", self.p("build.json"), "--out-dir", self.p("pkg"),
                          "--report", self.p("report.md"), "--registry", reg)
        self.assertEqual(code, 0, mf)
        self.assertEqual(mf["registered_forecasts"], 1)
        index["datasets"] = index["datasets"][:1]  # drop ds-05: the forecast now cites an untraceable input
        index["steps"][0]["inputs"] = ["ds-03"]
        with open(self.p("build.json"), "w") as fh:
            json.dump(index, fh)
        code, mf, _ = run("build_manifest.py", self.p("build.json"), "--check", "--registry", reg)
        self.assertEqual(code, 3)
        self.assertTrue(any("ds-05" in e for e in mf["errors"]))


class TestEvidenceSearchOffline(unittest.TestCase):
    """Normalization checked against canned API responses (no network)."""

    def setUp(self):
        self.m = load("evidence_search")

    def test_europepmc_first_author_surname(self):
        canned = json.dumps({"resultList": {"result": [{
            "title": "Cyanobacteria in lakes", "authorString": "Smith JA, Doe B.", "pubYear": "2021",
            "doi": "10.1/abc", "pmid": "123", "citedByCount": 4, "journalInfo": {"journal": {"title": "J"}}}]}})
        self.m.fetch = lambda url, params, accept="application/json": canned
        rec = self.m.search_europepmc("q", 1, "a@b.c")[0]
        self.assertEqual(rec["first_author"], "Smith")
        self.assertEqual(rec["year"], 2021)
        self.assertEqual(rec["url"], "https://europepmc.org/article/MED/123")

    def test_openalex_abstract_rebuilt(self):
        canned = json.dumps({"results": [{
            "title": "Bloom forecasting", "authorships": [{"author": {"display_name": "Ana Lima"}}],
            "abstract_inverted_index": {"Blooms": [0], "are": [1], "forecast": [2]},
            "doi": "https://doi.org/10.2/xyz", "publication_year": 2020, "cited_by_count": 9,
            "primary_location": {"source": {"display_name": "WR"}}, "id": "https://openalex.org/W1"}]})
        self.m.fetch = lambda url, params, accept="application/json": canned
        rec = self.m.search_openalex("q", 1, "a@b.c")[0]
        self.assertEqual(rec["abstract"], "Blooms are forecast")
        self.assertEqual(rec["doi"], "10.2/xyz")
        self.assertEqual(rec["first_author"], "Lima")

    def test_crossref_record(self):
        canned = json.dumps({"message": {"items": [{
            "title": ["Lake twins"], "author": [{"family": "Ivanova", "given": "Olga"}],
            "issued": {"date-parts": [[2019, 5]]}, "DOI": "10.3/q", "is-referenced-by-count": 2,
            "container-title": ["Hydrobiologia"]}]}})
        self.m.fetch = lambda url, params, accept="application/json": canned
        rec = self.m.search_crossref("q", 1, "a@b.c")[0]
        self.assertEqual((rec["first_author"], rec["year"], rec["doi"]), ("Ivanova", 2019, "10.3/q"))


class TestLintParser(unittest.TestCase):
    """The no-PyYAML fallback must still catch the v1.8 frontmatter defect."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("check_package", os.path.join(ROOT, "tests", "check_package.py"))
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self._saved = sys.modules.get("yaml")
        sys.modules["yaml"] = None  # force the fallback parser

    def tearDown(self):
        if self._saved is None:
            sys.modules.pop("yaml", None)
        else:
            sys.modules["yaml"] = self._saved

    def test_unquoted_colon_rejected(self):
        with self.assertRaises(ValueError):
            self.m.parse_yaml("name: x\ndescription: Designs twins. Full cycle: scoping\n")

    def test_nested_metadata_parsed(self):
        data, parser = self.m.parse_yaml('name: x\ndescription: "a: b"\nmetadata:\n  version: "2.0"\n')
        self.assertEqual(data["metadata"]["version"], "2.0")
        self.assertEqual(data["description"], "a: b")
        self.assertIn("minimal", parser)


class TestIndices(Tmp):
    """v2.3 water-quality indices (T30): WPI, Carlson TSI, HPI, index modes."""
    m = load("trend_test")

    def test_wpi_hand_value(self):
        r = self.m.water_pollution_index([
            {"name": "BOD5", "concentration": 6, "mac": 3},
            {"name": "NH4", "concentration": 0.4, "mac": 0.5},
            {"name": "NO3", "concentration": 9, "mac": 10},
        ])
        self.assertAlmostEqual(r["wpi"], 3.7 / 3, places=4)  # (2.0 + 0.8 + 0.9) / 3
        self.assertEqual(r["n"], 3)
        self.assertEqual(r["class"], "moderately polluted (III)")

    def test_wpi_dissolved_oxygen_inverted(self):
        r = self.m.water_pollution_index([
            {"name": "DO", "concentration": 4, "mac": 6, "dissolved_oxygen": True}])
        self.assertAlmostEqual(r["terms"][0]["ratio"], 1.5)  # MAC/C below the standard
        r = self.m.water_pollution_index([
            {"name": "DO", "concentration": 8, "mac": 6, "dissolved_oxygen": True}])
        self.assertAlmostEqual(r["terms"][0]["ratio"], 1.0)  # at/above the standard: no excess
        with self.assertRaises(ValueError):
            self.m.water_pollution_index([{"name": "X", "concentration": 1, "mac": 0}])
        with self.assertRaises(ValueError):
            self.m.water_pollution_index([])

    def test_tsi_hand_value(self):
        r = self.m.carlson_tsi(sd_m=2, chl_ug_l=10, tp_ug_l=30)
        # Hand-computed: 60-14.41*ln2; 9.81*ln10+30.6; 14.42*ln30+4.15
        self.assertAlmostEqual(r["tsi_sd"], 50.0117, places=4)
        self.assertAlmostEqual(r["tsi_chl"], 53.1884, places=4)
        self.assertAlmostEqual(r["tsi_tp"], 53.1953, places=4)
        self.assertAlmostEqual(r["tsi_composite"], 52.1318, places=4)
        self.assertEqual(r["class"], "eutrophic")

    def test_tsi_partial_and_invalid(self):
        r = self.m.carlson_tsi(sd_m=2)
        self.assertAlmostEqual(r["tsi_composite"], r["tsi_sd"])
        self.assertIsNone(r["tsi_chl"])
        self.assertEqual(r["class"], "eutrophic")  # 50.01 is in the 50-70 band
        with self.assertRaises(ValueError):
            self.m.carlson_tsi()
        with self.assertRaises(ValueError):
            self.m.carlson_tsi(chl_ug_l=0)

    def test_hpi_hand_value(self):
        r = self.m.heavy_metal_pollution_index([
            {"name": "Pb", "measured": 8, "standard": 10, "ideal": 0},
            {"name": "Cd", "measured": 2, "standard": 5, "ideal": 0},
        ])
        # W: 0.1, 0.2; Q: 80, 40; HPI = (8 + 8) / 0.3
        self.assertAlmostEqual(r["hpi"], 53.3333, places=4)
        self.assertFalse(r["critical"])
        self.assertEqual(r["threshold"], 100)

    def test_hpi_critical_and_ideal(self):
        r = self.m.heavy_metal_pollution_index([
            {"name": "Pb", "measured": 25, "standard": 10, "ideal": 0}])
        self.assertAlmostEqual(r["hpi"], 250.0)
        self.assertTrue(r["critical"])
        r = self.m.heavy_metal_pollution_index([
            {"name": "Zn", "measured": 30, "standard": 100, "ideal": 10}])
        self.assertAlmostEqual(r["hpi"], 100 * 20 / 90, places=4)  # single metal: HPI == Q
        with self.assertRaises(ValueError):
            self.m.heavy_metal_pollution_index([{"name": "X", "measured": 1, "standard": 5, "ideal": 5}])

    def test_trend_json_input(self):
        wtext(self.p("t.json"), json.dumps({
            "values": list(range(1, 13)),
            "timestamps": [f"2020-{k:02d}-01" for k in range(1, 13)]}))
        code, out, _ = run("trend_test.py", self.p("t.json"))
        self.assertEqual(code, 0)
        self.assertEqual(out["mode"], "trend")
        self.assertEqual(out["s_stat"], 66)  # strictly increasing 12 values: 12*11/2
        self.assertEqual(out["trend"], "increasing")
        self.assertLess(out["p_value"], 0.05)
        self.assertAlmostEqual(out["theil_sen_slope"], 12.0, places=1)  # +1/month
        self.assertIn("hamed_rao_factor", out)

    def test_mode_flags_cli(self):
        wtext(self.p("w.json"), json.dumps({"indicators": [
            {"name": "BOD5", "concentration": 6, "mac": 3},
            {"name": "NH4", "concentration": 0.4, "mac": 0.5}]}))
        code, out, _ = run("trend_test.py", self.p("w.json"), "--mode", "wpi")
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["wpi"], 1.4, places=4)  # (2.0 + 0.8) / 2
        wtext(self.p("h.json"), json.dumps({"metals": [
            {"name": "Pb", "measured": 25, "standard": 10, "ideal": 0}]}))
        code, out, _ = run("trend_test.py", self.p("h.json"), "--mode", "hpi")
        self.assertEqual(code, 0)
        self.assertTrue(out["critical"])
        wtext(self.p("bad.json"), json.dumps({"indicators": []}))
        code, _, err = run("trend_test.py", self.p("bad.json"), "--mode", "wpi")
        self.assertEqual(code, 2)
        self.assertIn("at least one indicator", err)


class TestSSRMSE(Tmp):
    """v2.3 SS_RMSE and admission verdict (T31)."""
    m = load("skill_scores")

    def test_ss_rmse_hand_value(self):
        self.assertAlmostEqual(self.m.ss_rmse(1.0, 2.0), 0.5)
        self.assertAlmostEqual(self.m.ss_rmse(2.0, 2.0), 0.0)
        self.assertAlmostEqual(self.m.ss_rmse(3.0, 2.0), -0.5)
        self.assertIsNone(self.m.ss_rmse(0.0, 0.0))  # perfect baseline: ratio undefined
        self.assertIsNone(self.m.ss_rmse(1.0, 0.0))

    def _persistence_model_csv(self, path):
        # sim == previous observation: the model IS the rolling persistence
        rows, d = [], date(2020, 1, 15)
        obs = [10 + k + (k % 2) for k in range(24)]
        for k, o in enumerate(obs):
            sim = obs[k - 1] if k else 10
            rows.append([d.isoformat(), o, sim])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=15)
        write_csv(path, ["time", "obs", "sim"], rows)

    def test_admission_boundary(self):
        # SS_RMSE == 0 exactly: the model ties the naive baseline, so the
        # verdict must be REJECTED (admission needs strictly > 0).
        self._persistence_model_csv(self.p("p.csv"))
        code, out, _ = run("skill_scores.py", "continuous", self.p("p.csv"),
                           "--train-end", "2020-12-31", "--season", "none")
        self.assertEqual(code, 3)  # gate fails: baseline not beaten
        self.assertAlmostEqual(out["ss_rmse"], 0.0)
        self.assertEqual(out["admission_verdict"], "REJECTED_BELOW_BENCHMARK")

    def test_good_model_admitted(self):
        rows, d = [], date(2015, 1, 15)
        import random
        rng = random.Random(11)
        for k in range(72):
            obs = 10 + 5 * math.sin(2 * math.pi * (d.month - 1) / 12) + rng.gauss(0, 1.5)
            sim = obs + (0.1 if k % 2 else -0.1)
            rows.append([d.isoformat(), f"{obs:.4f}", f"{sim:.4f}"])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=15)
        write_csv(self.p("s.csv"), ["time", "obs", "sim"], rows)
        code, out, _ = run("skill_scores.py", "continuous", self.p("s.csv"),
                           "--train-end", "2018-12-31", "--thresholds", "NSE>=0.5")
        self.assertEqual(code, 0, out)
        self.assertGreater(out["ss_rmse"], 0)
        self.assertEqual(out["admission_verdict"], "ADMITTED")
        # SS_RMSE and the MSE-ratio skill share the > 0 boundary, not the value.
        self.assertGreater(out["metrics"]["skill_vs_persistence"], 0)
        self.assertNotAlmostEqual(out["metrics"]["skill_vs_persistence"], out["ss_rmse"])
        # Cross-check: SS_RMSE == 1 - RMSE_model / sqrt(MSE_persistence).
        expect = 1 - out["metrics"]["rmse"] / math.sqrt(out["baselines"][0]["mse_baseline"])
        self.assertAlmostEqual(out["ss_rmse"], expect)

    def test_no_holdout_no_verdict(self):
        rows, d = [], date(2015, 1, 15)
        for k in range(24):
            rows.append([d.isoformat(), 10 + k, 10 + k])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=15)
        write_csv(self.p("s.csv"), ["time", "obs", "sim"], rows)
        code, out, _ = run("skill_scores.py", "continuous", self.p("s.csv"), "--no-holdout")
        self.assertEqual(code, 0)
        self.assertIsNone(out["admission_verdict"])
        self.assertIn("no admission verdict", " ".join(out["warnings"]))


class TestPackage(unittest.TestCase):
    def test_package_lint_passes(self):
        code, out, _ = run(os.path.join("..", "tests", "check_package.py"))
        self.assertEqual(code, 0, json.dumps(out["errors"] if out else None, indent=2))


if __name__ == "__main__":
    unittest.main()
