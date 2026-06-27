# Paper Map & Status — Zhipu AI (2513.HK) Valuation + Capability-Surprise Event Study

**Title:** *Capability Surprise as the Pricing Mechanism of an Early-Commercial-Stage Foundation-Model Lab:
How Model-Release and Benchmark Events Drive Price Discovery and Drift (Zhipu AI, 2513.HK).*
**Author:** Zhesheng Xu（许哲圣）· 42353012 · 公司金融（英）· 2025-2026-2.
**Build:** XeLaTeX (`paper/main.tex` → `main.pdf`, 12 pp). **Data as of 2026-06-26.**

> Term-paper rules satisfied: title carries core concept (*capability surprise*) + mechanism (price discovery
> & drift); abstract ~165 words (limit 400); main body ~2,095 words (limit 3,000); full reference list at end.

---

## Structure (current)

| § | Section | Role | Key content |
|---|---|---|---|
| Cover | SWUFE official template | — | 西南财经大学本科考试 / 课程论文, official crest watermark |
| 0 | Abstract (≤400w) | — | subject, dual method, headline, takeaway |
| 1 | Introduction | setup | 3 research questions; capability-surprise reframing |
| 2 | Background: Company, Financials, Listing | **condensed** | open-weight model; 3 financial facts (revenue, gross-margin collapse, negative equity); IPO + re-rating + MiniMax divergence |
| 3 | Industry, Macro, Strategy | **condensed** | Porter + leaderboard cost-disruption; **HK AI-IPO landscape incl. Wenge AI (decision-intelligence, not a comparable)**; macro + flow events |
| 4 | **Valuation** (main line) | **emphasised** | CAPM/WACC; 3-scenario DCF; **reverse DCF**; relative val (MiniMax direct; Wenge excluded); **real options (fundamental vs option value)** |
| 5 | **Capability Surprise: Event Study** (original) | **emphasised** | hypothesis; method; CAR results; **flow vs capability events**; peer-adjusted robustness; honesty box |
| 6 | Conclusion | — | capability momentum priced as option; preliminary PCAD |
| A | Appendix: Financial Statements | reproducibility | income statement + balance sheet (RMB) |
| B | Appendix: Base-Case DCF Projection | reproducibility | full 10-yr chain: Revenue→Growth→EBIT margin→NOPAT→Reinvest→FCFF→TV→Equity→per share |

## Four unique points (kept central, per supervisor feedback)
1. **Capability Surprise** — title + conclusion centre, not a side analysis.
2. **Reverse DCF** — "what must the company achieve to justify the price."
3. **Fundamental value vs option value** — not "above DCF ⇒ bubble," but a right-tail option.
4. **Capability vs flow catalysts** — model releases separated from index/Stock-Connect flows.

## Headline numbers (2026-06-26)
- Price HK$2,046 (~+1,660%, ~17×); mcap ~US$114B; **P/S ~570×**; vol ~193%.
- DCF: bear/base/bull HK$29/46/84; prob-weighted **HK$47 (~2% of price)**.
- Reverse DCF: price implies **~US$100B revenue by 2035 (~100% CAGR)**.
- Event study (mean-adj): reaction **+17.8%**, drift **+1.5%** (bimodal); peer-adj drift **+19.2%**.
  GLM-5.2 drift window **truncated** (7/9 days) — provisional.

## Sourcing policy (granular; primary > news)
Key data cite, via the bibliography (not just footnotes):
- **HKEX prospectus / announcements** — `prospectus2513`, `prospectus1956` (offering terms, financials, market share).
- **Official model cards / technical reports** — `glm_modelcard` (architecture, benchmarks).
- **Hang Seng Indexes Company announcements** — `hsi2026` (index inclusion / flows).
- **Formal market database** — `tushare2026` (HK daily prices, cross-checked with HKEX).
- **Academic** — Ball–Brown, Bernard–Thomas, Fama, MacKinlay, Black–Scholes, Damodaran, Guosen (2020).
News media corroborate only; they do not carry the most important numbers.

## TODO — data refresh after 2026-07-03 close (user will supply)
1. Re-pull `hk_daily` for 2513/00100/01956 through 2026-07-03; rerun `recompute.py` → new prices, vol, CAR, figures.
2. **GLM-5.2 drift window completes** (≥+10 trading days from 06-15): remove the "truncated/provisional" caveat once full.
3. Update market row in Table~\ref{tab:dcf} (price/mcap/P/S) and reverse-DCF target.
4. Re-export `model/valuation_model.xlsx` Summary; refresh README headline numbers.
5. Optionally extend the event panel with MiniMax / Wenge (Decitron, Yayi) releases for a multi-lab study.

## Repo
```
paper/        main.tex, refs.bib (12 refs), crest_watermark.png, main.pdf
42353012_许哲圣_*.pdf   submission copy
model/        valuation_model.xlsx (live formulas)
eventstudy/   car_robustness.csv, base_projection.csv, zhipu_car.csv
figures/      fig1-4 (regenerated 2026-06-26)
data/         Zhipu_/MiniMax_/WengeAI_daily.csv, price_summary.csv
DATA_TABLES.md, EVENT_STUDY.md, README.md, LICENSE
```
