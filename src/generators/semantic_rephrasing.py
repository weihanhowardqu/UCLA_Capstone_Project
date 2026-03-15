from __future__ import annotations
import random
from typing import Dict, Any, List

from src.generators.base import GenResult
from src.utils.text import normalize_spaces

TEMPLATES: List[str] = [
    "{q}\n\n(Answer the question above.)",
    "{q}\n\n(Compute the requested value.)",
    "{q}\n\n(Find the final result.)",
    "Read carefully and solve:\n{q}",
    "Solve the following:\n{q}",
    "Determine the answer:\n{q}",
    "Compute the result:\n{q}",
    "Work out the solution:\n{q}",
    "Use the given information to solve:\n{q}",
    "Based on the scenario, compute the answer:\n{q}",
]

def generate(example: Dict[str, Any], rng: random.Random, params: Dict[str, Any]) -> GenResult:
    q = normalize_spaces(example["question"])
    a = example["final_answer"]

    template_bank_size = int(params.get("template_bank_size", len(TEMPLATES)))
    bank = TEMPLATES[: max(1, min(template_bank_size, len(TEMPLATES)))]
    t = rng.choice(bank)

    # Family-unique tag prevents collisions with other families' fallbacks/prefixes
    new_q = f"[REPHRASE] " + t.format(q=q)

    return GenResult(
        question=new_q,
        final_answer=a,
        applied=True,
        notes={"template": t, "mode": params.get("mode", "template_bank")}
    )
