# front-react

`front-react`는 "웹 기초 -> React mental model -> 제품형 UI"를 하나의 읽기 흐름으로 묶은 학습 레포다. 이 저장소의 공개 표면은 각 프로젝트마다 아래 질문에 바로 답하도록 정리한다.

- 무슨 문제를 풀었는가
- 어떤 답을 구현했는가
- 무엇으로 검증했는가
- 다음 단계가 왜 필요한가

현재 활성 작업 공간은 아래 두 축으로 읽으면 된다.

- `study/`: 실행 가능한 학습 프로젝트와 테스트
- `docs/`: 저장소 공통 규칙, 커리큘럼, 검증 기준

## 읽는 순서

1. [docs/README.md](docs/README.md)에서 저장소 공통 규칙과 문서 역할을 먼저 확인한다.
2. 아래 핵심 커리큘럼 표를 위에서 아래 순서대로 읽는다.
3. 각 프로젝트에서는 `problem/README.md -> 구현 README -> docs/README.md` 순서로 본다.
4. 전체 맥락이 필요하면 [docs/curriculum-map.md](docs/curriculum-map.md)와 각 트랙 README를 함께 본다.

## 핵심 커리큘럼

| 순서 | 프로젝트 | 문제 질문 | 내가 만든 답 | 바로가기 |
| --- | --- | --- | --- | --- |
| 01 | `frontend-foundations`<br>[01-semantic-layouts-and-a11y](study/frontend-foundations/01-semantic-layouts-and-a11y/README.md) | semantic 구조와 접근성을 갖춘 UI shell은 어떻게 설계하는가 | landmark, labeled form, inline validation, keyboard flow를 갖춘 vanilla 설정 화면 | [problem](study/frontend-foundations/01-semantic-layouts-and-a11y/problem/README.md) · [vanilla](study/frontend-foundations/01-semantic-layouts-and-a11y/vanilla/README.md) · [docs](study/frontend-foundations/01-semantic-layouts-and-a11y/docs/README.md) |
| 02 | `frontend-foundations`<br>[02-dom-state-and-events](study/frontend-foundations/02-dom-state-and-events/README.md) | filter, selection, edit, URL, local persistence를 같은 화면에서 어떻게 동기화하는가 | query state, local state, root delegation, focus 복원을 묶은 task board | [problem](study/frontend-foundations/02-dom-state-and-events/problem/README.md) · [vanilla](study/frontend-foundations/02-dom-state-and-events/vanilla/README.md) · [docs](study/frontend-foundations/02-dom-state-and-events/docs/README.md) |
| 03 | `frontend-foundations`<br>[03-networked-ui-patterns](study/frontend-foundations/03-networked-ui-patterns/README.md) | loading, empty, error, retry, abort를 제품처럼 다루려면 무엇이 필요한가 | mock API와 race-aware state를 갖춘 directory/explorer UI | [problem](study/frontend-foundations/03-networked-ui-patterns/problem/README.md) · [vanilla](study/frontend-foundations/03-networked-ui-patterns/vanilla/README.md) · [docs](study/frontend-foundations/03-networked-ui-patterns/docs/README.md) |
| 04 | `react-internals`<br>[01-vdom-foundations](study/react-internals/01-vdom-foundations/README.md) | JSX와 DOM 사이의 최소 Virtual DOM 계층은 어떻게 동작하는가 | `createElement`부터 `render`까지 구현한 TypeScript VDOM 패키지 | [problem](study/react-internals/01-vdom-foundations/problem/README.md) · [ts](study/react-internals/01-vdom-foundations/ts/README.md) · [docs](study/react-internals/01-vdom-foundations/docs/README.md) |
| 05 | `react-internals`<br>[02-render-pipeline](study/react-internals/02-render-pipeline/README.md) | 최소 DOM 변경 계산과 render/commit 분리는 어떻게 설계하는가 | diff, patch, cooperative work loop를 묶은 render pipeline 패키지 | [problem](study/react-internals/02-render-pipeline/problem/README.md) · [ts](study/react-internals/02-render-pipeline/ts/README.md) · [docs](study/react-internals/02-render-pipeline/docs/README.md) |
| 06 | `react-internals`<br>[03-hooks-and-events](study/react-internals/03-hooks-and-events/README.md) | hooks, effect cleanup, delegated event를 하나의 runtime으로 어떻게 묶는가 | `useState`, `useEffect`, delegated event를 갖춘 학습용 runtime | [problem](study/react-internals/03-hooks-and-events/problem/README.md) · [ts](study/react-internals/03-hooks-and-events/ts/README.md) · [docs](study/react-internals/03-hooks-and-events/docs/README.md) |
| 07 | `react-internals`<br>[04-runtime-demo-app](study/react-internals/04-runtime-demo-app/README.md) | 직접 만든 runtime을 실제 상호작용 앱 위에서 어디까지 설명할 수 있는가 | debounced search, load more, render metrics를 갖춘 runtime consumer app | [problem](study/react-internals/04-runtime-demo-app/problem/README.md) · [ts](study/react-internals/04-runtime-demo-app/ts/README.md) · [docs](study/react-internals/04-runtime-demo-app/docs/README.md) |
| 08 | `frontend-portfolio`<br>[01-ops-triage-console](study/frontend-portfolio/01-ops-triage-console/README.md) | 데이터가 많은 운영 화면에서 triage workflow를 어떻게 설계하고 검증하는가 | dashboard, queue, bulk action, optimistic update를 갖춘 Next.js 운영 콘솔 | [problem](study/frontend-portfolio/01-ops-triage-console/problem/README.md) · [next](study/frontend-portfolio/01-ops-triage-console/next/README.md) · [docs](study/frontend-portfolio/01-ops-triage-console/docs/README.md) |
| 09 | `frontend-portfolio`<br>[02-client-onboarding-portal](study/frontend-portfolio/02-client-onboarding-portal/README.md) | 고객-facing onboarding flow에서 validation, draft, route guard를 어떻게 묶는가 | sign-in, wizard, invite, retry를 갖춘 Next.js onboarding 앱 | [problem](study/frontend-portfolio/02-client-onboarding-portal/problem/README.md) · [next](study/frontend-portfolio/02-client-onboarding-portal/next/README.md) · [docs](study/frontend-portfolio/02-client-onboarding-portal/docs/README.md) |
| 10 | `frontend-portfolio`<br>[03-realtime-collab-workspace](study/frontend-portfolio/03-realtime-collab-workspace/README.md) | 실시간 협업 UI에서 optimistic patch, reconnect replay, conflict surface를 어떻게 설명 가능하게 만들 것인가 | shared board, doc blocks, presence, conflict banner를 갖춘 Next.js 협업 워크스페이스 | [problem](study/frontend-portfolio/03-realtime-collab-workspace/problem/README.md) · [next](study/frontend-portfolio/03-realtime-collab-workspace/next/README.md) · [docs](study/frontend-portfolio/03-realtime-collab-workspace/docs/README.md) |

## 검증 시작점

패키지 매니저는 `npm`, 기준 Node 버전은 `20 LTS`다. 전체 핵심 경로를 한 번에 검증하려면 `study/` 워크스페이스에서 아래 명령을 실행한다.

```bash
cd study
npm install
npm run verify:core
```

트랙 단위 검증 명령은 아래를 따른다.

- `npm run verify:foundations`
- `npm run verify:internals`
- `npm run verify:portfolio`

## 의도적으로 범위 밖

이 저장소는 주니어 끝자락까지를 목표로 하며, 아래 범위는 의도적으로 다루지 않는다.

- production-grade CRDT/OT와 대규모 협업 병합 해결
- 대규모 SSR caching 전략
- micro-frontends
- production backend 운영
- 대규모 observability/infra
