# Data Tables - Zhipu (2513.HK), MiniMax (00100.HK), Wenge AI (01956.HK)

Market data via **Tushare `hk_daily`** with public-source fallback/cross-checks from **Tencent Finance** (Hong Kong) and **Nasdaq** (US), **as of 2026-08-31** (CSV in `data/`).
The two core event-study series now cover the latest available Hong Kong trading day, 2026-08-31.
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

## Table D2 - Market Performance (IPO to 2026-08-31)

| Metric | Zhipu | MiniMax | Wenge AI |
|---|---|---|---|
| IPO price (HK$) | 116.20 | 165.00 | 60.70 |
| Day-1 close (HK$) | 131.5 | 345.0 (+109%) | 111.7 (+84%) |
| Latest close (HK$) | 1195.0 (2026-08-31) | 349.0 (2026-08-31) | 86.0 (2026-08-31) |
| Return vs IPO | **+928% (~10.3x)** | +112% | +42% |
| Period high / low (close) | 2,410.0 / 131.5 | 1,238.0 / 193.1 | 111.7 / 60.0 |
| Latest market cap | **~HK$532.8B (~US$68.3B)** | ~HK$104.9B (~US$13.45B) | ~HK$15.3B (~US$1.96B) |
| Equity value / revenue | **311.5x (FY26E)** | 81.4x (LTM 2026H1) | 28.8x (LTM 2026H1; different model) |

## Table D3 - Layered Valuation Comparables

The cohorts are deliberately separated because private funding marks, listed-company market caps, and revenue periods are not mechanically interchangeable. Only the private-lab transaction range is used in the relative-valuation football field; the listed cohorts are display-only context.

| Cohort | Company | Equity-value / revenue | Measurement basis | Use in valuation |
|---|---|---:|---|---|
| Core frontier labs | Zhipu | **311.5x** | 2026-08-28 market equity value / FY2026E revenue | subject company; not in peer median |
| Core frontier labs | MiniMax | 81.4x | 2026-08-28 market equity value / LTM 2026H1 revenue | direct listed cross-check; not in private-round range |
| Core frontier labs | OpenAI | 34.1x | 2026 financing-round value / 2026 revenue run-rate | primary private transaction |
| Core frontier labs | Anthropic | 20.5x | 2026 financing-round value / 2026 revenue run-rate | primary private transaction |
| Core frontier labs | Mistral | 39.0x | older 2025 financing mark / contemporaneous revenue estimate | secondary private transaction |
| Hong Kong adjacent | SenseTime | 9.7x | 2026-08-28 market equity value / LTM 2026H1 revenue | display only |
| Hong Kong adjacent | PHANCY | 1.6x | 2026-08-28 market equity value / LTM 2026H1 revenue | display only |
| Hong Kong adjacent | Wenge AI | 28.8x | 2026-08-28 market equity value / LTM 2026H1 revenue | display only |
| Commercialization reference | Palantir | 100.0x | 2026-08-28 market equity value / latest complete fiscal-year revenue | display only |
| Commercialization reference | Cloudflare | 49.1x | 2026-08-28 market equity value / latest complete fiscal-year revenue | display only |
| Commercialization reference | Snowflake | 24.3x | 2026-08-28 market equity value / latest complete fiscal-year revenue | display only |

Private-lab transaction range: **20.5-39.0x**, median **34.1x** (OpenAI, Anthropic, Mistral). MiniMax, the Hong Kong adjacent group, and the commercialization references are shown to explain market context, not pooled into that range.

## Table D4 - Risk / Volatility

| Metric | Zhipu | MiniMax |
|---|---|---|
| Annualized volatility (daily x sqrt(252)) | **~192%** | ~155% |
| Pattern | peaked ~HK$2,410 then pulled back to HK$1,090 | boom-bust (peaked 1,238; latest 300.4) |
| Beta | bottom-up/comparable **beta ~= 1.6** (HK index not in feed; global AI-software comps, unlever-to-relever) |

## Table D5 - Fundamentals (Zhipu, from prospectus and annual report; RMB unless noted)

| Period | Revenue | Gross margin | Net loss |
|---|---|---|---|
| FY2022 | RMB 57.4M | total 54.6%; cloud 76.1% | RMB 143.7M |
| FY2023 | RMB 124.5M | total 64.6%; cloud 31.0% | RMB 788.0M |
| FY2024 | RMB 312.4M (~US$44M) | total 56.3%; cloud 3.4% | RMB 2,958M |
| FY2025 | RMB 724.3M (~US$102M) | total 41.0%; cloud 18.9% | RMB 4,718M |
| FY2026E | ~US$200M | model assumption | n/a |

