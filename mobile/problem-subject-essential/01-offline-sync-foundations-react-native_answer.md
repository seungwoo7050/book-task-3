# 01-offline-sync-foundations-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

deterministic fake sync service를 사용해 outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다. 핵심은 `seeded`와 `snapshot`, `OfflineSyncStudyApp` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 새로 설계한 offline-sync foundations 문제 정의
- task create queue
- retry and DLQ
- 첫 진입점은 `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`이고, 여기서 `seeded`와 `snapshot` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`: `seeded`, `snapshot`, `OfflineSyncStudyApp`, `styles`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/01-offline-sync-foundations/react-native/src/syncEngine.ts`: `createTaskDraft`, `FakeSyncServer`, `mergeServerAssignedFields`, `flushQueue`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/01-offline-sync-foundations/react-native/.eslintrc.js`: 핵심 구현을 담는 파일이다.
- `../study/product-systems/01-offline-sync-foundations/react-native/.prettierrc.js`: 핵심 구현을 담는 파일이다.
- `../study/product-systems/01-offline-sync-foundations/react-native/App.tsx`: 핵심 구현을 담는 파일이다.
- `../study/product-systems/01-offline-sync-foundations/react-native/tests/offline-sync.test.ts`: `offline sync engine`, `syncs a pending task and assigns server id`, `moves a repeatedly failing job to dlq`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/product-systems/01-offline-sync-foundations/problem/script/verify_task.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/product-systems/01-offline-sync-foundations/react-native/app.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `offline sync engine` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make app-build && make app-test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `offline sync engine`와 `syncs a pending task and assigns server id`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make app-build && make app-test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`
- `../study/product-systems/01-offline-sync-foundations/react-native/src/syncEngine.ts`
- `../study/product-systems/01-offline-sync-foundations/react-native/.eslintrc.js`
- `../study/product-systems/01-offline-sync-foundations/react-native/.prettierrc.js`
- `../study/product-systems/01-offline-sync-foundations/react-native/App.tsx`
- `../study/product-systems/01-offline-sync-foundations/react-native/tests/offline-sync.test.ts`
- `../study/product-systems/01-offline-sync-foundations/problem/script/verify_task.sh`
- `../study/product-systems/01-offline-sync-foundations/react-native/app.json`
- `../study/product-systems/01-offline-sync-foundations/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`
- `../study/product-systems/01-offline-sync-foundations/react-native/ios/IncidentOpsMobileClient/Images.xcassets/Contents.json`
