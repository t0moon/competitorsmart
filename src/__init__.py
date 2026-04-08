"""
competitorsmart / 竞争情报工具包 — 源码包

目录职责
--------
config          环境变量与 competitors_input.json 解析
constants       全局常量（模型名、默认 API Base）
agent/          LangGraph ReAct：搜索 + 抓取 + 单份长报告（主流程）
integrations/   外部服务（智谱 GLM、Crunchbase 等）
prompts/        历史三步流程遗留的英文 prompt 模板（当前主流程未引用）
models/         结构化竞品数据模型
templates/      人工填写用的 Markdown 模板（不参与 import 链）
"""
