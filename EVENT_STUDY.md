# Capability Surprise, Not Earnings Surprise
### An event-driven read of how the market prices an early-commercial-stage AI lab (Zhipu, 2513.HK)

> Core market data as of **2026-07-17**. A foundation-model lab has **no earnings to be surprised by**. So we replace the
> classic *earnings* surprise with a **capability surprise** - a model release or benchmark-leaderboard jump - and ask the only question that matters for market efficiency: *does the price react once and stop, or does it
> keep drifting?* This is the AI analogue of post-earnings-announcement drift (PEAD) to **PCAD**.
>
> Method: mean-adjusted abnormal returns (`AR_t = R_t - average(R[-20,-6])`, where the average is the raw return
> over event days -20 through -6) on market prices through 2026-07-17; three windows:
> leakage `[-5,-1]`, reaction `[0,+1]`, drift `[+2,+10]`; robustness via peer-adjustment (benchmark = MiniMax).

---

## 1. Independently dated events, with prices as a descriptive cross-check
Event dates are taken from **official GLM release announcements**, not inferred from the price series. As a
*descriptive* cross-check, several of Zhipu's largest abnormal up-days coincide with these independently dated
events:

| Data-found spike | Daily ret | Matches |
|---|---:|---|
| 2026-02-09 to 02-11 | +36% | **GLM-5** launch |
| 2026-04-01 | +32% | run-up *into* **GLM-5.1** (leakage) |
| 2026-06-15 | +33% | **GLM-5.2** launch (first trading day after 06-13) |
| 2026-02-20 / 05-13 | +43% / +37% | **non-capability: index/flow** (Hang Seng Tech inclusion + Stock Connect anticipation) |

The two flow-driven spikes are themselves a finding: not every move is capability; some is index/liquidity.
See `figures/fig2_daily_returns.png`.

![Daily returns](figures/fig2_daily_returns.png)

## 2. Reaction is loud; drift is where efficiency breaks
Average CAR across the four GLM events (mean-adjusted):

| Window | Avg CAR | Read |
|---|---:|---|
| Leakage `[-5,-1]` | small | no systematic front-running |
| Reaction `[0,+1]` | **+18.7%** | market *does* price capability, fast |
| Drift `[+2,+10]` | **+4.8%** (bimodal) | sign depends on release type; see below |

![Average CAR](figures/fig3_car_eventtime.png)
![Reaction vs drift](figures/fig4_reaction_vs_drift.png)

## 3. Three cases
- **GLM-5.2 (06-15) - under-reaction / momentum.** +30.8% reaction and **+28.2% further drift** across the
  complete nine-trading-day `[+2,+10]` window. A genuine SOTA jump (MIT open weights, 1M context) kept re-rating.
- **GLM-5.1 (04-08) - over-reaction / reversal.** +13.8% reaction then **-14.2% drift**: an *incremental*
  upgrade was "buy the rumor, sell the news"; see the peer-adjusted result in Section 5.
- **MiniMax M2.7 / M3 - the cross-section test.** M2.7 had a -5.5% reaction and -49.1% drift; M3 had a
  -21.1% reaction and -40.8% drift. MiniMax de-rated while Zhipu kept climbing (`fig1`). Same sector, opposite paths: **capability surprise, not
  sector beta, drives the cross-section.**

![Price paths](figures/fig1_price_paths.png)

## 4. Verdict
The market is **neither efficient nor a blind bubble**. It prices capability *immediately and discriminately*
(separating Zhipu from MiniMax on model quality, not sector) but **mis-times magnitude**: under-reacting to
true SOTA leaps, over-reacting to incremental ones. The **~10x / ~316x equity-value-to-revenue** re-rating is best read as
**capability momentum priced as an option**. The fundamental anchor (DCF + real options) tells you *the level*;
the event study tells you *how price gets there*.

## 5. Robustness & honesty box
- **Peer-adjusted** (benchmark = MiniMax): reaction robust (**+18.7% to +18.5%**); average drift **strengthens
  to +20.5%** once the falling sector is removed. GLM-5.1's reversal flips to continuation (-14.2% to +12.9%).
  The under-reaction/PCAD pattern is reinforced, not weakened.
- **Expanded event panel framework:** `data/event_catalog_input.csv` tracks Zhipu capability events,
  Zhipu screened-but-excluded model releases, Zhipu index/flow catalysts, MiniMax M2.7/M3, MiniMax vertical
  audio/music releases, listing events, and candidate Wenge/Moonshot/Kimi events. Only events with day-level
  dating, enough local post-listing price history and a clean event window enter the generated
  `eventstudy/event_panel.csv`; excluded candidates carry an explicit reason instead of being forced into the
  statistics.
- **Preliminary, diagnostic** evidence consistent with PCAD, *not* a proven anomaly: n = 4 single-firm events
  (+2 peer) over ~5 months, and windows can overlap a fast release cadence or competing-lab news.
  No statistical significance is claimed.
- Extensions: multi-lab panel (MiniMax, Wenge releases), NLP-scored surprise magnitude.

*Inputs: market prices through 2026-07-17 for the core Zhipu/MiniMax series in `data/`; CAR tables to `eventstudy/car_robustness.csv`; charts to `figures/`.*
