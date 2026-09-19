"""Incrementally update all market-data CSV files to a fixed cutoff.

Primary source: Tushare ``hk_daily`` / ``us_daily``.
Public fallback: Tencent Finance (then East Money) daily K-lines for Hong
Kong stocks and the official Nasdaq historical endpoint for US stocks.
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

import pandas as pd
import requests
import tushare as ts


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
EASTMONEY_URL = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
TENCENT_URL = "https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get"
NASDAQ_URL = "https://api.nasdaq.com/api/quote/{ticker}/historical"

# csv filename, Tushare code, market, public-source identifier
STOCKS = [
    ("Zhipu_KnowledgeAtlas_daily.csv", "02513.HK", "hk", "hk02513"),
    ("MiniMax_daily.csv", "00100.HK", "hk", "hk00100"),
    ("WengeAI_daily.csv", "01956.HK", "hk", "hk01956"),
    ("Alibaba_daily.csv", "9988.HK", "hk", "hk09988"),
    ("Baidu_daily.csv", "9888.HK", "hk", "hk09888"),
    ("Tencent_daily.csv", "0700.HK", "hk", "hk00700"),
    ("Meituan_daily.csv", "3690.HK", "hk", "hk03690"),
    ("Google_daily.csv", "GOOGL", "us", "GOOGL"),
    ("Meta_daily.csv", "META", "us", "META"),
    ("Microsoft_daily.csv", "MSFT", "us", "MSFT"),
    ("Tesla_daily.csv", "TSLA", "us", "TSLA"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--end-date",
        default=pd.Timestamp.now().strftime("%Y%m%d"),
        help="Inclusive cutoff in YYYYMMDD format (default: today).",
    )
    parser.add_argument(
        "--source",
        choices=("auto", "tushare", "public"),
        default="auto",
        help="Data source policy (default: auto, with public fallback).",
    )
    args = parser.parse_args()
    try:
        args.end_date = pd.Timestamp(args.end_date).strftime("%Y%m%d")
    except ValueError as exc:
        parser.error(f"invalid --end-date {args.end_date!r}: {exc}")
    return args


def request_json(url: str, *, params: dict, headers: dict | None = None) -> dict:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed after 3 attempts: {last_error}")


def rows_with_returns(
    existing: pd.DataFrame,
    records: list[dict],
    stored_code: str,
) -> pd.DataFrame:
    previous_close = float(existing.sort_values("trade_date").iloc[-1]["close"])
    rows: list[dict] = []
    for record in sorted(records, key=lambda item: item["trade_date"]):
        close = float(record["close"])
        change = close - previous_close
        pct_chg = change / previous_close * 100 if previous_close else pd.NA
        rows.append(
            {
                "ts_code": stored_code,
                "trade_date": record["trade_date"],
                "open": float(record["open"]),
                "high": float(record["high"]),
                "low": float(record["low"]),
                "close": close,
                "pre_close": previous_close,
                "change": change,
                "pct_chg": pct_chg,
                "vol": float(record["vol"]),
                "amount": float(record["amount"]),
            }
        )
        previous_close = close
    return pd.DataFrame(rows, columns=existing.columns)


def fetch_eastmoney(
    existing: pd.DataFrame,
    public_id: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    payload = request_json(
        EASTMONEY_URL,
        params={
            "secid": f"116.{public_id[2:]}",
            "klt": "101",
            "fqt": "0",
            "beg": start_date,
            "end": end_date,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        },
    )
    data = payload.get("data") or {}
    records = []
    for line in data.get("klines") or []:
        fields = line.split(",")
        records.append(
            {
                "trade_date": fields[0].replace("-", ""),
                "open": fields[1],
                "close": fields[2],
                "high": fields[3],
                "low": fields[4],
                "vol": fields[5],
                "amount": fields[6],
            }
        )
    stored_code = str(existing.iloc[-1]["ts_code"])
    return rows_with_returns(existing, records, stored_code)


def fetch_tencent(
    existing: pd.DataFrame,
    public_id: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    start = pd.Timestamp(start_date).strftime("%Y-%m-%d")
    end = pd.Timestamp(end_date).strftime("%Y-%m-%d")
    payload = request_json(
        TENCENT_URL,
        params={"param": f"{public_id},day,{start},{end},640,qfq"},
        headers={"User-Agent": "Mozilla/5.0"},
    )
    security = ((payload.get("data") or {}).get(public_id) or {})
    rows = security.get("day") or security.get("qfqday") or []
    records = []
    for fields in rows:
        trade_date = str(fields[0]).replace("-", "")
        if not start_date <= trade_date <= end_date:
            continue
        close = float(fields[2])
        volume = float(fields[5])
        try:
            amount = float(fields[8]) * 10_000
        except (IndexError, TypeError, ValueError):
            amount = close * volume
        records.append(
            {
                "trade_date": trade_date,
                "open": fields[1],
                "close": close,
                "high": fields[3],
                "low": fields[4],
                "vol": volume,
                "amount": amount,
            }
        )
    stored_code = str(existing.iloc[-1]["ts_code"])
    return rows_with_returns(existing, records, stored_code)


def parse_us_number(value: str) -> float:
    return float(str(value).replace("$", "").replace(",", ""))


def fetch_nasdaq(
    existing: pd.DataFrame,
    ticker: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    start = pd.Timestamp(start_date).strftime("%Y-%m-%d")
    end = pd.Timestamp(end_date).strftime("%Y-%m-%d")
    payload = request_json(
        NASDAQ_URL.format(ticker=ticker),
        params={
            "assetclass": "stocks",
            "fromdate": start,
            "todate": end,
            "limit": "5000",
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/",
        },
    )
    rows = (((payload.get("data") or {}).get("tradesTable") or {}).get("rows") or [])
    records = []
    for row in rows:
        close = parse_us_number(row["close"])
        volume = parse_us_number(row["volume"])
        records.append(
            {
                "trade_date": pd.Timestamp(row["date"]).strftime("%Y%m%d"),
                "open": parse_us_number(row["open"]),
                "high": parse_us_number(row["high"]),
                "low": parse_us_number(row["low"]),
                "close": close,
                "vol": volume,
                "amount": close * volume,
            }
        )
    stored_code = str(existing.iloc[-1]["ts_code"])
    return rows_with_returns(existing, records, stored_code)


def fetch_tushare(
    pro,
    existing: pd.DataFrame,
    ts_code: str,
    market: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    if pro is None:
        raise RuntimeError("TUSHARE_TOKEN is not set")
    if market == "hk":
        new_data = pro.hk_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    else:
        new_data = pro.us_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    if new_data is None or new_data.empty:
        return pd.DataFrame(columns=existing.columns)
    new_data = new_data.sort_values("trade_date").reset_index(drop=True)
    new_data["trade_date"] = new_data["trade_date"].astype(str)
    for column in set(existing.columns) - set(new_data.columns):
        new_data[column] = pd.NA
    return new_data[existing.columns]


def write_combined(path: Path, existing: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat([existing, new_data], ignore_index=True)
    combined["trade_date"] = combined["trade_date"].astype(str)
    combined = combined.drop_duplicates(subset=["trade_date"], keep="last")
    combined = combined.sort_values("trade_date").reset_index(drop=True)
    temporary = path.with_suffix(".tmp.csv")
    combined.to_csv(temporary, index=False)
    os.replace(temporary, path)
    return combined


def main() -> int:
    args = parse_args()
    token = (os.environ.get("TUSHARE_TOKEN") or os.environ.get("tushare_token") or "").strip()
    pro = ts.pro_api(token) if token else None
    errors: list[str] = []

    for csv_name, ts_code, market, public_id in STOCKS:
        csv_path = DATA_DIR / csv_name
        existing = pd.read_csv(csv_path)
        existing["trade_date"] = existing["trade_date"].astype(str)
        last_date = existing["trade_date"].max()
        start_date = (pd.Timestamp(last_date) + pd.Timedelta(days=1)).strftime("%Y%m%d")
        if start_date > args.end_date:
            print(f"[SKIP] {csv_name}: already up to {last_date}")
            continue

        print(f"[FETCH] {csv_name}: {start_date} -> {args.end_date}")
        new_data: pd.DataFrame | None = None
        source_used = ""
        if args.source in {"auto", "tushare"}:
            try:
                new_data = fetch_tushare(pro, existing, ts_code, market, start_date, args.end_date)
                source_used = "Tushare"
            except Exception as exc:
                if args.source == "tushare":
                    errors.append(f"{csv_name}: Tushare: {exc}")
                    print(f"  ERROR Tushare: {exc}")
                    continue
                print(f"  WARN Tushare unavailable; using public fallback: {exc}")

        if new_data is None:
            try:
                if market == "hk":
                    try:
                        new_data = fetch_tencent(existing, public_id, start_date, args.end_date)
                        source_used = "Tencent Finance"
                        if new_data.empty:
                            print("  WARN Tencent returned no new rows; trying East Money")
                            new_data = fetch_eastmoney(existing, public_id, start_date, args.end_date)
                            source_used = "East Money"
                    except Exception as tencent_exc:
                        print(f"  WARN Tencent unavailable; trying East Money: {tencent_exc}")
                        new_data = fetch_eastmoney(existing, public_id, start_date, args.end_date)
                        source_used = "East Money"
                else:
                    new_data = fetch_nasdaq(existing, public_id, start_date, args.end_date)
                    source_used = "Nasdaq"
            except Exception as exc:
                errors.append(f"{csv_name}: public fallback: {exc}")
                print(f"  ERROR public fallback: {exc}")
                continue

        if new_data.empty:
            print(f"  no new rows ({source_used})")
            continue
        combined = write_combined(csv_path, existing, new_data)
        print(
            f"  +{len(new_data)} rows via {source_used}; "
            f"total {len(combined)}, latest {combined['trade_date'].max()}"
        )

    print("\n--- Verification ---")
    for csv_name, _, _, _ in STOCKS:
        frame = pd.read_csv(DATA_DIR / csv_name)
        print(
            f"{csv_name}: {len(frame)} rows, last {int(frame['trade_date'].max())}, "
            f"close {frame.sort_values('trade_date').iloc[-1]['close']}"
        )

    if errors:
        print("\n[FAIL] " + " | ".join(errors))
        return 1
    print("\n[DONE] All data files updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
