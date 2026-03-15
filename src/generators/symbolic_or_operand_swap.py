from __future__ import annotations
import random
import re
from typing import Dict, Any, List

from src.generators.base import GenResult
from src.utils.text import normalize_spaces


_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def _split_sentences_keep_punct(text: str) -> List[str]:
    parts = [p.strip() for p in _SPLIT_RE.split(text) if p.strip()]
    return parts


def generate(example: Dict[str, Any], rng: random.Random, params: Dict[str, Any]) -> GenResult:
    q = normalize_spaces(example["question"])
    a = example["final_answer"]

    # Ignore name-renaming knobs entirely for safety.
    reorder_sentences = bool(params.get("reorder_sentences", True))

    new_q = q
    applied = False
    notes: Dict[str, Any] = {
        "rename_entities": False,
        "safety_policy": "no_name_changes_no_operand_changes"
    }

    if reorder_sentences:
        parts = _split_sentences_keep_punct(new_q)

        # Only reorder when we have at least 3 chunks:
        #   [desc1, desc2, ..., question]
        # and keep the final chunk fixed.
        if len(parts) >= 3:
            head = parts[:-1]
            tail = parts[-1]
            head[0], head[1] = head[1], head[0]
            rebuilt = " ".join(head + [tail])
            new_q = rebuilt
            applied = True
            notes["sentence_reorder"] = "swap_first_two_keep_question_last"

    if not applied:
        new_q = "[SWAP] " + new_q
        notes["fallback"] = "no_safe_reorder"

    return GenResult(
        question=new_q,
        final_answer=a,
        applied=applied,
        notes=notes,
    )
