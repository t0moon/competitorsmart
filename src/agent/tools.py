"""
LangGraph Agent 工具集

两个核心工具，无需 API Key：
  - search_web   : DuckDuckGo 网络搜索
  - fetch_webpage: 网页内容抓取 + HTML 清洗
"""

from __future__ import annotations

import re
import textwrap

import requests
from langchain_core.tools import tool

from src.redact import safe_error_message


@tool
def search_web(query: str) -> str:
    """搜索网络，获取竞争对手的公开信息。
    输入一个搜索词（中文或英文均可），返回多条搜索结果摘要。
    适合用于：查找竞品官网、功能介绍、用户评价、融资动态、市场定位等。
    """
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        results = list(DDGS().text(query, max_results=6))
        if not results:
            return "未找到搜索结果，请尝试换一个更具体的搜索词。"

        lines: list[str] = []
        for r in results:
            title = r.get("title", "").strip()
            body = r.get("body", "").strip()
            href = r.get("href", "").strip()
            lines.append(f"### {title}\n{body}\n来源: {href}")

        return "\n\n---\n\n".join(lines)

    except ImportError:
        return "错误：请先安装搜索包（pip install ddgs）"
    except Exception as e:
        return f"搜索失败（{type(e).__name__}）: {safe_error_message(e, None)}"


@tool
def fetch_webpage(url: str) -> str:
    """抓取指定网页并提取纯文本内容（最多返回 4000 字符）。
    适合用于：获取竞品官网主页文案、定价页、关于页面等详细内容。
    注意：JavaScript 渲染的内容可能无法获取，遇到此类页面请改用 search_web。
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html = resp.text

        # 清洗 HTML：去除 script / style / 标签
        html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<!--.*?-->", " ", html, flags=re.DOTALL)
        html = re.sub(r"<[^>]+>", " ", html)
        html = re.sub(r"&[a-z]+;", " ", html)          # HTML entities
        html = re.sub(r"\s{2,}", "\n", html).strip()   # 合并空白

        content = textwrap.shorten(html, width=4000, placeholder="…（内容已截断）")
        return content if content else "页面内容为空或无法解析。"

    except requests.exceptions.Timeout:
        return f"请求超时（15s）: {url}"
    except requests.exceptions.HTTPError as e:
        return f"HTTP 错误 {e.response.status_code}: {url}"
    except Exception as e:
        return f"无法获取页面（{type(e).__name__}）: {safe_error_message(e, None)}"
