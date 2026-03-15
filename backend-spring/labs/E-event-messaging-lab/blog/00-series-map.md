# E-event-messaging-lab series map

이 시리즈는 `E-event-messaging-lab`을 "Kafka를 붙인 lab"이 아니라 "DB 안에 남겨 둔 outbox 사실을 언제 publish-ready 상태로 볼 것인가"라는 문제로 다시 읽는다. 실제 구현은 이벤트 브로커 연동보다 outbox row 생성과 상태 전이에 훨씬 더 가깝다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   outbox row 생성, `PENDING -> PUBLISHED` 전이, Kafka 부재 상태에서의 실제 동작을 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 이 lab에서 "publish"는 실제로 무엇을 의미하는가
- Kafka/Redpanda dependency가 있어도 runtime은 왜 broker 없이 동작하는가
- outbox boundary를 설명하는 데 필요한 것과 아직 빠져 있는 것은 무엇인가
