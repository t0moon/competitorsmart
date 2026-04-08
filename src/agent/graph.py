"""
LangGraph ReAct Agent — 竞争情报自主研究

架构（ReAct 循环）：

    START → agent ⟷ tools → … → END（报告通过完整性校验后结束）

工具：
  - search_web(query)   : DuckDuckGo 网络搜索
  - fetch_webpage(url)  : 抓取网页文本内容

LLM：
  - 智谱AI GLM（via OpenAI-compatible API）
  - 支持 Function Calling / Tool Use
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from rich.console import Console
from typing_extensions import TypedDict

from src.config import Config
from src.constants import ZHIPU_DEFAULT_BASE_URL, ZHIPU_DEFAULT_MODEL
from .tools import fetch_webpage, search_web

console = Console()

# ── Prompt ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """你是一名专业的竞争情报（Competitive Intelligence）分析师，
擅长市场竞争分析和产品定位策略。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
铁律（违反即失败）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 在所有竞品全部搜集完毕之前，你只能调用工具，不得输出任何解释性文字。
2. 不得输出"我正在研究"、"接下来我将"、"已完成X，继续Y"等过渡句。
3. 只有当所有竞品信息覆盖核心字段后，才能一次性输出完整报告。
4. 最终报告必须以 "# 竞品调研报告：" 或 "# 竞争情报报告：" 开头。
5. 每个关键结论必须附来源 URL；信息不足必须标注“待核实”或“未公开”。
6. 最终报告总字数必须 >= 4000 字。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
工作流程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

阶段一：逐个搜集所有竞品信息（不得中途输出文字）
  对竞品列表中的每一个竞品，执行“官网优先 + 交叉验证”流程：
  1) search_web("{竞品名} 官网")
  2) 官网优先抓取：pricing/plans、features/product、docs/help、blog/news、changelog/release notes
  3) 至少做 2 类外部交叉验证：评测媒体、应用商店、社区、新闻稿、招聘、案例库
  4) 必须覆盖：定位、功能、价格、用户分层、近期更新、分发渠道、商业模式、风险短板
  5) 若证据不足，继续调用工具补齐。

阶段二：一次性输出“11章深度模板”报告
  停止调用工具，输出完整 Markdown 报告，严格使用以下二级标题：

## 一、报告概述（Executive Summary）
## 二、市场与赛道分析（Market Context）
## 三、竞品选择与分层（Competitive Landscape）
## 四、核心能力拆解（Product Capability Analysis）
## 五、商业模式分析（Monetization）
## 六、增长与分发策略（Growth Strategy）
## 七、用户与场景分析（User & Use Case）
## 八、优劣势对比（SWOT / 对比矩阵）
## 九、关键差异与壁垒（Moat Analysis）
## 十、机会点与策略建议（Opportunities）
## 十一、数据附录（Appendix）

