# Anthropic IPO 底稿（起始版本 2026-10-11，信息复核至 2026-10-23）

2026-10-11 从 `D:/Quant/Financial Valuation & Modeling/midterm/anthropic_ipo_20260930/` 迁入，共 28 项原始内容；源文件夹已清空。原目录名虽含 20260930，Excel 和生成脚本的研究截止日实际为 2026-10-11。旧版底稿通过 Git 历史查阅。

| 入口 | 内容 |
|---|---|
| [估值工作簿](Anthropic_IPO_Basic_Valuation.xlsx) | 保留 Valuation / Comps / Inputs 三表；当前披露已同步至 23 日 |
| [演示 PDF](Anthropic_IPO_Valuation_Beamer.pdf) | 同步收入锚、DCF，并补充 10 月 18—23 日进展及期后事项边界 |
| [演示源文件](Anthropic_IPO_Valuation_Beamer.tex) | 本地 XeLaTeX 可编译 |
| [生成脚本](build_model.mjs) | 输出路径改为本目录，不再写回源文件夹 |

DCF EV 为 US$788.539bn，前瞻收入倍数法 EV 为 US$1,950bn。底稿起始日为 10 月 11 日，当前工作簿的信息复核截止已更新至北京时间 23 日，估值日仍假设为 12 月 31 日。最新 IPO 投资者讨论基准为 US$1,500bn；原 US$2,000bn 保留为历史压力情景。季度收入及年度假设对照已加入工作簿，US$64bn 仍为分析者假设。来源见[披露核验](../../DISCLOSURE_UPDATE_2026-10-23.md)。

## 已纳入智谱项目

独立复算：`python scripts/anthropic_ipo_crosscheck.py`（从仓库根目录运行）。对应输入和结果位于 `data/anthropic_ipo_projection_input.csv` 与 `eventstudy/anthropic_ipo_*.csv`。可比表另抽取为 `data/anthropic_ipo_comps_reference.csv`。完整口径说明见 [Anthropic 对照](../../ANTHROPIC_COMPARISON.md)。

## 使用原始工作簿时的口径限制

- 14.657× 中位数来自 OpenAI 两个估值时点，并非两个独立同行。不同组混合 ARR、年度预测、NTM 收入及不同估值日期。
- Comps 中部分 EV 倍数结果被标成股权价值，使用前应补现金／债务桥。本项目不把它们合并进智谱的核心已成交交易区间。
- 2026 年收入输入为 64，未提供可复算的月度确认收入推导；原文「model output」不能当作已核验的推导证据。
- 经营亏损与净亏损可以因融资工具会计损益而不同，原表中「两种亏损不可能同时成立」的判断不采用。未公开 S-1 不代表不存在审计报表。
- 所有私有二级市场、IPO 目标及媒体转述按原来源性质保留，不能等同已完成融资；原可比输入未逐项独立证实。

`node_modules` 是指向 Codex 运行时的本机依赖链接；`.workbuddy` 保存迁入的本机记录，均不进入 Git。重新生成起始 Excel 会恢复底稿原有文字，请以上述说明及智谱集成结果为核对依据。
