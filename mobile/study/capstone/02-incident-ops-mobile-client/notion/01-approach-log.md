# 01 — Approach Log: Incident Ops Mobile Client 구현 과정

## Phase 1: lib 계층 — 인프라 함수

앱의 기반은 `src/lib/` 디렉토리의 7개 모듈이다.
화면이나 상태 관리 코드를 쓰기 전에 이 계층을 먼저 완성했다.

### api.ts — HTTP/WS 경계

`requestJson<T>()` 제네릭 함수가 모든 API 호출의 기반이다.
- `normalizeBaseUrl`로 trailing slash 정리
- `buildWebsocketUrl`로 http→ws 프로토콜 변환 + lastEventId 쿼리 파라미터
- `ApiError` 클래스로 status code 포함한 에러 전파
- idempotency key를 `x-idempotency-key` 헤더로 전달

개별 API 함수: `loginRequest`, `listIncidents`, `listAudit`, `createIncidentRequest`, `acknowledgeIncidentRequest`, `requestResolutionRequest`, `decideApprovalRequest`.
모두 typed input → typed output 패턴이다.

### storage.ts — AsyncStorage 추상화

`StorageAdapter` 인터페이스로 AsyncStorage를 추상화했다.
테스트에서 `createMemoryStorage()`로 교체 가능하다.

영속화 대상 4가지:
- `session` — 로그인 토큰 + AuthActor
- `settings` — baseUrl
- `outbox` — QueuedMutation 배열
- `lastEventId` — WebSocket 재연결 커서

`readJson<T>` + `saveJson<T>` 헬퍼로 JSON 직렬화/역직렬화를 통일했다.
파싱 실패 시 fallback을 반환하는 방어적 처리.

### outbox.ts — 오프라인 큐 핵심 로직

`createQueuedMutation` → `markQueuedMutationSynced` / `markQueuedMutationFailed` → `retryQueuedMutation`.
이 4개 순수 함수가 outbox 상태 머신이다.

`MAX_OUTBOX_ATTEMPTS`(3)를 초과하면 `failed`(DLQ) 상태가 된다.

가장 복잡한 함수는 `buildIncidentList`:
- 서버 인시던트 목록과 outbox를 병합한다
- `POST /incidents` 중 synced가 아닌 것 → optimistic item으로 추가
- 기존 인시던트에 pending mutation이 있으면 → `applyActionToIncident`로 낙관적 상태 전이
- 각 아이템에 `source`(server/optimistic), `syncState`(live/queued/failed), `pendingActions` 메타데이터 추가

### stream.ts — WebSocket 래퍼

`openIncidentStream`은 WebSocket 연결을 열고 cleanup 함수를 반환한다.
`onEvent` 콜백으로 `StreamEvent`를 파싱해 전달한다.
onOpen/onClose/onError 콜백으로 연결 상태를 추적한다.

### connectivity.ts — NetInfo 래퍼

`@react-native-community/netinfo`의 `NetInfoState`를 `ConnectionState` 타입으로 변환한다.
`isConnected && isInternetReachable !== false` 조합으로 실제 인터넷 도달 가능성을 판단한다.

### forms.ts — Zod 스키마

4개 스키마: `loginSchema`, `createIncidentSchema`, `resolutionSchema`, `approvalDecisionSchema`.
contracts에서 가져온 `USER_ROLES`, `INCIDENT_SEVERITIES`, `APPROVAL_DECISIONS` 상수를 `z.enum()`에 직접 전달한다.
한국어 에러 메시지로 UX를 고려했다.

### queries.ts — React Query 키

`incidentKeys.feed(baseUrl, userId)`와 `auditKeys.detail(baseUrl, incidentId)`.
키에 baseUrl과 userId를 포함해 서버 변경이나 사용자 전환 시 캐시가 자동 분리된다.

## Phase 2: AppModel — 전역 상태 관리

`AppModel.tsx`가 이 앱의 심장이다.
React Context + hooks로 모든 상태와 액션을 제공한다.

### Bootstrap

