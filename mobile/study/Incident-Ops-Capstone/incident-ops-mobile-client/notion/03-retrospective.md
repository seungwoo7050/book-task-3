# 03 — Retrospective: Incident Ops Mobile Client 회고

## 설계 핵심 — Outbox-First Architecture

이 앱의 가장 중요한 아키텍처 결정은 **모든 mutation을 outbox를 통해 처리**한 것이다.

사용자가 액션을 누르면 직접 API를 호출하지 않는다.
먼저 outbox에 `QueuedMutation`을 생성하고, 별도의 flush 프로세스가 실행한다.

이 결정의 즉각적인 이점:
- **오프라인 지원**: 네트워크 없이도 액션이 즉시 반영된다(낙관적 UI).
- **재시도 자동화**: 실패한 mutation은 pending으로 남아 재연결 시 자동 재시도.
- **감사 추적**: 모든 의도된 액션이 outbox에 기록되어 "사용자가 무엇을 시도했는가"를 추적 가능.
- **시연 용이**: SettingsScreen에서 base URL을 잘못 바꾸면 장애를 즉시 재현. 복구 후 flush하면 복원. 이것이 포트폴리오 데모의 핵심 장면이다.

### DLQ 패턴

`MAX_OUTBOX_ATTEMPTS`(3) 초과 시 `failed` 상태로 전환한다.
이것은 실질적으로 Dead Letter Queue다.
사용자가 OutboxScreen에서 수동으로 retry할 수 있고,
이 UI가 "앱이 장애를 숨기지 않고 드러낸다"는 메시지를 전달한다.

## 설계 판단 — AppModel의 Context 중앙화

모든 상태(session, settings, outbox, connection, streamStatus, lastEventId)와
모든 액션(login, logout, queue*, retry, flush)이 하나의 Context에 있다.

### 왜 Redux/Zustand를 쓰지 않았는가

상태의 복잡도가 "Context로 충분한 수준"이었다.
이 앱의 상태는 대부분 "한 장소에서 읽고 한 장소에서 쓴다".
Redux의 action/reducer 분리나 Zustand의 store 패턴이 추가 가치를 제공하지 않았다.
서버 상태 캐시는 @tanstack/react-query가 담당하므로 클라이언트 상태만 Context에.

### useRef와 useState의 사용 분리

- `lastEventIdRef` — WebSocket 콜백에서 클로저 문제 없이 최신 값 참조
- `flushInFlightRef` — flush 중복 실행 가드 (렌더를 트리거하면 안 되는 값)
- useState — UI에 바인딩되는 모든 값

이 분리가 "렌더에 영향 없는 값은 ref, 렌더에 필요한 값은 state"라는 원칙을 보여준다.

## 설계 판단 — Optimistic UI와 서버 상태 병합

`buildIncidentList`는 서버 인시던트 목록과 outbox를 병합한다.
이 함수가 앱에서 가장 복잡한 순수 함수다.

두 가지 유형의 낙관적 처리:
1. **생성**: `POST /incidents` pending → `local-xxx` id로 목록에 추가
2. **변경**: pending mutation의 action에 따라 인시던트 status를 낙관적으로 전이

`IncidentListItem`은 `Incident`를 확장해 `source`, `syncState`, `pendingActions` 메타데이터를 추가한다.
화면에서 이 메타데이터로 상태 표시를 다르게 한다(live vs queued vs failed).

## 설계 판단 — Contract 재사용

harness와 동일한 `@incident-ops/contracts`를 `file:` 프로토콜로 공유한다.
서버 API의 request/response shape이 타입으로 고정되어 있으므로
클라이언트에서 잘못된 필드를 보내는 것이 컴파일 타임에 잡힌다.

## 설계 판단 — StorageAdapter 추상화

AsyncStorage를 직접 호출하지 않고 `StorageAdapter` 인터페이스를 둔다.
테스트에서 `createMemoryStorage()`로 교체한다.
이것이 "외부 의존성을 인터페이스 뒤에 숨긴다"는 가장 단순한 형태의 DI(Dependency Injection)다.

## 배운 것

### 1. Outbox는 UX 기능이다

outbox를 "기술적 안전장치"로만 보면 OutboxScreen이 불필요해 보인다.
하지만 사용자에게 "당신의 액션이 어디까지 처리됐는지" 투명하게 보여주는 것은 제품 가치다.
특히 인시던트 운영 도구에서 "내 ack이 서버에 도달했는가"는 중요한 정보다.

### 2. WebSocket + React Query의 조합

WebSocket 이벤트를 받으면 React Query 캐시를 invalidate한다.
이벤트 payload를 직접 캐시에 반영하지 않는다.
이 "nuke & refetch" 전략은 단순하지만 정합성이 보장된다.
더 정교한 패턴(이벤트 payload로 캐시 업데이트)은 복잡성 대비 이점이 불확실했다.

### 3. 포트폴리오 데모 = 재현 가능한 장애 시나리오

portfolio-presentation.md에서 가장 인상적인 슬라이드는
"base URL을 잘못 바꿔서 장애를 유발하고, outbox에 쌓인 mutation을 보여주고, 복구 후 flush"하는 시퀀스다.
이것이 "환경을 통제하여 장애를 재현하는 능력"을 보여준다.

### 4. zod + react-hook-form 통합

`z.enum(USER_ROLES)` 패턴으로 contracts의 상수 배열이 폼 검증 스키마까지 연결된다.
타입 정의 → 런타임 검증 → 에러 메시지까지 한 줄로 관통한다.

## 한계와 미래 개선

| 한계 | 이유 | 개선 방향 |
|------|------|-----------|
| Context 리렌더 범위 | AppModel 변경 시 모든 소비자가 리렌더 | useMemo로 값 분리 또는 상태 분할 |
| WebSocket 자동 재연결 없음 | onError/onClose에서 재연결 로직 미구현 | exponential backoff 재연결 |
| 낙관적 UI 불일치 가능성 | 서버 응답과 낙관적 전이가 다를 경우 | 서버 응답으로 outbox 아이템 reconcile |

## harness와의 대비

| 관점 | harness | client |
|------|---------|--------|
| API 호출 | 없음 (순수 함수) | fetch + WebSocket |
| 상태 관리 | 변수 체이닝 | Context + useRef + AsyncStorage |
| 테스트 | 입출력 검증 | 통합 테스트 + e2e (Maestro) |
| 목적 | 워크플로우 설계 검증 | 제품 수준 구현 증명 |
