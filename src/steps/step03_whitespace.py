"""
Step 3 — 空白空间映射
目标：识别叙事空白，找到定位差异化机会
"""

from __future__ import annotations
from pathlib import Path
from src.integrations.ai.openai_client import get_best_available_client
from src.prompts import whitespace_prompts
from src.steps.base_step import BaseStep


class WhitespaceMapper(BaseStep):

    def run(self) -> None:
        competitors = self.config.competitor_list
        market = self.config.market or self.config.default_product_category

        # 读取 Step 2 的叙事矩阵输出（如果存在）
        narrative_output = self._load_narrative_matrix()

        self.log("[bold]识别叙事空白[/bold]")
        whitespace = self._identify_whitespace(market, narrative_output, competitors)
        self.save_output("whitespace_analysis.md", whitespace)

        self.log("[bold]推荐定位坐标轴[/bold]")
        axes = self._suggest_axes(market)
        self.save_output("positioning_axes.md", axes)

    def _load_narrative_matrix(self) -> str:
        """尝试加载上一步生成的叙事矩阵文件"""
        narrative_dir = self.config.output_dir / "narrativeanalyzer"
        if narrative_dir.exists():
            files = sorted(narrative_dir.glob("*narrative_matrix.md"), reverse=True)
            if files:
                self.log(f"  [dim]加载叙事矩阵: {files[0].name}[/dim]")
                return files[0].read_text(encoding="utf-8")
        self.log("  [yellow]未找到叙事矩阵文件，使用占位符[/yellow]")
        return "[Step 2 叙事矩阵输出将显示在这里]"

    def _identify_whitespace(
        self, market: str, narrative_output: str, competitors: list[str]
    ) -> str:
        ai = get_best_available_client(self.config, step="whitespace")
        prompt = whitespace_prompts.identify_whitespace(market, narrative_output)
        result = ai.complete(prompt)

        header = f"# 空白空间分析\n\n**市场：** {market}\n**竞争对手：** {', '.join(competitors)}\n\n"
        return header + result

    def _suggest_axes(self, market: str) -> str:
        ai = get_best_available_client(self.config, step="whitespace")
        buyer_profile = "B2B SaaS buyers"
        prompt = whitespace_prompts.positioning_axes_suggestion(market, buyer_profile)
        result = ai.complete(prompt)
        return f"# 定位坐标轴建议\n\n{result}"
