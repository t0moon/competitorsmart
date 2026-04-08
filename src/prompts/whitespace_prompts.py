"""
Step 3 — 空白空间映射 Prompt 模板
"""


def identify_whitespace(product_category: str, narrative_matrix_output: str) -> str:
    return (
        f"Here is a summary of how the top competitors in {product_category} position themselves:\n\n"
        f"{narrative_matrix_output}\n\n"
        f"Based on this, identify:\n"
        f"1. The narrative territory that is most overcrowded.\n"
        f"2. The narrative gaps — what pain points or buyer anxieties is nobody addressing?\n"
        f"3. What outcomes are competitors hinting at but never quantifying?\n"
        f"4. If you were positioning a new entrant, what angle would give the clearest differentiation?"
    )


def positioning_axes_suggestion(product_category: str, buyer_profile: str) -> str:
    return (
        f"For a product in the {product_category} category targeting {buyer_profile}, "
        f"suggest the two most meaningful axes for a positioning whitespace map. "
        f"These axes should reflect what buyers in this segment care most about — "
        f"not what makes our product look best. "
        f"Common axes include: ease of use vs power, SMB vs enterprise focus, "
        f"breadth vs depth, speed vs accuracy, price vs capability."
    )
