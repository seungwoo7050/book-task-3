# 03-rule-and-guardrail-engine 문제 정의

## 이 stage가 푸는 문제

mandatory notice, forbidden promise, PII, escalation 규칙을 deterministic failure code로 환원하는 단계다.

## 성공 기준

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## 왜 지금 이 단계를 먼저 보는가

- v0에서 추가한 escalation rule과 MP2 guardrail tests를 축소한 pack이다.
- failure codes는 dashboard failures 페이지와 golden set assertion의 공통 언어가 된다.

## 먼저 알고 있으면 좋은 것

- 상담 품질 평가가 단순 친절도보다 안전성과 정책 준수를 우선해야 함을 이해해야 한다.

## 확인할 증거

- `python/tests/test_guardrails.py`가 네 가지 규칙을 각각 분리 검증한다.
- 룰은 JSON 파일로 분리되어 정책 변경이 코드 diff 없이도 보인다.

## 아직 남아 있는 불확실성

동의어와 문맥 변형을 모두 포착하지는 못한다. 이 pack은 rule surface를 설명하기 위한 최소 범위다.
