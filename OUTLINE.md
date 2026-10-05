# Paper Map & Status - Zhipu AI (2513.HK) Valuation + Capability-Surprise Event Study

**Title:** *Capability Surprise and the Pricing of an Early-Commercial-Stage Foundation-Model Lab:
Evidence from Zhipu AI (2513.HK).*  
**Author:** Zhesheng Xu (42353012), Corporate Finance, 2025-2026-2.  
**Build:** XeLaTeX (`paper/main.tex` to `main.pdf`). **Information cutoff 2026-09-30; market data as of 2026-09-30; original event cohort through 2026-08-31.**

> This revision has no word-count cap. The paper separates evidence of immediate capability repricing
> from unestablished durable drift and includes a full reference list. The default validator retains
> course word limits; use `python scripts/validate_outputs.py --ignore-word-limits` for this expanded draft.

---

## Structure (current)

| Section | Role | Key content |
|---|---|---|
| Cover | SWUFE official template | official course-paper cover and crest watermark |
| Abstract | summary | subject, dual method, headline valuation gap, takeaway |
| 1. Introduction | setup | 3 research questions; capability-surprise reframing; frontier-AI financing moving into public price discovery |
| 2. Background | condensed | open-weight model; Zhipu H1 2026 API-led growth and loss profile; IPO, July placement, re-rating, and MiniMax H1/model-event comparison |
| 3. Industry, Macro, Strategy | condensed | Porter + leaderboard cost-disruption; HK AI-IPO landscape; macro + flow events |
| 4. Valuation | main line | WACC; 3-scenario DCF; reverse DCF + heatmap; layered relative valuation; real-options reading |
| 5. Capability Surprise | empirical evidence | CAR results; capability and flow events; peer adjustment; block-bootstrap evidence for immediate repricing and limits on drift |
| 6. Discussion | interpretation and extension | September partial unwinding and incomplete windows; financing and trust hypotheses; Anthropic as a commercialization and valuation-method illustration |
| 7. Conclusion | close | immediate capability repricing; demanding price-implied operating assumptions; durable drift not statistically established |
| Appendix A-D | reproducibility | statements, DCF chain, beta bridge, reverse-DCF sensitivity grid |

## Argument
The valuation estimates recover the operating conditions required by the observed price. The event study asks how prices respond when new capability information arrives. Five independently dated releases support immediate repricing, while the drift test leaves persistence unresolved. September price changes and the Anthropic comparison extend the discussion without adding identified causal effects or a second empirical test of Zhipu.

- Capability surprise is the information event examined in the paper.
- Reverse DCF states what the company would have to achieve to support the price.
- Real options describe the possible value of favorable future outcomes; the DCF gap alone does not establish mispricing.
- Model releases are dated separately from index and Stock Connect events.

## Headline numbers (2026-09-30)
- Price HK$641 (+452%, 5.5x IPO); post-placement market cap ~US$40.1B; **equity value / LTM 2026H1 revenue 191.3x**; vol ~184%.
- H1 2026 revenue RMB953.9M (+399.7%); open platform/API 86.5% of revenue and 24.6% gross margin; operating loss widened to RMB2.15B and adjusted net loss widened 12.1%.
- The results announcement was released at 18:56 after the 31-Aug close; the same-day +9.63% return predates disclosure and overlaps an MSCI closing rebalance.
- Layered comps: private-lab transaction range **20.5-39.0x** (median **34.1x**) is the only peer range used in the football field; MiniMax, Hong Kong adjacent names, and commercialization references remain display-only context.
- DCF (US$700M FY2026E revenue, -100% initial margin, US$6.293B pro forma net cash, NOL carryforward): bear/base/bull HK$56/102/255; probability-weighted **HK$116 (~18.1% of price)**.
- Reverse DCF: price implies **~US$47.9B revenue by 2035 (~59.9% annual, 2026-2035)** after fixing the FY2026E base. Sensitivity corners are US$14.5B at 10% WACC / 50% terminal margin and US$68.1B at 15% WACC / 40% margin (rounded to 14 and 68 in the appendix).
- Event study (mean-adjusted, `[-20,-6]` estimation window): reaction **+13.7%**, drift **+4.6%** (bimodal);
  peer-adjusted reaction/drift **+15.3% / +16.8%** across five GLM events. The reaction sits at the block-bootstrap null distribution's 99.2nd percentile; drift stays within its 95% interval, so durable drift is not statistically established.

