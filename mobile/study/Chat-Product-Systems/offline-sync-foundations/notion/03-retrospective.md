# Retrospective — Offline Sync Foundations

## 가장 크게 배운 것

오프라인 동기화는 "데이터를 나중에 보내는 것"이 아니라, **"실패를 구조적으로 다루는 것"**이었다.

처음에는 queue에 넣고 flush하면 끝이라고 생각했다. 하지만 실제로 만들어보니 "실패 시 재시도", "영구 실패 격리", "중복 전송 방지"라는 세 가지 방어선이 없으면 큐가 의미 없었다. retry 없는 큐는 그냥 지연된 단발 요청이고, DLQ 없는 retry는 무한 루프이며, idempotency 없는 재전송은 데이터 오염이다.

이 세 가지를 하나의 `flushQueue` 함수에 응축하고, 각각을 독립 테스트로 증명한 경험이 이 프로젝트의 핵심 성과다.

## 예상과 달랐던 것

**DLQ를 별도 스토어가 아니라 상태값으로 표현하는 게 더 나았다.** 처음에는 `dlqJobs: QueueJob[]`을 별도로 관리하려 했는데, 같은 job 배열 안에서 `state: 'dlq'`로 표현하니 구현도 간단하고, "전체 큐 상태를 한눈에 보기"도 쉬워졌다.

**Idempotency key 설계가 클라이언트 로직의 핵심이었다.** 서버가 idempotency를 보장한다고 해서 클라이언트가 아무 키나 보내도 되는 게 아니었다. LocalId 기반 결정론적 키를 만들어야 "같은 의도의 같은 요청"에 대해 서버가 정확히 중복을 감지할 수 있었다.

## 약했던 점

- 실제 네트워크 단절/복구 시뮬레이션이 없다. `FakeSyncServer`는 동기 호출이라 비동기 타이밍 문제를 재현하지 못한다.
- AsyncStorage 연동을 생략했기 때문에, 앱이 종료됐다가 다시 시작한 후 큐가 복구되는 시나리오를 다루지 않았다.
- conflict merge가 `mergeServerAssignedFields` 한 함수로 끝나서, 실제 서버/클라이언트 동시 수정 충돌은 다루지 않았다.

## 다음 단계에 넘긴 것

- 채팅 도메인에서의 sync 적용 → `realtime-chat`
- 영속화된 outbox + 수동 retry UI → `incident-ops-mobile-client`
- 실제 서버와의 연동 → `incident-ops-mobile`의 node-server
