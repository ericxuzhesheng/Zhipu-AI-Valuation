# Data Tables - Zhipu (2513.HK), MiniMax (00100.HK), Wenge AI (01956.HK)

Market data via **Tushare `hk_daily`** with public-source fallback/cross-checks from **Tencent Finance** (Hong Kong) and **Nasdaq / Yahoo Finance** (US), **as of 2026-09-18** (CSV in `data/`).
All 11 market series end on 2026-09-18. Information cutoff includes that evening. Completed financing, product-trust events and data provenance are documented in [the weekly note](UPDATE_2026-09-18.md). Wenge H1 inputs remain in `data/wenge_financials_input.csv`.
Fundamentals come from the **HKEX Chapter-18C prospectus**, **2025 Annual Report**, and **H1 2026 interim-results announcement** (stock code 2513). All figures are consistent with the paper and `data/zhipu_financials_input.csv`.

---

## Table D1 - Company & IPO Snapshot

| Item | Zhipu (Knowledge Atlas) | MiniMax | Wenge AI |
|---|---|---|---|
| HKEX ticker | 2513.HK | 00100.HK | 01956.HK |
| Listing date | 2026-01-08 | 2026-01-09 | 2026-06-26 |
| Listing regime | Chapter 18C | Chapter 18C | Main Board |
| IPO price | HK$116.20 | HK$165.00 | HK$60.70 |
| Gross proceeds | ~HK$6.4B before / ~HK$5.0B after over-allotment | ~HK$4.8B (US$620M) | n/a |
| IPO valuation | ~US$6.7-7.4B | ~US$6.5B | ~HK$10.5B (~US$1.3B) |
| HQ / founded | Beijing, 2019 (Tsinghua KEG) | Shanghai, 2021 | Beijing, 2017 (CAS Inst. of Automation) |
| Positioning | general foundation-model lab | general/multimodal foundation lab | enterprise decision-intelligence (DIOS/Decitron/Yayi) |

## Table D2 - Market Performance (IPO to 2026-09-18)

| Metric | Zhipu | MiniMax | Wenge AI |
|---|---|---|---|
| IPO price (HK$) | 116.20 | 165.00 | 60.70 |
| Day-1 close (HK$) | 131.5 | 345.0 (+109%) | 111.7 (+84%) |
| Latest close (HK$) | 780.0 (2026-09-18) | 303.0 (2026-09-18) | 79.7 (2026-09-18) |
| Return vs IPO | **+571% (~6.7x)** | +84% | +31% |
| Period high / low (close) | 2,410.0 / 131.5 | 1,238.0 / 193.1 | 111.7 / 60.0 |
| Latest market cap | **~HK$380.3B (~US$48.8B)** | ~HK$105.8B (~US$13.57B) | ~RMB12.0B (~US$1.69B) |
| Equity value / revenue | **232.8x (LTM 2026H1)** | 82.1x (LTM 2026H1) | 26.2x (LTM 2026H1; different model) |

See [September update](UPDATE_2026-09-18.md) for carried-forward share counts and dated reference inputs.

## Table D3 - Layered Valuation Comparables

The cohorts are deliberately separated because private funding marks, listed-company market caps, and revenue periods are not mechanically interchangeable. Only the private-lab transaction range is used in the relative-valuation football field; the listed cohorts are display-only context.

