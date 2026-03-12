# React Internals

이 트랙은 React를 흉내 내는 장난감 만들기가 아니라, 주니어가 설명할 수 있어야 하는 핵심 mental model을 4단계로 압축한 경로다. 각 단계는 이전 단계의 패키지를 실제로 소비하면서 다음 추상화를 쌓는다.

## 프로젝트 인덱스

| 프로젝트 | 문제 질문 | 내가 만든 답 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01-vdom-foundations](01-vdom-foundations/README.md)<br>[problem](01-vdom-foundations/problem/README.md) · [ts](01-vdom-foundations/ts/README.md) · [docs](01-vdom-foundations/docs/README.md) | JSX와 DOM 사이의 최소 Virtual DOM 계층은 어떻게 동작하는가 | `createElement`, `createTextElement`, `createDom`, `updateDom`, `render`를 구현한 기반 패키지 | `test:vdom`, `typecheck:vdom`, `verify:vdom` | 최소 DOM 변경 계산과 commit 타이밍 분리로 이동 |
| [02-render-pipeline](02-render-pipeline/README.md)<br>[problem](02-render-pipeline/problem/README.md) · [ts](02-render-pipeline/ts/README.md) · [docs](02-render-pipeline/docs/README.md) | 무엇이 바뀌었는지 계산하고 언제 DOM에 반영할지를 어떻게 분리하는가 | diff, patch, cooperative work loop, `flushSync`를 갖춘 render pipeline | `verify --workspace @front-react/render-pipeline`<br>`vitest` + `typecheck` | hooks, effect, delegated event가 같은 runtime에서 만나는 단계로 이동 |
| [03-hooks-and-events](03-hooks-and-events/README.md)<br>[problem](03-hooks-and-events/problem/README.md) · [ts](03-hooks-and-events/ts/README.md) · [docs](03-hooks-and-events/docs/README.md) | hooks, effect cleanup, delegated event를 하나의 runtime으로 어떻게 묶는가 | `useState`, `useEffect`, delegated event, runtime integration을 갖춘 학습용 runtime | `verify --workspace @front-react/hooks-and-events`<br>`vitest` + `typecheck` | 직접 만든 runtime을 소비하는 앱 단계로 이동 |
| [04-runtime-demo-app](04-runtime-demo-app/README.md)<br>[problem](04-runtime-demo-app/problem/README.md) · [ts](04-runtime-demo-app/ts/README.md) · [docs](04-runtime-demo-app/docs/README.md) | 직접 만든 runtime이 실제 상호작용 앱 위에서 어디까지 설명 가능한가 | debounced search, load more, render metrics를 갖춘 runtime consumer app | `verify --workspace @front-react/runtime-demo-app`<br>`vitest` + `typecheck` | 제품형 UI 신호가 필요한 `frontend-portfolio` 트랙으로 이동 |

## 워크스페이스 명령

```bash
cd study
npm run verify:internals
```

왜 4단계로 압축했는지는 [docs/phase-map.md](docs/phase-map.md)에 따로 정리한다.
