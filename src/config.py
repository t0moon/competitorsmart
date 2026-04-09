"""
全局配置模块 — 从 .env 加载所有环境变量并做统一管理
支持通过结构化 JSON 文件输入竞争对手名单及相关信息
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.constants import ZHIPU_DEFAULT_BASE_URL
from src.models.competitor import CompetitorInfo

load_dotenv()


@dataclass
class Config:
    # ── 运行时覆盖 ──────────────────────────────────────────────
    competitors_override: Optional[str] = None
    market_override: Optional[str] = None
    input_file: Optional[str] = None          # --input 指定的 JSON 文件路径

    # ── 智谱AI（GLM）— 多 Key（Agent 与扩展能力共用）──────────
    # Key 1：主用（glm-4.7，见 src/constants.py）
    zhipu_api_key_1: str = field(
        default_factory=lambda: os.getenv("ZHIPU_API_KEY_1", ""),
        repr=False,
        metadata={"secret": True},
    )
    # Key 2：备用
    zhipu_api_key_2: str = field(
        default_factory=lambda: os.getenv("ZHIPU_API_KEY_2", ""),
        repr=False,
        metadata={"secret": True},
    )
    # Key 3：备用
    zhipu_api_key_3: str = field(
        default_factory=lambda: os.getenv("ZHIPU_API_KEY_3", ""),
        repr=False,
        metadata={"secret": True},
    )
    # Key 4：可选备用
    zhipu_api_key_4: str = field(
        default_factory=lambda: os.getenv("ZHIPU_API_KEY_4", ""),
        repr=False,
        metadata={"secret": True},
    )
    zhipu_api_base_url: str = field(
        default_factory=lambda: os.getenv("ZHIPU_API_BASE_URL", ZHIPU_DEFAULT_BASE_URL)
    )

    # ── 竞争监控工具 ────────────────────────────────────────────
    google_alerts_rss_url: str = field(default_factory=lambda: os.getenv("GOOGLE_ALERTS_RSS_URL", ""))
    crunchbase_api_key: str = field(
        default_factory=lambda: os.getenv("CRUNCHBASE_API_KEY", ""),
        repr=False,
        metadata={"secret": True},
    )

    # ── CRM 集成 ────────────────────────────────────────────────
    salesforce_client_id: str = field(default_factory=lambda: os.getenv("SALESFORCE_CLIENT_ID", ""))
    salesforce_client_secret: str = field(
        default_factory=lambda: os.getenv("SALESFORCE_CLIENT_SECRET", ""),
        repr=False,
        metadata={"secret": True},
    )
    salesforce_instance_url: str = field(default_factory=lambda: os.getenv("SALESFORCE_INSTANCE_URL", ""))
    hubspot_api_key: str = field(
        default_factory=lambda: os.getenv("HUBSPOT_API_KEY", ""),
        repr=False,
        metadata={"secret": True},
    )
    pipedrive_api_token: str = field(
        default_factory=lambda: os.getenv("PIPEDRIVE_API_TOKEN", ""),
        repr=False,
        metadata={"secret": True},
    )

    # ── 数据存储 ────────────────────────────────────────────────
    notion_api_key: str = field(
        default_factory=lambda: os.getenv("NOTION_API_KEY", ""),
        repr=False,
        metadata={"secret": True},
    )
    notion_database_id: str = field(default_factory=lambda: os.getenv("NOTION_DATABASE_ID", ""))
    google_sheets_service_account_json: str = field(
        default_factory=lambda: os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON", ""),
        repr=False,
        metadata={"secret": True},
    )
    google_sheets_spreadsheet_id: str = field(
        default_factory=lambda: os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    )
    airtable_api_key: str = field(
        default_factory=lambda: os.getenv("AIRTABLE_API_KEY", ""),
        repr=False,
        metadata={"secret": True},
    )
    airtable_base_id: str = field(default_factory=lambda: os.getenv("AIRTABLE_BASE_ID", ""))

    # ── 通知与分发 ──────────────────────────────────────────────
    slack_webhook_url: str = field(
        default_factory=lambda: os.getenv("SLACK_WEBHOOK_URL", ""),
        repr=False,
        metadata={"secret": True},
    )
    slack_channel: str = field(default_factory=lambda: os.getenv("SLACK_CHANNEL", "#competitive-intel"))
    smtp_host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", ""))
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    smtp_user: str = field(default_factory=lambda: os.getenv("SMTP_USER", ""))
    smtp_password: str = field(
        default_factory=lambda: os.getenv("SMTP_PASSWORD", ""),
        repr=False,
        metadata={"secret": True},
    )
    notify_email_to: str = field(default_factory=lambda: os.getenv("NOTIFY_EMAIL_TO", ""))

    # ── 应用基础配置 ────────────────────────────────────────────
    node_env: str = field(default_factory=lambda: os.getenv("NODE_ENV", "development"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "info"))
    monitoring_interval_days: int = field(
        default_factory=lambda: int(os.getenv("MONITORING_INTERVAL_DAYS", "30"))
    )
    default_market: str = field(default_factory=lambda: os.getenv("DEFAULT_MARKET", ""))
    default_product_category: str = field(
        default_factory=lambda: os.getenv("DEFAULT_PRODUCT_CATEGORY", "")
    )

    # ── 输出目录 ────────────────────────────────────────────────
    output_dir: Path = field(default_factory=lambda: Path("outputs"))

    def __post_init__(self) -> None:
        self.output_dir.mkdir(exist_ok=True)
        self._input_data: dict = {}
        self._structured_competitors: list[CompetitorInfo] = []

        # 优先从 JSON 输入文件加载
        if self.input_file:
            self._load_input_file(self.input_file)
        elif Path("competitors_input.json").exists():
            self._load_input_file("competitors_input.json")

        # 命令行 --competitors 再次覆盖（仅名称列表）
        if self.competitors_override:
            self._competitor_list_raw = self.competitors_override
        elif self._structured_competitors:
            self._competitor_list_raw = ",".join(c.name for c in self._structured_competitors)
        else:
            self._competitor_list_raw = os.getenv("COMPETITOR_LIST", "")

        # 市场覆盖
        if self.market_override:
            self.default_market = self.market_override
        elif self._input_data.get("market") and not self.default_market:
            self.default_market = self._input_data["market"]
        if self._input_data.get("product_category") and not self.default_product_category:
            self.default_product_category = self._input_data["product_category"]

    def _load_input_file(self, path: str) -> None:
        """从结构化 JSON 输入文件加载竞争对手及市场信息"""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"输入文件不存在: {path}")
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        self._input_data = data
        raw_list = data.get("competitors", [])
        self._structured_competitors = [
            CompetitorInfo.from_dict(item) for item in raw_list if isinstance(item, dict)
        ]

    @property
    def competitor_list(self) -> list[str]:
        """返回已清洗的竞争对手名称列表"""
        return [c.strip() for c in self._competitor_list_raw.split(",") if c.strip()]

    @property
    def competitors(self) -> list[CompetitorInfo]:
        """返回结构化竞争对手列表（含详细信息）；若无 JSON 输入则降级为仅名称的对象"""
        if self._structured_competitors:
            return self._structured_competitors
        return [CompetitorInfo(name=name) for name in self.competitor_list]

    @property
    def input_geography(self) -> str:
        return self._input_data.get("geography", "")

    @property
    def input_company_size(self) -> str:
        return self._input_data.get("company_size", "")

    @property
    def our_product(self) -> str:
        """结构化 JSON 中的我方产品名（可选）"""
        return (self._input_data.get("our_product") or "").strip()

    @property
    def market(self) -> str:
        return self.default_market

    def has_ai_key(self) -> bool:
        return bool(
            self.zhipu_api_key_1
            or self.zhipu_api_key_2
            or self.zhipu_api_key_3
            or self.zhipu_api_key_4
        )

    def validate(self) -> list[str]:
        """返回缺失的必要配置项列表"""
        warnings: list[str] = []
        if not self.has_ai_key():
            warnings.append("未配置任何 AI API Key（请在 .env 中配置 ZHIPU_API_KEY_1 / _2 / _3 / _4）")
        if not self.competitor_list:
            warnings.append("未配置 COMPETITOR_LIST，请在 .env 或命令行参数中指定竞争对手")
        return warnings
