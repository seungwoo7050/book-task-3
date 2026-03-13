# Evidence Ledger: 02 Incident Ops Mobile Client

## 독립 프로젝트 판정

- 판정: 처리
- 근거: auth, feed, role action, persistent outbox, replay-safe realtime, portfolio demo 자료를 자기 폴더 안에서 독립적으로 갖춘 hiring-facing React Native 프로젝트다.
- 소스 경로: `mobile/study/capstone/02-incident-ops-mobile-client`

## 사용한 근거

- `mobile/study/capstone/02-incident-ops-mobile-client/README.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/problem/README.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/README.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/node-server/README.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/docs/portfolio-presentation.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/docs/assets/portfolio/README.md`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/src/navigation/RootNavigator.tsx`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/src/lib/outbox.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/src/lib/storage.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/src/lib/stream.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/__tests__/app-shell.test.tsx`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/__tests__/outbox.test.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/__tests__/storage.test.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/react-native/maestro/smoke-login-create.yaml`
- `mobile/study/capstone/02-incident-ops-mobile-client/node-server/src/server.integration.test.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/node-server/src/demo/runDemo.ts`
- `mobile/study/capstone/02-incident-ops-mobile-client/demo/e2e-summary.json`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native
npm install --no-audit --no-fund
npm run verify

cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/node-server
npm install --no-audit --no-fund
npm run typecheck
npm test
npm run demo-e2e
```

## Chronology Ledger

### Phase 1 | auth, session restore, navigation shell을 먼저 닫는다

- 당시 목표: contract harness를 제품 앱으로 올리기 전에 login, bootstrap, tab/navigation shell을 안정적으로 만든다.
- 변경 단위: `react-native/src/app/AppModel.tsx`, `react-native/src/navigation/RootNavigator.tsx`, `react-native/src/lib/storage.ts`
- 처음 가설: auth entry와 persisted session이 흔들리면 이후 outbox와 realtime을 붙여도 제품 흐름이 성립하지 않는다.
- 실제 조치: bootstrap 단계에서 settings/session/outbox/lastEventId를 `Promise.all`로 읽고, `RootNavigator`가 `LoadingScreen`, `AuthStack`, `MainTabs`를 session 상태로 갈라서 렌더링하게 했다.
- CLI:
```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native
npm run verify
```
- 검증 신호:
- current replay에서 `PASS __tests__/storage.test.ts`
- `__tests__/app-shell.test.tsx`는 현재 실패한다.
- 실패 내용은 React Query async update 경고와 함께 `Unable to find an element with testID: login-user-id-input`이다.
- 핵심 코드 앵커:
```ts
const [savedSettings, savedSession, savedOutbox, savedLastEventId] =
  await Promise.all([
    loadSettings(appStorage),
    loadSession(appStorage),
    loadOutbox(appStorage),
    loadLastEventId(appStorage),
  ]);
```
- 새로 배운 것: 제품형 RN 앱에서는 bootstrap lifecycle 자체가 별도 검증 단위가 된다.
- 다음: persistent outbox와 optimistic incident list를 붙인다.

### Phase 2 | persistent outbox와 optimistic list를 제품 흐름 안으로 넣는다

- 당시 목표: offline mutation이 사라지지 않고 feed와 outbox 화면에 동시에 반영되게 만든다.
- 변경 단위: `react-native/src/lib/outbox.ts`, `react-native/src/app/AppModel.tsx`, `react-native/src/lib/storage.ts`
- 처음 가설: hiring-facing 완성작은 단순 create form보다 실패 후 복구를 설명할 수 있어야 한다.
- 실제 조치: `createQueuedMutation`, `markQueuedMutationFailed`, `retryQueuedMutation`, `buildIncidentList`로 pending/synced/failed 상태를 관리하고, `AppModel.tsx`는 flush 성공 시 query invalidation을, 실패 시 attempt 누적과 failed 전이를 기록하게 했다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS __tests__/outbox.test.ts`
- failed mutation은 3회 시도 후 `failed`로 이동한다.
- optimistic create item은 `local-` id와 `queued` sync state로 feed 맨 앞에 합쳐진다.
- 핵심 코드 앵커:
```ts
return {
  ...item,
  attempts,
  state: attempts >= MAX_OUTBOX_ATTEMPTS ? 'failed' : 'pending',
  lastError,
};
```
- 새로 배운 것: outbox는 숨겨진 내부 큐가 아니라 feed와 같은 수준의 제품 surface여야 복구 경험을 설명할 수 있다.
- 다음: realtime replay, server demo, portfolio capture를 evidence로 붙인다.

### Phase 3 | realtime replay와 portfolio demo를 붙이되 현재 RN verify 불일치를 남긴다

- 당시 목표: 제품 앱이 role workflow와 recovery를 실제 발표 자료와 재현 가능한 demo로 설명되게 만든다.
- 변경 단위: `react-native/src/lib/stream.ts`, `react-native/maestro/smoke-login-create.yaml`, `docs/portfolio-presentation.md`, `node-server/src/server.integration.test.ts`, `node-server/src/demo/runDemo.ts`, `demo/e2e-summary.json`
- 처음 가설: 최종 프로젝트는 코드만으로 끝나지 않고, 흐름 재현과 발표 자료가 함께 있어야 hiring-facing 산출물로 읽힌다.
- 실제 조치: websocket stream은 `lastEventId` 기반으로 다시 열리고, Maestro smoke flow는 login -> create incident를 자동화하며, server demo는 approve/reject/replay 결과를 summary artifact로 남긴다.
- CLI:
```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/node-server
npm run typecheck
npm test
npm run demo-e2e
```
- 검증 신호:
- server current replay에서 `1`개 test file, `3`개 테스트 통과
- `demo/e2e-summary.json`에는 `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`, `replayedEvents: 1`, `auditRecords: 4`
- `maestro/smoke-login-create.yaml`은 `login-user-id-input`과 `queue-incident-button`을 직접 눌러 smoke flow를 정의한다.
- 다만 RN `npm run verify`는 현재 `__tests__/app-shell.test.tsx` 실패로 전체 green이 아니다.
- 핵심 코드 앵커:
```ts
const disconnect = openIncidentStream({
  baseUrl: settings.baseUrl,
  lastEventId: lastEventIdRef.current,
  onEvent: event => {
    lastEventIdRef.current = Math.max(lastEventIdRef.current, event.eventId);
    setLastEventId(current => Math.max(current, event.eventId));
  },
});
```
- 새로 배운 것: hiring-facing 완성작은 presentation asset과 smoke flow가 강한 근거가 되지만, test gate 불일치는 그대로 기록해야 신뢰가 생긴다.
- 다음: 이 프로젝트는 현재 delivery용 글까지 마무리하되, RN app-shell test 수리가 후속 안정화 항목으로 남는다.