## September 30 integrated evidence
- September 24–30: Zhipu +0.39%, MiniMax −10.32%, Wenge −10.13%; all remain below August 31. The September retreat describes partial unwinding of prior gains, without establishing statistical mean reversion. Financing and product-trust mechanisms remain hypotheses, with no identified causal effects.
- ZCode's pre-cutoff source remains v3.14.3; remediation is not independently reproduced.
- MiniMax's September 29 notice confirms the preview and forthcoming subscription migration; October offers remain prospective.
- Eight sessions follow September 18 evening news: two reaction days and six drift days. The September 24 report has four later sessions. Original August events remain fixed.
- Anthropic: 2027–2036 UFCF, 12% WACC / 3% terminal growth; US$1,950bn revenue-multiple EV versus US$788.3bn DCF EV. This is an illustration of commercialization conditions and valuation methods, not an extra Zhipu target price or empirical validation. IPO targets stay outside completed financing comparables.
- See [September 30 update](UPDATE_2026-09-30.md) and [Anthropic comparison](ANTHROPIC_COMPARISON.md).

## Sourcing policy (granular; primary > news)
Key data cite, via the bibliography:
- **Comparable beta bridge** - `nasdaqsec2026` (60 month-end returns against SPY through 2026-08-31; Nasdaq prices and latest pre-cutoff SEC debt/share disclosures). Auto-generated by `scripts/comps_beta_and_reverse_dcf.py`.
- **Private-lab funding rounds** - `openai2026`, `anthropic2026`, and the older 2025 Mistral transaction mark; transaction values and contemporaneous revenue run-rates are kept distinct from listed-company market caps.
- **Layered valuation comparables** - `data/valuation_comps_input.csv` records source dates and revenue bases; `data/valuation_comps.csv` is the computed audit table. Only OpenAI, Anthropic, and Mistral define the 20.5-39.0x football-field range.
- **HKEX interim / annual reports and exchange quotes** - Zhipu, MiniMax, and Wenge AI repriced to 2026-09-30; SenseTime and PHANCY retain 2026-08-31 market-equity inputs; listed references are shown separately from private transactions.
- **SEC filings and company annual reports** - Palantir, Cloudflare, and Snowflake latest complete fiscal-year revenue; 2026-08-31 market-equity multiples are display only.
- **HKEX prospectus / annual report / interim results / placement announcements** - `prospectus2513`, `annualreport2513`, `interim2026`, `placement2513`, `agm2513`, `prospectus1956`.
- **Official model cards / technical reports** - `glm_modelcard`.
- **Hang Seng Indexes Company announcements** - `hsi2026`.
- **Formal market database** - `tushare2026` (HK daily prices, cross-checked with HKEX).
- **Market data fallback** - Tencent Finance supplies Hong Kong daily bars and Nasdaq supplies US daily bars when Tushare frequency or permission limits bind.
- News media corroborate only; they do not carry the most important numbers.

## Remaining items
1. Optionally extend the event panel with Wenge (Decitron, Yayi) releases for a multi-lab study once dated events are pinned.
2. Validate the expanded revision with `python scripts/validate_outputs.py --ignore-word-limits`; use the default validator when auditing the course word limits.

## Repo
```
paper/        main.tex, refs.bib, beta_bridge_auto.tex, crest_watermark.png, main.pdf
model/        valuation_model.xlsx (live formulas)
eventstudy/   car_robustness.csv, nonparametric_robustness.csv, block_bootstrap_summary.csv, block_bootstrap_distribution.csv, base_projection.csv, zhipu_car.csv, reverse_dcf_sensitivity.csv
figures/      fig1-11
data/         Zhipu_/MiniMax_/WengeAI_daily.csv, zhipu_financials_input.csv, minimax_financials_input.csv, price_summary.csv, valuation_comps_input.csv, valuation_comps.csv
scripts/      rebuild_outputs.py, validate_outputs.py, comps_beta_and_reverse_dcf.py
DATA_TABLES.md, EVENT_STUDY.md, README.md, LICENSE
```
