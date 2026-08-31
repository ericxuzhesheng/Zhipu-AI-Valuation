# 智谱 AI 估值与能力惊喜事件研究 | Zhipu AI Valuation and Capability-Surprise Event Study

<p align="center">
  <a href="#中文"><img src="https://img.shields.io/badge/语言-中文-E84D3D?style=for-the-badge&labelColor=3B3F47" alt="中文"></a>
  &nbsp;
  <a href="#english"><img src="https://img.shields.io/badge/Language-English-2F73C9?style=for-the-badge&labelColor=3B3F47" alt="English"></a>
</p>

<p align="center">
  <strong>Zhesheng Xu（许哲圣）</strong><br>
  Corporate Finance Final Project<br>
  <strong>核心数据截至 / Core data through</strong> 2026-08-28
</p>

<p align="center">
  <a href="paper/main.pdf"><strong>完整论文 / Paper</strong></a> ·
  <a href="model/valuation_model.xlsx"><strong>估值模型 / Model</strong></a> ·
  <a href="presentation/zhipu_beamer.pdf"><strong>演示文稿 / Slides</strong></a> ·
  <a href="data/valuation_comps.csv"><strong>可比口径 / Comparable Data</strong></a>
</p>

---

## 中文

### 项目概览

这个项目从一个具体的估值难题开始。智谱 AI 于 2026 年 1 月 8 日成为全球首家上市的基础模型公司。到 8 月 28 日，公司市值约为 623 亿美元，相当于 FY2026E 收入的约 312 倍。公司同期仍在深度亏损，净权益为负。这个价格留下了一个可以计算的问题。市场已经为多大的未来增长付了钱。

我先用 CAPM 和 WACC 建立折现率，随后完成三情景 DCF、反向 DCF 与分层可比估值。概率加权 DCF 约为每股 HK$32，2026 年 8 月 28 日市价为 HK$1,090。反向 DCF 把这段差距转成一项经营要求。公司收入需要在 2035 年达到约 710 亿美元，对应 2026 至 2035 年连续九个增长区间约 92% 的年复合增速。

估值结果说明市场预期有多高，事件研究继续考察价格怎样吸收新信息。我把模型发布和榜单跃升定义为“能力惊喜”，独立确定五个 GLM 事件日期，再用 MiniMax 做同业调整。五次事件的原始两日平均反应为 13.7%，同业调整后为 15.3%。

样本只覆盖智谱上市后的前八个月和五个能力事件。本文把结果视为一个本科案例中的诊断性证据，不据此推断普遍的市场异象。完整模型、逐行可比口径、事件结果和重建脚本都保留在仓库中。

### 我完成的工作

| 研究环节 | 具体工作 | 可核查成果 |
|---|---|---|
| 基本面估值 | 建立 CAPM/WACC、三情景 DCF、敏感性分析和反向 DCF | [活公式估值模型](model/valuation_model.xlsx) |
| 相对估值 | 分开基础模型实验室、港股邻近公司与成熟 AI 软件公司，并统一记录估值日和收入口径 | [逐行可比数据](data/valuation_comps.csv) |
| 事件研究 | 独立确定模型发布日期，计算原始与同业调整 CAR，并检查反转、漂移和非能力事件 | [事件研究结果](eventstudy/event_panel_summary.csv) |
| 可复算设计 | 把主要表格、图形和论文构建过程写入脚本，并增加输出校验 | [构建脚本](scripts/build_project.py) · [校验脚本](scripts/validate_outputs.py) |

### 阅读入口

