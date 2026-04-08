"""
竞争分析报告生成器（按章节 API 生成）

1) 11 章各一次 API 调用
2) 在已配置的 ZHIPU_API_KEY_1～4 间按章节轮转
3) 上下文来自 Step 输出目录（定义见 report/definitions.py）
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

from src.config import Config
from src.integrations.ai.openai_client import get_balanced_client_for_chapter, pick_zhipu_key_for_chapter
from src.redact import safe_error_message
from src.report.definitions import CHAPTER_SPECS, FILE_LABEL_MAP, STEP_DIR_MAP

console = Console()


def _get_label(filename: str) -> str:
    for key, label in FILE_LABEL_MAP.items():
        if key in filename:
            return label
    return filename


def _read_step_outputs(step_dir: Path) -> list[tuple[str, str]]:
    if not step_dir.exists():
        return []
    files = sorted(step_dir.glob("*.md"))
    outputs: list[tuple[str, str]] = []
    for file in files:
        content = file.read_text(encoding="utf-8").strip()
        if content:
            outputs.append((_get_label(file.stem), content))
    return outputs


def _strip_top_heading(content: str) -> str:
    lines: list[str] = []
    for line in content.splitlines():
        if line.startswith("# "):
            lines.append("#### " + line[2:])
        else:
            lines.append(line)
    return "\n".join(lines)


def _extract_urls(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"https?://[^\s)]+", text)))


def _build_context(outputs: list[tuple[str, str]]) -> str:
    chunks: list[str] = []
    for label, content in outputs:
        chunks.append(f"### {label}\n{_strip_top_heading(content)}")
    return "\n\n".join(chunks) if chunks else "无可用步骤输出。"


def _build_toc() -> str:
    lines = ["## 目录", ""]
    for spec in CHAPTER_SPECS:
        heading = spec["title"]
        anchor = heading.lower().replace(" ", "-").replace("/", "").replace("（", "").replace("）", "")
        lines.append(f"- [{heading}](#{anchor})")
    return "\n".join(lines)


def _generate_chapter(
    config: Config,
    chapter_spec: dict[str, str],
    competitors: list[str],
    market: str,
    context: str,
    urls: list[str],
) -> str:
    chapter_idx = int(chapter_spec["idx"])
    chapter_title = chapter_spec["title"]
    must_include = chapter_spec["must"]
    key_name, _ = pick_zhipu_key_for_chapter(config, chapter_idx)

    console.print(
        f"[dim]生成章节 {chapter_idx:02d}（{chapter_title}），使用 {key_name}[/dim]"
    )

    client = get_balanced_client_for_chapter(config, chapter_idx)
    prompt = (
        f"请生成 Markdown 章节：`{chapter_title}`。\n\n"
        f"已知研究对象：{', '.join(competitors) if competitors else '未指定'}\n"
        f"研究赛道：{market}\n"
        f"本章必须覆盖：{must_include}\n\n"
        "写作要求：\n"
        "1) 只输出本章内容，以 `## ` 开头。\n"
        "2) 结论必须可执行，尽量量化；信息缺失写“待核实”或“未公开”。\n"
        "3) 若有证据，使用 `（来源：URL）` 标注。\n"
        "4) 内容要与竞品研究语境一致，不要泛泛而谈。\n\n"
        f"可用上下文如下：\n{context}\n\n"
        f"可用 URL（可选引用）：\n" + ("\n".join(f"- {u}" for u in urls[:80]) if urls else "- 暂无")
    )
    content = client.complete(prompt, system="你是资深产品经理与竞争情报分析师。请用简体中文输出。").strip()

    if not content.startswith("## "):
        content = f"## {chapter_title}\n\n{content}"
    return content


def generate_report(
    config: Config,
    steps_run: Optional[list[int]] = None,
    output_path: Optional[Path] = None,
) -> Path:
    pm_steps = set(STEP_DIR_MAP.keys())
    effective_steps = [s for s in (steps_run or list(STEP_DIR_MAP.keys())) if s in pm_steps]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    if output_path is None:
        output_path = config.output_dir / f"competitive_analysis_report_{ts}.md"

    competitors = config.competitor_list
    market = config.market or config.default_product_category or "（未指定）"

    all_outputs: list[tuple[str, str]] = []
    for step_num in effective_steps:
        step_dir = config.output_dir / STEP_DIR_MAP[step_num]
        all_outputs.extend(_read_step_outputs(step_dir))

    context = _build_context(all_outputs)
    urls = _extract_urls(context)

    report_lines: list[str] = [
        "# 竞品调研报告：深度版",
        "",
        f"> **生成时间：** {date_str}  ",
        f"> **研究对象：** {', '.join(competitors) if competitors else '（未指定）'}  ",
        f"> **研究赛道：** {market}  ",
        "",
        "> **API 分配规则：** 按章节在已配置的 `ZHIPU_API_KEY_1`～`_4` 间轮转（跳过未填写的 Key）",
        "",
        "---",
        "",
        _build_toc(),
        "",
        "---",
        "",
    ]

    for spec in CHAPTER_SPECS:
        try:
            chapter_content = _generate_chapter(config, spec, competitors, market, context, urls)
        except Exception as exc:
            chapter_content = (
                f"## {spec['title']}\n\n"
                f"> 本章生成失败：{safe_error_message(exc, config)}\n\n"
                "> 请检查 API 额度/网络后重试。\n"
            )
        report_lines += [chapter_content, "", "---", ""]

    report_lines += [
        "> ⚠️ AI 输出仅供参考，所有结论请结合一手用户洞察与业务数据二次校验。",
        "",
    ]

    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    return output_path
