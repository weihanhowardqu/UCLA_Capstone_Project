from __future__ import annotations
import json
from typing import Dict, Any, List, Tuple, Set

def validate_jsonl_records(records: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    required = ["base_id", "variant_id", "family", "source", "question", "final_answer"]

    seen_variant_ids: Set[str] = set()
    seen_questions: Set[str] = set()

    for i, r in enumerate(records):
        for k in required:
            if k not in r:
                errors.append(f"Record {i} missing required field: {k}")
        vid = r.get("variant_id")
        if vid:
            if vid in seen_variant_ids:
                errors.append(f"Duplicate variant_id: {vid}")
            seen_variant_ids.add(vid)

        q = r.get("question", "")
        if q:
            if q in seen_questions:
                errors.append(f"Duplicate question text at record {i} (possible no-op)")
            seen_questions.add(q)

        ans = str(r.get("final_answer", "")).strip()
        try:
            float(ans)
        except Exception:
            errors.append(f"Non-numeric final_answer at record {i}: {ans}")

    return errors
