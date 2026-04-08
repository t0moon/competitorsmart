"""
竞争对手数据模型 — 支持结构化输入
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional


CompetitorCategory = Literal["direct", "indirect", "adjacent", "status_quo"]


@dataclass
class CompetitorInfo:
    """单个竞争对手的完整信息结构"""

    # ── 必填 ────────────────────────────────────────────────────
    name: str

    # ── 基础信息 ─────────────────────────────────────────────────
    category: CompetitorCategory = "direct"
    website: str = ""
    founded: str = ""
    stage_size: str = ""
    primary_market: str = ""
    funding: str = ""
    crunchbase_permalink: str = ""

    # ── 官网/落地页文案（粘贴后直接用于叙事分析，无需占位符）──
    website_copy: str = ""

    # ── 销售情报 ─────────────────────────────────────────────────
    sales_notes: str = ""        # 销售团队对该竞争对手的笔记
    win_loss_notes: str = ""     # 胜负访谈摘要

    # ── 额外标签 ─────────────────────────────────────────────────
    geography: str = ""
    industry_focus: str = ""
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "CompetitorInfo":
        """从字典（JSON 解析结果）构建实例，忽略多余字段"""
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def has_website_copy(self) -> bool:
        return bool(self.website_copy and self.website_copy.strip())

    def has_sales_intelligence(self) -> bool:
        return bool(self.sales_notes or self.win_loss_notes)

    def display_label(self) -> str:
        category_map = {
            "direct": "直接竞争",
            "indirect": "间接竞争",
            "adjacent": "邻近竞争",
            "status_quo": "现状/惯性",
        }
        cat = category_map.get(self.category, self.category)
        return f"{self.name} [{cat}]"
