#!/usr/bin/env python3
"""
Unit tests for the bundled scripts. Standard library only; network not needed.

  python3 -m unittest discover -s tests -v      (from the skill root)

Formulas are checked against hand-computed values; CLIs are run as
subprocesses so exit codes and gate behavior are tested as an agent sees them.
"""

import collections
import csv
import importlib.util
import json
import math
import os
import random
import re
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


class TestSignposting(Tmp):
    """T34: FAIR Signposting entries in the RO-Crate manifest (Round 1 of the v2.5 program)."""

    def index(self, **over):
        idx = {
            "name": "Lake test package", "description": "Unit-test package",
            "license": "https://creativecommons.org/licenses/by/4.0/", "datePublished": "2027-10-01",
            "doi": "10.5281/zenodo.23657185",
            "datasets": [{"id": "ds-01", "name": "Sentinel-2 L2A", "url": "https://example.org/s2",
                          "version": "L2A", "retrieved": "2027-09-01", "license": "CC-BY-4.0"}],
            "models": [{"id": "m-01", "name": "TP-lag regression", "version": "0.2"}],
            "steps": [{"id": "st-01", "name": "Fit and hindcast", "instrument": "m-01",
                       "inputs": ["ds-01"]}],
            "outputs": [{"id": "out-01", "name": "Summer mean chlorophyll-a", "value": 18.2,
                         "unit": "mg/m3", "produced_by": "st-01", "headline": True}],
        }
        idx.update(over)
        with open(self.p("build.json"), "w") as fh:
            json.dump(idx, fh)
        return self.p("build.json")

    def crate_root(self, **over):
        code, out, _ = run("build_manifest.py", self.index(**over), "--out-dir", self.p("pkg"))
        self.assertEqual(code, 0, out)
        crate = json.loads(rtext(self.p("pkg/ro-crate-metadata.json")))
        return {e["@id"]: e for e in crate["@graph"]}["./"]

    def test_signposting_with_doi(self):
        root = self.crate_root()
        self.assertEqual(root["identifier"], "https://doi.org/10.5281/zenodo.23657185")
        links = {e["relation"]: e for e in root["signposting"]}
        self.assertEqual(set(links), {"cite-as", "describedby", "license"})
        self.assertEqual(links["cite-as"]["href"], "https://doi.org/10.5281/zenodo.23657185")
        self.assertEqual(links["describedby"]["href"], "ro-crate-metadata.json")
        self.assertEqual(links["describedby"]["type"], "application/ld+json")
        self.assertEqual(links["license"]["href"], "https://creativecommons.org/licenses/by/4.0/")

    def test_signposting_without_doi(self):
        path = self.index()
        with open(path) as fh:
            data = json.load(fh)
        data.pop("doi")
        with open(path, "w") as fh:
            json.dump(data, fh)
        code, out, _ = run("build_manifest.py", path, "--out-dir", self.p("pkg"))
        self.assertEqual(code, 0, out)
        crate = json.loads(rtext(self.p("pkg/ro-crate-metadata.json")))
        root = {e["@id"]: e for e in crate["@graph"]}["./"]
        self.assertNotIn("identifier", root)
        links = {e["relation"]: e for e in root["signposting"]}
        self.assertNotIn("cite-as", links)
        self.assertIn("describedby", links)
        self.assertIn("license", links)

    def test_signposting_bare_doi_and_license_forms(self):
        root = self.crate_root(doi="doi.org/10.5281/zenodo.23657185", license="CC-BY-4.0")
        self.assertEqual(root["identifier"], "https://doi.org/10.5281/zenodo.23657185")
        links = {e["relation"]: e for e in root["signposting"]}
        self.assertEqual(links["cite-as"]["href"], "https://doi.org/10.5281/zenodo.23657185")
        # a bare licence string is not a URL: no license link is invented
        self.assertNotIn("license", links)
        self.assertIn("describedby", links)


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


class TestRegistryCadenceLeadTime(Tmp):
    """T32: forecast cadence and lead time (v2.4 candidate)."""

    def clock(self, t):
        return {"ECO_TWIN_CLOCK": t}

    def issue(self, fid, *extra, at="2027-05-01T08:00:00Z", horizon="2027-08-31"):
        return run("registry.py", "issue", "--registry", self.p("reg.jsonl"), "--id", fid,
                   "--kind", "quantity", "--target", "Jul-Aug mean chl-a (mg/m3)", "--value", "18",
                   "--horizon-end", horizon, "--model", "TP-lag", "--model-version", "0.2",
                   "--inputs", "ds-03,ds-05", *extra, env=self.clock(at))

    def test_issue_records_cadence_and_lead_time(self):
        code, out, err = self.issue("C1", "--cadence", "seasonal", "--lead-time", "90",
                                    "--lead-time-unit", "days")
        self.assertEqual(code, 0, err)
        self.assertEqual(out["registered"]["cadence"], "seasonal")
        self.assertEqual(out["registered"]["lead_time"], {"value": 90.0, "unit": "days"})
        self.assertEqual(run("registry.py", "verify", "--registry", self.p("reg.jsonl"))[0], 0)

    def test_invalid_cadence_refused(self):
        code, _, err = self.issue("C1", "--cadence", "sometimes")
        self.assertEqual(code, 2)
        self.assertIn("cadence", err)

    def test_lead_time_validation(self):
        self.assertEqual(self.issue("C1", "--lead-time", "0")[0], 2)
        self.assertEqual(self.issue("C1", "--lead-time", "-5")[0], 2)
        self.assertEqual(self.issue("C1", "--lead-time-unit", "weeks")[0], 2)
        code, out, err = self.issue("C1", "--lead-time", "48", "--lead-time-unit", "hours")
        self.assertEqual(code, 0, err)
        self.assertEqual(out["registered"]["lead_time"], {"value": 48.0, "unit": "hours"})
        code, out, err = self.issue("C2", "--lead-time", "3")
        self.assertEqual(code, 0, err)
        self.assertEqual(out["registered"]["lead_time"], {"value": 3.0, "unit": "days"})

    def test_invalid_fields_fail_verify(self):
        reg = load("registry")
        base = {"type": "forecast", "id": "X1", "issued_at": "2027-05-01T08:00:00+00:00",
                "horizon_end": "2027-08-31T23:59:59+00:00", "target": "x", "kind": "quantity",
                "value": 18.0, "lower": None, "upper": None, "interval_method": None,
                "unit": None, "model": "m", "model_version": "1", "inputs": ["ds-01"],
                "metric": "abs_error", "trial": False, "supersedes": None, "clock": "system",
                "cadence": "sometimes", "lead_time": None}
        path = self.p("bad-cadence.jsonl")
        reg.append(path, dict(base), [])
        code, out, _ = run("registry.py", "verify", "--registry", path)
        self.assertEqual(code, 3)
        self.assertEqual(out["line"], 1)
        self.assertIn("cadence", out["problem"])
        bad_lead = dict(base, id="X2", cadence="weekly",
                        lead_time={"value": -1.0, "unit": "days"})
        path2 = self.p("bad-lead.jsonl")
        reg.append(path2, bad_lead, [])
        code, out, _ = run("registry.py", "verify", "--registry", path2)
        self.assertEqual(code, 3)
        self.assertEqual(out["line"], 1)
        self.assertIn("lead_time", out["problem"])

    def test_pre_v24_record_still_verifies(self):
        code, out, err = self.issue("C1")
        self.assertEqual(code, 0, err)
        self.assertIsNone(out["registered"]["cadence"])
        self.assertIsNone(out["registered"]["lead_time"])
        self.assertEqual(run("registry.py", "verify", "--registry", self.p("reg.jsonl"))[0], 0)


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


class TestOnboardingChecklist(unittest.TestCase):
    """T33: Phase 1 data-onboarding checklist (v2.4 candidate)."""

    def test_skill_checklist_present(self):
        text = rtext(os.path.join(ROOT, "SKILL.md")).lower()
        items = ["phase 1 checklist", "source and access date", "licence",
                 "resolution and coverage", "qc performed", "[нет данных]"]
        missing = [i for i in items if i not in text]
        self.assertEqual(missing, [])

    def test_passport_and_templates_carry_onboarding(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("Онбординг данных (Phase 1 checklist)", skill)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Data onboarding (Phase 1 checklist)", templates)
        self.assertIn("Refresh cadence", templates)
        self.assertIn("Usable warning lead time", templates)


class TestTaxonomyHandover(unittest.TestCase):
    """T35: scenario taxonomy, scenario card, handover note (Round 1 of the v2.5 program)."""

    def test_taxonomy_present_and_scenario_zero_unchanged(self):
        # wrapped markdown lines: collapse whitespace before matching
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        for phrase in ("Scenario 0 — the No-Action counterfactual",
                       "Planning scenarios", "What-if intervention scenarios",
                       "Storyline scenarios",
                       "A scenario without a declared class is not scored"):
            self.assertIn(phrase, skill)
        scenarios = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        self.assertIn("## Scenario taxonomy — four classes", scenarios)
        for phrase in ("Scenario 0 — No-Action counterfactual",
                       "Planning scenarios", "What-if intervention scenarios",
                       "Storyline scenarios"):
            self.assertIn(phrase, scenarios)
        counter = rtext(os.path.join(ROOT, "references", "uncertainty-decision.md"))
        self.assertIn("Freeze the no-action baseline", counter)
        self.assertIn("class 0 of the scenario taxonomy", counter)

    def test_scenario_card_and_handover(self):
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("## 6. Scenario card (Phase 5)", templates)
        self.assertIn("Class: ____ (0 No-Action counterfactual / Planning / What-if intervention / Storyline)", templates)
        self.assertIn("Handover (who maintains the twin after the author)", templates)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("Передача сопровождения (Handover)", skill)
        self.assertIn("the twelve fillable forms", skill)  # Round 4 of the v2.7 program: eleven → twelve (mismatch register entry)


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


class TestDrift(Tmp):
    """Round 2 of the v2.5 program: recalibration trigger (T36)."""
    m = load("trend_test")

    def _months(self, start, n):
        d = start
        out = []
        for _ in range(n):
            out.append(d)
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
        return out

    def _calibration(self, path):
        # Flat series, mean 10, sd ~1: no level shift, no trend to chase.
        import random
        rng = random.Random(7)
        rows = [[d.isoformat(), round(rng.gauss(10, 1.0), 3)]
                for d in self._months(date(2020, 1, 1), 24)]
        write_csv(path, ["time", "value"], rows)

    def _batch(self, path, values, qc=None):
        rows = []
        for k, d in enumerate(self._months(date(2022, 1, 1), len(values))):
            row = [d.isoformat(), values[k]]
            if qc is not None:
                row.append(qc[k])
            rows.append(row)
        write_csv(path, ["time", "value"] + (["qc_flag"] if qc is not None else []), rows)

    def _drift(self, cal, new, *extra):
        return run("trend_test.py", "--mode", "drift", "--baseline", cal, new, *extra)

    def test_level_drift_fires(self):
        self._calibration(self.p("cal.csv"))
        self._batch(self.p("new.csv"), [14 + (0.3 if k % 2 else -0.3) for k in range(10)])
        code, out, _ = self._drift(self.p("cal.csv"), self.p("new.csv"))
        self.assertEqual(code, 0, out)
        self.assertTrue(out["trigger"])
        self.assertEqual(out["action"], "recalibrate")
        self.assertTrue(out["level_fires"])
        self.assertGreater(out["drift_level"], 2.0)
        self.assertFalse(out["trend_fires"])  # flat batch: the trend component stays quiet

    def test_stable_batch_quiet(self):
        self._calibration(self.p("cal.csv"))
        self._batch(self.p("new.csv"), [10 + (0.3 if k % 2 else -0.3) for k in range(10)])
        code, out, _ = self._drift(self.p("cal.csv"), self.p("new.csv"))
        self.assertEqual(code, 0, out)
        self.assertFalse(out["trigger"])
        self.assertEqual(out["action"], "no action")
        self.assertLess(out["drift_level"], 0.5)
        self.assertFalse(out["trend_fires"])

    def test_trend_drift_fires(self):
        # Rising batch, same mean as the calibration: level stays quiet,
        # the Sen slope (about +5.3/yr) falls outside the calibration CI.
        self._calibration(self.p("cal.csv"))
        self._batch(self.p("new.csv"),
                    [round(8 + (4 / 9) * k + (0.2 if k % 2 else -0.2), 3) for k in range(10)])
        code, out, _ = self._drift(self.p("cal.csv"), self.p("new.csv"))
        self.assertEqual(code, 0, out)
        self.assertTrue(out["trigger"])
        self.assertFalse(out["level_fires"])
        self.assertLess(out["drift_level"], 0.5)
        self.assertTrue(out["trend_fires"])
        self.assertAlmostEqual(out["slope_new"], 5.34, places=1)

    def test_qc_flagged_row_excluded(self):
        # One wild row (50.0) would fire the trigger if counted; flagged
        # "range" it must be excluded and the batch stays quiet.
        self._calibration(self.p("cal.csv"))
        values = [10 + (0.3 if k % 2 else -0.3) for k in range(10)]
        flags = ["ok"] * 10
        values[5], flags[5] = 50.0, "range"
        self._batch(self.p("new.csv"), values, qc=flags)
        code, out, _ = self._drift(self.p("cal.csv"), self.p("new.csv"))
        self.assertEqual(code, 0, out)
        self.assertEqual(out["rows_excluded_qc"], 1)
        self.assertFalse(out["trigger"])

    def test_input_errors(self):
        self._calibration(self.p("cal.csv"))
        self._batch(self.p("new.csv"), [10.0] * 10)
        code, _, err = run("trend_test.py", "--mode", "drift", self.p("new.csv"))
        self.assertEqual(code, 2)  # no --baseline
        self.assertIn("--baseline", err)
        self._batch(self.p("tiny.csv"), [10.0, 10.5])
        code, _, _ = self._drift(self.p("cal.csv"), self.p("tiny.csv"))
        self.assertEqual(code, 2)  # fewer than 3 usable new values


class TestRevalidate(Tmp):
    """Round 2 of the v2.5 program: continuous revalidation (T37)."""
    m = load("skill_scores")

    def _combined(self, path, degraded=False):
        import random
        rng = random.Random(11)

        def obs_at(d):
            return 10 + 5 * math.sin(2 * math.pi * (d.month - 1) / 12)

        rows, d = [], date(2020, 1, 1)
        for _ in range(12):  # calibration year: model tracks observations
            o = obs_at(d) + rng.gauss(0, 0.5)
            rows.append([d.isoformat(), f"{o:.4f}", f"{o + 0.1:.4f}"])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
        d = date(2021, 1, 1)
        for _ in range(6):  # new batch: the model under test
            o = obs_at(d) + rng.gauss(0, 0.5)
            sim = "10.0000" if degraded else f"{o - 0.1:.4f}"
            rows.append([d.isoformat(), f"{o:.4f}", sim])
            d = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
        write_csv(path, ["time", "obs", "sim"], rows)

    def _revalidate(self, path, *extra):
        return run("skill_scores.py", "revalidate", path, "--train-end", "2020-12-31",
                   "--previous-verdict", "ADMITTED", "--previous-ss-rmse", "0.4", *extra)

    def test_good_batch_keeps_admission(self):
        self._combined(self.p("s.csv"))
        code, out, _ = self._revalidate(self.p("s.csv"))
        self.assertEqual(code, 0, out)
        self.assertGreater(out["ss_rmse"], 0.9)
        self.assertEqual(out["admission_verdict"], "ADMITTED")
        self.assertEqual(out["revalidation"]["status"], "ADMITTED")
        self.assertEqual(out["revalidation"]["transition"], "ADMITTED -> ADMITTED")
        self.assertFalse(out["revalidation"]["revoked"])
        self.assertEqual(out["revalidation"]["maturity_action"], "keep")

    def test_degraded_batch_revokes(self):
        self._combined(self.p("s.csv"), degraded=True)
        code, out, _ = self._revalidate(self.p("s.csv"))
        self.assertEqual(code, 3, out)
        self.assertLess(out["ss_rmse"], 0)
        self.assertEqual(out["admission_verdict"], "REJECTED_BELOW_BENCHMARK")
        self.assertEqual(out["revalidation"]["status"], "NOT_ADMITTED")
        self.assertEqual(out["revalidation"]["transition"], "ADMITTED -> NOT_ADMITTED")
        self.assertTrue(out["revalidation"]["revoked"])
        self.assertEqual(out["revalidation"]["maturity_action"], "drop")

    def test_train_end_required(self):
        self._combined(self.p("s.csv"))
        code, _, err = run("skill_scores.py", "revalidate", self.p("s.csv"),
                           "--previous-verdict", "ADMITTED")
        self.assertEqual(code, 2)  # argparse: --train-end is required
        self.assertIn("--train-end", err)


class TestTwoTiers(unittest.TestCase):
    """T38: EDITO two tiers — Focus Application and What-if Scenario forms (Round 3 of the v2.5 program)."""

    def test_focus_application_form(self):
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("## 7. Focus application (for builders)", templates)
        for field in ("Application ID", "Purpose", "Inputs", "Outputs",
                      "Who builds it", "Maturity level targeted", "Update cadence"):
            self.assertIn(field, templates)

    def test_what_if_form_and_skill_tiers(self):
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("## 8. What-if scenario (for decision-makers)", templates)
        for field in ("Decision ID", "The decision to be made", "Options compared",
                      "Evidence per option", "Recommendation",
                      "What would change the recommendation", "Decision-maker and date"):
            self.assertIn(field, templates)
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("Focus Applications for the builders", skill)
        self.assertIn("What-if Scenarios for the decision-makers", skill)
        self.assertIn("the twelve fillable forms", skill)  # Round 4 of the v2.7 program: eleven → twelve (mismatch register entry)


class TestExplainabilityFusion(unittest.TestCase):
    """T39: explainability under pressure and fusion checklist (Round 3 of the v2.5 program)."""

    def test_explainability_present(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        for phrase in ("what the model used, what it did not use, and how confident it is",
                       "no black-box verdicts"):
            self.assertIn(phrase, skill)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Explanation — what drove the result", templates)
        counter = rtext(os.path.join(ROOT, "references", "uncertainty-decision.md"))
        self.assertIn("Explainability under pressure", counter)
        self.assertIn("Freeze the no-action baseline", counter)

    def test_fusion_checklist_present(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        for phrase in ("fusion checklist", "cross-source consistency checks",
                       "Fusion extends the onboarding checklist"):
            self.assertIn(phrase, skill)
        skill_raw = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("Синтез источников (fusion checklist)", skill_raw)
        sources = rtext(os.path.join(ROOT, "references", "data-sources.md"))
        self.assertIn("## Multi-source fusion", sources)
        self.assertIn("## Contents", sources)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Fusion checklist (multi-source)", templates)


class TestGallery(Tmp):
    """T40: prototype gallery — one working twin per task type (Round 4 of the v2.5 program)."""

    def run_gallery(self, entry):
        out = self.p(entry)
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", entry, "run.py"),
                              "--out", out],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        summary = json.loads(res.stdout)
        self.assertEqual(summary["entry"], entry)
        self.assertTrue(os.path.exists(os.path.join(out, "summary.json")))
        return summary

    def test_pond(self):
        s = self.run_gallery("pond")
        self.assertEqual(s["maturity"], 3)
        self.assertEqual(s["tp_trend"]["direction"], "increasing")
        self.assertLess(s["tp_trend"]["p_value"], 0.01)
        self.assertAlmostEqual(s["tsi_latest"]["tsi_composite"], 65.1, delta=0.5)
        self.assertEqual(s["tsi_latest"]["class"], "eutrophic")
        self.assertEqual(s["calibration"]["gate"], "pass")
        self.assertEqual(s["calibration"]["admission_verdict"], "ADMITTED")
        self.assertGreater(s["calibration"]["ss_rmse"], 0.9)
        self.assertEqual(s["alerts"]["status"], "red")
        self.assertEqual(s["alerts"]["amber"], 3)
        self.assertEqual(s["alerts"]["red"], 1)

    def test_river(self):
        s = self.run_gallery("river")
        self.assertEqual(s["maturity"], 2)
        self.assertEqual(s["qc"]["rows_flagged"], 0)
        self.assertEqual(s["flow_trend"]["direction"], "no significant trend")
        self.assertAlmostEqual(s["flow_max_m3_s"], 625.8, delta=0.1)
        self.assertEqual(s["days_above_amber"], 9)
        self.assertEqual(s["days_above_red"], 4)
        self.assertEqual(s["alerts"]["status"], "red")
        self.assertEqual(s["alerts"]["red"], 1)

    def test_field(self):
        s = self.run_gallery("field")
        self.assertEqual(s["maturity"], 2)
        self.assertEqual(s["qc"]["rows_flagged"], 0)
        self.assertEqual(s["moisture_trend"]["direction"], "decreasing")
        self.assertLess(s["moisture_trend"]["p_value"], 0.01)
        self.assertEqual(s["days_below_amber"], 26)
        self.assertEqual(s["days_below_red"], 3)
        self.assertEqual(s["alerts"]["status"], "red")
        self.assertEqual(s["alerts"]["red"], 1)

    def test_air(self):
        # Re-located Oct 26, 2026: Ulan-Ude -> Prince George, BC (new
        # synthetic series; 10 days above amber, 4 above red).
        s = self.run_gallery("air")
        self.assertEqual(s["maturity"], 2)
        self.assertEqual(s["qc"]["rows_flagged"], 0)
        self.assertEqual(s["pm25_trend"]["direction"], "no significant trend")
        self.assertEqual(s["days_above_amber"], 10)
        self.assertEqual(s["days_above_red"], 4)
        self.assertEqual(s["alerts"]["status"], "red")
        self.assertEqual(s["alerts"]["red"], 1)

    def test_biodiversity(self):
        # Replacement Oct 26, 2026: Gusinoye (real GBIF data) removed by the
        # author's decision ('Убери гусиное'); replaced the same day with
        # Khubsugul lakeshore birds, Mongolia (synthetic records — the GBIF
        # pull was blocked, HTTP 403).
        s = self.run_gallery("biodiversity")
        self.assertEqual(s["maturity"], 2)
        self.assertEqual(s["records"], 20)
        self.assertEqual(s["species"], 18)
        self.assertEqual(s["generalized"], 19)
        self.assertEqual(s["withheld"], 1)
        self.assertEqual(s["check"]["gate"], "pass")
        self.assertEqual(s["check"]["violations"], [])
        self.assertEqual(s["cells_0_1_degree"], 4)
        self.assertEqual(s["max_species_per_cell"], 7)
        with open(os.path.join(self.p("biodiversity"), "generalized.csv"),
                  newline="") as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            if r["category"] == "extreme":
                self.assertEqual(r["decimalLatitude"], "")
                self.assertEqual(r["decimalLongitude"], "")
            elif r["decimalLatitude"]:
                self.assertRegex(r["decimalLatitude"], r"^\d+\.\d$")
                self.assertRegex(r["decimalLongitude"], r"^\d+\.\d$")

    def test_gallery_index_and_skill_reference(self):
        index = rtext(os.path.join(ROOT, "examples", "gallery.md"))
        for entry in ("pond", "river", "field", "air", "biodiversity"):
            self.assertIn(f"`{entry}/`", index)
        for phrase in ("Synthetic", "Real", "Maturity"):
            self.assertIn(phrase, index)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("`examples/gallery.md` — prototype gallery", skill)


class TestWetland(Tmp):
    """T41: wetland gallery prototype — Everglades treatment wetland + marsh (first item of the v2.6 program)."""

    def test_wetland(self):
        out = self.p("wetland")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "wetland", "run.py"),
                              "--out", out],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        summary = json.loads(res.stdout)
        self.assertEqual(summary["entry"], "wetland")
        self.assertEqual(summary["maturity"], 2)
        self.assertTrue(os.path.exists(os.path.join(out, "summary.json")))
        self.assertEqual(summary["qc"]["tp_out_rows"], 13)
        self.assertEqual(summary["qc"]["tp_out_flagged"], 0)
        self.assertEqual(summary["qc"]["level_rows"], 121)
        self.assertEqual(summary["qc"]["level_flagged"], 0)
        self.assertEqual(summary["removal"]["n_months"], 13)
        self.assertAlmostEqual(summary["removal"]["median_pct"], 35.4, delta=0.05)
        self.assertAlmostEqual(summary["removal"]["mean_pct"], 33.6, delta=0.05)
        self.assertEqual(summary["removal"]["document_mean_pct"], 33.3)
        self.assertEqual(summary["removal"]["beira_reference_median_pct"], 46.0)
        self.assertEqual(summary["removal_trend"]["direction"], "no significant trend")
        self.assertAlmostEqual(summary["removal_trend"]["p_value"], 0.227, delta=0.01)
        self.assertEqual(summary["level_trend"]["direction"], "decreasing")
        self.assertLess(summary["level_trend"]["p_value"], 0.001)
        self.assertAlmostEqual(summary["level_trend"]["sen_slope_per_year"], -2.60, delta=0.05)
        self.assertAlmostEqual(summary["level_start_ft"], 6.10, delta=0.01)
        self.assertAlmostEqual(summary["level_min_ft"], 5.26, delta=0.01)
        self.assertAlmostEqual(summary["level_end_ft"], 5.48, delta=0.01)
        self.assertEqual(summary["days_below_amber"], 14)
        self.assertEqual(summary["days_below_red"], 8)
        self.assertEqual(summary["tp_alerts"]["status"], "red")
        self.assertEqual(summary["tp_alerts"]["n_alerts"], 3)
        self.assertEqual(summary["tp_alerts"]["amber"], 1)
        self.assertEqual(summary["tp_alerts"]["red"], 2)
        self.assertEqual(summary["level_alerts"]["status"], "red")
        self.assertEqual(summary["level_alerts"]["n_alerts"], 4)
        self.assertEqual(summary["level_alerts"]["amber"], 2)
        self.assertEqual(summary["level_alerts"]["red"], 2)

    def test_wetland_index_and_skill_reference(self):
        index = rtext(os.path.join(ROOT, "examples", "gallery.md"))
        self.assertIn("`wetland/`", index)
        self.assertIn("STA-1W", index)
        self.assertIn("EDEN 10", index)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        # The gallery bullet is a living list: it names every entry, so the
        # expected ending moves with each change (the biodiversity entry was
        # removed Oct 26, 2026, 'Убери гусиное'; update this string when the
        # next entry lands).
        self.assertIn("wetland, forest-fire, forest-logging, forest-carbon)", skill)


