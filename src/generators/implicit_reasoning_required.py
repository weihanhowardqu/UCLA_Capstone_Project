from __future__ import annotations
import random
import re
from typing import Dict, Any, Optional, Tuple

from src.generators.base import GenResult
from src.utils.text import normalize_spaces, append_sentence


_PACK_PATTERN = re.compile(r"\bpack(?:s)?\b|\bbox(?:es)?\b|\bbottle(?:s)?\b|\bbag(?:s)?\b", re.IGNORECASE)
_FRACTION_PATTERN = re.compile(r"\bhalf\b|\bone-third\b|\bthird\b|\bquarter\b|\b1/\d+\b", re.IGNORECASE)

def generate(example: Dict[str, Any], rng: random.Random, params: Dict[str, Any]) -> GenResult:
    q = normalize_spaces(example["question"])
    a = example["final_answer"]

    allowed = params.get("allowed_inference_types", [])
    mode = params.get("mode", "conservative")

    applied = False
    notes: Dict[str, Any] = {}

    if "whole_units_only" in allowed and _PACK_PATTERN.search(q):
        new_q = append_sentence(q, "Assume items can only be bought or used in whole units (no partial packs).")
        applied = True
        notes["inference_hook"] = "whole_units_only"
        return GenResult(question=new_q, final_answer=a, applied=True, notes=notes)

    if "leftover_discarded" in allowed and _FRACTION_PATTERN.search(q):
        new_q = append_sentence(q, "If any fractional remainder occurs, assume it is discarded and does not count.")
        applied = True
        notes["inference_hook"] = "leftover_discarded"
        return GenResult(question=new_q, final_answer=a, applied=True, notes=notes)

    if "capacity_constraint" in allowed and re.search(r"\bfit\b", q, re.IGNORECASE):
        new_q = append_sentence(q, "Assume capacities must be satisfied exactly; you cannot exceed any capacity.")
        applied = True
        notes["inference_hook"] = "capacity_constraint"
        return GenResult(question=new_q, final_answer=a, applied=True, notes=notes)

    new_q = "[IMPLICIT] " + q
    return GenResult(question=new_q, final_answer=a, applied=False, notes={"fallback": "no_safe_implicit_hook"})