| Cohort | Company | Equity-value / revenue | Measurement basis | Use in valuation |
|---|---|---:|---|---|
| Core frontier labs | Zhipu | **232.8x** | 2026-09-18 market equity value / LTM 2026H1 revenue | subject company; same listed-peer denominator rule as MiniMax |
| Core frontier labs | MiniMax | 82.1x | 2026-09-18 market equity value / LTM 2026H1 revenue | direct listed cross-check; not in private-round range |
| Core frontier labs | OpenAI | 34.1x | 2026 financing-round value / 2026 revenue run-rate | primary private transaction |
| Core frontier labs | Anthropic | 20.5x | 2026 financing-round value / 2026 revenue run-rate | primary private transaction |
| Core frontier labs | Mistral | 39.0x | older 2025 financing mark / contemporaneous revenue estimate | secondary private transaction |
| Hong Kong adjacent | SenseTime | 9.4x | 2026-08-31 market equity value / LTM 2026H1 revenue | display only |
| Hong Kong adjacent | PHANCY | 1.6x | 2026-08-31 market equity value / LTM 2026H1 revenue | display only |
| Hong Kong adjacent | Wenge AI | 26.2x | 2026-09-18 market equity value / LTM 2026H1 revenue | display only |
| Commercialization reference | Palantir | 100.1x | 2026-08-31 market equity value / latest complete fiscal-year revenue | display only |
| Commercialization reference | Cloudflare | 49.9x | 2026-08-31 market equity value / latest complete fiscal-year revenue | display only |
| Commercialization reference | Snowflake | 24.5x | 2026-08-31 market equity value / latest complete fiscal-year revenue | display only |

Private-lab transaction range: **20.5-39.0x**, median **34.1x** (OpenAI, Anthropic, Mistral). MiniMax, the Hong Kong adjacent group, and the commercialization references are shown to explain market context, not pooled into that range.

## Table D4 - Risk / Volatility

| Metric | Zhipu | MiniMax |
|---|---|---|
| Annualized volatility (daily x sqrt(252)) | **~187%** | ~151% |
| Pattern | peaked ~HK$2,410; latest HK$780 | boom-bust (peaked 1,238; latest 303.0) |
| Beta | bottom-up/comparable **beta ~= 1.6** (60 monthly returns vs SPY through 2026-08-31; 1.55 unlevered median rounded with an early-stage buffer) |

## Table D5 - Fundamentals (Zhipu, from prospectus, annual report, and interim results; RMB unless noted)

| Period | Revenue | Gross margin | Net loss |
|---|---|---|---|
| FY2022 | RMB 57.4M | total 54.6%; cloud 76.1% | RMB 143.7M |
| FY2023 | RMB 124.5M | total 64.6%; cloud 31.0% | RMB 788.0M |
| FY2024 | RMB 312.4M (~US$44M) | total 56.3%; cloud 3.4% | RMB 2,958M |
| FY2025 | RMB 724.3M (~US$102M) | total 41.0%; cloud 18.9% | RMB 4,718M |
| H1 2025 | RMB 190.9M | total 50.0%; API/cloud −0.4% | RMB 2,357.9M; adjusted RMB 1,752.0M |
| H1 2026 | **RMB 953.9M (+399.7%)** | total 26.4%; API/cloud 24.6% | RMB 2,072.0M; adjusted **RMB 1,963.9M** |
| LTM through 2026H1 | **RMB 1,487.3M (~US$209.5M)** | n/a | n/a |
| FY2026E | **US$700M (RMB 4.97B)** | model assumption; 2026E operating margin −100% | n/a |

Balance sheet @ 30-Jun-2026: cash RMB 3,993.7M, short-term FVPL investments RMB 506.1M, bank loans RMB 2,224.8M, lease liabilities RMB 379.4M, and positive equity RMB 4,429.6M. The 13-Jul placement added 19.78M shares and HK$31,374.95M of net proceeds after the reporting date. The September placement then raises shares to 487.58809M. Adding its net proceeds and bond net proceeds, less the issue-date bond principal proxy, gives US$6,307.8M pro forma net cash. This excludes undisclosed subsequent cash burn; see the weekly note for the approximation and financing sources.

**Implied market equity value / LTM revenue = 232.8x** (US$48.8B / US$209.5M). The LTM denominator is FY2025 revenue less H1 2025 plus H1 2026, translated at RMB7.1/US$. The US$700M FY2026E estimate remains a DCF assumption and no longer enters the listed-company trading-multiple comparison.

