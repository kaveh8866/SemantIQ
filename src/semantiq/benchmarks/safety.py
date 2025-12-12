from __future__ import annotations

import re
from typing import List


_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"\b(?:\+\d{1,3}[\s-]?)?(?:\(\d{1,4}\)[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b")
_MEDICAL = re.compile(r"\b(diagnos|prescription|therapy|oncology|psychiatr|depress|anxiety)\b", re.I)
_ILLEGAL = re.compile(r"\b(how to make|explosive|hack|malware|credit card|ssn|social security)\b", re.I)
_POLITICAL = re.compile(r"\b(election|propaganda|extremist|far-right|far-left)\b", re.I)


def check_prompt_safety(text: str) -> List[str]:
    issues: List[str] = []
    if _EMAIL.search(text):
        issues.append("contains email-like pattern")
    if _PHONE.search(text):
        issues.append("contains phone-like pattern")
    if _MEDICAL.search(text):
        issues.append("contains medical-diagnostic terms")
    if _ILLEGAL.search(text):
        issues.append("contains potentially illegal content")
    if _POLITICAL.search(text):
        issues.append("contains extreme political terms")
    return issues
