"""
Step 1 — 景观映射
目标：识别竞争群体，为每个竞争对手生成基础资料，综合融资/招聘信号
"""

from __future__ import annotations
from src.integrations.ai.openai_client import get_best_available_client
from src.models.competitor import CompetitorInfo
from src.redact import safe_error_message
from src.prompts import landscape_prompts
from src.steps.base_step import BaseStep


class LandscapeMapper(BaseStep):

    def run(self) -> None:
        config = self.config
        competitors = config.competitors          # 结构化列表（含详细信息）
        market = config.market or config.default_product_category

        if not competitors:
            self.log("[yellow]未设置竞争对手列表，跳过 Step 1[/yellow]")
            return

        # Phase A: 竞争格局综合（Perplexity 联网搜索）
        self.log("[bold]Phase A — 竞争格局综合[/bold]")
        overview = self._landscape_overview(market, competitors)
        self.save_output("landscape_overview.md", overview)

        # Phase B: 逐个竞争对手叙事分析（LLM 分析）
        self.log("[bold]Phase B — 竞争对手叙事分析[/bold]")
        for competitor in competitors:
            self.log(f"  分析竞争对手: [cyan]{competitor.display_label()}[/cyan]")
            self._analyze_competitor_narrative(competitor)

        # Phase C: 融资与招聘信号
        self.log("[bold]Phase C — 融资与招聘信号[/bold]")
        funding_signals = self._get_funding_signals(competitors)
        if funding_signals:
            self.save_output("funding_signals.md", funding_signals)

    def _landscape_overview(self, market: str, competitors: list[CompetitorInfo]) -> str:
        names = [c.name for c in competitors]
        ai = get_best_available_client(self.config, step="landscape")

        prompt = landscape_prompts.landscape_overview(
            product_category=self.config.default_product_category or market,
            market=market,
            geography=self.config.input_geography,
            company_size=self.config.input_company_size,
        )
        result = ai.complete(prompt)

        funding_prompt = landscape_prompts.funding_and_hiring(names)
        funding_info = ai.complete(funding_prompt)

        return f"# 竞争格局概述\n\n{result}\n\n## 融资与招聘动态\n\n{funding_info}"

    def _analyze_competitor_narrative(self, competitor: CompetitorInfo) -> None:
        """
        叙事分析：若输入文件中已提供官网文案则直接使用，
        否则生成占位符模板供用户填写后重新运行。
        """
        ai = get_best_available_client(self.config, step="landscape")

        if competitor.has_website_copy():
            copy_text = competitor.website_copy
            self.log(f"    [green]已使用输入文件中的官网文案[/green]")
        else:
            copy_text = (
                f"[请将 {competitor.name} 的主页和核心落地页文案粘贴到 "
                f"competitors_input.json 的 website_copy 字段中，然后重新运行]"
            )
            self.log(f"    [yellow]未提供官网文案，生成占位符模板[/yellow]")

        prompt = landscape_prompts.competitor_narrative_deep_dive(competitor.name, copy_text)
        analysis = ai.complete(prompt)

        # 追加销售情报摘要（若存在）
        if competitor.has_sales_intelligence():
            sales_section = "\n\n---\n\n## 销售情报（来自输入文件）\n\n"
            if competitor.sales_notes:
                sales_section += f"**销售笔记：** {competitor.sales_notes}\n\n"
            if competitor.win_loss_notes:
                sales_section += f"**胜负分析：** {competitor.win_loss_notes}\n"
            analysis += sales_section

        self.save_output(f"narrative_{competitor.name.replace(' ', '_')}.md", analysis)

    def _get_funding_signals(self, competitors: list[CompetitorInfo]) -> str:
        from src.integrations.monitoring.crunchbase import CrunchbaseClient
        client = CrunchbaseClient(self.config.crunchbase_api_key)
        if not client.is_available():
            return ""

        lines = ["# 融资信号追踪\n"]
        for competitor in competitors:
            # 优先使用输入文件中指定的 crunchbase_permalink
            permalink = (
                competitor.crunchbase_permalink
                or competitor.name.lower().replace(" ", "-")
            )
            try:
                rounds = client.get_recent_funding_rounds(permalink, limit=3)
                if rounds:
                    summary = client.format_funding_summary(rounds)
                    lines.append(f"## {competitor.name}\n{summary}\n")
            except Exception as e:
                self.log(
                    f"  [dim]Crunchbase 查询 {competitor.name} 失败: "
                    f"{safe_error_message(e, self.config)}[/dim]"
                )
        return "\n".join(lines)
