"""
无头浏览器截图工具（Playwright）

由 build_graph 按单次运行注入输出目录；截图保存为 PNG，供最终 Markdown 用相对路径引用。
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse

from langchain_core.tools import tool

from src.redact import safe_error_message


def _is_allowed_http_url(url: str) -> bool:
    u = (url or "").strip()
    if not u.startswith(("http://", "https://")):
        return False
    try:
        parsed = urlparse(u)
    except Exception:
        return False
    host = (parsed.hostname or "").lower()
    if not host or host == "localhost":
        return False
    if host.endswith(".local"):
        return False
    # 简单拦截常见内网（截图工具不应扫内网）
    if re.match(r"^(127\.|10\.|172\.(1[6-9]|2\d|3[01])\.|192\.168\.)", host):
        return False
    return True


def _filename_for_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.netloc or "page").replace(":", "_")
    host = re.sub(r"[^\w.\-]+", "_", host)[:80]
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    return f"{host}_{digest}.png"


def create_screenshot_webpage_tool(screenshot_dir: Path, md_relative_dir: str):
    """
    screenshot_dir: 绝对路径，PNG 写入此处。
    md_relative_dir: 相对「报告所在目录」的文件夹名，如 20250409_120000_screenshots。
    """
    screenshot_dir = Path(screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    @tool
    def screenshot_webpage(
        url: str,
        image_label: str = "",
        full_page: bool = False,
    ) -> str:
        """对公开网页进行无头浏览器截图并保存为 PNG。

        适用于：竞品官网首页、定价页、功能介绍页等需要「视觉证据」的场景；
        若 fetch_webpage 得到内容很少（多为前端渲染），可优先尝试本工具截屏。

        参数：
        - url：以 http:// 或 https:// 开头的地址。
        - image_label：简短说明，用于报告插图标题（中文），如「Visify 定价页」。
        - full_page：是否截取整页长图；默认 false 仅可视区域（更快、文件更小）。

        返回：本次运行内可用的 Markdown 图片引用（相对路径相对最终报告文件所在目录），请写入正式报告。
        """
        if not _is_allowed_http_url(url):
            return (
                "截图被拒绝：仅允许 http/https 公网 URL，且不允许 localhost/内网地址。"
                f" 收到: {url!r}"
            )

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return (
                "截图不可用：未安装 Playwright。请执行 "
                "`pip install playwright` 后运行 `playwright install chromium`。"
            )

        path = screenshot_dir / _filename_for_url(url)
        label = (image_label or "").strip() or urlparse(url).netloc or "页面截图"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    context = browser.new_context(
                        viewport={"width": 1280, "height": 720},
                        user_agent=(
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
                        ),
                        locale="zh-CN",
                    )
                    page = context.new_page()
                    page.goto(url, wait_until="domcontentloaded", timeout=45_000)
                    page.wait_for_timeout(800)
                    page.screenshot(path=str(path), full_page=full_page)
                finally:
                    browser.close()
        except Exception as e:
            return (
                f"截图失败（{type(e).__name__}）: {safe_error_message(e, None)}。"
                " 若提示缺少浏览器，请运行: playwright install chromium"
            )

        rel = f"{md_relative_dir}/{path.name}"
        alt = label.replace("]", "").replace("[", "")
        md = f"![{alt}]({rel})"
        return (
            "截图已保存。\n\n"
            "请在最终报告的对应竞品小节（建议第四章）或「十一、数据附录」中原样插入下列 Markdown：\n\n"
            f"{md}\n\n"
            f"来源页: {url}"
        )

    return screenshot_webpage
