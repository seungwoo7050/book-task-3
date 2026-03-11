# 03-rule-and-guardrail-engine 디버그 기록

## 검증 메모

- 테스트는 네 가지 대표 failure type을 각각 직접 검증한다.
- 이 단계는 recall보다 설명 가능성과 deterministic behavior를 우선한다.

## 실패 사례와 수정 내용

### 사례 1
- 증상: 민원 또는 분쟁 표현이 들어와도 상담원 이관 부재가 따로 보이지 않을 수 있었다.
- 원인: escalation 규칙을 mandatory notice와 같은 bucket으로 섞으면 원인 분석이 어려웠다.
- 수정: escalation 전용 failure type과 trigger term 목록을 분리했다.
- 확인: `test_escalation_rule`이 `ESCALATION_MISS`를 직접 기대한다.

## 재발 방지 체크리스트

- `python/data/rules.json`
- `python/src/stage03/guardrails.py`
- `python/tests/test_guardrails.py`
