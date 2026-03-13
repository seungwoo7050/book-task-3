# Structure Plan: 01 Offline Sync Foundations

## 글의 중심 질문

- 이 프로젝트는 채팅 앱 전에 outbox, retry, DLQ, idempotency만 따로 떼어 다루기 위한 브리지 문제다. 그래서 구현도 task/job 동시 생성 -> flush 규칙 -> RN summary 순으로 흐른다.

## 구현 순서 요약

- `createTaskDraft()`로 local task와 queue job을 동시에 만든다.
- `flushQueue()`에서 retry, DLQ, merge 규칙을 닫는다.
- RN app과 tests가 같은 queue vocabulary를 쓰게 만든다.

## 섹션 설계

1. Phase 1: task와 queue job을 같은 생성 지점에서 만든다.
변경 단위: `react-native/src/syncEngine.ts#createTaskDraft`
코드 앵커: `task` + `job` 동시 생성
2. Phase 2: retry/DLQ/merge를 `flushQueue()`에 모은다.
변경 단위: `react-native/src/syncEngine.ts#flushQueue`
코드 앵커: `job.state = ... ? 'dlq' : 'failed'`
3. Phase 3: RN summary와 unit tests가 같은 queue vocabulary를 쓴다.
변경 단위: `react-native/src/OfflineSyncStudyApp.tsx`, `react-native/tests/offline-sync.test.ts`
코드 앵커: `outboxCount`, `dlqCount`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `4`개 테스트 통과
- concept: outbox는 optimistic UI가 아니라 재전송 가능한 mutation log다

## 개념 설명 포인트

- 새로 이해한 것: retry와 DLQ를 분리해야 실패를 숨기지 않고 상태로 다룰 수 있다
- 이 프로젝트의 핵심은 UI가 아니라 queue vocabulary를 먼저 고정하는 데 있다

## 마무리 질문

- 다음 프로젝트에서는 이 vocabulary를 채팅 UX 안으로 밀어 넣어도 같은 설명이 유지되는지 본다.
