# Front React Study Blog

`front-react/study` 아래에는 작은 실습부터 포트폴리오 앱까지 성격이 다른 프로젝트가 섞여 있다. 이 디렉터리는 그 결과물을 README 요약처럼 늘어놓는 대신, 각 프로젝트가 실제로 어디서부터 막혔고 어떤 코드와 검증으로 다음 단계로 넘어갔는지를 따라가도록 다시 정리한 읽기용 블로그다.

예전 초안은 [_legacy/20260313-isolate-and-rewrite](_legacy/20260313-isolate-and-rewrite/README.md) 아래에 보관해 두었다. 새 문서는 그 문체를 입력으로 삼지 않고, 소스코드, README, docs, 테스트, CLI replay만 근거로 다시 썼다.

## 읽는 법

각 프로젝트는 항상 두 단계로 읽게 만들었다.

1. `00-series-map.md`
   - 프로젝트를 한 줄로 정의하고, 왜 이 순서로 읽어야 하는지, 어떤 근거를 썼는지, 현재 검증 상태가 어떤지 먼저 알려 준다.
2. 본문 글
   - 구현 순서가 실제로 어떻게 흘렀는지, 어떤 코드가 전환점이었는지, 마지막에 무엇이 남았는지를 서사적으로 복원한다.

간단한 프로젝트는 `series map + 본문 1편`으로 끝난다. 복잡한 프로젝트는 구현 축이 갈리는 지점에서 본문을 여러 편으로 나눴다.

## 트랙 안내

### [frontend-foundations](frontend-foundations/README.md)

브라우저가 원래 제공하는 구조와 상태를 몸으로 익히는 트랙이다. semantic shell, URL/local state 경계, request lifecycle을 React 이전 단계에서 먼저 고정한다.

- [01-semantic-layouts-and-a11y](frontend-foundations/01-semantic-layouts-and-a11y/00-series-map.md)
- [02-dom-state-and-events](frontend-foundations/02-dom-state-and-events/00-series-map.md)
- [03-networked-ui-patterns](frontend-foundations/03-networked-ui-patterns/00-series-map.md)

### [react-internals](react-internals/README.md)

JSX에서 시작해 VDOM, diff/commit, hook runtime, consumer app까지 한 단계씩 직접 만들어 보는 트랙이다. React를 "쓴다"보다 "어떻게 움직이는지 설명한다"에 더 가까운 기록이 모여 있다.

- [01-vdom-foundations](react-internals/01-vdom-foundations/00-series-map.md)
- [02-render-pipeline](react-internals/02-render-pipeline/00-series-map.md)
- [03-hooks-and-events](react-internals/03-hooks-and-events/00-series-map.md)
- [04-runtime-demo-app](react-internals/04-runtime-demo-app/00-series-map.md)

### [frontend-portfolio](frontend-portfolio/README.md)

학습용 과제에서 한 걸음 더 나가 실제 제품처럼 설명 가능한 결과물을 정리한 트랙이다. 내부도구형 UI, 고객-facing onboarding flow, 실시간 협업 UI를 각각 다른 관점에서 다룬다.

- [01-ops-triage-console](frontend-portfolio/01-ops-triage-console/00-series-map.md)
- [02-client-onboarding-portal](frontend-portfolio/02-client-onboarding-portal/00-series-map.md)
- [03-realtime-collab-workspace](frontend-portfolio/03-realtime-collab-workspace/00-series-map.md)
