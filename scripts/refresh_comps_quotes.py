"""Fetch price bridges for the five contextual public comparables (not new fundamentals)."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
SPECS = {'SenseTime':'hk00020', 'Phancy':'hk06682', 'Palantir':'PLTR',
         'Cloudflare':'NET', 'Snowflake':'SNOW'}
END = '2026-10-23'

def fetch(item):
    company, symbol = item
    ticker = f'{int(symbol[2:]):04d}.HK' if symbol.startswith('hk') else symbol
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
    params = {'period1':int(datetime(2026,8,31,tzinfo=timezone.utc).timestamp()),
              'period2':int((pd.Timestamp(END,tz='UTC')+pd.Timedelta(days=1)).timestamp()),'interval':'1d'}
    response = requests.get(url,params=params,headers={'User-Agent':'Mozilla/5.0'},timeout=40)
    response.raise_for_status()
    payload = response.json()
    stage = ROOT/'tmp/1017_sources'
    stage.mkdir(parents=True,exist_ok=True)
    (stage/f'{symbol}.json').write_text(json.dumps({'url':response.url,'response':payload}),encoding='utf-8')
    result = payload['chart']['result'][0]
    prices = {datetime.fromtimestamp(t,timezone.utc).strftime('%Y-%m-%d'):p
              for t,p in zip(result['timestamp'],result['indicators']['quote'][0]['close'])}
    if symbol.startswith('hk'):
        prices = {day: round(price, 3) for day, price in prices.items() if price is not None}
    return [dict(company=company,ticker=symbol,trade_date=d,close=prices[d],source_url=response.url)
            for d in sorted({'2026-08-31', '2026-10-16', END})]

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = [row for group in pool.map(fetch,SPECS.items()) for row in group]
    frame = pd.DataFrame(rows)
    assert len(frame) == 15 and frame.close.gt(0).all()
    frame.to_csv(ROOT/'data/comps_price_bridge.csv',index=False)
    print(frame[['company','trade_date','close']].to_string(index=False))
