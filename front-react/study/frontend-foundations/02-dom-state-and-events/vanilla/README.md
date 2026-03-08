# Vanilla Implementation

상태: `verified`

## problem scope covered

- search, status filter, sort
- delegated row interaction
- inline edit and selection detail
- local persistence
- URL query serialization

## build command

```bash
cd study
npm run build --workspace @front-react/dom-state-and-events
```

## test command

```bash
cd study
npm run verify --workspace @front-react/dom-state-and-events
```

## current status

- `verified`

## known gaps

- 실제 network request는 없다.
- multi-select, drag and drop, schema migration은 다루지 않는다.
- keyboard flow는 query -> select -> edit -> save 핵심 경로에 집중한다.

## implementation notes

- `vanilla/src/state.ts`가 query parsing, serialization, persistence를 담당한다.
- `vanilla/src/app.ts`는 root-level input/change/click/keydown delegation으로 UI를 갱신한다.
- rerender 뒤에도 검색과 selection 흐름을 이어가기 위해 포커스를 명시적으로 복원한다.
