"""Reproduce the user's companion Anthropic IPO model as a separate comparison.

USD billions; information cutoff 2026-09-30; assumed valuation date 2026-12-31.
Model assumptions are not company guidance or a completed funding transaction.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WACC = 0.12
TERMINAL_G = 0.03
TAX = 0.25
ANCHOR_REVENUE = 60.0
FORWARD_MULTIPLE = 10.0
IPO_BENCHMARK = 2000.0
NET_CASH_ASSUMPTION = 0.0


def calculate(wacc=WACC, terminal_g=TERMINAL_G):
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
    required_terminal_fcf = (IPO_BENCHMARK-NET_CASH_ASSUMPTION-pv_explicit)*(1+wacc)**10*(wacc-terminal_g)
    required_margin = (required_terminal_fcf+(terminal_revenue-previous_revenue)*last.nwc_to_revenue-terminal_revenue*(last.da_to_revenue-last.capex_to_revenue))/(terminal_revenue*(1-TAX))
    revenue_2028 = rows[1]['revenue_usdbn']
    summary = {
        'Information cutoff':'2026-09-30', 'Assumed valuation date':'2026-12-31',
        '2028 revenue midpoint (USD bn)':revenue_2028, 'Forward EV / 2028 revenue':FORWARD_MULTIPLE,
        'Revenue-multiple EV (USD bn)':revenue_2028*FORWARD_MULTIPLE,
        'DCF EV (USD bn)':pv_explicit+pv_terminal, 'PV explicit UFCF (USD bn)':pv_explicit,
        'PV terminal value (USD bn)':pv_terminal, 'Terminal value share':pv_terminal/(pv_explicit+pv_terminal),
        'Reported IPO equity benchmark (USD bn)':IPO_BENCHMARK,
        'Net cash assumption (USD bn)':NET_CASH_ASSUMPTION, 'WACC assumption':wacc,
        'Terminal growth assumption':terminal_g, 'Cash tax rate assumption':TAX,
        'Required terminal EBIT margin at benchmark':required_margin,
    }
    return pd.DataFrame(rows), summary


def main():
    projection, summary = calculate()
    assert abs(summary['DCF EV (USD bn)'] - 788.3047505219974) < 1e-8
    assert abs(projection.loc[projection.year.eq(2028), 'ufcf_usdbn'].iloc[0] - 18.0) < 1e-8
    projection.to_csv(ROOT/'eventstudy/anthropic_ipo_projection.csv', index=False)
    pd.DataFrame(summary.items(), columns=['metric','value']).to_csv(ROOT/'eventstudy/anthropic_ipo_summary.csv', index=False)
    rows=[]
    for wacc in [0.10,0.12,0.14]:
        for terminal_g in [0.02,0.03,0.04]:
            _, s = calculate(wacc,terminal_g)
            rows.append({'wacc':wacc,'terminal_growth':terminal_g,'dcf_ev_usdbn':s['DCF EV (USD bn)']})
    pd.DataFrame(rows).to_csv(ROOT/'eventstudy/anthropic_ipo_sensitivity.csv',index=False)
    print(pd.Series(summary).to_string())


if __name__ == '__main__':
    main()
