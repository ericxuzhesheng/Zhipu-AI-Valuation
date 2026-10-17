"""Rebuild the October 16 valuation snapshot, retaining the fixed August event cohort."""
from pathlib import Path
import json
import pandas as pd
import rebuild_outputs as r
import comps_beta_and_reverse_dcf as reverse
import event_panel

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-16'
CUTOFF = 20261016

def main():
    assert r.MARKET.date.strftime('%Y-%m-%d') == DATE
    path = ROOT / 'data/valuation_comps_input.csv'
    comps = pd.read_csv(path, keep_default_na=False)
    comps['equity_value_bn'] = pd.to_numeric(comps['equity_value_bn'], errors='coerce')
    for company, filename in [('MiniMax','MiniMax_daily.csv'), ('Wenge AI','WengeAI_daily.csv')]:
        prices = pd.read_csv(ROOT / 'data' / filename).set_index('trade_date')
        mask = comps.company.eq(company)
        old_date = int(comps.loc[mask,'valuation_date'].iloc[0].replace('-',''))
        comps.loc[mask,'equity_value_bn'] *= float(prices.loc[CUTOFF,'close']) / float(prices.loc[old_date,'close'])
        comps.loc[mask,'valuation_date'] = DATE
        symbol = {'MiniMax':'0100.HK', 'Wenge AI':'1956.HK'}[company]
        comps.loc[mask,'valuation_source_url'] = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        comps.loc[mask,'comparability_note'] = comps.loc[mask,'comparability_note'].str.split(' Price refreshed').str[0] + f' Price refreshed to {DATE}; share-count and FX basis carried forward from 2026-08-31.'
    bridge = pd.read_csv(ROOT/'data/comps_price_bridge.csv')
    for company, rows in bridge.groupby('company'):
        mask = comps.company.eq(company)
        old_date = comps.loc[mask,'valuation_date'].iloc[0]
        prices = rows.set_index('trade_date').close
        comps.loc[mask,'equity_value_bn'] *= float(prices.loc[DATE]) / float(prices.loc[old_date])
        comps.loc[mask,'valuation_date'] = DATE
        comps.loc[mask,'valuation_source_url'] = rows.source_url.iloc[0]
        comps.loc[mask,'comparability_note'] = comps.loc[mask,'comparability_note'].str.split(' Price refreshed').str[0] + f' Price refreshed to {DATE}; August share-count and FX basis retained, not a newly verified market capitalization.'
    comps.loc[comps.company.eq('Zhipu'),'valuation_date'] = DATE
    comps.loc[comps.company.eq('Zhipu'),'valuation_source_url'] = 'https://query1.finance.yahoo.com/v8/finance/chart/2513.HK'
    comps.to_csv(path,index=False)
    r.write_price_summary_csv()
    r.write_valuation_summary_csv()
    comps = r.build_valuation_comps()
    r.write_valuation_comps_csv(comps)
    r.write_football_field(comps)
    r.write_comps_chart(comps)
    r.write_price_paths()
    r.write_daily_returns()
    reverse.main()
    events = [event_panel.PanelEvent(company,ticker,name,day0,kind,
        'dated disclosures; first subsequent session; overlapping news',filename,peer)
        for company,ticker,name,day0,kind,filename,peer in [
        ('Zhipu','02513.HK','ZCode evening response / public source','2026-09-21','product_trust','Zhipu_KnowledgeAtlas_daily.csv','MiniMax_daily.csv'),
        ('MiniMax','00100.HK','Code CLI evening release','2026-09-21','developer_tool','MiniMax_daily.csv','Zhipu_KnowledgeAtlas_daily.csv'),
        ('Zhipu','02513.HK','Formal interim report','2026-09-25','financial_disclosure','Zhipu_KnowledgeAtlas_daily.csv','MiniMax_daily.csv'),
        ('MiniMax','00100.HK','M3.1-Flash-Preview availability','2026-09-28','capability_preview','MiniMax_daily.csv','Zhipu_KnowledgeAtlas_daily.csv'),
        ('Zhipu','02513.HK','September share awards','2026-10-02','share_award','Zhipu_KnowledgeAtlas_daily.csv','MiniMax_daily.csv'),
    ]]
    supplement = event_panel.event_panel_rows(events)
    supplement.insert(0,'data_cutoff',DATE)
    supplement.to_csv(ROOT/'eventstudy/october_window_update.csv',index=False)
    returns = []
    for company,filename in [('Zhipu','Zhipu_KnowledgeAtlas_daily.csv'),('MiniMax','MiniMax_daily.csv'),('Wenge AI','WengeAI_daily.csv')]:
        prices = pd.read_csv(ROOT/'data'/filename).set_index('trade_date').close
        returns.append(dict(company=company,data_cutoff=DATE,close_0930=float(prices.loc[20260930]),
            latest_close=float(prices.loc[CUTOFF]),return_from_0930_pct=(prices.loc[CUTOFF]/prices.loc[20260930]-1)*100,
            return_from_0831_pct=(prices.loc[CUTOFF]/prices.loc[20260831]-1)*100))
    pd.DataFrame(returns).to_csv(ROOT/'eventstudy/october_returns.csv',index=False)
    multiple = float(comps.loc[comps.company.eq('MiniMax'),'multiple_x'].iloc[0])
    peer_price = multiple*r.REV_LTM_USDM/r.SHARES_M*r.USD_HKD
    growth, revenue = reverse.solve_required_path(r.WACC,0.40)
    payload = dict(audit=r.valuation_audit_rows(),comps=comps.where(pd.notna(comps),None).values.tolist(),
        market_date=DATE,market_price=r.MARKET.price_hkd,market_cap_bn=r.MARKET.equity_value_usdm/1000,
        zhipu_multiple=r.MARKET.revenue_multiple,minimax_multiple=multiple,peer_price=peer_price,
        peer_discount_pct=(1-peer_price/r.MARKET.price_hkd)*100,required_revenue_bn=revenue/1000,
        required_growth_2027_pct=growth*100,required_cagr_pct=((revenue/r.REV_2026_USDM)**(1/9)-1)*100,
        weighted_dcf=sum(s.probability*r.project_scenario(s)['per_share_hkd'] for s in r.SCENARIOS),returns=returns)
    (ROOT/'tmp/refresh_1011_workbook.json').write_text(json.dumps(payload),encoding='utf-8')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('audit','comps')},indent=2))
    print(supplement[['event','reaction_days','drift_days','drift_full']].to_string(index=False))

if __name__ == '__main__':
    main()