Balance sheet @ 31-Dec-2025: net liabilities **-RMB 8,111.0M** (negative equity), net current liabilities
**-RMB 8,834.8M**, cash and cash equivalents RMB 2,259.1M. Shares outstanding ~445.8M (per AGM circular 2026-06-22). FX: HK$7.8/US$, RMB 7.1/US$.
**Implied market equity value / revenue = 311.5x FY26E** (US$62.3B / US$200M).

## Table D6 - Product / Competitive Data (leaderboard thread)

| Item | Detail |
|---|---|
| GLM-4.6 | ~355B params / 32B active (MoE), 200K context, open-weight |
| GLM-5 family (2026) | GLM-5 (02-11), GLM-5-Turbo (03-16), GLM-5.1 (04-08), GLM-5.2 (06-15 trading day), GLM-5.3 (08-14), GLM-5.3-Flash (08-26) |
| GLM-5.1 | #1 SWE-Bench Pro (58.4%); within ~2.6 pts of leading closed model |
| GLM-5.2 | MIT open weights, 1M-token context, at unchanged pricing |
| Pricing power | 8-17% API price rises with each GLM-5.x release |
| Strategy | open-weight + low token price = cost-disruption / developer flywheel |

## Table D7 - Capability-Event CAR (mean-adjusted, through 2026-08-31)

| Event | Day 0 | React [0,+1] | Drift [+2,+10] | Note |
|---|---|---:|---:|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | -19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | -14.2% | over-reaction (flips +12.9% peer-adj) |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | strong under-reaction |
| GLM-5.3 | 2026-08-14 | -6.5% | +3.8% | anticipated; +2.4% / +1.8% peer-adjusted |
| MiniMax M2.7 | 2026-03-18 | -5.5% | -49.1% | muted / de-rate |
| MiniMax M3 | 2026-06-01 | -21.1% | -40.8% | failed catalyst / de-rate |
| **Avg (5 GLM)** | | **+13.7%** | **+4.6%** | peer-adj: +15.3% / +16.8% |

Mean-adjusted abnormal return: `AR_t = R_t - average(R[-20,-6])`, where the average is the raw return over event days -20 through -6.
GLM-5.2 and GLM-5.3 both have complete nine-day [+2,+10] windows as of 2026-08-31. Non-capability spikes:
02-20 (+43%), 05-13 (+37%) = Hang Seng Tech inclusion / Stock Connect flow events.

### Screened but not in core CAR

| Event group | Treatment | Reason |
|---|---|---|
| Zhipu GLM-Image / GLM-4.7-Flash / GLM-OCR | catalog only | no clean pre-event estimation window after IPO |
| Zhipu GLM-5V-Turbo | catalog only | multimodal branch; drift window overlaps GLM-5.1 |
| Zhipu GLM-5.3-Flash | catalog only | 08-26 release has only two post-event trading days by the cutoff |
| Zhipu ZCode IDE | catalog only | product launch outside the core foundation-model capability set |
| MiniMax M2.5 series | catalog only | month-level date in source screenshot; wait for day-level source |
| MiniMax H3 / Speech / Music releases | catalog only | video/audio/music models, not text-agent peer events |

## Remaining / refresh items
1. Expand `data/event_catalog_input.csv` as Wenge/Moonshot/Kimi obtain dated model events and enough listed-price history; `eventstudy/event_catalog.csv` and `eventstudy/event_panel.csv` are generated from that input, with the current computable CAR panel at n=26.

---

### Sources (priority: primary > news)
- **HKEX prospectus** (stock code 2513; and 1956 for Wenge) - offering terms, financials, market share.
- **2025 annual report** (stock code 2513) - FY2025 revenue, margins, net loss, and balance-sheet data.
- **AGM poll results** (stock code 2513, 2026-06-22) - confirmed total issued shares 445,843,090; all 20 resolutions passed.
- **HKEX interim / annual reports** (stock codes 00100, 00020, 06682, and 01956) - revenue periods and issued-share cross-checks for MiniMax and the Hong Kong adjacent cohort.
- **Company financing announcements and primary investor materials** (OpenAI, Anthropic, Mistral) - private transaction values and disclosed or contemporaneous revenue run-rates.
- **SEC filings and company annual reports** (Palantir, Cloudflare, Snowflake) - latest complete fiscal-year revenue for the commercialization-reference cohort.
- **Official model cards / technical reports** (Z.ai; Hugging Face `zai-org/GLM-4.6`) - architecture, benchmarks.
- **Hang Seng Indexes Company** announcements - index inclusion / Stock Connect flows.
- **Tushare `hk_daily`**, with Tencent Finance (Hong Kong), Nasdaq (US), and public exchange quotes as fallbacks - 2026-08-28 prices and daily series to `data/*.csv`.
- News (Caixin, CNBC, SCMP, Bloomberg, Investing.com) - corroboration only.
