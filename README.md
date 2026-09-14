# 智谱 AI 估值与能力惊喜事件研究 | Zhipu AI Valuation and Capability-Surprise Event Study

<p align="center">
  <a href="#中文"><img src="https://img.shields.io/badge/语言-中文-E84D3D?style=for-the-badge&labelColor=3B3F47" alt="中文"></a>
  &nbsp;
  <a href="#english"><img src="https://img.shields.io/badge/Language-English-2F73C9?style=for-the-badge&labelColor=3B3F47" alt="English"></a>
</p>

<p align="center">
  <strong>Zhesheng Xu（许哲圣）</strong><br>
  Corporate Finance Final Project<br>
  <strong>信息截止 / Information cutoff</strong> 2026-09-13 · <strong>行情 / Prices</strong> 2026-09-11
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

这个项目从一个具体的估值难题开始。智谱 AI 于 2026 年 1 月 8 日成为全球首家上市的基础模型公司。9 月 11 日收盘，公司市值约为 473 亿美元。8 月 31 日收盘后发布的半年业绩显示，H1 收入同比增长 399.7% 至人民币 9.54 亿元，开放平台与 API 已占收入的 86.5%。商业化正在加速，但经营亏损仍扩大至人民币 21.47 亿元，经调整净亏损也同比扩大 12.1%。研究重点随之落在市场为这种增长预付了多少。

我把披露事实与预测假设分开。公司没有提供全年收入指引；FY2026E 的 7 亿美元来自 H1 实际收入和 8 月经营节奏，属于模型估计。2026 年经营利润率取 −100%，较 H1 的 −225% 假定了明显改善。在此基础上，我用 CAPM/WACC、三情景 DCF、反向 DCF 与分层可比估值交叉检验。概率加权 DCF 约为每股 HK$88，9 月 11 日收盘价为 HK$793。反向 DCF 显示，若要支撑现价，2035 年收入需接近 605 亿美元。

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

### 2026H1 半年业绩更新

[港交所中期业绩公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0831/2026083101539.pdf)于 8 月 31 日收盘后发布，数据未经审计并由 KPMG 审阅。

| 指标 | 2026H1 | 2025H1 | 同比变化 |
|---|---:|---:|---:|
| 收入 | RMB 953.9M | RMB 190.9M | +399.7% |
| 毛利 | RMB 251.6M | RMB 95.4M | +163.7% |
| 总毛利率 | 26.4% | 50.0% | −23.6ppt |
| 开放平台与 API 收入 | RMB 825.2M，占 86.5% | RMB 29.1M，占 15.2% | +2,735.7% |
| API 毛利率 | 24.6% | −0.4% | 约 +25ppt |
| 经营亏损 | RMB 2,146.6M | RMB 1,899.2M | 扩大约 13.0% |
| 经调整净亏损 | RMB 1,964.1M | RMB 1,752.0M | 扩大 12.1% |

收入结构已经从本地部署转向调用和订阅，API 毛利率也转正。与此同时，应收款、算力预付款和研发投入继续上升。报告中的净亏损收窄来自毛利增加和投资者金融工具相关损失大幅下降，经营亏损和经调整净亏损仍在扩大，因此本文没有把 headline 写成“盈利改善”。公告未呈列经营现金流，相关指标在数据表和模型中保留为空缺。

### MiniMax 2026H1 同业更新

[MiniMax 中期业绩公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082600680.pdf)于 8 月 26 日收盘后发布。H1 收入同比增长 283.1% 至 US$116.6M，开放平台和企业服务收入增长 703.1% 至 US$73.9M、占收入 63.4%；毛利率由 12.1% 升至 17.9%。但经调整净亏损从 US$138.7M 扩大到 US$293.0M，说明商业化提速仍伴随高研发投入。估值可比中的 US$165.2M LTM 收入，按 FY2025 收入减去 2025H1、再加 2026H1 计算，而不是把半年收入简单年化。

### 9 月 13 日融资与闻歌半年业绩

