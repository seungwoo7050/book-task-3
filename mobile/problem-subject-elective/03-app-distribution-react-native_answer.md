# 03-app-distribution-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

검증된 realtime-chat snapshot을 release candidate로 가져와, 실제 credential을 저장소에 넣지 않고도 packaging, env separation, automation rehearsal을 증명하는 과제다. 핵심은 `createPendingMessage`와 `reconcileAck`, `applyReplayEvents` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- realtime-chat verified snapshot
- release candidate 복제
- development, staging, production 환경 분리
- 첫 진입점은 `../study/product-systems/03-app-distribution/react-native/src/chatModel.ts`이고, 여기서 `createPendingMessage`와 `reconcileAck` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/product-systems/03-app-distribution/react-native/src/chatModel.ts`: `createPendingMessage`, `reconcileAck`, `applyReplayEvents`, `dedupeReplay`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/03-app-distribution/react-native/src/RealtimeChatStudyApp.tsx`: `messages`, `typingState`, `schemaLabel`, `RealtimeChatStudyApp`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/03-app-distribution/react-native/src/releasePlan.ts`: `releaseTargets`, `summarizeReleaseTargets`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/03-app-distribution/react-native/src/storageSchema.ts`: `chatSchema`, `chatSchemaSummary`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/product-systems/03-app-distribution/react-native/.eslintrc.js`: 핵심 구현을 담는 파일이다.
- `../study/product-systems/03-app-distribution/react-native/tests/realtime-chat.test.ts`: `realtime chat model`, `reconciles an ack into a pending message`, `filters replay events by lastEventId`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/product-systems/03-app-distribution/react-native/tests/release-plan.test.ts`: `release plan`, `defines the three release channels`, `builds stable rehearsal summary strings`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/product-systems/03-app-distribution/problem/script/verify_task.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.

## 정답을 재구성하는 절차

1. `../study/product-systems/03-app-distribution/react-native/src/chatModel.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `realtime chat model` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make app-build && make app-test && make release-rehearsal`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make app-build && make app-test && make release-rehearsal
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/03-app-distribution/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/03-app-distribution/react-native && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `realtime chat model`와 `reconciles an ack into a pending message`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make app-build && make app-test && make release-rehearsal`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/product-systems/03-app-distribution/react-native/src/chatModel.ts`
- `../study/product-systems/03-app-distribution/react-native/src/RealtimeChatStudyApp.tsx`
- `../study/product-systems/03-app-distribution/react-native/src/releasePlan.ts`
- `../study/product-systems/03-app-distribution/react-native/src/storageSchema.ts`
- `../study/product-systems/03-app-distribution/react-native/.eslintrc.js`
- `../study/product-systems/03-app-distribution/react-native/tests/realtime-chat.test.ts`
- `../study/product-systems/03-app-distribution/react-native/tests/release-plan.test.ts`
- `../study/product-systems/03-app-distribution/problem/script/verify_task.sh`
- `../study/product-systems/03-app-distribution/react-native/app.json`
- `../study/product-systems/03-app-distribution/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`
