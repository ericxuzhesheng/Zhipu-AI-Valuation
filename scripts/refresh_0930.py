"""Refresh the September 30 market snapshot without changing the August event cohort.

Run after staging the four new daily bars per series in tmp/0930_sources/.
Existing rows and workbook formulas are preserved; workbook edits use artifact-tool.
"""
from pathlib import Path
from dataclasses import replace
import json
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
CUTOFF = 20260930
DATE = '2026-09-30'
NEW_DATES = [20260925, 20260928, 20260929, 20260930]

# Validate every staged series before any data mutation, then append only new rows.
staged = []
for path in sorted((ROOT / 'data').glob('*_daily.csv')):
    old = pd.read_csv(path)
    new_path = ROOT / 'tmp/0930_sources' / path.name
    new = pd.read_csv(new_path)
    assert list(old.columns) == list(new.columns), path.name
    assert list(new.trade_date) == NEW_DATES, path.name
    assert old.trade_date.is_unique and old.trade_date.is_monotonic_increasing, path.name
    assert int(old.trade_date.max()) in (20260924, CUTOFF), path.name
    if int(old.trade_date.max()) == CUTOFF:
        pd.testing.assert_frame_equal(old.tail(4).reset_index(drop=True), new, check_dtype=False)
        continue
    assert abs(float(new.pre_close.iloc[0]) - float(old.close.iloc[-1])) < 1e-7, path.name
    staged.append((path, new_path))
for path, new_path in staged:
    existing = path.read_bytes()
    increment = new_path.read_bytes().split(b'\n', 1)[1]
    path.write_bytes(existing + (b'' if existing.endswith(b'\n') else b'\n') + increment)

import rebuild_outputs as r
import comps_beta_and_reverse_dcf as reverse
import event_panel

path = ROOT / 'data/valuation_comps_input.csv'
comps = pd.read_csv(path, keep_default_na=False)
comps['equity_value_bn'] = pd.to_numeric(comps['equity_value_bn'], errors='coerce')
for company, filename in [('MiniMax', 'MiniMax_daily.csv'), ('Wenge AI', 'WengeAI_daily.csv')]:
    prices = pd.read_csv(ROOT / 'data' / filename).set_index('trade_date')
    mask = comps.company.eq(company)
    old_date = int(comps.loc[mask, 'valuation_date'].iloc[0].replace('-', ''))
    comps.loc[mask, 'equity_value_bn'] *= float(prices.loc[CUTOFF, 'close']) / float(prices.loc[old_date, 'close'])
    comps.loc[mask, 'valuation_date'] = DATE
    comps.loc[mask, 'valuation_source_url'] = 'https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get'
    note = f' Price refreshed to {DATE}; share-count and FX basis carried forward from the 2026-08-31 snapshot.'
    if note.strip() not in comps.loc[mask, 'comparability_note'].iloc[0]:
        comps.loc[mask, 'comparability_note'] += note
comps.loc[comps.company.eq('Zhipu'), 'valuation_date'] = DATE
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

# Retain all original events/estimates. Newly observed windows remain a supplement.
names = {'GLM-5.3-Flash', 'Hy4 preview', '2026 H1 results announcement', 'MSCI Emerging Markets inclusion rebalance'}
events = []
for event in event_panel.load_panel_events():
    if event.event in names:
        if event.company == 'Zhipu' and event.event == '2026 H1 results announcement':
            event = replace(event, day0='2026-09-01')
        events.append(replace(event, reason_if_excluded=''))
for company, ticker, name, day0, event_type, filename, peer in [
    ('Zhipu', '02513.HK', 'ZCode evening response / public source', '2026-09-21', 'product_trust', 'Zhipu_KnowledgeAtlas_daily.csv', 'MiniMax_daily.csv'),
    ('MiniMax', '00100.HK', 'Code CLI evening release', '2026-09-21', 'developer_tool', 'MiniMax_daily.csv', 'Zhipu_KnowledgeAtlas_daily.csv'),
    ('Zhipu', '02513.HK', 'Formal interim report', '2026-09-25', 'financial_disclosure', 'Zhipu_KnowledgeAtlas_daily.csv', 'MiniMax_daily.csv'),
    ('MiniMax', '00100.HK', 'M3.1-Flash-Preview availability', '2026-09-28', 'capability_preview', 'MiniMax_daily.csv', 'Zhipu_KnowledgeAtlas_daily.csv'),
]:
    events.append(event_panel.PanelEvent(company, ticker, name, day0, event_type,
                  'dated disclosures; first subsequent session; overlapping news', filename, peer))
supplement = event_panel.event_panel_rows(events)
supplement.insert(0, 'data_cutoff', DATE)
supplement.to_csv(ROOT / 'eventstudy/september_window_update.csv', index=False)

returns = []
for company, filename in [('Zhipu','Zhipu_KnowledgeAtlas_daily.csv'), ('MiniMax','MiniMax_daily.csv'), ('Wenge AI','WengeAI_daily.csv')]:
    prices = pd.read_csv(ROOT / 'data' / filename).set_index('trade_date').close
    row = {'company':company, 'data_cutoff':DATE, 'close_0930':prices.loc[CUTOFF]}
    for date, label in [(20260831,'0831'), (20260918,'0918'), (20260924,'0924')]:
        row[f'close_{label}'] = prices.loc[date]
        row[f'return_from_{label}_pct'] = (prices.loc[CUTOFF] / prices.loc[date] - 1) * 100
    returns.append(row)
pd.DataFrame(returns).to_csv(ROOT / 'eventstudy/september_24_30_returns.csv', index=False)

minimax_multiple = float(comps.loc[comps.company.eq('MiniMax'), 'multiple_x'].iloc[0])
peer_price = minimax_multiple * r.REV_LTM_USDM / r.SHARES_M * r.USD_HKD
start_growth, required_revenue = reverse.solve_required_path(r.WACC, 0.40)
payload = {
    'audit': r.valuation_audit_rows(), 'comps': comps.where(pd.notna(comps), None).values.tolist(),
    'market_date':DATE, 'market_price':r.MARKET.price_hkd, 'market_cap_bn':r.MARKET.equity_value_usdm/1000,
    'zhipu_multiple':r.MARKET.revenue_multiple, 'minimax_multiple':minimax_multiple,
    'peer_price':peer_price, 'peer_discount_pct':(1-peer_price/r.MARKET.price_hkd)*100,
    'required_revenue_bn':required_revenue/1000, 'required_growth_2027_pct':start_growth*100,
    'required_cagr_pct':((required_revenue/r.REV_2026_USDM)**(1/9)-1)*100,
    'weighted_dcf':sum(s.probability*r.project_scenario(s)['per_share_hkd'] for s in r.SCENARIOS),
    'returns':returns,
}
(ROOT / 'tmp/refresh_0930_workbook.json').write_text(json.dumps(payload), encoding='utf-8')
print(json.dumps({k:v for k,v in payload.items() if k not in ('comps','audit')}, indent=2))
print(supplement[['company','event','reaction_days','drift_days','react_mean','drift_mean','drift_full']].to_string(index=False))
