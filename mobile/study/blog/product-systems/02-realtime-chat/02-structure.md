# Structure Plan: 02 Realtime Chat

## 글의 중심 질문

- 이 프로젝트는 채팅 화면을 만드는 것보다, pending/ack/replay/typing이 같은 message lifecycle을 공유하게 만드는 데 더 가깝다.

## 구현 순서 요약

- `chatModel.ts`에서 message identity rule을 먼저 닫는다.
- `storageSchema.ts`와 `RealtimeChatStudyApp.tsx`에서 schema와 UI가 그 모델을 같이 읽게 한다.
- `realtime-chat.test.ts`로 ack/replay/dedupe를 공개 게이트로 만든다.

## 섹션 설계

1. Phase 1: pending, ack, replay, dedupe를 순수 함수로 먼저 정리한다.
변경 단위: `react-native/src/chatModel.ts`
코드 앵커: `reconcileAck()`, `dedupeReplay()`
2. Phase 2: schema summary와 화면이 같은 vocabulary를 쓴다.
변경 단위: `react-native/src/storageSchema.ts`, `react-native/src/RealtimeChatStudyApp.tsx`
코드 앵커: `chatSchemaSummary`
3. Phase 3: message lifecycle을 테스트로 잠근다.
변경 단위: `react-native/tests/realtime-chat.test.ts`
코드 앵커: `applyReplayEvents(...)`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `3`개 테스트 통과
- concept: ack reconcile과 replay dedupe는 같은 identity rule을 공유한다

## 개념 설명 포인트

- 새로 이해한 것: pending message는 임시 UI state가 아니라 sync 대상 record다
- schema와 UI가 같은 vocabulary를 써야 replay-safe 모델이 설명된다

## 마무리 질문

- 다음 프로젝트에서는 이 verified snapshot을 release candidate로 복제해 배포 discipline을 따로 떼어 본다.
