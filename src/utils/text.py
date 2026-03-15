from __future__ import annotations
import re
from typing import List, Tuple

_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_NUMBER = re.compile(r"(?<!\w)(?:\d+(?:\.\d+)?)")

def normalize_spaces(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\s+", " ", s).strip()
    return s

def ensure_period(s: str) -> str:
    s = s.rstrip()
    if not s.endswith((".", "?", "!")):
        return s + "."
    return s

def append_sentence(question: str, sentence: str) -> str:
    q = normalize_spaces(question)
    q = ensure_period(q)
    sentence = sentence.strip()
    if not sentence:
        return q
    # Ensure a space before sentence
    if not sentence[0].isalnum() and sentence[0] not in ("(", '"', "'"):
        sentence = " " + sentence
    return q + " " + sentence

def extract_numbers(s: str) -> List[str]:
    return _NUMBER.findall(s)

def extract_titlecase_names(s: str) -> List[str]:
    """
    Very light heuristic: any TitleCase token not at sentence start? We'll still keep it simple.
    """
    tokens = re.findall(r"\b[A-Z][a-z]+\b", s)
    # Filter common words that appear titlecased at sentence start in GSM
    stop = {"If", "How", "What", "On", "In", "At", "After", "When", "Then", "A", "An", "The"}
    return [t for t in tokens if t not in stop]

def safe_replace_whole_word(text: str, old: str, new: str) -> str:
    """
    Replace whole-word occurrences only.
    """
    pattern = re.compile(rf"\b{re.escape(old)}\b")
    return pattern.sub(new, text)

def find_units_tokens(s: str) -> List[str]:
    """
    Return unit tokens that appear in text; used for cautious unit conversions.
    """
    units = ["hour", "hours", "minute", "minutes", "dollar", "dollars", "cent", "cents",
             "ounce", "ounces", "cup", "cups", "pint", "pints", "feet", "foot", "yard", "yards"]
    lower = s.lower()
    return [u for u in units if re.search(rf"\b{re.escape(u)}\b", lower)]
