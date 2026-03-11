from pathlib import Path

from stage03.guardrails import evaluate, load_rules


RULES = load_rules(Path('data/rules.json'))


def test_mandatory_notice_rule():
    assert 'MISSING_MANDATORY_STEP' in evaluate('해지하려면?', '절차를 안내드리겠습니다.', RULES)


def test_forbidden_promise_rule():
    assert 'UNSUPPORTED_CLAIM' in evaluate('할인돼요?', '무조건 가능합니다.', RULES)


def test_pii_rule():
    assert 'PII_EXPOSURE' in evaluate('입력할까요?', '주민번호 990101-1234567 입력하세요.', RULES)


def test_escalation_rule():
    assert 'ESCALATION_MISS' in evaluate('분쟁 접수하고 싶어요', '정책만 안내드립니다.', RULES)
