"""
AI 客户端基类 — 统一接口，便于在不同 LLM 之间切换
"""

from abc import ABC, abstractmethod


class BaseAIClient(ABC):
    """所有 AI 客户端需实现此接口"""

    @abstractmethod
    def complete(self, prompt: str, system: str = "") -> str:
        """发送 prompt，返回模型文本回复"""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """检查客户端是否已配置 API Key"""
        ...
