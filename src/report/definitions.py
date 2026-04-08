"""
报告生成相关静态定义：步骤输出目录映射、章节模板、文件名标签。
"""

from __future__ import annotations

# Step 编号 → outputs 下子目录名（与 BaseStep 保存路径一致：类名小写）
STEP_DIR_MAP: dict[int, str] = {
    1: "landscapemapper",
    2: "narrativeanalyzer",
    3: "whitespacemapper",
}

# 中间产物文件名关键词 → 报告内展示标题
FILE_LABEL_MAP: dict[str, str] = {
    "landscape_overview": "竞争格局概述",
    "funding_signals": "融资与招聘信号",
    "narrative_matrix": "叙事矩阵",
    "narrative_": "叙事深度分析",
    "archetype_": "叙事原型识别",
    "whitespace_analysis": "空白空间分析",
    "positioning_axes": "定位坐标轴建议",
}

# 深度报告 11 章：idx 与 API 轮转章节号一致
CHAPTER_SPECS: list[dict[str, str]] = [
    {"idx": "1", "title": "一、报告概述（Executive Summary）", "must": "研究目标、研究范围、3-5条核心结论、关键机会点"},
    {"idx": "2", "title": "二、市场与赛道分析（Market Context）", "must": "TAM/SAM/SOM、增长趋势、赛道细分、价值链、关键驱动因素"},
    {"idx": "3", "title": "三、竞品选择与分层（Competitive Landscape）", "must": "筛选逻辑、分层、2x2定位地图"},
    {"idx": "4", "title": "四、核心能力拆解（Product Capability Analysis）", "must": "4.1功能结构、4.2技术能力、4.3用户体验，并逐个竞品对比"},
    {"idx": "5", "title": "五、商业模式分析（Monetization）", "must": "收费模式、定价对比、成本结构、ARPU估算"},
    {"idx": "6", "title": "六、增长与分发策略（Growth Strategy）", "must": "渠道、获取方式、转化策略"},
    {"idx": "7", "title": "七、用户与场景分析（User & Use Case）", "must": "目标用户画像、场景、高频/低频、动机、痛点"},
    {"idx": "8", "title": "八、优劣势对比（SWOT / 对比矩阵）", "must": "各竞品 SWOT + 横向对比矩阵"},
    {"idx": "9", "title": "九、关键差异与壁垒（Moat Analysis）", "must": "技术、产品、渠道、品牌/社区壁垒"},
    {"idx": "10", "title": "十、机会点与策略建议（Opportunities）", "must": "可切入机会、产品策略、增长策略、商业化策略、P0/P1/P2"},
    {"idx": "11", "title": "十一、数据附录（Appendix）", "must": "数据来源、测试方法、证据材料与可信度声明"},
]
