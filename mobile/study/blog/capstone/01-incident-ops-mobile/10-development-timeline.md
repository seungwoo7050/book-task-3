# 01 Incident Ops Mobile

최종 앱을 곧바로 만드는 방식으로는 incident domain의 경계를 설명하기 어렵다. 이 프로젝트는 그 반대로 간다. 먼저 shared DTO contract를 canonical source로 고정하고, 그 계약을 React Native harness와 Node server가 같은 방식으로 해석한다는 사실을 작은 화면과 재현 가능한 demo artifact로 증명한다.

## 이번 글에서 따라갈 구현 순서

- shared contract에서 role, status, event vocabulary를 먼저 고정한다.
- RN harness에서 actor/action/replay 규칙을 그대로 눈에 보이게 만든다.
- Node server와 demo artifact로 approve/reject/replay를 end-to-end evidence로 남긴다.

## 새로 이해한 것: 제품 UX보다 먼저 contract correctness를 분리해 증명해야 capstone이 읽힌다

이 프로젝트의 중요한 점은 “React Native 앱을 하나 만들었다”가 아니다. shared contract가 어디 있고, 어떤 상태 전이가 허용되며, replay cursor와 approval rule이 어떤 vocabulary로 움직이는지가 먼저 정리돼야 이후의 제품 완성작도 설명할 수 있다. 그래서 이 글의 중심은 화면의 화려함이 아니라 contract boundary를 어떻게 닫았는가에 있다.

## Phase 1
### canonical shared contract를 먼저 고정한다

- 당시 목표: role, incident status, approval, stream event, queue action을 하나의 canonical source로 모은다.
- 변경 단위: `problem/code/contracts/contracts.ts`
- 처음 가설: contract vocabulary가 흩어져 있으면 RN harness와 server가 같은 시스템을 다룬다는 설명 자체가 성립하지 않는다.
- 실제 진행: `USER_ROLES`, `INCIDENT_STATUSES`, `APPROVAL_DECISIONS`, `STREAM_EVENT_TYPES`, `QueueAction`과 DTO 타입들을 shared contract로 모았다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native
npm run verify
```

검증 신호:

- role, status, event, queue action 문자열이 모두 contract 파일에서 직접 읽힌다.
- 이후 RN harness와 Node server는 같은 status vocabulary를 그대로 소비한다.

핵심 코드:

```ts
export const STREAM_EVENT_TYPES = [
  "incident.created",
  "incident.updated",
  "approval.requested",
  "approval.decided",
] as const;
```

왜 이 코드가 중요했는가:

capstone의 핵심을 “앱 기능”이 아니라 “시스템이 공유하는 언어”로 옮겨 놓는 출발점이기 때문이다.

새로 배운 것:

- shared contract는 나중에 재사용하는 타입 모음이 아니라, 프로젝트 서술 순서를 결정하는 기준점이다.

다음:

- contract를 작은 RN harness에서 바로 읽히게 만든다.

## Phase 2
### RN harness로 상태 전이와 replay를 곧바로 보여 준다

- 당시 목표: 제품형 화면 대신, contract correctness를 가장 짧은 경로로 검증하는 RN surface를 만든다.
- 변경 단위: `react-native/src/harnessModel.ts`, `react-native/src/IncidentOpsHarnessApp.tsx`, `react-native/tests/incident-ops-harness.test.tsx`
- 처음 가설: actor 선택, ack, resolution request, approval, replay cursor만 있으면 contract 해석이 충분히 증명된다.
- 실제 진행: `harnessModel.ts`에 role별 action gate와 approval decision 결과를 함수로 정리하고, `IncidentOpsHarnessApp.tsx`는 actor 선택, incident 상태, approval 상태, audit timeline, replay diagnostics를 한 화면에 배치했다.

CLI:

```bash
npm run verify
```

검증 신호:

- current replay에서 `PASS tests/incident-ops-harness.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 5 passed`
- 테스트는 operator ack, resolution request, approver approve, missed replay event count를 함께 확인한다.

핵심 코드:

```ts
export function replayFrom(lastEventId: number): StreamEvent[] {
  return streamEvents.filter(event => event.eventId > lastEventId);
}
```

왜 이 코드가 중요했는가:

이 harness가 단순 mock 화면이 아니라, contract에서 정의한 event history를 실제 replay cursor 규칙으로 읽는다는 사실을 가장 짧게 보여 주기 때문이다.

새로 배운 것:

- contract harness는 기능 수를 늘리기보다 state transition과 replay rule을 읽기 쉽게 노출하는 쪽이 훨씬 강하다.

다음:

- 같은 vocabulary를 Node server와 demo artifact까지 연결한다.

## Phase 3
### Node server와 demo artifact로 contract를 end-to-end로 잠근다

- 당시 목표: harness가 임의 시뮬레이션이 아니라 실제 approve/reject/replay 흐름과 맞물린다는 evidence를 남긴다.
- 변경 단위: `node-server/src/server.integration.test.ts`, `node-server/src/demo/runDemo.ts`, `demo/e2e-summary.json`
- 처음 가설: contract 프로젝트의 최종 증거는 설명문보다 approve/reject/replay가 재현되는 summary artifact다.
- 실제 진행: integration test는 create -> ack -> request-resolution -> decision -> audit 흐름을 검증했고, demo script는 approve branch, reject branch, websocket replay, audit count를 `demo/e2e-summary.json`으로 기록했다.

CLI:

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/node-server
npm run typecheck
npm test
npm run demo-e2e
```

검증 신호:

- current replay에서 server `1`개 test file, `3`개 테스트 통과
- `demo/e2e-summary.json`에 `ackStatus: ACKED`, `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`
- 같은 artifact에 `initialEvents: 12`, `replayedEvents: 1`, `auditRecords: 4`

핵심 코드:

```ts
expect(actions).toContain("incident.create");
expect(actions).toContain("incident.ack");
expect(actions).toContain("incident.request_resolution");
expect(actions).toContain("approval.decide");
```

왜 이 코드가 중요했는가:

shared contract가 실제 backend audit vocabulary와도 맞물린다는 사실을 가장 직접적으로 남기기 때문이다.

새로 배운 것:

- contract capstone은 “작은 harness + end-to-end artifact” 조합일 때 가장 설명력이 높다.

다음:

- 다음 프로젝트에서는 같은 incident domain 위에 auth, outbox, session restore, hiring-facing presentation까지 얹은 mobile client 완성작으로 이동한다.

## 여기까지 정리

- 이 프로젝트가 실제로 남긴 것은 완성형 제품 UI가 아니라, incident domain을 shared contract와 replay 가능한 evidence로 먼저 닫는 감각이다.
- 다음 단계의 질문: 같은 도메인을 유지한 채, 제품 UX와 offline recovery를 어디까지 추가해야 완성작이 되는가?