class TestForestFire(Tmp):
    """T42: forest-fire gallery prototype — Prince Albert FMA fire seasons (second item of the v2.6 program)."""

    def test_forest_fire(self):
        out = self.p("forest-fire")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "forest-fire", "run.py"),
                              "--out", out],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        summary = json.loads(res.stdout)
        self.assertEqual(summary["entry"], "forest-fire")
        self.assertEqual(summary["maturity"], 2)
        self.assertTrue(os.path.exists(os.path.join(out, "summary.json")))
        self.assertEqual(summary["qc"]["fires_rows"], 49)
        self.assertEqual(summary["qc"]["fires_flagged"], 0)
        self.assertEqual(summary["qc"]["area_rows"], 49)
        self.assertEqual(summary["qc"]["area_flagged"], 0)
        self.assertEqual(summary["fires_trend"]["direction"], "increasing")
        self.assertAlmostEqual(summary["fires_trend"]["p_value"], 0.011, delta=0.002)
        self.assertAlmostEqual(summary["fires_trend"]["sen_slope_per_year"], 0.167, delta=0.01)
        self.assertEqual(summary["area_trend"]["direction"], "increasing")
        self.assertAlmostEqual(summary["area_trend"]["p_value"], 0.0012, delta=0.0005)
        self.assertAlmostEqual(summary["area_trend"]["sen_slope_per_year"], 210.2, delta=1.0)
        self.assertEqual(summary["biggest_season"]["year"], 2025)
        self.assertEqual(summary["biggest_season"]["fires"], 62)
        self.assertEqual(summary["biggest_season"]["burned_ha"], 128830)
        self.assertEqual(summary["months_above_amber_fires"], 13)
        self.assertEqual(summary["months_above_red_fires"], 7)
        self.assertEqual(summary["months_above_amber_area"], 17)
        self.assertEqual(summary["months_above_red_area"], 5)
        self.assertEqual(summary["fires_alerts"]["status"], "red")
        self.assertEqual(summary["fires_alerts"]["n_alerts"], 5)
        self.assertEqual(summary["fires_alerts"]["amber"], 4)
        self.assertEqual(summary["fires_alerts"]["red"], 1)
        self.assertEqual(summary["area_alerts"]["status"], "red")
        self.assertEqual(summary["area_alerts"]["n_alerts"], 5)
        self.assertEqual(summary["area_alerts"]["amber"], 4)
        self.assertEqual(summary["area_alerts"]["red"], 1)
        annual = {y["year"]: y for y in summary["annual"]}
        self.assertEqual(annual[2019]["burned_ha"], 101400)
        self.assertEqual(annual[2021]["burned_ha"], 90405)

    def test_forest_fire_index_and_skill_reference(self):
        index = rtext(os.path.join(ROOT, "examples", "gallery.md"))
        self.assertIn("`forest-fire/`", index)
        self.assertIn("Prince Albert", index)
        readme = rtext(os.path.join(ROOT, "examples", "gallery", "forest-fire", "README.md"))
        self.assertIn("FIRMS", readme)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        # Living list: the gallery bullet names every entry; the expected
        # ending moves with each new entry (forest carbon is fourth in the
        # v2.6 program; update this string when the next entry lands).
        self.assertIn("wetland, forest-fire, forest-logging, forest-carbon)", skill)


class TestForestLogging(Tmp):
    """T43: forest-logging gallery prototype — British Columbia timber supply areas (third item of the v2.6 program)."""

    def test_forest_logging(self):
        out = self.p("forest-logging")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "forest-logging", "run.py"),
                              "--out", out],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        summary = json.loads(res.stdout)
        self.assertEqual(summary["entry"], "forest-logging")
        self.assertEqual(summary["maturity"], 2)
        self.assertTrue(os.path.exists(os.path.join(out, "summary.json")))
        self.assertEqual(summary["qc"]["area_rows"], 11)
        self.assertEqual(summary["qc"]["area_flagged"], 0)
        self.assertEqual(summary["qc"]["volume_rows"], 11)
        self.assertEqual(summary["qc"]["volume_flagged"], 0)
        self.assertEqual(summary["area_trend"]["direction"], "increasing")
        self.assertAlmostEqual(summary["area_trend"]["p_value"], 0.0000516, delta=0.00001)
        self.assertAlmostEqual(summary["area_trend"]["sen_slope_per_year"], 1220.0, delta=1.0)
        self.assertEqual(summary["volume_trend"]["direction"], "increasing")
        self.assertAlmostEqual(summary["volume_trend"]["p_value"], 0.0000516, delta=0.00001)
        self.assertAlmostEqual(summary["volume_trend"]["sen_slope_per_year"], 272750.0, delta=1.0)
        self.assertEqual(summary["biggest_year"]["year"], 2025)
        self.assertEqual(summary["biggest_year"]["logged_ha"], 30600)
        self.assertEqual(summary["biggest_year"]["harvest_m3"], 6426000)
        self.assertEqual(summary["largest_district"], "Prince George")
        self.assertAlmostEqual(summary["district_shares_2015_2025"]["Prince George"], 0.47, delta=0.001)
        self.assertAlmostEqual(summary["district_shares_2015_2025"]["Quesnel"], 0.31, delta=0.001)
        self.assertAlmostEqual(summary["district_shares_2015_2025"]["Mackenzie"], 0.22, delta=0.001)
        self.assertEqual(summary["years_above_amber_area"], 4)
        self.assertEqual(summary["years_above_red_area"], 2)
        self.assertEqual(summary["years_above_amber_volume"], 4)
        self.assertEqual(summary["years_above_red_volume"], 2)
        self.assertEqual(summary["area_alerts"]["status"], "red")
        self.assertEqual(summary["area_alerts"]["n_alerts"], 2)
        self.assertEqual(summary["area_alerts"]["amber"], 1)
        self.assertEqual(summary["area_alerts"]["red"], 1)
        self.assertEqual(summary["volume_alerts"]["status"], "red")
        self.assertEqual(summary["volume_alerts"]["n_alerts"], 2)
        self.assertEqual(summary["volume_alerts"]["amber"], 1)
        self.assertEqual(summary["volume_alerts"]["red"], 1)
        annual = {y["year"]: y for y in summary["annual"]}
        self.assertEqual(annual[2015]["logged_ha"], 17900)
        self.assertEqual(annual[2015]["harvest_m3"], 3436800)
        self.assertLess(annual[2020]["logged_ha"], annual[2019]["logged_ha"])

    def test_forest_logging_index_and_skill_reference(self):
        index = rtext(os.path.join(ROOT, "examples", "gallery.md"))
        self.assertIn("`forest-logging/`", index)
        self.assertIn("Prince George", index)
        readme = rtext(os.path.join(ROOT, "examples", "gallery", "forest-logging", "README.md"))
        self.assertIn("GFW", readme)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        # Living list: the gallery bullet names every entry; the expected
        # ending moves with each new entry (forest carbon is fourth in the
        # v2.6 program; update this string when the next entry lands).
        self.assertIn("forest-fire, forest-logging, forest-carbon)", skill)


class TestForestCarbon(Tmp):
    """T44: forest-carbon gallery prototype — Prince Albert FMA carbon stock (third forest entry, fourth item of the v2.6 program)."""

    def test_forest_carbon(self):
        out = self.p("forest-carbon")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "forest-carbon", "run.py"),
                              "--out", out],
                             capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        summary = json.loads(res.stdout)
        self.assertEqual(summary["entry"], "forest-carbon")
        self.assertEqual(summary["maturity"], 2)
        self.assertTrue(os.path.exists(os.path.join(out, "summary.json")))
        self.assertEqual(summary["qc"]["density_rows"], 11)
        self.assertEqual(summary["qc"]["density_flagged"], 0)
        self.assertEqual(summary["density_trend"]["direction"], "increasing")
        self.assertAlmostEqual(summary["density_trend"]["p_value"], 0.0000262, delta=0.00001)
        self.assertAlmostEqual(summary["density_trend"]["sen_slope_per_year"], 0.208, delta=0.01)
        self.assertEqual(summary["change_trend"]["direction"], "decreasing")
        self.assertAlmostEqual(summary["change_trend"]["p_value"], 0.039, delta=0.01)
        self.assertAlmostEqual(summary["change_trend"]["sen_slope_per_year"], -0.017, delta=0.01)
        self.assertAlmostEqual(summary["start_density_t_ha"], 52.00, delta=0.01)
        self.assertAlmostEqual(summary["end_density_t_ha"], 53.92, delta=0.01)
        self.assertAlmostEqual(summary["start_stock_mt_c"], 140.40, delta=0.01)
        self.assertAlmostEqual(summary["end_stock_mt_c"], 145.58, delta=0.01)
        self.assertAlmostEqual(summary["stock_change_mt_c"], 5.18, delta=0.01)
        self.assertAlmostEqual(summary["stock_change_pct"], 3.7, delta=0.1)
        self.assertEqual(summary["years_below_amber_change"], 3)
        self.assertEqual(summary["years_below_red_change"], 0)
        self.assertEqual(summary["change_alerts"]["status"], "amber")
        self.assertEqual(summary["change_alerts"]["n_alerts"], 1)
        self.assertEqual(summary["change_alerts"]["amber"], 1)
        self.assertEqual(summary["change_alerts"]["red"], 0)
        annual = {y["year"]: y for y in summary["annual"]}
        self.assertEqual(annual[2015]["net_change_t_ha_yr"], None)
        self.assertAlmostEqual(annual[2015]["carbon_density_t_ha"], 52.00, delta=0.01)
        self.assertAlmostEqual(annual[2025]["carbon_density_t_ha"], 53.92, delta=0.01)
        self.assertAlmostEqual(annual[2025]["net_change_t_ha_yr"], 0.04, delta=0.01)

    def test_forest_carbon_index_and_skill_reference(self):
        index = rtext(os.path.join(ROOT, "examples", "gallery.md"))
        self.assertIn("`forest-carbon/`", index)
        self.assertIn("UNEP", index)
        readme = rtext(os.path.join(ROOT, "examples", "gallery", "forest-carbon", "README.md"))
        self.assertIn("Verra", readme)
        self.assertIn("synthetic", readme.lower())
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        # Living list: the gallery bullet names every entry; the expected
        # ending moves with each new entry (forest carbon is fourth in the
        # v2.6 program; update this string when the next entry lands).
        self.assertIn("forest-logging, forest-carbon)", skill)


class TestScenarioGenerate(Tmp):
    """T48: seeded scenario generator (Round 1 of the v2.7 program, Digital Baikal)."""
    m = load("scenario_generate")

    def test_fit_hand_values(self):
        mean, sd, rho = self.m.fit_ar1([10, 12, 11, 13, 12])
        self.assertAlmostEqual(mean, 11.6, places=4)
        self.assertAlmostEqual(sd, 1.140175, places=4)  # sample sd, variance 5.2/4
        self.assertAlmostEqual(rho, -0.223077, places=4)  # -1.16 / 5.2

    def test_deterministic_and_seed_sensitive(self):
        rows = [["2020-01-01", v] for v in [10, 12, 11, 13, 12, 14, 13, 15, 14, 16]]
        write_csv(self.p("d.csv"), ["time", "value"], rows)
        code, out, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "5",
                           "--seed", "42", "--out", self.p("a.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["n_series"], 5)
        self.assertEqual(out["seed"], 42)
        self.assertEqual(out["kind"], "scenario draw, not a measurement")
        first = rtext(self.p("a.csv"))
        code, out2, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "5",
                            "--seed", "42", "--out", self.p("b.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(rtext(self.p("b.csv")), first)  # same seed: byte-identical
        code, _, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "5",
                         "--seed", "7", "--out", self.p("c.csv"))
        self.assertEqual(code, 0)
        self.assertNotEqual(rtext(self.p("c.csv")), first)  # different seed: different draws
        got = read_csv(self.p("a.csv"))
        self.assertEqual(len(got), 10)  # same length as the input
        self.assertEqual(len(got[0]), 6)  # time + 5 scenarios
        # First draw of scenario 1 pins the RNG stream order: x0 = mean + sd * gauss.
        mean, sd, rho = self.m.fit_ar1([10, 12, 11, 13, 12, 14, 13, 15, 14, 16])
        rng = random.Random(42)
        self.assertAlmostEqual(float(got[0]["scenario_1"]), mean + sd * rng.gauss(0, 1), places=5)

    def test_watch_share_extremes(self):
        rows = [["2020-01-01", v] for v in [10, 12, 11, 13, 12, 14, 13, 15, 14, 16]]
        write_csv(self.p("d.csv"), ["time", "value"], rows)
        code, out, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "10",
                           "--seed", "42", "--out", self.p("w.csv"), "--watch", ">=1000")
        self.assertEqual(code, 0)
        self.assertEqual(out["watch"]["scenarios_breaching"], 0)
        self.assertEqual(out["watch"]["share"], 0.0)
        code, out, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "10",
                           "--seed", "42", "--out", self.p("w2.csv"), "--watch", "<=-1000")
        self.assertEqual(code, 0)
        self.assertEqual(out["watch"]["scenarios_breaching"], 0)
        code, out, _ = run("scenario_generate.py", self.p("d.csv"), "--n", "10",
                           "--seed", "42", "--out", self.p("w3.csv"), "--watch", ">=0")
        self.assertEqual(code, 0)
        self.assertEqual(out["watch"]["share"], 1.0)  # every generated value is positive here

    def test_input_errors(self):
        code, _, err = run("scenario_generate.py", self.p("missing.csv"), "--out", self.p("o.csv"))
        self.assertEqual(code, 2)
        write_csv(self.p("d.csv"), ["time", "value"], [["2020-01-01", 10], ["2020-01-02", 12]])
        code, _, err = run("scenario_generate.py", self.p("d.csv"), "--out", self.p("o.csv"))
        self.assertEqual(code, 2)  # fewer than 3 values
        self.assertIn("at least 3", err)
        code, _, err = run("scenario_generate.py", self.p("d.csv"), "--n", "0", "--out", self.p("o.csv"))
        self.assertEqual(code, 2)
        code, _, err = run("scenario_generate.py", self.p("d.csv"), "--out", self.p("o.csv"),
                           "--watch", "about 25")
        self.assertEqual(code, 2)

    def test_generator_documented(self):
        scenarios = rtext(os.path.join(ROOT, "references", "scenarios.md"))
        self.assertIn("## Stochastic scenario generation", scenarios)
        self.assertIn("scenario draw, never a measurement", scenarios)
        self.assertIn("scripts/scenario_generate.py", scenarios)


class TestReplay(Tmp):
    """T47: historical-event replay (Round 1 of the v2.7 program, Digital Baikal)."""
    m = load("registry")

    def _series_with_alert(self):
        # Daily values Oct 1-13: flat 10, then a sustained rise Oct 10-13.
        rows, d = [], date(2026, 10, 1)
        for k in range(13):
            v = 10 if k < 9 else 22 + 2 * (k - 9)
            rows.append([d.isoformat(), v])
            d += timedelta(days=1)
        write_csv(self.p("s.csv"), ["time", "value"], rows)
        code, out, _ = run("alert_bands.py", self.p("s.csv"), "--indicator", "flow, m3/s",
                           "--amber", ">=20", "--red", ">=30", "--window-hours", "24",
                           "--anchor", "test anchor")
        self.assertEqual(code, 0)
        self.assertEqual(len(out["alerts"]), 1)
        self.assertEqual(out["alerts"][0]["start"][:10], "2026-10-10")
        return out["alerts"][0]

    def test_replay_end_to_end_and_score_ignores_it(self):
        alert = self._series_with_alert()
        lead = (date(2026, 10, 14) - date.fromisoformat(alert["start"][:10])).days
        self.assertEqual(lead, 4)
        import shutil
        shutil.copy(os.path.join(ROOT, "examples", "beira", "registry.jsonl"), self.p("reg.jsonl"))
        code, out, _ = run("registry.py", "replay", "--registry", self.p("reg.jsonl"),
                           "--id", "TEST-R-001", "--event", "synthetic flood peak",
                           "--event-date", "2026-10-14", "--data-cutoff", "2026-10-13",
                           "--alert-fired", "yes", "--lead-time-days", str(lead),
                           "--method", "alert_bands.py --amber '>=20' --window-hours 24",
                           "--inputs", "TEST-DS", "--model", "test pipeline", "--model-version", "1")
        self.assertEqual(code, 0)
        self.assertEqual(out["registered"]["type"], "replay")
        self.assertEqual(out["registered"]["lead_time_days"], 4)
        code, out, _ = run("registry.py", "verify", "--registry", self.p("reg.jsonl"))
        self.assertEqual(code, 0)
        self.assertEqual(out, {"ok": True, "records": 2})
        code, out, _ = run("registry.py", "score", "--registry", self.p("reg.jsonl"))
        self.assertEqual(code, 0)
        self.assertEqual(out["forecasts"], [])  # replays are never scored
        self.assertTrue(out["chain"]["ok"])
        # The real Beira registry is untouched: BEIRA-F-001 alone, chain verifies.
        code, out, _ = run("registry.py", "verify", "--registry",
                           os.path.join(ROOT, "examples", "beira", "registry.jsonl"))
        self.assertEqual(code, 0)
        self.assertEqual(out, {"ok": True, "records": 1})

    def test_replay_refusals(self):
        import shutil
        shutil.copy(os.path.join(ROOT, "examples", "beira", "registry.jsonl"), self.p("reg.jsonl"))
        base = ["registry.py", "replay", "--registry", self.p("reg.jsonl"),
                "--id", "TEST-R-002", "--event", "synthetic flood peak",
                "--event-date", "2026-10-14", "--data-cutoff", "2026-10-13",
                "--method", "alert_bands.py", "--inputs", "TEST-DS",
                "--model", "test pipeline", "--model-version", "1"]
        code, _, err = run(*base, "--alert-fired", "yes", "--lead-time-days", "4")
        self.assertEqual(code, 0)  # valid record registered
        code, _, err = run(*base, "--alert-fired", "yes", "--lead-time-days", "4")
        self.assertEqual(code, 2)  # duplicate id
        self.assertIn("already registered", err)
        code, _, err = run("registry.py", "replay", "--registry", self.p("reg.jsonl"),
                           "--id", "TEST-R-003", "--event", "synthetic flood peak",
                           "--event-date", "2026-10-14", "--data-cutoff", "2026-10-15",
                           "--alert-fired", "yes", "--lead-time-days", "1",
                           "--method", "m", "--inputs", "TEST-DS",
                           "--model", "m", "--model-version", "1")
        self.assertEqual(code, 2)  # cutoff after the event: the pipeline would see it
        self.assertIn("on or before the event date", err)
        code, _, err = run("registry.py", "replay", "--registry", self.p("reg.jsonl"),
                           "--id", "TEST-R-004", "--event", "synthetic flood peak",
                           "--event-date", "2026-10-14", "--data-cutoff", "2026-10-13",
                           "--alert-fired", "yes",
                           "--method", "m", "--inputs", "TEST-DS",
                           "--model", "m", "--model-version", "1")
        self.assertEqual(code, 2)  # fired alert with no lead time
        self.assertIn("needs --lead-time-days", err)
        code, _, err = run("registry.py", "replay", "--registry", self.p("reg.jsonl"),
                           "--id", "TEST-R-005", "--event", "synthetic flood peak",
                           "--event-date", "2026-10-14", "--data-cutoff", "2026-10-13",
                           "--alert-fired", "no", "--lead-time-days", "2",
                           "--method", "m", "--inputs", "TEST-DS",
                           "--model", "m", "--model-version", "1")
        self.assertEqual(code, 2)  # a miss has no lead time
        self.assertIn("has no lead time", err)

    def test_replay_protocol_documented(self):
        doc = rtext(os.path.join(ROOT, "references", "uncertainty-decision.md"))
        self.assertIn("5. Historical-event replay", doc)
        self.assertIn("## 5. Historical-event replay", doc)
        self.assertIn("Cut the data at the last observation before the event", doc)
        self.assertIn("A miss is a finding, not a failure to report", doc)
        self.assertIn("Boundary — replay vs storyline", doc)
        self.assertIn("registry.py replay", doc)


class TestHazardQuotientIndex(Tmp):
    """T49: hazard quotient / hazard index (Round 1 of the v2.7 program, Digital Baikal)."""
    m = load("trend_test")

    def test_bychkov_fire_smoke_acute_triple(self):
        out = self.m.hazard_quotient_index([
            {"name": "suspended solids", "exposure": 11.3, "reference": 1.0, "duration": "acute"},
            {"name": "formaldehyde", "exposure": 0.14, "reference": 0.1, "duration": "acute"},
            {"name": "carbon monoxide", "exposure": 12, "reference": 10, "duration": "acute"},
        ])
        self.assertAlmostEqual(out["hi"], 13.9, places=4)  # 11.3 + 1.4 + 1.2
        self.assertAlmostEqual(out["hi_acute"], 13.9, places=4)
        self.assertAlmostEqual(out["hi_chronic"], 0.0, places=4)
        self.assertTrue(out["unsafe"])
        self.assertTrue(out["unsafe_acute"])
        self.assertEqual(out["threshold"], 1)
        self.assertAlmostEqual(out["terms"][0]["hq"], 11.3, places=4)

    def test_safe_case_and_chronic_split(self):
        out = self.m.hazard_quotient_index([
            {"name": "PM2.5", "exposure": 10, "reference": 25, "duration": "chronic", "target": "respiratory"},
            {"name": "NO2", "exposure": 20, "reference": 40, "duration": "chronic"},
        ])
        self.assertAlmostEqual(out["hi"], 0.9, places=4)  # 0.4 + 0.5
        self.assertFalse(out["unsafe"])
        self.assertEqual(out["terms"][0]["target"], "respiratory")

    def test_input_errors(self):
        with self.assertRaises(ValueError):
            self.m.hazard_quotient_index([])
        with self.assertRaises(ValueError):
            self.m.hazard_quotient_index([{"name": "x", "exposure": 1, "reference": 0}])
        with self.assertRaises(ValueError):
            self.m.hazard_quotient_index([{"name": "x", "exposure": -1, "reference": 1}])
        with self.assertRaises(ValueError):
            self.m.hazard_quotient_index([{"name": "x", "exposure": 1, "reference": 1, "duration": "subacute"}])
        with self.assertRaises(ValueError):
            self.m.hazard_quotient_index([{"name": "x", "exposure": 1}])  # no reference

    def test_cli_mode(self):
        with open(self.p("hq.json"), "w") as fh:
            json.dump({"stressors": [
                {"name": "suspended solids", "exposure": 11.3, "reference": 1.0, "duration": "acute"},
                {"name": "formaldehyde", "exposure": 0.14, "reference": 0.1, "duration": "acute"},
                {"name": "carbon monoxide", "exposure": 12, "reference": 10, "duration": "acute"},
            ]}, fh)
        code, out, _ = run("trend_test.py", self.p("hq.json"), "--mode", "hq")
        self.assertEqual(code, 0)
        self.assertEqual(out["mode"], "hq")
        self.assertAlmostEqual(out["hi"], 13.9, places=4)
        with open(self.p("bad.json"), "w") as fh:
            json.dump({"stressors": []}, fh)
        code, _, _ = run("trend_test.py", self.p("bad.json"), "--mode", "hq")
        self.assertEqual(code, 2)

    def test_hq_documented(self):
        indicators = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("### Hazard quotient and hazard index (HQ/HI)", indicators)
        self.assertIn("1 is the safety line", indicators)
        self.assertIn("same quotient family as HPI", indicators)
        self.assertIn("11.3", indicators)


