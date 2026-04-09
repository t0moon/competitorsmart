"""一次性抓取报告配图（公开网页）。"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "微信小程序-美图秀秀与腾讯ARC-竞品分析_screenshots"
SHOTS: list[tuple[str, str, bool]] = [
    (
        "https://arc.tencent.com/zh/ai-demos",
        "arc_ai_demos_hub.png",
        False,
    ),
    (
        "https://arc.tencent.com/zh/ai-demos/humansegmentation",
        "arc_human_segmentation.png",
        False,
    ),
    (
        "https://m.kuai8.com/xcx/10272.html",
        "meitu_miniprogram_thirdparty_intro.png",
        True,
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
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
            for url, name, full_page in SHOTS:
                path = OUT / name
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                    page.wait_for_timeout(1200)
                    page.screenshot(path=str(path), full_page=full_page)
                    print("ok", path)
                except Exception as e:
                    print("fail", url, e)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