컴포넌트 마운트 시 AsyncStorage에서 4개 값을 병렬 로드한다:
```typescript
const [savedSettings, savedSession, savedOutbox, savedLastEventId] =
  await Promise.all([loadSettings, loadSession, loadOutbox, loadLastEventId]);
```
완료 후 `bootstrapState`가 'loading' → 'ready'로 전환된다.

### 자동 영속화

`settings`, `session`, `outbox`, `lastEventId`가 변경될 때마다 useEffect로 AsyncStorage에 저장한다.
bootstrapState가 'ready'일 때만 저장해서 초기 로드 시 덮어쓰기를 방지한다.

### Outbox Flush

`flushPendingMutations`는 pending 상태의 mutation을 순서대로 실행한다.
- 성공 → `markQueuedMutationSynced`
- 실패 → `markQueuedMutationFailed`
- 완료 후 → incident/audit 쿼리 invalidate

`flushInFlightRef`로 중복 실행을 방지한다.
connection이 online이고 pending mutation이 있으면 useEffect가 자동으로 flush를 트리거한다.

### WebSocket Stream

세션이 있고 온라인이면 자동으로 WebSocket 연결을 연다.
이벤트 수신 시 `lastEventId`를 갱신하고 쿼리를 invalidate한다.
`lastEventIdRef`로 최신 값을 클로저 문제 없이 참조한다.

### Custom Hooks

- `useAppModel()` — Context에서 전체 상태/액션 접근
- `useIncidentItems()` — infinite query + outbox 병합 → `IncidentListItem[]`
- `usePendingApprovalItems()` — RESOLUTION_PENDING 필터
- `useIncidentAudit(incidentId)` — 감사 로그 쿼리

## Phase 3: 화면 구현

### LoginScreen

react-hook-form + zodResolver로 폼을 구성한다.
`Controller` 컴포넌트로 각 필드를 제어한다.
역할 선택은 `USER_ROLES.map(role => <ActionButton>)` 패턴이다.
선택된 역할은 `setValue('role', role, { shouldValidate: true })`로 반영한다.

### IncidentsScreen

FlatList + ListHeaderComponent(outbox summary, stream status, New Incident 버튼) + 렌더링.
각 아이템에 `StatusPill`로 status와 syncState를 시각화한다.
"Load more" 버튼으로 다음 페이지를 가져온다.

### IncidentDetailScreen

`route.params.incidentId`로 현재 인시던트를 찾는다.
역할과 상태에 따라 canAck/canRequestResolution/canDecide를 계산한다.
zod로 reason/note 입력을 검증한 후 outbox에 mutation을 추가한다.

### OutboxScreen

FlatList로 outbox 전체를 표시한다.
pending/synced/failed 카운트, flush 버튼, clear synced 버튼.
failed 아이템에만 retry 버튼이 보인다.

### ApprovalsScreen

`usePendingApprovalItems()`로 RESOLUTION_PENDING만 필터링해 표시한다.
별도 API 없이 incident feed에서 파생된 뷰다.

### SettingsScreen

base URL 변경, 연결 상태 표시, 로그아웃.
base URL로 장애 시뮬레이션이 가능하다 — 잘못된 URL 입력 → outbox failure 재현.

## Phase 4: 네비게이션

`RootNavigator`가 3가지 분기를 제어한다:
- bootstrapState !== 'ready' → `LoadingScreen`
- session === null → `AuthStack` (Login)
- session exists → `MainTabs` (Bottom Tabs)

MainTabs의 IncidentsTab은 내부에 Native Stack(Feed → Create → Detail)을 중첩한다.
나머지 탭(Approvals, Outbox, Settings)은 단일 화면이다.

## Phase 5: UI 컴포넌트

`Ui.tsx`에 공유 컴포넌트를 집중시켰다:
- `ScreenLayout` — SafeAreaView + scroll 옵션
- `SectionCard` — eyebrow + title + body 카드
- `ActionButton` — solid/ghost/danger tone
- `AppTextField` — label + error text
- `StatusPill` — 상태 뱃지
- `MetricRow` — label: value 한 줄
- `EmptyState` — 빈 목록 안내
