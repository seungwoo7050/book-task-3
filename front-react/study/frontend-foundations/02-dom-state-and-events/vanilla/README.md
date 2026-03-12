# Vanilla 구현

상태: `verified`

## 이 구현이 답하는 범위

- search, status filter, sort
- delegated row interaction
- inline edit and selection detail
- local persistence
- URL query serialization

## 핵심 파일

- `src/state.ts`: query parsing, serialization, persistence helper
- `src/app.ts`: root-level event delegation과 UI rerender
- `tests/board.spec.ts`: query -> select -> edit -> save 흐름 smoke

## 실행과 검증

```bash
cd study
npm run build --workspace @front-react/dom-state-and-events
npm run verify --workspace @front-react/dom-state-and-events
```

## 현재 한계

- 실제 network request는 없다.
- multi-select, drag and drop, schema migration은 다루지 않는다.
- keyboard flow는 query -> select -> edit -> save 핵심 경로에 집중한다.
