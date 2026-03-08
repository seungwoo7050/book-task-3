from __future__ import annotations

from evaluator.rule_eval import evaluate_rules


def test_forbidden_promise_is_critical():
    results = evaluate_rules(
        user_message="할인 받을 수 있어요?",
        assistant_response="특별히 무료로 해드리겠습니다.",
        rules_dir="backend/rules",
    )
    assert any(item.failure_type == "FORBIDDEN_PROMISE" and item.severity == "critical" for item in results)



def test_pii_detection_is_critical():
    results = evaluate_rules(
        user_message="",
        assistant_response="주민등록번호는 900101-1234567 입니다.",
        rules_dir="backend/rules",
    )
    assert any(item.failure_type == "PII_EXPOSURE" and item.severity == "critical" for item in results)



def test_mandatory_notice_warning():
    results = evaluate_rules(
        user_message="해지하고 싶어요",
        assistant_response="바로 접수 가능합니다.",
        rules_dir="backend/rules",
    )
    assert any(item.failure_type == "MISSING_MANDATORY_STEP" for item in results)


def test_clean_response_has_no_critical_violation():
    results = evaluate_rules(
        user_message="베이직 요금 알려주세요",
        assistant_response="베이직 요금제는 월 29,000원이며 부가세 포함입니다.",
        rules_dir="backend/rules",
    )
    assert all(item.severity != "critical" for item in results)
