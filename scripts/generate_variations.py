from __future__ import annotations
import os
import json
import random
import yaml
from typing import Dict, Any, List

from src.utils.id import make_variant_id
from src.generators import GENERATOR_REGISTRY
from src.validate.basic import validate_jsonl_records

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out

def main():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    seed = int(cfg.get("seed", 263))
    rng = random.Random(seed)

    base_path = cfg["paths"]["base_data"]
    out_dir = cfg["paths"]["output_dir"]
    out_file = cfg["paths"]["output_file"]
    out_path = os.path.join(out_dir, out_file)
    os.makedirs(out_dir, exist_ok=True)

    families = cfg["week1"]["families"]
    include_clean = bool(cfg["week1"].get("generate_base_in_output", True))

    family_params = cfg.get("family_params", {})

    base = load_jsonl(base_path)
    if len(base) != int(cfg["week1"]["base_size"]):
        print(f"[WARN] Expected {cfg['week1']['base_size']} base examples but found {len(base)}")

    records: List[Dict[str, Any]] = []

    for ex in base:
        base_id = ex["base_id"]

        # clean version
        if include_clean:
            records.append({
                "base_id": base_id,
                "variant_id": make_variant_id(base_id, "clean", 1),
                "family": "clean",
                "source": ex.get("source", "GSM8K"),
                "config": ex.get("config", "main"),
                "split": ex.get("split", "train"),
                "deduped_index": ex.get("deduped_index"),
                "question": ex["question"],
                "final_answer": ex["final_answer"],
                "family_params": {},
                "gen_applied": True,
                "gen_notes": {},
            })

        for fam in families:
            gen_fn = GENERATOR_REGISTRY[fam]
            params = family_params.get(fam, {})
            # Derive per-example randomness while still reproducible:
            # use a sub-RNG seeded by (global_seed, base_id, family)
            sub_seed = hash((seed, base_id, fam)) & 0xFFFFFFFF
            sub_rng = random.Random(sub_seed)

            res = gen_fn(ex, sub_rng, params)

            records.append({
                "base_id": base_id,
                "variant_id": make_variant_id(base_id, fam, 1),
                "family": fam,
                "source": ex.get("source", "GSM8K"),
                "config": ex.get("config", "main"),
                "split": ex.get("split", "train"),
                "deduped_index": ex.get("deduped_index"),
                "question": res.question,
                "final_answer": res.final_answer,
                "family_params": params,
                "gen_applied": bool(res.applied),
                "gen_notes": res.notes,
            })

    # Validate
    errors = validate_jsonl_records(records)
    if errors:
        print("\n".join(["[VALIDATION ERRORS]"] + errors[:50]))
        raise SystemExit(f"Validation failed with {len(errors)} errors.")

    # Write
    with open(out_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} records to {out_path}")

if __name__ == "__main__":
    main()
