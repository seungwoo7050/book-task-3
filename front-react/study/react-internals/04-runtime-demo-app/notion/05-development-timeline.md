# 개발 타임라인 — demo app 프로젝트 구축 과정

## Phase 0: 프로젝트 초기화

```bash
cd study
npm install
```

workspace 루트에서 install을 실행. `@front-react/runtime-demo-app`의 package.json에 선언된 `@front-react/hooks-and-events` 의존이 symlink로 연결된다. hooks-and-events가 다시 render-pipeline를, render-pipeline이 vdom-foundations를 참조하므로 전체 4단계 의존 체인이 형성된다.

이 프로젝트는 Vite를 사용하므로 dev server와 build도 가능:

```bash
npm run dev --workspace @front-react/runtime-demo-app
```

## Phase 1: 데이터 모듈 구성

```
ts/src/data.ts
```

DemoItem 인터페이스 정의 + 10개의 데모 아이템 배열 작성. 각 아이템은 runtime의 특정 측면을 설명하는 내용으로 구성. 카테고리: metrics, interaction, search, pagination, effects, integration, limitations.

## Phase 2: 앱 컴포넌트 구현

```
ts/src/app.ts
```

순서대로 구현:
1. `useDebouncedValue` — 커스텀 hook (useState + useEffect + setTimeout)
2. `updateMetrics` — metrics 갱신 헬퍼 함수
3. `DemoApp` — 메인 컴포넌트 (query, debouncedQuery, visibleCount, metrics 4개 상태)
4. 검색 결과 필터링 + pagination + metrics panel UI
5. `mountRuntimeDemo` / `resetRuntimeDemo` — 진입점 함수

createElement 호출로 전체 UI 구성 (JSX 없음):
- header: 소개 텍스트
- section (controls): 검색 input + status
- section (grid): results panel + metrics panel

## Phase 3: 스타일 시트

```
ts/src/styles.css
```

CSS 작성:
- IBM Plex Sans 기반 타이포그래피
- 2컬럼 그리드 레이아웃 (results + metrics)
- 카드 디자인 (results-panel, result-card)
- 반응형 breakpoint (880px → 1컬럼)
- focus-visible outline 스타일

## Phase 4: 진입점 설정

```
ts/src/main.ts
index.html
```

main.ts에서 `#app` 컨테이너를 찾아 mountRuntimeDemo 호출. index.html에서 main.ts를 로드.

```bash
npm run dev --workspace @front-react/runtime-demo-app
```

Vite dev server로 브라우저에서 확인. debounce 동작, Load more 버튼, metrics panel 갱신을 시각적으로 검증.

## Phase 5: 테스트 작성

```
ts/tests/demo.test.ts
```

세 가지 통합 테스트:

```bash
npm run test --workspace @front-react/runtime-demo-app
```

1. **debounce search**: input에 "metrics" 입력 → 즉시는 10개 → 260ms 후 2개로 줄어듦 + metric-query 확인
2. **pagination**: Load more 클릭 → 4개 → 8개 + metric-visible 확인
3. **multiple interactions**: 클릭 + 검색 조합 → renderCount > 1 + commit-ms 존재 확인

테스트 환경:
- `vi.useFakeTimers()` — setTimeout 제어
- `vi.advanceTimersByTimeAsync(260)` — debounce 타이머 발동
- `resetRuntimeDemo()` — 각 테스트 전 상태 초기화

## Phase 6: 타입 체크

```bash
npm run typecheck --workspace @front-react/runtime-demo-app
```

hooks-and-events의 타입과 이 프로젝트의 타입이 올바르게 연결되는지 확인. createElement에 Function type을 전달하는 부분, DelegatedEvent 타입 호환 등.

## Phase 7: 문서 작성

```
docs/concepts/shared-runtime-consumption.md
docs/concepts/runtime-limitation-note.md
docs/references/verification-notes.md
docs/presentation.md
```

- shared-runtime-consumption: workspace dependency 경계 설명
- runtime-limitation-note: 현재 한계 목록 (profiler 없음, async 미지원 등)
- verification-notes: 검증 범위
- presentation: 5분 발표 흐름 (demo app 전용)

## Phase 8: 전체 검증

```bash
cd study
npm run verify --workspace @front-react/runtime-demo-app
```

verify = test + typecheck. 모든 검증 통과 후 `verified` 상태로 전환.

## 사용된 도구 정리

| 도구 | 용도 |
|------|------|
| TypeScript 5.3 | strict mode 타입 체크 |
| Vitest 1.6.0 | 통합 테스트, fake timer |
| jsdom 24.0.0 | DOM API 에뮬레이션 |
| Vite 5.4 | dev server + 빌드 |
| npm workspaces | 전체 의존 체인 관리 |
| vi.useFakeTimers | setTimeout 제어 (debounce 테스트) |
| performance.now() | 렌더 시간 측정 (학습용) |

## 디렉토리 구조

```
04-runtime-demo-app/
├── index.html            # Vite 진입점
├── package.json          # @front-react/runtime-demo-app
├── tsconfig.json
├── vite.config.ts
├── vitest.config.ts
├── README.md
├── docs/
│   ├── concepts/
│   │   ├── shared-runtime-consumption.md
│   │   └── runtime-limitation-note.md
│   ├── references/
│   │   └── verification-notes.md
│   └── presentation.md
├── problem/              # 레거시 capstone 원문
├── ts/
│   ├── src/
│   │   ├── data.ts       # DemoItem 데이터
│   │   ├── app.ts        # DemoApp 컴포넌트 + useDebouncedValue
│   │   ├── main.ts       # 진입점
│   │   └── styles.css    # UI 스타일
│   └── tests/
│       └── demo.test.ts  # 통합 테스트 3개
└── notion/               # (로컬 전용)
```
