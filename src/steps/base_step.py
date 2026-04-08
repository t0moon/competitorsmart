"""
步骤基类 — PM 三步分析（景观 / 叙事 / 空白）均继承此类
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from rich.console import Console

from src.config import Config

console = Console()


class BaseStep(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.output_dir: Path = config.output_dir / self.__class__.__name__.lower()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def run(self) -> None:
        """执行该步骤的完整流程"""
        ...

    def validate(self) -> None:
        """Dry-run 时调用：验证配置是否完整"""
        warnings = self.config.validate()
        for w in warnings:
            console.print(f"  [yellow]⚠ {w}[/yellow]")
        if not warnings:
            console.print("  [green]配置验证通过[/green]")

    def save_output(self, filename: str, content: str) -> Path:
        """将输出内容保存到 outputs/ 目录"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.output_dir / f"{ts}_{filename}"
        path.write_text(content, encoding="utf-8")
        console.print(f"  [dim]→ 已保存: {path}[/dim]")
        return path

    def log(self, msg: str) -> None:
        console.print(f"  {msg}")
