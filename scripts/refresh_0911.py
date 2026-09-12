from pathlib import Path
import sys
import json
from dataclasses import replace
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import rebuild_outputs as r
import comps_beta_and_reverse_dcf as reverse
import event_panel

# Refresh traded reference values using the existing share-count and FX bases.
path = ROOT / 'data/valuation_comps_input.csv'
comps = pd.read_csv(path, keep_default_na=False)
comps['equity_value_bn'] = pd.to_numeric(comps['equity_value_bn'], errors='coerce')
for company, filename in [('MiniMax', 'MiniMax_daily.csv'), ('Wenge AI', 'WengeAI_daily.csv')]:
    prices = pd.read_csv(ROOT / 'data' / filename).set_index('trade_date')
    mask = comps.company.eq(company)
    old_date = int(comps.loc[mask, 'valuation_date'].iloc[0].replace('-', ''))
    ratio = float(prices.loc[20260911, 'close']) / float(prices.loc[old_date, 'close'])
    comps.loc[mask, 'equity_value_bn'] = float(comps.loc[mask, 'equity_value_bn'].iloc[0]) * ratio
    comps.loc[mask, 'valuation_date'] = '2026-09-11'
    comps.loc[mask, 'valuation_source_url'] = 'https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get'
    note = ' Price refreshed to 2026-09-11; share-count and FX basis carried forward from the 2026-08-31 snapshot.'
    if note.strip() not in comps.loc[mask, 'comparability_note'].iloc[0]:
        comps.loc[mask, 'comparability_note'] += note
mask = comps.company.eq('Zhipu')
comps.loc[mask, 'valuation_date'] = '2026-09-11'
comps.loc[mask, 'valuation_source_url'] = 'https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get'
comps.to_csv(path, index=False)

r.write_price_summary_csv()
r.write_valuation_summary_csv()
comps = r.build_valuation_comps()
r.write_valuation_comps_csv(comps)
r.write_football_field(comps)
r.write_comps_chart(comps)
r.write_price_paths()
r.write_daily_returns()
reverse.main()

# Preserve the original five-event sample and bootstrap. Report newly observable
# windows separately, including disclosure dates shifted to the next session.
names = {'GLM-5.3-Flash', 'Hy4 preview', '2026 H1 results announcement', 'MSCI Emerging Markets inclusion rebalance'}
events = []
for event in event_panel.load_panel_events():
    if event.event in names:
        if event.company == 'Zhipu' and event.event == '2026 H1 results announcement':
            event = replace(event, day0='2026-09-01')
        events.append(replace(event, reason_if_excluded=''))
supplement = event_panel.event_panel_rows(events)
supplement.insert(0, 'data_cutoff', '2026-09-11')
supplement.to_csv(ROOT / 'eventstudy/september_window_update.csv', index=False)

payload = {
    'audit': r.valuation_audit_rows(),
    'comps': comps.where(pd.notna(comps), None).values.tolist(),
    'market_date': '2026-09-11', 'market_price': r.MARKET.price_hkd,
}
(ROOT / 'tmp/refresh_0911_workbook.json').write_text(json.dumps(payload), encoding='utf-8')
print(pd.read_csv(ROOT / 'data/price_summary.csv').to_string(index=False))
print(supplement[['company','event','reaction_days','drift_days','react_mean','drift_mean','drift_full']].to_string(index=False))
