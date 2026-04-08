# 竞争情报工具包 — AI Agent 指南

## 项目概述

本项目是一个 AI 辅助竞争情报（Competitive Intelligence）分析工具，面向产品经理（PMM）。  
核心能力：竞争格局映射 → 叙事分析 → 空白空间识别。

## 技能库（Skills）

项目内置两套产品经理技能库，位于 `skills/` 目录，AI 可直接读取并调用。

### 使用方式

当用户提出相关任务时，**优先读取对应 SKILL.md，按其中的指令执行**，不要忽略 skills 直接凭经验回答。

---

## skills/claude-skills — 商业测试验证技能

已在商业环境实测，质量较高。

| 技能目录 | SKILL.md 路径 | 触发场景 |
|---------|--------------|---------|
| **竞品分析** | `skills/claude-skills/competitive-analysis/SKILL.md` | 用户要求做竞品分析、竞品对比、竞争对手研究，或分析多个产品/公司 |
| **PRD 生成** | `skills/claude-skills/prd-generator/SKILL.md` | 用户要求写 PRD、产品需求文档、功能规格，或从产品想法生成文档 |

---

## skills/lenny-pm-skills — Lenny 产品经理全技能库

覆盖产品经理工作的全生命周期，共 86 个技能。

### 产品策略与定位

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 问题定义 | `skills/lenny-pm-skills/01-问题定义-problem-definition/SKILL.md` | 帮我定义/拆解这个产品问题 |
| 产品愿景 | `skills/lenny-pm-skills/04-产品愿景-product-vision/SKILL.md` | 帮我制定产品愿景/使命 |
| 北极星指标 | `skills/lenny-pm-skills/05-北极星指标-north-star-metrics/SKILL.md` | 帮我找北极星指标/核心度量 |
| OKR 设定 | `skills/lenny-pm-skills/06-OKR目标设定-okrs-goals/SKILL.md` | 帮我制定 OKR/目标 |
| 路线图优先级 | `skills/lenny-pm-skills/07-路线图优先级-roadmap-prioritization/SKILL.md` | 帮我排优先级/做路线图 |
| 权衡取舍 | `skills/lenny-pm-skills/08-权衡取舍-trade-offs/SKILL.md` | 帮我分析这个决策的取舍 |
| 范围裁剪 | `skills/lenny-pm-skills/11-范围裁剪-scoping-cutting/SKILL.md` | 帮我裁减功能范围/定义 MVP |
| 产品发布 | `skills/lenny-pm-skills/12-产品发布-shipping/SKILL.md` | 帮我规划产品上线/发布 |
| 逆向工作法 | `skills/lenny-pm-skills/17-逆向工作法-working-backwards/SKILL.md` | 帮我从用户价值倒推需求 |
| PMF 测量 | `skills/lenny-pm-skills/54-PMF测量-product-market-fit/SKILL.md` | 帮我评估产品市场契合度 |
| 定位策略 | `skills/lenny-pm-skills/60-定位策略-positioning/SKILL.md` | 帮我做产品定位/差异化 |

### 用户研究

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 用户访谈 | `skills/lenny-pm-skills/02-用户访谈-user-interviews/SKILL.md` | 帮我设计用户访谈/准备问题 |
| 用户反馈分析 | `skills/lenny-pm-skills/03-用户反馈分析-feedback-analysis/SKILL.md` | 帮我分析用户反馈/评论 |
| 问卷设计 | `skills/lenny-pm-skills/18-问卷设计-designing-surveys/SKILL.md` | 帮我设计用户调研问卷 |
| 可用性测试 | `skills/lenny-pm-skills/19-可用性测试-usability-testing/SKILL.md` | 帮我规划可用性测试 |
| 行为设计 | `skills/lenny-pm-skills/23-行为设计-behavioral-design/SKILL.md` | 帮我优化用户行为/习惯养成 |
| 用户引导 | `skills/lenny-pm-skills/59-用户引导-user-onboarding/SKILL.md` | 帮我设计用户 onboarding |

### 竞品与市场分析

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 竞品分析 | `skills/lenny-pm-skills/09-竞品分析-competitive-analysis/SKILL.md` | 帮我做竞品分析 |
| 市场定价 | `skills/lenny-pm-skills/56-定价策略-pricing/SKILL.md` | 帮我制定/分析定价策略 |
| 平台策略 | `skills/lenny-pm-skills/49-平台策略-platform-strategy/SKILL.md` | 帮我思考平台策略 |
| 集市场景 | `skills/lenny-pm-skills/58-集市场景-marketplace/SKILL.md` | 帮我分析双边市场 |

### 文档写作

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| PRD 撰写 | `skills/lenny-pm-skills/10-PRD撰写-writing-prds/SKILL.md` | 帮我写 PRD |
| 规格文档 | `skills/lenny-pm-skills/16-规格文档-writing-specs-designs/SKILL.md` | 帮我写功能规格/设计文档 |
| 书面沟通 | `skills/lenny-pm-skills/14-书面沟通-written-communication/SKILL.md` | 帮我写对齐邮件/文档 |
| 演讲展示 | `skills/lenny-pm-skills/52-演讲展示-presentations/SKILL.md` | 帮我准备 PPT/演讲 |

