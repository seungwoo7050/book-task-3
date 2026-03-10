# Approach Log — Offline Sync Foundations

## 첫 번째 결정: FakeSyncServer를 쓸 것인가, 실제 서버를 띄울 것인가

이 프로젝트의 목적은 "동기화 로직 자체"를 검증하는 것이지, 네트워크 통신을 검증하는 것이 아니다. 그래서 실제 HTTP서버 대신 인메모리 `FakeSyncServer` 클래스를 만들었다.

`FakeSyncServer`는 두 가지만 한다:
1. `syncCreate(job)`을 호출하면 payload에 `FAIL`이 포함되어 있으면 예외를 던지고, 아니면 `serverId`를 발급한다.
2. 이미 본 `idempotencyKey`면 기존 `serverId`를 반환하고 `accepted: false`를 돌려준다.

이 설계 덕분에 테스트에서 "정상 동기화", "일시 실패", "영구 실패", "중복 요청" 네 가지 시나리오를 조합할 수 있었다.

## 두 번째 결정: QueueJob의 상태 머신 설계

큐 잡의 상태를 `pending → synced` 또는 `pending → failed → dlq` 흐름으로 설계했다.

처음에는 `pending`, `synced`, `failed` 세 가지만 있었다. 그런데 "failed인데 재시도 가능한 것"과 "failed이고 더 이상 재시도하면 안 되는 것"을 구분해야 했다. 그래서 `dlq`(Dead Letter Queue) 상태를 추가했다.

`maxAttempts`를 넘기면 자동으로 `dlq`로 이동시키는 규칙을 `flushQueue` 함수 안에 넣었다. 이 결정이 중요했던 이유는, DLQ를 별도 릴레이션이 아니라 **같은 job의 상태값**으로 표현함으로써 큐 구조를 단순하게 유지할 수 있었기 때문이다.

## 세 번째 결정: Idempotency key 생성 규칙

idempotency key를 `create-${localId}` 형태로 만들었다. 이렇게 하면 같은 로컬 리소스에 대한 create 요청은 항상 같은 키를 갖게 되고, 서버가 중복 요청을 정확히 감지할 수 있다.

다른 선택지로는 UUID를 매번 새로 만드는 방식이 있었지만, 그러면 "같은 의도의 같은 요청"을 서버가 구분할 수 없게 된다. LocalId 기반 키가 더 결정론적이고 테스트하기도 쉬웠다.

## 네 번째 결정: mergeServerAssignedFields의 범위

서버가 `serverId`와 `updatedAt`을 돌려줬을 때 로컬 레코드에 어디까지 반영할 것인가?

`title` 같은 사용자 입력 필드는 서버 응답으로 덮어쓰지 않기로 했다. 서버가 할당하는 필드(`serverId`, `updatedAt`)와 클라이언트가 소유하는 필드(`title`)를 명확히 분리한 것이다. 이 원칙은 이후 `realtime-chat`에서 메시지 text를 서버 응답으로 덮어쓰지 않는 것과 동일한 맥락이다.

## 다섯 번째 결정: flushQueue를 왜 하나의 함수로 만들었나

큐 전체를 순회하면서 각 job을 처리하고, 결과를 한 번에 반환하는 `flushQueue` 함수를 만들었다. job별로 독립 함수를 호출하는 방식도 가능했지만, "reconnect 시 한 번에 밀어내기(flush)"라는 실제 사용 패턴을 코드 구조에 반영하고 싶었다.

이 함수는 `tasks`와 `jobs` 배열을 받아서 새로운 `tasks`와 `jobs`를 반환하는 순수 함수다. 원본을 변경하지 않기 때문에 테스트에서 before/after를 자유롭게 비교할 수 있다.
