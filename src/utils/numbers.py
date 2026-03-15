from __future__ import annotations
import random
from typing import List, Set

def pick_distinct_ints(rng: random.Random, k: int, avoid: Set[int], lo: int = 7, hi: int = 200) -> List[int]:
    """
    Pick k integers in [lo, hi] that avoid collisions with avoid.
    """
    result = []
    tries = 0
    while len(result) < k and tries < 2000:
        tries += 1
        x = rng.randint(lo, hi)
        if x in avoid:
            continue
        if x in result:
            continue
        result.append(x)
    if len(result) < k:
        # fallback: expand range
        while len(result) < k:
            x = rng.randint(hi + 1, hi + 1000)
            if x not in avoid and x not in result:
                result.append(x)
    return result

def numbers_in_text_as_ints(nums: List[str]) -> Set[int]:
    out = set()
    for n in nums:
        try:
            if "." in n:
                # ignore decimals for collision set
                continue
            out.add(int(n))
        except Exception:
            pass
    return out
