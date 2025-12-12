from __future__ import annotations

import json
import logging
import os
import re
from typing import Any


_API_KEY_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"(Bearer\s+)[A-Za-z0-9\-_.]{16,}"),
    re.compile(r"([A-Za-z0-9]{24,})"),
]
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"\b(?:\+\d{1,3}[\s-]?)?(?:\(\d{1,4}\)[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b")


def sanitize_api_keys(text: str) -> str:
    if not text:
        return text
    s = str(text)
    for pat in _API_KEY_PATTERNS:
        s = pat.sub(lambda m: _mask_token(m.group(0)), s)
    return s


def _mask_token(tok: str) -> str:
    if not tok or len(tok) < 8:
        return "***"
    return tok[:2] + "***" + tok[-4:]


def sanitize_user_generated_text(text: str) -> str:
    if not text:
        return text
    s = sanitize_api_keys(text)
    s = _EMAIL.sub("[redacted-email]", s)
    s = _PHONE.sub("[redacted-phone]", s)
    if len(s) > 2000:
        s = s[:2000] + "…"
    return s


def sanitize_model_response(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    def _clean(val: Any) -> Any:
        if isinstance(val, str):
            return sanitize_user_generated_text(val)
        if isinstance(val, dict):
            return {k: _clean(v) for k, v in val.items()}
        if isinstance(val, list):
            return [ _clean(v) for v in val ]
        return val
    cleaned = _clean(raw)
    s = json.dumps(cleaned)
    if len(s) > 10000:
        return {"truncated": True}
    return cleaned


class _SanitizingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                record.msg = sanitize_api_keys(record.msg)
            if hasattr(record, "args") and isinstance(record.args, tuple):
                record.args = tuple(sanitize_api_keys(str(a)) for a in record.args)
        except Exception:
            pass
        return True


def get_logger(name: str, json_mode: bool | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        level = os.getenv("SEMANTIQ_LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, level, logging.INFO))
        handler = logging.StreamHandler()
        handler.addFilter(_SanitizingFilter())
        if (json_mode or os.getenv("SEMANTIQ_LOG_FORMAT") == "json"):
            handler.setFormatter(_JSONFormatter())
        else:
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return logger


class _JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": getattr(record, "created", None),
            "level": record.levelname,
            "logger": record.name,
            "message": sanitize_api_keys(record.getMessage()),
        }
        return json.dumps(payload)
