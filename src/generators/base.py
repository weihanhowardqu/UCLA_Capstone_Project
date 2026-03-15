from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class GenResult:
    question: str
    final_answer: str
    applied: bool
    notes: Dict[str, Any]
