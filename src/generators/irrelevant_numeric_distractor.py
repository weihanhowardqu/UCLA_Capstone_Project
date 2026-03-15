from __future__ import annotations
import random
from typing import Dict, Any

from src.generators.base import GenResult
from src.utils.text import extract_numbers, append_sentence
from src.utils.numbers import numbers_in_text_as_ints, pick_distinct_ints

def generate(example: Dict[str, Any], rng: random.Random, params: Dict[str, Any]) -> GenResult:
    q = example["question"]
    a = example["final_answer"]

    distractor_count = int(params.get("distractor_count", 2))
    placement = params.get("placement", "append")
    avoid_collisions = bool(params.get("avoid_number_collisions", True))
    lo = int(params.get("number_range", {}).get("min", 7))
    hi = int(params.get("number_range", {}).get("max", 200))

    existing_nums = numbers_in_text_as_ints(extract_numbers(q)) if avoid_collisions else set()
    distractors = pick_distinct_ints(rng, distractor_count, existing_nums, lo=lo, hi=hi)

    # Neutral irrelevant sentence(s)
    if distractor_count == 1:
        sent = f"For reference, a nearby store has {distractors[0]} shelves."
    else:
        sent = f"For reference, a nearby store has {distractors[0]} shelves and {distractors[1]} carts."

    if placement != "append":
        notes = {"requested_placement": placement, "used_placement": "append"}
    else:
        notes = {"used_placement": "append"}

    new_q = append_sentence(q, sent)

    notes.update({"distractor_numbers": distractors, "distractor_count": distractor_count})
    return GenResult(question=new_q, final_answer=a, applied=True, notes=notes)
