# E-event-messaging-lab 설계 메모

이 문서는 이벤트 랩이 현재 무엇을 증명했고 무엇을 아직 증명하지 않았는지 정리한다.

## 현재 구현 범위

- outbox table과 JPA entity
- order event 생성 endpoint
- pending -> published lifecycle 예시
- Redpanda-ready Compose 환경

## 의도적 단순화

- long-running publisher worker는 아직 없다
- Kafka delivery는 state transition 설명이 중심이다
- DLQ와 retry는 개념과 문서 수준으로 남겨 두었다

## 다음 개선 후보

- scheduled publisher job 추가
- real Kafka publish/consume 검증
- delivery failure metadata와 replay 판단 근거 저장
