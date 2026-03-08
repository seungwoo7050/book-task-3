import json
from pathlib import Path


def seed_knowledge_base(root: Path) -> dict[str, str]:
    return {path.name: path.read_text(encoding="utf-8").strip() for path in sorted(root.glob('*.md'))}


def retrieve(query: str, kb: dict[str, str]) -> list[str]:
    query_terms = {token for token in query.split() if token}
    scored = []
    for doc_id, content in kb.items():
        score = sum(1 for term in query_terms if term in content or term in doc_id)
        if score:
            scored.append((score, doc_id))
    scored.sort(reverse=True)
    return [doc_id for _, doc_id in scored] or list(kb)[:1]


def run_replay(path: Path, kb_root: Path) -> dict[str, object]:
    kb = seed_knowledge_base(kb_root)
    replay = json.loads(path.read_text(encoding='utf-8'))
    items = []
    for session in replay['sessions']:
        docs = retrieve(session['user_message'], kb)
        items.append({'user_message': session['user_message'], 'retrieved_doc_ids': docs})
    return {'session_count': len(items), 'items': items}
