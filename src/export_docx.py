"""
将 Markdown 报告导出为 Word（.docx）。

依赖本机已安装 Pandoc（https://pandoc.org），以便正确处理标题、列表、表格与相对路径图片。
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class PandocNotFoundError(RuntimeError):
    """未在 PATH 中找到 pandoc 可执行文件。"""


def markdown_to_docx(md_path: Path, docx_path: Path | None = None) -> Path:
    """
    将 Markdown 转为 .docx。图片使用与 Markdown 相同的相对路径时，
    通过 --resource-path 指向 .md 所在目录以便 Pandoc 解析。

    返回生成的 .docx 绝对路径。
    """
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise PandocNotFoundError(
            "未找到 pandoc。请先安装 Pandoc 并确保在 PATH 中可用："
            "https://pandoc.org/installing.html "
            "（Windows 可用 winget install --id JohnMacFarlane.Pandoc）"
        )

    md_path = md_path.resolve()
    if not md_path.is_file():
        raise FileNotFoundError(f"Markdown 文件不存在: {md_path}")

    if docx_path is None:
        docx_path = md_path.with_suffix(".docx")
    else:
        docx_path = docx_path.resolve()
    docx_path.parent.mkdir(parents=True, exist_ok=True)

    base = md_path.parent
    proc = subprocess.run(
        [
            pandoc,
            str(md_path),
            "-o",
            str(docx_path),
            "-f",
            "markdown",
            "-t",
            "docx",
            "--resource-path",
            str(base),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
        raise RuntimeError(f"Pandoc 导出失败: {err}")

    return docx_path
