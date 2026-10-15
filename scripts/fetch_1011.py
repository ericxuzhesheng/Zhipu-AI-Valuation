"""Stage October 12-14 prices; append only after all eleven series validate."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / 'tmp/1015_sources'
STAGE.mkdir(parents=True, exist_ok=True)
SPECS = {
    'Zhipu_KnowledgeAtlas': 'hk02513', 'MiniMax': 'hk00100', 'WengeAI': 'hk01956',
    'Alibaba': 'hk09988', 'Baidu': 'hk09888', 'Tencent': 'hk00700', 'Meituan': 'hk03690',
    'Google': 'GOOGL', 'Meta': 'META', 'Microsoft': 'MSFT', 'Tesla': 'TSLA',
}

def fetch(spec):
    name, symbol = spec
    old = pd.read_csv(ROOT / f'data/{name}_daily.csv')
    assert int(old.trade_date.max()) == 20261009, name
    if symbol.startswith('hk'):
        url = 'https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get'
        params = {'param': f'{symbol},day,2026-10-09,2026-10-14,640,qfq'}
    else:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        params = {'period1': int(datetime(2026, 10, 9, tzinfo=timezone.utc).timestamp()),
                  'period2': int(datetime(2026, 10, 15, tzinfo=timezone.utc).timestamp()), 'interval': '1d'}
    response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=40)
    response.raise_for_status()
    payload = response.json()
    (STAGE / f'{symbol}.json').write_text(json.dumps({'url':response.url,'response':payload}), encoding='utf-8')
    records = []
    if symbol.startswith('hk'):
        security = payload['data'][symbol]
        for row in security.get('day', security.get('qfqday', [])):
            records.append(dict(trade_date=int(row[0].replace('-','')), open=float(row[1]),
                close=float(row[2]), high=float(row[3]), low=float(row[4]), vol=float(row[5]),
                amount=float(row[8])*10000))
        expected = [20261012,20261013,20261014]
    else:
        result = payload['chart']['result'][0]
        quote = result['indicators']['quote'][0]
        for i, timestamp in enumerate(result['timestamp']):
            if quote['close'][i] is None:
                continue
            records.append(dict(trade_date=int(datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y%m%d')),
                **{key:round(quote[key][i], 4) for key in ('open','high','low','close')},
                vol=quote['volume'][i], amount=quote['volume'][i]*quote['close'][i]))
        expected = [20261012,20261013,20261014]
    rows = []
    previous = float(old.close.iloc[-1])
    for row in records:
        if not 20261009 < row['trade_date'] <= 20261014:
            continue
        assert row['low'] <= min(row['open'],row['close']) <= max(row['open'],row['close']) <= row['high']
        row.update(ts_code=old.ts_code.iloc[-1], pre_close=previous,
                   change=row['close']-previous, pct_chg=(row['close']/previous-1)*100)
        previous = row['close']
        rows.append(row)
    new = pd.DataFrame(rows, columns=old.columns)
    assert new.trade_date.tolist() == expected, (name,new.trade_date.tolist())
    new.to_csv(STAGE / f'{name}_daily.csv', index=False)
    return name, new

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        staged = list(pool.map(fetch, SPECS.items()))
    assert abs(dict(staged)['Zhipu_KnowledgeAtlas'].close.iloc[-1] - 572.0) < 1e-8
    for name, new in staged:
        path = ROOT / f'data/{name}_daily.csv'
        original = path.read_bytes()
        increment = (STAGE / path.name).read_bytes().split(b'\n',1)[1]
        path.write_bytes(original + (b'' if original.endswith(b'\n') else b'\n') + increment)
        print(name, len(new), float(new.close.iloc[-1]))
