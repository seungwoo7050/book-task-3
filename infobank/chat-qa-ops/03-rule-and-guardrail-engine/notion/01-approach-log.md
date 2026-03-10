# 03-rule-and-guardrail-engine 접근 기록

## 이 stage의 질문

상담 품질 관리에서 반드시 잡아야 하는 안전 규칙을 어떻게 설명 가능하게 구현할 것인가?

## 선택한 방향

- 실패 원인을 `MISSING_MANDATORY_STEP`, `UNSUPPORTED_CLAIM`, `PII_EXPOSURE`, `ESCALATION_MISS`로 분리했다. 이유: dashboard와 golden set이 어떤 축에서 실패했는지 바로 읽어야 하기 때문이다.
- 정책 소스는 JSON으로 두고 engine은 단순 membership 검사로 유지했다. 이유: stage 목표가 regex DSL 확장이 아니라 규칙 종류를 분명히 드러내는 데 있기 때문이다.

## 제외한 대안

- stage 단계에서 LLM safety classifier에 의존하는 방식
- 하나의 generic compliance score만 남기고 failure type을 버리는 방식

## 선택 기준

- mandatory notice, unsupported claim, PII exposure, escalation miss가 각각 독립 코드로 검출된다.
- LLM 없이도 재현 가능한 deterministic regression이 가능하다.
- 후속 score merge에서 compliance 축을 해석할 수 있다.

## 커리큘럼 안에서의 역할

- v0에서 추가한 escalation rule과 MP2 guardrail tests를 축소한 pack이다.
- failure codes는 dashboard failures 페이지와 golden set assertion의 공통 언어가 된다.

## 아직 열어 둔 판단

동의어와 문맥 변형을 모두 포착하지는 못한다. 이 pack은 rule surface를 설명하기 위한 최소 범위다.
