# 02 — Debug Log: Contract Harness 디버깅 기록

## 문제 1: approval이 null인 상태에서의 listAvailableActions

### 상황

`listAvailableActions`는 세 번째 파라미터로 `approval`을 받는다.
그런데 인시던트가 OPEN 상태일 때는 아직 approval 객체가 존재하지 않는다.
`requestResolution`이 호출되어야 비로소 approval이 생성된다.

### 문제

approval이 null이면 `approval.status === 'PENDING'` 비교에서 TypeError가 발생할 수 있다.
함수 안에서 approval에 접근하기 전에 null 체크가 필수다.

### 해결

`listAvailableActions`는 APPROVER 분기에서만 approval에 접근한다.
OPERATOR 분기에서는 incident.status만 확인하고 approval은 무시한다.
APPROVER 분기도 `approval && approval.status === 'PENDING'` 패턴으로 안전하게 처리한다.

이 방어적 접근이 없으면 OPERATOR 로그인 → OPEN 상태에서 함수 호출 시 크래시가 난다.

## 문제 2: 역할 전환 시 상태 초기화 범위

### 상황

UI 테스트에서 Operator가 ack + requestResolution 후 Approver로 전환해야 한다.
역할을 바꿔도 incident, approval, auditLogs 상태는 유지되어야 한다.

### 문제

`loginAs`는 AuthActor만 반환한다.
만약 역할 전환 시 모든 상태를 초기화하면 Approver는 OPEN 인시던트를 보게 된다.
테스트에서 이 부분을 어떻게 제어하는가?

### 해결

테스트는 순차적으로 state를 변수에 저장한다:
```
let incident = initialIncident;
let result = acknowledgeIncident(incident, operator);
incident = result.incident;
result = requestResolution(incident, operator);
incident = result.incident;
let approval = result.approval;
// 여기서 actor만 approver로 교체
result = decideApproval(incident, approval, approver, 'APPROVE');
```

harness 모델이 순수 함수이기 때문에 가능한 패턴이다.
상태가 함수 외부의 변수에 있고, 함수는 새 상태를 반환할 뿐이다.
역할 전환은 actor 변수만 바꾸면 된다.

## 문제 3: replayFrom의 eventId 비교 — 문자열 vs 숫자

### 상황

`streamEvents`의 eventId는 숫자(1, 2, 3, 4)다.
`replayFrom(lastEventId)`도 숫자를 받는다.

### 주의점

TypeScript에서 `>` 비교는 숫자끼리는 안전하지만,
만약 eventId가 문자열이 되면 사전순 비교로 바뀐다.
"10" < "9"가 true인 문제.

### 현재 상태

streamEvents의 eventId 타입이 number로 명시되어 있어 현재는 안전하다.
그러나 실제 서버 구현에서 eventId가 문자열(UUID 등)로 바뀔 경우,
비교 로직을 수정해야 한다.

## 문제 4: UI 테스트의 rerender 타이밍

### 상황

UI 테스트에서 버튼을 `fireEvent.press()`로 누른 뒤
바로 `getByText('status: ACKED')`를 검증한다.

### 문제

React의 상태 업데이트가 비동기인 경우 즉시 반영되지 않을 수 있다.

### 해결

테스트에서 `act()` 래퍼와 `waitFor`를 사용해 렌더 사이클을 보장한다.
harness 모델이 동기 함수이므로 setState → rerender가 즉시 완료되어
일반적으로는 문제가 없지만, Testing Library best practice를 따르는 것이 안전하다.

## 문제 5: contracts 패키지의 file: 프로토콜 경로

### 상황

package.json에서 `"@incident-ops/contracts": "file:../problem/code/contracts"` 의존성이 있다.

### 문제

`npm install` 시 심볼릭 링크가 생성된다.
workspace 경로가 달라지면(다른 머신, CI 환경) 설치가 실패할 수 있다.
또한 contracts 내용을 변경한 후 `npm install`을 다시 하지 않으면 변경이 반영되지 않는 경우가 있다.

### 해결

file: 프로토콜은 로컬 개발용이다.
변경 후에는 `npm install` 재실행 또는 `npm link`를 사용한다.
CI에서는 contracts를 npm registry에 퍼블리시하거나, monorepo 도구(turborepo, nx)를 사용하는 것이 보통이다.
이 프로젝트에서는 학습 목적이므로 file: 프로토콜이 충분하다.
