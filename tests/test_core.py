from __future__ import annotations

import unittest
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import event_panel
import rebuild_outputs


class EventPanelTests(unittest.TestCase):
    def test_event_catalog_input_drives_panel(self) -> None:
        events = event_panel.load_panel_events()
        self.assertEqual(len(events), 62)
        panel = event_panel.event_panel_rows(events)
        self.assertEqual(len(panel), 62)
        self.assertEqual(int(panel["included"].sum()), 29)
        zcode = panel.loc[panel["event"] == "ZCode IDE"].iloc[0]
        self.assertFalse(bool(zcode["included"]))
        self.assertIn("outside the core foundation-model capability event set", zcode["exclusion_reason"])
        tech100 = panel.loc[panel["event"] == "HKEX Tech 100 insight"].iloc[0]
        self.assertTrue(bool(tech100["included"]))
        glm5v = panel.loc[panel["event"] == "GLM-5V-Turbo"].iloc[0]
        self.assertFalse(bool(glm5v["included"]))
        self.assertIn("overlaps GLM-5.1", glm5v["exclusion_reason"])
        glm53 = panel.loc[panel["event"] == "GLM-5.3"].iloc[0]
        self.assertTrue(bool(glm53["included"]))
        glm53flash = panel.loc[panel["event"] == "GLM-5.3-Flash"].iloc[0]
        self.assertFalse(bool(glm53flash["included"]))
        self.assertIn("insufficient post-event window", glm53flash["exclusion_reason"])
        interim = panel.loc[
            (panel["company"] == "Zhipu") & (panel["event"] == "2026 H1 results announcement")
        ].iloc[0]
        self.assertFalse(bool(interim["included"]))
        self.assertIn("same-day return predates disclosure", interim["exclusion_reason"])
        minimax_m25 = panel.loc[(panel["company"] == "MiniMax") & (panel["event"] == "M2.5")].iloc[0]
        self.assertTrue(bool(minimax_m25["included"]))
        self.assertAlmostEqual(float(minimax_m25["react_mean"]), 24.20)
        self.assertAlmostEqual(float(minimax_m25["drift_mean"]), -2.09)
        minimax_h3 = panel.loc[(panel["company"] == "MiniMax") & (panel["event"] == "H3")].iloc[0]
        self.assertFalse(bool(minimax_h3["included"]))
        self.assertIn("outside the text-agent capability peer set", minimax_h3["exclusion_reason"])
        minimax_interim = panel.loc[
            (panel["company"] == "MiniMax") & (panel["event"] == "2026 H1 results announcement")
        ].iloc[0]
        self.assertFalse(bool(minimax_interim["included"]))
        self.assertIn("next trading day after disclosure", minimax_interim["exclusion_reason"])
        openai_proxy = panel.loc[panel["event"] == "GPT-5.6 proxy"].iloc[0]
        self.assertFalse(bool(openai_proxy["included"]))
        self.assertIn("not the model issuer", openai_proxy["exclusion_reason"])
        msci = panel.loc[panel["event"] == "MSCI Emerging Markets inclusion rebalance"].iloc[0]
        self.assertFalse(bool(msci["included"]))
        self.assertIn("closing-auction flows", msci["exclusion_reason"])

        generated_catalog = pd.read_csv(ROOT / "eventstudy" / "event_catalog.csv")
        self.assertEqual(len(generated_catalog), len(events))

    def test_first_capability_event_car_is_stable(self) -> None:
        first_event = event_panel.load_panel_events()[0]
        result = event_panel.compute_event_window_cars(first_event)
        self.assertTrue(result["included"])
        self.assertAlmostEqual(result["react_mean"], 22.48)
        self.assertAlmostEqual(result["drift_mean"], 24.72)
        self.assertAlmostEqual(result["react_peer"], 17.19)

    def test_panel_summary_has_expected_total_row(self) -> None:
        panel = event_panel.event_panel_rows(event_panel.load_panel_events())
        included = panel[panel["included"] == True]
        summary = event_panel.summarize_event_panel(included)
        total = summary.loc[summary["event_type"] == "ALL_INCLUDED"].iloc[0]
        self.assertEqual(int(total["n_events"]), 29)
        self.assertAlmostEqual(float(total["mean_reaction_car_pct"]), 3.87)
        self.assertAlmostEqual(float(total["mean_drift_car_pct"]), -2.28)
        large_tech = summary.loc[summary["event_type"] == "large_tech_peer"].iloc[0]
        self.assertEqual(int(large_tech["n_events"]), 16)
        self.assertAlmostEqual(float(large_tech["mean_reaction_car_pct"]), 2.32)
        self.assertAlmostEqual(float(large_tech["mean_drift_car_pct"]), -3.04)
        self.assertEqual(int(large_tech["full_drift_windows"]), 16)


class ValuationTests(unittest.TestCase):
    def test_base_case_per_share_value_is_stable(self) -> None:
        result = rebuild_outputs.project_scenario(rebuild_outputs.SCENARIOS[1])
        self.assertAlmostEqual(result["per_share_hkd"], 72.8, places=1)

    def test_valuation_comps_are_built_from_input(self) -> None:
        comps = rebuild_outputs.build_valuation_comps()
        input_path = ROOT / "data" / "valuation_comps_input.csv"
        self.assertTrue(input_path.exists())

        inputs = pd.read_csv(input_path, keep_default_na=False)
        self.assertNotIn("multiple_x", inputs.columns)
        self.assertGreaterEqual(len(comps), 10)

        expected = comps["equity_value_bn"] / comps["revenue_bn"]
        self.assertTrue(((comps["multiple_x"] - expected).abs() <= 0.051).all())
        included = comps.loc[comps["include_in_private_range"] == 1]
        self.assertEqual(set(included["company"]), {"OpenAI", "Anthropic", "Mistral"})
        self.assertAlmostEqual(float(included["multiple_x"].min()), 20.5, delta=0.15)
        self.assertAlmostEqual(float(included["multiple_x"].median()), 34.1, delta=0.15)
        self.assertAlmostEqual(float(included["multiple_x"].max()), 39.0, delta=0.15)

        minimax = comps.loc[comps["company"] == "MiniMax", "multiple_x"].iloc[0]
        self.assertAlmostEqual(float(minimax), 94.6, delta=0.15)

        zhipu = comps.loc[comps["company"] == "Zhipu", "multiple_x"].iloc[0]
        self.assertAlmostEqual(float(zhipu), 340.5, delta=0.15)
        self.assertEqual(
            comps.loc[comps["company"] == "Zhipu", "revenue_basis"].iloc[0],
            "LTM through 2026H1",
        )


if __name__ == "__main__":
    unittest.main()
