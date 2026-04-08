"""
智谱AI（BigModel）GLM 客户端
接口兼容 OpenAI SDK，无需额外依赖
用途：
  Key 1 (ZHIPU_API_KEY_1) — Step 1 景观综合 + Step 5 监控  → GLM-4.6V-FlashX
  Key 2 (ZHIPU_API_KEY_2) — Step 2 叙事分析 + Step 3 空白  → GLM-4.6V-FlashX
  Key 3 (ZHIPU_API_KEY_3) — Step 4 销售赋能（战斗卡）      → GLM-4.6V-FlashX
文档：https://open.bigmodel.cn/dev/api
"""

from __future__ import annotations
from openai import OpenAI
from src.constants import ZHIPU_DEFAULT_BASE_URL, ZHIPU_DEFAULT_MODEL
from .base import BaseAIClient

DEFAULT_BASE_URL = ZHIPU_DEFAULT_BASE_URL

# 步骤 → (config 属性名, 模型)；模型统一走 constants
_STEP_MAP: dict[str, tuple[str, str]] = {
    "landscape":  ("zhipu_api_key_1", ZHIPU_DEFAULT_MODEL),
    "narrative":  ("zhipu_api_key_2", ZHIPU_DEFAULT_MODEL),
    "whitespace": ("zhipu_api_key_2", ZHIPU_DEFAULT_MODEL),
    "enablement": ("zhipu_api_key_3", ZHIPU_DEFAULT_MODEL),
    "monitor":    ("zhipu_api_key_3", ZHIPU_DEFAULT_MODEL),
}


class ZhipuClient(BaseAIClient):
    """
    智谱AI GLM 客户端，复用 OpenAI SDK（base_url 替换）。
    默认使用 GLM-4.6V-FlashX。
    """

    def __init__(
        self,
        api_key: str,
        model: str = ZHIPU_DEFAULT_MODEL,
        base_url: str = DEFAULT_BASE_URL,
    ) -> None:
        self._api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                api_key=self._api_key,
                base_url=self.base_url,
            )
        return self._client

    def is_available(self) -> bool:
        return bool(self._api_key)

    def complete(self, prompt: str, system: str = "") -> str:
        if not self.is_available():
            raise RuntimeError("ZHIPU_API_KEY 未配置")

        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._get_client().chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""


def get_zhipu_client_for_step(step: str, config) -> ZhipuClient | None:
    """
    根据步骤名称选取对应的 Key 和模型，返回 ZhipuClient；
    如果对应 Key 未配置则返回 None。

    step 可选值：landscape | narrative | whitespace | enablement | monitor
    """
    key_attr, model = _STEP_MAP.get(step, ("zhipu_api_key_1", ZHIPU_DEFAULT_MODEL))
    api_key: str = getattr(config, key_attr, "")
    base_url: str = getattr(config, "zhipu_api_base_url", DEFAULT_BASE_URL) or DEFAULT_BASE_URL

    if not api_key:
        return None
    return ZhipuClient(api_key=api_key, model=model, base_url=base_url)