class TestCovariateAwareAlerts(Tmp):
    """T50: covariate-aware alerts (Round 1 of the v2.7 program, Southern Water)."""
    m = load("alert_bands")

    def series(self, values, name="s.csv"):
        rows = [[f"2027-07-{k + 1:02d}T00:00:00", v] for k, v in enumerate(values)]
        write_csv(self.p(name), ["time", "value"], rows)
        return self.p(name)

    def alert(self, path, *extra):
        return run("alert_bands.py", path, "--indicator", "turbidity, NTU",
                   "--amber", ">=25", "--red", ">=50", "--window-hours", "24",
                   "--anchor", "test anchor", *extra)

    def test_breach_explained_by_driver(self):
        main = self.series([10, 10, 30, 32, 31, 33, 10, 10, 10, 10])
        driver = self.series([0, 0, 40, 42, 41, 43, 0, 0, 0, 0], "d.csv")
        code, out, _ = self.alert(main, "--explained-by", driver, "--driver-amber", ">=25")
        self.assertEqual(code, 0)
        self.assertEqual(out["status"], "green")  # the only breach was explained
        self.assertEqual(out["alerts"], [])
        self.assertEqual(len(out["explained_breaches"]), 1)
        expl = out["explained_breaches"][0]
        self.assertEqual(expl["band"], "amber")
        self.assertEqual(expl["explained_by"]["driver_band"], "amber")
        self.assertEqual(expl["explained_by"]["driver_start"][:10], "2027-07-03")
        self.assertEqual(expl["explained_by"]["driver_threshold"], ">=25.0")

    def test_breach_unexplained_without_driver_episode(self):
        main = self.series([10, 10, 30, 32, 31, 33, 10, 10, 10, 10])
        driver = self.series([0] * 10, "d.csv")
        code, out, _ = self.alert(main, "--explained-by", driver, "--driver-amber", ">=25")
        self.assertEqual(code, 0)
        self.assertEqual(out["status"], "amber")
        self.assertEqual(len(out["alerts"]), 1)
        self.assertEqual(out["explained_breaches"], [])

    def test_driver_spike_explains_nothing(self):
        main = self.series([10, 10, 30, 32, 31, 33, 10, 10, 10, 10])
        driver = self.series([0, 0, 0, 0, 0, 40, 0, 0, 0, 0], "d.csv")  # one high reading, not sustained
        code, out, _ = self.alert(main, "--explained-by", driver, "--driver-amber", ">=25")
        self.assertEqual(code, 0)
        self.assertEqual(out["status"], "amber")
        self.assertEqual(len(out["alerts"]), 1)
        self.assertEqual(out["explained_breaches"], [])

    def test_fail_on_considers_unexplained_only(self):
        main = self.series([10, 10, 30, 32, 31, 33, 10, 10, 10, 10])
        driver = self.series([0, 0, 40, 42, 41, 43, 0, 0, 0, 0], "d.csv")
        code, out, _ = self.alert(main, "--explained-by", driver, "--driver-amber", ">=25",
                                  "--fail-on", "amber")
        self.assertEqual(code, 0)  # explained breach does not fail
        driver2 = self.series([0] * 10, "d2.csv")
        code, out, _ = self.alert(main, "--explained-by", driver2, "--driver-amber", ">=25",
                                  "--fail-on", "amber")
        self.assertEqual(code, 3)  # unexplained breach fails

    def test_explained_by_input_errors(self):
        main = self.series([10, 10, 30, 32, 31, 33, 10, 10, 10, 10])
        code, _, err = self.alert(main, "--explained-by", self.p("d.csv"))
        self.assertEqual(code, 2)  # no driver band
        self.assertIn("--driver-amber", err)
        code, _, _ = self.alert(main, "--explained-by", self.p("missing.csv"),
                                "--driver-amber", ">=25")
        self.assertEqual(code, 2)
        write_csv(self.p("d.csv"), ["time", "rain"], [[f"2027-07-{k + 1:02d}T00:00:00", 0] for k in range(10)])
        code, _, err = self.alert(main, "--explained-by", self.p("d.csv"), "--driver-amber", ">=25")
        self.assertEqual(code, 2)  # default driver column 'value' is absent
        self.assertIn("driver column 'value'", err)

    def test_covariate_rule_documented(self):
        indicators = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("## 20. Watch levels and alert rules", indicators)
        self.assertIn("20 Watch levels and alert rules", indicators)
        self.assertIn("Covariate-aware alerts", indicators)
        self.assertIn("driver spike explains nothing", indicators)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Alerts — alerts fired", templates)
        self.assertIn("--explained-by", templates)


class TestAlertTrial(Tmp):
    """T51: alert trial (Round 1 of the v2.7 program, Southern Water)."""
    m = load("skill_scores")

    def trial(self, rows, *extra):
        write_csv(self.p("t.csv"), ["kind", "relevant"], rows)
        return run("skill_scores.py", "alert-trial", self.p("t.csv"), *extra)

    def test_pass_wessex_shape(self):
        rows = [["alert", 1]] * 9 + [["alert", 0]] + [["critical_event", 1]] * 2
        code, out, _ = self.trial(rows)
        self.assertEqual(code, 0)
        self.assertEqual(out["verdict"], "PASS")
        self.assertEqual(out["precision"], 0.9)
        self.assertEqual(out["n_missed_criticals"], 0)
        self.assertEqual(out["miss_rate"], 0.0)
        self.assertEqual(out["alarm_volume"], 10)

    def test_fail_precision(self):
        rows = [["alert", 1]] * 8 + [["alert", 0]] * 2
        code, out, _ = self.trial(rows)
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertEqual(out["precision"], 0.8)
        self.assertIn("below the minimum", out["failures"][0])

    def test_fail_missed_critical(self):
        rows = [["alert", 1]] * 10 + [["critical_event", 1], ["critical_event", 0]]
        code, out, _ = self.trial(rows)
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertEqual(out["n_missed_criticals"], 1)
        self.assertEqual(out["miss_rate"], 0.5)

    def test_fail_alarm_volume(self):
        rows = [["alert", 1]] * 10
        code, out, _ = self.trial(rows, "--max-alarms", "5")
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertIn("above the cap", out["failures"][0])

    def test_fail_no_alerts(self):
        rows = [["critical_event", 1]] * 2
        code, out, _ = self.trial(rows)
        self.assertEqual(code, 3)  # a silent trial proves nothing
        self.assertEqual(out["verdict"], "FAIL")
        self.assertIsNone(out["precision"])
        self.assertIn("no alerts", out["failures"][0])

    def test_quiet_window_inconclusive(self):
        # A window with no alerts and no critical events is not a failure:
        # nothing to score, so the verdict is INCONCLUSIVE_QUIET_WINDOW
        # (exit 0) — it neither admits nor rejects.
        code, out, _ = self.trial([])
        self.assertEqual(code, 0)
        self.assertEqual(out["verdict"], "INCONCLUSIVE_QUIET_WINDOW")
        self.assertEqual(out["n_alerts"], 0)
        self.assertEqual(out["n_critical_events"], 0)
        self.assertIsNone(out["precision"])
        self.assertIsNone(out["miss_rate"])
        self.assertEqual(out["alarm_volume"], 0)
        self.assertEqual(out["failures"], [])
        self.assertIn("neither admits nor rejects", out["note"])

    def test_criticals_without_alerts_still_fail(self):
        # Critical events with no alerts: the model stayed silent when it
        # mattered — still a FAIL, unlike the quiet window.
        rows = [["critical_event", 0]]
        code, out, _ = self.trial(rows)
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertEqual(out["n_missed_criticals"], 1)
        self.assertEqual(out["miss_rate"], 1.0)
        self.assertIn("no alerts", out["failures"][0])

    def test_input_errors(self):
        code, _, err = self.trial([["warning", 1]])
        self.assertEqual(code, 2)
        self.assertIn("kind must be", err)
        code, _, err = self.trial([["alert", "maybe"]])
        self.assertEqual(code, 2)
        self.assertIn("relevant must be", err)
        write_csv(self.p("t.csv"), ["kind"], [["alert"]])
        code, _, err = run("skill_scores.py", "alert-trial", self.p("t.csv"))
        self.assertEqual(code, 2)
        with open(self.p("t.csv"), "w") as fh:
            fh.write("kind,relevant\n")
        # A header-only file is a quiet window, not an input error:
        # INCONCLUSIVE_QUIET_WINDOW, exit 0 (see test_quiet_window_inconclusive).
        code, out, _ = run("skill_scores.py", "alert-trial", self.p("t.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["verdict"], "INCONCLUSIVE_QUIET_WINDOW")

    def test_alert_trial_documented(self):
        doc = rtext(os.path.join(ROOT, "references", "uncertainty-decision.md"))
        self.assertIn("Alerts are trialled separately from the model", doc)
        self.assertIn("alert-trial", doc)
        self.assertIn("both must pass", doc)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("alert trial verdict", templates)
        self.assertIn("skill_scores.py alert-trial", templates)


class TestAdmit(Tmp):
    """T52: calibration plausibility gate (Round 1 of the v2.7 program, lake platforms)."""
    m = load("skill_scores")

    def admit(self, dossier, *extra):
        with open(self.p("d.json"), "w") as fh:
            json.dump(dossier, fh)
        return run("skill_scores.py", "admit", self.p("d.json"), *extra)

    def dossier(self, ss=(0.42, 0.31), growth=0.55):
        return {"variables": [{"name": "TP", "ss_rmse": ss[0]},
                              {"name": "chl-a", "ss_rmse": ss[1]}],
                "parameters": [{"name": "growth_rate", "value": growth, "bounds": [0.2, 2.0],
                                "source": "Reynolds 2006"}]}

    def test_admit_clean(self):
        code, out, _ = self.admit(self.dossier())
        self.assertEqual(code, 0)
        self.assertEqual(out["verdict"], "ADMITTED")
        self.assertEqual(out["failures"], [])

    def test_reject_parameter_outside_bounds_even_when_ss_rmse_positive(self):
        code, out, _ = self.admit(self.dossier(growth=3.5))
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "REJECTED")
        self.assertEqual(len(out["failures"]), 1)
        self.assertIn("growth_rate", out["failures"][0])
        self.assertIn("outside declared bounds", out["failures"][0])
        self.assertIn("Reynolds 2006", out["failures"][0])

    def test_reject_variable_below_benchmark(self):
        code, out, _ = self.admit(self.dossier(ss=(0.42, -0.05)))
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "REJECTED")
        self.assertIn("chl-a", out["failures"][0])
        self.assertIn("SS_RMSE", out["failures"][0])

    def test_secondary_variable_below_benchmark_does_not_block(self):
        # A secondary background variable (buffered pH) below the benchmark
        # does not block admission when every primary variable passes.
        dossier = {"variables": [{"name": "TP", "ss_rmse": 0.42, "primary": True},
                                 {"name": "pH", "ss_rmse": -0.05, "primary": False}],
                   "parameters": [{"name": "growth_rate", "value": 0.55, "bounds": [0.2, 2.0],
                                   "source": "Reynolds 2006"}]}
        code, out, _ = self.admit(dossier)
        self.assertEqual(code, 0)
        self.assertEqual(out["verdict"], "ADMITTED")
        self.assertEqual(out["failures"], [])
        self.assertEqual(out["variables"][0]["primary"], True)
        self.assertEqual(out["variables"][1]["primary"], False)

    def test_primary_variable_below_benchmark_rejects(self):
        # A PRIMARY variable below the benchmark still rejects, and the
        # verdict names the offending primary variable.
        dossier = {"variables": [{"name": "TP", "ss_rmse": -0.05, "primary": True},
                                 {"name": "chl-a", "ss_rmse": 0.31, "primary": False}],
                   "parameters": [{"name": "growth_rate", "value": 0.55, "bounds": [0.2, 2.0],
                                   "source": "Reynolds 2006"}]}
        code, out, _ = self.admit(dossier)
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "REJECTED")
        self.assertIn("TP", out["failures"][0])
        self.assertIn("SS_RMSE", out["failures"][0])

    def test_no_primary_flags_means_all_primary(self):
        # Backward compatibility: when no variable carries a "primary"
        # flag, every variable is primary (the pre-2.7 behaviour) — a
        # background variable below the benchmark then blocks admission,
        # and the output echoes every variable as primary.
        dossier = {"variables": [{"name": "TP", "ss_rmse": 0.42},
                                 {"name": "pH", "ss_rmse": -0.05}],
                   "parameters": [{"name": "growth_rate", "value": 0.55, "bounds": [0.2, 2.0],
                                   "source": "Reynolds 2006"}]}
        code, out, _ = self.admit(dossier)
        self.assertEqual(code, 3)
        self.assertEqual(out["verdict"], "REJECTED")
        self.assertTrue(all(v["primary"] for v in out["variables"]))
        self.assertIn("pH", out["failures"][0])

    def test_input_errors(self):
        code, _, err = self.admit({"variables": [], "parameters": []})
        self.assertEqual(code, 2)
        code, _, err = self.admit({"variables": [{"name": "TP"}],
                                   "parameters": []})
        self.assertEqual(code, 2)  # no ss_rmse
        code, _, err = self.admit({"variables": [{"name": "TP", "ss_rmse": 0.4}],
                                   "parameters": [{"name": "g", "value": 0.5,
                                                   "bounds": [2.0, 0.2]}]})
        self.assertEqual(code, 2)  # inverted bounds
        with open(self.p("d.json"), "w") as fh:
            fh.write("{not json")
        code, _, _ = run("skill_scores.py", "admit", self.p("d.json"))
        self.assertEqual(code, 2)
        code, _, _ = run("skill_scores.py", "admit", self.p("missing.json"))
        self.assertEqual(code, 2)

    def test_plausibility_gate_documented(self):
        bounds = rtext(os.path.join(ROOT, "references", "calibration-bounds.md"))
        self.assertIn("Bounds come from the literature, not from the fit", bounds)
        self.assertIn("0.2–2.0 d⁻¹", bounds)
        self.assertIn("Reynolds", bounds)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("Admission has two", skill)
        self.assertIn("gates, both must pass", skill)
        self.assertIn("references/calibration-bounds.md", skill)
        self.assertIn("`references/calibration-bounds.md`", skill)  # Companion Documents


class TestStoryline(unittest.TestCase):
    """T46: event storyline scenario class (Round 1 of the v2.7 program, DestinE)."""

    def test_storyline_class_construction_rule_and_boundary(self):
        scenarios = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        for phrase in ("Storyline scenarios",
                       "named historical extreme event from the object's own record",
                       "state the drivers changed and what is held fixed",
                       "state the impact scored",
                       "combine two drivers at once",
                       "Boundary — storyline vs replay",
                       "replays an event under CHANGED drivers",
                       "never substitute for each other"):
            self.assertIn(phrase, scenarios)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Storyline (Storyline class only)", templates)
        self.assertIn("drivers changed", templates)
        self.assertIn("impact scored", templates)


class TestImpactChain(unittest.TestCase):
    """T45: impact chains (Round 1 of the v2.7 program, DestinE)."""

    def test_impact_chain_section_and_card_field(self):
        scenarios = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        self.assertIn("## Impact chains", scenarios)
        for phrase in ("hazard", "exposure", "vulnerability", "impact",
                       "published impact function", "applicable range",
                       "goes to the [НЕТ ДАННЫХ] register",
                       "impact-based watch levels"):
            self.assertIn(phrase, scenarios)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Impact chain — driver", templates)
        self.assertIn("a link with no published function goes to the [НЕТ ДАННЫХ] register", templates)


