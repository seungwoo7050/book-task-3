# Frontend Foundations

이 트랙은 React 이전에 브라우저 자체를 이해하는 단계다. 의미 구조, DOM 상태, 이벤트, 비동기 UI를 직접 다루면서 이후 React 학습의 바닥 체력을 만든다.

## 프로젝트 인덱스

| 프로젝트 | 문제 질문 | 내가 만든 답 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01-semantic-layouts-and-a11y](01-semantic-layouts-and-a11y/README.md)<br>[problem](01-semantic-layouts-and-a11y/problem/README.md) · [vanilla](01-semantic-layouts-and-a11y/vanilla/README.md) · [docs](01-semantic-layouts-and-a11y/docs/README.md) | semantic 구조와 접근성을 갖춘 UI shell은 어떻게 설계하는가 | landmark, labeled form, inline validation, keyboard flow가 있는 vanilla 설정 화면 | `verify --workspace @front-react/semantic-layouts-a11y`<br>`vitest` + `playwright` | DOM state와 이벤트를 같은 화면에서 다루는 단계로 이동 |
| [02-dom-state-and-events](02-dom-state-and-events/README.md)<br>[problem](02-dom-state-and-events/problem/README.md) · [vanilla](02-dom-state-and-events/vanilla/README.md) · [docs](02-dom-state-and-events/docs/README.md) | selection, filter, sort, edit, URL, local persistence를 어떻게 동기화하는가 | query state, local state, root delegation, focus 복원을 묶은 task board | `verify --workspace @front-react/dom-state-and-events`<br>`vitest` + `playwright` | 비동기 요청 상태와 navigation state를 다루는 단계로 이동 |
| [03-networked-ui-patterns](03-networked-ui-patterns/README.md)<br>[problem](03-networked-ui-patterns/problem/README.md) · [vanilla](03-networked-ui-patterns/vanilla/README.md) · [docs](03-networked-ui-patterns/docs/README.md) | loading, empty, error, retry, abort를 제품처럼 다루려면 무엇이 필요한가 | mock API, request race 보호, query-driven navigation을 갖춘 explorer UI | `verify --workspace @front-react/networked-ui-patterns`<br>`vitest` + `playwright` | React rendering model을 직접 구현하는 `react-internals` 트랙으로 이동 |

## 워크스페이스 명령

```bash
cd study
npm run verify:foundations
```

개별 프로젝트를 실행하거나 검증할 때는 각 프로젝트 README의 workspace 명령을 그대로 사용한다.
