"""
AI 客户端统一调度 — 全流程使用智谱AI（GLM）
"""

from src.constants import ZHIPU_DEFAULT_BASE_URL, ZHIPU_DEFAULT_MODEL
from .base import BaseAIClient


def get_best_available_client(config, step: str = "") -> BaseAIClient:
    """
    根据步骤名称选取对应的智谱AI Key，返回 ZhipuClient。
    Key 分配规则：
      landscape / monitor  → ZHIPU_API_KEY_1
      narrative / whitespace → ZHIPU_API_KEY_2
      enablement           → ZHIPU_API_KEY_3
    未匹配步骤时依次尝试 Key 1 → Key 2 → Key 3。

    :param step: 步骤名称，可选值：landscape | narrative | whitespace | enablement | monitor
    """
    from .zhipu import ZhipuClient, get_zhipu_client_for_step

    if step:
        client = get_zhipu_client_for_step(step, config)
        if client and client.is_available():
            return client

    # 无 step 或对应 Key 未配置时，按顺序兜底
    base_url = getattr(config, "zhipu_api_base_url", ZHIPU_DEFAULT_BASE_URL)
    for attr in ("zhipu_api_key_1", "zhipu_api_key_2", "zhipu_api_key_3", "zhipu_api_key_4"):
        key = getattr(config, attr, "")
        if key:
            return ZhipuClient(api_key=key, model=ZHIPU_DEFAULT_MODEL, base_url=base_url)

    raise RuntimeError("未配置任何智谱AI API Key（ZHIPU_API_KEY_1/2/3/4），请检查 .env 文件")


def pick_zhipu_key_for_chapter(config, chapter_index: int) -> tuple[str, str]:
    """
    在已配置的 Key（1–4，按顺序、跳过空值）之间轮转。
    返回 (环境变量名, api_key)。
    """
    slots: list[tuple[str, str]] = []
    for i in range(1, 5):
        k = getattr(config, f"zhipu_api_key_{i}", "") or ""
        if k:
            slots.append((f"ZHIPU_API_KEY_{i}", k))
    if not slots:
        raise RuntimeError("未配置任何智谱AI API Key（ZHIPU_API_KEY_1/2/3/4），请检查 .env 文件")
    idx = (max(1, chapter_index) - 1) % len(slots)
    return slots[idx]


def get_balanced_client_for_chapter(config, chapter_index: int) -> BaseAIClient:
    """
    按章节在已配置的 Key 之间均匀轮转（若配置了 4 个则周期为 4）。
    """
    from .zhipu import ZhipuClient

    base_url = getattr(config, "zhipu_api_base_url", ZHIPU_DEFAULT_BASE_URL)
    _, key = pick_zhipu_key_for_chapter(config, chapter_index)
    return ZhipuClient(api_key=key, model=ZHIPU_DEFAULT_MODEL, base_url=base_url)
