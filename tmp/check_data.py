import pandas as pd, os

for f in sorted(os.listdir('data')):
    if f.endswith('_daily.csv'):
        df = pd.read_csv(os.path.join('data', f))
        last = df.iloc[-1]
        print(f"{f}: {len(df)} rows, last date: {last['trade_date']}, last close: {last['close']}")
