# 02 — Debug Log: Incident Ops Mobile Client 디버깅 기록

## 문제 1: Outbox flush 중복 실행

### 상황

`flushPendingMutations`이 useEffect에서 자동 트리거된다.
dependency array에 `outbox`가 포함되어 있다.
flush가 outbox를 변경(synced 마킹)하면 → useEffect 재실행 → 또 flush.

### 발생 조건

pending mutation이 여러 개 있을 때, 첫 번째 mutation이 synced되면
outbox state가 갱신되어 useEffect가 다시 실행된다.
이때 아직 flush가 진행 중이면 이중 실행이 발생한다.

### 해결

`flushInFlightRef`(useRef)로 가드를 건다.
```typescript
if (flushInFlightRef.current || !session || !connection.isConnected) {
  return;
}
flushInFlightRef.current = true;
try { /* flush loop */ }
finally { flushInFlightRef.current = false; }
```
useRef는 렌더를 트리거하지 않으면서 최신 값을 유지한다.

## 문제 2: lastEventId 클로저 문제

### 상황

WebSocket onEvent 콜백은 useEffect 안에서 정의된다.
이 클로저는 생성 시점의 lastEventId를 캡처한다.
이벤트를 받아 lastEventId를 갱신해도 클로저 안의 값은 바뀌지 않는다.

### 문제

`Math.max(lastEventId, event.eventId)`에서 lastEventId가 항상 초기값이면
매번 0과 비교하게 되어 실질적으로 의미가 없다.

### 해결

`lastEventIdRef`(useRef)를 분리해서 최신 값을 항상 참조한다.
```typescript
lastEventIdRef.current = Math.max(lastEventIdRef.current, event.eventId);
setLastEventId(current => Math.max(current, event.eventId));
```
ref는 클로저 문제를 우회하고, setState는 영속화를 트리거한다.

## 문제 3: Optimistic item의 id 충돌

### 상황

outbox에서 생성한 optimistic 인시던트의 id는 `local-${item.id}`다.
서버에서 실제로 생성된 인시던트는 서버가 부여한 UUID를 가진다.

### 문제

같은 인시던트가 optimistic item(id: local-xxx)과 server item(id: uuid) 두 개로 표시될 수 있다.
outbox mutation이 synced 상태가 되면 optimistic item은 필터링되지만,
synced 처리와 서버 목록 갱신 사이에 타이밍 차이가 있으면 중복이 보인다.

### 해결

`toOptimisticIncident` 함수에서 `item.state === 'synced'`이면 null을 반환한다.
flush 완료 후 `queryClient.invalidateQueries`로 서버 목록을 즉시 갱신한다.
이 두 조치로 중복 표시 윈도우를 최소화한다.

## 문제 4: applyActionToIncident의 incidentId 매칭

### 상황

outbox의 각 mutation은 `payload.incidentId`로 어떤 인시던트에 적용할지 결정한다.
`POST /incidents`(생성)는 incidentId가 없다 — 서버가 id를 부여하니까.

### 문제

`buildIncidentList`에서 서버 인시던트에 outbox를 적용할 때,
`POST /incidents` mutation이 서버 인시던트와 매칭되면 안 된다.
생성 mutation은 optimistic item으로만 표시되어야 한다.

### 해결

```typescript
const related = outbox.filter(item => {
  if (item.action === 'POST /incidents') return false;
  return safeString(item.payload.incidentId) === incident.id;
});
```
`POST /incidents`를 명시적으로 제외한다.

## 문제 5: zod 검증과 outbox 연동

### 상황

IncidentDetailScreen에서 resolution reason이나 approval note를 입력할 때
zod 스키마(`resolutionSchema`, `approvalDecisionSchema`)로 검증한다.

### 문제

검증은 화면에서, mutation 생성은 AppModel에서 한다.
AppModel의 `queueRequestResolution`은 검증 없이 outbox에 바로 넣는다.

### 현재 처리

화면에서 `safeParse` → 성공 시에만 AppModel 함수를 호출한다.
```typescript
const parsed = resolutionSchema.safeParse({ reason: note });
if (!parsed.success) {
  setActionError(parsed.error.issues[0]?.message ?? 'invalid reason');
  return;
}
queueRequestResolution(currentIncident.id, { reason: parsed.data.reason });
```
검증 책임은 화면(경계)에, 실행 책임은 AppModel에 두는 분리.

## 문제 6: file: 프로토콜과 metro 번들러

### 상황

`@incident-ops/contracts`가 `file:../problem/code/contracts`로 설치된다.
metro 번들러의 `watchFolders`에 이 경로가 포함되지 않으면 심볼릭 링크를 따라가지 못한다.

### 증상

`Unable to resolve module '@incident-ops/contracts'` 에러.
node_modules에 심볼릭 링크는 있지만 metro가 번들에 포함하지 못함.

### 해결

metro.config.js에서 watchFolders에 contracts 경로를 추가하거나,
`resolver.nodeModulesPaths`를 설정해 심볼릭 링크 해석을 허용한다.
또는 metro 캐시를 정리: `npx react-native start --reset-cache`.

## 문제 7: Bootstrap 중 AsyncStorage 저장 방지

### 상황

앱 시작 시 AsyncStorage에서 값을 로드한다.
로드 중 기본값(빈 outbox 등)이 state에 들어간다.
이 기본값이 useEffect에 의해 AsyncStorage에 저장되면 기존 데이터가 덮어쓰여진다.

### 해결

모든 영속화 useEffect에 `bootstrapState !== 'ready'` 가드를 건다.
```typescript
useEffect(() => {
  if (bootstrapState !== 'ready') return;
  void saveOutbox(outbox, appStorage);
}, [bootstrapState, outbox]);
```
bootstrap 완료 전에는 저장하지 않는다.
