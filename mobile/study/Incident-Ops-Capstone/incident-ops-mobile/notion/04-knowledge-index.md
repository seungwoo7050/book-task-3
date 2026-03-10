# 04 — Knowledge Index: Contract Harness 기술 색인

## 파일 맵

| 파일 | 역할 | 핵심 |
|------|------|------|
| `react-native/src/contracts.ts` | 계약 re-export | `@incident-ops/contracts`에서 타입 + 상수 re-export |
| `react-native/src/harnessModel.ts` | 워크플로우 모델 | 6개 순수 함수 + 4개 초기 데이터 상수 |
| `react-native/App.tsx` | UI 엔트리 | HarnessApp 렌더링 |
| `react-native/tests/incident-ops-harness.test.tsx` | 테스트 | 3 모델 + 2 UI 테스트 |
| `problem/code/contracts/contracts.ts` | 공유 계약 | 모든 타입, 인터페이스, DTO 정의 |
| `problem/Makefile` | 빌드/테스트 | test, app-build, app-test, server-test, demo-e2e |

## 타입 시스템

### 역할 & 상태

```
UserRole = "REPORTER" | "OPERATOR" | "APPROVER"
IncidentStatus = "OPEN" | "ACKED" | "RESOLUTION_PENDING" | "RESOLVED"
ApprovalStatus = "PENDING" | "APPROVED" | "REJECTED"
ApprovalDecision = "APPROVE" | "REJECT"
```

### 핵심 인터페이스

| 인터페이스 | 주요 필드 |
|-----------|-----------|
| Incident | id, title, severity, status, reportedBy, assigneeId, approvalId |
| Approval | id, incidentId, requestedBy, status, decision, decidedBy, decidedAt |
| AuditLog | id, incidentId, actorId, actorRole, action, result, detail, timestamp |
| StreamEvent | eventId, type, payload, timestamp |
| AuthActor | userId, role |
| QueueJob | id, action, payload, idempotencyKey, attempts, state |

### DTO

| DTO | 방향 | 용도 |
|-----|------|------|
| LoginRequest / LoginResponse | 요청/응답 | role → AuthActor + token |
| CreateIncidentRequest | 요청 | 인시던트 생성 |
| RequestResolutionBody | 요청 | 해결 요청 |
| ApprovalDecisionBody | 요청 | 승인/거절 |

## 상태 머신

```
OPEN ──(ack, OPERATOR)──▶ ACKED
ACKED ──(request-resolution, OPERATOR)──▶ RESOLUTION_PENDING
RESOLUTION_PENDING ──(approve, APPROVER)──▶ RESOLVED
RESOLUTION_PENDING ──(reject, APPROVER)──▶ ACKED  ←── 다시 시도 가능
```

## 함수 레퍼런스

| 함수 | 입력 | 출력 |
|------|------|------|
| `loginAs(role)` | UserRole | AuthActor |
| `listAvailableActions(actor, incident, approval)` | AuthActor, Incident, Approval \| null | string[] |
| `acknowledgeIncident(incident, actor)` | Incident, AuthActor | { incident, auditLog } |
| `requestResolution(incident, actor)` | Incident, AuthActor | { incident, approval, auditLog } |
| `decideApproval(incident, approval, actor, decision)` | Incident, Approval, AuthActor, ApprovalDecision | { incident, approval, auditLog } |
| `replayFrom(lastEventId)` | number | StreamEvent[] |

## 초기 데이터

| 상수 | 값 |
|------|-----|
| `initialIncident` | P1 severity, OPEN, "Database latency spike" |
| `initialApproval` | PENDING, incidentId 연결 |
| `initialAuditLogs` | 인시던트 생성 기록 1건 |
| `streamEvents` | 4건 (created, updated, approval.requested, approval.decided) |

## Makefile 타겟

| 타겟 | 명령 | 용도 |
|------|------|------|
| `test` | app-test | 기본 테스트 |
| `app-build` | cd react-native && npx tsc --noEmit | 타입 체크 |
| `app-test` | cd react-native && npx jest | Jest 테스트 |
| `server-test` | cd node-server && npm test | 서버 테스트 |
| `demo-e2e` | cd demo && node run-e2e.mjs | e2e 데모 |

## 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| react-native | 0.84.1 | 프레임워크 |
| typescript | ^5.8.3 | 타입 시스템 |
| jest | ^29.6.3 | 테스트 러너 |
| @testing-library/react-native | ^12.9.0 | UI 테스트 |
| @incident-ops/contracts | file:../problem/code/contracts | 공유 계약 |

## 연관 프로젝트

- **incident-ops-mobile-client**: 이 harness가 검증한 워크플로우를 실제 API + 오프라인 큐로 구현
- **realtime-chat**: StreamEvent 패턴의 선행 학습 (WebSocket 기반 실시간 통신)
- **offline-sync-foundations**: QueueJob 패턴의 선행 학습 (AsyncStorage 오프라인 큐)
