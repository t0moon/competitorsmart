"""
Step 2 — 叙事分析 Prompt 模板
"""


def narrative_matrix(competitors_copy: str) -> str:
    """
    :param competitors_copy: 多个竞争对手官网文案，格式化后的字符串
    """
    return (
        "I'm going to give you the homepage and key landing page copy for multiple competitors. "
        "For each one, complete this narrative matrix:\n"
        "- Core claim\n"
        "- Primary emotion\n"
        "- Who is the hero (product or customer?)\n"
        "- What is the villain / enemy\n"
        "- What proof mechanism do they use\n"
        "- What do they NEVER mention\n\n"
        f"Here is the copy:\n{competitors_copy}"
    )


def narrative_archetype(competitor_name: str, summary: str) -> str:
    """识别叙事原型：效率型、成长型、风险型、简洁型、智能型、社区型"""
    return (
        f"Based on the following positioning summary for {competitor_name}, "
        f"which narrative archetype best describes their positioning?\n"
        f"Options: THE EFFICIENCY PLAY / THE GROWTH PLAY / THE RISK PLAY / "
        f"THE SIMPLICITY PLAY / THE INTELLIGENCE PLAY / THE COMMUNITY PLAY\n"
        f"Explain your reasoning and identify the secondary archetype if present.\n\n"
        f"Summary:\n{summary}"
    )
