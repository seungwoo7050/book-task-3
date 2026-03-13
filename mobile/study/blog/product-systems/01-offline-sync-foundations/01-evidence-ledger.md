# Evidence Ledger: 01 Offline Sync Foundations

## 독립 프로젝트 판정

- 판정: 처리
- 근거: queue/retry/DLQ 문제를 RN app, sync engine, tests, docs로 독립적으로 설명할 수 있는 최소 단위다.
- 소스 경로: `mobile/study/product-systems/01-offline-sync-foundations`

## 사용한 근거

- `mobile/study/product-systems/01-offline-sync-foundations/README.md`
- `mobile/study/product-systems/01-offline-sync-foundations/problem/README.md`
- `mobile/study/product-systems/01-offline-sync-foundations/react-native/README.md`
- `mobile/study/product-systems/01-offline-sync-foundations/docs/concepts/queue-replay-model.md`
- `mobile/study/product-systems/01-offline-sync-foundations/react-native/src/syncEngine.ts`
- `mobile/study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`
- `mobile/study/product-systems/01-offline-sync-foundations/react-native/tests/offline-sync.test.ts`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native
npm install --no-audit --no-fund
npm run verify
```

## Chronology Ledger

### Phase 1 | outbox와 queue job을 같은 생성 지점에서 만든다

- 당시 목표: local task와 queue mutation을 동시에 만들고 idempotency key를 붙인다.
- 변경 단위: `react-native/src/syncEngine.ts#createTaskDraft`
- 처음 가설: optimistic UI와 재전송 job이 따로 생성되면 나중에 동기화 설명이 어긋난다.
- 실제 조치: `createTaskDraft()`가 `task`와 `job`을 동시에 만들고 `create-local-x` idempotency key를 함께 부여하게 했다.
- CLI:
```bash
npm test
```
- 검증 신호:
- `TaskRecord`와 `QueueJob`은 같은 `localId`/`taskLocalId`를 공유한다.
- failing payload는 title에 `FAIL`이 포함되면 서버가 거부한다.
- 핵심 코드 앵커:
```ts
return {
  task: { localId, serverId: null, title, status: 'draft', ... },
  job: { taskLocalId: localId, idempotencyKey, state: 'pending', ... },
};
```
- 새로 배운 것: outbox는 UI 흔적이 아니라 재전송 가능한 mutation log다.
- 다음: 서버 응답과 실패 상태를 queue flush 규칙으로 정리한다.

### Phase 2 | retry, DLQ, merge를 flush 규칙으로 닫는다

- 당시 목표: 성공, 일시 실패, DLQ 전환, server-assigned field merge를 한 함수에서 다룬다.
- 변경 단위: `react-native/src/syncEngine.ts#flushQueue`, `mergeServerAssignedFields`
- 처음 가설: retry 규칙이 흩어지면 local-first 설명이 아니라 예외 처리 모음이 된다.
- 실제 조치: `flushQueue()`가 `pending`과 `failed` job만 다시 실행하고, 성공하면 `synced`, 실패하면 attempt 증가와 함께 `failed` 또는 `dlq`로 바꾸게 했다.
- CLI:
```bash
npm run typecheck
```
- 검증 신호:
- `attempts >= maxAttempts`일 때 `dlq`로 내려간다.
- duplicate flush는 같은 `serverId`를 유지한다.
- 핵심 코드 앵커:
```ts
job.attempts += 1;
job.lastError = error instanceof Error ? error.message : 'unknown';
job.state = job.attempts >= maxAttempts ? 'dlq' : 'failed';
```
- 새로 배운 것: retry와 DLQ를 분리해야 실패를 숨기지 않고 상태로 설명할 수 있다.
- 다음: 이 규칙을 RN 앱에서 섹션별로 드러낸다.

### Phase 3 | RN 앱과 테스트가 같은 sync vocabulary를 쓴다

- 당시 목표: task/outbox/dlq/diagnostics 화면과 unit tests가 같은 모델을 읽게 만든다.
- 변경 단위: `react-native/src/OfflineSyncStudyApp.tsx`, `react-native/tests/offline-sync.test.ts`
- 처음 가설: 앱 화면이 요약 카드라도 queue summary를 직접 읽어야 docs와 테스트가 같은 언어를 유지할 수 있다.
- 실제 조치: 앱은 `snapshot.jobs`에서 outbox와 dlq 개수를 계산해 섹션 카드로 보여 줬고, 테스트는 sync success, repeated failure, idempotency, merge 규칙을 각각 고정했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/offline-sync.test.ts`
- `Test Suites: 1 passed`, `Tests: 4 passed`
- 핵심 코드 앵커:
```ts
const outboxCount = snapshot.jobs.filter(job => job.state !== 'synced').length;
const dlqCount = snapshot.jobs.filter(job => job.state === 'dlq').length;
```
- 새로 배운 것: offline-first 기초는 UI보다 queue vocabulary를 먼저 고정할 때 다음 프로젝트에 재사용된다.
- 다음: 같은 규칙을 이제 채팅이라는 사용자 경험 안으로 밀어 넣는다.
