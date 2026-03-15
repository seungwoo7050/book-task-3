# 02-realtime-chat-react-native 문제지

## 왜 중요한가

offline sync 규칙을 배운 다음에는 그 규칙을 제품형 상호작용 안에 넣어야 한다. 이 프로젝트는 "실시간 채팅이라는 사용자 경험을 유지하면서도 duplicate-safe replay를 설명할 수 있는가"를 묻는다.

## 목표

offline send, ack reconcile, replay from lastEventId, typing/presence update를 하나의 local-first message model로 검증하는 채팅 과제다.

## 시작 위치

- `../study/product-systems/02-realtime-chat/react-native/src/chatModel.ts`
- `../study/product-systems/02-realtime-chat/react-native/src/RealtimeChatStudyApp.tsx`
- `../study/product-systems/02-realtime-chat/react-native/src/storageSchema.ts`
- `../study/product-systems/02-realtime-chat/react-native/.eslintrc.js`
- `../study/product-systems/02-realtime-chat/react-native/tests/realtime-chat.test.ts`
- `../study/product-systems/02-realtime-chat/problem/script/verify_task.sh`
- `../study/product-systems/02-realtime-chat/react-native/app.json`
- `../study/product-systems/02-realtime-chat/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`

## starter code / 입력 계약

- `../study/product-systems/02-realtime-chat/react-native/src/chatModel.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기존 realtime-chat 과제 요구사항
- pending message creation
- server ack reconciliation
- replay dedupe

## 제외 범위

- `../study/product-systems/02-realtime-chat/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `createPendingMessage`와 `reconcileAck`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `realtime chat model`와 `reconciles an ack into a pending message`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/product-systems/02-realtime-chat/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make app-build && make app-test`가 통과한다.

## 검증 방법

```bash
make test && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/02-realtime-chat/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/product-systems/02-realtime-chat/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-realtime-chat-react-native_answer.md`](02-realtime-chat-react-native_answer.md)에서 확인한다.
