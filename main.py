"""
竞争情报工具包 — 自动化主入口（面向产品经理）

运行方式（仅 LangGraph ReAct Agent：联网搜索 + 抓取 + 长文报告）:
    python main.py                               # 需已通过 --competitors 或 competitors_input.json 指定竞品
    python main.py --input my_input.json         # 结构化竞争对手输入文件
    python main.py --competitors A,B,C           # 快速指定竞争对手名称
    python main.py --dry-run                     # 仅验证配置与依赖，不执行 API 调用
    python main.py --competitors A,B --export-docx  # 报告生成后额外导出 Word（需本机 Pandoc）
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel

from src.config import Config
from src.redact import safe_error_message

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="竞争情报工具包 — AI 辅助竞争分析（Agent 自主研究）"
    )
    parser.add_argument(
        "--input",
        type=str,
        metavar="FILE",
        help="结构化竞争对手输入文件路径（JSON）",
    )
    parser.add_argument(
        "--competitors",
        type=str,
        help="快速指定竞争对手名称，逗号分隔",
    )
    parser.add_argument(
        "--market",
        type=str,
        help="覆盖市场/地区描述",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="验证配置、智谱 Key 与 Agent 依赖，不调用 API",
    )
    parser.add_argument(
        "--export-docx",
        action="store_true",
        help="Agent 报告保存为 Markdown 后，用 Pandoc 再导出同名的 .docx（需本机已安装 pandoc）",
    )
    return parser.parse_args()


def _print_competitors_table(config: Config) -> None:
    if not config.competitors:
        return
    from rich.table import Table

    table = Table(title="已加载竞争对手", show_header=True, header_style="bold cyan")
    table.add_column("名称", style="cyan")
    table.add_column("类别")
    table.add_column("官网文案", justify="center")
    table.add_column("销售情报", justify="center")
    for c in config.competitors:
        table.add_row(
            c.display_label(),
            c.category,
            "✓" if c.has_website_copy() else "—",
            "✓" if c.has_sales_intelligence() else "—",
        )
    console.print(table)
    console.print()


def main() -> None:
    args = parse_args()

    console.print(
        Panel.fit(
            "[bold]竞争情报工具包[/bold]\n"
            "LangGraph Agent · 联网检索 · 竞争情报长报告",
            border_style="cyan",
        )
    )

    config = Config(
        input_file=args.input,
        competitors_override=args.competitors,
        market_override=args.market,
    )

    if not config.competitor_list:
        console.print(
            "[red]✗ 请指定竞争对手："
            "--competitors A,B,C 或使用 --input competitors_input.json[/red]"
        )
        sys.exit(1)

    if not config.has_ai_key():
        console.print(
            "[red]✗ 未配置智谱AI Key，"
            "请在 .env 中设置 ZHIPU_API_KEY_1 / _2 / _3 / _4[/red]"
        )
        sys.exit(1)

    try:
        from src.agent.graph import run_agent
    except ImportError as e:
        console.print(
            f"[red]✗ Agent 依赖未安装: {safe_error_message(e, config)}\n"
            f"  请运行: pip install langgraph langchain-openai duckduckgo-search[/red]"
        )
        sys.exit(1)

    _print_competitors_table(config)

    if args.dry_run:
        console.print("[yellow]— Dry Run：配置与依赖校验通过，未调用 API[/yellow]\n")
        warnings = config.validate()
        for w in warnings:
            console.print(f"  [yellow]⚠ {w}[/yellow]")
        try:
            import playwright  # noqa: F401
        except ImportError:
            console.print(
                "  [yellow]⚠ 未安装 playwright；Agent 截图工具将不可用。"
                "请 pip install playwright 并执行 playwright install chromium[/yellow]"
            )
        if args.export_docx:
            import shutil

            if shutil.which("pandoc"):
                console.print("  [green]✓ 检测到 pandoc，可用于 --export-docx[/green]")
            else:
                console.print(
                    "  [yellow]⚠ 未检测到 pandoc；使用 --export-docx 前请先安装："
                    "https://pandoc.org/installing.html[/yellow]"
                )
        if not warnings:
            console.print("  [green]配置验证通过[/green]")
        sys.exit(0)

    try:
        run_agent(config, export_docx=args.export_docx)
    except Exception as e:
        console.print(f"[red]✗ Agent 运行失败: {safe_error_message(e, config)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