### MiniMax H1 2026 peer financials (USD, unless noted)

| Metric | H1 2026 | H1 2025 | Change |
|---|---:|---:|---:|
| Revenue | US$116.6M | US$30.4M | +283.1% |
| Gross profit | US$20.8M | US$3.7M | +464.8% |
| Gross margin | 17.9% | 12.1% | +5.8ppt |
| AI-native products revenue | US$42.6M | US$21.2M | +100.9% |
| Open Platform and enterprise-service revenue | US$73.9M (63.4%) | US$9.2M (30.3%) | +703.1% |
| R&D expense | US$296.9M | US$124.3M | +138.8% |
| Net loss | US$358.0M | US$402.2M | narrowed 11.0% |
| Adjusted net loss | US$293.0M | US$138.7M | widened 111.2% |

MiniMax reported a 30-Jun-2026 cash balance of US$1,322.8M and bank borrowings of US$133.6M. Its US$165.2M LTM revenue denominator is FY2025 revenue US$79.0M less H1 2025 US$30.4M plus H1 2026 US$116.6M. The 26-Aug announcement was released after the close; the next trading day is catalogued as a financial-disclosure event, but the full [+2,+10] window was unavailable at the original August 31 cutoff; the September supplement now reports it. Source and row-level figures are retained in `data/minimax_financials_input.csv`.

## Table D6 - Product / Competitive Data (leaderboard thread)

| Item | Detail |
|---|---|
| GLM-4.6 | ~355B params / 32B active (MoE), 200K context, open-weight |
| GLM-5 family (2026) | GLM-5 (02-11), GLM-5-Turbo (03-16), GLM-5.1 (04-08), GLM-5.2 (06-15 trading day), GLM-5.3 (08-14), GLM-5.3-Flash (08-26) |
| GLM-5.1 | #1 SWE-Bench Pro (58.4%); within ~2.6 pts of leading closed model |
| GLM-5.2 | MIT open weights, 1M-token context, at unchanged pricing |
| Pricing power | 8-17% API price rises with each GLM-5.x release |
| Strategy | open-weight + low token price = cost-disruption / developer flywheel |

## Table D7 - Capability-Event CAR (mean-adjusted, through 2026-09-18)

| Event | Day 0 | React [0,+1] | Drift [+2,+10] | Note |
|---|---|---:|---:|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | -19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | -14.2% | over-reaction (flips +12.9% peer-adj) |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | strong under-reaction |
| GLM-5.3 | 2026-08-14 | -6.5% | +3.8% | anticipated; +2.4% / +1.8% peer-adjusted |
| MiniMax M2.5 | 2026-02-12 | +24.2% | -2.1% | positive launch reaction; little subsequent drift |
| MiniMax M2.7 | 2026-03-18 | -5.5% | -49.1% | muted / de-rate |
| MiniMax M3 | 2026-06-01 | -21.1% | -40.8% | failed catalyst / de-rate |
| **Avg (5 GLM)** | | **+13.7%** | **+4.6%** | peer-adj: +15.3% / +16.8% |

Mean-adjusted abnormal return: `AR_t = R_t - average(R[-20,-6])`, where the average is the raw return over event days -20 through -6.
GLM-5.2 and GLM-5.3 both have complete nine-day [+2,+10] windows as of 2026-09-18. Non-capability spikes:
02-20 (+43%), 05-13 (+37%) = Hang Seng Tech inclusion / Stock Connect flow events.

## Table D8 - July-August additions to the large-tech comparator panel

| Event | Day 0 | React [0,+1] | Drift [+2,+10] | Reading |
|---|---|---:|---:|---|
| Tencent Hy3 | 2026-07-06 | +8.2% | +9.8% | under-reaction |
| Meta Muse Spark 1.1 | 2026-07-09 | +14.9% | -7.6% | reversal |
| Google Gemini 3.6 Flash | 2026-07-21 | -2.3% | +13.0% | delayed reaction |
| Alibaba Qwen3.8-Max | 2026-08-03 | +5.3% | -12.8% | reversal |
| Google Gemini 3.7 Flash | 2026-08-13 | +0.9% | -0.7% | muted |
| **Average (16 large-tech events, full panel)** | | **+2.3%** | **-3.0%** | issuer-level listed-equity evidence |

