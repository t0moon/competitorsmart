# 竞品分析（CompetitorSmart）

面向 **产品经理 / PMM** 的 AI 辅助竞争情报工具。主流程为 **LangGraph ReAct Agent**：通过 DuckDuckGo 检索与网页抓取收集证据，调用 **智谱 GLM**（OpenAI 兼容接口）自主补全信息，最终落盘为 **11 章** Markdown 深度报告（市场、竞品分层、能力、商业化、增长、SWOT、壁垒与机会等）。

默认模型与 API Base 在 `src/constants.py` 统一维护（当前默认：`GLM-4.6V-FlashX`）。

---

## 功能概览

| 项目 | 说明 |
|------|------|
| Agent 流程 | 搜索 → 抓取 → 推理；关键结论需附来源 URL，报告有字数与章节完整性约束 |
| 报告输出 | `outputs/agent/<时间戳>_agent_report.md` |
| 模型与 Key | 智谱；支持 `ZHIPU_API_KEY_1`～`ZHIPU_API_KEY_4`（任一生效即可用于 Agent） |
| 输入方式 | 命令行竞品列表，或 `competitors_input.json` 结构化上下文（市场、品类、官网文案等） |

`requirements.txt` 中还包含 CRM、Notion、表格等集成依赖，供扩展使用；**一键跑通报告仅需智谱 Key + Agent 相关包**（见下文）。

---

## 环境准备

- **Python**：建议 3.10+
- **复制环境模板**：将 `.env.example` 复制为 `.env`，至少填写 `ZHIPU_API_KEY_1`
- **可选**：通过 `ZHIPU_API_BASE_URL` 覆盖默认智谱 OpenAI 兼容地址

**安全**：勿将 `.env` 提交到版本库。仓库已忽略 `.env`；若使用 Git，可设置 `git config core.hooksPath githooks` 启用预提交钩子，避免误提交密钥文件。

---

## 安装

```bash
pip install -r requirements.txt
```

若仅 Agent 报错缺包，可针对性安装：

```bash
pip install langgraph langchain-openai duckduckgo-search
```

---

## 使用方式

```bash
# 根目录已有 competitors_input.json 且其中包含竞品列表时
python main.py

# 快速指定竞品（逗号分隔），可选赛道描述
python main.py --competitors "竞品A,竞品B" --market "SaaS CRM"

# 指定 JSON 输入文件（推荐：可带 website_copy、sales_notes 等）
python main.py --input competitors_input.json

# 仅校验配置与依赖，不调用 API
python main.py --dry-run
```

**报告目录**：`outputs/agent/`。

---

## 报告结构（Agent 模板）

最终 Markdown 固定包含以下二级章节（详见 `src/agent/graph.py` 内 `SYSTEM_PROMPT`）：

1. 报告概述  
2. 市场与赛道分析  
3. 竞品选择与分层  
4. 核心能力拆解（每竞品单独小节）  
5. 商业模式分析  
6. 增长与分发策略  
7. 用户与场景分析  
8. 优劣势对比（SWOT / 对比矩阵）  
9. 关键差异与壁垒  
10. 机会点与策略建议  
11. 数据附录（含来源列表等）  

单次运行可能耗时较长；若遇额度或限流，可更换 Key 或稍后重试。

---

## 输入说明

- **`--competitors`**：仅名称，适合试跑；Agent 自行检索官网与第三方信息。  
- **`competitors_input.json`**：可包含 `market`、`product_category`、`geography`、`our_product`、`competitors[].name`、`category`、`website`、`website_copy`、`sales_notes` 等字段，与 `src/config.py` 中 `Config` 加载逻辑一致。  
- 人工整理竞品档案时可参考 `src/templates/competitor_profile.md`。

---

## 仓库目录（核心）

```
main.py                    CLI 入口
competitors_input.json     结构化输入示例（可自命名并通过 --input 指定）
outputs/agent/             Agent 生成的 Markdown 报告

src/
  constants.py             默认模型名、智谱 API Base
  config.py                环境变量与 JSON 输入解析
  agent/                   LangGraph Agent（工具、图、校验）
  integrations/ai/         智谱 OpenAI 兼容客户端与 Key 选择
  models/                  竞品等数据模型
  prompts/                 历史多步流程提示模板（当前主流程未使用）
  templates/               竞品资料填写参考

skills/                    PM 方法论技能库（Claude / Lenny 等），供人或 AI 辅助分析时引用
AGENTS.md                  给协作者与 AI 的详细说明（技能索引、启动命令）
```

---

## 方法论提示

- 叙事与功能并重，结论尽量有买家语境。  
- 先承认对手强项，再谈差异化更可信。  
- 多用可验证来源；AI 加速搜集，业务判断仍需人工交叉验证。  
- 竞品情报应持续更新，单次报告是快照而非终稿。

---

## 延伸阅读

- 环境变量逐项说明：`.env.example`  
- 技能库与项目约定：**[AGENTS.md](AGENTS.md)**
