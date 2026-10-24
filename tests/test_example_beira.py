"""Tests for examples/beira/beira_twin.py — published-data worked example."""
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = os.path.join(os.path.dirname(HERE), "examples", "beira")
sys.path.insert(0, EXAMPLE)

import beira_twin  # noqa: E402


class BeiraExampleTests(unittest.TestCase):
    def test_carlson_index_round_trip(self):
        self.assertAlmostEqual(beira_twin.tsi_tp(beira_twin.tp_from_tsi(80.0)), 80.0, places=9)
        self.assertEqual(round(beira_twin.tp_from_tsi(80.0)), 192)

    def test_state_classes_match_published_thresholds(self):
        rows = {(r["indicator"], r["season"]): r for r in beira_twin.step1_state()}
        self.assertEqual(rows[("WPI", "dry")]["class"], "highly polluted")
        self.assertTrue(rows[("WPI", "wet")]["whole_band_above_top_threshold"])
        self.assertEqual(rows[("TSI(TP)", "wet")]["class"], "hypertrophic")
        self.assertEqual(rows[("HPI", "dry")]["class"], "below all thresholds")
        self.assertEqual(rows[("HPI", "wet")]["class"], "unsuitable for drinking")

    def test_wetland_alone_leaves_lake_hypertrophic(self):
        cases = beira_twin.step3_wetland_alone()["cases"]
        best, worst = cases
        self.assertEqual(best["class_after"], "hypertrophic")
        self.assertAlmostEqual(best["TSI_after_46pct_cut"], 81.7, places=1)
        self.assertAlmostEqual(best["reduction_needed_to_leave_hypertrophic_pct"], 51.9, places=1)
        self.assertAlmostEqual(worst["reduction_needed_to_leave_hypertrophic_pct"], 96.7, places=1)

    def test_source_check_flags_mean_close_to_maximum(self):
        s = beira_twin.step2_source_check()
        self.assertLess(abs(s["TSI_of_reported_max_TP"] - s["wet_mean_TSI_TP"]), 0.5)

    def test_value_of_information_is_never_negative(self):
        table = beira_twin.step4_value_of_information()
        self.assertTrue(all(v["VOI_disposal_units"] >= 0 for v in table))
        top = max(table, key=lambda v: v["VOI_disposal_units"])
        self.assertEqual((top["p_compliant"], top["field_route_cost"], top["VOI_disposal_units"]), (0.8, 0.5, 0.4))

    def test_registered_forecast_chain_verifies(self):
        reg = os.path.join(EXAMPLE, "registry.jsonl")
        script = os.path.join(os.path.dirname(HERE), "scripts", "registry.py")
        out = subprocess.run([sys.executable, script, "verify", "--registry", reg],
                             capture_output=True, text=True, check=False)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertTrue(json.loads(out.stdout)["ok"])

    def test_cli_json(self):
        out = subprocess.run([sys.executable, os.path.join(EXAMPLE, "beira_twin.py"), "--json"],
                             capture_output=True, text=True, check=True)
        data = json.loads(out.stdout)
        self.assertEqual(len(data["cross_check"]), 3)
        self.assertTrue(all(g.startswith("[НЕТ ДАННЫХ]") for g in data["gaps"]))


if __name__ == "__main__":
    unittest.main()
