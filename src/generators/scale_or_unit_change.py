from __future__ import annotations
import random
import re
from typing import Dict, Any, Optional, Tuple, Callable

from src.generators.base import GenResult
from src.utils.text import normalize_spaces


_MONEY_DOLLARS = re.compile(r"\$(\d+)(?!\.\d)")  # integer dollars only
_CENTS = re.compile(r"\b(\d+)\s+cents?\b", re.IGNORECASE)
_HOURS = re.compile(r"\b(\d+)\s+hours?\b", re.IGNORECASE)
_MINUTES = re.compile(r"\b(\d+)\s+minutes?\b", re.IGNORECASE)

def _try_convert_dollars_to_cents(q: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    m = _MONEY_DOLLARS.search(q)
    if not m:
        return None
    x = int(m.group(1))
    cents = x * 100
    new_q = q[:m.start()] + f"{cents} cents" + q[m.end():]
    return new_q, {"conversion": "dollars_to_cents", "from": f"${x}", "to": f"{cents} cents"}

def _try_convert_cents_to_dollars(q: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    m = _CENTS.search(q)
    if not m:
        return None
    x = int(m.group(1))
    # only convert if divisible by 100 to keep dollars integer
    if x % 100 != 0:
        return None
    dollars = x // 100
    new_q = q[:m.start()] + f"${dollars}" + q[m.end():]
    return new_q, {"conversion": "cents_to_dollars", "from": f"{x} cents", "to": f"${dollars}"}

def _try_convert_hours_to_minutes(q: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    m = _HOURS.search(q)
    if not m:
        return None
    x = int(m.group(1))
    minutes = x * 60
    new_q = q[:m.start()] + f"{minutes} minutes" + q[m.end():]
    return new_q, {"conversion": "hours_to_minutes", "from": f"{x} hours", "to": f"{minutes} minutes"}

def _try_convert_minutes_to_hours(q: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    m = _MINUTES.search(q)
    if not m:
        return None
    x = int(m.group(1))
    # Only convert if divisible by 60 to keep hours integer
    if x % 60 != 0:
        return None
    hours = x // 60
    # Preserve singular/plural
    unit = "hour" if hours == 1 else "hours"
    new_q = q[:m.start()] + f"{hours} {unit}" + q[m.end():]
    return new_q, {"conversion": "minutes_to_hours", "from": f"{x} minutes", "to": f"{hours} {unit}"}

_CONV_MAP: Dict[str, Callable[[str], Optional[Tuple[str, Dict[str, Any]]]]] = {
    "dollars_to_cents": _try_convert_dollars_to_cents,
    "cents_to_dollars": _try_convert_cents_to_dollars,
    "hours_to_minutes": _try_convert_hours_to_minutes,
    "minutes_to_hours": _try_convert_minutes_to_hours,
}

def generate(example: Dict[str, Any], rng: random.Random, params: Dict[str, Any]) -> GenResult:
    q = normalize_spaces(example["question"])
    a = example["final_answer"]

    if not bool(params.get("enabled", True)):
        return GenResult(question=q, final_answer=a, applied=False, notes={"disabled": True})

    allowed = params.get("allowed_conversions", [])
    max_conv = int(params.get("max_conversions_per_item", 1))
    max_conv = max(1, max_conv)

    # Try conversions in random order (deterministic due to seeded rng)
    candidates = [c for c in allowed if c in _CONV_MAP]
    rng.shuffle(candidates)

    for conv in candidates:
        out = _CONV_MAP[conv](q)
        if out:
            new_q, meta = out
            meta["max_conversions_per_item"] = max_conv
            meta["keep_gold_answer_numeric_equal"] = bool(params.get("keep_gold_answer_numeric_equal", True))
            return GenResult(question=new_q, final_answer=a, applied=True, notes=meta)

    # Fallback: family-unique prefix (prevents duplicate text collisions)
    new_q = "[SCALE/UNIT] " + q
    return GenResult(question=new_q, final_answer=a, applied=False, notes={"fallback": "no_applicable_conversion"})

