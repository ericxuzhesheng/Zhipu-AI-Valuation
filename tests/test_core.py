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
        self.assertEqual(len(events), 14)
        panel = event_panel.event_panel_rows(events)
        self.assertEqual(len(panel), 14)
        self.assertEqual(int(panel["included"].sum()), 9)

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
        self.assertEqual(int(total["n_events"]), 9)
        self.assertAlmostEqual(float(total["mean_reaction_car_pct"]), 8.92)
        self.assertAlmostEqual(float(total["mean_drift_car_pct"]), 7.14)


class ValuationTests(unittest.TestCase):
    def test_base_case_per_share_value_is_stable(self) -> None:
        result = rebuild_outputs.project_scenario(rebuild_outputs.SCENARIOS[1])
        self.assertAlmostEqual(result["per_share_hkd"], 28.1, places=1)


if __name__ == "__main__":
    unittest.main()
