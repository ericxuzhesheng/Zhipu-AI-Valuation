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
END = '2026-10-14'

def fetch(item):
    company, symbol = item
    if symbol.startswith('hk'):
        url = 'https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get'
        params = {'param':f'{symbol},day,2026-08-31,{END},640,qfq'}
    else:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        params = {'period1':int(datetime(2026,8,31,tzinfo=timezone.utc).timestamp()),
                  'period2':int(datetime(2026,10,15,tzinfo=timezone.utc).timestamp()),'interval':'1d'}
    response = requests.get(url,params=params,headers={'User-Agent':'Mozilla/5.0'},timeout=40)
    response.raise_for_status()
    payload = response.json()
    stage = ROOT/'tmp/1015_sources'
    stage.mkdir(parents=True,exist_ok=True)
    (stage/f'{symbol}.json').write_text(json.dumps({'url':response.url,'response':payload}),encoding='utf-8')
    if symbol.startswith('hk'):
        security = payload['data'][symbol]
        prices = {row[0]:float(row[2]) for row in security.get('day',security.get('qfqday',[]))}
    else:
        result = payload['chart']['result'][0]
        prices = {datetime.fromtimestamp(t,timezone.utc).strftime('%Y-%m-%d'):p
                  for t,p in zip(result['timestamp'],result['indicators']['quote'][0]['close'])}
    return [dict(company=company,ticker=symbol,trade_date=d,close=prices[d],source_url=response.url)
            for d in ['2026-08-31', END]]

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = [row for group in pool.map(fetch,SPECS.items()) for row in group]
    frame = pd.DataFrame(rows)
    assert len(frame) == 10 and frame.close.gt(0).all()
    frame.to_csv(ROOT/'data/comps_price_bridge.csv',index=False)
    print(frame[['company','trade_date','close']].to_string(index=False))
