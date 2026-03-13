# Structure Plan: 01 Incident Ops Mobile

## 글의 중심 질문

- 이 프로젝트의 질문은 제품 UX를 만들기 전에 shared contract correctness를 어디까지 독립적으로 증명할 수 있느냐다. 그래서 글도 UI polish가 아니라 contract, harness, server artifact 순서로 가야 한다.

## 구현 순서 요약

- `contracts.ts`에서 role, status, event, queue action vocabulary를 먼저 고정한다.
- `harnessModel.ts`와 `IncidentOpsHarnessApp.tsx`로 actor/action/replay 규칙을 작은 RN surface에 드러낸다.
- `server.integration.test.ts`와 `demo/e2e-summary.json`으로 approve/reject/replay를 end-to-end evidence로 남긴다.

## 섹션 설계

1. Phase 1: canonical shared contract를 먼저 고정한다.
변경 단위: `problem/code/contracts/contracts.ts`
코드 앵커: `INCIDENT_STATUSES`, `STREAM_EVENT_TYPES`, `QueueAction`
2. Phase 2: RN harness가 role-based action과 replay cursor를 그대로 읽게 만든다.
변경 단위: `react-native/src/harnessModel.ts`, `react-native/src/IncidentOpsHarnessApp.tsx`
코드 앵커: `listAvailableActions`, `replayFrom`
3. Phase 3: Node server와 demo artifact로 contract를 end-to-end로 잠근다.
변경 단위: `node-server/src/server.integration.test.ts`, `node-server/src/demo/runDemo.ts`, `demo/e2e-summary.json`
코드 앵커: approval flow assertions, replay summary values

## 반드시 넣을 근거

- CLI: RN `npm run verify`, server `npm run typecheck`, `npm test`, `npm run demo-e2e`
- verification: RN `1`개 suite `5`개 테스트 통과, server `1`개 file `3`개 테스트 통과
- artifact: `ackStatus: ACKED`, `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`, `replayedEvents: 1`, `auditRecords: 4`

## 개념 설명 포인트

- 새로 이해한 것: capstone을 제품 화면과 분리해 contract artifact로 먼저 설명하면 도메인 경계가 훨씬 또렷해진다.
- 이 프로젝트의 진짜 출력물은 polished UX가 아니라 shared vocabulary와 replay 가능한 approve/reject evidence다.

## 마무리 질문

- 다음 단계에서는 같은 incident domain을 hiring-facing RN client 완성작으로 다시 쌓을 때 무엇이 추가로 필요해지는가를 다룬다.
