from __future__ import annotations

def make_variant_id(base_id: str, family: str, vnum: int = 1) -> str:
    """
    Example: gsm50_0001__irrelevant_numeric_distractor__v1
    """
    return f"{base_id}__{family}__v{vnum}"
