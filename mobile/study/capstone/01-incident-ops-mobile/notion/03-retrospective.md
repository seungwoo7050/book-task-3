# 03 — Retrospective: Contract Harness 회고

## 설계 판단 — Contract-First Development

이 프로젝트에서 가장 핵심적인 판단은 **서버를 구현하기 전에 계약을 먼저 확정**한 것이다.

`contracts.ts`에 모든 인터페이스와 DTO를 정의하고,
클라이언트(react-native)와 서버(node-server)가 모두 이 파일을 의존하게 만들었다.
이 접근의 장점은 세 가지다:

### 1. 서버 없이 전체 워크플로우 검증 가능

harnessModel.ts가 순수 함수로 전체 인시던트 생명주기를 시뮬레이션한다.
서버 API를 호출하지 않아도 OPEN → ACKED → RESOLUTION_PENDING → RESOLVED 전이를 테스트할 수 있다.
이것이 "harness"라는 이름의 의미다 — 실제 엔진 없이 동작을 묶어서 검증하는 테스트 하네스.

### 2. 역할 기반 접근 제어의 명시적 모델링

`listAvailableActions` 함수가 RBAC 로직을 한 곳에 집중시켰다.
"이 역할이 이 상태에서 무엇을 할 수 있는가"라는 질문에 코드로 답한다.
이 함수만 보면 전체 권한 매트릭스를 이해할 수 있다.

### 3. 타입 안전성의 전파

`as const` + indexed access type 패턴으로 상수와 타입이 동기화된다.
`USER_ROLES` 배열에 새 역할을 추가하면 `UserRole` 타입이 자동으로 확장된다.
contracts를 import하는 모든 코드에서 타입 체크가 동작한다.

## 아키텍처 선택 — 왜 순수 함수인가

harnessModel.ts의 모든 함수가 side-effect가 없다.
상태를 변이(mutate)하지 않고, spread operator로 새 객체를 반환한다.

```typescript
return {
  incident: { ...incident, status: 'ACKED' },
  auditLog: { /* 새 기록 */ }
};
```

이 선택의 이점:
- **테스트 용이**: 입력을 넣으면 출력이 결정적이다. mock이 필요 없다.
- **합성 가능**: 함수 결과를 다음 함수의 입력으로 체이닝한다.
- **디버깅 투명**: 각 단계의 스냅샷을 변수에 저장할 수 있다.

## 범위 결정 — 무엇을 하지 않았는가

이 프로젝트는 의도적으로 다음을 제외했다:

| 제외 항목 | 이유 |
|-----------|------|
| 실제 REST API 호출 | harness는 API 없이 동작을 검증하는 것이 목적 |
| AsyncStorage 저장 | 오프라인 동기화는 incident-ops-mobile-client의 영역 |
| WebSocket 연결 | replayFrom은 재연결 패턴의 "모델"만 구현 |
| 에러 핸들링 | Happy path의 워크플로우 검증에 집중 |

이 범위 결정이 프로젝트를 명확하게 만들었다.
"contract harness가 무엇을 검증하는가"에 정확히 답할 수 있다.

## 테스트 전략 — 모델 + UI 이중 검증

테스트가 두 레이어로 나뉜다:

**모델 테스트**는 함수의 입출력만 검증한다.
서버 mock도, 렌더링도 필요 없다. 가장 빠르고 안정적인 테스트.

**UI 테스트**는 사용자 관점에서 전체 플로우를 검증한다.
role 선택 → 버튼 클릭 → 상태 변경 텍스트 확인.
Testing Library의 `render` + `fireEvent` + `getByText` 패턴.

이 이중 구조가 좋은 이유는,
모델 테스트가 로직 정확성을 보장하고
UI 테스트가 "사용자가 실제로 이 플로우를 경험할 수 있는가"를 보장한다.

## 배운 것

### 1. file: 프로토콜의 효용

npm의 `file:` 의존성으로 monorepo 없이도 패키지 공유가 가능하다.
작은 프로젝트에서 turborepo/nx를 세팅하는 오버헤드 없이 코드 공유를 달성했다.

### 2. 상태 머신 + RBAC의 조합

상태 머신 전이와 역할 기반 권한을 하나의 함수(`listAvailableActions`)에 담으면
전체 시스템의 행동 명세가 코드로 표현된다.
이것이 "실행 가능한 사양(executable specification)"이다.

### 3. Harness 패턴의 가치

실제 인프라 없이 도메인 로직의 설계를 반복할 수 있다.
"서버 먼저 만들고, 클라이언트는 나중에"가 아니라
"계약 먼저, 검증 먼저, 구현은 나중에"가 가능하다.

## 다음 단계와의 연결

이 contract harness가 incident-ops-mobile-client의 기반이 된다.
harness에서 검증한 워크플로우를 실제 서버 API로 구현하고,
클라이언트에서 react-hook-form, @tanstack/react-query, AsyncStorage outbox로 현실화한다.
harness는 "설계 청사진", client는 "실제 건물"이다.
