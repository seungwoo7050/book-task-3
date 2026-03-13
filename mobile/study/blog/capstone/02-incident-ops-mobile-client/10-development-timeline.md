# 02 Incident Ops Mobile Client

`incident-ops-mobile`이 contract correctness를 먼저 증명하는 프로젝트였다면, 이 프로젝트는 같은 domain을 채용 제출용 React Native 완성작으로 다시 쌓는 단계다. auth, feed, role action, persistent outbox, replay-safe realtime, 발표용 데모 자료까지 모두 한 폴더 안에 모였고, 그래서 글도 제품 흐름 중심으로 다시 써야 한다.

## 이번 글에서 따라갈 구현 순서

- auth, session restore, navigation shell을 먼저 닫는다.
- persistent outbox와 optimistic incident list로 offline recovery를 제품 surface 안에 넣는다.
- realtime replay, server demo, Maestro, portfolio capture를 묶어 delivery package를 만든다.

## 새로 이해한 것: hiring-facing 완성작은 기능 목록보다 복구 흐름과 발표 재현성이 더 중요하다

이 프로젝트가 중요한 이유는 incident CRUD를 하나 더 만들었기 때문이 아니다. 같은 domain 위에서 session restore, queue retry, replay cursor, role-based action, 발표용 flow까지 한 번에 설명해야 비로소 “완성작”이 된다. 그래서 여기서는 단순 화면 구현보다 bootstrap과 recovery가 얼마나 재현 가능하게 남았는지가 더 중요해진다.

## Phase 1
### auth, session restore, navigation shell을 먼저 닫는다

- 당시 목표: login 이후의 화면 흐름과 앱 재실행 복구를 먼저 안정화한다.
- 변경 단위: `react-native/src/app/AppModel.tsx`, `react-native/src/navigation/RootNavigator.tsx`, `react-native/src/lib/storage.ts`
- 처음 가설: auth와 bootstrap이 흔들리면 이후 feed, outbox, realtime은 모두 불안정해진다.
- 실제 진행: `AppModel.tsx`는 settings, session, outbox, lastEventId를 `Promise.all`로 읽어 bootstrap하고, `RootNavigator.tsx`는 loading/auth/tab shell을 session 상태로 분기한다. storage helper는 session, settings, outbox, event cursor를 각각 영속화한다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native
npm run verify
```

검증 신호:

- current replay에서 `PASS __tests__/storage.test.ts`
- storage test는 session, settings, outbox, `lastEventId = 12` round-trip을 확인한다.
- 반면 `__tests__/app-shell.test.tsx`는 현재 실패한다.
- 실패 메시지는 React Query async update 경고와 함께 `Unable to find an element with testID: login-user-id-input`이다.

핵심 코드:

```ts
const [savedSettings, savedSession, savedOutbox, savedLastEventId] =
  await Promise.all([
    loadSettings(appStorage),
    loadSession(appStorage),
    loadOutbox(appStorage),
    loadLastEventId(appStorage),
  ]);
```

왜 이 코드가 중요했는가:

이 앱이 단순 시작 화면이 아니라, 재실행 이후에도 같은 운영 상태를 복원하는 제품이어야 한다는 요구를 직접 반영하기 때문이다.

새로 배운 것:

- 제품형 RN 앱에서는 bootstrap lifecycle이 별도 기능처럼 다뤄져야 한다.

다음:

- offline queue와 optimistic incident list를 제품 surface 안으로 끌어들인다.

## Phase 2
### persistent outbox와 optimistic incident list를 제품 surface로 만든다

- 당시 목표: 네트워크 실패가 일어났을 때 mutation이 사라지지 않고 feed와 outbox에 모두 반영되게 한다.
- 변경 단위: `react-native/src/lib/outbox.ts`, `react-native/src/app/AppModel.tsx`, `react-native/src/lib/storage.ts`
- 처음 가설: hiring-facing 앱이라면 성공 케이스보다 실패 후 복구를 더 분명히 보여 줄 수 있어야 한다.
- 실제 진행: `createQueuedMutation`으로 job을 만들고, `markQueuedMutationFailed`가 시도 횟수를 누적하며, `buildIncidentList`는 optimistic create item과 pending action overlay를 server incident list 위에 합친다. `flushPendingMutations()`는 성공 시 synced 처리와 query invalidation을, 실패 시 retry/fail 전이를 담당한다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS __tests__/outbox.test.ts`
- failed job은 3회 시도 후 `failed`로 이동한다.
- optimistic create item은 `local-` prefix id, `queued` sync state, pending action label을 가진다.

