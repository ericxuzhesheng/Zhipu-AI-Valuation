# Data Tables - Zhipu (2513.HK), MiniMax (00100.HK), Wenge AI (01956.HK)

Market data via **Tushare `hk_daily`** cross-checked with HKEX, **as of 2026-06-30** (CSV in `data/`).
Tushare data through 2026-06-29; 2026-06-30 close was manually recorded from East Money close screenshots.
Fundamentals from the **HKEX Chapter-18C prospectus** and **2025 Annual Report** (stock code 2513). All figures are consistent with the paper.

---

## Table D1 - Company & IPO Snapshot

| Item | Zhipu (Knowledge Atlas) | MiniMax | Wenge AI |
|---|---|---|---|
| HKEX ticker | 2513.HK | 00100.HK | 01956.HK |
| Listing date | 2026-01-08 | 2026-01-09 | 2026-06-26 |
| Listing regime | Chapter 18C | Chapter 18C | Main Board |
| IPO price | HK$116.20 | HK$165.00 | HK$60.70 |
| Gross proceeds | ~HK$4.3B | ~HK$4.8B (US$620M) | n/a |
| IPO valuation | ~US$6.7-7.4B | ~US$6.5B | ~HK$10.5B (~US$1.3B) |
| HQ / founded | Beijing, 2019 (Tsinghua KEG) | Shanghai, 2021 | Beijing, 2017 (CAS Inst. of Automation) |
| Positioning | general foundation-model lab | general/multimodal foundation lab | enterprise decision-intelligence (DIOS/Decitron/Yayi) |

## Table D2 - Market Performance (IPO to 2026-06-30)

| Metric | Zhipu | MiniMax | Wenge AI |
|---|---|---|---|
| IPO price (HK$) | 116.20 | 165.00 | 60.70 |
| Day-1 close (HK$) | 131.5 | 345.0 (+109%) | 111.7 (+84%) |
| Latest close 2026-06-30 (HK$) | 2,104.0 | 417.0 | 85.5 |
| Return vs IPO | **+1,711% (~18x)** | +153% | +41% |
| Period high / low (close) | 2,410 / 131.5 | 1,238 / 345 | 111.7 / 85.5 |
| Latest market cap | **~HK$938B (~US$120B)** | ~HK$131B (~US$17B) | ~HK$14.8B |
| Equity value / revenue (FY26E US$200M) | **~601x** | far lower than Zhipu | n/a (different model) |

## Table D3 - Risk / Volatility

| Metric | Zhipu | MiniMax |
|---|---|---|
| Annualized volatility (daily x sqrt(252)) | **~192%** | ~154% |
| Pattern | re-rating resumed on 6/30 (+7.3%) | boom-bust (peaked 1,238 to ~417) |
| Beta | bottom-up/comparable **beta ~= 1.6** (HK index not in feed; global AI-software comps, unlever-to-relever) |

## Table D4 - Fundamentals (Zhipu, from prospectus and annual report; RMB unless noted)

| Period | Revenue | Gross margin | Net loss |
|---|---|---|---|
| FY2022 | RMB 57.4M | total 54.6%; cloud 76.1% | RMB 143.7M |
| FY2023 | RMB 124.5M | total 64.6%; cloud 31.0% | RMB 788.0M |
| FY2024 | RMB 312.4M (~US$44M) | total 56.3%; cloud 3.4% | RMB 2,958M |
| FY2025 | RMB 724.3M (~US$102M) | total 41.0%; cloud 18.9% | RMB 4,718M |
| FY2026E | ~US$200M | model assumption | n/a |

Balance sheet @ 31-Dec-2025: net liabilities **-RMB 8,111.0M** (negative equity), net current liabilities
**-RMB 8,834.8M**, cash and cash equivalents RMB 2,259.1M. Shares outstanding ~445.8M (per AGM circular 2026-06-22). FX: HK$7.8/US$, RMB 7.1/US$.
**Implied market equity value / revenue ~= 601x FY26E** (US$120B / US$200M).

## Table D5 - Product / Competitive Data (leaderboard thread)

| Item | Detail |
|---|---|
| GLM-4.6 | ~355B params / 32B active (MoE), 200K context, open-weight |
| GLM-5 family (2026) | GLM-5 (02-11), GLM-5-Turbo (03-15), GLM-5.1 (~04-07/08), GLM-5.2 (06-13) |
| GLM-5.1 | #1 SWE-Bench Pro (58.4%); within ~2.6 pts of leading closed model |
| GLM-5.2 | MIT open weights, 1M-token context, at unchanged pricing |
| Pricing power | 8-17% API price rises with each GLM-5.x release |
| Strategy | open-weight + low token price = cost-disruption / developer flywheel |

## Table D6 - Capability-Event CAR (mean-adjusted, through 2026-06-30)

| Event | Day 0 | React [0,+1] | Drift [+2,+10] | Note |
|---|---|---:|---:|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | -19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | -14.2% | over-reaction (flips +12.9% peer-adj) |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | strong under-reaction |
| MiniMax M2.7 | 2026-03-18 | -5.5% | -49.1% | muted / de-rate |
| **Avg (4 GLM)** | | **+18.7%** | **+4.8%** | peer-adj: +18.5% / +20.5% |

Mean-adjusted abnormal return: `AR_t = R_t - average(R[-20,-6])`, where the average is the raw return over event days -20 through -6.
GLM-5.2's [+2,+10] window is complete through all 9 trading days as of 2026-06-30. Non-capability spikes:
02-20 (+43%), 05-13 (+37%) = Hang Seng Tech inclusion / Stock Connect flow events.

## Remaining / refresh items
1. Tushare data refreshed through 2026-06-29; 2026-06-30 close still from East Money screenshots (Tushare had not published that day's data at time of writing).
2. Expand `data/event_catalog_input.csv` as Wenge/Moonshot/Kimi obtain dated model events and enough listed-price history; `eventstudy/event_catalog.csv` and `eventstudy/event_panel.csv` are generated from that input, with the current computable CAR panel at n=9.

---

### Sources (priority: primary > news)
- **HKEX prospectus** (stock code 2513; and 1956 for Wenge) - offering terms, financials, market share.
- **2025 annual report** (stock code 2513) - FY2025 revenue, margins, net loss, and balance-sheet data.
- **AGM poll results** (stock code 2513, 2026-06-22) - confirmed total issued shares 445,843,090; all 20 resolutions passed.
- **Official model cards / technical reports** (Z.ai; Hugging Face `zai-org/GLM-4.6`) - architecture, benchmarks.
- **Hang Seng Indexes Company** announcements - index inclusion / Stock Connect flows.
- **Tushare `hk_daily`** (cross-checked with HKEX) - daily prices to `data/*.csv`.
- **East Money screenshots** - manual 2026-06-30 close records pending database refresh.
- News (Caixin, CNBC, SCMP, Bloomberg, Investing.com) - corroboration only.
