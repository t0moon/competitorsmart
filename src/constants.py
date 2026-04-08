"""
项目级常量 — 避免模型名、Base URL 在多处硬编码分叉。
"""

# 智谱 OpenAI 兼容接口默认模型（与 .env.example 说明一致）
ZHIPU_DEFAULT_MODEL = "GLM-4.6V-FlashX"

# 智谱 API Base（可被环境变量 ZHIPU_API_BASE_URL 覆盖）
ZHIPU_DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
