# 02-incident-ops-mobile-client-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다. 핵심은 `AppModelContext`와 `createId`, `defaultConnectionState` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- capstone/01-incident-ops-mobile의 shared contract
- node-server/ local backend reference
- auth entry와 session restore
- 첫 진입점은 `../study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`이고, 여기서 `AppModelContext`와 `createId` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`: `AppModelContext`, `createId`, `defaultConnectionState`, `getIncidentId`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/components/Ui.tsx`: `ScreenLayout`, `SectionCard`, `ActionButton`, `FieldLabel`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/contracts.ts`: 핵심 구현을 담는 파일이다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/lib/api.ts`: `ApiError`, `normalizeBaseUrl`, `buildWebsocketUrl`, `requestJson`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/lib/connectivity.ts`: `toConnectionState`, `fetchCurrentConnection`, `subscribeToConnectivity`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts`: `USER_ROLES`, `INCIDENT_SEVERITIES`, `INCIDENT_STATUSES`, `APPROVAL_DECISIONS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/app-shell.test.tsx`: `jsonResponse`, `incident ops app shell`, `logs in and opens the incident feed`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/outbox.test.ts`: `outbox helpers`, `moves a job into failed after max attempts`, `applies optimistic state to an incident list`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts`와 `../study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `jsonResponse` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make app-build && make app-test && make server-test && make demo-e2e`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make app-build && make app-test && make server-test && make demo-e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native && npm run verify
```

- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `jsonResponse`와 `incident ops app shell`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make app-build && make app-test && make server-test && make demo-e2e`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/components/Ui.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/contracts.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/lib/api.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/lib/connectivity.ts`
- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/app-shell.test.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/outbox.test.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/storage.test.ts`
- `../study/capstone/02-incident-ops-mobile-client/problem/script/verify_task.sh`
