# 지식 인덱스: 이 프로젝트에서 연결되는 것들

## 핵심 개념 → 문서 연결

| 개념 | 프로젝트 내 문서 | 비고 |
| --- | --- | --- |
| 상태 층 분리 (URL / localStorage / memory) | `docs/concepts/state-and-url-boundaries.md` | 세 층의 경계와 우선순위 |
| 이벤트 위임 | `docs/concepts/event-delegation-notes.md` | delegation 선택 이유와 구조적 효과 |
| 검증 전략 | `docs/references/verification-notes.md` | unit, DOM, E2E 분리 |

## 핵심 파일 → 역할 요약

| 파일 | 역할 |
| --- | --- |
| `vanilla/src/types.ts` | 전체 상태 타입 정의 (BoardItem, BoardQuery, SelectionState, BoardState) |
| `vanilla/src/data.ts` | 하드코딩된 4개 태스크 항목 |
| `vanilla/src/state.ts` | URL 파싱/직렬화, localStorage 읽기/쓰기, 필터/정렬, selection reconciliation |
| `vanilla/src/app.ts` | 마크업 생성, mount 함수, 이벤트 위임 핸들러, render cycle |
| `vanilla/src/main.ts` | 앱 진입점 |
| `vanilla/src/styles.css` | board 스타일링 |
| `vanilla/tests/state.test.ts` | query 파싱, 직렬화, persistence, selection reconciliation 단위 테스트 |
| `vanilla/tests/shell.test.ts` | DOM 수준 통합 테스트 (URL 동기화, delegation 기반 편집) |
| `vanilla/tests/board.spec.ts` | Playwright E2E (필터 동기화, reload 후 복원, 키보드 편집) |

## 이 프로젝트의 위치

```
frontend-foundations 트랙
├── 01-semantic-layouts-and-a11y  ← 의미 구조, 접근성 기초
├── 02-dom-state-and-events       ← 현재
└── 03-networked-ui-patterns      ← 비동기 UI, abort, retry
```

- **이전**: `01-semantic-layouts-and-a11y` — landmark, form pairing, keyboard flow
- **다음**: `03-networked-ui-patterns` — 이 프로젝트에서 비어 있는 비동기/네트워크 축을 채운다
- **연결**: `react-internals/01-vdom-foundations`에서 이 프로젝트의 innerHTML 교체 방식의 한계를 Virtual DOM으로 해결한다