핵심 코드:

```ts
return {
  ...item,
  attempts,
  state: attempts >= MAX_OUTBOX_ATTEMPTS ? 'failed' : 'pending',
  lastError,
};
```

왜 이 코드가 중요했는가:

offline recovery를 숨겨진 내부 구현이 아니라, 제품이 사용자의 실패 경험을 어떻게 다루는지 보여 주는 핵심 surface로 만들기 때문이다.

새로 배운 것:

- outbox는 “나중에 동기화하자” 수준의 보조 기능이 아니라, feed와 같은 비중으로 설명해야 하는 제품 설계 요소다.

다음:

- realtime replay와 demo 자료를 붙여 완성작의 재현성을 닫는다.

## Phase 3
### realtime replay, server demo, portfolio capture를 묶어 delivery package로 만든다

- 당시 목표: 이 앱을 코드뿐 아니라 발표와 재현 흐름까지 포함한 완성작으로 남긴다.
- 변경 단위: `react-native/src/lib/stream.ts`, `react-native/maestro/smoke-login-create.yaml`, `docs/portfolio-presentation.md`, `docs/assets/portfolio/README.md`, `node-server/src/server.integration.test.ts`, `node-server/src/demo/runDemo.ts`, `demo/e2e-summary.json`
- 처음 가설: hiring-facing 프로젝트는 “무엇을 만들었는가”보다 “어떻게 재현하고 설명할 수 있는가”가 더 중요하다.
- 실제 진행: websocket은 `lastEventId`를 붙여 다시 열리고, Maestro smoke flow는 login -> create incident를 자동화하며, portfolio docs는 iPhone simulator 기반의 발표 순서를 문서화한다. Node server demo는 approve/reject/replay 결과를 JSON summary로 남긴다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/node-server
npm run typecheck
npm test
npm run demo-e2e
```

검증 신호:

- server current replay에서 `1`개 test file, `3`개 테스트 통과
- `demo/e2e-summary.json`에 `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`, `replayedEvents: 1`, `auditRecords: 4`
- `maestro/smoke-login-create.yaml`은 `login-user-id-input`, `new-incident-button`, `queue-incident-button`을 차례로 눌러 최소 smoke path를 정의한다.
- 다만 RN `npm run verify`는 현재 `__tests__/app-shell.test.tsx` 실패로 전체 gate가 green이 아니다.

핵심 코드:

```ts
socket.onmessage = event => {
  const parsed = JSON.parse(event.data) as StreamEvent;
  input.onEvent(parsed);
};
```

왜 이 코드가 중요했는가:

이 앱의 realtime은 단순 live update가 아니라, reconnect 이후에도 어떤 event부터 다시 읽어야 하는지를 제품 상태와 함께 유지하는 규칙이기 때문이다.

새로 배운 것:

- 완성작은 코드, smoke flow, 발표 자료, summary artifact가 함께 움직여야 비로소 설득력이 생긴다.

다음:

- 현재 남은 후속 과제는 `app-shell.test.tsx`를 다시 green으로 돌려 RN verify와 portfolio evidence 사이의 간극을 없애는 일이다.

## 여기까지 정리

- 이 프로젝트가 실제로 남긴 것은 incident domain의 화면 구현만이 아니라, bootstrap, offline recovery, replay-safe realtime, 발표 재현성을 한 묶음으로 만든 delivery package다.
- 동시에 현재 상태에서는 RN unit/integration gate가 완전히 green이 아니므로, 완성도와 안정화 사이의 마지막 간극도 분명히 보인다.
