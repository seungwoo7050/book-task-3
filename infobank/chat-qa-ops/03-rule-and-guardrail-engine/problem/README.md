# 03 규칙 엔진과 가드레일 문제 정의

mandatory notice, forbidden promise, PII, escalation 규칙을 deterministic failure code로 환원하는 단계다.

## 문제 해석

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## 입력

- 해지/환불/명의변경 시 본인확인이 필요하다는 도메인 규칙
- 과장 약속, PII 노출, 민원/분쟁 escalation 조건

## 기대 산출물

- `python/data/rules.json` rule set
- `python/src/stage03/guardrails.py` 룰 엔진
- failure type별 pytest

## 완료 기준

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## 현재 확인 가능한 증거

- `python/tests/test_guardrails.py`가 네 가지 규칙을 각각 분리 검증한다.
- 룰은 JSON 파일로 분리되어 정책 변경이 코드 diff 없이도 보인다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: rule matcher, deterministic guardrail tests
- 이번 단계에서 일부러 제외한 범위: YAML loader 대신 JSON 사용
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
