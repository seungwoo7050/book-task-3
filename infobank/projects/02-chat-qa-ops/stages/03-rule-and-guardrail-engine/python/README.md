# Python 구현 안내

mandatory notice, 금지 약속, PII 노출, escalation miss를 작은 규칙 엔진으로 검증한다. rule 데이터와 엔진 코드를 분리해 실패 유형을 설명 가능하게 유지한다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. 네 가지 핵심 failure type이 모두 pytest로 재현된다.
- 남은 범위: 복잡한 regex DSL이나 외부 rule engine은 포함하지 않는다.

## 먼저 볼 파일

- `data/rules.json`
- `src/stage03/guardrails.py`
- `tests/test_guardrails.py`
