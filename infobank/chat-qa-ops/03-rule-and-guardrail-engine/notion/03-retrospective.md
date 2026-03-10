# 03-rule-and-guardrail-engine 회고

## 이번 stage로 강화된 점

- 실패 이유가 명확해 품질 논의를 human-review와 연결하기 쉽다.
- golden regression에서 재현 가능한 failure taxonomy를 제공한다.

## 아직 약한 부분

- rule coverage 확장은 수동 유지보수 비용이 든다.

## 학생이 여기서 바로 가져갈 것

- 정책 위반을 점수 저하가 아니라 명시적인 failure code로 남기는 방식
- 한국어 상담 시나리오에서도 deterministic rule이 충분한 설명력을 가질 수 있게 만드는 방식

## 다음 stage로 넘기는 자산

- rule-based guardrail
- failure type taxonomy
- 한국어 상담 시나리오의 escalation 조건

## 05-development-timeline.md와 같이 읽을 포인트

- guardrail 테스트를 먼저 읽고 나서 규칙 정의 파일을 보면 failure taxonomy가 더 잘 보인다.
- 이후 claim/evidence stage를 볼 때도, rule violation과 groundedness failure를 섞지 않는 기준을 여기서 다시 확인한다.

## 나중에 다시 볼 것

- 실제 상담 로그를 더 확보하면 synonym dictionary를 늘리거나 regex DSL을 도입할 수 있다.
