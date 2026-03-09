# 지식 인덱스: 이 프로젝트에서 연결되는 것들

## 핵심 개념 → 문서 연결

| 개념 | 프로젝트 내 문서 | 비고 |
| --- | --- | --- |
| 요청 상태 분류 (idle/loading/success/empty/error) | `docs/concepts/request-lifecycle.md` | 목록과 상세의 독립적 상태 관리 |
| URL에 넣을 상태의 경계 | `docs/concepts/query-navigation.md` | search, category, item vs 디버그 상태 |
| 검증 범위 | `docs/references/verification-notes.md` | service, DOM, E2E 역할 분리 |

## 핵심 파일 → 역할 요약

| 파일 | 역할 |
| --- | --- |
| `vanilla/src/types.ts` | DirectoryItem, AsyncState, ExplorerService 인터페이스 정의 |
| `vanilla/src/data.ts` | 5개 하드코딩 문서 항목 |
| `vanilla/src/service.ts` | mock service (인위적 지연, AbortSignal 존중, simulateFailure) |
| `vanilla/src/state.ts` | URL 파싱/직렬화, requestTracker |
| `vanilla/src/app.ts` | 마크업 생성, mount 함수, 비동기 로드, 이벤트 위임 |
| `vanilla/src/main.ts` | 앱 진입점 |
| `vanilla/tests/service.test.ts` | AbortError, requestTracker 단위 테스트 |
| `vanilla/tests/explorer.test.ts` | DOM 수준 통합 테스트 (검색 동기화, 실패/재시도) |
| `vanilla/tests/explorer.spec.ts` | Playwright E2E (query param, 실패/재시도, 키보드) |

## 이 프로젝트의 위치

```
frontend-foundations 트랙
├── 01-semantic-layouts-and-a11y  ← 의미 구조, 접근성
├── 02-dom-state-and-events       ← DOM 상태, 이벤트 위임
└── 03-networked-ui-patterns      ← 현재 (비동기 UI 마감)

→ react-internals 트랙으로 이어짐
  ├── 01-vdom-foundations         ← innerHTML 교체의 한계를 VDOM으로 해결
  └── ...
```

- **이전**: `02-dom-state-and-events` — 동기 상태와 이벤트의 기초
- **이후**: `react-internals/01-vdom-foundations` — 이 프로젝트에서 체감한 innerHTML 교체의 한계를 Virtual DOM으로 풀기 시작
- **포트폴리오 연결**: `frontend-portfolio` 트랙이 이 비동기 패턴을 실제 제품 수준으로 확장
