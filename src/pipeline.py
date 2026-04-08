"""
三步分析管线 — 注册 Step 与展示名称，供 main 调度。

架构位置：
  main.py          CLI 入口、参数解析
  pipeline.py      Step 注册表（本模块）
  steps/           各 Step 实现（写 outputs/<StepClass>/）
  report/          读取上述输出，按章节 API 拼最终 Markdown
  agent/           LangGraph 自主检索模式（与 pipeline 并行，互不依赖）
"""

from __future__ import annotations

from typing import Type

from src.steps.base_step import BaseStep
from src.steps.step01_landscape import LandscapeMapper
from src.steps.step02_narrative import NarrativeAnalyzer
from src.steps.step03_whitespace import WhitespaceMapper

# Step 编号 → (控制台展示名, 步骤类)
STEPS: dict[int, tuple[str, Type[BaseStep]]] = {
    1: ("景观映射", LandscapeMapper),
    2: ("叙事分析", NarrativeAnalyzer),
    3: ("空白空间映射", WhitespaceMapper),
}
