# Evidence Ledger: 01 Incident Ops Mobile

## 독립 프로젝트 판정

- 판정: 처리
- 근거: shared contract, React Native harness, Node server, demo artifact를 한 폴더 안에서 독립적으로 재현할 수 있는 capstone이다.
- 소스 경로: `mobile/study/capstone/01-incident-ops-mobile`

## 사용한 근거

- `mobile/study/capstone/01-incident-ops-mobile/README.md`
- `mobile/study/capstone/01-incident-ops-mobile/problem/README.md`
- `mobile/study/capstone/01-incident-ops-mobile/react-native/README.md`
- `mobile/study/capstone/01-incident-ops-mobile/node-server/README.md`
- `mobile/study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`
- `mobile/study/capstone/01-incident-ops-mobile/react-native/src/harnessModel.ts`
- `mobile/study/capstone/01-incident-ops-mobile/react-native/src/IncidentOpsHarnessApp.tsx`
- `mobile/study/capstone/01-incident-ops-mobile/react-native/tests/incident-ops-harness.test.tsx`
- `mobile/study/capstone/01-incident-ops-mobile/node-server/src/server.integration.test.ts`
- `mobile/study/capstone/01-incident-ops-mobile/node-server/src/demo/runDemo.ts`
- `mobile/study/capstone/01-incident-ops-mobile/demo/e2e-summary.json`

## CLI Replay

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native
npm install --no-audit --no-fund
npm run verify

cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/node-server
npm install --no-audit --no-fund
npm run typecheck
npm test
npm run demo-e2e
```

## Chronology Ledger

### Phase 1 | canonical shared contract를 먼저 고정한다

- 당시 목표: polished UI보다 먼저 role, incident status, approval, stream event vocabulary를 한 군데에 모은다.
- 변경 단위: `problem/code/contracts/contracts.ts`
- 처음 가설: capstone을 바로 제품 앱으로 설명하면 contract boundary가 흐려지고, RN과 server가 같은 모델을 보는지 확인하기 어려워진다.
- 실제 조치: `USER_ROLES`, `INCIDENT_STATUSES`, `STREAM_EVENT_TYPES`, `QueueAction`, DTO 타입들을 shared contract로 고정했다.
- CLI:
```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native
npm run verify
```
- 검증 신호:
- contract file 안에서 role, status, queue action 문자열이 모두 명시적으로 드러난다.
- RN harness와 Node demo는 이 타입 집합을 기준으로 같은 incident lifecycle을 해석한다.
- 핵심 코드 앵커:
```ts
export const INCIDENT_STATUSES = [
  "OPEN",
  "ACKED",
  "RESOLUTION_PENDING",
  "RESOLVED",
] as const;
```
- 새로 배운 것: capstone의 첫 출력물은 화면이 아니라 shared vocabulary다.
- 다음: 작은 RN harness에서 이 vocabulary가 실제 상태 전이로 보이게 만든다.

### Phase 2 | RN harness로 상태 전이와 replay를 눈에 보이게 만든다

- 당시 목표: contract correctness를 작은 화면 안에서 곧바로 확인한다.
- 변경 단위: `react-native/src/harnessModel.ts`, `react-native/src/IncidentOpsHarnessApp.tsx`, `react-native/tests/incident-ops-harness.test.tsx`
- 처음 가설: 제품 UI를 다 만들지 않아도 actor 전환, ack, resolution request, approval, replay cursor만 있으면 contract 해석이 충분히 검증된다.
- 실제 조치: `harnessModel.ts`에 role별 action gate와 approval decision 규칙을 넣고, `IncidentOpsHarnessApp.tsx`는 actor 선택, incident 상태, approval 상태, audit timeline, replay diagnostics를 한 화면에 모았다.
- CLI:
```bash
npm run verify
```
- 검증 신호:
- current replay에서 `PASS tests/incident-ops-harness.test.tsx`
- `Test Suites: 1 passed`
- `Tests: 5 passed`
- 테스트는 operator ack, resolution request, approver approve, replay miss count를 함께 확인한다.
- 핵심 코드 앵커:
```ts
if (actor.role === 'OPERATOR' && incident.status === 'OPEN') {
  return ['ack'];
}

if (actor.role === 'APPROVER' && approval?.status === 'PENDING') {
  return ['approve', 'reject'];
}
```
- 새로 배운 것: contract harness는 예쁜 화면보다 state transition을 읽기 쉽게 드러내는 편이 훨씬 강한 증거가 된다.
- 다음: 같은 contract를 소비하는 Node server와 demo artifact를 연결한다.

### Phase 3 | Node server와 demo artifact로 contract를 end-to-end로 잠근다

- 당시 목표: RN harness가 임의 모델이 아니라 server와 같은 incident workflow를 읽는다는 사실을 남긴다.
- 변경 단위: `node-server/src/server.integration.test.ts`, `node-server/src/demo/runDemo.ts`, `demo/e2e-summary.json`
- 처음 가설: contract 프로젝트의 최종 증거는 README 설명보다 approve/reject/replay가 모두 재현되는 e2e artifact다.
- 실제 조치: integration test가 create -> ack -> request-resolution -> approval decision -> audit 흐름을 검증하고, demo script는 replay와 audit 숫자를 `demo/e2e-summary.json`으로 기록하게 했다.
- CLI:
```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/node-server
npm run typecheck
npm test
npm run demo-e2e
```
- 검증 신호:
- current replay에서 server `1`개 test file, `3`개 테스트 통과
- `demo/e2e-summary.json`에는 `ackStatus: ACKED`, `approvedStatus: RESOLVED`, `rejectedStatus: ACKED`가 기록된다.
- 같은 summary는 `initialEvents: 12`, `replayedEvents: 1`, `auditRecords: 4`를 남긴다.
- 핵심 코드 앵커:
```ts
expect(decided.incident.status).toBe("RESOLVED");
expect(decided.approval.status).toBe("APPROVED");
```
- 새로 배운 것: contract capstone은 앱 완성도보다 approve/reject/replay를 재생 가능한 artifact로 남길 때 가장 선명해진다.
- 다음: 같은 incident domain을 제품 완성작으로 다시 구현한 mobile client 프로젝트로 넘어간다.
