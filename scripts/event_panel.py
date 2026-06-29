from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EVENTSTUDY = ROOT / "eventstudy"
EVENT_INPUT = DATA / "event_catalog_input.csv"


@dataclass(frozen=True)
class PanelEvent:
    company: str
    ticker: str
    event: str
    day0: str
    event_type: str
    source_type: str
    data_file: str | None
    peer_file: str | None = None
    reason_if_excluded: str = ""


def _blank_to_none(value: object) -> str | None:
    text = "" if value is None else str(value).strip()
    return text or None


def load_panel_events(path: Path = EVENT_INPUT) -> list[PanelEvent]:
    df = pd.read_csv(path, keep_default_na=False)
    required = {
        "company",
        "ticker",
        "event",
        "day0",
        "event_type",
        "source_type",
        "data_file",
        "peer_file",
        "reason_if_excluded",
    }
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"{path} missing required columns: {', '.join(missing)}")

    events = []
    for row in df.to_dict("records"):
        events.append(
            PanelEvent(
                company=str(row["company"]).strip(),
                ticker=str(row["ticker"]).strip(),
                event=str(row["event"]).strip(),
                day0=str(row["day0"]).strip(),
                event_type=str(row["event_type"]).strip(),
                source_type=str(row["source_type"]).strip(),
                data_file=_blank_to_none(row["data_file"]),
                peer_file=_blank_to_none(row["peer_file"]),
                reason_if_excluded=str(row["reason_if_excluded"]).strip(),
            )
        )
    return events


def _price_frame(filename: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / filename)
    df["date"] = pd.to_datetime(df["trade_date"].astype(str))
    df = df.sort_values("date").reset_index(drop=True)
    df["daily_return"] = df["close"].pct_change()
    return df


def compute_event_window_cars(event: PanelEvent) -> dict:
    if not event.data_file or event.reason_if_excluded:
        return {
            "included": False,
            "exclusion_reason": event.reason_if_excluded or "missing local price file",
        }
    prices = _price_frame(event.data_file)
    day0 = pd.Timestamp(event.day0)
    matches = prices.index[prices["date"] == day0]
    if len(matches) == 0:
        return {"included": False, "exclusion_reason": "event date not in local price series"}
    loc = int(matches[0])
    if loc < 20:
        return {"included": False, "exclusion_reason": "insufficient pre-event estimation window"}
    expected = prices.loc[loc - 20 : loc - 6, "daily_return"].mean()
    if pd.isna(expected):
        return {"included": False, "exclusion_reason": "expected return unavailable"}

    def sum_mean_adjusted(start_rel: int, end_rel: int) -> tuple[float, int, bool]:
        values = []
        for rel in range(start_rel, end_rel + 1):
            pos = loc + rel
            if 0 <= pos < len(prices):
                values.append(float((prices.loc[pos, "daily_return"] - expected) * 100))
        return round(float(np.sum(values)), 2), len(values), len(values) == end_rel - start_rel + 1

    leakage, leakage_days, leakage_full = sum_mean_adjusted(-5, -1)
    reaction, reaction_days, reaction_full = sum_mean_adjusted(0, 1)
    drift, drift_days, drift_full = sum_mean_adjusted(2, 10)
    raw_day0 = float(prices.loc[loc, "daily_return"] * 100)

    result = {
        "included": True,
        "exclusion_reason": "",
        "leakage_mean": leakage,
        "react_mean": reaction,
        "drift_mean": drift,
        "leakage_days": leakage_days,
        "reaction_days": reaction_days,
        "drift_days": drift_days,
        "leakage_full": leakage_full,
        "reaction_full": reaction_full,
        "drift_full": drift_full,
        "raw_day0_return": round(raw_day0, 2),
    }
    if event.peer_file:
        peer = _price_frame(event.peer_file)[["date", "daily_return"]].rename(
            columns={"daily_return": "peer_return"}
        )
        merged = prices[["date", "daily_return"]].merge(peer, on="date", how="left")
        peer_matches = merged.index[merged["date"] == day0]
        if len(peer_matches) == 1:
            peer_loc = int(peer_matches[0])

            def sum_peer_adjusted(start_rel: int, end_rel: int) -> float | None:
                values = []
                for rel in range(start_rel, end_rel + 1):
                    pos = peer_loc + rel
                    if 0 <= pos < len(merged) and not pd.isna(merged.loc[pos, "peer_return"]):
                        values.append(float((merged.loc[pos, "daily_return"] - merged.loc[pos, "peer_return"]) * 100))
                return round(float(np.sum(values)), 2) if values else None

            result["react_peer"] = sum_peer_adjusted(0, 1)
            result["drift_peer"] = sum_peer_adjusted(2, 10)
    return result


