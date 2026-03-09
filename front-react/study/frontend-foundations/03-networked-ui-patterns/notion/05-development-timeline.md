# 개발 타임라인: 처음부터 검증까지

---

## Phase 0: 프로젝트 스캐폴딩

### 디렉토리 구조

```
03-networked-ui-patterns/
├── index.html
├── package.json            # @front-react/networked-ui-patterns
├── vite.config.ts
├── vitest.config.ts
├── playwright.config.ts
├── tsconfig.json
├── problem/
├── vanilla/src/
├── vanilla/tests/
└── docs/
```

### 의존성

이전 프로젝트와 동일한 devDependencies:

```bash
cd study
npm install
```

- Vite `^7.1.12`, TypeScript `^5.9.3`, Vitest `^4.0.18`, jsdom `^28.1.0`, Playwright `^1.58.2`

---

## Phase 1: 데이터 모델과 서비스 인터페이스

### vanilla/src/types.ts 작성

새로운 타입 도입:
- `AsyncState`: `"idle" | "loading" | "success" | "empty" | "error"` — 비동기 상태 enum
- `ExplorerService`: `listDirectory()`와 `getDirectoryItem()`을 가진 인터페이스. AbortSignal을 매개변수로 받는다.

### vanilla/src/data.ts 작성

5개의 운영 문서 항목: runbook 2개, policy 2개, guide 1개.

### vanilla/src/service.ts 작성

mock service 구현. 가장 중요한 부분:

1. **`wait()` 함수**: `setTimeout`과 `AbortSignal`을 결합. signal이 abort되면 타이머를 클리어하고 `AbortError`를 던진다.
2. **`listDirectory()`**: 인위적 지연(140 + 검색어 길이 * 25ms) → `simulateFailure` 체크 → 필터링 + 정렬
3. **`getDirectoryItem()`**: 90ms 지연 → ID로 조회

---

## Phase 2: 상태 관리

### vanilla/src/state.ts 작성

- `parseUrlState()` / `serializeUrlState()`: URL ↔ ExplorerUrlState (search, category, item)
- `createRequestTracker()`: 증가하는 token으로 최신 요청인지 판별하는 유틸리티

이전 프로젝트의 `parseQuery()`/`serializeQuery()`와 같은 패턴이지만, `item` 파라미터가 추가되어 상세 패널의 선택 상태도 URL에 반영된다.

---

## Phase 3: UI 마크업

### vanilla/src/app.ts — getMarkup() 작성

`ExplorerState`를 받아서 전체 HTML을 반환. 상태별 분기가 핵심:

- `listState === "loading"` → "Loading directory…" + 로딩 영역
- `listState === "error"` → 에러 메시지 + Retry 버튼
- `listState === "empty"` → "No matching results" 안내
- `listState === "success"` → 결과 목록 (각 항목이 button으로 클릭 가능)
- 상세 패널도 `detailState`에 따라 같은 패턴

### vanilla/src/styles.css 작성

explorer 레이아웃, 결과 목록 스타일, 에러 상태 강조, 로딩 표시.

### 개발 서버 확인

```bash
npm run dev --workspace @front-react/networked-ui-patterns
# → http://127.0.0.1:4173 에서 확인
```

---

## Phase 4: 비동기 로드 로직

### mountDirectoryExplorer() 작성

이 프로젝트에서 가장 복잡한 부분. 두 개의 AbortController와 두 개의 requestTracker를 운용한다.

**loadList()** 흐름:
1. 이전 listController를 abort
2. 새 AbortController 생성
3. requestTracker에서 token 발급
4. `listState: "loading"`으로 render
5. service.listDirectory() 호출
6. 응답 시 token이 최신인지 확인
7. 결과 있으면 success + selectedId 결정 → loadDetail() 호출
8. 결과 없으면 empty
9. 실패 시 AbortError면 무시, 아니면 error 상태

**loadDetail()** 흐름:
1. 이전 detailController를 abort
2. 새 AbortController + token 발급
3. `detailState: "loading"`으로 render
4. service.getDirectoryItem() 호출
5. 응답 시 token 체크 → 성공/실패 상태 반영

### 이벤트 핸들러 연결 (delegation)

| 이벤트 | 대상 | 동작 |
| --- | --- | --- |
| `input` | 검색 input | query.search 변경 → loadList() |
| `change` | 카테고리 select | query.category 변경 → loadList() |
| `click` + `data-action="open-item"` | 결과 항목 버튼 | loadDetail(itemId) |
| `click` + `data-action="retry-list"` | Retry 버튼 | loadList() 재호출 |
| `click` + `data-action="retry-detail"` | Detail retry | loadDetail(selectedId) 재호출 |
| `click` + `data-action="simulate-failure"` | 실패 시뮬레이션 토글 | simulateFailureNext 전환 |

### 초기 로드

mount 직후 `void loadList("#searchInput")`를 호출해서 초기 목록을 로드한다.

---

## Phase 5: 테스트 작성

### 단위 테스트

```bash
npm run test --workspace @front-react/networked-ui-patterns
```

**vanilla/tests/service.test.ts** (2개 테스트):
- AbortController로 요청 취소 시 AbortError 발생 확인
- requestTracker의 token 최신 여부 검증

**vanilla/tests/explorer.test.ts** (2개 테스트):
- mock service 주입 후 검색 → URL 동기화 + 상세 로드 확인
- simulate failure → 에러 UI 표시 → retry → 복구 확인

### E2E 테스트

```bash
npm run e2e --workspace @front-react/networked-ui-patterns
```

**vanilla/tests/explorer.spec.ts** (2개 시나리오):
1. 검색어 입력 → URL search/item 파라미터 반영 → 상세 패널에 문서 표시
2. Simulate failure → 에러 → Retry → 복구 → 키보드로 항목 선택

---

## Phase 6: 문서 작성

### docs/concepts/
- `request-lifecycle.md`: 5가지 AsyncState의 분류와 목록/상세 상태 분리 이유
- `query-navigation.md`: URL에 넣는 상태(search, category, item)와 넣지 않는 상태의 경계

### docs/references/
- `verification-notes.md`: service, DOM, E2E 테스트의 역할

---

## Phase 7: 최종 검증

```bash
cd study
npm run verify --workspace @front-react/networked-ui-patterns
# → vitest 4개 테스트 통과
# → playwright 2개 E2E 시나리오 통과
```

검증 일시: 2026-03-08

---

## 사용한 도구 요약

| 도구 | 용도 |
| --- | --- |
| Vite | 개발 서버 |
| TypeScript | 정적 타입 (AsyncState, ExplorerService 인터페이스가 핵심) |
| Vitest + jsdom | 서비스 단위 테스트, DOM 통합 테스트 |
| Playwright | E2E (비동기 로딩/에러/복구 시나리오) |
| AbortController (Web API) | 요청 취소 |

## 자주 사용한 CLI 명령어

```bash
npm run dev --workspace @front-react/networked-ui-patterns
npm run test --workspace @front-react/networked-ui-patterns
npm run e2e --workspace @front-react/networked-ui-patterns
npm run verify --workspace @front-react/networked-ui-patterns
npm run test:watch --workspace @front-react/networked-ui-patterns
```