class TestVirtualSensor(unittest.TestCase):
    """T53: virtual sensors (Round 2 of the v2.7 program, Gironde)."""

    def test_virtual_sensor_block_in_passport(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        for phrase in ("Virtual sensors (registered proxy sensors)",
                       "physical quantity",
                       "proxy source + deterministic formula",
                       "calibration station",
                       "skill score against the station (SS_RMSE)",
                       "validity window",
                       "QC and alert machinery as a physical sensor",
                       "when the proxy leaves calibration, its readings go to the [НЕТ ДАННЫХ] register"):
            self.assertIn(phrase, templates)

    def test_satellite_proxies_listed_as_virtual_sensor_sources(self):
        sources = " ".join(rtext(os.path.join(ROOT, "references", "data-sources.md")).split())
        self.assertIn("Satellite proxies as virtual sensors", sources)
        self.assertIn("Sentinel-2 chlorophyll-a", sources)
        self.assertIn("registered virtual sensor in the passport", sources)
        self.assertIn("its readings go to the [НЕТ ДАННЫХ] register when it leaves calibration", sources)


class TestDriftModule(Tmp):
    """T54: deterministic drift / connectivity (Round 2 of the v2.7 program, EDITO)."""
    m = load("drift")

    def files(self):
        write_csv(self.p("rel.csv"), ["id", "lat", "lon"],
                  [["R1", "50.0", "100.0"], ["R2", "50.0", "101.0"]])
        write_csv(self.p("cur.csv"), ["time", "u", "v"],
                  [["2027-01-01T00:00:00", "0.5", "0"]])
        write_csv(self.p("tgt.csv"), ["zone", "lat_min", "lat_max", "lon_min", "lon_max"],
                  [["intake", "49.9", "50.1", "100.1", "100.2"]])
        return self.p("rel.csv"), self.p("cur.csv"), self.p("tgt.csv")

    def drift(self, *extra):
        rel, cur, tgt = self.files()
        return run("drift.py", "--release", rel, "--currents", cur, "--targets", tgt, *extra)

    def test_connectivity_and_travel_time(self):
        # 0.5 m/s east = 0.025152 deg lon/hour at 50 N; 0.1 deg takes 4 steps.
        code, out, _ = self.drift()
        self.assertEqual(code, 0)
        self.assertEqual(out["released"], 2)
        self.assertEqual(out["zones"][0]["zone"], "intake")
        self.assertEqual(out["zones"][0]["arrivals"], 1)
        self.assertAlmostEqual(out["zones"][0]["connectivity"], 0.5)
        self.assertEqual(out["zones"][0]["median_travel_hours"], 4.0)
        self.assertEqual(out["particles"][0]["travel_hours"], 4.0)
        self.assertIsNone(out["particles"][1]["arrived_zone"])
        self.assertIsNone(out["particles"][1]["travel_hours"])

    def test_wind_leeway_speeds_arrival(self):
        # leeway 0.5 x wind-u 1.0 m/s doubles the eastward speed: 2 steps.
        code, out, _ = self.drift("--wind-u", "1.0", "--leeway", "0.5", "--max-hours", "10")
        self.assertEqual(code, 0)
        self.assertEqual(out["zones"][0]["median_travel_hours"], 2.0)
        self.assertEqual(out["particles"][0]["travel_hours"], 2.0)

    def test_no_arrival_reports_null(self):
        write_csv(self.p("tgt2.csv"), ["zone", "lat_min", "lat_max", "lon_min", "lon_max"],
                  [["far", "49.9", "50.1", "105.0", "105.1"]])
        rel, cur, _ = self.files()
        code, out, _ = run("drift.py", "--release", rel, "--currents", cur,
                           "--targets", self.p("tgt2.csv"), "--max-hours", "10")
        self.assertEqual(code, 0)
        self.assertEqual(out["zones"][0]["connectivity"], 0.0)
        self.assertIsNone(out["zones"][0]["median_travel_hours"])
        self.assertEqual([p["arrived_zone"] for p in out["particles"]], [None, None])

    def test_input_errors(self):
        rel, cur, tgt = self.files()
        code, _, err = run("drift.py", "--release", self.p("missing.csv"),
                           "--currents", cur, "--targets", tgt)
        self.assertEqual(code, 2)
        write_csv(self.p("bad.csv"), ["id", "lat"], [["R1", "50.0"]])
        code, _, err = run("drift.py", "--release", self.p("bad.csv"),
                           "--currents", cur, "--targets", tgt)
        self.assertEqual(code, 2)
        self.assertIn("column 'lon'", err)
        code, _, _ = run("drift.py", "--release", rel, "--currents", cur,
                         "--targets", tgt, "--leeway", "-0.5")
        self.assertEqual(code, 2)
        code, _, _ = run("drift.py", "--release", rel, "--currents", cur,
                         "--targets", tgt, "--max-hours", "0")
        self.assertEqual(code, 2)

    def test_drift_documented(self):
        # T92: the I/O table moved from SKILL.md to references/scripts.md;
        # the content is pinned there, SKILL.md keeps only the pointer.
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("`scripts/drift.py`", skill)
        table = rtext(os.path.join(ROOT, "references", "scripts.md"))
        self.assertIn("connectivity", table)
        self.assertIn("median_travel_hours", table)


class TestForecastBulletin(Tmp):
    """T55: daily forecast bulletin (Round 2 of the v2.7 program, Gironde)."""
    m = load("forecast_bulletin")

    def registry_with_forecast(self):
        reg = self.p("r.jsonl")
        code, out, _ = run("registry.py", "issue", "--registry", reg,
                           "--id", "TEST-F-001", "--kind", "quantity",
                           "--target", "TP, ug/L, test lake", "--value", "45",
                           "--lower", "40", "--upper", "50",
                           "--interval-method", "bootstrap", "--unit", "ug/L",
                           "--horizon-end", "2027-12-31", "--model", "persistence",
                           "--model-version", "1", "--inputs", "M1",
                           "--metric", "abs_error", "--cadence", "weekly",
                           "--lead-time", "7", "--lead-time-unit", "days")
        self.assertEqual(code, 0, out)
        write_csv(self.p("obs.csv"), ["time", "value"],
                  [["2027-06-01", "38"], ["2027-06-02", "41"], ["2027-06-03", "44"]])
        return reg

    def test_bulletin_renders_registry_entry_and_latest_observation(self):
        reg = self.registry_with_forecast()
        code, _, err = run("forecast_bulletin.py", "--registry", reg,
                           "--id", "TEST-F-001", "--observations", self.p("obs.csv"),
                           "--amber", ">=40", "--red", ">=50",
                           "--output", self.p("bul.md"))
        self.assertEqual(code, 0, err)
        text = rtext(self.p("bul.md"))
        for phrase in ("# Forecast bulletin — TEST-F-001",
                       "Target: TP, ug/L, test lake",
                       "Observed value today: 44.0 ug/L (latest observation, 2027-06-03)",
                       "Forecast: 45.0 ug/L (interval 40.0–50.0 ug/L, bootstrap)",
                       "Watch status: latest observation amber (amber >=40, red >=50); forecast value amber",
                       "will be scored on 2027-12-31",
                       "against the abs_error metric, exactly as issued",
                       "usable warning lead time: 7.0 days"):
            self.assertIn(phrase, text)

    def test_bulletin_without_bands_states_status_not_stated(self):
        reg = self.registry_with_forecast()
        code, _, err = run("forecast_bulletin.py", "--registry", reg,
                           "--id", "TEST-F-001", "--observations", self.p("obs.csv"),
                           "--output", self.p("bul.md"))
        self.assertEqual(code, 0, err)
        self.assertIn("Watch status: not stated (no bands given)", rtext(self.p("bul.md")))

    def test_bulletin_input_errors(self):
        reg = self.registry_with_forecast()
        code, _, err = run("forecast_bulletin.py", "--registry", reg,
                           "--id", "NOPE", "--observations", self.p("obs.csv"))
        self.assertEqual(code, 2)
        self.assertIn("not in the registry", err)
        code, _, err = run("forecast_bulletin.py", "--registry", reg,
                           "--id", "TEST-F-001", "--observations", self.p("missing.csv"))
        self.assertEqual(code, 2)
        code, _, err = run("forecast_bulletin.py", "--registry", reg,
                           "--id", "TEST-F-001", "--observations", self.p("obs.csv"),
                           "--amber", "25")
        self.assertEqual(code, 2)
        self.assertIn("--amber must look like", err)

    def test_bulletin_form_in_templates(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("## 9. Forecast bulletin", templates)
        for phrase in ("Observed value today", "Forecast value (and interval",
                       "Watch status (of the latest observation and of the forecast value",
                       "Date the forecast will be scored (horizon end)",
                       "Trial forecast (no decision weight)?",
                       "Generated by: `scripts/forecast_bulletin.py`"):
            self.assertIn(phrase, templates)


class TestPublicStatusLine(unittest.TestCase):
    """T56: public status line (Round 2 of the v2.7 program, Southern Water)."""

    def test_status_line_form_in_templates(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("## 10. Public status line", templates)
        for phrase in ("One paragraph in plain language",
                       "generated from the runner's summary JSON",
                       "Current state:",
                       "What changed since the last status line:",
                       "Maturity label",
                       "Gaps ([НЕТ ДАННЫХ]):",
                       "distinct from the handover note",
                       "and from RO-Crate (for machines)"):
            self.assertIn(phrase, templates)

    def test_skill_requires_a_status_line_per_twin(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("Every twin also ships a public status line", skill)
        self.assertIn("`assets/templates.md` §10", skill)
        self.assertIn("it is for the client and the public", skill)


class TestDecisionProduct(unittest.TestCase):
    """T57: one product per audience + dissemination register (Round 2 of the v2.7 program, Patos)."""

    def test_decision_product_form(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("## 11. Decision product", templates)
        for phrase in ("One product per audience",
                       "Audience (who it is for):",
                       "Thresholds (the levels that trigger this product's message):",
                       "Format (map / bulletin / table / message):",
                       "Channel (WhatsApp / email / app / public board / TV):",
                       "Refresh cadence (daily / weekly / event-driven):"):
            self.assertIn(phrase, templates)

    def test_dissemination_register_in_passport(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Dissemination register (who receives which product, by what channel)", templates)
        self.assertIn("who receives it", templates)

    def test_twelve_forms_counted(self):
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("# Templates — the twelve fillable forms", templates)
        self.assertIn("## 12. Mismatch register entry", templates)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("the twelve fillable forms", skill)


class TestAssetClearance(Tmp):
    """T58: asset-relative safety margin (Round 2 of the v2.7 program, Patos)."""
    m = load("registry")

    def issue(self, reg, value="2.4", clearance=None):
        args = ["registry.py", "issue", "--registry", reg,
                "--id", "TEST-C-001", "--kind", "quantity",
                "--target", "water level, m, test pier", "--value", value,
                "--unit", "m", "--horizon-end", "2027-12-31",
                "--model", "persistence", "--model-version", "1",
                "--inputs", "M1", "--metric", "abs_error"]
        if clearance:
            args += ["--clearance", clearance]
        return run(*args)

    def test_clearance_recorded_on_issue(self):
        reg = self.p("r.jsonl")
        code, out, err = self.issue(reg, clearance="pier:2.5,pump:1.8")
        self.assertEqual(code, 0, err)
        self.assertEqual(out["registered"]["clearance"],
                         [{"asset": "pier", "threshold": 2.5, "clearance": 0.1},
                          {"asset": "pump", "threshold": 1.8, "clearance": -0.6}])
        code, out, err = run("registry.py", "verify", "--registry", reg)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, {"ok": True, "records": 1})

    def test_clearance_without_option_absent_and_old_records_verify(self):
        reg = self.p("r.jsonl")
        code, out, err = self.issue(reg)
        self.assertEqual(code, 0, err)
        self.assertIsNone(out["registered"]["clearance"])
        code, out, err = run("registry.py", "verify", "--registry", reg)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, {"ok": True, "records": 1})

    def test_clearance_validation(self):
        base = {"value": 2.4, "clearance": [{"asset": "pier", "threshold": 2.5, "clearance": 0.1}]}
        self.assertIsNone(self.m.validate_forecast_fields(base))
        self.assertIsNotNone(self.m.validate_forecast_fields(
            {"value": 2.4, "clearance": [{"asset": "pier", "threshold": 2.5, "clearance": 0.2}]}))
        self.assertIsNotNone(self.m.validate_forecast_fields(
            {"value": 2.4, "clearance": [{"asset": "pier", "threshold": "2.5", "clearance": 0.1}]}))
        self.assertIsNotNone(self.m.validate_forecast_fields(
            {"value": 2.4, "clearance": [{"asset": "", "threshold": 2.5, "clearance": 0.1}]}))
        self.assertIsNotNone(self.m.validate_forecast_fields(
            {"value": 2.4, "clearance": "pier:2.5"}))

    def test_clearance_input_errors(self):
        reg = self.p("r.jsonl")
        for bad in ("pier", "pier:abc", "pier:2.5,:1.8"):
            code, _, err = self.issue(reg, clearance=bad)
            self.assertEqual(code, 2, err)

    def test_clearance_documented(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Clearance table (asset-relative safety margin)", templates)
        for phrase in ("clearance (threshold − forecast value)",
                       "A positive clearance is the margin the asset has",
                       "Generalizes beyond floods: clearance of a pollutant below its limit",
                       "Clearance per asset — asset ____ / threshold ____ / forecast value ____"):
            self.assertIn(phrase, templates)


class TestUserClassThresholds(Tmp):
    """T59: user-class operational thresholds (Round 2 of the v2.7 program, Patos)."""
    m = load("alert_bands")

    def series(self, values, name="s.csv"):
        rows = [[f"2027-07-{k + 1:02d}T00:00:00", v] for k, v in enumerate(values)]
        write_csv(self.p(name), ["time", "value"], rows)
        return self.p(name)

    def classes(self, rows, name="c.csv"):
        write_csv(self.p(name), ["class", "limit"], rows)
        return self.p(name)

    def alert(self, path, *extra):
        return run("alert_bands.py", path, "--indicator", "flood depth, m",
                   "--amber", ">=0.30", "--red", ">=0.35", "--window-hours", "1",
                   "--anchor", "test anchor", *extra)

    def test_class_thresholds_at_peak(self):
        main = self.series([0.10, 0.20, 0.30, 0.35, 0.40])  # peak 0.40, latest 0.40
        cl = self.classes([["car", "0.30"], ["ambulance", "0.35"], ["pickup", "0.45"]])
        code, out, err = self.alert(main, "--class-thresholds", cl)
        self.assertEqual(code, 0, err)
        by_class = {c["class"]: c for c in out["class_thresholds"]}
        self.assertEqual(by_class["car"]["limit"], 0.30)
        self.assertEqual(by_class["car"]["latest_value"], 0.40)
        self.assertEqual(by_class["car"]["peak_value"], 0.40)
        self.assertIs(by_class["car"]["latest_within"], False)
        self.assertIs(by_class["car"]["peak_within"], False)
        self.assertIs(by_class["car"]["can_operate"], False)
        self.assertIs(by_class["ambulance"]["can_operate"], False)
        self.assertIs(by_class["pickup"]["can_operate"], True)
        self.assertIs(by_class["pickup"]["peak_within"], True)

    def test_class_thresholds_latest_below_limit_after_peak(self):
        main = self.series([0.40, 0.40, 0.25])  # peak 0.40, latest 0.25
        cl = self.classes([["car", "0.30"]])
        code, out, err = self.alert(main, "--class-thresholds", cl)
        self.assertEqual(code, 0, err)
        c = out["class_thresholds"][0]
        self.assertEqual(c["peak_value"], 0.40)
        self.assertIs(c["latest_within"], True)   # can operate now
        self.assertIs(c["peak_within"], False)    # could not operate at the peak
        self.assertIs(c["can_operate"], False)

    def test_class_thresholds_input_errors(self):
        main = self.series([0.10, 0.20])
        code, _, err = self.alert(main, "--class-thresholds", self.p("missing.csv"))
        self.assertEqual(code, 2)
        write_csv(self.p("bad.csv"), ["class", "value"], [["car", "0.30"]])
        code, _, err = self.alert(main, "--class-thresholds", self.p("bad.csv"))
        self.assertEqual(code, 2)
        self.assertIn("class-threshold column 'limit' not found", err)
        write_csv(self.p("bad2.csv"), ["class", "limit"], [["car", "abc"]])
        code, _, err = self.alert(main, "--class-thresholds", self.p("bad2.csv"))
        self.assertEqual(code, 2)
        write_csv(self.p("bad3.csv"), ["class", "limit"], [["car", "0.30"], ["car", "0.35"]])
        code, _, err = self.alert(main, "--class-thresholds", self.p("bad3.csv"))
        self.assertEqual(code, 2)
        self.assertIn("duplicate class 'car'", err)

    def test_class_thresholds_documented(self):
        indicators = " ".join(rtext(os.path.join(ROOT, "references", "indicators.md")).split())
        self.assertIn("**User-class operational thresholds.**", indicators)
        for phrase in ("--class-thresholds classes.csv",
                       "can_operate",
                       "Distinct from the per-asset clearance",
                       "for each decision-maker, their operational limit in the same units as the indicator"):
            self.assertIn(phrase, indicators)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Decision-makers' operational limits (Phase 1):", templates)
        # T92: the I/O table moved from SKILL.md to references/scripts.md.
        table = rtext(os.path.join(ROOT, "references", "scripts.md"))
        self.assertIn("--class-thresholds FILE", table)


class TestExposureInventory(unittest.TestCase):
    """T60: exposure inventory + exposed fraction (Round 2 of the v2.7 program, EDITO)."""

    def test_exposure_block_on_scenario_card(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("## 6. Scenario card", templates)
        for phrase in ("Exposure — the exposed elements (people, assets, habitats, intakes, cages)",
                       "the exposed fraction per class (exposed ÷ total in the zone)",
                       "computed by table arithmetic from the hazard extent and the exposure inventory"):
            self.assertIn(phrase, templates)

    def test_exposure_in_scoring_rule_and_subsection(self):
        scenarios = rtext(os.path.join(ROOT, "references", "scenarios.md"))
        flat = " ".join(scenarios.split())
        self.assertIn("the exposed fraction per class (exposed ÷ total in the zone), co-benefits, and equity", flat)  # Round 4 of the v2.7 program: scoring gains co-benefits + equity
        self.assertIn("## Exposure inventory and exposed fraction", flat)
        after = flat.split("## Exposure inventory and exposed fraction", 1)[1]
        before = flat.split("## Impact chains", 1)[1]
        self.assertIn("The impact chain's Exposure link names who or what is in the hazard's path; the exposed fraction quantifies it per class", after)
        self.assertIn("a fraction with no inventory behind it is not a number, it is a guess, and goes to the [НЕТ ДАННЫХ] register", after)
        self.assertIn("Coastal Risk Projections", after)
        self.assertIn("Flooded Fraction", after)
        self.assertTrue(after.index("The impact chain's Exposure link") < after.index("## Stochastic scenario generation"))
        # the fraction is table arithmetic: four of five cages is 0.8
        self.assertIn("A fraction of 0.8 of the cages means four of five cages", after)
        self.assertAlmostEqual(4 / 5, 0.8)


class TestHindcastGate(unittest.TestCase):
    """T61: hindcast reproduction gate (Round 3 of the v2.7 program, EDITO)."""

    def test_reproduction_check_on_scenario_card(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Reproduction check — the scenario model run on the historical window with the intervention switched off", templates)
        self.assertIn("reported as \"unvalidated, direction only\" — never as a number", templates)

    def test_gate_rule_and_boundaries(self):
        scenarios = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        self.assertIn("## Hindcast reproduction gate", scenarios)
        for phrase in ("reproduce the observed historical period with the intervention switched off",
                       "within a declared tolerance",
                       "alert-band width or the calibration SD",
                       "unvalidated, direction only",
                       "Boundary — hindcast gate vs replay",
                       "checks the scenario MODEL before its delta is trusted",
                       "a passed gate never claims the alert fired"):
            self.assertIn(phrase, scenarios)
        replay = " ".join(rtext(os.path.join(ROOT, "references", "uncertainty-decision.md")).split())
        self.assertIn("Boundary — replay vs hindcast gate", replay)
        self.assertIn("The replay verifies an alert; the gate validates a scenario model", replay)
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("hindcast reproduction gate passes", skill)


class TestSkillHorizon(Tmp):
    """T62: skill-vs-lead-time curve (Round 3 of the v2.7 program, lake platforms)."""
    m = load("skill_scores")

    def test_horizon_stops_at_first_failure(self):
        # lead 1: model rmse 1.0, naive rmse 2.0 -> SS_RMSE 0.5 (beats).
        # lead 2: model rmse 3.0, naive rmse 1.0 -> SS_RMSE -2.0 (dies).
        # lead 3: model rmse 0, naive rmse 3.0 -> SS_RMSE 1.0 (recovery: noise, not skill).
        pairs = {1: [(10, 11, 8), (12, 11, 14), (11, 12, 9)],
                 2: [(10, 13, 11), (12, 9, 11), (11, 14, 12)],
                 3: [(10, 10, 13), (12, 12, 9), (11, 11, 14)]}
        per_lead, horizon, warnings = self.m.skill_horizon_by_lead(pairs)
        self.assertEqual(horizon, 1)
        self.assertAlmostEqual(per_lead[0]["ss_rmse"], 0.5)
        self.assertAlmostEqual(per_lead[1]["ss_rmse"], -2.0)
        self.assertAlmostEqual(per_lead[2]["ss_rmse"], 1.0)
        self.assertTrue(any("non-monotone recovery" in w for w in warnings))

    def test_no_skill_at_shortest_lead(self):
        per_lead, horizon, _ = self.m.skill_horizon_by_lead(
            {1: [(10, 13, 11), (12, 9, 11)], 2: [(10, 10, 13), (12, 12, 9)]})
        self.assertIsNone(horizon)

    def test_cli_and_input_errors(self):
        rows = [["lead", "obs", "sim", "naive"],
                ["1", "10", "11", "8"], ["1", "12", "11", "14"], ["1", "11", "12", "9"],
                ["2", "10", "13", "11"], ["2", "12", "9", "11"], ["2", "11", "14", "12"]]
        write_csv(self.p("h.csv"), rows[0], rows[1:])
        code, out, _ = run("skill_scores.py", "skill-horizon", self.p("h.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["skill_horizon"], 1)
        self.assertEqual(out["lead_unit"], "days")
        write_csv(self.p("bad.csv"), ["lead", "obs", "sim"], [["1", "10", "11"]])
        code, _, _ = run("skill_scores.py", "skill-horizon", self.p("bad.csv"))
        self.assertEqual(code, 2)

    def test_horizon_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "analytics-forecasting.md")).split())
        self.assertIn("Skill horizon", text)
        self.assertIn("not trusted beyond its horizon", text)
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("Skill horizon", templates)
        self.assertIn("skill_scores.py skill-horizon", templates)


class TestNudge(Tmp):
    """T63: observation-nudged forecast (Round 3 of the v2.7 program, lake platforms)."""

    def pairs(self, rows):
        write_csv(self.p("pairs.csv"), ["time", "obs", "sim"], rows)
        return self.p("pairs.csv")

    def test_mean_residual_shifts_the_forecast(self):
        # residuals all +2 (sim runs 2 above obs) -> raw 15 nudges to 13.
        path = self.pairs([[f"2027-01-0{i}", str(v), str(v + 2)]
                           for i, v in enumerate([10, 11, 12, 11, 10], start=1)])
        code, out, _ = run("skill_scores.py", "nudge", path, "--forecast", "15")
        self.assertEqual(code, 0)
        self.assertEqual(out["n_declared"], 5)
        self.assertEqual(out["n_used"], 5)
        self.assertAlmostEqual(out["mean_residual"], 2.0)
        self.assertAlmostEqual(out["nudged_forecast"], 13.0)
        self.assertAlmostEqual(out["correction"], -2.0)

    def test_last_n_pairs_only_and_short_window_warning(self):
        rows = [[f"2027-01-0{i}", str(v), str(v)] for i, v in enumerate([10, 10, 10, 20, 20], start=1)]
        path = self.pairs(rows)
        code, out, _ = run("skill_scores.py", "nudge", path, "--forecast", "20", "--n", "2")
        self.assertEqual(code, 0)
        self.assertEqual(out["n_used"], 2)
        self.assertAlmostEqual(out["mean_residual"], 0.0)
        self.assertAlmostEqual(out["nudged_forecast"], 20.0)
        code, out, _ = run("skill_scores.py", "nudge", path, "--forecast", "20", "--n", "10")
        self.assertEqual(code, 0)
        self.assertEqual(out["n_used"], 5)
        self.assertTrue(any("only 5 of the declared 10" in w for w in out["warnings"]))

    def test_input_errors(self):
        path = self.pairs([["2027-01-01", "10", "12"]])
        code, _, _ = run("skill_scores.py", "nudge", path, "--forecast", "15")
        self.assertEqual(code, 2)  # one pair only: need at least 2
        code, _, _ = run("skill_scores.py", "nudge", path, "--forecast", "15", "--n", "0")
        self.assertEqual(code, 2)

    def test_nudge_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "analytics-forecasting.md")).split())
        self.assertIn("Observation-nudged forecast", text)
        self.assertIn("mean(sim − obs)", text)
        self.assertIn("scored per lead time by `skill-horizon`", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Nudge window N", templates)
        self.assertIn("Nudge correction applied", templates)


class TestPhenomenonMetrics(unittest.TestCase):
    """T64: phenomenon-oriented metrics (Round 3 of the v2.7 program, EDITO)."""

    def test_metrics_table_and_rule(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "analytics-forecasting.md")).split())
        self.assertIn("Phenomenon-oriented metrics", text)
        for phrase in ("onset-date error", "peak-magnitude error", "duration error",
                       "peak-level error", "timing error", "season-start error",
                       "exceedance-days error",
                       "admission rule stays SS_RMSE",
                       "A metric that cannot be computed yet"):
            self.assertIn(phrase, text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Phenomenon metrics", templates)
        self.assertIn("onset-date error, peak error, duration error", templates)
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("phenomenon-oriented metrics alongside the generic score", skill)


class TestDiversity(Tmp):
    """T65: diversity indices (Round 3 of the v2.7 program, BioDT)."""
    m = load("diversity")

    def test_shannon_pielou_hand_values(self):
        # counts 10, 5, 5: H' = -(0.5 ln 0.5 + 0.25 ln 0.25 + 0.25 ln 0.25) = 1.0397
        h = self.m.shannon([10, 5, 5])
        self.assertAlmostEqual(h, 1.0397207708399179, places=6)
        self.assertAlmostEqual(self.m.pielou(h, 3), h / math.log(3), places=6)
        self.assertIsNone(self.m.pielou(h, 1))

    def test_delta_plus_same_genus_and_mixed(self):
        same_genus = [{"genus": "Aythya", "family": "Anatidae", "order": "Anseriformes",
                       "class": "Aves", "phylum": "Chordata"} for _ in range(3)]
        self.assertAlmostEqual(self.m.taxonomic_distinctness(same_genus), 1.0)
        mixed = [
            {"genus": "Aythya", "family": "Anatidae", "order": "Anseriformes", "class": "Aves", "phylum": "Chordata"},
            {"genus": "Aythya", "family": "Anatidae", "order": "Anseriformes", "class": "Aves", "phylum": "Chordata"},
            {"genus": "Anser", "family": "Anatidae", "order": "Anseriformes", "class": "Aves", "phylum": "Chordata"},
        ]
        # pairs: Aythya-Aythya 1, Aythya-Anser 2, Aythya-Anser 2 -> mean 5/3
        self.assertAlmostEqual(self.m.taxonomic_distinctness(mixed), 5 / 3, places=6)
        class_only = {"genus": "", "family": "", "order": "", "class": "Aves", "phylum": "Chordata"}
        duck = {"genus": "Aythya", "family": "Anatidae", "order": "Anseriformes", "class": "Aves", "phylum": "Chordata"}
        self.assertEqual(self.m.taxon_distance(class_only, duck), 4)
        self.assertIsNone(self.m.taxonomic_distinctness([duck]))

    def test_cli_on_khubsugul_counts(self):
        counts = os.path.join(ROOT, "examples", "gallery", "biodiversity", "occurrences.csv")
        rows = list(csv.DictReader(open(counts, newline="")))
        tally = {}
        for r in rows:
            tally[r["species"]] = tally.get(r["species"], 0) + 1
        write_csv(self.p("counts.csv"), ["species", "count"],
                  [[sp, tally[sp]] for sp in sorted(tally)])
        tax = os.path.join(ROOT, "examples", "gallery", "biodiversity", "taxonomy.csv")
        code, out, _ = run("diversity.py", "indices", self.p("counts.csv"), "--taxonomy", tax)
        self.assertEqual(code, 0)
        self.assertEqual(out["richness"], 18)
        self.assertEqual(out["total"], 20)
        self.assertAlmostEqual(out["shannon"], 2.8571, places=4)
        self.assertAlmostEqual(out["pielou"], 0.9885, places=4)
        self.assertAlmostEqual(out["delta_plus"], 3.5098, places=4)
        self.assertTrue(any("Aves sp." in w for w in out["warnings"]))

    def test_input_errors(self):
        write_csv(self.p("bad.csv"), ["species", "count"], [["A", "-1"]])
        code, _, _ = run("diversity.py", "indices", self.p("bad.csv"))
        self.assertEqual(code, 2)
        write_csv(self.p("empty.csv"), ["species", "count"], [["A", "0"]])
        code, _, _ = run("diversity.py", "indices", self.p("empty.csv"))
        self.assertEqual(code, 2)

    def test_diversity_documented_and_in_gallery(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "indicators.md")).split())
        self.assertIn("### Diversity indices", text)
        self.assertIn("Clarke", text)
        self.assertIn("Shannon H′", text)
        out = self.p("biodiversity")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "biodiversity", "run.py"),
                              "--out", out], capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        s = json.loads(res.stdout)
        self.assertAlmostEqual(s["diversity"]["shannon"], 2.8571, places=4)
        self.assertAlmostEqual(s["diversity"]["delta_plus"], 3.5098, places=4)


class TestPFTShares(Tmp):
    """T66: plant functional type shares (Round 3 of the v2.7 program, BioDT)."""

    def test_shares_from_cover_hand_values(self):
        write_csv(self.p("cover.csv"), ["species", "cover"],
                  [["Triticum aestivum", "70"], ["Trifolium pratense", "10"],
                   ["Lolium perenne", "8"], ["Taraxacum officinale", "5"],
                   ["Elymus repens", "4"], ["Cirsium arvense", "3"]])
        table = os.path.join(ROOT, "examples", "gallery", "field", "pft_table.csv")
        code, out, _ = run("diversity.py", "pft", self.p("cover.csv"), "--pft-table", table)
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["shares_by_pft"]["grass"], 0.82)
        self.assertAlmostEqual(out["shares_by_pft"]["legume"], 0.10)
        self.assertAlmostEqual(out["shares_by_pft"]["forb"], 0.08)
        self.assertAlmostEqual(out["shares_by_pathway"]["C3"], 1.0)
        self.assertEqual(out["total"], 100)
        self.assertEqual(out["n_species"], 6)

    def test_missing_species_excluded_and_named(self):
        write_csv(self.p("cover.csv"), ["species", "cover"], [["Unknown sp.", "50"], ["Triticum aestivum", "50"]])
        table = os.path.join(ROOT, "examples", "gallery", "field", "pft_table.csv")
        code, out, _ = run("diversity.py", "pft", self.p("cover.csv"), "--pft-table", table)
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["shares_by_pft"]["grass"], 0.5)
        self.assertTrue(any("Unknown sp." in w for w in out["warnings"]))

    def test_pft_in_field_gallery_and_docs(self):
        out = self.p("field")
        res = subprocess.run([sys.executable,
                              os.path.join(ROOT, "examples", "gallery", "field", "run.py"),
                              "--out", out], capture_output=True, text=True, timeout=120)
        self.assertEqual(res.returncode, 0, res.stderr)
        s = json.loads(res.stdout)
        self.assertAlmostEqual(s["pft_shares"]["by_pft"]["grass"], 0.82)
        self.assertAlmostEqual(s["pft_shares"]["by_pathway"]["C3"], 1.0)
        text = " ".join(rtext(os.path.join(ROOT, "references", "indicators.md")).split())
        self.assertIn("### Plant functional type shares", text)
        self.assertIn("one quantity only", text)
        self.assertIn("TRY Plant Trait Database", text)


