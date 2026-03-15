# 01-offline-sync-foundations-react-native 문제지

## 왜 중요한가

local-first 제품 과제를 바로 풀기 전에 sync 규칙만 독립 변수로 다루기 위해 만든 브리지 문제다. 이 과제의 목적은 채팅 앱이나 캡스톤에서 반복될 queue/retry 패턴을 먼저 몸에 익히는 것이다.

## 목표

deterministic fake sync service를 사용해 outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다.

## 시작 위치

- `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`
- `../study/product-systems/01-offline-sync-foundations/react-native/src/syncEngine.ts`
- `../study/product-systems/01-offline-sync-foundations/react-native/.eslintrc.js`
- `../study/product-systems/01-offline-sync-foundations/react-native/.prettierrc.js`
- `../study/product-systems/01-offline-sync-foundations/react-native/tests/offline-sync.test.ts`
- `../study/product-systems/01-offline-sync-foundations/problem/script/verify_task.sh`
- `../study/product-systems/01-offline-sync-foundations/react-native/app.json`
- `../study/product-systems/01-offline-sync-foundations/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`

## starter code / 입력 계약

- `../study/product-systems/01-offline-sync-foundations/react-native/src/OfflineSyncStudyApp.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 새로 설계한 offline-sync foundations 문제 정의
- task create queue
- retry and DLQ
- idempotency key handling

## 제외 범위

- `../study/product-systems/01-offline-sync-foundations/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `seeded`와 `snapshot`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `offline sync engine`와 `syncs a pending task and assigns server id`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/product-systems/01-offline-sync-foundations/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make app-build && make app-test`가 통과한다.

## 검증 방법

```bash
make test && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/01-offline-sync-foundations/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-offline-sync-foundations-react-native_answer.md`](01-offline-sync-foundations-react-native_answer.md)에서 확인한다.
