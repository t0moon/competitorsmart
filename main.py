"""
竞争情报工具包 — 自动化主入口（面向产品经理）

运行方式:
    python main.py                               # 执行完整流程（景观→叙事→空白空间），并生成最终竞争分析报告
    python main.py --input my_input.json         # 指定结构化竞争对手输入文件
    python main.py --step 1                      # 仅执行某一步（1/2/3）
    python main.py --competitors A,B,C           # 快速指定竞争对手名称（无详情）
    python main.py --dry-run                     # 仅验证配置，不执行 API 调用
    python main.py --report-only                 # 跳过步骤执行，仅汇总已有输出生成报告
    python main.py --no-report                   # 执行步骤后不生成汇总报告

    ── Agent 模式（LangGraph ReAct，自主搜索 + 分析）──
    python main.py --agent                       # 自主搜集信息并生成报告（需配置 ZHIPU_API_KEY）
    python main.py --agent --competitors A,B,C   # 指定竞品，Agent 自主研究
    python main.py --agent --input my_input.json # 从 JSON 文件读取竞品，Agent 自主研究
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel

from src.config import Config
from src.pipeline import STEPS
from src.redact import safe_error_message
from src.report.report_generator import generate_report

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="竞争情报工具包 — AI 辅助竞争分析自动化（面向产品经理）"
    )
    parser.add_argument(
        "--step",
        type=int,
        choices=list(STEPS.keys()),
        help="仅执行指定步骤 (1/2/3)，默认执行全部",
    )
    parser.add_argument(
        "--input",
        type=str,
        metavar="FILE",
        help="结构化竞争对手输入文件路径（JSON），包含名称、官网文案、销售笔记等详情",
    )
    parser.add_argument(
        "--competitors",
        type=str,
        help="快速指定竞争对手名称，逗号分隔（无详细信息时使用）",
    )
    parser.add_argument(
        "--market",
        type=str,
        help="覆盖市场/地区描述",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="验证配置和连接，不执行实际 API 调用",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="跳过所有执行步骤，仅将已有输出汇总为最终竞争分析报告",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="执行步骤后不生成汇总报告",
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        help=(
            "[Agent 模式] 使用 LangGraph ReAct Agent 自主搜索网络、"
            "抓取竞品官网、分析并生成报告（无需手动提供官网文案）"
        ),
    )
    return parser.parse_args()


def run_step(step_num: int, step_class, config: Config, dry_run: bool) -> bool:
    step_name, _ = STEPS[step_num]
    console.rule(f"[bold cyan]Step {step_num} — {step_name}")
    try:
        runner = step_class(config)
        if dry_run:
            runner.validate()
        else:
            runner.run()
        console.print(f"[green]✓ Step {step_num} 完成[/green]\n")
        return True
    except Exception as e:
        console.print(f"[red]✗ Step {step_num} 失败: {safe_error_message(e, config)}[/red]\n")
        return False


def build_report(config: Config, steps_run: list[int]) -> None:
    """整合所有步骤输出，生成最终竞争分析 Markdown 报告"""
    console.rule("[bold]生成竞争分析报告")
    try:
        report_path = generate_report(config, steps_run=steps_run)
        console.print(
            f"\n[bold green]✓ 竞争分析报告已生成:[/bold green]\n"
            f"  [cyan]{report_path}[/cyan]\n"
        )
    except Exception as e:
        console.print(f"[red]✗ 报告生成失败: {safe_error_message(e, config)}[/red]\n")


def main() -> None:
    args = parse_args()

    console.print(
        Panel.fit(
            "[bold]竞争情报工具包[/bold]\nAI 辅助 · 竞争格局映射 · 叙事分析 · 空白空间识别",
            border_style="cyan",
        )
    )

    config = Config(
        input_file=args.input,
        competitors_override=args.competitors,
        market_override=args.market,
    )

    # ── Agent 模式（LangGraph ReAct）────────────────────────────────────
    if args.agent:
        if not config.competitor_list:
            console.print(
                "[red]✗ Agent 模式需要指定竞争对手，"
                "请通过 --competitors A,B,C 或 --input file.json 传入[/red]"
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
        try:
            run_agent(config)
        except Exception as e:
            console.print(f"[red]✗ Agent 运行失败: {safe_error_message(e, config)}[/red]")
            sys.exit(1)
        sys.exit(0)

    # 展示已加载的竞争对手列表
    if config.competitors:
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

    # ── 仅生成报告模式 ───────────────────────────────────────────
    if args.report_only:
        console.print("[yellow]— Report-Only 模式：跳过步骤执行，直接汇总输出[/yellow]\n")
        build_report(config, steps_run=list(STEPS.keys()))
        sys.exit(0)

    if args.dry_run:
        console.print("[yellow]— Dry Run 模式：仅验证配置[/yellow]\n")

    # ── 执行各步骤 ───────────────────────────────────────────────
    steps_to_run = [args.step] if args.step else list(STEPS.keys())
    results = []

    for step_num in steps_to_run:
        step_name, step_class = STEPS[step_num]
        success = run_step(step_num, step_class, config, dry_run=args.dry_run)
        results.append((step_num, step_name, success))

    # ── 打印执行汇总 ─────────────────────────────────────────────
    console.rule("[bold]执行结果汇总")
    for step_num, step_name, success in results:
        status = "[green]✓[/green]" if success else "[red]✗[/red]"
        console.print(f"  {status} Step {step_num} — {step_name}")
    console.print()

    # ── 生成竞争分析报告 ─────────────────────────────────────────
    # dry-run 或显式 --no-report 时跳过报告生成
    if not args.dry_run and not args.no_report:
        succeeded_steps = [r[0] for r in results if r[2]]
        if succeeded_steps:
            build_report(config, steps_run=succeeded_steps)

    failed = [r for r in results if not r[2]]
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
