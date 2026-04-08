"""
competitorsmart / 竞争情报工具包 — 源码包

目录职责
--------
config          环境变量与 competitors_input.json 解析
constants       全局常量（模型名、默认 API Base）
pipeline        三步分析 Step 注册（main 只依赖此处枚举 Step）
steps/          Step1 景观映射、Step2 叙事、Step3 空白空间（落盘 outputs/）
report/         读取 Step 产物，按 11 章模板 + 多 Key 轮转调用 API 生成总报告
agent/          LangGraph ReAct：搜索 + 抓取 + 单份长报告（与 report 流程独立）
integrations/   外部服务（智谱 GLM、Crunchbase 等）
prompts/        各 Step 的英文 prompt 模板
models/         结构化竞品数据模型
templates/      人工填写用的 Markdown 模板（不参与 import 链）
"""
