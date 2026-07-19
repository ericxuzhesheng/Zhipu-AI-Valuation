"""
增量更新所有 data/*_daily.csv 到最新交易日。
使用 Tushare hk_daily / us_daily API。
"""
import os
import time
import pandas as pd
import tushare as ts

TOKEN = os.environ.get("TUSHARE_TOKEN") or os.environ.get("tushare_token")
if not TOKEN:
    raise RuntimeError("TUSHARE_TOKEN not set")

pro = ts.pro_api(TOKEN)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# (csv_filename, ts_code, market: 'hk' or 'us')
STOCKS = [
    ("Zhipu_KnowledgeAtlas_daily.csv", "02513.HK", "hk"),
    ("MiniMax_daily.csv", "00100.HK", "hk"),
    ("WengeAI_daily.csv", "01956.HK", "hk"),
    ("Alibaba_daily.csv", "9988.HK", "hk"),
    ("Baidu_daily.csv", "9888.HK", "hk"),
    ("Tencent_daily.csv", "0700.HK", "hk"),
    ("Meituan_daily.csv", "3690.HK", "hk"),
    ("Google_daily.csv", "GOOGL", "us"),
    ("Meta_daily.csv", "META", "us"),
    ("Microsoft_daily.csv", "MSFT", "us"),
    ("Tesla_daily.csv", "TSLA", "us"),
]

TODAY = pd.Timestamp.now().strftime("%Y%m%d")

for csv_name, ts_code, market in STOCKS:
    csv_path = os.path.join(DATA_DIR, csv_name)
    
    # 读取已有数据确定起始日期
    existing = pd.read_csv(csv_path)
    last_date = str(existing["trade_date"].max())
    # 从最后一天的下一天开始取
    start_date = (pd.Timestamp(last_date) + pd.Timedelta(days=1)).strftime("%Y%m%d")
    
    if start_date > TODAY:
        print(f"[SKIP] {csv_name}: already up to {last_date}")
        continue
    
    print(f"[FETCH] {csv_name} ({ts_code}): {start_date} -> {TODAY} ...", end=" ")
    
    try:
        if market == "hk":
            new_data = pro.hk_daily(ts_code=ts_code, start_date=start_date, end_date=TODAY)
        else:
            new_data = pro.us_daily(ts_code=ts_code, start_date=start_date, end_date=TODAY)
        
        if new_data is None or len(new_data) == 0:
            print("no new data")
            continue
        
        # Tushare 返回倒序，需排序
        new_data = new_data.sort_values("trade_date").reset_index(drop=True)
        
        # 确保列与已有数据一致
        new_data = new_data[existing.columns]
        
        # 追加
        combined = pd.concat([existing, new_data], ignore_index=True)
        combined = combined.drop_duplicates(subset=["trade_date"], keep="last")
        combined = combined.sort_values("trade_date").reset_index(drop=True)
        combined.to_csv(csv_path, index=False)
        
        print(f"+{len(new_data)} rows -> total {len(combined)} rows, new last: {combined['trade_date'].max()}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Tushare API rate limit
    time.sleep(0.5)

print("\n[DONE] All data files updated.")

# 验证结果
print("\n--- 验证 ---")
for csv_name, ts_code, market in STOCKS:
    csv_path = os.path.join(DATA_DIR, csv_name)
    df = pd.read_csv(csv_path)
    print(f"{csv_name}: {len(df)} rows, last: {df['trade_date'].max()}, close: {df.iloc[-1]['close']}")
