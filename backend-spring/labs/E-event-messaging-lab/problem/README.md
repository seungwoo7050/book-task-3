# E-event-messaging-lab 문제 정의

Spring 백엔드가 request-response만으로 끝나지 않고 이벤트 기반 처리로 넘어갈 때 어떤 경계가 필요한지 보여주는 랩을 만든다.

## 성공 기준

- 도메인 변경 사실을 outbox record로 남기는 흐름이 존재한다.
- "이벤트 생성"과 "브로커 publish"를 다른 문제로 나눠 설명할 수 있다.
- Kafka/Redpanda가 왜 필요한지 handoff boundary 관점에서 설명 가능하다.

## 이번 단계에서 다루지 않는 것

- production-grade publisher worker
- real consumer contract 검증
- DLQ와 retry 정책의 완성 구현

이 디렉터리는 구현 코드가 아니라 canonical problem statement와 범위 제약을 기록한다.
