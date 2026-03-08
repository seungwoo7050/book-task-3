# Stage 03 Guardrails Docs

mandatory notice, forbidden promise, PII, escalation 규칙을 deterministic failure code로 환원하는 단계다.

## Concept Focus

- rule-based guardrail
- failure type taxonomy
- 한국어 상담 시나리오의 escalation 조건

## Capstone Mapping

- v0에서 추가한 escalation rule과 MP2 guardrail tests를 축소한 pack이다.
- failure codes는 dashboard failures 페이지와 golden set assertion의 공통 언어가 된다.

## Implementation Snapshot

- 구현됨: rule matcher, deterministic guardrail tests
- staged/known gap: YAML loader 대신 JSON 사용

## Verification

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

## Notes

- 테스트는 네 가지 대표 failure type을 각각 직접 검증한다.
- 이 단계는 recall보다 설명 가능성과 deterministic behavior를 우선한다.
