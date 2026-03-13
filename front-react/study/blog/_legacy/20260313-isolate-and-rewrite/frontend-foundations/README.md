# frontend-foundations blog

`frontend-foundations`는 React 이전에 브라우저의 구조, 상태, 비동기 UI를 직접 다루는 단계다. 이 blog 레이어는 semantic shell -> DOM state orchestration -> networked UI lifecycle 순서를 소스와 verify CLI 기준으로 다시 복원한다.

## 이 레이어가 쓰는 근거

- 프로젝트 README, `problem/README.md`, `vanilla/README.md`, `docs/README.md`
- `vanilla/src/*`, `vanilla/tests/*`, `package.json`, `vite`/`vitest`/`playwright` 설정
- `git log --reverse --stat -- study/frontend-foundations/<project>`
- 2026-03-13 재실행한 `npm run verify --workspace ...`

## 프로젝트 목록

| 프로젝트 | 최종 blog | evidence ledger | structure |
| --- | --- | --- | --- |
| Semantic Layouts and A11y | [01-semantic-layouts-and-a11y/10-development-timeline.md](01-semantic-layouts-and-a11y/10-development-timeline.md) | [01-evidence-ledger.md](01-semantic-layouts-and-a11y/01-evidence-ledger.md) | [02-structure.md](01-semantic-layouts-and-a11y/02-structure.md) |
| DOM State and Events | [02-dom-state-and-events/10-development-timeline.md](02-dom-state-and-events/10-development-timeline.md) | [01-evidence-ledger.md](02-dom-state-and-events/01-evidence-ledger.md) | [02-structure.md](02-dom-state-and-events/02-structure.md) |
| Networked UI Patterns | [03-networked-ui-patterns/10-development-timeline.md](03-networked-ui-patterns/10-development-timeline.md) | [01-evidence-ledger.md](03-networked-ui-patterns/01-evidence-ledger.md) | [02-structure.md](03-networked-ui-patterns/02-structure.md) |
