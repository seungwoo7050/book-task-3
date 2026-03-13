# Structure Plan: 02 Incident Ops Mobile Client

## 글의 중심 질문

- 이 프로젝트의 질문은 같은 incident domain을 hiring-facing RN 완성작으로 다시 쌓을 때 무엇이 새로 필요해지느냐다. 그래서 글은 auth/bootstrap, outbox/recovery, realtime/demo/presentation 순서로 가야 한다.

## 구현 순서 요약

- `AppModel.tsx`와 `RootNavigator.tsx`에서 login, session restore, tab shell을 먼저 닫는다.
- `outbox.ts`와 storage helpers로 offline queue와 optimistic incident list를 제품 흐름에 넣는다.
- `stream.ts`, server demo, Maestro, portfolio docs로 replay와 발표 재현성을 붙인다.

## 섹션 설계

1. Phase 1: auth, session restore, navigation shell을 먼저 닫는다.
변경 단위: `react-native/src/app/AppModel.tsx`, `react-native/src/navigation/RootNavigator.tsx`, `react-native/src/lib/storage.ts`
코드 앵커: bootstrap `Promise.all`, `bootstrapState !== 'ready' ? <LoadingScreen /> : ...`
2. Phase 2: persistent outbox와 optimistic incident list를 제품 surface로 만든다.
변경 단위: `react-native/src/lib/outbox.ts`, `react-native/src/app/AppModel.tsx`
코드 앵커: `markQueuedMutationFailed`, `buildIncidentList`, `flushPendingMutations`
3. Phase 3: realtime replay, server demo, Maestro, portfolio asset를 묶어 완성작으로 설명한다.
변경 단위: `react-native/src/lib/stream.ts`, `react-native/maestro/smoke-login-create.yaml`, `docs/portfolio-presentation.md`, `demo/e2e-summary.json`
코드 앵커: `openIncidentStream`, smoke flow ids, summary artifact values

## 반드시 넣을 근거

- CLI: RN `npm run verify`, server `npm run typecheck`, `npm test`, `npm run demo-e2e`
- verification: RN은 `storage.test.ts`, `outbox.test.ts` 통과하지만 `app-shell.test.tsx` 실패
- failure detail: `login-user-id-input` 미탐색, React Query async update 경고
- server/demo: `1`개 file `3`개 테스트 통과, `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`, `replayedEvents: 1`
- docs: portfolio presentation과 Maestro smoke flow가 재현 경로를 제공함

## 개념 설명 포인트

- 새로 이해한 것: 완성작의 핵심은 화면 수가 아니라 bootstrap, offline recovery, presentation evidence를 하나의 제품 흐름으로 묶는 능력이다.
- 이 프로젝트의 진짜 출력물은 RN client와 server demo, portfolio capture가 함께 움직이는 delivery package다.

## 마무리 질문

- 현재 남은 질문은 제품 완성도를 유지한 채 app-shell integration test를 어떻게 다시 green으로 돌릴 것인가다.