### 增长与运营

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 增长循环 | `skills/lenny-pm-skills/55-增长循环-growth-loops/SKILL.md` | 帮我设计增长飞轮/循环 |
| 用户留存 | `skills/lenny-pm-skills/57-用户留存-retention/SKILL.md` | 帮我分析/提升留存 |
| 产品运营 | `skills/lenny-pm-skills/22-产品运营-product-operations/SKILL.md` | 帮我规划产品运营 |
| 品牌故事 | `skills/lenny-pm-skills/61-品牌故事-brand-storytelling/SKILL.md` | 帮我做品牌叙事 |
| 发布营销 | `skills/lenny-pm-skills/62-发布营销-launch-marketing/SKILL.md` | 帮我规划上线营销 |
| 内容营销 | `skills/lenny-pm-skills/63-内容营销-content-marketing/SKILL.md` | 帮我做内容营销策略 |

### AI 与技术

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| AI 产品策略 | `skills/lenny-pm-skills/46-AI产品策略-ai-strategy/SKILL.md` | 帮我制定 AI 产品策略 |
| LLM 构建 | `skills/lenny-pm-skills/47-LLM构建-building-llms/SKILL.md` | 帮我规划 LLM 产品 |
| AI 评测 | `skills/lenny-pm-skills/51-AI评测-ai-evals/SKILL.md` | 帮我设计 AI 模型评测 |
| 技术评估 | `skills/lenny-pm-skills/48-技术评估-evaluating-tech/SKILL.md` | 帮我评估技术方案 |
| 技术债务 | `skills/lenny-pm-skills/81-技术债务-tech-debt/SKILL.md` | 帮我分析/处理技术债 |

### 团队与管理

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 利益相关者对齐 | `skills/lenny-pm-skills/13-利益相关者对齐-stakeholder-alignment/SKILL.md` | 帮我做跨部门对齐 |
| 高效会议 | `skills/lenny-pm-skills/15-高效会议-effective-meetings/SKILL.md` | 帮我设计/改善会议 |
| 一对一谈话 | `skills/lenny-pm-skills/33-一对一谈话-1-1s/SKILL.md` | 帮我准备 1:1 |
| 困难对话 | `skills/lenny-pm-skills/34-困难对话-difficult-conversations/SKILL.md` | 帮我准备困难谈话 |
| 跨部门协作 | `skills/lenny-pm-skills/40-跨部门协作-cross-functional/SKILL.md` | 帮我处理跨部门问题 |
| 决策流程 | `skills/lenny-pm-skills/37-决策流程-decision-processes/SKILL.md` | 帮我设计决策框架 |

### 创业与融资

| 技能 | 路径 | 触发场景 |
|-----|------|---------|
| 创业思考 | `skills/lenny-pm-skills/24-创业思考-startup-ideation/SKILL.md` | 帮我验证/分析创业想法 |
| 融资准备 | `skills/lenny-pm-skills/72-融资准备-fundraising/SKILL.md` | 帮我准备融资/BP |
| 创始人销售 | `skills/lenny-pm-skills/73-创始人销售-founder-sales/SKILL.md` | 帮我做早期销售 |
| 企业销售 | `skills/lenny-pm-skills/75-企业销售-enterprise-sales/SKILL.md` | 帮我拓展企业客户 |

---

## 本项目核心文件

| 文件/目录 | 说明 |
|----------|------|
| `main.py` | 主入口，运行 `python main.py` 启动分析流程 |
| `src/pipeline.py` | 三步 Step 注册表（编号→类），`main` 只从这里取 `STEPS` |
| `src/constants.py` | 全局常量：默认模型名、智谱 API Base URL（单一来源） |
| `src/agent/graph.py` | LangGraph ReAct Agent，使用 GLM + DuckDuckGo 自主研究竞品 |
| `src/steps/` | 三步分析流程（景观映射→叙事分析→空白空间识别） |
| `src/report/` | 读取 Step 输出目录，按 11 章 + 多 Key 轮转生成总报告 |
| `src/report/definitions.py` | 报告章节定义、Step 输出目录映射、文件名标签 |
| `src/prompts/` | 各步骤 AI prompt 模板 |
| `competitors_input.json` | 结构化竞争对手输入文件（复制并填写） |
| `outputs/` | 所有分析输出（Markdown 报告） |
| `.env.example` | 环境变量模板，复制为 `.env` 并填入 API Key |

## 快速启动

```bash
# 1. 配置环境
cp .env.example .env   # 填入 ZHIPU_API_KEY_1 等

# 2. 安装依赖
pip install -r requirements.txt

# 3a. 使用 Agent 模式（自动联网搜索）
python main.py --agent --competitors "竞品A,竞品B" --market "SaaS CRM"

# 3b. 使用结构化输入（提供官网文案）
python main.py --input competitors_input.json
```
