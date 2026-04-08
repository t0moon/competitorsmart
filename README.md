# 竞争情报工具包

面向产品经理（PMM）的 **AI 辅助竞品分析** 工具：自动完成「竞争格局 → 叙事分析 → 空白空间」三步，并可选 **联网 Agent** 或 **11 章深度报告**（按章节调用 API、多 Key 负载均衡）。

---

## 能做什么

| 能力 | 说明 |
|------|------|
| **三步分析** | Step1 景观映射、Step2 叙事分析、Step3 空白空间；结果写入 `outputs/<步骤类名>/` |
| **最终报告** | 读取上述输出，生成 **11 章** Markdown 竞品调研报告（市场、分层、能力、商业化、增长、SWOT、壁垒、策略、附录等） |
| **多 Key 轮转** | 支持 `ZHIPU_API_KEY_1`～`_4`；报告按章节在已配置的 Key 间轮转，减轻单 Key 限流 |
| **Agent 模式** | LangGraph ReAct：DuckDuckGo 搜索 + 网页抓取 + 长文竞争情报报告（需单独满足 Agent 的完整性与字数规则） |
| **结构化输入** | 通过 `competitors_input.json` 提供竞品名称、类别、官网文案、销售笔记等，提升 Step 质量 |

默认大模型与 Base URL 在 **`src/constants.py`** 统一配置（当前默认：`GLM-4.6V-FlashX`）。

---

## 快速开始

### 1. 环境

```bash
cp .env.example .env
```

在 `.env` 中至少填写 **`ZHIPU_API_KEY_1`**（建议同时配置 `_2`、`_3`，报告生成更稳；可选 `_4` 做章节轮转扩容）。

**推送到 Git 前：** 勿提交 `.env`；仓库里只保留无真实值的 `.env.example`。初始化仓库后建议启用钩子，防止误提交环境文件：

```bash
git config core.hooksPath githooks
```

推送前可执行 `git check-ignore -v .env`，应显示 `.env` 已被忽略。

### 推送到 GitHub（本机执行）

官方空仓库：[**t0moon/competitorsmart**](https://github.com/t0moon/competitorsmart)（`https://github.com/t0moon/competitorsmart.git`）。

在已安装 Git 的终端中，于项目根目录执行（将邮箱、姓名改成你的）：

```bash
git config user.email "你的邮箱"
git config user.name "你的名字"
git init -b main
git config core.hooksPath githooks
git add -A
git commit -m "chore: 初始化竞争情报工具仓库（.env 忽略、提交钩子、密钥脱敏）"
git remote add origin https://github.com/t0moon/competitorsmart.git
git push -u origin main
```

若已存在 `origin`，改用：`git remote set-url origin https://github.com/t0moon/competitorsmart.git` 再 `git push -u origin main`。

**PowerShell 一键（提交并推送）：**

```powershell
.\scripts\init-and-commit.ps1 -Email "你的邮箱" -Name "你的名字" -RemoteUrl "https://github.com/t0moon/competitorsmart.git" -Push
```

首次 `push` 时 GitHub 会要求登录；HTTPS 请使用 **Personal Access Token** 作为密码。

### 2. 依赖

```bash
pip install -r requirements.txt
```

Agent 模式若缺依赖，按报错安装，例如：

```bash
pip install langgraph langchain-openai duckduckgo-search
```

### 3. 常用命令

```bash
# 完整跑三步 + 自动生成最终 Markdown 报告
python main.py

# 指定竞品名称（逗号分隔，无官网文案时 Step 会提示补全）
python main.py --competitors "竞品A,竞品B" --market "你的赛道描述"

# 使用结构化输入（推荐：含 website_copy 等）
python main.py --input competitors_input.json

# 只跑某一步
python main.py --step 1

# 已有 Step 输出时，只生成报告（11 章 API 合成）
python main.py --report-only

# 跑完三步但不生成汇总报告
python main.py --no-report

# 校验配置、不调用 API
python main.py --dry-run

# Agent：自主联网研究（需配置智谱 Key）
python main.py --agent --competitors "竞品A,竞品B" --market "赛道描述"
```

报告默认输出在 **`outputs/`**，Agent 报告在 **`outputs/agent/`**。

---

## 项目结构（源码）

```
main.py                 CLI 入口
competitors_input.json  竞品结构化输入（可选）
outputs/                所有生成物

src/
  constants.py          默认模型名、智谱 API Base（单一来源）
  config.py             .env + JSON 输入解析
  pipeline.py           三步 Step 注册表（STEPS）
  steps/                Step1/2/3 实现
  prompts/              各 Step 的 LLM 提示模板
  report/
    definitions.py      11 章定义、Step 输出目录映射
    report_generator.py 按章调用 API 拼最终报告
  agent/                LangGraph Agent（搜索 + 抓取 + 长报告）
  integrations/ai/      智谱 OpenAI 兼容客户端与 Key 选择
  models/               竞品数据模型
  templates/              人工填写参考（如 competitor_profile.md）
```

更细的协作说明见 **`AGENTS.md`**（给 AI / 协作者用）。

---

## 输入说明

- **`--competitors`**：仅名称列表，适合快速试跑；无官网文案时叙事类 Step 质量受限。
- **`competitors_input.json`**：可写 `market`、`product_category`、`competitors[].name`、`category`、`website_copy`、`sales_notes` 等，与 `Config` 加载逻辑一致。
- 竞品资料模板可参考 **`src/templates/competitor_profile.md`**。

---

## 方法论摘要（为何不是功能表）

1. **叙事与功能同样重要**：买家更容易记住「故事」而非功能列表。  
2. **诚实看待对手强项**：再谈差异化才可信。  
3. **用买家原话**：来自访谈、工单、评测的语言优于内部营销话。  
4. **竞品情报要持续更新**：一次性画布会过时。  
5. **AI 加速、人做判断**：输出需用业务事实与用户洞察交叉验证。

---

## 注意事项

- **API 额度**：若返回余额不足或限流，报告章节可能失败占位；可配置多个 Key 或稍后重试 `--report-only`。  
- **Agent 模式**对最终报告有完整性校验（章节、字数、来源等），运行时间可能较长。  
- **勿将 `.env` 或 Key 提交到 Git**（仓库已 `.gitignore` 忽略 `.env`）。

完整环境变量说明见 **[`.env.example`](.env.example)**。
