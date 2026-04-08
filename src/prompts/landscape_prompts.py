"""
Step 1 — 景观映射 Prompt 模板
"""


def landscape_overview(product_category: str, market: str, geography: str = "", company_size: str = "") -> str:
    geo_part = f" Focus on {geography} geography." if geography else ""
    size_part = f" Target {company_size} company segments." if company_size else ""
    return (
        f"Give me a comprehensive overview of the competitive landscape for "
        f"{product_category} in {market}. Include the main players, their positioning, "
        f"target customers, and any recent market developments.{geo_part}{size_part}"
    )


def funding_and_hiring(competitors: list[str]) -> str:
    names = ", ".join(competitors)
    return (
        f"Which of these competitors has raised funding in the last 12 months, "
        f"and what does their recent hiring activity suggest about their strategic direction? "
        f"Competitors: {names}"
    )


def competitor_narrative_deep_dive(competitor_name: str, copy_text: str) -> str:
    return (
        f"Analyse this competitor's messaging for {competitor_name}. "
        f"What core value proposition are they making? "
        f"Who are they speaking to? "
        f"What emotional triggers are they using? "
        f"What are they NOT saying? "
        f"What objections are they preemptively addressing?\n\n"
        f"Copy:\n{copy_text}"
    )


def buyer_type_analysis(competitor_name: str, copy_text: str) -> str:
    return (
        f"Based on this messaging from {competitor_name}, what type of buyer are they optimising for — "
        f"technical evaluator, economic buyer, or end user? "
        f"What does that tell us about where they're weakest?\n\n"
        f"Copy:\n{copy_text}"
    )


def win_loss_synthesis(sales_notes: str) -> str:
    return (
        f"Here are notes from sales conversations and lost deal analyses where competitors were mentioned. "
        f"Identify: "
        f"(1) the top 3 recurring objections raised against us when competitors were in the evaluation, "
        f"(2) the top 3 reasons buyers chose competitors over us, "
        f"(3) any language patterns buyers used repeatedly that we should incorporate into our own positioning.\n\n"
        f"Notes:\n{sales_notes}"
    )


def monthly_signal_brief(competitor: str, recent_updates: str) -> str:
    return (
        f"Here are the latest news, job postings, and content updates from {competitor} over the past month. "
        f"What do these signals suggest about their strategic direction? "
        f"Are there any shifts in their positioning, target market, or product focus I should be aware of?\n\n"
        f"Updates:\n{recent_updates}"
    )
