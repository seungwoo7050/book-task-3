# 01 Offline Sync Foundations

local-first 제품을 바로 채팅 앱이나 캡스톤으로 시작하면 변수 수가 너무 많아진다. 이 프로젝트가 먼저 한 일은 queue, retry, DLQ, idempotency, merge 규칙만 떼어 내어 독립 문제로 줄이는 것이었다.

## 이번 글에서 따라갈 구현 순서

- `createTaskDraft()`에서 local task와 queue job을 동시에 만든다.
- `flushQueue()`에서 retry, DLQ, merge 규칙을 닫는다.
- RN app과 tests가 같은 queue vocabulary를 쓰도록 맞춘다.

## 새로 이해한 것: outbox는 optimistic UI가 아니라 mutation log다

이 프로젝트는 outbox를 “나중에 다시 보내는 임시 저장함” 정도로 두지 않는다. task와 queue job을 같은 생성 지점에서 만들고, idempotency key와 attempts를 같이 관리하면서 mutation log처럼 다룬다. 이 감각이 뒤의 채팅과 캡스톤까지 이어진다.

## Phase 1
### local task와 queue job을 동시에 만든다

- 당시 목표: optimistic UI record와 재전송 job이 같은 시작점을 공유하게 만든다.
- 변경 단위: `react-native/src/syncEngine.ts#createTaskDraft`
- 처음 가설: task와 queue가 따로 생기면 나중에 sync 설명이 항상 어긋난다.
- 실제 진행: `createTaskDraft()`가 `TaskRecord`와 `QueueJob`을 동시에 만들고, `taskLocalId`, `idempotencyKey`, `createdAt`을 같이 부여했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native
npm test
```

검증 신호:

- 같은 draft에서 `task.localId`와 `job.taskLocalId`가 연결된다.
- failing payload는 title에 `FAIL`이 포함될 때만 서버가 거부한다.

핵심 코드:

```ts
return {
  task: { localId, serverId: null, title, status: 'draft', ... },
  job: { taskLocalId: localId, idempotencyKey, attempts: 0, state: 'pending', ... },
};
```

왜 이 코드가 중요했는가:

outbox를 화면 부속물이 아니라 mutation log로 다루기 시작하는 지점이기 때문이다.

새로 배운 것:

- optimistic UI와 sync queue는 별개가 아니라 같은 생성 사건의 두 표현이다.

다음:

- 성공, 실패, DLQ, merge를 하나의 flush 규칙으로 묶는다.

## Phase 2
### retry, DLQ, merge를 flush 규칙으로 닫는다

- 당시 목표: queue 상태 전이를 한 함수에서 읽히게 만든다.
- 변경 단위: `react-native/src/syncEngine.ts#flushQueue`, `mergeServerAssignedFields`
- 처음 가설: retry 규칙이 분산되면 local-first가 아니라 예외 처리 모음처럼 보인다.
- 실제 진행: `flushQueue()`는 `pending`과 `failed` job만 다시 실행하고, 성공하면 `synced`, 실패하면 attempts를 올리며 `failed` 또는 `dlq`로 내린다. 성공 시에는 `mergeServerAssignedFields()`로 server id와 updatedAt만 반영한다.

CLI:

```bash
npm run typecheck
```

검증 신호:

- repeated failure는 `dlq`까지 내려간다.
- duplicate flush는 같은 `serverId`를 유지한다.

핵심 코드:

```ts
job.attempts += 1;
job.lastError = error instanceof Error ? error.message : 'unknown';
job.state = job.attempts >= maxAttempts ? 'dlq' : 'failed';
```

왜 이 코드가 중요했는가:

queue 상태 전이가 문장 설명이 아니라 명시적인 state machine처럼 읽히기 때문이다.

새로 배운 것:

- retry와 DLQ를 분리해야 실패를 감추지 않고 제품 모델의 일부로 다룰 수 있다.

다음:

- 이 vocabulary를 RN 앱과 테스트가 그대로 읽도록 만든다.

## Phase 3
### RN app과 tests가 같은 queue vocabulary를 쓴다

- 당시 목표: task/outbox/dlq/diagnostics 화면과 unit tests가 같은 모델을 바라보게 만든다.
- 변경 단위: `react-native/src/OfflineSyncStudyApp.tsx`, `react-native/tests/offline-sync.test.ts`
- 처음 가설: 앱이 예쁜 데모보다 queue summary를 직접 드러내야 docs와 테스트가 같은 언어를 유지한다.
- 실제 진행: 앱은 `snapshot.jobs`에서 outbox와 dlq 개수를 집계해 섹션 카드에 보여 줬고, 테스트는 success, repeated failure, idempotency, merge 규칙을 각각 고정했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/offline-sync.test.ts`
- `Test Suites: 1 passed`
- `Tests: 4 passed`

핵심 코드:

```ts
const outboxCount = snapshot.jobs.filter(job => job.state !== 'synced').length;
const dlqCount = snapshot.jobs.filter(job => job.state === 'dlq').length;
```

왜 이 코드가 중요했는가:

이 프로젝트가 결국 무엇을 보여 주는지, UI 안에서도 queue vocabulary로 직접 드러나기 때문이다.

새로 배운 것:

- offline-first 기초는 멋진 UX보다 queue vocabulary를 먼저 고정할 때 다음 프로젝트에 재사용된다.

다음:

- 이제 같은 vocabulary를 채팅이라는 사용자 경험 안으로 밀어 넣는다.

## 여기까지 정리

- 이 프로젝트가 남긴 핵심은 outbox를 mutation log로 읽는 감각과 retry/DLQ 상태를 숨기지 않는 vocabulary다.
- 다음 단계의 질문: 같은 규칙을 채팅 앱에 넣어도 사용자 경험과 충돌하지 않을까?