| 阅读时间 | 建议入口 |
|---|---|
| 约 1 分钟 | 继续阅读本页的[估值结论](#估值结论)和[事件研究](#事件研究) |
| 约 10 分钟 | 查看[演示文稿](presentation/zhipu_beamer.pdf) |
| 完整阅读 | 打开[论文 PDF](paper/main.pdf) |
| 核查假设 | 打开[估值模型](model/valuation_model.xlsx)和[数据来源](#数据来源) |

### 研究问题

> 对一家尚无稳定盈利的基础模型公司，怎样建立可解释的估值边界？模型能力信息进入股价后，短窗反应和后续漂移呈现什么特征？

经典事件研究常以“盈余惊喜”为信息事件（Ball 与 Brown，1968；Bernard 与 Thomas，1989）。前沿大模型公司仍在深度亏损，短期盈余很难承载投资者最关心的信息。本文把模型发布和基准榜单跃迁定义为“能力惊喜”，并把国信证券《超预期投资全攻略》（2020）的 CAR 三窗口框架用于这一新资产类别。

### 研究设计

| 研究环节 | 方法 | 研究用途 |
|---|---|---|
| 基本面估值 | CAPM/WACC、三情景 DCF、反向 DCF、可比公司和实物期权 | 给出现金流价值范围，并还原市价隐含的经营路径 |
| 能力事件研究 | GLM-5 至 GLM-5.3 五个事件，以 MiniMax 作同业调整 | 观察模型能力信息进入股价后的即时反应与后续漂移 |

### 估值结论

WACC 约为 13.5%，其中自下而上 β 约为 1.6，Rf 为 4%，ERP 为 6%。模型统一采用 HK$7.8/US$、RMB 7.1/US$ 和约 4.46 亿股。活公式见 [`model/valuation_model.xlsx`](model/valuation_model.xlsx)，十年完整 Base Case 见论文附录 B。

| 情景 | 收入 CAGR 2026 至 2035 | 终期利润率 | 股权价值 | 每股（HK$） |
|---|---|---|---|---|
| 悲观 (p=0.35) | 21% | 18% | $0.7B | 12 |
| 中性 (p=0.45) | 31% | 28% | $1.6B | 27 |
| 乐观 (p=0.20) | 46% | 35% | $4.6B | 80 |
| **概率加权** | N/A | N/A | **$1.9B** | **32** |
| *市价 (2026-08-28)* | N/A | N/A | *$62.3B* | *1,090* |

**反向 DCF** 要支撑现价，需相信 2035 年收入约 **US$710 亿**，对应 2026 至 2035 年约 **92%** 的年复合增速和约 355 倍 FY26E 收入。

**分层可比** MiniMax 按 2026 年 8 月 28 日市值和截至 2026H1 的 LTM 收入重算为 **81.4×**；智谱为 **311.5× FY2026E 收入**。

OpenAI、Anthropic 与 Mistral 的私有交易参照更接近智谱的业务形态，因此它们构成 football field 的核心可比区间。倍数落在 **20.5 至 39.0×**，中位数为 **34.1×**，对应智谱每股约 HK$72 至 136。MiniMax 使用上市公司市值和 LTM 收入口径，单独计算后对应约 HK$285。两项结果都明显低于 HK$1,090。

SenseTime、Phancy 和中科闻歌放在港股邻近组。Palantir、Cloudflare 和 Snowflake 放在商业化参照组。它们能帮助读者判断港股 AI 资产和成熟 AI 软件的估值位置，商业模式与收入结构却和基础模型实验室差别很大，因此不参与核心中位数。逐行口径、估值日和来源见 [`data/valuation_comps.csv`](data/valuation_comps.csv)。

### 事件研究

把模型发布/榜单事件当作信息事件，计算累计异常收益（CAR，均值调整；以 MiniMax 为基准做同业调整稳健性）。

| 事件 | Day 0 | 反应[0,+1] | 漂移[+2,+10] | 读数 |
|---|---|---|---|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | 反应不足 |
| GLM-5-Turbo | 2026-03-16 | +7.7% | −19.3% | 反转 |
| GLM-5.1 | 2026-04-08 | +13.8% | −14.2% | 过度反应 |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | 强反应不足 |
| GLM-5.3 | 2026-08-14 | −6.5% | +3.8% | 信息可能提前进入价格，同业调整后为正 |
| *MiniMax M2.7* | 2026-03-18 | −5.5% | −49.1% | 反应较弱，随后估值收缩 |
| *MiniMax M3* | 2026-06-01 | −21.1% | −40.8% | 发布后估值收缩 |
| **均值(5)** | | **+13.7%** | **+4.6%** | |

均值调整采用 `AR_t = R_t - average(R[-20,-6])`。截至 2026-08-28，GLM-5.2 与 GLM-5.3 的 [+2,+10] 窗口均覆盖完整 9 个交易日。GLM-5.3-Flash 的后续窗口不足，因此只进入扩展目录。

事件日期独立取自官方发布公告，没有按股价走势倒推。原始短窗五次中有四次为正，均值为 +13.7%。同业调整后，五次反应与后续漂移均为正，均值分别为 +15.3% 和 +16.8%。2 月 20 日与 5 月 13 日的尖峰来自指数调整和资金流事件，未计为能力事件。

五个事件能够支撑一个有意思的本科案例。样本数量和上市历史仍然有限，结论只作为初步诊断性证据，不用于证明普遍异象。

### 港股 AI 参照公司

截至 2026 年 8 月 28 日，港股 AI 参照公司可按业务分为基础模型实验室和企业 AI 平台。

| 公司 | 代码 | 定位 | 上市表现 |
|---|---|---|---|
| 智谱AI | 2513.HK | 通用基础大模型实验室 | IPO HK$116.20 → HK$1,090（+838%） |
| MiniMax | 00100.HK | 通用/多模态基础模型公司 | IPO HK$165 → HK$300.4（+82%，首日翻倍后大幅回落） |
| SenseTime 商汤 | 00020.HK | 生成式 AI、计算机视觉与解决方案平台 | 2026-08-28 收盘 HK$1.48，约 9.7× LTM 收入 |
| Phancy 范式智能 | 06682.HK | 企业 AI 平台与智能体服务 | 2026-08-28 收盘 HK$27.76，约 1.6× LTM 收入 |
| 中科闻歌 Wenge AI | 01956.HK | 企业级决策大模型与 AI 解决方案商 | 2026-06-26 上市，IPO HK$60.70 → HK$87.8；约 28.8× LTM 收入 |

> *Recent Hong Kong AI listings include foundation-model laboratories such as Zhipu AI and MiniMax, as well as enterprise-focused AI platforms. Wenge AI is an enterprise decision-intelligence provider and belongs in the Hong Kong-adjacent cohort.*

中科闻歌由中科院自动化所团队 2017 年创立，主打 DIOS 决策智能操作系统与 Decitron、雅意等模型，2025 年中国企业级决策智能大模型市场收入第一（~10.2% 份额）。SenseTime、Phancy 和中科闻歌都保留在港股邻近组。它们的收入结构与基础模型实验室差别很大，因此只展示倍数，不参与核心中位数。

### 关键图表

<p align="center"><img src="figures/fig1_price_paths.png" width="800" alt="价格路径"></p>
<p align="center"><img src="figures/fig5_football_field.png" width="720" alt="估值足球场"></p>
<p align="center"><img src="figures/fig6_ps_comps.png" width="760" alt="分层收入倍数对比"></p>
<p align="center"><img src="figures/fig3_car_eventtime.png" width="640" alt="平均CAR"></p>
<p align="center"><img src="figures/fig4_reaction_vs_drift.png" width="560" alt="反应vs漂移"></p>

### 数据来源

来源按以下顺序取舍。**HKEX 招股书与公告 > 官方模型卡和技术报告 > 恒生指数公司公告 > 正式市场数据库**。新闻媒体只作交叉核对。

- **行情** 使用 Tushare `hk_daily`。频率或权限受限时，以腾讯财经港股日线和 Nasdaq 美股日线补齐并交叉核对，见 [`data/`](data/)。
- **财务** 使用港交所第 18C 章招股书及 2025 年度报告，详见论文附录 A。
- **估值可比** 输入表与生成表分别见 [`data/valuation_comps_input.csv`](data/valuation_comps_input.csv) 和 [`data/valuation_comps.csv`](data/valuation_comps.csv)，逐行保留估值日、收入周期、币种和来源。
- **AGM 通函** 使用 2026 年 6 月 22 日股东大会投票结果公告。该公告确认总股本为 445,843,090 股，并记录股权激励方案等 20 项决议全票通过。
- **能力事件** 使用 GLM 和 MiniMax 官方模型卡、ZCode 发布记录与 SWE-Bench Pro 等榜单。
- **指数和资金流** 使用恒生指数公司指数调整公告与 HKEX、SSE 港股通名单。

> ⚠️ Tushare token 仅通过环境变量传入，切勿写入代码或提交到仓库；无权限时可运行公开来源回退模式。

### 项目结构

```text
.
├── paper/                 # 论文 XeLaTeX 源 (main.tex) 与 main.pdf
├── 42353012_许哲圣_*.pdf   # 按"学号_姓名_论文名"命名的提交版 PDF
├── model/                 # 活公式估值模型 valuation_model.xlsx
├── eventstudy/            # 事件研究 CAR 结果与 Base Case 预测 (csv)
├── figures/               # 论文/README 图表
├── data/                  # 行情与分层估值可比口径 CSV
├── OUTLINE.md / DATA_TABLES.md / EVENT_STUDY.md  # 过程文档
```

### 如何编译

```bash
python scripts/build_project.py
```

手动等价命令

```bash
cd paper
python ../scripts/rebuild_outputs.py
python ../scripts/comps_beta_and_reverse_dcf.py
# 需 TeX Live + XeLaTeX（封面含中文，必须用 xelatex；参考文献为内嵌 APA 列表，无需 bibtex）
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
cd ..
python scripts/validate_outputs.py
```

---

## English

### Project Overview

I built this project around a valuation problem that conventional earnings-surprise analysis handles poorly. Zhipu AI listed as Knowledge Atlas under 2513.HK on the HKEX Main Board under Chapter 18C on 8 January 2026. The company was still deeply loss-making, with negative book equity and about US$200 million in expected 2026 revenue. By 28 August 2026, its market capitalization had reached about US$62.3 billion, equivalent to 311.5 times FY2026E revenue.

The project asks what investors are pricing when near-term earnings provide little information. I use a three-scenario DCF, reverse DCF, layered comparables and a real-options interpretation to establish a fundamental range. I then define model releases and benchmark gains as capability-surprise events and run a peer-adjusted event study using MiniMax as the comparison firm.

The probability-weighted DCF produces about HK$32 per share, equal to roughly 3.0 percent of the HK$1,090 market price on 28 August 2026. The reverse DCF indicates that the observed price requires about US$71 billion in 2035 revenue, implying approximately 92 percent annual growth from 2026 through 2035. These scenario outputs define the assumptions embedded in the price. They do not constitute a price target.

The event study covers five independently dated GLM events from GLM-5 through GLM-5.3. The average two-day reaction is 13.7 percent before peer adjustment and 15.3 percent after adjustment. The sample covers one company during its first eight months as a listed firm, so I present the result as diagnostic evidence from an undergraduate case. It cannot establish a general market anomaly.

### Work Completed

| Research step | Work performed | Auditable output |
|---|---|---|
| Fundamental valuation | Built the CAPM/WACC bridge, three-scenario DCF, sensitivity analysis and reverse DCF | [Live-formula model](model/valuation_model.xlsx) |
| Relative valuation | Separated frontier laboratories, Hong Kong adjacent firms and mature AI software companies; recorded the valuation date and revenue basis for each row | [Comparable-company data](data/valuation_comps.csv) |
| Event study | Dated releases independently, calculated raw and peer-adjusted CARs, and separated capability events from index and flow events | [Event-study results](eventstudy/event_panel_summary.csv) |
| Reproducibility | Connected the main tables, figures and paper to build scripts and output checks | [Build script](scripts/build_project.py) · [Validation script](scripts/validate_outputs.py) |

### Where to Start

| Time available | Suggested entry point |
|---|---|
| About 1 minute | Read the [valuation results](#valuation-summary-market-row-at-2026-08-28) and [event study](#event-study) |
| About 10 minutes | Open the [presentation](presentation/zhipu_beamer.pdf) |
| Full review | Read the [paper](paper/main.pdf) |
| Assumption check | Inspect the [valuation model](model/valuation_model.xlsx) and [comparable-company data](data/valuation_comps.csv) |

### Research Question and Design

How can a defensible valuation range be built for a foundation-model company without stable earnings? Once capability information reaches the market, what do the short-window reaction and subsequent drift look like?

| Research step | Method | Purpose |
|---|---|---|
| Fundamental valuation | CAPM/WACC, three-scenario DCF, reverse DCF, comparables and real options | Establish a cash-flow range and recover the operating path embedded in the market price |
| Capability event study | Five events from GLM-5 through GLM-5.3 with MiniMax peer adjustment | Observe the immediate reaction and subsequent drift following capability information |

### Valuation Summary (market row at 2026-08-28)

WACC is approximately 13.5 percent, using a bottom-up beta of about 1.6. The model applies HK$7.8/US$, RMB 7.1/US$ and approximately 446 million shares. The live workbook is [`model/valuation_model.xlsx`](model/valuation_model.xlsx), and the paper's Appendix B contains the full ten-year Base case.

| Scenario | Revenue CAGR 2026 to 2035 | Terminal margin | Equity value | Per share (HK$) |
|---|---|---|---|---|
| Bear (p=0.35) | 21% | 18% | $0.7B | 12 |
| Base (p=0.45) | 31% | 28% | $1.6B | 27 |
| Bull (p=0.20) | 46% | 35% | $4.6B | 80 |
| **Probability weighted** | N/A | N/A | **$1.9B** | **32** |
| *Market (2026-08-28)* | N/A | N/A | *$62.3B* | *1,090* |

**Reverse DCF** indicates that the price requires about US$71 billion in revenue by 2035, equivalent to roughly 92 percent annual growth from 2026 through 2035 and about 355 times FY2026E revenue.
Zhipu trades at about **311.5× FY2026E revenue**. The closest listed peer, MiniMax, is **81.4× LTM revenue**.
Paired private-market references for OpenAI, Anthropic, and Mistral run from **20.5× to 39.0×**, with a **34.1× median**.
That private range implies about HK$72 to HK$136 per Zhipu share, while the MiniMax multiple implies about HK$285; both remain well below HK$1,090.
SenseTime, Phancy, and Wenge AI form a separate Hong Kong-adjacent cohort, while Palantir, Cloudflare, and Snowflake are commercialization references. Neither cohort enters the private-deal range. Row-level bases and sources are in [`data/valuation_comps.csv`](data/valuation_comps.csv).

### Event Study

| Event | Day 0 | Reaction [0,+1] | Drift [+2,+10] | Reading |
|---|---|---|---|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | −19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | −14.2% | over-reaction |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | strong under-reaction |
| GLM-5.3 | 2026-08-14 | −6.5% | +3.8% | anticipated; positive peer-adjusted reaction |
| *MiniMax M2.7* | 2026-03-18 | −5.5% | −49.1% | muted / de-rate |
| *MiniMax M3* | 2026-06-01 | −21.1% | −40.8% | failed catalyst / de-rate |
| **Average (5)** | | **+13.7%** | **+4.6%** | |

The mean-adjusted return is defined as `AR_t = R_t - average(R[-20,-6])`. As of 2026-08-28, GLM-5.2 and GLM-5.3 both have complete nine-day [+2,+10] windows. GLM-5.3-Flash remains in the extended catalog because its post-event window is incomplete.

The event dates come from official release announcements and were set independently of the share-price path. Mean reaction rises from +13.7 percent before adjustment to +15.3 percent after peer adjustment. Subsequent drift rises from +4.6 percent to +16.8 percent, and all five adjusted reaction and drift windows are positive. The spikes on 20 February and 13 May are index and flow events linked to Hang Seng Tech inclusion and Stock Connect.

The five events support a focused undergraduate case. The small sample and short listing history limit the result to preliminary diagnostic evidence and do not support a general market anomaly.

### Repository Structure

```text
.
├── paper/      # Thesis XeLaTeX source (main.tex) and main.pdf
├── 42353012_许哲圣_*.pdf   # submission PDF named 学号_姓名_论文名
├── model/      # Live-formula valuation model
├── eventstudy/ # CAR results + Base-case projection (csv)
├── figures/    # Figures
└── data/       # Tushare / Tencent Finance / Nasdaq market-data CSVs
```

### How to Build

```bash
python scripts/build_project.py
```

Quick checks

```bash
python -m unittest discover -s tests
python scripts/validate_outputs.py
```

Manual equivalent

```bash
cd paper
python ../scripts/rebuild_outputs.py
python ../scripts/comps_beta_and_reverse_dcf.py
# XeLaTeX required (CJK cover); references are an inline APA list, so no bibtex step
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
cd ..
python scripts/validate_outputs.py
```

> ⚠️ Pass any Tushare token only through an environment variable; the updater can use public fallbacks when permissions bind.

---

## License

MIT License, see [LICENSE](LICENSE). Copyright (c) 2026 Zhesheng Xu (许哲圣). Student ID 42353012.
