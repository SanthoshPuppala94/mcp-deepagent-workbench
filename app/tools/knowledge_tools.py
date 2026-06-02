from pathlib import Path

from app.config import KNOWLEDGE_DIR


def search_knowledge(query: str, limit: int = 3) -> list[dict[str, str | int]]:
    terms = {term.lower() for term in query.split() if len(term) > 2}
    results: list[dict[str, str | int]] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        score = sum(text.lower().count(term) for term in terms)
        if score:
            results.append({"source": path.name, "score": score, "text": text[:1200]})
    return sorted(results, key=lambda item: int(item["score"]), reverse=True)[:limit]


def read_resource_file(name: str) -> str:
    safe_name = Path(name).name
    path = KNOWLEDGE_DIR / safe_name
    if not path.exists():
        raise FileNotFoundError(f"Knowledge resource not found: {safe_name}")
    return path.read_text(encoding="utf-8")

