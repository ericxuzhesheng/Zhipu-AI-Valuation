"""Reproduce the user's companion Anthropic IPO model as a separate comparison.

USD billions; Anthropic information cutoff 2026-10-26; assumed valuation date 2026-12-31.
Model assumptions are not company guidance or a completed funding transaction.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WACC = 0.12
TERMINAL_G = 0.03
TAX = 0.25
ANCHOR_REVENUE = 64.0
FORWARD_MULTIPLE = 10.0
DISCLOSURES = pd.read_csv(ROOT / 'data/anthropic_ipo_disclosures_input.csv').set_index('metric')
IPO_BENCHMARK = float(DISCLOSURES.loc['Latest IPO equity discussion', 'value'])
NET_CASH_ASSUMPTION = 0.0
INFORMATION_CUTOFF = '2026-10-26'
S1_FINANCIALS = pd.read_csv(ROOT / 'data/anthropic_s1_financials_input.csv').set_index('period')
S1_BALANCE = pd.read_csv(ROOT / 'data/anthropic_s1_balance_input.csv').set_index('metric')


def calculate(wacc=WACC, terminal_g=TERMINAL_G, ipo_benchmark=IPO_BENCHMARK,
              net_cash_adjustment=NET_CASH_ASSUMPTION):
    assert wacc > terminal_g
    inputs = pd.read_csv(ROOT / 'data/anthropic_ipo_projection_input.csv')
    previous_revenue = ANCHOR_REVENUE
    previous_nwc = ANCHOR_REVENUE * float(inputs.iloc[0].nwc_to_revenue)
    rows = []
    for t, row in enumerate(inputs.iloc[1:].itertuples(index=False), 1):
        revenue = previous_revenue * (1 + row.revenue_growth)
        ebit = revenue * row.ebit_margin
        taxes = max(ebit, 0) * TAX
        da = revenue * row.da_to_revenue
        capex = revenue * row.capex_to_revenue
        nwc = revenue * row.nwc_to_revenue
        delta_nwc = nwc - previous_nwc
        fcf = ebit - taxes + da - capex - delta_nwc
        rows.append(dict(year=row.year, revenue_usdbn=revenue, revenue_growth=row.revenue_growth,
            ebit_margin=row.ebit_margin, after_tax_ebit_usdbn=ebit-taxes, da_usdbn=da,
            capex_usdbn=capex, delta_nwc_usdbn=delta_nwc, ufcf_usdbn=fcf,
            discount_period=t, pv_ufcf_usdbn=fcf/(1+wacc)**t))
        previous_revenue, previous_nwc = revenue, nwc
    last = inputs.iloc[-1]
    terminal_revenue = previous_revenue * (1+terminal_g)
    terminal_fcf = terminal_revenue * (last.ebit_margin*(1-TAX)+last.da_to_revenue-last.capex_to_revenue) - (terminal_revenue-previous_revenue)*last.nwc_to_revenue
    pv_explicit = sum(row['pv_ufcf_usdbn'] for row in rows)
    pv_terminal = terminal_fcf / (wacc-terminal_g) / (1+wacc)**10
    required_terminal_fcf = (ipo_benchmark-net_cash_adjustment-pv_explicit)*(1+wacc)**10*(wacc-terminal_g)
    required_margin = (required_terminal_fcf+(terminal_revenue-previous_revenue)*last.nwc_to_revenue-terminal_revenue*(last.da_to_revenue-last.capex_to_revenue))/(terminal_revenue*(1-TAX))
    revenue_2028 = rows[1]['revenue_usdbn']
    summary = {
        'Information cutoff':f'{INFORMATION_CUTOFF} (Beijing time)', 'Assumed valuation date':'2026-12-31',
        '2028 revenue midpoint (USD bn)':revenue_2028, 'Forward EV / 2028 revenue':FORWARD_MULTIPLE,
        'Revenue-multiple EV (USD bn)':revenue_2028*FORWARD_MULTIPLE,
        'DCF EV (USD bn)':pv_explicit+pv_terminal, 'PV explicit UFCF (USD bn)':pv_explicit,
        'PV terminal value (USD bn)':pv_terminal, 'Terminal value share':pv_terminal/(pv_explicit+pv_terminal),
        'Reported IPO equity benchmark (USD bn)':ipo_benchmark,
        'Net cash assumption (USD bn)':net_cash_adjustment, 'WACC assumption':wacc,
        'Terminal growth assumption':terminal_g, 'Cash tax rate assumption':TAX,
        'Required terminal EBIT margin at benchmark':required_margin,
        'DCF equity value (USD bn)':pv_explicit+pv_terminal+net_cash_adjustment,
        'DCF discount to IPO discussion':1-(pv_explicit+pv_terminal+net_cash_adjustment)/ipo_benchmark,
        'Reported Q1-Q3 revenue (USD bn)':sum(float(DISCLOSURES.loc[q+' revenue','value']) for q in ['Q1','Q2','Q3']),
        'Earlier Reuters compute commitment observation (USD bn)':float(DISCLOSURES.loc['Long-term compute commitments','value']),
        'S1 minimum purchase commitments (USD bn)':float(S1_BALANCE.loc['Minimum purchase commitments','value']),
        'S1 uncommenced lease obligations (USD bn)':float(S1_BALANCE.loc['Uncommenced lease obligations','value']),
        'S1 H1 revenue (USD bn)':float(S1_FINANCIALS.loc['H1 2026','revenue_usdbn']),
        'S1 H1 operating income (USD bn)':float(S1_FINANCIALS.loc['H1 2026','operating_income_usdbn']),
        'S1 H1 net income (USD bn)':float(S1_FINANCIALS.loc['H1 2026','net_income_usdbn']),
        'S1 H1 operating cash flow (USD bn)':float(S1_FINANCIALS.loc['H1 2026','operating_cash_flow_usdbn']),
    }
    h1 = S1_FINANCIALS.loc['H1 2026']
    summary['S1 H1 cash flow less cash capex (USD bn)'] = float(h1.operating_cash_flow_usdbn-h1.cash_capex_usdbn)
    summary['Q4 revenue required for annual anchor (USD bn)'] = ANCHOR_REVENUE-summary['Reported Q1-Q3 revenue (USD bn)']
    summary['Required Q4 sequential growth'] = summary['Q4 revenue required for annual anchor (USD bn)']/float(DISCLOSURES.loc['Q3 revenue','value'])-1
    return pd.DataFrame(rows), summary


def historical_cash_bridge():
    """June snapshots are sensitivities, not a December net-cash forecast or IPO price."""
    balance = S1_BALANCE['value']
    liquidity = float(balance['Cash and equivalents'] + balance['Short-term investments'])
    finance_leases = float(balance['Finance lease liabilities'])
    notes = float(balance['Amazon 2023 note principal'] + balance['Amazon 2024 note principal'])
    rows = []
    for name, note_principal in [('All June note principal retained', notes),
                                 ('Full conversion illustrative ceiling', 0.0)]:
        adjustment = liquidity-finance_leases-note_principal
        _, result = calculate(net_cash_adjustment=adjustment)
        rows.append(dict(case=name, balance_date='2026-06-30', liquidity_usdbn=liquidity,
            finance_lease_liabilities_usdbn=finance_leases, note_principal_usdbn=note_principal,
            net_cash_proxy_usdbn=adjustment, dcf_equity_usdbn=result['DCF equity value (USD bn)'],
            required_terminal_ebit_margin=result['Required terminal EBIT margin at benchmark'],
            classification='Historical principal-based sensitivity; no H2 cash roll-forward, IPO proceeds or new funding; conversion subject to 12% ownership cap; not an existing-common equity allocation'))
    return pd.DataFrame(rows)


def main():
    projection, summary = calculate()
    assert abs(summary['DCF EV (USD bn)'] - 788.5394443995484) < 1e-8
    assert abs(projection.loc[projection.year.eq(2028), 'ufcf_usdbn'].iloc[0] - 18.16) < 1e-8
    projection.to_csv(ROOT/'eventstudy/anthropic_ipo_projection.csv', index=False)
    pd.DataFrame(summary.items(), columns=['metric','value']).to_csv(ROOT/'eventstudy/anthropic_ipo_summary.csv', index=False)
    rows=[]
    for wacc in [0.10,0.12,0.14]:
        for terminal_g in [0.02,0.03,0.04]:
            _, s = calculate(wacc,terminal_g)
            rows.append({'wacc':wacc,'terminal_growth':terminal_g,'dcf_ev_usdbn':s['DCF EV (USD bn)']})
    pd.DataFrame(rows).to_csv(ROOT/'eventstudy/anthropic_ipo_sensitivity.csv',index=False)
    historical_cash_bridge().to_csv(ROOT/'eventstudy/anthropic_s1_cash_bridge.csv',index=False)
    runtime = ROOT/'tmp/1011_runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    _, historical = calculate(ipo_benchmark=2000)
    payload = dict(cutoff=INFORMATION_CUTOFF, dcf=summary['DCF EV (USD bn)'],
        requiredMargin=summary['Required terminal EBIT margin at benchmark'],
        historicalMargin=historical['Required terminal EBIT margin at benchmark'],
        q4Required=summary['Q4 revenue required for annual anchor (USD bn)'],
        q4Growth=summary['Required Q4 sequential growth'],
        quarters=[float(DISCLOSURES.loc[q+' revenue','value']) for q in ['Q1','Q2','Q3']],
        financials=S1_FINANCIALS.fillna('').to_dict(orient='index'),
        balance=S1_BALANCE['value'].to_dict(), bridges=historical_cash_bridge().to_dict(orient='records'))
    (runtime/'anthropic-latest.json').write_text(json.dumps(payload),encoding='utf-8')
    print(pd.Series(summary).to_string())


if __name__ == '__main__':
    main()
