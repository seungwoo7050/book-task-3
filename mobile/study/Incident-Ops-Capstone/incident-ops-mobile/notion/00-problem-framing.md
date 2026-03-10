# 00 — Problem Framing: 인시던트 관리 Contract Harness

## 문제의 출발점

인시던트 관리 시스템은 다수의 역할(Reporter, Operator, Approver)이 
정해진 워크플로우(보고 → 인지 → 해결 요청 → 승인/거부)를 따라 협업하는 시스템이다.
백엔드 서버가 인시던트 상태를 관리하고, 클라이언트는 그 상태를 읽고 허용된 액션을 실행한다.

서버와 클라이언트가 서로 다른 언어·플랫폼에서 동작하므로,
**공유 DTO 계약(contract)**이 양쪽의 유일한 접점이다.
계약이 정확하지 않으면 서버가 보낸 데이터를 클라이언트가 잘못 해석하거나,
클라이언트가 보낸 요청을 서버가 거부한다.

이 프로젝트의 질문은:
**인시던트 관리 시스템의 공유 계약을 TypeScript로 정의하고, 
React Native harness가 그 계약을 올바르게 해석한다는 것을 어떻게 증명할 수 있는가?**

## Contract Harness의 역할

이 프로젝트는 **시스템 경계에서 멈추는** harness다.
UI 완성도, 오프라인 지원, 포트폴리오 패키징은 scope 밖이다.
하네스가 증명하는 것:

1. 공유 계약의 타입이 서버와 클라이언트 양쪽에서 올바르게 import된다
2. 역할별 허용 액션이 계약에 따라 올바르게 결정된다
3. 상태 전이(OPEN → ACKED → RESOLUTION_PENDING → RESOLVED)가 계약에 부합한다
4. Audit log가 모든 액션에 대해 정확하게 생성된다
5. Event stream replay가 lastEventId 기준으로 올바르게 동작한다

## 시스템 아키텍처

```
problem/code/contracts/     ← 공유 DTO 타입 (canonical source)
    ├── contracts.ts         ← Incident, Approval, AuditLog, StreamEvent, etc.
    └── package.json         ← @incident-ops/contracts 패키지

node-server/                 ← Express 백엔드 (계약 구현)

react-native/                ← 모바일 harness (계약 해석)
    ├── src/contracts.ts     ← @incident-ops/contracts re-export
    └── src/harnessModel.ts  ← 순수 함수 기반 워크플로우 모델
```

`@incident-ops/contracts`는 `file:` 프로토콜로 로컬 패키지를 참조한다.
서버와 클라이언트가 같은 TypeScript 타입 정의를 공유한다.

## 인시던트 워크플로우

```
REPORTER: 인시던트 생성
    ↓
OPEN → OPERATOR: ack → ACKED
    ↓
ACKED → OPERATOR: request-resolution → RESOLUTION_PENDING
    ↓
RESOLUTION_PENDING → APPROVER: approve → RESOLVED
                   → APPROVER: reject → ACKED (되돌아감)
```

각 단계에서:
- `listAvailableActions(actor, incident, approval)`이 허용된 액션 목록을 반환
- 액션 실행 시 incident 상태가 갱신되고 audit log가 생성된다
- 승인이 거부되면 ACKED 상태로 롤백되어 Operator가 다시 해결을 요청할 수 있다

## 학습 범위

| 영역 | 구체적 목표 |
|------|-------------|
| 공유 계약 | TypeScript DTO로 서버-클라이언트 경계 고정 |
| 역할 기반 제어 | REPORTER, OPERATOR, APPROVER별 허용 액션 분리 |
| 상태 머신 | 인시던트 4단계 + 승인 3단계 상태 전이 |
| Audit trail | 모든 액션에 대한 감사 로그 생성 |
| Event replay | lastEventId 기준 이벤트 스트림 재생 |