额外约束：
- 第四章中，每个竞品使用三级或四级标题单列小节（如 ### Retake 或 #### Retake）
- 每个竞品至少 8 个字段（建议写法：- **字段名**：结论（证据：...；来源：URL））
- 关键章节（二/三/四/五/六/十）应有可执行结论，避免空泛描述
- 附录至少包含来源列表与测试方法
"""


# ── State ─────────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ── Graph Builder ──────────────────────────────────────────────────────────────

def _build_llm(config: Config) -> ChatOpenAI:
    """构建智谱AI GLM 客户端（OpenAI-compatible）"""
    api_key = (
        config.zhipu_api_key_1
        or config.zhipu_api_key_2
        or config.zhipu_api_key_3
        or config.zhipu_api_key_4
    )
    if not api_key:
        raise RuntimeError(
            "未配置任何智谱AI Key，请在 .env 中设置 ZHIPU_API_KEY_1 / _2 / _3 / _4"
        )
    return ChatOpenAI(
        model=ZHIPU_DEFAULT_MODEL,
        api_key=api_key,
        base_url=config.zhipu_api_base_url or ZHIPU_DEFAULT_BASE_URL,
        temperature=0.3,
        max_tokens=8192,
    )


def build_graph(config: Config):
    """
    构建 LangGraph ReAct 图：
      agent ──(有tool_calls)──▶ tools ──▶ agent（循环）
      agent ──(无tool_calls)──▶ END
    """
    tools = [search_web, fetch_webpage]
    llm = _build_llm(config).bind_tools(tools)
    tool_node = ToolNode(tools)

    def _strip_markdown_links(text: str) -> str:
        return re.sub(r"\[[^\]]+\]\((https?://[^)]+)\)", r"\1", text)

    def _extract_competitor_sections(content: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        headings = list(re.finditer(r"^#{3,4}\s+(.+?)\s*$", content, flags=re.MULTILINE))
        if not headings:
            return sections
        for i, m in enumerate(headings):
            name = m.group(1).strip()
            start = m.end()
            end = headings[i + 1].start() if i + 1 < len(headings) else len(content)
            sections[name] = content[start:end]
        return sections

    def _field_count(section_text: str) -> int:
        # 统计常见字段写法：- **字段**：...
        return len(re.findall(r"-\s*\*\*[^*\n]{1,40}\*\*\s*[:：]", section_text))

    def _source_count(text: str) -> int:
        plain = _strip_markdown_links(text)
        return len(re.findall(r"https?://[^\s)]+", plain))

    def _section_min_bullets(content: str, section_title: str, minimum: int = 6) -> bool:
        pattern = rf"^##\s+{re.escape(section_title)}\s*$"
        m = re.search(pattern, content, flags=re.MULTILINE)
        if not m:
            return False
        start = m.end()
        next_h2 = re.search(r"^##\s+.+$", content[start:], flags=re.MULTILINE)
        end = start + next_h2.start() if next_h2 else len(content)
        block = content[start:end]
        bullets = len(re.findall(r"^\s*[-*]\s+", block, flags=re.MULTILINE))
        return bullets >= minimum

    def _report_is_complete(content: str) -> bool:
        stripped = content.lstrip()
        if not content or not (
            stripped.startswith("# 竞争情报报告：")
            or stripped.startswith("# 竞品调研报告：")
        ):
            return False

        if len(content) < 4000:
            return False

        required_h2 = [
            "一、报告概述（Executive Summary）",
            "二、市场与赛道分析（Market Context）",
            "三、竞品选择与分层（Competitive Landscape）",
            "四、核心能力拆解（Product Capability Analysis）",
            "五、商业模式分析（Monetization）",
            "六、增长与分发策略（Growth Strategy）",
            "七、用户与场景分析（User & Use Case）",
            "八、优劣势对比（SWOT / 对比矩阵）",
            "九、关键差异与壁垒（Moat Analysis）",
            "十、机会点与策略建议（Opportunities）",
            "十一、数据附录（Appendix）",
        ]
        for title in required_h2:
            if f"## {title}" not in content:
                return False

        # 至少有基础来源链接数量，防止“无证据空报告”
        if _source_count(content) < max(12, len(config.competitor_list) * 4):
            return False

        # 每个竞品至少 8 个字段（按三级标题段落统计）
        sections = _extract_competitor_sections(content)
        if not sections:
            return False

        for competitor in config.competitor_list:
            # 容错：只要标题里包含竞品名即认为命中
            matched_section = ""
            for h, body in sections.items():
                if competitor.lower() in h.lower():
                    matched_section = body
                    break
            if not matched_section:
                return False
            if _field_count(matched_section) < 8:
                return False

        # 章节要点门槛（表格章节除外）
        if not _section_min_bullets(content, "二、市场与赛道分析（Market Context）", minimum=3):
            return False
        if not _section_min_bullets(content, "四、核心能力拆解（Product Capability Analysis）", minimum=3):
            return False
        if not _section_min_bullets(content, "五、商业模式分析（Monetization）", minimum=3):
            return False
        if not _section_min_bullets(content, "十、机会点与策略建议（Opportunities）", minimum=3):
            return False

        return True

    # ── 节点：LLM 决策 ──
    def agent_node(state: AgentState) -> dict:
        from langchain_core.messages import ToolMessage
        messages = list(state["messages"])
        # 仅在第一轮注入 system prompt
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

        try:
            response = llm.invoke(messages)
        except Exception as e:
            err_str = str(e)
            # GLM 内容过滤 (1301) → 截断工具消息内容后重试
            if "1301" in err_str or "contentFilter" in err_str:
                console.print("  [yellow]内容过滤触发，截断搜索结果后重试...[/yellow]")
                clean_messages = []
                for m in messages:
                    if isinstance(m, ToolMessage):
                        # 截断工具返回内容至 400 字符
                        short = (m.content or "")[:400]
                        clean_messages.append(ToolMessage(
                            content=short,
                            tool_call_id=m.tool_call_id,
                        ))
                    else:
                        clean_messages.append(m)
                response = llm.invoke(clean_messages)
            else:
                raise
        return {"messages": [response]}

    # ── 路由：有 tool_calls → tools；报告通过完整性校验 → END；否则继续 → agent ──
    def route(state: AgentState) -> Literal["tools", "agent", "__end__"]:
        last: AIMessage = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        # 只有当输出满足完整性门槛时才结束
        content = getattr(last, "content", "") or ""
        if _report_is_complete(content):
            return END
        # 未完成报告，继续驱动 agent 工作
        return "agent"

    # ── 组装图 ──
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", route, {"tools": "tools", "agent": "agent", "__end__": END})
    graph.add_edge("tools", "agent")

    return graph.compile()


# ── Runner ────────────────────────────────────────────────────────────────────

def run_agent(config: Config) -> str:
    """
    启动 Agent，流式打印进度，最终返回报告文件路径。
    """
    compiled = build_graph(config)

    competitors_str = "、".join(config.competitor_list)
    market = config.market or config.default_product_category or "未指定"
    our_line = (
        f"**我方产品：** {config.our_product}\n"
        if getattr(config, "our_product", None)
        else ""
    )

    user_task = (
        f"请对以下竞争对手进行全面研究，并生成竞争情报报告：\n\n"
        f"{our_line}"
        f"**竞争对手：** {competitors_str}\n"
        f"**市场/产品类别：** {market}\n"
        f"**地理范围：** {config.input_geography or '全球'}\n"
        f"**目标客群：** {config.input_company_size or '未指定'}\n\n"
        f"请按系统提示的工作流程逐步完成：先用工具搜集每个竞品的信息，"
        f"搜集完毕后输出完整的竞争情报报告。"
    )

    console.print(
        "\n[bold cyan]╔══════════════════════════════════╗[/bold cyan]"
    )
    console.print(
        "[bold cyan]║   [AI]  竞争情报 Agent 已启动    ║[/bold cyan]"
    )
    console.print(
        "[bold cyan]╚══════════════════════════════════╝[/bold cyan]\n"
    )
    console.print(f"  竞争对手  [cyan]{competitors_str}[/cyan]")
    console.print(f"  市场      [cyan]{market}[/cyan]\n")

    # ── 流式执行，实时打印工具调用 ──
    final_report = ""
    tool_call_count = 0

    for chunk in compiled.stream(
        {"messages": [("user", user_task)]},
        stream_mode="updates",
    ):
        for node_name, node_output in chunk.items():
            msgs: list[BaseMessage] = node_output.get("messages", [])

            if node_name == "agent":
                for msg in msgs:
                    if not isinstance(msg, AIMessage):
                        continue
                    # 有 tool_calls → 打印即将调用的工具
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            tool_call_count += 1
                            args = tc.get("args", {})
                            arg_val = next(iter(args.values()), "") if args else ""
                            preview = str(arg_val)[:70]
                            icon = "[S]" if tc["name"] == "search_web" else "[W]"
                            console.print(
                                f"  [{tool_call_count:02d}] {icon} "
                                f"[bold]{tc['name']}[/bold]  "
                                f"[dim]{preview}[/dim]"
                            )
                    # 无 tool_calls 且包含报告标志 → 最终报告
                    elif msg.content and (
                        "# 竞争情报报告" in msg.content or "# 竞品调研报告" in msg.content
                    ):
                        final_report = msg.content

            elif node_name == "tools":
                for msg in msgs:
                    content = getattr(msg, "content", "") or ""
                    preview = content[:60].replace("\n", " ")
                    console.print(f"        [dim]>> {preview}...[/dim]")

    # ── 保存报告 ──
    output_dir = config.output_dir / "agent"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"{ts}_agent_report.md"
    report_path.write_text(final_report, encoding="utf-8")

    console.print(
        f"\n[bold green]✓ 报告已生成:[/bold green] [cyan]{report_path}[/cyan]"
    )
    return str(report_path)
