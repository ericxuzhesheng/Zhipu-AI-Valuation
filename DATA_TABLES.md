# Data Tables — Zhipu (2513.HK), MiniMax (00100.HK), Wenge AI (01956.HK)

Market data via **Tushare `hk_daily`** cross-checked with HKEX, **as of 2026-06-26** (CSV in `data/`).
Fundamentals from the **HKEX Chapter-18C prospectus** (stock code 2513). All figures consistent with the paper.

---

## Table D1 — Company & IPO Snapshot

| Item | Zhipu (Knowledge Atlas) | MiniMax | Wenge AI (中科闻歌) |
|---|---|---|---|
| HKEX ticker | 2513.HK | 00100.HK | 01956.HK |
| Listing date | 2026-01-08 | 2026-01-09 | 2026-06-26 |
| Listing regime | Chapter 18C | Chapter 18C | Main Board |
| IPO price | HK$116.20 | HK$165.00 | HK$60.70 |
| Gross proceeds | ~HK$4.3B | ~HK$4.8B (US$620M) | — |
| IPO valuation | ~US$6.7–7.4B | ~US$6.5B | ~HK$10.5B (~US$1.3B) |
| HQ / founded | Beijing, 2019 (Tsinghua KEG) | Shanghai, 2021 | Beijing, 2017 (CAS Inst. of Automation) |
| Positioning | general foundation-model lab | general/multimodal foundation lab | enterprise decision-intelligence (DIOS/Decitron/Yayi) |

## Table D2 — Market Performance (IPO → 2026-06-26)

| Metric | Zhipu | MiniMax | Wenge AI |
|---|---|---|---|
| IPO price (HK$) | 116.20 | 165.00 | 60.70 |
| Day-1 close (HK$) | 131.5 | 345.0 (+109%) | 111.7 (+84%) |
| Latest close 2026-06-26 (HK$) | 2,046.0 | 427.0 | 111.7 |
| Return vs IPO | **+1,661% (~17×)** | +159% | +84% |
| Period high / low (close) | 2,410 / 131.5 | 1,238 / 345 | — (1 day) |
| Latest market cap | **~HK$890B (~US$114B)** | ~HK$130B (~US$17B) | ~HK$10.5B |
| P/S (FY26E US$200M) | **~570×** | far lower than Zhipu | n/a (different model) |

## Table D3 — Risk / Volatility

| Metric | Zhipu | MiniMax |
|---|---|---|
| Annualized volatility (daily ×√252) | **~193%** | ~155% |
| Pattern | re-rating, pulled back 6/26 (−13%) | boom-bust (peaked 1,238 → ~427) |
| Beta | bottom-up/comparable **β ≈ 1.6** (HK index not in feed; global AI-software comps, unlever→relever) |

## Table D4 — Fundamentals (Zhipu, from prospectus; RMB unless noted)

| Period | Revenue | Gross margin | Net loss |
|---|---|---|---|
| FY2022 | — | 76.1% | — |
| FY2024 | RMB 312.4M (~US$44M) | 3.4% | RMB 2,958M |
| H1 2025 | RMB ~190 (cash 190.9M) | −0.4% | — |
| FY2025 | RMB 724.3M (~US$102M, +132%) | ~0% | ~RMB 4,700M (+237%) |
| FY2026E | ~US$200M | — | — |

Balance sheet @ 30-Jun-2025: net liabilities **−RMB 6,150.8M** (negative equity), net current liabilities
−RMB 9,564.8M, cash RMB 190.9M. Shares outstanding ~435M. FX: HK$7.8/US$, RMB 7.1/US$.
**Implied market P/S ≈ 570× FY26E** (US$114B / US$200M).

## Table D5 — Product / Competitive Data (leaderboard thread)

| Item | Detail |
|---|---|
| GLM-4.6 | ~355B params / 32B active (MoE), 200K context, open-weight |
| GLM-5 family (2026) | GLM-5 (02-11), GLM-5-Turbo (03-15), GLM-5.1 (~04-07/08), GLM-5.2 (06-13) |
| GLM-5.1 | #1 SWE-Bench Pro (58.4%); within ~2.6 pts of leading closed model |
| GLM-5.2 | MIT open weights, 1M-token context, at unchanged pricing |
| Pricing power | 8–17% API price rises with each GLM-5.x release |
| Strategy | open-weight + low token price = cost-disruption / developer flywheel |

## Table D6 — Capability-Event CAR (mean-adjusted, through 2026-06-26)

| Event | Day 0 | React [0,+1] | Drift [+2,+10] | Note |
|---|---|---:|---:|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | −19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | −14.2% | over-reaction (flips +12.9% peer-adj) |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2%† | strong under-reaction |
| MiniMax M2.7 | 2026-03-18 | −5.5% | −49.1% | muted / de-rate |
| **Avg (4 GLM)** | | **+18.7%** | **+4.8%†** | peer-adj: +18.5% / +19.2% |

† GLM-5.2 drift window truncated (7/9 days through 06-26) — provisional. Non-capability spikes: 02-20 (+43%),
05-13 (+37%) = Hang Seng Tech inclusion / Stock Connect flow events.

## Remaining / refresh items
1. After **2026-07-03 close**: re-pull prices, rerun `recompute.py`; GLM-5.2 window completes (drop the † caveat).
2. MiniMax / Wenge absolute financials for a multi-lab event panel (extension, not required).

---

### Sources (priority: primary > news)
- **HKEX prospectus** (stock code 2513; and 1956 for Wenge) — offering terms, financials, market share.
- **Official model cards / technical reports** (Z.ai; Hugging Face `zai-org/GLM-4.6`) — architecture, benchmarks.
- **Hang Seng Indexes Company** announcements — index inclusion / Stock Connect flows.
- **Tushare `hk_daily`** (cross-checked with HKEX) — daily prices → `data/*.csv`.
- News (Caixin, CNBC, SCMP, Bloomberg, Investing.com) — corroboration only.
