import json
import os
from typing import List, Dict

# Simple in-memory knowledge index for prototype
KNOWLEDGE_INDEX: List[Dict] = []


def load_from_dicts(docs: List[Dict]) -> int:
    """Load a list of dict documents into the knowledge index.

    Expected doc format: { "id": str, "title": str, "text": str, "lang": "hi"/"en" }
    Returns number of docs added.
    """
    added = 0
    for d in docs:
        if not isinstance(d, dict):
            continue
        entry = {
            "id": str(d.get("id", len(KNOWLEDGE_INDEX) + 1)),
            "title": d.get("title", ""),
            "text": d.get("text", ""),
            "lang": d.get("lang", "hi")
        }
        KNOWLEDGE_INDEX.append(entry)
        added += 1
    return added


def load_from_file(path: str) -> int:
    """Load JSON file from `path`. Expects an array of docs or a single doc.
    Returns number of docs loaded.
    """
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return load_from_dicts(data)
    elif isinstance(data, dict):
        return load_from_dicts([data])
    return 0


def clear_index():
    KNOWLEDGE_INDEX.clear()


def query_knowledge(query: str, top_k: int = 3) -> List[Dict]:
    """Very simple keyword overlap scoring to return top_k knowledge entries.

    This is a prototype retrieval method. For production, replace with embeddings + ANN search.
    """
    qtokens = set([t.strip().lower() for t in query.split() if t.strip()])
    scored = []
    for doc in KNOWLEDGE_INDEX:
        text = (doc.get("title", "") + " " + doc.get("text", "")).lower()
        tokens = set([t.strip() for t in text.split() if t.strip()])
        score = len(qtokens.intersection(tokens))
        scored.append((score, doc))
    scored = sorted(scored, key=lambda x: x[0], reverse=True)
    results = [d for s, d in scored if s > 0][:top_k]
    # If no matches, fall back to returning top_k recent docs
    if not results and KNOWLEDGE_INDEX:
        return KNOWLEDGE_INDEX[:top_k]
    return results
