from __future__ import annotations

from src.generators.irrelevant_numeric_distractor import generate as gen_distractor
from src.generators.symbolic_or_operand_swap import generate as gen_swap
from src.generators.scale_or_unit_change import generate as gen_scale
from src.generators.semantic_rephrasing import generate as gen_rephrase
from src.generators.implicit_reasoning_required import generate as gen_implicit

GENERATOR_REGISTRY = {
    "irrelevant_numeric_distractor": gen_distractor,
    "symbolic_or_operand_swap": gen_swap,
    "scale_or_unit_change": gen_scale,
    "semantic_rephrasing": gen_rephrase,
    "implicit_reasoning_required": gen_implicit,
}
