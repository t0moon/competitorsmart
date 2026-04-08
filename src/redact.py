"""
避免在日志、报告或异常信息中泄露 API Key 等敏感配置。
"""

from __future__ import annotations

import re
from dataclasses import fields
from typing import Iterable

from src.config import Config

# 部分 SDK/网关错误体会带上 Bearer token，与具体 .env 无关时也做一次泛化脱敏
_BEARER_PATTERN = re.compile(r"Bearer\s+[A-Za-z0-9._\-]{16,}", re.IGNORECASE)


def gather_secrets_from_config(config: Config) -> list[str]:
    """从 Config 中收集标记为 secret 的字段值（用于字符串替换）。"""
    out: list[str] = []
    for f in fields(config):
        if not f.metadata.get("secret"):
            continue
        val = getattr(config, f.name, None)
        if isinstance(val, str) and len(val.strip()) >= 8:
            out.append(val)
    return out


def redact_secrets(message: str, secrets: Iterable[str]) -> str:
    """将 message 中出现的已知密钥替换为占位符；并对 Bearer token 做泛化脱敏。"""
    text = message
    unique = sorted({s for s in secrets if s and len(s.strip()) >= 8}, key=len, reverse=True)
    for s in unique:
        text = text.replace(s, "[REDACTED]")
    text = _BEARER_PATTERN.sub("Bearer [REDACTED]", text)
    return text


def safe_error_message(exc: BaseException, config: Config | None = None) -> str:
    """供终端或报告展示的异常文案（脱敏后）。"""
    msg = str(exc)
    if config is not None:
        msg = redact_secrets(msg, gather_secrets_from_config(config))
    else:
        msg = _BEARER_PATTERN.sub("Bearer [REDACTED]", msg)
    return msg