def event_panel_rows(events: list[PanelEvent]) -> pd.DataFrame:
    rows = []
    for event in events:
        result = compute_event_window_cars(event)
        rows.append(
            {
                "company": event.company,
                "ticker": event.ticker,
                "event": event.event,
                "day0": event.day0,
                "event_type": event.event_type,
                "source_type": event.source_type,
                "included": result.get("included", False),
                "exclusion_reason": result.get("exclusion_reason", ""),
                "leakage_mean": result.get("leakage_mean"),
                "react_mean": result.get("react_mean"),
                "drift_mean": result.get("drift_mean"),
                "react_peer": result.get("react_peer"),
                "drift_peer": result.get("drift_peer"),
                "raw_day0_return": result.get("raw_day0_return"),
                "leakage_days": result.get("leakage_days"),
                "reaction_days": result.get("reaction_days"),
                "drift_days": result.get("drift_days"),
                "drift_full": result.get("drift_full"),
            }
        )
    return pd.DataFrame(rows)


def summarize_event_panel(panel: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    if panel.empty:
        return pd.DataFrame(summary_rows)
    for event_type, group in panel.groupby("event_type", sort=True):
        react = group["react_mean"].astype(float)
        drift = group["drift_mean"].astype(float)
        summary_rows.append(
            {
                "event_type": event_type,
                "n_events": int(len(group)),
                "mean_reaction_car_pct": round(float(react.mean()), 2),
                "median_reaction_car_pct": round(float(react.median()), 2),
                "positive_reaction_events": int((react > 0).sum()),
                "mean_drift_car_pct": round(float(drift.mean()), 2),
                "median_drift_car_pct": round(float(drift.median()), 2),
                "positive_drift_events": int((drift > 0).sum()),
                "full_drift_windows": int(group["drift_full"].map(bool).sum()),
            }
        )
    react = panel["react_mean"].astype(float)
    drift = panel["drift_mean"].astype(float)
    summary_rows.append(
        {
            "event_type": "ALL_INCLUDED",
            "n_events": int(len(panel)),
            "mean_reaction_car_pct": round(float(react.mean()), 2),
            "median_reaction_car_pct": round(float(react.median()), 2),
            "positive_reaction_events": int((react > 0).sum()),
            "mean_drift_car_pct": round(float(drift.mean()), 2),
            "median_drift_car_pct": round(float(drift.median()), 2),
            "positive_drift_events": int((drift > 0).sum()),
            "full_drift_windows": int(panel["drift_full"].map(bool).sum()),
        }
    )
    return pd.DataFrame(summary_rows)


def write_event_panel_outputs(write_csv, input_path: Path = EVENT_INPUT) -> None:
    catalog = event_panel_rows(load_panel_events(input_path))
    write_csv(catalog, EVENTSTUDY / "event_catalog.csv")
    panel = catalog[catalog["included"] == True].copy()
    write_csv(panel, EVENTSTUDY / "event_panel.csv")
    write_csv(summarize_event_panel(panel), EVENTSTUDY / "event_panel_summary.csv")
