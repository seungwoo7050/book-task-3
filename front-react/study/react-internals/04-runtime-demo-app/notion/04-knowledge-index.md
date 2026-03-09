# 지식 색인 — demo app 핵심 개념 정리

## useDebouncedValue (커스텀 hook)

```typescript
function useDebouncedValue<T>(value: T, delayMs: number): T
```

입력값의 debounced 버전을 반환하는 커스텀 hook. 내부적으로 useState + useEffect를 조합한다.

- value가 바뀌면 타이머 시작 (setTimeout)
- delayMs 후에 debounced 값 갱신
- value가 다시 바뀌면 이전 타이머 cleanup (clearTimeout)
- 기본 지연: DEBOUNCE_MS = 250ms

관련 코드: `ts/src/app.ts`

## DemoItem

```typescript
interface DemoItem {
  id: string;
  title: string;
  category: string;
  excerpt: string;
}
```

데모 데이터 아이템. 10개, 6개 카테고리(metrics, interaction, search, pagination, effects, integration, limitations).

검색은 `title + category + excerpt`를 합쳐서 소문자 includes로 수행.

관련 코드: `ts/src/data.ts`

## DemoMetrics

```typescript
interface DemoMetrics {
  renderCount: number;
  lastCommitMs: number;
  visibleCount: number;
  matchCount: number;
  activeQuery: string;
}
```

app state로 관리하는 렌더 관찰값. production profiler가 아닌 학습용 metrics.

- `renderCount`: 관찰된 렌더 횟수 (누적)
- `lastCommitMs`: 마지막 render→effect까지의 시간 (performance.now 기반)
- `visibleCount`: 현재 화면에 보이는 아이템 수
- `matchCount`: 검색 결과 전체 수
- `activeQuery`: 현재 적용된 검색어 ("all" 또는 정규화된 검색어)

관련 코드: `ts/src/app.ts`의 `updateMetrics`

## Pagination 패턴

```
PAGE_SIZE = 4
visibleItems = filteredItems.slice(0, visibleCount)
hasMore = visibleItems.length < filteredItems.length
```

- Load more 클릭 → `setVisibleCount(c => c + PAGE_SIZE)`
- 검색어 변경 → `setVisibleCount(PAGE_SIZE)` (리셋)
- 버튼 상태: `hasMore ? "Load more results" : "All results loaded"`

## 상태 흐름 다이어그램

```
[input 이벤트]
  ↓
setQuery(value)  ← 즉시
  ↓
useDebouncedValue
  ↓ (250ms 후)
debouncedQuery 갱신  ← setTimeout callback
  ↓
normalizedQuery = debouncedQuery.trim().toLowerCase()
  ↓
filteredItems = DEMO_ITEMS.filter(...)
  ↓
visibleItems = filteredItems.slice(0, visibleCount)
  ↓
useEffect → setVisibleCount(PAGE_SIZE)     ← 검색어 변경 시
useEffect → updateMetrics(...)              ← 결과 변경 시
```

## Shared Runtime Consumption

이 demo app이 import하는 것:
- `createElement` — VNode 생성
- `render` — root에 VNode 트리를 마운트
- `resetRuntime` — 테스트용 상태 초기화
- `useState` — 상태 관리
- `useEffect` — 부수 효과
- `SetStateAction` — 타입 (functional update 지원)

모두 `@front-react/hooks-and-events`에서 가져옴.

## Vite Dev Server

```bash
npm run dev --workspace @front-react/runtime-demo-app
```

브라우저에서 실제 demo를 확인하기 위한 개발 서버. 이전 프로젝트들(01, 02, 03)은 Vitest + jsdom만으로 검증했지만, 이 프로젝트는 시각적 확인이 필요.

- `index.html` → `ts/src/main.ts` → `app.ts`의 `mountRuntimeDemo`
- styles.css로 CSS 적용

## CSS 구조 요약

| 클래스 | 용도 |
|--------|------|
| `.demo-shell` | 전체 래퍼, min-height: 100vh |
| `.demo-hero` | 상단 소개 영역 |
| `.demo-controls` | 검색 입력 + 결과 상태 |
| `.demo-grid` | 2컬럼 그리드 (results + metrics) |
| `.results-panel` | 검색 결과 카드 리스트 |
| `.metrics-panel` | 렌더 메트릭 dl 목록 |
| `.result-card` | 개별 결과 카드 |
| `.load-more` | 페이지네이션 버튼 |
| `.empty-state` | 검색 결과 없음 메시지 |

반응형: `@media (max-width: 880px)` → 1컬럼

## npm Workspace 의존 체인 (전체)

```
vdom-foundations (01)
  ↑
render-pipeline (02)
  ↑
hooks-and-events (03)
  ↑
runtime-demo-app (04) — 최종 consumer
```

```json
"dependencies": {
  "@front-react/hooks-and-events": "*"
}
```

## Runtime 한계 (이 프로젝트에서 확인된 것)

| 한계 | 설명 |
|------|------|
| Profiler API 없음 | metrics는 app state로 추정, phase별 분리 불가 |
| async data fetching 미지원 | 정적 DEMO_ITEMS만 사용 |
| useState/useEffect만 | useReducer, useMemo, useRef 등 미지원 |
| 단일 root | 다중 root mount 불가 |
| attribute 범위 제한 | data-* 등 확장 속성 미포함 |
| infinite scroll 불가 | Load more 클릭 기반 pagination만 |

관련 문서: `docs/concepts/runtime-limitation-note.md`
