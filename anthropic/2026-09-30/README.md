# Anthropic IPO 原始估值底稿（2026-09-30）

来源对话：**Build Anthropic IPO valuation model**。原文件目录为 `D:/Quant/Financial Valuation & Modeling/outputs/anthropic_ipo_20260930_01a0f147/`，于 **2026-10-01** 复制到本仓库。研究信息截止 2026-09-30；模型估值日假设为 2026-12-31。

## 文件入口

| 文件 | 内容 |
|---|---|
| [Anthropic_IPO_Basic_Valuation.xlsx](Anthropic_IPO_Basic_Valuation.xlsx) | 原始活公式模型，含 Valuation 与 Inputs 工作表、预测、终值、敏感性和 IPO 发行机制 |
| [Anthropic_IPO_Valuation_Beamer.pdf](Anthropic_IPO_Valuation_Beamer.pdf) | 7 页英文展示稿 |
| [Anthropic_IPO_Valuation_Beamer.tex](Anthropic_IPO_Valuation_Beamer.tex) | 展示稿 LaTeX 源文件，可用 pdfLaTeX 编译 |
| [build_model.mjs](build_model.mjs) | 原模型生成脚本；复制后仅把输出目录改为脚本所在目录 |
| [verification.json](verification.json) | 原模型的独立计算核对值及公式错误检查结果 |
| [assumptions.png](assumptions.png) | 假设输入预览 |
| [dcf_forecast.png](dcf_forecast.png) | 逐年现金流预测预览 |
| [public_sources.png](public_sources.png) | 原参考数据及来源链接预览 |
| [valuation_detail.png](valuation_detail.png) | 终值、敏感性及发行机制预览 |
| [valuation_summary.png](valuation_summary.png) | 估值概要与收入预测图预览 |

Excel、PDF、TeX、核验 JSON 与五张 PNG 均保持原文件字节。模型生成脚本仅修改输出路径，不再写回原对话目录。依赖目录、编译缓存和运行诊断文件未纳入归档。

## 使用与复算

Excel 可直接打开并修改输入；当前快照的前瞻收入倍数法 EV 为 US$1,950bn，DCF EV 为 US$788.3bn。净现金假设为零，发行股数与募资额尚未确定；报道的 IPO 目标属于拟议股权估值。实际结果、报道预测与分析者假设分别保存在 Inputs 表。

跨平台数值复算可使用仓库现有脚本，不依赖这个原始输出目录：

```bash
python scripts/anthropic_ipo_crosscheck.py
```

生成 Excel 需要 Node.js 和 Codex 附带的 `@oai/artifact-tool`。依赖可解析后运行下列命令；它会覆盖本归档目录中的 Excel、预览及核验 JSON，因此重新生成前应保存希望保留的人工修改：

```bash
node anthropic/2026-09-30/build_model.mjs
```

英文展示稿使用固定数值快照；更改 Excel 假设后需同步 TeX 数字，再编译：

```bash
cd anthropic/2026-09-30
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error Anthropic_IPO_Valuation_Beamer.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error Anthropic_IPO_Valuation_Beamer.tex
```

与智谱论文集成的口径说明见 [Anthropic 对照](../../ANTHROPIC_COMPARISON.md)；结构化预测与敏感性已保存在仓库的 data 和 eventstudy 目录。
