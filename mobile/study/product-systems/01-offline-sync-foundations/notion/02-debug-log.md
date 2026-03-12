# Debug Log — Offline Sync Foundations

## DLQ 상태 전이 버그

처음 `flushQueue`를 구현했을 때 DLQ 판정에 미묘한 버그가 있었다. `failed` 상태인 job을 다시 flush할 때 `attempts`를 증가시킨 뒤에 `maxAttempts`와 비교해야 하는데, 비교를 먼저 하고 증가를 나중에 하는 순서로 작성해서 DLQ 전환이 한 번 늦게 발생했다.

테스트에서 "두 번째 flush 후 dlq"를 기대했는데 "세 번째 flush 후 dlq"가 되는 현상이었다. catch 블록 안에서 `attempts += 1`을 먼저 하고, 그 다음에 `>=` 비교를 하도록 순서를 바꿔서 해결했다.

이 경험은 "상태 전이 로직에서 연산 순서가 결과를 바꾼다"는 아주 기본적이지만 실수하기 쉬운 패턴을 다시 상기시켰다.

## FakeSyncServer의 seenKeys 초기화 문제

테스트에서 `FakeSyncServer` 인스턴스를 테스트 간에 공유하면 `seenKeys`가 쌓여서 idempotency 테스트 결과가 달라지는 문제가 있었다. 각 테스트에서 새 인스턴스를 생성하도록 바꿨다.

다만 idempotency 테스트(`keeps idempotency stable on duplicate flushes`)에서는 의도적으로 **같은** 서버 인스턴스를 두 번의 flush에 걸쳐 사용한다. 이 구분이 중요하다 — "서버 상태가 유지되는 상황에서 같은 키로 두 번 요청하면 같은 serverId를 받는다"를 검증하는 것이기 때문이다.

## AsyncStorage mock 미사용

초기에는 `@react-native-async-storage/async-storage`를 실제로 사용해 큐를 영속화하려 했다. 하지만 이 프로젝트의 핵심은 영속화 계층이 아니라 큐 로직 자체이므로, AsyncStorage 연동은 앱 shell 수준에만 두고 테스트 대상에서 제외했다. 영속화된 outbox는 `incident-ops-mobile-client`에서 본격적으로 다룬다.
