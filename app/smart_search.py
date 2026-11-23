import math
import re
from collections import Counter
from functools import lru_cache
from typing import Any

from app.records import load_records

SEARCH_FIELDS = (
    "concept",
    "plain_definition",
    "example",
    "module_chapter",
    "risk_warning",
)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _record_text(record: dict[str, Any]) -> str:
    return " ".join(str(record.get(field, "")) for field in SEARCH_FIELDS)


@lru_cache(maxsize=1)
def _build_search_index() -> tuple[
    list[dict[str, Any]], dict[str, float], list[tuple[dict[str, float], float]]
]:
    records = load_records()
    if not records:
        return [], {}, []

    num_docs = len(records)
    doc_freqs: Counter[str] = Counter()
    doc_tokens: list[list[str]] = []

    for record in records:
        tokens = _tokenize(_record_text(record))
        doc_tokens.append(tokens)
        for t in set(tokens):
            doc_freqs[t] += 1

    idf = {
        t: math.log((num_docs + 1) / (df + 1)) + 1.0
        for t, df in doc_freqs.items()
    }

    doc_vectors: list[tuple[dict[str, float], float]] = []
    for tokens in doc_tokens:
        tf = Counter(tokens)
        vec = {t: count * idf.get(t, 1.0) for t, count in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        doc_vectors.append((vec, norm))

    return records, idf, doc_vectors


def smart_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Return records ranked by TF-IDF cosine similarity to ``query`` without heavy external dependencies."""
    if not isinstance(query, str) or not query.strip() or top_k <= 0:
        return []

    records, idf, doc_vectors = _build_search_index()
    if not records:
        return []

    q_tokens = _tokenize(query)
    q_tf = Counter(q_tokens)
    q_vec = {t: count * idf.get(t, 1.0) for t, count in q_tf.items() if t in idf}
    if not q_vec:
        return []

    q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

    scored = []
    for idx, (doc_vec, doc_norm) in enumerate(doc_vectors):
        dot = sum(q_vec[t] * doc_vec.get(t, 0.0) for t in q_vec)
        if dot > 0:
            sim = dot / (q_norm * doc_norm)
            scored.append({"record": records[idx], "score": float(sim)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
