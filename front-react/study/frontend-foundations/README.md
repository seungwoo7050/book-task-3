# Frontend Foundations Track

이 트랙은 주니어 경로의 시작점이다. React 이전에 브라우저와 HTML/CSS, DOM 상태, 이벤트, 비동기 UI를 직접 다루며 제품형 프론트의 바닥 체력을 만든다.

## 왜 Vanilla Web부터 시작하는가

- semantic HTML과 a11y는 프레임워크와 무관한 기초다.
- DOM state와 event는 React가 추상화하기 전의 원형을 이해해야 한다.
- async UI 상태는 fetch, retry, empty/error state를 직접 다룰 때 더 선명하게 보인다.

## 프로젝트 목록

| 순서 | 프로젝트 | 상태 | 설명 |
| --- | --- | --- | --- |
| 01 | [01-semantic-layouts-and-a11y](01-semantic-layouts-and-a11y/README.md) | verified | semantic HTML, responsive layout, forms, keyboard navigation |
| 02 | [02-dom-state-and-events](02-dom-state-and-events/README.md) | verified | DOM state sync, event handling, localStorage, URL state |
| 03 | [03-networked-ui-patterns](03-networked-ui-patterns/README.md) | verified | fetch, loading/error/retry, abort, query-driven navigation |

## 구현 스택

- Vanilla web
- TypeScript
- Vite
- Vitest
- Playwright

## 검증 원칙

현재 `verified` 상태인 foundations 프로젝트는 세 개 전부다. 루트에서는 `verify:foundations`가 전체 foundations 체인을 실행한다.