class TestTraitMatch(Tmp):
    """T67: trait-environment matching (Round 3 of the v2.7 program, BioDT)."""

    def conditions(self, cond):
        path = self.p("cond.json")
        with open(path, "w") as fh:
            json.dump(cond, fh)
        return path

    def test_saline_site_fits_only_halophytes(self):
        # Corrected Ellenberg values (verified 2026-10-26 against the
        # Ellenberg column in Tichý et al. 2023, Zenodo 7427088):
        # Puccinellia distans S = 7, not 8 — only Salicornia europaea
        # (S = 9) reaches the site's S ≥ 8.
        table = os.path.join(ROOT, "examples", "gallery", "field", "trait_table.csv")
        cond = self.conditions({"S": {"mode": "at_least", "value": 8}})
        code, out, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 0)
        self.assertEqual(out["fits"], ["Salicornia europaea"])
        failed = {f["taxon"]: f["failed"] for f in out["fails"]}
        self.assertIn("Puccinellia distans", failed)
        self.assertIn("S: 7.0 < 8 (needs >= 8)", failed["Puccinellia distans"][0])
        self.assertEqual(out["indifferent"], [])  # no "x" in the S column

    def test_nitrogen_and_temperature_rules(self):
        table = os.path.join(ROOT, "examples", "gallery", "field", "trait_table.csv")
        # N ≥ 7: Trifolium pratense has NO N value in Ellenberg
        # (indifferent, "x") — it is not excluded, and the output names
        # it as indifferent; Salicornia (N=4) and Puccinellia (N=4) are.
        cond = self.conditions({"N": {"mode": "at_least", "value": 7}})
        code, out, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 0)
        self.assertEqual(out["fits"], ["Trifolium pratense", "Lolium perenne",
                                       "Taraxacum officinale", "Elymus repens",
                                       "Cirsium arvense"])
        self.assertNotIn("Puccinellia distans", out["fits"])  # N=4
        self.assertNotIn("Salicornia europaea", out["fits"])  # N=4
        self.assertEqual([(i["taxon"], i["trait"]) for i in out["indifferent"]],
                         [("Trifolium pratense", "N")])
        self.assertIn("indifferent", out["indifferent"][0]["note"])
        # T within 6 ± 1: all 7 taxa fit, but two of them (Trifolium and
        # Taraxacum) have no T value — they fit by indifference, not by
        # value, and the output names them.
        cond = self.conditions({"T": {"mode": "within", "value": 6, "window": 1}})
        code, out, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 0)
        self.assertEqual(len(out["fits"]), 7)
        self.assertEqual([(i["taxon"], i["trait"]) for i in out["indifferent"]],
                         [("Trifolium pratense", "T"), ("Taraxacum officinale", "T")])
        cond = self.conditions({"S": {"mode": "at_least", "value": 8},
                                "T": {"mode": "within", "value": 6, "window": 1}})
        code, out, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(out["fits"], ["Salicornia europaea"])

    def test_indifferent_value_does_not_exclude(self):
        # A taxon with "x" for a trait is not excluded by a condition on
        # that trait; a cell that is neither a number nor "x" is refused.
        write_csv(self.p("t.csv"), ["taxon", "S", "T"],
                  [["A sp.", "x", "6"], ["B sp.", "7", "6"]])
        cond = self.conditions({"S": {"mode": "at_least", "value": 8}})
        code, out, _ = run("trait_match.py", self.p("t.csv"), "--conditions", cond)
        self.assertEqual(code, 0)
        self.assertEqual(out["fits"], ["A sp."])
        self.assertEqual([(i["taxon"], i["trait"]) for i in out["indifferent"]],
                         [("A sp.", "S")])
        write_csv(self.p("bad.csv"), ["taxon", "S"], [["C sp.", "abc"]])
        code, _, _ = run("trait_match.py", self.p("bad.csv"), "--conditions", cond)
        self.assertEqual(code, 2)

    def test_input_errors(self):
        table = os.path.join(ROOT, "examples", "gallery", "field", "trait_table.csv")
        cond = self.conditions({"Z": {"mode": "at_least", "value": 1}})
        code, _, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 2)  # unknown trait column
        cond = self.conditions({"S": {"mode": "above", "value": 8}})
        code, _, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 2)  # unknown mode
        cond = self.conditions({"T": {"mode": "within", "value": 6}})
        code, _, _ = run("trait_match.py", table, "--conditions", cond)
        self.assertEqual(code, 2)  # 'within' without a window

    def test_trait_match_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "indicators.md")).split())
        self.assertIn("### Trait–environment matching", text)
        self.assertIn("Ellenberg indicator values", text)
        self.assertIn("Tichý et al. 2023", text)
        self.assertIn("7427088", text)
        self.assertIn("2026-10-26", text)
        self.assertIn("verified against the published source before client use", text)


class TestSamplingPriority(Tmp):
    """T68: spread-informed sampling priority (Round 3 of the v2.7 program, lake platforms)."""
    m = load("uncertainty_budget")

    def test_ranking_by_disagreement(self):
        ranked, top = self.m.sampling_priority([("A", 10, 10), ("B", 12, 20), ("C", 15, 12)])
        self.assertEqual(top, "B")
        self.assertEqual([r["target"] for r in ranked], ["B", "C", "A"])
        self.assertEqual([r["disagreement"] for r in ranked], [8, 3, 0])
        self.assertEqual([r["rank"] for r in ranked], [1, 2, 3])
        # ties break by input order, deterministically
        ranked, top = self.m.sampling_priority([("X", 5, 7), ("Y", 1, 3)])
        self.assertEqual(top, "X")
        self.assertEqual([r["target"] for r in ranked], ["X", "Y"])

    def test_cli_model_vs_naive_and_model_a_vs_b(self):
        write_csv(self.p("t.csv"), ["target", "model", "naive"],
                  [["A", "10", "10"], ["B", "12", "20"], ["C", "15", "12"]])
        code, out, _ = run("uncertainty_budget.py", "sampling-priority", self.p("t.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["basis"], "admitted model vs naive benchmark")
        self.assertEqual(out["sample_next"], "B")
        write_csv(self.p("t2.csv"), ["target", "model_a", "model_b"],
                  [["A", "10", "12"], ["B", "5", "5"]])
        code, out, _ = run("uncertainty_budget.py", "sampling-priority", self.p("t2.csv"))
        self.assertEqual(code, 0)
        self.assertEqual(out["basis"], "candidate model A vs candidate model B")
        self.assertEqual(out["sample_next"], "A")

    def test_input_errors_and_old_cli_untouched(self):
        write_csv(self.p("bad.csv"), ["target", "model"], [["A", "10"]])
        code, _, _ = run("uncertainty_budget.py", "sampling-priority", self.p("bad.csv"))
        self.assertEqual(code, 2)
        write_csv(self.p("empty.csv"), ["target", "model", "naive"], [])
        code, _, _ = run("uncertainty_budget.py", "sampling-priority", self.p("empty.csv"))
        self.assertEqual(code, 2)
        # the budget CLI is unchanged: ensemble.csv with no subcommand
        write_csv(self.p("ens.csv"), ["output", "source", "member", "value"],
                  [["x", "parameter", "1", "10"], ["x", "parameter", "2", "12"],
                   ["x", "all", "1", "11"], ["x", "all", "2", "13"]])
        code, out, _ = run("uncertainty_budget.py", self.p("ens.csv"), "--interval", "90")
        self.assertEqual(code, 0)
        self.assertIn("outputs", out)

    def test_sampling_priority_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "uncertainty-decision.md")).split())
        self.assertIn("Spread-informed sampling priority", text)
        self.assertIn("sample here next", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Sampling priority", templates)
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("where the models disagree most, the twin samples next", skill)


class TestSensitivityScreen(Tmp):
    """T69: sensitivity-first calibration (Round 4 of the v2.7 program, Gironde)."""
    m = load("sensitivity_screen")

    def model(self, body="def run(p):\n    return 2 * p['a'] + 0.1 * p['b'] + p['c']\n"):
        wtext(self.p("model.py"), body)
        return self.p("model.py")

    def params(self, spec=None):
        spec = spec or {"parameters": [{"name": "a", "value": 10, "perturb": 0.1},
                                       {"name": "b", "value": 10, "perturb": 0.1},
                                       {"name": "c", "value": 5, "perturb": 0.1}]}
        with open(self.p("params.json"), "w") as fh:
            json.dump(spec, fh)
        return self.p("params.json")

    def test_ranking_by_relative_change(self):
        # baseline 2*10 + 0.1*10 + 5 = 26; a moves +-2, c +-0.5, b +-0.1.
        code, out, _ = run("sensitivity_screen.py", self.model(), "--params", self.params(),
                           "--metric", "tp")
        self.assertEqual(code, 0)
        self.assertAlmostEqual(out["baseline"], 26.0)
        self.assertEqual([r["parameter"] for r in out["parameters"]], ["a", "c", "b"])
        self.assertEqual([r["rank"] for r in out["parameters"]], [1, 2, 3])
        self.assertAlmostEqual(out["parameters"][0]["rel_change"], 2 / 26)
        self.assertAlmostEqual(out["parameters"][1]["abs_change"], 0.5)
        self.assertIn("one-at-a-time misses interactions", out["limit"])

    def test_range_endpoints_and_zero_baseline(self):
        code, out, _ = run("sensitivity_screen.py",
                           self.model("def run(p):\n    return p['a'] - p['a']\n"),
                           "--params", self.params({"parameters": [
                               {"name": "a", "value": 5, "range": [0, 10]}]}))
        self.assertEqual(code, 0)
        self.assertEqual(out["baseline"], 0)
        self.assertIsNone(out["parameters"][0]["rel_change"])  # relative change undefined at 0
        self.assertEqual(out["parameters"][0]["perturbed_values"], [0, 10])

    def test_input_errors(self):
        code, _, _ = run("sensitivity_screen.py", self.model("x = 1\n"), "--params", self.params())
        self.assertEqual(code, 2)  # no run()
        code, _, _ = run("sensitivity_screen.py", self.model(), "--params",
                         self.params({"parameters": [{"name": "a", "value": 5, "perturb": 1.5}]}))
        self.assertEqual(code, 2)  # perturb must be a fraction in (0, 1)
        code, _, _ = run("sensitivity_screen.py", self.model(), "--params",
                         self.params({"parameters": [{"name": "a", "value": 5, "range": [10, 0]}]}))
        self.assertEqual(code, 2)  # inverted range
        code, _, _ = run("sensitivity_screen.py", self.model(), "--params",
                         self.params({"parameters": []}))
        self.assertEqual(code, 2)  # empty parameters
        code, _, _ = run("sensitivity_screen.py", self.p("missing.py"), "--params", self.params())
        self.assertEqual(code, 2)

    def test_sensitivity_screen_documented(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("sensitivity screen", skill)
        self.assertIn("calibrate only the influential parameters", skill)
        self.assertIn("One-at-a-time misses interactions, unlike Sobol", skill)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Sensitivity screen", templates)
        self.assertIn("sensitivity_screen.py", templates)


class TestModelLadder(unittest.TestCase):
    """T70: model ladder (Round 4 of the v2.7 program, Digital Baikal)."""

    def test_model_ladder_documented(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("Model ladder", skill)
        self.assertIn("SCREENING ONLY", skill)
        self.assertIn("declared tolerance of the full model", skill)
        self.assertIn("A fast model outside its tolerance is not used for decisions", skill)

    def test_model_ladder_in_passport(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Model ladder", templates)
        self.assertIn("fast model (screening only)", templates)
        self.assertIn("declared tolerance between them on the same hold-out", templates)


class TestAdaptationFollowUp(Tmp):
    """T71: adaptation appraisal with equity + M&E (Round 4 of the v2.7 program, DestinE)."""

    def clock(self, t):
        return {"ECO_TWIN_CLOCK": t}

    def test_follow_up_forecast_scores_like_any_forecast(self):
        # M&E follow-up: predicted impact 20 registered with check date 2027-07-01;
        # observed impact 24 -> abs_error 4.0. Same discipline as BEIRA-F-001.
        reg = self.p("r.jsonl")
        args = ["registry.py", "issue", "--registry", reg, "--id", "WET-ME-001",
                "--kind", "quantity", "--target", "TP removed by wetland, kg/yr",
                "--value", "20", "--horizon-end", "2027-07-01", "--model", "wetland",
                "--model-version", "1", "--inputs", "ds-01", "--metric", "abs_error"]
        code, _, err = run(*args, env=self.clock("2027-01-01T00:00:00Z"))
        self.assertEqual(code, 0, err)
        code, _, err = run("registry.py", "resolve", "--registry", reg, "--id", "WET-ME-001",
                           "--outcome", "24", env=self.clock("2027-07-02T00:00:00Z"))
        self.assertEqual(code, 0, err)
        code, out, _ = run("registry.py", "score", "--registry", reg, "--now", "2027-07-03")
        self.assertEqual(code, 0)
        self.assertEqual(out["forecasts"][0]["abs_error"], 4.0)

    def test_adaptation_appraisal_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        self.assertIn("equity (who bears the cost, who gains)", text)
        self.assertIn("Adaptation appraisal and follow-up", text)
        self.assertIn("did the measure work", text)
        self.assertIn("same Brier-style discipline as BEIRA-F-001", text)
        self.assertIn("without a chain the impact avoided is [НЕТ ДАННЫХ]", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Impact avoided (from the impact chain", templates)
        self.assertIn("Equity — who bears the cost", templates)
        self.assertIn("Follow-up check date", templates)


class TestDriverPerturbationTable(unittest.TestCase):
    """T72: driver-perturbation table (Round 4 of the v2.7 program, Southern Water)."""

    def test_driver_perturbation_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "scenarios.md")).split())
        self.assertIn("## Driver-perturbation table", text)
        self.assertIn("(+10%, +25%, −10%)", text)
        self.assertIn("whether the watch level is crossed", text)
        self.assertIn("Boundary — driver table vs sensitivity screen", text)
        self.assertIn("Different questions, different tables, never merged", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Sensitivity (driver-perturbation table)", templates)
        self.assertIn("perturbation (+10% / +25% / −10%)", templates)
        self.assertIn("watch level crossed?", templates)


class TestMismatchRegister(Tmp):
    """T73: mismatch register (Round 4 of the v2.7 program, Patos)."""
    m = load("mismatch")

    def tables(self, obs=None, mod=None):
        obs = obs if obs is not None else [["A", "1"], ["B", "1"], ["C", "1"], ["D", "0"]]
        mod = mod if mod is not None else [["A", "0"], ["B", "1"], ["C", "1"], ["D", "1"]]
        write_csv(self.p("obs.csv"), ["cell", "value"], obs)
        write_csv(self.p("mod.csv"), ["cell", "value"], mod)
        return self.p("obs.csv"), self.p("mod.csv")

    def test_extent_misses_and_false_alarms(self):
        # observed {A,B,C}, modeled {B,C,D}: extent 2/3, miss A, false alarm D.
        obs, mod = self.tables()
        code, out, _ = run("mismatch.py", "--observed", obs, "--modeled", mod)
        self.assertEqual(code, 0)
        self.assertEqual(out["n_cells"], 4)
        self.assertEqual(out["n_observed"], 3)
        self.assertAlmostEqual(out["extent"], 2 / 3)
        self.assertEqual(out["misses"], ["A"])
        self.assertEqual(out["false_alarms"], ["D"])
        self.assertEqual(out["hits"], ["B", "C"])

    def test_no_observed_positives_extent_null(self):
        obs, mod = self.tables(obs=[["A", "0"], ["B", "0"]], mod=[["A", "0"], ["B", "1"]])
        code, out, _ = run("mismatch.py", "--observed", obs, "--modeled", mod)
        self.assertEqual(code, 0)
        self.assertIsNone(out["extent"])
        self.assertEqual(out["false_alarms"], ["B"])

    def test_register_append_and_input_errors(self):
        obs, mod = self.tables()
        reg = self.p("mm.jsonl")
        code, out, err = run("mismatch.py", "--observed", obs, "--modeled", mod,
                             "--register", reg, "--id", "FLOOD-M-001",
                             "--cause", "suspected underground drainage [ГИПОТЕЗА]",
                             "--confirm-measurement", "drainage survey of cell A",
                             "--model", "region-growing flood model", "--model-version", "1")
        self.assertEqual(code, 0, err)
        self.assertEqual(out["registered"]["id"], "FLOOD-M-001")
        self.assertAlmostEqual(out["registered"]["extent"], 2 / 3)
        with open(reg, encoding="utf-8") as fh:
            entry = json.loads(fh.read())
        self.assertEqual(entry["misses"], ["A"])
        self.assertEqual(entry["cause"], "suspected underground drainage [ГИПОТЕЗА]")
        # --register without the cause fields is refused
        code, _, _ = run("mismatch.py", "--observed", obs, "--modeled", mod,
                         "--register", self.p("mm2.jsonl"), "--id", "X-1")
        self.assertEqual(code, 2)
        # mismatched cell sets, non-binary values, empty tables are refused
        obs2, _ = self.tables(obs=[["A", "1"], ["B", "1"]])
        code, _, _ = run("mismatch.py", "--observed", obs2, "--modeled", mod)
        self.assertEqual(code, 2)
        obs3, mod3 = self.tables(obs=[["A", "2"], ["B", "1"]], mod=[["A", "1"], ["B", "1"]])
        code, _, _ = run("mismatch.py", "--observed", obs3, "--modeled", mod3)
        self.assertEqual(code, 2)

    def test_mismatch_register_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "uncertainty-decision.md")).split())
        self.assertIn("Mismatch register — learning from the pattern of the error", text)
        self.assertIn("The register is the learning log, not a gate", text)
        self.assertIn("A failed validation with no register entry is a score with no lesson", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("## 12. Mismatch register entry", templates)
        self.assertIn("Inferred hidden cause ([ГИПОТЕЗА] / [НЕТ ДАННЫХ])", templates)
        self.assertIn("Measurement that would confirm it", templates)


class TestPromotionRecord(Tmp):
    """T74: promotion record (Round 4 of the v2.7 program, Gironde)."""
    m = load("registry")

    def promote(self, reg, pid="PROM-001", *extra):
        return run("registry.py", "promote", "--registry", reg, "--id", pid,
                   "--model", "TP-lag", "--model-version", "0.2",
                   "--promoted-by", "R. Baldanova (lead modeler)",
                   "--evidence", "SS_RMSE 0.42 on hold-out; alert trial PASS", *extra)

    def test_promote_records_operational_and_scores_ignore_it(self):
        reg = self.p("r.jsonl")
        code, out, err = self.promote(reg)
        self.assertEqual(code, 0, err)
        rec = out["registered"]
        self.assertEqual(rec["type"], "promotion")
        self.assertEqual(rec["status"], "operational")
        self.assertEqual(rec["promoted_by"], "R. Baldanova (lead modeler)")
        self.assertEqual(rec["evidence"], "SS_RMSE 0.42 on hold-out; alert trial PASS")
        code, out, _ = run("registry.py", "verify", "--registry", reg)
        self.assertEqual(code, 0)
        self.assertEqual(out, {"ok": True, "records": 1})
        code, out, _ = run("registry.py", "score", "--registry", reg)
        self.assertEqual(code, 0)
        self.assertEqual(out["operational"]["n_scored"], 0)  # a promotion is governance, not a forecast
        self.assertTrue(out["chain"]["ok"])

    def test_promote_refusals(self):
        reg = self.p("r.jsonl")
        self.assertEqual(self.promote(reg)[0], 0)
        code, _, err = self.promote(reg)
        self.assertEqual(code, 2)  # duplicate id
        self.assertIn("already registered", err)
        code, _, err = run("registry.py", "promote", "--registry", reg, "--id", "PROM-002",
                           "--model", "m", "--model-version", "1", "--evidence", "Y")
        self.assertEqual(code, 2)  # --promoted-by is required (argparse)
        code, _, err = self.promote(reg, "PROM-003", "--promoted-by", "   ")
        self.assertEqual(code, 2)  # blank promoter is not a signature
        code, _, err = self.promote(reg, "PROM-003", "--evidence", "   ")
        self.assertEqual(code, 2)  # blank evidence is not evidence

    def test_promotion_documented(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("A model is operational only after a recorded promotion", skill)
        self.assertIn("without one it is exploratory", skill)
        self.assertIn("registry.py promote", skill)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Promotion record: status (exploratory | operational)", templates)
        self.assertIn("promoted by (name/role)", templates)


class TestSemanticMappings(Tmp):
    """T75: semantic mapping sets (Round 4 of the v2.7 program, BioDT)."""
    m = load("build_manifest")
    GALLERY = os.path.join(ROOT, "examples", "gallery")

    def base_index(self):
        return {"name": "twin", "description": "test", "license": "CC-BY-4.0",
                "datasets": [{"id": "ds-01", "name": "pond", "path": "examples/gallery/pond/data.csv"}],
                "models": [{"id": "md-01", "name": "m", "version": "1"}],
                "steps": [{"id": "st-01", "instrument": "md-01", "action": "run",
                           "inputs": ["ds-01"], "parameters": {}, "date": "2026-10-26"}],
                "outputs": [{"id": "out-01", "name": "x", "value": 1.0, "produced_by": "st-01"}]}

    def test_every_gallery_field_is_mapped_or_explicitly_unmapped(self):
        # Every header column of every gallery CSV is either mapped to a
        # standard term or recorded as unmapped with a reason; a field
        # absent from mappings.csv is a failure, not a silent gap.
        for site in sorted(os.listdir(self.GALLERY)):
            d = os.path.join(self.GALLERY, site)
            if not os.path.isdir(d):
                continue
            mp_path = os.path.join(d, "mappings.csv")
            self.assertTrue(os.path.exists(mp_path), f"{site}: no mappings.csv")
            with open(mp_path, newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(list(rows[0].keys()),
                             ["file", "local_field", "standard_term", "standard", "justification"])
            mapped = {(r["file"], r["local_field"]): r for r in rows}
            for r in rows:
                self.assertTrue(r["justification"].strip(), f"{site} {r}: empty justification")
                if not r["standard_term"]:
                    self.assertEqual(r["standard"], "unmapped", f"{site} {r}: empty term but not marked unmapped")
            for name in sorted(os.listdir(d)):
                if not name.endswith(".csv") or name == "mappings.csv":
                    continue
                with open(os.path.join(d, name), newline="", encoding="utf-8") as fh:
                    header = next(csv.reader(fh))
                for col in header:
                    self.assertIn((name, col), mapped,
                                  f"{site}/{name}: column '{col}' is missing from mappings.csv")

    def test_manifest_mapping_entity(self):
        idx = self.base_index()
        idx["mappings"] = [{"id": "map-01", "dataset": "ds-01",
                            "path": "examples/gallery/pond/mappings.csv", "standard": "Darwin Core"}]
        errors, warnings, datasets, models, steps, outputs, mappings = self.m.validate(idx, self.d)
        self.assertEqual(errors, [])
        crate = self.m.build(idx, datasets, models, steps, outputs, mappings)
        ms = [e for e in crate["@graph"] if e.get("additionalType") == "MappingSet"]
        self.assertEqual(len(ms), 1)
        self.assertEqual(ms[0]["@id"], "examples/gallery/pond/mappings.csv")
        self.assertEqual(ms[0]["about"], {"@id": "examples/gallery/pond/data.csv"})
        self.assertEqual(ms[0]["conformsTo"], {"@id": "https://w3id.org/sssom/"})
        root = [e for e in crate["@graph"] if e["@id"] == "./"][0]
        self.assertIn({"@id": "examples/gallery/pond/mappings.csv"}, root["hasPart"])

    def test_manifest_mapping_validation(self):
        idx = self.base_index()
        idx["mappings"] = [{"id": "map-01", "dataset": "no-such-dataset",
                            "path": "examples/gallery/pond/mappings.csv"}]
        errors, _, _, _, _, _, _ = self.m.validate(idx, self.d)
        self.assertTrue(any("no-such-dataset" in e for e in errors))
        idx["mappings"] = [{"id": "map-01", "dataset": "ds-01"}]
        errors, _, _, _, _, _, _ = self.m.validate(idx, self.d)
        self.assertTrue(any("'path'" in e for e in errors))
        idx["mappings"] = [{"id": "map-01", "dataset": "ds-01",
                            "path": "examples/gallery/pond/mappings.csv"},
                           {"id": "map-01", "dataset": "ds-01",
                            "path": "examples/gallery/river/mappings.csv"}]
        errors, _, _, _, _, _, _ = self.m.validate(idx, self.d)
        self.assertTrue(any("duplicate" in e for e in errors))

    def test_semantic_mapping_documented(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "data-sources.md")).split())
        self.assertIn("Semantic mapping sets (`mappings.csv`)", text)
        self.assertIn("explicitly recorded as unmapped, with the reason", text)
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("semantic mapping (mappings.csv — local field → standard term + justification, per dataset)", templates)


class TestValidUseField(unittest.TestCase):
    """T76: 'Valid use / out of scope' field (Round 4 of the v2.7 program, BioDT)."""

    def test_valid_use_field_in_passport(self):
        passport = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Valid use / out of scope: valid use (the decisions this twin is built for)", passport)
        self.assertIn("out of scope (what the twin must NOT be used for)", passport)


class TestThreeZoneIngestion(unittest.TestCase):
    """T77: three-zone file ingestion (Laguna borrowing patch)."""

    def test_zones_documented_in_skill(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("three zones", skill)
        for zone in ("landing/", "trusted/", "refined/"):
            self.assertIn(zone, skill)
        self.assertIn("A file leaves `landing/` only after its QC is recorded", skill)
        self.assertIn("a file enters `refined/` only after its conversion is recorded", skill)

    def test_zone_field_in_onboarding_and_qc_note(self):
        templates = rtext(os.path.join(ROOT, "assets", "templates.md"))
        self.assertIn("file zone (landing / trusted / refined)", templates)
        qc = rtext(os.path.join(ROOT, "scripts", "qc_series.py"))
        self.assertIn("landing/", qc)
        self.assertIn("never moves or edits files", qc)


class TestTwinToTwinNotification(unittest.TestCase):
    """T78: twin-to-twin notifications (Laguna borrowing patch)."""

    def test_notification_step_in_stage_7(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("When an alert fires, the twin also notifies its linked nodes", skill)
        self.assertIn("recorded on the trigger–action–response plan", skill)
        self.assertIn("not in the forecast registry", skill)
        self.assertIn("a notified node re-checks its own alert bands on the next batch", skill)

    def test_tarp_carries_notification_field(self):
        templates = " ".join(rtext(os.path.join(ROOT, "assets", "templates.md")).split())
        self.assertIn("Linked nodes notified:", templates)
        self.assertIn("re-checks its own alert bands on the next batch", templates)


class TestTwinWorkspaceLayout(unittest.TestCase):
    """T79: per-twin workspace layout (Laguna borrowing patch)."""

    def test_layout_documented_in_skill(self):
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("A twin's working folder follows one layout", skill)
        for folder in ("common/", "etl/", "calibration/", "forecasts/", "simulations/"):
            self.assertIn(folder, skill)

    def test_layout_cross_referenced_from_manifest_and_no_ml_training(self):
        # Laguna's layout carries an ml-training folder; this skill has no
        # ML-training step, so the layout adapts it away — the absence is
        # pinned, not assumed.
        skill = " ".join(rtext(os.path.join(ROOT, "SKILL.md")).split())
        self.assertIn("records the twin workspace layout from Stage 2", skill)
        self.assertNotIn("ml-training", skill.lower())


class TestFieldTwinEtlStreams(unittest.TestCase):
    """T80: four named open-data ETL streams for the field twin (Laguna borrowing patch)."""

    def test_four_streams_listed_in_data_sources(self):
        text = " ".join(rtext(os.path.join(ROOT, "references", "data-sources.md")).split())
        self.assertIn("## Field-twin open-data streams", text)
        for stream in ("Daily weather", "Forecast weather", "Historical weather", "NDVI"):
            self.assertIn(stream, text)
        self.assertIn("ERA5", text)
        self.assertIn("Sentinel-2", text)
        self.assertIn("10.1016/j.compind.2025.104347", text)

    def test_field_readme_cross_references_without_duplicating(self):
        readme = rtext(os.path.join(ROOT, "examples", "gallery", "field", "README.md"))
        self.assertIn("references/data-sources.md", readme)
        # The list lives in one place only: the README points at it, it does
        # not repeat the stream names.
        self.assertNotIn("Historical weather", readme)


class TestNewSections(unittest.TestCase):
    """T81: v2.8 domain sections §21-§29 in the indicator catalogue."""

    def test_sections_present_with_expected_row_counts(self):
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        parts = re.split(r"\n## (\d+)\. ", text)
        got = {}
        for i in range(1, len(parts), 2):
            n = int(parts[i])
            rows = [l for l in parts[i + 1].splitlines()
                    if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                    and not re.match(r"^\|[-: |]+\|$", l)]
            got[n] = len(rows)
        expected = {21: 15, 22: 17, 23: 18, 24: 15, 25: 24,
                    26: 22, 27: 20, 28: 19, 29: 17}
        for n, count in expected.items():
            self.assertEqual(got.get(n), count, f"§{n} row count")
        self.assertEqual(sum(expected.values()), 167)

    def test_quick_sets_present_and_skill_points_at_sections(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for name in ("Cryosphere / mountain", "Steppe / natural grassland",
                     "Livestock farm", "Peatland", "Marine / coastal", "Urban",
                     "Aquaculture", "Desert / arid", "Tundra / polar"):
            self.assertIn(name, text)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("§21 Cryosphere", skill)
        self.assertIn("§29 Tundra and polar", skill)
        self.assertIn("Ecosystem Digital Twin by Rigjita Baldanova", skill)

    def test_both_unverified_flags_closed(self):
        """T89, 2026-10-28: both remaining [unverified] flags closed as verified
        negative results — marmot (no density standard; baseline/trend +
        Enkhsaikhan founder minimums + Xu plague cut-point) and WHO 9 m²
        (Italian law D.M. 1444/1968, not WHO)."""
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for flag in ("[unverified] — no standardised marmot density threshold",
                     "[unverified as a WHO publication"):
            self.assertNotIn(flag, text)
        self.assertNotIn("[unverified — the 500 t threshold was", text)
        self.assertNotIn("[unverified] — set from the permit", text)
        self.assertIn("50,000 kg/yr", text)
        self.assertIn("16,000–42,000", text)

    def test_new_section_tables_are_single_fragments(self):
        """T81: each §21-§29 table is one contiguous block. A hard-wrapped
        row splits the table in strict Markdown rendering (the §27 table
        arrived split into 12 fragments; fixed in loop round 1)."""
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        parts = re.split(r"\n## (\d+)\. ", text)
        expected = {21: 17, 22: 19, 23: 20, 24: 17, 25: 26,
                    26: 24, 27: 22, 28: 21, 29: 19, 30: 23, 31: 23,
                    32: 21}
        for i in range(1, len(parts), 2):
            n = int(parts[i])
            if n < 21:
                continue
            lines = parts[i + 1].splitlines()
            idx = [j for j, l in enumerate(lines) if l.startswith("|")]
            self.assertEqual(len(idx), expected[n], f"§{n} table lines")
            between = [l for l in lines[idx[0]:idx[-1] + 1]
                       if l.strip() and not l.startswith("|")]
            self.assertEqual(between, [], f"§{n} table split by prose")

    def test_worked_examples_and_sources_present(self):
        """T81: worked examples and full source lists for §21-§32 live in
        references/ (first-layer improvements, 2026-10-27; second-layer
        check, 2026-10-28; §30 Forest added 2026-10-28; §31 Cropland added
        2026-10-27; §32 Non-peat wetlands and marshes added 2026-10-28;
        second §30 example — Barguzinsky bear — added 2026-10-28).
        Both files carry a
        ## Contents list near the top, one worked example and one source list
        per new section, the closed [NEXT DATA] values and the remaining
        lemming-density gap, and the Liu et al. 2026 DOI."""
        names = ("Cryosphere", "Steppe", "Livestock", "Peatland",
                 "Marine", "Urban", "Aquaculture", "Desert", "Tundra",
                 "Forest", "Cropland", "Wetlands")
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        for text in (ex, src):
            head = "\n".join(text.splitlines()[:15])
            self.assertIn("## Contents", head)
            for name in names:
                self.assertIn(name, text)
        self.assertEqual(ex.count("## Worked example:"), 12)
        self.assertEqual(src.count("## Sources and verification status"), 12)
        self.assertIn("21,701", ex)
        self.assertIn("75–85 families", ex)
        self.assertIn("26,600", ex)
        self.assertIn("[NEXT DATA] gap — lemming densities", ex)
        self.assertIn("10.34133/remotesensing.1062", src)
        ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("21,402", ind)
        self.assertNotIn("provisional", ind)


class TestForestSection(unittest.TestCase):
    """T84: v2.8 domain section §30 Forest in the indicator catalogue
    (added 2026-10-28, looped to 9/10 by the same protocol as §21-§29)."""

    def _section(self, text, number):
        import re
        parts = re.split(r"\n## (\d+)\. ", text)
        for i in range(1, len(parts), 2):
            if int(parts[i]) == number:
                return parts[i + 1]
        self.fail(f"§{number} not found")

    def test_section_present_with_expected_row_counts(self):
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 30)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 21, "§30 row count")
        cross = [l for l in rows if "Cross-reference — see §" in l]
        self.assertEqual(len(cross), 5, "§30 cross-reference rows")
        self.assertEqual(len(rows) - len(cross), 16, "§30 new rows")
        self.assertIn("Forest extent and net area change", sec)
        self.assertIn("Primary and old-growth forest area and share", sec)
        self.assertIn("Harvested area and volume against the allowable "
                      "annual cut", sec)
        self.assertIn("Forest loss by driver", sec)
        self.assertIn("Pest and disease outbreak", sec)
        self.assertIn("Regeneration: seedling and sapling density", sec)
        self.assertIn("Net carbon flux: NEE / NEP", sec)

    def test_section_table_is_single_fragment(self):
        """T84: the §30 table is one contiguous block (see T81 for §21-§29)."""
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 30)
        lines = sec.splitlines()
        idx = [j for j, l in enumerate(lines) if l.startswith("|")]
        self.assertEqual(len(idx), 23, "§30 table lines")
        between = [l for l in lines[idx[0]:idx[-1] + 1]
                   if l.strip() and not l.startswith("|")]
        self.assertEqual(between, [], "§30 table split by prose")

    def test_quick_set_present_and_counts_updated(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("30 Forest", text)
        self.assertIn("- **Forest:** forest extent and net area change", text)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("§30 Forest", skill)
        self.assertIn("32-section tiered indicator catalogue", skill)
        self.assertIn("226 new table rows: 163 new indicators plus "
                      "63 cross-references", skill)
        self.assertIn("twelve new sections §21–§32", skill)
        skill_ru = rtext(os.path.join(ROOT, "SKILL.ru.md"))
        self.assertIn("§30 Лес", skill_ru)
        self.assertIn("каталог индикаторов из 32 разделов", skill_ru)

    def test_worked_example_and_sources_present(self):
        """T84: Harvard Forest worked example and the §30 source list live
        in references/, with published values and named [NEXT DATA] gaps."""
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        self.assertIn("## §30 — Forest", ex)
        self.assertIn("what a twin for Harvard Forest would show", ex)
        self.assertIn("2.0 ± 0.4 Mg C/ha/yr", ex)
        self.assertIn("29.6–53.0 m²/ha", ex)
        self.assertIn("net carbon source after 2014", ex)
        self.assertIn("Current canopy-cover percentage", ex)
        self.assertIn("## §30 — Forest", src)
        self.assertIn("10.1126/science.1201609", src)  # Pan et al. 2011
        self.assertIn("10.1126/science.1062962", src)  # Barford et al. 2001
        self.assertIn("10.1126/science.aau3445", src)  # Curtis et al. 2018
        self.assertIn("10.1002/ecm.1423", src)  # Finzi et al. 2020
        self.assertIn("4.14 B ha", src)
        self.assertIn("714 Gt", src)

    def test_no_new_unverified_flags_in_section(self):
        """T84: no §30 indicator row carries an [unverified] flag; exactly
        one [NEXT DATA] row is allowed — the mast yield index, added
        2026-10-28 with the Barguzinsky bear example (no published
        quantitative mast index for Buryatia 2026 exists). The
        worked-example note at the end of the section may name the
        example's gaps, and the sources file states the verification note.
        (The note is prose, not a row.)"""
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 30)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 21)
        for row in rows:
            self.assertNotIn("[unverified]", row)
        gaps = [l for l in rows if "[NEXT DATA]" in l]
        self.assertEqual(len(gaps), 1, "one [NEXT DATA] row in §30")
        self.assertIn("Mast yield index", gaps[0])
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        sec_src = src.split("## §30 — Forest", 1)[1]
        self.assertIn("No [unverified] flags in this section", sec_src)



class TestCroplandSection(unittest.TestCase):
    """T85: v2.8 domain section §31 Cropland in the indicator catalogue
    (added 2026-10-27, looped to 9/10 by the same protocol as §21-§30)."""

    def _section(self, text, number):
        import re
        parts = re.split(r"\n## (\d+)\. ", text)
        for i in range(1, len(parts), 2):
            if int(parts[i]) == number:
                return parts[i + 1]
        self.fail(f"§{number} not found")

    def test_section_present_with_expected_row_counts(self):
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 31)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 21, "§31 row count")
        cross = [l for l in rows if "Cross-reference — see §" in l]
        self.assertEqual(len(cross), 6, "§31 cross-reference rows")
        self.assertEqual(len(rows) - len(cross), 15, "§31 new rows")
        self.assertIn("Cropland extent and net area change", sec)
        self.assertIn("Crop rotation diversity and fallow share", sec)
        self.assertIn("Soil organic carbon stock under tillage", sec)
        self.assertIn("Irrigation water use and efficiency", sec)
        self.assertIn("Soil salinisation: ECe trend and salt-affected share", sec)
        self.assertIn("Fertiliser N/P balance, nitrogen-use efficiency and runoff", sec)
        self.assertIn("Pesticide pressure: use intensity and risk", sec)
        self.assertIn("Yield and yield stability", sec)
        self.assertIn("Soil erosion on arable land", sec)
        self.assertIn("Field-margin and biodiversity-strip share and condition", sec)
        self.assertIn("Rice-paddy water regime and methane", sec)

    def test_section_table_is_single_fragment(self):
        """T85: the §31 table is one contiguous block (see T81 for §21-§30)."""
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 31)
        lines = sec.splitlines()
        idx = [j for j, l in enumerate(lines) if l.startswith("|")]
        self.assertEqual(len(idx), 23, "§31 table lines")
        between = [l for l in lines[idx[0]:idx[-1] + 1]
                   if l.strip() and not l.startswith("|")]
        self.assertEqual(between, [], "§31 table split by prose")

    def test_quick_set_present_and_counts_updated(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("31 Cropland", text)
        self.assertIn("- **Cropland:** cropland extent and net area change", text)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("§31 Cropland", skill)
        self.assertIn("32-section tiered indicator catalogue", skill)
        self.assertIn("226 new table rows: 163 new indicators plus "
                      "63 cross-references", skill)
        self.assertIn("twelve new sections §21–§32", skill)
        skill_ru = rtext(os.path.join(ROOT, "SKILL.ru.md"))
        self.assertIn("§31 Пашня", skill_ru)
        self.assertIn("каталог индикаторов из 32 разделов", skill_ru)

    def test_worked_example_and_sources_present(self):
        """T85: GEPIS rice-paddy worked example and the §31 source list live
        in references/, with published values and named [NEXT DATA] gaps."""
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        self.assertIn("## §31 — Cropland", ex)
        self.assertIn("what a twin for the GEPIS rice paddies in Sri Lanka "
                      "would show", ex)
        self.assertIn("5.5–6.2 t/ha", ex)
        # T97: the national yield context is the DCS series, not the 2,853 study average.
        self.assertIn("3,731 kg/ha", ex)
        self.assertIn("470 mm", ex)
        self.assertIn("2.4–2.5", ex)
        self.assertIn("## §31 — Cropland", src)
        self.assertIn("10.1038/s41467-017-00232-0", src)  # Borrelli et al. 2017
        self.assertIn("10.1016/j.oneear.2020.02.007", src)  # Bowles et al. 2020
        self.assertIn("10.1111/ele.13576", src)  # Albrecht et al. 2020
        self.assertIn("10.1111/j.1365-2389.2005.00741.x", src)  # Mikhailova & Post 2006
        self.assertIn("10.3390/w16111616", src)  # Prasad et al. 2024
        self.assertIn("1,381 Mha", src)
        self.assertIn("185 Mt", src)

    def test_no_new_unverified_flags_in_section(self):
        """T85: no §31 indicator row carries an [unverified] flag or a
        [NEXT DATA] gap; the worked-example note at the end of the section
        may name the example's gaps, and the sources file states the
        verification note. (The note is prose, not a row.)"""
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 31)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 21)
        for row in rows:
            self.assertNotIn("[unverified]", row)
            self.assertNotIn("[NEXT DATA]", row)
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        sec_src = src.split("## §31 — Cropland", 1)[1]
        self.assertIn("No [unverified] flags in this section", sec_src)


