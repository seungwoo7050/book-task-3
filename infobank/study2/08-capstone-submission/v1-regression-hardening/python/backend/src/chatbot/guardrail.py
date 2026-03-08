from __future__ import annotations

import re

from core.types import RuleResult

FORBIDDEN_PROMISE_PATTERN = re.compile(r"(할인|감면|면제|무료).{0,10}(해드리|해 드리|적용해|제공)")
PII_RRN_PATTERN = re.compile(r"\d{6}[-−]?[1-4]\d{6}")



def run_online_guardrail(response: str) -> list[RuleResult]:
    results: list[RuleResult] = []
    if FORBIDDEN_PROMISE_PATTERN.search(response):
        results.append(
            RuleResult(
                rule_id="guardrail-forbid-discount-promise",
                severity="critical",
                failure_type="FORBIDDEN_PROMISE",
                matched=True,
                evidence=response,
                message="응답에서 금지 약속 문구가 감지됨",
            )
        )
    if PII_RRN_PATTERN.search(response):
        results.append(
            RuleResult(
                rule_id="guardrail-pii-rrn",
                severity="critical",
                failure_type="PII_EXPOSURE",
                matched=True,
                evidence=response,
                message="응답에서 주민등록번호 패턴이 감지됨",
            )
        )
    return results