### Screened but not in core CAR

| Event group | Treatment | Reason |
|---|---|---|
| Zhipu GLM-Image / GLM-4.7-Flash / GLM-OCR | catalog only | no clean pre-event estimation window after IPO |
| Zhipu GLM-5V-Turbo | catalog only | multimodal branch; drift window overlaps GLM-5.1 |
| Zhipu GLM-5.3-Flash | catalog only | 08-26 release has only three post-event trading days by the cutoff |
| Zhipu H1 2026 results | financial-disclosure catalog only | released at 18:56 after the 08-31 close; no post-announcement price window by the cutoff |
| Zhipu MSCI inclusion | flow catalog only | effective after the 08-31 close; same-day closing flow may be visible, but no post-event window exists by the cutoff |
| Zhipu ZCode IDE | catalog only | product launch outside the core foundation-model capability set |
| MiniMax H3 / Speech / Music releases | catalog only | dated official releases, but audio-video/music/speech outputs are not comparable with the text-agent peer set |
| MiniMax H1 2026 results | financial-disclosure catalog only | released after the 08-26 close; full post-event window is unavailable by 08-31 |
| OpenAI and xAI releases | catalog only | Microsoft and Tesla are not the model issuers; their share returns are excluded rather than treated as issuer proxies |
| Alibaba Qwen3.8 open-weight variants / Qwen3.8-Flash | catalog only | same release cluster as Qwen3.8-Max; Flash also lacks a full post-event window |
| Tencent Hy4 preview | catalog only | 08-28 release lacks a full post-event window |
| Google Gemini Transcribe / Omni 1.1 | catalog only | vertical models released 08-26/27 and lack full post-event windows |

## Remaining / refresh items
1. Expand `data/event_catalog_input.csv` as Wenge/Moonshot/Kimi obtain dated model events and enough listed-price history; `eventstudy/event_catalog.csv` and `eventstudy/event_panel.csv` are generated from that input. The catalog now has 62 rows and the computable CAR panel has n=29, including three MiniMax text/agent releases and 16 issuer-level large-tech releases.

---

### Sources (priority: primary > news)
- **HKEX prospectus** (stock code 2513; and 1956 for Wenge) - offering terms, financials, market share.
- **2025 annual report and H1 2026 interim-results announcement** (stock code 2513) - revenue, margins, losses, balance sheet, and disclosure limitations.
- **June monthly return and 13-Jul placement completion announcement** (stock code 2513) - 465,623,090 post-placement shares and HK$31,374.95M net proceeds.
- **HKEX interim / annual reports** (stock codes 00100, 00020, 06682, and 01956) - MiniMax H1 financials, revenue-period construction, and issued-share cross-checks for the Hong Kong peer cohorts.
- **Company financing announcements and primary investor materials** (OpenAI, Anthropic, Mistral) - private transaction values and disclosed or contemporaneous revenue run-rates.
- **SEC filings and company annual reports** (Palantir, Cloudflare, Snowflake) - latest complete fiscal-year revenue for the commercialization-reference cohort.
- **Official model cards / technical reports** (Z.ai; Hugging Face `zai-org/GLM-4.6`) - architecture, benchmarks.
- **Hang Seng Indexes Company** announcements - index inclusion / Stock Connect flows.
- **Tushare `hk_daily`**, with Tencent Finance (Hong Kong), Nasdaq (US), and HKEX day quotes as fallbacks/cross-checks - 2026-09-18 prices and daily series to `data/*.csv`.
- News (Caixin, CNBC, SCMP, Bloomberg, Investing.com) - corroboration only.
