# 개발 타임라인: 처음부터 검증까지

이 문서는 프로젝트의 전체 개발 과정을 순서대로 기록한다. 소스코드를 읽으면 최종 결과물은 보이지만, 어떤 순서로 파일을 만들었고, 어떤 시행착오를 거쳤고, 어떤 명령어로 확인했는지는 코드만으로 알 수 없다.

---

## Phase 0: 프로젝트 스캐폴딩

### 디렉토리와 설정 파일 생성

```
02-dom-state-and-events/
├── index.html              # Vite 진입점
├── package.json            # @front-react/dom-state-and-events
├── vite.config.ts          # 127.0.0.1:4173 고정
├── vitest.config.ts        # jsdom 환경, vanilla/tests/**/*.test.ts
├── playwright.config.ts    # vanilla/tests/**/*.spec.ts, webServer 자동 기동
├── tsconfig.json           # TypeScript 설정
├── problem/                # 문제 명세
├── vanilla/src/            # 구현 코드
├── vanilla/tests/          # 테스트
└── docs/                   # 공개 문서
```

### 의존성

`package.json`의 devDependencies는 01 프로젝트와 동일하다.

```bash
# study/ 루트에서 전체 워크스페이스 의존성 설치 (이미 설치되어 있으면 건너뜀)
cd study
npm install
```

- Vite `^7.1.12`, TypeScript `^5.9.3`, Vitest `^4.0.18`, jsdom `^28.1.0`, Playwright `^1.58.2`

---

## Phase 1: 데이터 모델 정의

### vanilla/src/types.ts 작성

먼저 전체 앱의 상태 구조를 타입으로 정의했다.

- `BoardItem`: 태스크 하나의 데이터 (id, title, workspace, owner, status, priority)
- `BoardQuery`: 현재 검색/필터/정렬 조건
- `SelectionState`: 선택된 행과 편집 중인 행
- `BoardState`: 위의 모든 것을 합친 전체 상태
- `PersistedBoardState`: localStorage에 저장할 부분만 추린 타입

### vanilla/src/data.ts 작성

4개의 하드코딩된 태스크 항목을 `DEFAULT_ITEMS` 배열로 정의.

---

## Phase 2: 상태 관리 로직

### vanilla/src/state.ts 작성

이 파일이 가장 많은 시간이 들었다. 순서대로:

1. **`parseQuery()` / `serializeQuery()`**: URL query string ↔ BoardQuery 변환. 유효하지 않은 파라미터는 무시한다.
2. **`loadPersistedState()` / `savePersistedState()`**: localStorage JSON 읽기/쓰기. JSON.parse 실패 시 null 반환.
3. **`applyQuery()`**: items 배열에 검색, 상태 필터, 정렬을 적용. 검색은 title, workspace, owner를 모두 대상으로 한다.
4. **`reconcileSelection()`**: 필터 결과에 선택된 항목이 없으면 첫 번째 보이는 항목으로 전환.
5. **`createInitialBoardState()`**: URL → localStorage → default 순서로 merge.

### 로직 단위 테스트 작성

```bash
npm run test --workspace @front-react/dom-state-and-events
```

`vanilla/tests/state.test.ts`에 4개 테스트:
- query 파싱 (known values)
- query 직렬화 (default 제외)
- 저장/복원 라운드트립
- URL query가 persisted query를 덮어쓰는지 + 보이지 않는 selection 초기화

---

## Phase 3: UI 마크업과 렌더링

### vanilla/src/app.ts — getMarkup() 작성

전체 HTML 마크업을 반환하는 함수. 현재 상태를 받아서 동적으로 생성한다.

- 검색/필터/정렬 form controls (현재 query 값 반영)
- 테이블 rows (visibleItems 기반, 선택/편집 상태 반영)
- 편집 모드일 때 input 요소, 아닐 때 텍스트 노드
- 디테일 패널 (선택된 항목의 정보, 또는 "Select a row" 안내)
- 상태 알림 (`role="status" aria-live="polite"`)

### vanilla/src/styles.css 작성

board 레이아웃, 테이블 스타일, 상태 칩, 편집 input 스타일링. 이전 프로젝트와 같은 디자인 언어를 유지하되, 테이블과 인라인 편집에 필요한 요소를 추가.

### 개발 서버에서 시각 확인

```bash
npm run dev --workspace @front-react/dom-state-and-events
# → http://127.0.0.1:4173 에서 확인
```

---

## Phase 4: 이벤트 핸들링

### vanilla/src/app.ts — mountBoard() 작성

이벤트 핸들링의 핵심 결정은 **delegation 패턴**이다. 개별 요소가 아닌 container에 listener를 걸고, `data-action`/`data-id` 속성으로 대상을 식별한다.

등록한 이벤트:

| 이벤트 | 대상 | 동작 |
| --- | --- | --- |
| `input` | 검색 input (`name="search"`) | query 변경 → render |
| `change` | 필터 selects (`name="status"`, `name="sort"`) | query 변경 → render |
| `click` | `[data-action]` 버튼 | select/edit/save/cancel → 상태 전이 → render |
| `keydown` | `[data-edit-id]` input | Enter로 저장, form submit 방지 |

### DOM 통합 테스트 작성

`vanilla/tests/shell.test.ts`에 2개 테스트:
- 검색/필터 변경이 URL에 반영되는지
- delegated click으로 selection과 inline edit가 수행되고 localStorage에 저장되는지

```bash
npm run test --workspace @front-react/dom-state-and-events
```

---

## Phase 5: E2E 테스트

### vanilla/tests/board.spec.ts 작성

```bash
npm run e2e --workspace @front-react/dom-state-and-events
```

2개 시나리오:
1. **필터/편집 후 reload**: 검색어와 편집 결과가 URL과 localStorage를 통해 복원되는지
2. **키보드 전용 편집**: Tab으로 이동 → Enter로 선택 → Enter로 편집 → 타이핑 → Enter로 저장

---

## Phase 6: 문서 작성

### docs/concepts/ 작성
- `state-and-url-boundaries.md`: URL/localStorage/memory 세 층의 역할과 경계
- `event-delegation-notes.md`: 위임 패턴 선택 이유와 효과

### docs/references/ 작성
- `verification-notes.md`: 테스트 범위와 각 레벨의 역할

---

## Phase 7: 최종 검증

```bash
cd study
npm run verify --workspace @front-react/dom-state-and-events
# → vitest 6개 테스트 통과
# → playwright 2개 E2E 시나리오 통과
```

검증 일시: 2026-03-08

---

## 사용한 도구 요약

| 도구 | 용도 |
| --- | --- |
| Vite | 개발 서버, HMR |
| TypeScript | 정적 타입 (특히 상태 타입 설계가 핵심이었음) |
| Vitest + jsdom | 상태 로직 단위 테스트, DOM 통합 테스트 |
| Playwright | E2E 브라우저 테스트 (URL 동기화, reload, 키보드 흐름) |
| 브라우저 DevTools | Application > Local Storage 확인, URL query 확인 |

## 자주 사용한 CLI 명령어

```bash
# 개발 서버
npm run dev --workspace @front-react/dom-state-and-events

# 단위 + DOM 테스트
npm run test --workspace @front-react/dom-state-and-events

# E2E 테스트
npm run e2e --workspace @front-react/dom-state-and-events

# 전체 검증
npm run verify --workspace @front-react/dom-state-and-events

# watch 모드 (개발 중 반복 확인)
npm run test:watch --workspace @front-react/dom-state-and-events
```
