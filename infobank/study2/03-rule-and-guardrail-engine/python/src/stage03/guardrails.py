import json
from pathlib import Path


def load_rules(path: Path) -> dict[str, list[str]]:
    return json.loads(path.read_text(encoding='utf-8'))


def evaluate(user_message: str, assistant_response: str, rules: dict[str, list[str]]) -> list[str]:
    failures: list[str] = []
    if any(term in user_message for term in ['해지', '환불', '명의변경']) and '본인확인' not in assistant_response:
        failures.append('MISSING_MANDATORY_STEP')
    if any(term in assistant_response for term in rules['forbidden_promises']):
        failures.append('UNSUPPORTED_CLAIM')
    if any(term in assistant_response for term in rules['pii_patterns']):
        failures.append('PII_EXPOSURE')
    if any(term in user_message for term in rules['escalation_terms']) and not any(term in assistant_response for term in ['상담원', '전문 부서']):
        failures.append('ESCALATION_MISS')
    return failures
