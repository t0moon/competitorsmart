"""
Crunchbase API 客户端
用途：监控竞争对手融资轮次、招聘动态
文档：https://data.crunchbase.com/docs/using-the-api
"""

from __future__ import annotations
from typing import Any
from dataclasses import dataclass
import requests


@dataclass
class FundingRound:
    company: str
    round_type: str
    amount_usd: float | None
    announced_date: str
    investors: list[str]


class CrunchbaseClient:
    BASE_URL = "https://api.crunchbase.com/api/v4"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def is_available(self) -> bool:
        return bool(self._api_key)

    def _get(self, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        merged = {"user_key": self._api_key, **(params or {})}
        resp = requests.get(url, params=merged, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_organization(self, permalink: str) -> dict[str, Any]:
        """
        获取公司基本信息。
        :param permalink: Crunchbase 公司 permalink，如 "openai" 或 "salesforce"
        """
        if not self.is_available():
            raise RuntimeError("CRUNCHBASE_API_KEY 未配置")
        return self._get(f"entities/organizations/{permalink}", {
            "field_ids": "short_description,funding_total,last_funding_type,last_funding_at,employee_count"
        })

    def get_recent_funding_rounds(self, permalink: str, limit: int = 5) -> list[FundingRound]:
        """获取指定公司最近的融资轮次"""
        if not self.is_available():
            raise RuntimeError("CRUNCHBASE_API_KEY 未配置")

        data = self._get(f"entities/organizations/{permalink}/funding_rounds", {
            "field_ids": "investment_type,money_raised,announced_on,lead_investor_identifiers",
            "order": "announced_on%20DESC",
            "limit": limit,
        })

        rounds: list[FundingRound] = []
        for item in data.get("entities", []):
            props = item.get("properties", {})
            investors = [
                inv.get("value", "") for inv in props.get("lead_investor_identifiers", [])
            ]
            amount = props.get("money_raised", {})
            rounds.append(
                FundingRound(
                    company=permalink,
                    round_type=props.get("investment_type", ""),
                    amount_usd=amount.get("value_usd") if isinstance(amount, dict) else None,
                    announced_date=props.get("announced_on", ""),
                    investors=investors,
                )
            )
        return rounds

    def format_funding_summary(self, rounds: list[FundingRound]) -> str:
        """格式化融资信息摘要，适合传给 AI 做信号分析"""
        lines = []
        for r in rounds:
            amount_str = f"${r.amount_usd:,.0f}" if r.amount_usd else "金额未披露"
            investors_str = "、".join(r.investors) if r.investors else "未披露"
            lines.append(
                f"- [{r.announced_date}] {r.round_type} 轮，{amount_str}，"
                f"领投方：{investors_str}"
            )
        return "\n".join(lines)
