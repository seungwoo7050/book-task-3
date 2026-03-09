# Knowledge Index

## Reusable concepts

- Outbox pattern:
  - DB transaction과 message publish 사이의 경계를 durable row로 끊는 패턴이다.
- Publish-oriented flow:
  - 요청 처리 자체보다 event handoff를 우선하는 설계다.
- DLQ thinking:
  - 재처리 불가능한 메시지를 별도로 격리해 관찰하는 사고방식이다.

## Glossary

- broker:
  - producer와 consumer 사이에서 메시지를 전달하는 시스템이다.
- outbox row:
  - 아직 publish되지 않았거나 publish history를 담는 durable event record다.

## References

- title:
  - E-event-messaging-lab Notes README
  - URL or local path: `/Users/woopinbell/work/web-pong/study2/labs/E-event-messaging-lab/docs/README.md`
  - checked date: `2026-03-09`
  - why it was consulted: 현재 구현 범위와 부족한 부분을 맞추기 위해 확인했다
  - what was learned: outbox는 구현되어 있지만 long-running publisher와 DLQ는 후속 단계다
  - what changed: 디버그 로그에서 과장 방지를 핵심 이슈로 적었다

