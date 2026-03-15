import json
import os
import random
import re
from datasets import load_dataset

SEED = 263
N = 100
OUT_PATH = "data/base/gsm100.jsonl"

def extract_final_answer(answer_text: str) -> str:
    marker = "####"
    if marker in answer_text:
        ans = answer_text.split(marker)[-1].strip()
    else:
        ans = answer_text.strip()

    ans = ans.replace(",", "").strip()
    m = re.search(r"-?\d+(\.\d+)?", ans)
    return m.group(0) if m else ans

def normalize_question(q: str) -> str:
    # collapse whitespace so near-identical formatting doesn't survive dedup
    return re.sub(r"\s+", " ", q.strip())

# Load dataset
ds = load_dataset("gsm8k", "main", verification_mode="no_checks")
train = ds["train"]

# Deduplicate by normalized question text only
seen_questions = set()
unique_rows = []

for ex in train:
    q_norm = normalize_question(ex["question"])
    if q_norm in seen_questions:
        continue
    seen_questions.add(q_norm)
    unique_rows.append(ex)

print(f"Raw train size: {len(train)}")
print(f"Unique train size after dedup by question: {len(unique_rows)}")

if len(unique_rows) < N:
    raise ValueError(f"Not enough unique examples to sample {N}")

# Deterministic sampling
random.seed(SEED)
idxs = random.sample(range(len(unique_rows)), N)

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    for i, idx in enumerate(idxs, start=1):
        ex = unique_rows[idx]
        base_id = f"gsm100_{i:04d}"
        record = {
            "base_id": base_id,
            "source": "GSM8K",
            "config": "main",
            "split": "train",
            "deduped_index": int(idx),
            "question": normalize_question(ex["question"]),
            "final_answer": extract_final_answer(ex["answer"]),
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Wrote {N} examples to {OUT_PATH}")