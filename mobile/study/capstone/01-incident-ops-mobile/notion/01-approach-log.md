# 01 — Approach Log: Contract Harness 구현 과정

## Phase 1: 공유 계약 정의 — @incident-ops/contracts

모든 것의 시작은 `problem/code/contracts/contracts.ts`다.
이 파일이 서버와 클라이언트의 유일한 공유 지점이다.

### 상수와 타입

```typescript
const USER_ROLES = ["REPORTER", "OPERATOR", "APPROVER"] as const;
type UserRole = (typeof USER_ROLES)[number];

const INCIDENT_STATUSES = ["OPEN", "ACKED", "RESOLUTION_PENDING", "RESOLVED"] as const;
type IncidentStatus = (typeof INCIDENT_STATUSES)[number];

const APPROVAL_DECISIONS = ["APPROVE", "REJECT"] as const;
type ApprovalDecision = (typeof APPROVAL_DECISIONS)[number];
```

`as const`와 indexed access type으로 상수 배열에서 union type을 추출한다.
이 패턴은 런타임 검증(배열에 포함 여부)과 컴파일 타임 타입 체크를 동시에 하는 standard 기법이다.

### 핵심 인터페이스

- **Incident**: id, title, severity, status, approvalId 등. status가 상태 머신의 현재 위치.
- **Approval**: incidentId와 연결. status는 PENDING → APPROVED/REJECTED. decision, decidedBy, decidedAt은 결정 전에는 null.
- **AuditLog**: 모든 액션에 대한 감사 기록. actorId, actorRole, action, result, detail.
- **StreamEvent**: eventId 기반 순서 보장. type은 incident.created, incident.updated, approval.requested, approval.decided.
- **QueueJob**: action(REST endpoint), idempotencyKey, attempts, state(pending/synced/failed) — 오프라인 큐용.

### 요청/응답 DTO

LoginRequest/Response, CreateIncidentRequest, RequestResolutionBody, ApprovalDecisionBody 등
REST API의 입력/출력 shape이 타입으로 고정되어 있다.

## Phase 2: Harness Model — harnessModel.ts

`harnessModel.ts`는 순수 함수 기반의 워크플로우 모델이다.
React state에 의존하지 않으므로 단위 테스트로 완전히 검증 가능하다.

### 초기 데이터

`initialIncident`는 P1 severity의 OPEN 인시던트다.
"Database latency spike — Checkout queries exceed SLO for 10 minutes"이라는 시나리오.
`initialApproval`은 PENDING 상태의 승인 객체.
`initialAuditLogs`는 인시던트 생성 로그 하나.

### loginAs(role)

역할을 선택해 AuthActor를 생성한다.
`loginAs('OPERATOR')` → `{ userId: 'operator.demo', role: 'OPERATOR' }`.
userId는 `${role.toLowerCase()}.demo` 패턴으로 결정적이다.

### listAvailableActions(actor, incident, approval)

역할과 현재 상태에 따라 허용된 액션 목록을 반환한다:
- OPERATOR + OPEN → ['ack']
- OPERATOR + ACKED → ['request-resolution']
- APPROVER + approval.PENDING → ['approve', 'reject']
- 그 외 → [] (빈 배열)

이 함수가 RBAC(Role-Based Access Control)의 핵심이다.
허용되지 않은 조합에서는 빈 배열이 반환되어 UI에서 버튼이 보이지 않게 된다.

### acknowledgeIncident(incident, actor)

OPEN 인시던트를 ACKED로 전이한다.
반환: 갱신된 incident + 새 auditLog.

### requestResolution(incident, actor)

ACKED 인시던트를 RESOLUTION_PENDING으로 전이하고, 새 Approval 객체를 생성한다.
반환: 갱신된 incident + 새 approval + 새 auditLog.

### decideApproval(incident, approval, actor, decision)

APPROVE면 RESOLVED, REJECT면 ACKED로 전이한다.
REJECT 시 ACKED로 돌아가는 것은 "Operator가 다시 해결을 시도할 수 있다"는 의미다.
반환: 갱신된 incident + 갱신된 approval + 새 auditLog.

### replayFrom(lastEventId)

`streamEvents` 배열에서 `eventId > lastEventId`인 이벤트만 필터링해 반환한다.
WebSocket 재연결 시 놓친 이벤트를 복구하는 패턴의 시뮬레이션이다.

## Phase 3: 테스트 구조

`incident-ops-harness.test.tsx`는 두 그룹의 테스트를 가진다:

### Model 테스트 (3개)

1. **Ack 검증**: OPEN 인시던트를 OPERATOR가 ack하면 ACKED가 되는지
2. **Request → Approve 검증**: ACKED → requestResolution → decideApproval(APPROVE) → RESOLVED
3. **Replay 검증**: `replayFrom(2)`가 eventId 3, 4만 반환하는지

### App UI 테스트 (2개)

4. **Operator flow**: role 선택 → ack 버튼 → "status: ACKED" 표시 → request-resolution → "RESOLUTION_PENDING"
5. **Full workflow**: Operator가 ack → request-resolution → Approver로 전환 → approve → "RESOLVED" + "APPROVED" 표시

UI 테스트가 `testID` 기반이다.
`role-button-OPERATOR`, `ack-button`, `request-resolution-button`, `approve-button` 등
명확한 testID로 버튼을 선택해 전체 워크플로우를 시뮬레이션한다.
