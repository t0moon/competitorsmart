"""
Step 2 — 叙事分析
目标：构建跨竞争对手叙事矩阵，识别各自的叙事原型
"""

from __future__ import annotations
from src.integrations.ai.openai_client import get_best_available_client
from src.prompts import narrative_prompts
from src.steps.base_step import BaseStep


NARRATIVE_MATRIX_TEMPLATE = """
# 叙事矩阵

| 元素 | {headers} |
|------|{sep}|
| 核心权利要求 | {core_claim} |
| 主要情感 | {primary_emotion} |
| 故事的英雄 | {hero} |
| 反派 / 敌人 | {villain} |
| 证明机制 | {proof} |
| 从未提及的 | {never_mentions} |
"""


class NarrativeAnalyzer(BaseStep):

    def run(self) -> None:
        competitors = self.config.competitor_list
        if not competitors:
            self.log("[yellow]未设置竞争对手列表，跳过 Step 2[/yellow]")
            return

        # 构建叙事矩阵
        self.log("[bold]构建叙事矩阵[/bold]")
        matrix_result = self._build_narrative_matrix(competitors)
        self.save_output("narrative_matrix.md", matrix_result)

        # 识别叙事原型
        self.log("[bold]识别叙事原型[/bold]")
        for competitor in competitors:
            self.log(f"  分析原型: [cyan]{competitor}[/cyan]")
            archetype = self._identify_archetype(competitor, matrix_result)
            self.save_output(f"archetype_{competitor.replace(' ', '_')}.md", archetype)

    def _build_narrative_matrix(self, competitors: list[str]) -> str:
        """
        调用 AI 分析叙事矩阵。
        实际使用中需要用户提供各竞争对手的官网文案。
        """
        ai = get_best_available_client(self.config, step="narrative")

        placeholder_copies = "\n\n".join(
            f"=== {c} ===\n[请将 {c} 的主页文案粘贴到此处]"
            for c in competitors
        )
        prompt = narrative_prompts.narrative_matrix(placeholder_copies)
        return ai.complete(prompt)

    def _identify_archetype(self, competitor: str, matrix_summary: str) -> str:
        ai = get_best_available_client(self.config, step="narrative")
        prompt = narrative_prompts.narrative_archetype(competitor, matrix_summary)
        return ai.complete(prompt)
