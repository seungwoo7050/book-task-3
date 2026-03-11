import json
from pathlib import Path


def evaluate_case(required_doc_ids: list[str], actual_doc_ids: list[str]) -> dict[str, object]:
    passed = any(doc_id in actual_doc_ids for doc_id in required_doc_ids)
    return {'passed': passed, 'reason_codes': [] if passed else ['MISSING_REQUIRED_EVIDENCE_DOC']}


def load_manifest(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding='utf-8'))