智谱 [港交所公告](https://www.hkexnews.hk/listedco/listconews/sehk/2026/0913/2026091300026_c.pdf)披露最多 2,196.5 万股配售（HK$714/股）及人民币 201.4 亿元、美元结算的零息可转债，合计约 50 亿美元融资规模。协议已签署，配售预计 9 月 16 日交割且仍有条件；截至 9 月 13 日不能视为资金已经到账。初始转股价 HK$892.50，债券 2027 年 9 月到期。原净现金桥及股本暂不加入本次拟融资。

闻歌 [半年业绩公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0825/2026082500959.pdf)显示收入 RMB172.750m（+46.0%），订阅/API 占 34.1%，毛利率 55.0%。总亏损收窄 24.5%，归母亏损收窄 27.6%，经调整亏损收窄 29.5%；研发增速 59.0%，且金融资产公允价值收益帮助报表亏损收窄。闻歌仍属商业模式不同的邻近可比。

8 月 31 日至 9 月 11 日智谱回撤 33.6%，MiniMax 回撤 22.6%。共同重估、较高估值和亏损压力可以解释脆弱性，但不能把周末融资公告倒推为此前下跌的已证实原因。详细条款、口径与分析见 [9 月 13 日更新](UPDATE_2026-09-13.md)。

### 估值结论

行情更新至 9 月 11 日；经营假设、净现金桥和 8 月末 beta 保持原口径。MiniMax、闻歌市值按原股本及汇率基础重估，其余参照保留逐行日期。9 月融资仍有交割条件，未计入已完成股本或现金，详见 [信息截止更新](UPDATE_2026-09-13.md)。

WACC 约为 13.5%，其中自下而上 β 以截至 8 月 31 日的 60 个月月度回归为起点，去杠杆中位数 1.55 后取约 1.6；Rf 为 4%，ERP 为 6%。模型统一采用 HK$7.8/US$、RMB 7.1/US$ 和配售后的 4.656 亿股。净现金采用可复核的 pro forma 桥接。6 月末现金与短期投资扣除银行借款及租赁负债，再加 7 月配售净款，合计约 42.89 亿美元。公司截至 8 月末的现金余额尚未披露，因此模型保留这项期后调整的口径说明。活公式见 [`model/valuation_model.xlsx`](model/valuation_model.xlsx)，十年完整 Base Case 见论文附录 B。

| 情景 | 收入 CAGR 2026 至 2035 | 终期利润率 | 股权价值 | 每股（HK$） |
|---|---|---|---|---|
| 悲观 (p=0.35) | 23% | 18% | $1.5B | 25 |
| 中性 (p=0.45) | 31% | 28% | $4.3B | 73 |
| 乐观 (p=0.20) | 47% | 35% | $13.9B | 233 |
| **概率加权** | N/A | N/A | **$5.3B** | **88** |
| *市价 (2026-09-11，收盘)* | N/A | N/A | *$47.3B* | *793* |

**反向 DCF** 固定 FY2026E 收入后重新求解增长路径。要支撑现价，2035 年收入需接近 **US$605 亿**，对应 2026 至 2035 年约 **64%** 的年复合增速。这项结果只用于呈现市价隐含条件。

**分层可比** 对两家上市基础模型公司采用同一规则：2026 年 9 月 11 日市值除以截至 2026H1 的 LTM 实际收入。智谱 LTM 收入为人民币 14.87 亿元（FY2025 减 2025H1、再加 2026H1），按 RMB7.1/US$ 折合 US$209.5M，对应 **226.0×**；MiniMax LTM 收入为 US$165.2M，对应 **73.2×**。

OpenAI、Anthropic 与 Mistral 的私有交易参照更接近基础模型实验室的业务形态，因此它们构成 football field 的核心交易区间。倍数落在 **20.5 至 39.0×**，中位数为 **34.1×**；由于私企只能取得同期收入 run-rate，这组交易参照仍单独应用于智谱 FY2026E，得到每股约 HK$240 至 457。统一 LTM 口径后，MiniMax 倍数对应智谱约 HK$257，较市价低 68%。最接近的上市同业不再能解释智谱的大部分市值，智谱相对 MiniMax 仍有约 3.1 倍的收入倍数溢价。

SenseTime、Phancy 和中科闻歌放在港股邻近组。Palantir、Cloudflare 和 Snowflake 放在商业化参照组。它们能帮助读者判断港股 AI 资产和成熟 AI 软件的估值位置，商业模式与收入结构却和基础模型实验室差别很大，因此不参与核心中位数。逐行口径、估值日和来源见 [`data/valuation_comps.csv`](data/valuation_comps.csv)。

### 事件研究

本节保留截至 8 月 31 日的原始五事件样本及 bootstrap；9 月新增可观察窗口另见 [9 月 11 日更新](UPDATE_2026-09-11.md)。

把模型发布/榜单事件当作信息事件，计算累计异常收益（CAR，均值调整；以 MiniMax 为基准做同业调整稳健性）。

| 事件 | Day 0 | 反应[0,+1] | 漂移[+2,+10] | 读数 |
|---|---|---|---|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | 反应不足 |
| GLM-5-Turbo | 2026-03-16 | +7.7% | −19.3% | 反转 |
| GLM-5.1 | 2026-04-08 | +13.8% | −14.2% | 过度反应 |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | 强反应不足 |
| GLM-5.3 | 2026-08-14 | −6.5% | +3.8% | 信息可能提前进入价格，同业调整后为正 |
| MiniMax M2.5 | 2026-02-12 | +24.2% | −2.1% | 发布当期获正面定价，后续基本持平 |
| MiniMax M2.7 | 2026-03-18 | −5.5% | −49.1% | 反应较弱，随后估值收缩 |
| MiniMax M3 | 2026-06-01 | −21.1% | −40.8% | 发布后估值收缩 |
| **均值(5)** | | **+13.7%** | **+4.6%** | |

均值调整采用 `AR_t = R_t - average(R[-20,-6])`。截至 2026-08-31，GLM-5.2 与 GLM-5.3 的 [+2,+10] 窗口均覆盖完整 9 个交易日。GLM-5.3-Flash 只有三个后续交易日，因此只进入扩展目录。H1 业绩公告于 8 月 31 日 18:56 收盘后发布，也只列入财务披露目录；当天 +9.63% 的涨幅不能写成“财报发布后的反应”。

事件日期独立取自官方发布公告，没有按股价走势倒推。原始短窗五次中有四次为正，均值为 +13.7%。同业调整后，五次反应与后续漂移均为正，均值分别为 +15.3% 和 +16.8%。2 月 20 日与 5 月 13 日的尖峰来自指数调整和资金流事件，未计为能力事件。

MiniMax 的主线事件现补齐 M2.5（2 月 12 日）、M2.7 和 M3。H3（7 月 31 日）与 Music 3.0（8 月 13 日）保留在扩展目录，但不进入 Table 2：前者以音视频生成作为主要输出，后者是音乐垂类模型，与文本、编码和 Agent 能力事件不在同一口径。MiniMax 半年报也作为财务披露事件列入目录；由于 8 月 26 日收盘后发布，截至 8 月 31 日没有完整漂移窗口，不计算 CAR。

论文 Table 2 另列出 16 个具备完整窗口、且模型发布方本身存在可交易股票的大型科技厂商事件。7—8 月新增腾讯 Hy3、阿里 Qwen3.8-Max、Google Gemini 3.6/3.7 Flash 和 Meta Muse Spark 1.1。Microsoft 代 OpenAI、Tesla 代 xAI 的 6 条代理事件已从 CAR 表和均值中移除，只留在审计目录；在原 8 月 31 日截止日没有完整后窗的 Qwen3.8-Flash、腾讯 Hy4 和 Gemini Transcribe/Omni 1.1 同样只进入目录。

五个事件能够支撑一个有意思的本科案例。样本数量和上市历史仍然有限，结论只作为初步诊断性证据，不用于证明普遍异象。

### 港股 AI 参照公司

截至 2026 年 9 月 11 日，港股 AI 参照公司可按业务分为基础模型实验室和企业 AI 平台。

| 公司 | 代码 | 定位 | 上市表现 |
|---|---|---|---|
| 智谱AI | 2513.HK | 通用基础大模型实验室 | IPO HK$116.20 → HK$793（+582%） |
| MiniMax | 00100.HK | 通用/多模态基础模型公司 | IPO HK$165 → HK$270（+64%，首日翻倍后曾明显回落） |
| SenseTime 商汤 | 00020.HK | 生成式 AI、计算机视觉与解决方案平台 | 2026-08-31 收盘 HK$1.44，约 9.4× LTM 收入 |
| Phancy 范式智能 | 06682.HK | 企业 AI 平台与智能体服务 | 2026-08-31 收盘 HK$28.02，约 1.6× LTM 收入 |
| 中科闻歌 Wenge AI | 01956.HK | 企业级决策大模型与 AI 解决方案商 | IPO HK$60.70 → HK$79.30（+31%）；约 26.0× LTM 收入 |

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
- **财务** 使用港交所第 18C 章招股书、2025 年报和 2026H1 中期业绩公告；智谱与 MiniMax 的结构化口径分别见 [`data/zhipu_financials_input.csv`](data/zhipu_financials_input.csv) 和 [`data/minimax_financials_input.csv`](data/minimax_financials_input.csv)。智谱截至 8 月 31 日的正式中期报告尚待发布，业绩公告也未呈列经营现金流量表。
- **估值可比** 输入表与生成表分别见 [`data/valuation_comps_input.csv`](data/valuation_comps_input.csv) 和 [`data/valuation_comps.csv`](data/valuation_comps.csv)，逐行保留估值日、收入周期、币种和来源。
- **股本与配售** 使用 6 月月报及 7 月 13 日配售完成公告。配售新增 19,780,000 股后，总股本为 465,623,090 股；约 313.75 亿港元净募资在估值桥中单列为期后 pro forma 调整。
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

The information cutoff is 13 September 2026, with prices through the September 11 close. The September 13 placement and convertible-bond announcement describes conditional transactions, so proceeds and new shares are not booked as settled. Wenge's H1 results and the September drawdown are discussed in the [September 13 update](UPDATE_2026-09-13.md); the original August event sample is unchanged.

I built this project around a valuation problem that conventional earnings-surprise analysis handles poorly. Zhipu AI listed under 2513.HK on 8 January 2026, becoming the first publicly traded foundation-model laboratory. By the close on 11 September, its market capitalization was approximately US$47.3 billion. Results released after the 31 August close showed H1 revenue of RMB953.9 million, up 399.7 percent, with open-platform and API sales contributing 86.5 percent. Operating loss nevertheless widened to RMB2.15 billion, and adjusted net loss increased by 12.1 percent. The central question is therefore measurable: how much future operating performance has the market already paid for?

The project asks what investors are pricing when near-term earnings provide little information. I use a three-scenario DCF, reverse DCF, layered comparables and a real-options interpretation to establish a fundamental range. I then define model releases and benchmark gains as capability-surprise events and run a peer-adjusted event study using MiniMax as the comparison firm.

I separate reported facts from forecast choices. The company gave no full-year revenue guidance; the model's US$700 million FY2026E revenue uses H1 actuals and the August run-rate, while a −100 percent FY2026 operating margin assumes substantial improvement from the reported H1 margin of −225 percent. The probability-weighted DCF is about HK$88 per share, or 11.1 percent of the HK$793 September 11 close. The reverse DCF requires roughly US$60.5 billion of 2035 revenue, a 64.1 percent compound annual growth rate from the FY2026E base. These outputs describe the assumptions embedded in the price rather than a price target.

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
| About 1 minute | Read the [valuation results](#valuation-summary-market-row-at-2026-09-11) and [event study](#event-study) |
| About 10 minutes | Open the [presentation](presentation/zhipu_beamer.pdf) |
| Full review | Read the [paper](paper/main.pdf) |
| Assumption check | Inspect the [valuation model](model/valuation_model.xlsx) and [comparable-company data](data/valuation_comps.csv) |

### Research Question and Design

How can a defensible valuation range be built for a foundation-model company without stable earnings? Once capability information reaches the market, what do the short-window reaction and subsequent drift look like?

| Research step | Method | Purpose |
|---|---|---|
| Fundamental valuation | CAPM/WACC, three-scenario DCF, reverse DCF, comparables and real options | Establish a cash-flow range and recover the operating path embedded in the market price |
| Capability event study | Five events from GLM-5 through GLM-5.3 with MiniMax peer adjustment | Observe the immediate reaction and subsequent drift following capability information |

### H1 2026 Results Update

The [HKEX interim-results announcement](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0831/2026083101539.pdf) was released after the 31 August close. The figures are unaudited and were reviewed by KPMG.

| Metric | H1 2026 | H1 2025 | Change |
|---|---:|---:|---:|
| Revenue | RMB953.9M | RMB190.9M | +399.7% |
| Gross profit | RMB251.6M | RMB95.4M | +163.7% |
| Total gross margin | 26.4% | 50.0% | −23.6ppt |
| Open-platform and API revenue | RMB825.2M, 86.5% of total | RMB29.1M, 15.2% | +2,735.7% |
| API gross margin | 24.6% | −0.4% | approximately +25ppt |
| Operating loss | RMB2,146.6M | RMB1,899.2M | widened approximately 13.0% |
| Adjusted net loss | RMB1,964.1M | RMB1,752.0M | widened 12.1% |

The mix has shifted decisively from on-premise deployment toward API usage and subscriptions, and API gross margin turned positive. Receivables, compute-service prepayments and R&D spending also increased. Reported net loss narrowed as gross profit rose and investor-instrument losses fell sharply; operating loss and adjusted net loss both widened. The announcement did not present an operating-cash-flow statement, so the project leaves that field undisclosed rather than inferring it from the change in cash.

### MiniMax H1 2026 Peer Update

MiniMax released its [interim results](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082600680.pdf) after the 26 August close. Revenue rose 283.1 percent to US$116.6 million, while Open Platform and enterprise-service revenue rose 703.1 percent to US$73.9 million, or 63.4 percent of the total. Gross margin improved from 12.1 to 17.9 percent, but adjusted net loss widened from US$138.7 million to US$293.0 million. The US$165.2 million LTM revenue used in the peer multiple equals FY2025 revenue less H1 2025 plus H1 2026; it is not a simple annualisation of the latest half.

### Valuation Summary (market row at 2026-09-11)

WACC is approximately 13.5 percent. The bottom-up beta starts from 60 monthly regressions through 31 August, with the 1.55 unlevered median rounded to 1.6. The model applies HK$7.8/US$, RMB7.1/US$ and 465.6 million post-placement shares. Its US$4.289 billion pro forma net-cash bridge starts with reported 30 June cash and short-term investments, deducts bank loans and leases, and adds July placement proceeds. It is not presented as a reported 31 August cash balance. The live workbook is [`model/valuation_model.xlsx`](model/valuation_model.xlsx), and the paper's Appendix B contains the full ten-year Base case.

| Scenario | Revenue CAGR 2026 to 2035 | Terminal margin | Equity value | Per share (HK$) |
|---|---|---|---|---|
| Bear (p=0.35) | 23% | 18% | $1.5B | 25 |
| Base (p=0.45) | 31% | 28% | $4.3B | 73 |
| Bull (p=0.20) | 47% | 35% | $13.9B | 233 |
| **Probability weighted** | N/A | N/A | **$5.3B** | **88** |
| *Market (2026-09-11, close)* | N/A | N/A | *$47.3B* | *793* |

**Reverse DCF** fixes the FY2026E base and solves for the growth path required by the observed price. It points to approximately US$60.5 billion of 2035 revenue, equivalent to roughly 64.1 percent annual growth from 2026 through 2035.
For the two listed foundation-model companies, the comparison now uses one rule: 11 September 2026 equity value divided by LTM revenue through 2026H1. Zhipu's RMB1,487.3 million LTM revenue, equal to FY2025 less H1 2025 plus H1 2026, translates to US$209.5 million at RMB7.1/US$ and gives **226.0×**. MiniMax remains at **73.2×** on US$165.2 million of LTM revenue.
Paired private-market references for OpenAI, Anthropic, and Mistral run from **20.5× to 39.0×**, with a **34.1× median**.
The private range still applies to Zhipu's FY2026E revenue because the private-company observations use contemporaneous revenue run-rates; it implies approximately HK$240 to HK$457 per share. Applying MiniMax's LTM multiple to Zhipu's LTM revenue gives about HK$257, 68 percent below the market. On the uniform listed-company basis, Zhipu trades at roughly 3.1 times MiniMax's revenue multiple, so the peer no longer explains most of the quote.
SenseTime, Phancy, and Wenge AI form a separate Hong Kong-adjacent cohort, while Palantir, Cloudflare, and Snowflake are commercialization references. Neither cohort enters the private-deal range. Row-level bases and sources are in [`data/valuation_comps.csv`](data/valuation_comps.csv).

### Event Study

This section preserves the original August 31 five-event cohort and bootstrap. Newly observable windows are reported separately in the [September 11 update](UPDATE_2026-09-11.md).

| Event | Day 0 | Reaction [0,+1] | Drift [+2,+10] | Reading |
|---|---|---|---|---|
| GLM-5 | 2026-02-11 | +22.5% | +24.7% | under-reaction |
| GLM-5-Turbo | 2026-03-16 | +7.7% | −19.3% | reversal |
| GLM-5.1 | 2026-04-08 | +13.8% | −14.2% | over-reaction |
| GLM-5.2 | 2026-06-15 | +30.8% | +28.2% | strong under-reaction |
| GLM-5.3 | 2026-08-14 | −6.5% | +3.8% | anticipated; positive peer-adjusted reaction |
| MiniMax M2.5 | 2026-02-12 | +24.2% | −2.1% | positive launch reaction; little subsequent drift |
| MiniMax M2.7 | 2026-03-18 | −5.5% | −49.1% | muted / de-rate |
| MiniMax M3 | 2026-06-01 | −21.1% | −40.8% | failed catalyst / de-rate |
| **Average (5)** | | **+13.7%** | **+4.6%** | |

The mean-adjusted return is defined as `AR_t = R_t - average(R[-20,-6])`. As of 2026-08-31, GLM-5.2 and GLM-5.3 both have complete nine-day [+2,+10] windows. GLM-5.3-Flash has only three subsequent trading days and remains in the extended catalog. The H1 results announcement was released at 18:56 after the 31 August close, so that day's 9.63 percent gain predates the disclosure and is not treated as an earnings reaction.

The event dates come from official release announcements and were set independently of the share-price path. Mean reaction rises from +13.7 percent before adjustment to +15.3 percent after peer adjustment. Subsequent drift rises from +4.6 percent to +16.8 percent, and all five adjusted reaction and drift windows are positive. The spikes on 20 February and 13 May are index and flow events linked to Hang Seng Tech inclusion and Stock Connect.

The MiniMax peer series now includes M2.5 (12 February), M2.7 and M3. H3 (31 July) and Music 3.0 (13 August) remain in the extended catalog but outside Table 2 because their audio-video and music outputs are not comparable with the text, coding and agent events in the core sample. MiniMax's results announcement is also catalogued as a financial disclosure, but its post-event window is incomplete at the cutoff.

Paper Table 2 also reports 16 complete-window large-tech events for which the model issuer itself has a traded security. The July-August refresh adds Tencent Hy3, Alibaba Qwen3.8-Max, Google Gemini 3.6/3.7 Flash and Meta Muse Spark 1.1. Six Microsoft-for-OpenAI and Tesla-for-xAI proxy events have been removed from the CAR table and its average, while remaining visible in the audit catalog. Qwen3.8-Flash, Tencent Hy4 and Gemini Transcribe/Omni 1.1 also remain catalog-only because their post-event windows were incomplete at the original August 31 cutoff.

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