class TestWetlandsSection(unittest.TestCase):
    """T86: v2.8 domain section §32 Non-peat wetlands and marshes in the
    indicator catalogue (added 2026-10-28, looped to 9/10 by the same
    protocol as §21-§31). No Russian worked example, pilot or showcase
    case in this module, by the user's correction of 2026-10-27; the
    regional case is Mongol Daguur, Mongolia."""

    def _section(self, text, number):
        import re
        parts = re.split(r"\n## (\d+)\. ", text)
        for i in range(1, len(parts), 2):
            if int(parts[i]) == number:
                return parts[i + 1]
        self.fail(f"§{number} not found")

    def test_section_present_with_expected_row_counts(self):
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 32)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 19, "§32 row count")
        cross = [l for l in rows if "Cross-reference — see §" in l]
        self.assertEqual(len(cross), 5, "§32 cross-reference rows")
        self.assertEqual(len(rows) - len(cross), 14, "§32 new rows")
        self.assertIn("Wetland extent and net area change", sec)
        self.assertIn("Hydroperiod: flooded duration", sec)
        self.assertIn("Water-level regime: stage, amplitude", sec)
        self.assertIn("Salinity regime (coastal and brackish marshes)", sec)
        self.assertIn("Sediment accretion and surface-elevation change", sec)
        self.assertIn("Nutrient retention: inflow–outflow", sec)
        self.assertIn("Waterbird use: breeding pairs", sec)
        self.assertIn("Fish nursery function", sec)
        self.assertIn("Invasive species: reed/cattail expansion", sec)
        self.assertIn("Drainage and reclamation pressure", sec)

    def test_section_table_is_single_fragment(self):
        """T86: the §32 table is one contiguous block (see T81 for §21-§31)."""
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 32)
        lines = sec.splitlines()
        idx = [j for j, l in enumerate(lines) if l.startswith("|")]
        self.assertEqual(len(idx), 21, "§32 table lines")
        between = [l for l in lines[idx[0]:idx[-1] + 1]
                   if l.strip() and not l.startswith("|")]
        self.assertEqual(between, [], "§32 table split by prose")

    def test_quick_set_present_and_counts_updated(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("32 Non-peat wetlands and marshes", text)
        self.assertIn("- **Non-peat wetlands and marshes:** wetland extent "
                      "and net area change", text)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("§32 Non-peat wetlands and marshes", skill)
        self.assertIn("32-section tiered indicator catalogue", skill)
        self.assertIn("226 new table rows: 163 new indicators plus "
                      "63 cross-references", skill)
        self.assertIn("twelve new sections §21–§32", skill)
        skill_ru = rtext(os.path.join(ROOT, "SKILL.ru.md"))
        self.assertIn("§32 Неторфяные водно-болотные угодья и марши", skill_ru)
        self.assertIn("каталог индикаторов из 32 разделов", skill_ru)

    def test_worked_example_and_sources_present(self):
        """T86: Everglades worked example and Mongol Daguur regional case,
        and the §32 source list, live in references/, with published values
        and named [NEXT DATA] gaps. No Russian worked example."""
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        self.assertIn("## §32 — Non-peat wetlands and marshes", ex)
        self.assertIn("what a twin for the Everglades would show", ex)
        self.assertIn("138,834", ex)
        self.assertIn("3,500 nests", ex)
        self.assertIn("Mongol Daguur", ex)
        self.assertIn("current sediment-accretion rate", ex)
        sec_ex = ex.split("## §32 — Non-peat wetlands and marshes", 1)[1]
        self.assertNotIn("Selenga", sec_ex)
        self.assertNotIn("Fefelov", sec_ex)
        self.assertIn("## §32 — Non-peat wetlands and marshes", src)
        self.assertIn("10.1071/MF14173", src)  # Davidson 2014
        self.assertIn("10.1073/pnas.032477999", src)  # Saltonstall 2002
        self.assertIn("10.1641/0006-3568(2001)051[0633:TICAMO]2.0.CO;2",
                      src)  # Beck et al. 2001
        self.assertIn("12.1 M km", src)
        self.assertIn("10 µg/L", src)

    def test_no_new_unverified_flags_in_section(self):
        """T86: no §32 indicator row carries an [unverified] flag or a
        [NEXT DATA] gap; the worked-example note at the end of the section
        may name the example's gaps, and the sources file states the
        verification note. (The note is prose, not a row.)"""
        import re
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        sec = self._section(text, 32)
        rows = [l for l in sec.splitlines()
                if l.startswith("| ") and not l.startswith("| Indicator | What it tells")
                and not re.match(r"^\|[-: |]+\|$", l)]
        self.assertEqual(len(rows), 19)
        for row in rows:
            self.assertNotIn("[unverified]", row)
            self.assertNotIn("[NEXT DATA]", row)
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        sec_src = src.split("## §32 — Non-peat wetlands and marshes", 1)[1]
        self.assertIn("No [unverified] flags in this section", sec_src)


class TestBarguzinskyBearExample(unittest.TestCase):
    """T87: Barguzinsky Reserve and the Buryatia taiga edge worked example
    (second example for §30, added 2026-10-28, on her decision of
    27 October 2026, 22:10 EDT — an explicit exception to the "no Russian
    worked examples" rule, only with links to authoritative sources for
    every figure)."""

    def test_example_present_with_verified_figures(self):
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        self.assertIn("Second worked example for §30", ex)
        self.assertIn("Barguzinsky Reserve and the Buryatia taiga edge", ex)
        self.assertIn("374,322 ha", ex)
        self.assertIn("6,113", ex)
        self.assertIn("6,276", ex)
        self.assertIn("5,385", ex)
        self.assertIn("4,625", ex)
        self.assertIn("0.21 per 1,000 ha", ex)
        self.assertIn("436 by 20 October", ex)
        self.assertIn("331 by 3 October", ex)
        self.assertIn("149 bears by", ex)
        self.assertIn("47 cases", ex)
        self.assertIn("Six attacks", ex)
        self.assertIn("two people died", ex)
        self.assertIn("1,272", ex)
        self.assertIn("1,500–2,000", ex)
        self.assertIn("22:10 EDT", ex)

    def test_reliability_caveat_and_gaps_named(self):
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        self.assertIn("summaries are not published openly", ex)
        for gap in ("Current brown bear numbers in the Barguzinsky Reserve",
                    "quantitative cedar-nut and berry mast index",
                    "Current wolf numbers in Buryatia",
                    "register of food attractants",
                    "numeric share of 2–3-year-old animals",
                    "long-term series of attacks in Buryatia by year"):
            self.assertIn(gap, ex)

    def test_cross_reference_rows_present(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("Brown bear abundance: state-monitoring count", text)
        self.assertIn("Age structure of conflict animals", text)
        self.assertIn("Human–wildlife conflict reports", text)
        self.assertIn("Food attractants register", text)
        self.assertIn("Quota uptake and regulated removal", text)
        self.assertIn("Mast yield index", text)
        self.assertIn("Taiga edge — human–bear conflict watch levels", text)
        self.assertIn("Zakamensk in September 2026", text)

    def test_sources_present(self):
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        self.assertIn("Barguzinsky bear sources", src)
        self.assertIn("zapovednoe-podlemorye.ru", src)
        self.assertIn("burunen.ru", src)
        self.assertIn("ulan.mk.ru", src)
        self.assertIn("vedomosti.ru", src)
        self.assertIn("yuga.ru", src)
        self.assertIn("Barguzinsky bear example (added 2026-10-28", src)
        self.assertIn("not published openly", src)


class TestFetchSatellite(Tmp):
    """T82: automated satellite fetch (scripts/fetch_satellite.py). All
    tests run offline on a recorded STAC response; no network is used."""

    FIXTURE = {
        "type": "FeatureCollection",
        "features": [
            {"id": "S2A_MSIL2A_20260810T045231_R076_T45RVM_20260810T112507",
             "collection": "sentinel-2-l2a",
             "properties": {"datetime": "2026-08-10T04:52:31.024000Z",
                            "eo:cloud_cover": 12.5},
             "assets": {
                 "B04": {"href": "https://example.invalid/s2/B04.tif",
                         "roles": ["data"],
                         "type": "image/tiff; application=geotiff; "
                                 "profile=cloud-optimized"},
                 "B08": {"href": "https://example.invalid/s2/B08.tif",
                         "roles": ["data"],
                         "type": "image/tiff; application=geotiff; "
                                 "profile=cloud-optimized"},
                 "visual": {"href": "https://example.invalid/s2/visual.tif",
                            "roles": ["overview"]}}},
            {"id": "S2A_MSIL2A_20260815T045231_R076_T45RVM_20260815T112507",
             "collection": "sentinel-2-l2a",
             "properties": {"datetime": "2026-08-15T04:52:31.024000Z",
                            "eo:cloud_cover": 45.0},
             "assets": {
                 "B04": {"href": "https://example.invalid/s2b/B04.tif",
                         "roles": ["data"]},
                 "B08": {"href": "https://example.invalid/s2b/B08.tif",
                         "roles": ["data"]}}},
            {"id": "S2A_MSIL2A_20260820T045231_R076_T45RVM_20260820T112507",
             "collection": "sentinel-2-l2a",
             "properties": {"datetime": "2026-08-20T04:52:31.024000Z"},
             "assets": {
                 "B04": {"href": "https://example.invalid/s2c/B04.tif",
                         "roles": ["data"]},
                 "B08": {"href": "https://example.invalid/s2c/B08.tif",
                         "roles": ["data"]}}},
        ],
    }

    def setUp(self):
        super().setUp()
        wtext(self.p("stac.json"), json.dumps(self.FIXTURE))

    def base_args(self, *extra):
        return ["--source", "sentinel-2",
                "--bbox", "85.5,28.2,86.0,28.5",
                "--start", "2026-08-01", "--end", "2026-08-31",
                "--stac-file", self.p("stac.json"),
                "--out", self.p("out"), *extra]

    def test_parse_scenes(self):
        mod = load("fetch_satellite")
        scenes = mod.parse_scenes(self.FIXTURE, "sentinel-2")
        self.assertEqual(len(scenes), 3)
        self.assertEqual(scenes[0]["id"],
                         "S2A_MSIL2A_20260810T045231_R076_T45RVM_20260810T112507")
        self.assertEqual(scenes[0]["datetime"], "2026-08-10T04:52:31.024000Z")
        self.assertEqual([s["cloud_cover"] for s in scenes],
                         [12.5, 45.0, None])
        self.assertEqual(sorted(scenes[0]["bands"]), ["B04", "B08"])
        # Overview assets are not data bands.
        self.assertEqual(scenes[0]["assets_available"], ["B04", "B08"])

    def test_ndvi_math(self):
        mod = load("fetch_satellite")
        values = mod.ndvi_from_arrays([100, 200, 0], [300, 200, 0])
        self.assertEqual(values, [0.5, 0.0, None])
        self.assertEqual(mod.ndvi_stats(values),
                         {"mean": 0.25, "min": 0.0, "max": 0.5,
                          "n_valid": 2, "n_total": 3})
        self.assertEqual(mod.ndvi_stats([None, None]),
                         {"mean": None, "min": None, "max": None,
                          "n_valid": 0, "n_total": 2})

    def test_check_mode_writes_manifest_no_download(self):
        code, out, err = run("fetch_satellite.py",
                             *self.base_args("--check", "--max-cloud", "100"))
        self.assertEqual(code, 0, err)
        self.assertIsNotNone(out)
        self.assertEqual(out["tool"], "fetch_satellite.py")
        self.assertEqual(out["version"], "2.8")
        with open(os.path.join(self.p("out"), "manifest.json")) as fh:
            manifest = json.load(fh)
        self.assertEqual(len(manifest["scenes"]), 3)
        self.assertEqual(manifest["downloads"], [])
        self.assertEqual(manifest["ndvi"]["status"], "not-computed")
        self.assertEqual([f for f in os.listdir(self.p("out"))
                          if f.endswith(".tif")], [])
        with open(os.path.join(self.p("out"), "virtual-sensor.json")) as fh:
            sensor = json.load(fh)
        self.assertEqual(sensor["name"], "satellite-sentinel-2-ndvi")
        self.assertEqual(sensor["quantity"], "NDVI")
        self.assertEqual(sensor["formula"], "(NIR - red) / (NIR + red)")
        self.assertEqual(sensor["collection"], "sentinel-2-l2a")
        self.assertIn("periodic virtual sensor", sensor["validity_window"])

    def test_max_cloud_filters(self):
        # Default --max-cloud 20: the 45% scene drops; the scene with no
        # cloud value is kept (an unmeasured cloud cover is a gap, not a
        # reason to drop).
        code, out, err = run("fetch_satellite.py",
                             *self.base_args("--check"))
        self.assertEqual(code, 0, err)
        self.assertEqual(len(out["scenes"]), 2)
        self.assertEqual([s["cloud_cover"] for s in out["scenes"]],
                         [12.5, None])

    def test_bad_bbox_rejected(self):
        code, out, err = run("fetch_satellite.py",
                             "--source", "sentinel-2",
                             "--bbox", "1,2,3",
                             "--start", "2026-08-01", "--end", "2026-08-31",
                             "--check")
        self.assertNotEqual(code, 0)
        self.assertIn("bbox", err)

    def test_unreachable_catalog_clear_error(self):
        code, out, err = run("fetch_satellite.py",
                             "--source", "sentinel-2",
                             "--bbox", "85.5,28.2,86.0,28.5",
                             "--start", "2026-08-01", "--end", "2026-08-31",
                             "--catalog-url", "http://127.0.0.1:9/stac/v1",
                             "--check")
        self.assertEqual(code, 3, err)
        self.assertIn("unreachable", err)

    def test_copernicus_landsat_rejected(self):
        code, out, err = run("fetch_satellite.py",
                             *self.base_args("--catalog", "copernicus",
                                            "--source", "landsat",
                                            "--check"))
        self.assertEqual(code, 2, err)
        self.assertIn("not served", err)

    def test_help(self):
        code, out, err = run("fetch_satellite.py", "--help")
        self.assertEqual(code, 0, err)


class TestRegisteredVirtualSensors(unittest.TestCase):
    """T83: registered virtual sensors (Variant B, 2026-10-28). Six
    registrations in the worked example, each with a published formula,
    a named calibration station, and a skill score or an explicit honest
    gap; Sentinel-1 and Open-Meteo in the source list."""

    def test_six_registrations_present(self):
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        self.assertIn("## Registered virtual sensors — worked example:",
                      ex)
        self.assertEqual(ex.count("### Sensor "), 6)
        for name in ("beira-chla-s2-ndci", "beira-wst-landsat-st",
                     "beira-extent-s2-mndwi", "beira-turbidity-s2-dogliotti",
                     "beira-zsd-s2-qaa", "langtang-displacement-s1-insar"):
            self.assertIn(name, ex)

    def test_formulas_scores_and_gaps(self):
        ex = rtext(os.path.join(ROOT, "references",
                                "worked-examples-new-sections.md"))
        # Published formulas, as registered (no invented coefficients).
        for formula in ("194.325", "86.115", "228.1 FNU", "3078.9 FNU",
                        "Min(Kd", "MNDWI = (Green",
                        "split-window algorithm",
                        "Δd = λ·Δφ / (4π)"):
            self.assertIn(formula, ex)
        # Published skill scores (generic validation, or Beira-local).
        for score in ("RMSE 1.43 µg/L", "RMSE 0.87 K", "RMSE 0.74 K",
                      "RMSE 20.5 FNU", "RMSE 0.049 m", "±10 mm"):
            self.assertIn(score, ex)
        # Every registration without a local score says so honestly:
        # five sensor-level [NEXT DATA] gaps, plus one mention in the
        # section intro; each of the six sensors carries a skill-score
        # field. (Phrases checked on whitespace-normalised text: the
        # file hard-wraps long lines.) The tail is bounded at the §30
        # section, which follows the sensor section in the file.
        tail = ex.split("## Registered virtual sensors — worked example:",
                        1)[1].split("\n## §30 — Forest", 1)[0]
        self.assertEqual(tail.count("[NEXT DATA]"), 6)
        self.assertEqual(tail.count("Skill score (SS_RMSE)"), 6)
        flat = " ".join(ex.split())
        self.assertIn("no in-situ turbidity", flat)
        self.assertIn("no GNSS station", flat)

    def test_sources_and_data_sources_updated(self):
        src = rtext(os.path.join(ROOT, "references",
                                 "sources-new-sections.md"))
        self.assertIn("## Sources — registered virtual sensors "
                      "(Variant B, 2026-10-28)", src)
        self.assertIn("10.1016/j.rse.2014.09.020", src)
        self.assertIn("10.3390/w16111616", src)
        self.assertIn("0.049 m", src)
        ds = rtext(os.path.join(ROOT, "references", "data-sources.md"))
        self.assertIn("| Sentinel-1 (Copernicus) | SAR C-band", ds)
        self.assertIn("| Open-Meteo (open-meteo.com) | Forecast weather API",
                      ds)
        self.assertIn("no API key", ds)


class TestSensorRegistry(unittest.TestCase):
    """T88: full sensor registry (2026-10-28). 59 rows (R01-R59) mapping
    every source in data-sources.md to the ecosystems and indicator rows
    it serves, in exactly four tiers; the seven registered virtual
    sensors carried verbatim; no invented formula, score, or station."""

    EXPECTED_SOURCES = (
        "Sentinel-2", "Sentinel-5P", "Sentinel-1", "Landsat 8/9",
        "MODIS / VIIRS", "Copernicus DEM", "ERA5",
        "National meteo services", "OpenAQ", "CAMS", "Open-Meteo",
        "National hydrology gauges", "GRDC", "GEMStat",
        "JRC Global Surface Water", "GRACE", "GLOSS",
        "Agency and institute archives", "Client and field sampling",
        "GBIF", "iNaturalist", "eBird", "National red lists",
        "Movebank", "Museum", "SoilGrids", "ESDAC",
        "National soil and cadastre maps", "CORINE", "SensorThings",
        "WaterML 2.0", "Darwin Core", "EML", "STAC", "CF conventions",
        "RO-Crate", "Evidence platforms", "In-situ sensors",
        "Farm records", "Prior studies and EIA reports",
        "NASA FIRMS", "Global Forest Watch", "ESA WorldCover",
        "OpenStreetMap", "GPM IMERG", "SMAP",
        "Copernicus Marine Service", "WDPA",
    )

    def _rows(self):
        reg = rtext(os.path.join(ROOT, "references", "sensor-registry.md"))
        rows = [ln for ln in reg.splitlines()
                if re.match(r"\| R\d\d \|", ln)]
        parsed = []
        for ln in rows:
            cells = [c.strip() for c in ln.split("|")]
            parsed.append(cells)
        return reg, parsed

    def test_registry_exists_and_counts(self):
        reg, rows = self._rows()
        self.assertEqual(len(rows), 59)
        ids = [c[1] for c in rows]
        self.assertEqual(ids, ["R%02d" % i for i in range(1, 60)])
        tiers = collections.Counter(c[7] for c in rows)
        self.assertEqual(tiers["Core"], 1)
        self.assertEqual(tiers["Conditional"], 35)
        self.assertEqual(tiers["Research"], 3)
        self.assertEqual(tiers["Context-only"], 20)
        self.assertEqual(len(rows[0]) - 2, 11)

    def test_every_source_appears(self):
        reg, _ = self._rows()
        self.assertEqual(len(self.EXPECTED_SOURCES), 48)
        for name in self.EXPECTED_SOURCES:
            self.assertIn(name, reg, "source missing from registry: %s"
                          % name)

    def test_section_coverage(self):
        _, rows = self._rows()
        served = set()
        for c in rows:
            served.update(int(x) for x in
                          re.findall(r"§(\d+)", c[6]))
        # Every indicator-bearing section is served; §§18-20 are meta
        # sections (quick sets, metadata, watch rules), served by the
        # catalogue itself, never by a sensor row.
        self.assertEqual(sorted(served),
                         list(range(1, 18)) + list(range(21, 33)))

    def test_tiers_only_allowed(self):
        _, rows = self._rows()
        for c in rows:
            self.assertIn(c[7], ("Core", "Conditional", "Research",
                                 "Context-only"), c[1])

    def test_core_has_formula_and_cited_score(self):
        _, rows = self._rows()
        cores = [c for c in rows if c[7] == "Core"]
        self.assertEqual(len(cores), 1)
        core = cores[0]
        self.assertEqual(core[1], "R05")
        self.assertIn("Min(Kd)", core[4])
        self.assertIn("0.049 m", core[9])
        self.assertIn("Prasad", core[9])
        # Every numeric score claim in the table carries a citation.
        for c in rows:
            score = c[9]
            if re.search(r"\d", score) and (
                    "RMSE" in score or "%" in score
                    or "accuracy" in score.lower()):
                self.assertRegex(" ".join(c),
                                 r"et al\.|20\d\d|Prasad|Hansen|Reichle"
                                 r"|Pekel|Eon|Dogliotti|Mishra|Molkov"
                                 r"|Lee",
                                 "uncited numeric score in %s" % c[1])

    def test_seven_registered_sensors_verbatim(self):
        reg, _ = self._rows()
        for name in ("beira-chla-s2-ndci", "beira-wst-landsat-st",
                     "beira-extent-s2-mndwi", "beira-turbidity-s2-dogliotti",
                     "beira-zsd-s2-qaa", "langtang-displacement-s1-insar"):
            self.assertIn(name, reg)
        for value in ("194.325", "86.115", "228.1 FNU", "3078.9 FNU",
                      "MNDWI = (Green", "split-window algorithm",
                      "0.049 m", "0.87 K", "0.74 K", "20.5 FNU",
                      "1.43 µg/L", "±10 mm"):
            self.assertIn(value, reg)
        self.assertIn("No seventh sensor with a formula exists",
                      " ".join(reg.split()))

    def test_new_sources_in_data_sources_and_skill_pointer(self):
        ds = rtext(os.path.join(ROOT, "references", "data-sources.md"))
        for name in ("NASA FIRMS", "Global Forest Watch / Hansen",
                     "ESA WorldCover", "OpenStreetMap", "GPM IMERG",
                     "SMAP", "Copernicus Marine Service", "WDPA"):
            self.assertIn(name, ds)
        self.assertIn("references/sensor-registry.md", ds)
        self.assertIn("Russian Federation", ds)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("references/sensor-registry.md", skill)


class TestUnverifiedFlagsClosed(unittest.TestCase):
    """T89: no live [unverified] flag remains in the catalogue; both closures
    carry verified anchors (2026-10-28, on her word "Заверши 2 пометки")."""

    def test_no_live_unverified_flag_in_indicator_rows(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        rows = [l for l in text.splitlines() if l.startswith("|")]
        self.assertTrue(rows)
        for row in rows:
            self.assertNotIn("[unverified", row)

    def test_marmot_row_closed_with_verified_anchors(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for s in ("Enkhsaikhan et al. 2021", "10.5564/pib.v37i1.3137",
                  "0.63 marmots/ha", "10.1038/s41598-023-38966-1",
                  "Endangered (IUCN criterion A2ad)", "Least Concern",
                  "no universal density threshold exists"):
            self.assertIn(s, text)

    def test_green_space_row_closed_with_verified_anchors(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for s in ("D.M. 1444/1968", "18 m² per inhabitant",
                  "10.3389/frsc.2025.1542464",
                  "10.1016/j.landurbplan.2025.105301",
                  "0.5–1 ha within 300 m"):
            self.assertIn(s, text)
        src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        self.assertNotIn("REMAINS [unverified]", src)
        self.assertIn("Both items this section had marked [unverified] are now RESOLVED", src)
        self.assertIn("RESOLVED 28 October 2026 — the marmot-density item is closed", src)


class TestThresholdsGuideApplied(unittest.TestCase):
    def test_file_exists_with_contents(self):
        path = os.path.join(ROOT, "references", "thresholds.md")
        self.assertTrue(os.path.exists(path))
        text = rtext(path)
        head = "\n".join(text.splitlines()[:15])
        self.assertIn("## Contents", head)
        self.assertIn("21 indicators", text)
        self.assertIn("7 jurisdictions", text)
        for section in ("## 0.", "## 7.", "## 8.", "## 9.", "## 10.", "## 11."):
            self.assertIn(section, text)

    def test_anchor_hierarchy_and_rules(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        for s in ("Иерархия якорей", "более строгий",
                  "Пороги по назначению",
                  "Оперативный порог раннего предупреждения",
                  "70–80%"):
            self.assertIn(s, text)
        ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for s in ("Anchor hierarchy", "Thresholds by use",
                  "Operational early-warning level",
                  "the stricter binding standard governs the red band",
                  "Threshold anchors for the 21 core indicators"):
            self.assertIn(s, ind)

    def test_key_anchors_present(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        for s in ("50 мг/л", "5 мкг/м³", "4 ≤ DHW < 8", "10 мкг/л",
                  "TSI 0–40", "0,01 мг/л", "Directive (EU) 2020/2184",
                  "WHO Global Air Quality Guidelines, 2021"):
            self.assertIn(s, text)

    def test_provisional_flags_preserved(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertEqual(text.count("[provisional"), 25)
        for s in ("СанПиН 1.2.3685-21 [provisional]", "7,1 [provisional]",
                  "32,0 [provisional]",
                  "[provisional — по вторичному пересказу]",
                  "[provisional — классы по вторичному источнику]"):
            self.assertIn(s, text)

    def test_russian_lead_not_entered(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        lead_row = [ln for ln in text.splitlines()
                    if ln.startswith("| Свинец, питьевая вода")]
        self.assertEqual(len(lead_row), 1)
        self.assertIn("Не проверено", lead_row[0])
        self.assertIn("значение для свинца не внесено из-за противоречия источников",
                      text)
        # the contested 0.03 figure appears for lead only where the guide
        # says it is NOT entered, never as an adopted limit
        lead_lines = [ln for ln in text.splitlines()
                      if "0,03 мг/л" in ln and "Свинец" in ln
                      or "0,03 мг/л" in ln and "свинца не внесено" in ln]
        self.assertEqual(len(lead_lines), 2)
        for ln in lead_lines:
            self.assertIn("не внесено", ln)

    def test_no_unverified_flags(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertNotIn("[unverified]", text)

    def test_skill_and_indicators_pointers(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertLessEqual(len(skill.splitlines()), 500)
        self.assertIn("references/thresholds.md", skill)
        self.assertIn("decision support", skill)
        self.assertIn("ЛПР", skill)
        ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("references/thresholds.md", ind)

    def test_open_items_preserved(self):
        text = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertIn("Что остаётся открытым", text)
        for s in ("Россия — воздух", "Море — растворённый кислород",
                  "не внесён", "Япония — воздух"):
            self.assertIn(s, text)


class TestRemainingNextDataGapsVerified(unittest.TestCase):
    """T91, 2026-10-28: the three priority [NEXT DATA] gaps (Beira-local
    SS_RMSE for Sensors 1-4, Langtang InSAR ground truth, Daursky marmot
    density) are closed as verified negative results, not as values —
    each with its reason and its named next data; nothing is invented."""

    def test_beira_gaps_are_verified_negatives_not_bare_flags(self):
        ex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))
        for s in ("verified 2026-10-28 (T91)",
                  "never applied NDCI or any chlorophyll-a retrieval",
                  "never used Landsat surface",
                  "is a single total, not a shoreline polygon or a mask",
                  "structurally impossible from the published record"):
            self.assertIn(s, ex)
        reg = rtext(os.path.join(ROOT, "references", "sensor-registry.md"))
        self.assertEqual(reg.count("verified 2026-10-28 (T91)"), 10)

    def test_no_invented_beira_local_rmse(self):
        import re as _re
        for name in ("worked-examples-new-sections.md", "sensor-registry.md"):
            text = rtext(os.path.join(ROOT, "references", name))
            for m in _re.finditer(r"Beira-local SS_RMSE[\s\S]{0,200}", text):
                window = " ".join(m.group(0).split())
                self.assertTrue("[NEXT DATA]" in window
                                or "verified 2026-10-28 (T91)" in window,
                                window)
            self.assertNotIn("Beira-local SS_RMSE: 0.", text)

    def test_supplement_maps_correction(self):
        ex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))
        self.assertIn("interpolated maps (supplement Figs. S7–S8", ex)
        self.assertIn("does not appear in the supplement list", ex)
        self.assertNotIn("values in the paper's supplement, Figs. S7–S9", ex)
        reg = rtext(os.path.join(ROOT, "references", "sensor-registry.md"))
        self.assertNotIn("Figs. S7–S9", reg)

    def test_langtang_ground_truth_never_retrospective(self):
        reg = rtext(os.path.join(ROOT, "references", "sensor-registry.md"))
        for s in ("10.1007/s12524-026-02611-x",
                  "no ground truth exists for that slope",
                  "can ever be collected retrospectively",
                  "cross-sensor, not ground truth"):
            self.assertIn(s, reg)
        src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        for s in ("Roy P., Majumdar R., Chauhan P. et al.",
                  "Sah A. K.", "non-peer-reviewed"):
            self.assertIn(s, src)

    def test_daursky_marmot_density_still_open_with_comparators(self):
        ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        for s in ("still unpublished", "1–7 ind/ha",
                  "6819035", "1.27 ind/ha", "Todgerel 2020",
                  "the primary Todgerel 2020 document was not consulted", "«Летопись природы»"):
            self.assertIn(s, ind)
        self.assertNotIn("provisional", ind)
        ex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))
        self.assertIn("Hustai National Park, ca. 1.27 ind/ha", ex)
        self.assertIn("not a Daursky value", ex)

    def test_registry_rows_carry_the_t91_verdict(self):
        reg = rtext(os.path.join(ROOT, "references", "sensor-registry.md"))
        for row in ("| R02 |", "| R03 |", "| R04 |", "| R09 |", "| R12 |"):
            line = [ln for ln in reg.splitlines() if ln.startswith(row)]
            self.assertEqual(len(line), 1, row)
            self.assertIn("verified 2026-10-28 (T91)", line[0], row)


class TestQuickFixesOct28(unittest.TestCase):
    """T92, 2026-10-28: quick fixes from the external 7.5/10 audit (verified
    against the files first — two of its points were wrong: the frontmatter
    error is only in SKILL.ru.md, and no code checks a '[NO DATA]' literal).
    Description rewritten for v2.8, script table moved to references/,
    SKILL.ru.md comment moved below the frontmatter."""

    def test_description_covers_v28_domains(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            fm = text.split("---\n", 2)[1]
            import yaml as _yaml
            desc = _yaml.safe_load(fm)["description"]
            self.assertLessEqual(len(desc), 1024)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        desc = skill.split("---\n", 2)[1]
        for s in ("forests", "peatlands", "marine and coastal",
                  "urban ecosystems", "deserts", "tundra and cryosphere",
                  "livestock farms", "cropland"):
            self.assertIn(s, desc)

    def test_script_table_moved_to_references(self):
        table = rtext(os.path.join(ROOT, "references", "scripts.md"))
        self.assertEqual(table.count("| `scripts/"), 17)
        for s in ("scripts/fetch_satellite.py", "scripts/trend_test.py",
                  "scripts/mismatch.py", "scripts/registry.py"):
            self.assertIn(s, table)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertLessEqual(len(skill.splitlines()), 500)
        self.assertIn("references/scripts.md", skill)
        # the full table no longer lives in SKILL.md
        self.assertEqual(skill.count("| `scripts/"), 0)

    def test_russian_frontmatter_starts_on_line_one(self):
        text = rtext(os.path.join(ROOT, "SKILL.ru.md"))
        self.assertTrue(text.startswith("---\n"))
        self.assertNotIn("<!--", text.split("---\n", 2)[1])
        self.assertIn("<!-- Русский перевод SKILL.md, версия 2.8. -->",
                      text.split("---\n", 2)[2][:200])


class TestSafetyGatePfasMicroplastics(unittest.TestCase):
    """T93, 2026-10-28: PFAS and microplastics in the circular-economy
    safety gate (on her word "Да, добавь PFAS и микро пластик"). The
    catalogue already carried both as conditional panels (§6); the gate
    did not. PFAS anchors are jurisdictional law (US EPA NPDWR Apr 2024;
    EU Directive 2020/2184), checked against the regulators' published
    values; no numeric microplastics limit is invented — the gate checks
    the method and the reported load, and [НЕТ ДАННЫХ] blocks."""

    def test_gate_names_pfas_and_microplastics(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertIn("PFAS", text)
            self.assertIn("микропластик", text.lower())
            gate = text.split("Template 2" if fname == "SKILL.md"
                               else "Шаблон 2")[1]
            self.assertIn("PFAS", gate)
            self.assertIn("микропластик", gate.lower())

    def test_pfas_anchors_are_jurisdictional(self):
        # T95 (2026-10-28): the numbers moved out of the gate into
        # references/thresholds.md §1.8; the gate keeps the rule only.
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        for s in ("4,0 нг/л", "0,1 мкг/л", "0,5 мкг/л", "2020/2184",
                  "NPDWR", "PFOA", "PFOS", "DüMV", "PFAS4 15"):
            self.assertIn(s, th)
        # the 2025 EPA reconsideration is disclosed, not hidden
        # T94 (2026-10-28): the May 2025 wording was wrong — May 2025 was
        # only EPA's announcement of intent; the formal proposal is
        # 20 May 2026 (Federal Register 2026-10085).
        self.assertIn("20 мая 2026", th)
        self.assertNotIn("май 2025", th)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertNotIn("май 2025", skill)

    def test_microplastics_gate_is_method_not_number(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        gate = skill.split("Template 2")[1].split("## Deterministic")[0]
        self.assertIn("числового норматива не изобретается", gate)
        for s in ("гармонизированный метод", "диапазон размеров",
                  "контрольные пробы", "[НЕТ ДАННЫХ]"):
            self.assertIn(s, gate)

    def test_non_negotiable_five_names_both(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertIn("PFAS", text)
            self.assertIn("микропластик", text.lower())


class TestSafetyGatePfasMatrices(unittest.TestCase):
    """T94, 2026-10-28: Claude Anthropic's point (e) corrections to the
    PFAS gate, verified against the primary sources before applying.
    The May 2025 date was wrong (that was only an announcement of
    intent); the formal rescission proposal is 20 May 2026, Federal
    Register 2026-10085, comments to 20 Jul 2026, not final as of Aug
    2026. Drinking-water ng/L limits do not apply to solid sediment in
    µg/kg — the gate now carries sediment anchors."""

    def test_rescission_date_is_may_2026_not_2025(self):
        # T95: the dates live in thresholds.md §1.8 now, not in the gate.
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        for s in ("20 мая 2026", "2026-10085", "20 июля 2026"):
            self.assertIn(s, th)
        self.assertNotIn("май 2025", th)
        for fname in ("SKILL.md", "SKILL.ru.md"):
            self.assertNotIn("май 2025",
                              rtext(os.path.join(ROOT, fname)))

    def test_four_values_marked_provisional(self):
        # T95: the values and their [provisional] marks live in §1.8.
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertIn("10 нг/л", th)
        self.assertIn("индекс опасности 1 для смесей [provisional]", th)
        self.assertIn("все шесть MCL действуют", th)

    def test_sediment_anchors_present_and_water_limits_excluded(self):
        # T95: anchors in §1.8; the "do NOT apply to solids" rule stays
        # in the gate itself.
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        for s in ("DüMV", "100", "50", "Danish EPA", "PFAS4 15",
                  "1 мкг/кг", "20 мкг/кг"):
            self.assertIn(s, th)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        gate = skill.split("Template 2")[1].split("## Deterministic")[0]
        self.assertIn("НЕ применимы", gate)

    def test_microplastics_row_unchanged(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        gate = skill.split("Template 2")[1].split("## Deterministic")[0]
        self.assertIn("числового норматива не изобретается", gate)


class TestGateThresholdRuleOct28(unittest.TestCase):
    """T95, 2026-10-28: Claude Anthropic's 8/10 review, verified point by
    point before applying, with the author's two amendments from Claude's
    own follow-up. (1) The gate rule: binding standard = red + block;
    guidance/draft = yellow, no block; no binding standard -> the
    threshold is chosen by the Stage 1 hierarchy and fixed in the Object
    Passport BEFORE data arrives, and becomes red for this build; no
    measurement ([НЕТ ДАННЫХ]) still blocks. (2) The brand-candidate line
    is removed from SKILL.md entirely (it lives in CHANGELOG now).
    PFAS numbers moved to references/thresholds.md §1.8; jurisdiction
    count 5 -> 7 (Germany, Denmark added)."""

    def test_pfas_numbers_live_in_thresholds_not_skill(self):
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertIn("### 1.8. PFAS", th)
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            gate = text.split("Template 2" if fname == "SKILL.md"
                               else "Шаблон 2")[1].split("## Deterministic" if fname == "SKILL.md" else "## Схемы ввода-вывода")[0]
            self.assertIn("references/thresholds.md", gate)
            self.assertIn("§1.8", gate)
            for s in ("4,0 нг/л", "2026-10085", "DüMV", "PFAS4 15"):
                self.assertNotIn(s, gate)

    def test_gate_rule_covers_both_cases(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        gate = skill.split("Template 2")[1].split("## Deterministic")[0]
        for s in ("красный уровень", "жёлтый уровень",
                  "ДО получения данных", "красным",
                  "для этой сборки", "блокирует",
                  "поток всегда", "[НЕТ ДАННЫХ]"):
            self.assertIn(s, gate)

    def test_brand_line_removed_from_skill(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertNotIn("ADIS", text)
            self.assertNotIn("кандидаты", text)

    def test_description_covers_steppe_and_aquaculture(self):
        en = rtext(os.path.join(ROOT, "SKILL.md"))
        desc_en = en.split('description: "')[1].split('"')[0]
        self.assertIn("steppe", desc_en)
        self.assertIn("aquaculture", desc_en)
        ru = rtext(os.path.join(ROOT, "SKILL.ru.md"))
        desc_ru = ru.split('description: "')[1].split('"')[0]
        self.assertIn("степь", desc_ru)
        self.assertIn("аквакультура", desc_ru)

    def test_jurisdiction_count_seven(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertNotIn("5 jurisdictions", text)
            self.assertNotIn("5 юрисдикций", text)
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertIn("21 indicators", th)
        self.assertIn("7 jurisdictions", th)
        self.assertIn("Germany, Denmark", th)

    def test_gap_markers_defined(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertIn("[NEXT DATA]", text)
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("Two gap markers", skill)

    def test_date_updated_to_oct_28(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertIn('last-reviewed: "2026-10-28"', text)
            self.assertIn("2.8 (2026-10-28)", text)
            self.assertNotIn("2026-10-27", text)

    def test_stage2_satellite_scope(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("returns scenes and NDVI, not water transparency/SDD",
                      skill)
        self.assertIn("signed through the data API", skill)


class TestTablesClosedOct28(unittest.TestCase):
    """T96, 2026-10-28: Claude Anthropic's full-candidate review (8/10),
    verified against primary sources before applying. The §31 table was
    not closed by a blank line (L1947-1948), so the prose after it rendered
    as table rows; the suite had no check for it. This class pins the
    closure rule for every table, the §31 regression, the §30-§32 format
    alignment (12 watch-levels subheads and 12 does-NOT-do subheads), and
    the gate qualification from the same review: the stricter *binding*
    standard governs red, guidance and drafts stay yellow."""

    def test_every_table_run_followed_by_blank_line(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        lines = text.split("\n")
        runs = 0
        i = 0
        while i < len(lines):
            if lines[i].startswith("|"):
                runs += 1
                j = i
                while j < len(lines) and lines[j].startswith("|"):
                    j += 1
                if j < len(lines):
                    self.assertEqual(
                        lines[j], "",
                        f"table run ending at line {j} is not followed by a blank line: {lines[j][:80]!r}")
                i = j
            else:
                i += 1
        self.assertEqual(runs, 29, "table count changed — check the catalogue")

    def test_section_31_table_closed_regression(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("as the diagnostic group |\n\n### How §20 watch levels apply here", text)

    def test_watch_levels_subheads_twelve_each(self):
        text = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertEqual(text.count("### How §20 watch levels apply here"), 12)
        self.assertEqual(text.count("### What this section does NOT do"), 12)
        self.assertNotIn("What this section does **not** do:", text)

    def test_stricter_binding_standard_qualifies_red(self):
        skill = rtext(os.path.join(ROOT, "SKILL.md"))
        self.assertIn("stricter binding standard governs red, guidance and drafts stay yellow",
                      skill)
        self.assertNotIn("the stricter governs red", skill)
        ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.assertIn("the stricter binding standard governs the red band; guidance and drafts stay yellow",
                      ind)
        self.assertNotIn("the stricter governs the red band", ind)


class TestT96FollowUpOct28(unittest.TestCase):
    """T97, 2026-10-28: Claude Anthropic's re-review of the T96 build
    (8.5/10). The T96 archive failed its own lint (a backticked path to the
    planned, not-yet-written gate_check.py in CHANGELOG.md); the §24 Tier 1
    factors were re-swapped (cropland and grassland values exchanged); the
    source list and the GEPIS worked example still carried the figures
    T96 corrected in the catalogue; one §25 sentence was broken; the §28
    topsoil/subsoil split was attributed to the 2024 report. This class
    pins each fix so it cannot drift back."""

    def setUp(self):
        self.ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        self.wex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))

    def test_tier1_factors_match_ipcc_table_2_1(self):
        self.assertIn(
            "cropland: 7.9 t CO₂-C/ha/yr boreal and temperate, 14.0 tropical; "
            "grassland: 5.7 boreal; temperate 5.3 nutrient-poor, 6.1 nutrient-rich "
            "deep-drained, 3.6 nutrient-rich shallow-drained; 9.6 tropical", self.ind)
        for wrong in ("cropland 5.7", "grassland 7.9", "5.3 warm temperate"):
            self.assertNotIn(wrong, self.ind)
        self.assertIn("cropland 7.9 boreal and temperate", " ".join(self.src.split()))

    def test_sources_synced_with_catalogue(self):
        flat = " ".join(self.src.split())
        for stale in ("Peatland Code v1.2 (2022) — five", "peak in the 1990s by 2021",
                      "NDVI-to-FVC scaling; the pixel-dichotomy form"):
            self.assertNotIn(stale, flat)
        for fresh in ("Peatland Code v2.1 (October 2024", "Gutman, G. & Ignatov, A. (1998)",
                      "Fluet-Chouinard, E. et al. 2023", "4.3 M ha in 2025",
                      "21 in Nepal, 25 in the Tibet", "2022/23 Maha 3,731 kg/ha",
                      "peak in 2003, about 490,000", "One Earth* 4(12)"):
            self.assertIn(fresh, flat)

    def test_worked_example_yields_synced(self):
        flat = " ".join(self.wex.split())
        self.assertNotIn("~2,853 kg/ha and Yala", flat)
        self.assertIn("2022/23 Maha 3,731 kg/ha and 2023 Yala 4,128 kg/ha", flat)

    def test_dhw_sentence_whole(self):
        self.assertIn("both limits are recorded in Phase 1 onboarding in the Object Passport. "
                      "Shellfish-bed closures follow biotoxin", self.ind)
        self.assertNotIn("not a DHW reading\nin Phase 1", self.ind)

    def test_salt_split_labelled_2021(self):
        self.assertIn("Depth split from the earlier FAO Global Map of Salt-Affected Soils (2021)",
                      self.ind)

    def test_cryosphere_quick_set(self):
        flat = " ".join(self.ind.split())
        self.assertIn("glacier mass balance where a glacier is present", flat)
        self.assertIn("(active-layer thickness per §29)", flat)

    def test_ru_stage1_carries_the_hierarchy(self):
        ru = " ".join(rtext(os.path.join(ROOT, "SKILL.ru.md")).split())
        self.assertIn("красный уровень задаёт более строгий обязательный норматив", ru)


class TestAccuracySweepOct28(unittest.TestCase):
    """T98, 2026-10-28: a further accuracy sweep of §21–§32 against primary
    sources (Claude, at the author's request). Confirmed without change:
    Taranger et al. 2015 (21 of 34 populations), EU 2024/1244 (500 t, from
    1 January 2028), Morris et al. 2016 (0.3 cm/yr), ITS_LIVE v2.0
    (The Cryosphere 19:3517), NYC CSO (398 outfalls, ~18 bn gal/yr),
    Western Arctic peak (490,000 in 2003, ADF&G). Corrected: the Everglades
    slope and remaining extent (the two cited sources differ — carried as
    'about 2 inches per mile or less' and 'about half'); the Norwegian
    density rule cited by title (paragraph confirmed as §19 in T99); the copper row
    given its ASC indicator and value; the §23 grazing rows reduced to
    cross-references to §22 plus the farm reading; draft wording cleared
    from the source list."""

    def setUp(self):
        self.ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        self.wex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))

    def test_everglades_slope_and_extent(self):
        flat = " ".join(self.ind.split())
        self.assertIn("less than two inches per mile (≈3 cm/km; Florida Museum", flat)
        self.assertNotIn("about 2.5 inches per mile (≈4 cm/km)", flat)
        self.assertIn("about half remains", flat)
        self.assertNotIn("just over half remains, mostly broken", flat)
        self.assertNotIn("just over half remains today", " ".join(self.wex.split()))

    def test_norway_density_cited_by_title(self):
        self.assertNotIn("Norwegian aquaculture regulation, §19", self.ind)
        self.assertIn("akvakulturdriftsforskriften", self.ind)

    def test_copper_row_has_asc_indicator(self):
        self.assertIn("ASC Salmon Standard, Indicator 4.7.4", self.ind)
        self.assertIn("34 mg/kg dry weight", self.ind)
        self.assertIn("Indicator 4.7.4", self.src)

    def test_section_23_grazing_rows_are_cross_references(self):
        s23 = self.ind.split("## 23. Livestock farm")[1].split("## 24. Peatlands")[0]
        self.assertEqual(s23.count("Method and anchors as in §22")
                         + s23.count("Method and starting anchor as in §22"), 3)
        self.assertNotIn("Wyoming Extension B-1320", s23)
        self.assertEqual(self.ind.count("Wyoming Extension B-1320"), 1)

    def test_morris_cited_from_primary_abstract(self):
        self.assertIn("Morris et al. 2016, Earth's Future — the abstract gives", self.ind)

    def test_har_us_nuur_endemics_as_range(self):
        self.assertNotIn("five endemic fish species (Ramsar", self.ind)
        self.assertIn('carry "three to five"', self.ind)

    def test_source_list_has_no_draft_wording(self):
        self.assertNotIn("this draft", self.src)
        self.assertNotIn("read before using", self.src)


class TestIndependentVerificationOct28(unittest.TestCase):
    """T99, 2026-10-28: Muse's independent verification of the T97/T98
    build against primary sources. Correction to the record: the T96 Tier 1
    'fix' swapped the cropland and grassland factors on a garbled FAOSTAT
    PDF extraction; the pre-T96 values were correct, T97 restored them, and
    T99 verified the assignment against ESSD Table 5 (Conchedda &
    Tubiello 2020, reproducing the 2013 IPCC Wetlands Supplement Table
    2.1). Verified and closed in T99, as corrected by T100/T101: DCS
    revised paddy yields; the Laksvel mortality band (four colour
    levels, Rapport fra Havforskningen 2025-40, §4.3); the Norwegian
    density paragraph (§25 «Tetthet», FOR-2008-06-17-822 — T99's §19
    cited the 1998 regulation's translation); USDA 2025/26 Sri Lanka
    record 3.7 Mt (ERS RCS-26H) with area and yield as trade-press
    values; the Danube Delta 2017 census count (9,581, institute figure
    via Agerpres) leading, 5,500 kept as an older summary. Still
    unverified: Todgerel 2020 (secondary citation only), the USDA area
    and yield, the Danube census report itself."""

    def setUp(self):
        self.ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        self.wex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))
        self.chlog = rtext(os.path.join(ROOT, "CHANGELOG.md"))

    def test_tier1_factors_correct_per_essd(self):
        flat = " ".join(self.ind.split())
        self.assertIn("cropland: 7.9 t CO₂-C/ha/yr boreal and temperate, 14.0 tropical", flat)
        self.assertIn("grassland: 5.7 boreal", flat)
        self.assertNotIn("cropland: 5.7", flat)
        self.assertNotIn("grassland: 7.9", flat)

    def test_laksvel_cited_from_primary_protocol(self):
        row = [ln for ln in self.ind.splitlines() if "Daily and cumulative mortality rate" in ln][0]
        self.assertIn("Rapport fra Havforskningen 2025-40", row)
        self.assertIn("level 3 (red level)", row)
        self.assertNotIn("Fish Health Report", row)
        self.assertIn("Rapport fra Havforskningen 2025-40", self.src)
        self.assertNotIn("via Norwegian Fish Health Report 2025", self.src)

    def test_norway_density_paragraph_confirmed(self):
        # T100: repointed. The full Norwegian text on FAOLEX (nor82122,
        # FOR-2008-06-17-822) gives the rule as § 25 «Tetthet», not §19.
        flat = " ".join(self.ind.split())
        self.assertIn("FOR-2008-06-17-822", flat)
        self.assertIn("§ 25 «Tetthet»", flat)
        self.assertNotIn('§19: "Fish density', flat)
        self.assertNotIn("confirm it on Lovdata", flat)

    def test_usda_verified_against_ers(self):
        # T100: repointed. ERS RCS-26H confirms production only; area and
        # yield remain trade-press values citing USDA.
        self.assertIn("ERS Rice Outlook RCS-26H", self.ind)
        self.assertIn("not yet read from a USDA document", self.ind)
        self.assertNotIn("which names the USDA FAS World Agricultural Production circular", self.ind)
        self.assertNotIn("to be checked against the USDA", self.ind)
        self.assertNotIn("not yet checked against the USDA release", self.src)

    def test_danube_5500_source_recorded(self):
        # T100: repointed. The 2017 census count leads; 5,500 is kept as an
        # older summary figure.
        flat = " ".join(self.ind.split())
        self.assertIn("9,581 species recorded in the 2017 biodiversity census", flat)
        self.assertIn("older summaries give over 5,500, Claudino-Sales 2018", flat)
        self.assertIn("Claudino-Sales 2018", self.src)

    def test_todgerel_still_flagged_secondary(self):
        self.assertIn("primary Todgerel 2020 document was not consulted", self.ind)
        self.assertIn("[provisional], a secondary citation", self.wex)

    def test_changelog_records_t99_verification(self):
        self.assertIn("Independent verification (T99, 2026-10-28)", self.chlog)
        self.assertIn("T96 Tier 1", self.chlog)


class TestT99FollowUpOct28(unittest.TestCase):
    """T100, 2026-10-28: Claude's review of the T99 build (9.3/10), fixes
    applied by Claude at the author's request. The Norwegian density rule
    is § 25 «Tetthet» in the regulation's full text on FAOLEX (T99 had
    asserted §19); the ERS Rice Outlook confirms the Sri Lanka production
    only; the Danube Delta leads with the 2017 census count; the Laksvel
    row gives the four colour levels from §4.3 (the protocol's 'very high'
    descriptor for the >2% case is not repeated in the row);
    the GEPIS example's 'roughly double the national average' no longer
    holds with the DCS yields; the CHANGELOG corrects the T99 record on
    Tier 1 and on which figures remain unverified."""

    def setUp(self):
        self.ind = rtext(os.path.join(ROOT, "references", "indicators.md"))
        self.src = rtext(os.path.join(ROOT, "references", "sources-new-sections.md"))
        self.wex = rtext(os.path.join(ROOT, "references", "worked-examples-new-sections.md"))
        self.chlog = rtext(os.path.join(ROOT, "CHANGELOG.md"))

    def test_norway_paragraph_25_everywhere(self):
        for text in (self.ind, self.src):
            flat = " ".join(text.split())
            self.assertIn("§ 25 «Tetthet»", flat)
        self.assertNotIn("the FAOLEX numbering is the one to quote", " ".join(self.src.split()))

    def test_laksvel_four_levels(self):
        row = [ln for ln in self.ind.splitlines() if "Daily and cumulative mortality rate" in ln][0]
        for s in ("level 0 (green) below 0.3%", "level 1 (yellow) 0.3–0.7%",
                  "level 2 (orange) 0.7–2%", "level 3 (red level) above 2%"):
            self.assertIn(s, row)
        self.assertNotIn("very high", row)
        self.assertIn("monthly mortality above 2% is level 3 (red level); level 0 (green)",
                      " ".join(self.src.split()))
        self.assertNotIn("described as 'very high'", self.src)

    def test_usda_area_and_yield_status(self):
        flat = " ".join(self.src.split())
        self.assertIn("Its pointer to the FAS World Agricultural Production circular sits in the Bangladesh paragraph", flat)
        self.assertIn("area and yield not yet read from a USDA document", " ".join(self.wex.split()))

    def test_gepis_ratio_matches_dcs_yields(self):
        flat = " ".join(self.wex.split())
        self.assertNotIn("roughly double the national average", flat)
        self.assertIn("about one and a half times the national average (3.7–4.1 t/ha", flat)

    def test_changelog_corrects_t99_record(self):
        flat = " ".join(self.chlog.split())
        self.assertIn("T99 follow-up (T100, 2026-10-28)", flat)
        self.assertIn("no cool/warm temperate split", flat)

    def test_readme_test_counts_agree(self):
        en = rtext(os.path.join(ROOT, "README.md"))
        ru = rtext(os.path.join(ROOT, "README.ru.md"))
        n_en = re.search(r"\*\*Automated:\*\* (\d+) unit", en).group(1)
        n_ru = re.search(r"\*\*Автоматически:\*\* (\d+) юнит", ru).group(1)
        self.assertEqual(n_en, n_ru, "README.md and README.ru.md give different test counts")


class TestT100FollowUpOct28(unittest.TestCase):
    """T101, 2026-10-28: Muse's verification of the T100 build against
    primary sources. Pins the corrections to the T100 record: DCS yields
    restored as verified (Muse T99, primary DCS table); the Laksvel
    'very high' descriptor is the protocol's own wording (§4.3) and the
    T100 rationale is corrected; the T100 test class holds six tests."""

    def setUp(self):
        self.chlog = rtext(os.path.join(ROOT, "CHANGELOG.md"))
        self.test_src = rtext(os.path.join(ROOT, "tests", "test_scripts.py"))

    def test_changelog_restores_dcs_as_verified(self):
        flat = " ".join(self.chlog.split())
        self.assertIn("DCS yields restored as verified", flat)
        self.assertIn("2022/23 Maha 3,731", flat)

    def test_changelog_corrects_laksvel_rationale(self):
        flat = " ".join(self.chlog.split())
        self.assertIn("This must be described as very high", flat)

    def test_t100_class_holds_six_tests(self):
        block = self.test_src.split("class TestT99FollowUpOct28")[1].split("class TestT100FollowUpOct28")[0]
        self.assertEqual(len(re.findall(r"def test_", block)), 6)


class TestReleaseV28(unittest.TestCase):
    """T102 (2026-10-28): release edits for v2.8. One release date, one DOI
    across README (EN/RU) and CITATION.cff, the DOI is no longer the v2.3
    record, no candidate wording left in references/thresholds.md, and the
    README states the skill's scope (no process-model core until v2.9)."""

    def setUp(self):
        self.readme = rtext(os.path.join(ROOT, "README.md"))
        self.readme_ru = rtext(os.path.join(ROOT, "README.ru.md"))
        self.cff = rtext(os.path.join(ROOT, "CITATION.cff"))

    def test_release_date_consistent(self):
        self.assertIn("Current version: **2.8** (2026-10-28)", self.readme)
        self.assertIn("Текущая версия: **2.8** (2026-10-28)", self.readme_ru)
        self.assertIn('date-released: "2026-10-28"', self.cff)
        chlog = rtext(os.path.join(ROOT, "CHANGELOG.md"))
        self.assertIn("## v2.8 — 2026-10-28", chlog)

    def test_one_doi_not_v23_record(self):
        doi = re.search(r"^doi: (\S+)", self.cff, re.M).group(1)
        self.assertNotEqual(doi, "10.5281/zenodo.23657185")
        for text in (self.readme, self.readme_ru):
            found = set(re.findall(r"10\.5281/zenodo\.\d+", text))
            self.assertEqual(found, {doi})

    def test_thresholds_no_candidate_wording(self):
        th = rtext(os.path.join(ROOT, "references", "thresholds.md"))
        self.assertIn("Status: part of release v2.8", th)
        for stale in ("v2.8 candidate", "Not applied to the live skill",
                      "кандидате v2.8", "предлагается BY-ND"):
            self.assertNotIn(stale, th)

    def test_readme_states_scope(self):
        flat = " ".join(self.readme.split())
        self.assertIn("does not yet ship a process model with data assimilation", flat)
        flat_ru = " ".join(self.readme_ru.split())
        self.assertIn("Процессной модели с усвоением данных в нём пока нет", flat_ru)
        for text in (self.readme, self.readme_ru):
            self.assertNotIn("ADIS", text)


class TestDualLicenceV28(unittest.TestCase):
    """T103 (2026-10-28): dual licence. Text and method under CC BY 4.0
    (LICENSE unchanged), code under Apache-2.0 (LICENSE-CODE, canonical
    text); README (EN/RU), SKILL frontmatter and CITATION state the split."""

    def test_licence_files(self):
        code = rtext(os.path.join(ROOT, "LICENSE-CODE"))
        self.assertIn("Apache License", code)
        self.assertIn("Version 2.0, January 2004", code)
        self.assertIn("END OF TERMS AND CONDITIONS", code)
        text = rtext(os.path.join(ROOT, "LICENSE"))
        self.assertIn("Attribution 4.0 International", text)

    def test_readme_licence_sections(self):
        for fname in ("README.md", "README.ru.md"):
            text = rtext(os.path.join(ROOT, fname))
            self.assertIn("[`LICENSE-CODE`](LICENSE-CODE)", text)
            self.assertIn("[`LICENSE`](LICENSE)", text)
            self.assertIn("Apache License 2.0", text)
            self.assertIn("CC BY 4.0", text)

    def test_skill_frontmatter_names_both(self):
        for fname in ("SKILL.md", "SKILL.ru.md"):
            head = rtext(os.path.join(ROOT, fname)).split("\n---", 1)[0]
            self.assertIn("CC-BY-4.0", head)
            self.assertIn("Apache-2.0", head)

    def test_citation_states_code_licence(self):
        cff = rtext(os.path.join(ROOT, "CITATION.cff"))
        self.assertIn("license: CC-BY-4.0", cff)
        flat = " ".join(cff.split())
        self.assertIn("under Apache-2.0 (LICENSE-CODE)", flat)


class TestPackage(unittest.TestCase):
    def test_package_lint_passes(self):
        code, out, _ = run(os.path.join("..", "tests", "check_package.py"))
        self.assertEqual(code, 0, json.dumps(out["errors"] if out else None, indent=2))


if __name__ == "__main__":
    unittest.main()
