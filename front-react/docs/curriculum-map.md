# Frontend Junior-End Curriculum Map

이 저장소의 공식 목표는 `front-react`를 "초보자 -> 주니어 끝자락" 경로로 읽히는 학습 저장소로 만드는 것이다. 핵심 경로는 breadth와 depth를 같이 보여 주기 위해 3트랙으로 나뉜다.

## Core Curriculum

| 순서 | 트랙 | 프로젝트 | 상태 | 핵심 질문 |
| --- | --- | --- | --- | --- |
| 01 | `frontend-foundations` | `01-semantic-layouts-and-a11y` | verified | 의미 구조와 접근성은 왜 UI 기초인가 |
| 02 | `frontend-foundations` | `02-dom-state-and-events` | verified | DOM 상태와 이벤트는 어떻게 동기화되는가 |
| 03 | `frontend-foundations` | `03-networked-ui-patterns` | verified | loading/empty/error/retry를 제품처럼 다루려면 무엇이 필요한가 |
| 04 | `react-internals` | `01-vdom-foundations` | verified | VNode와 동기 재귀 렌더는 어떻게 동작하는가 |
| 05 | `react-internals` | `02-render-pipeline` | verified | diff와 render/commit 분리는 왜 필요한가 |
| 06 | `react-internals` | `03-hooks-and-events` | verified | hooks와 delegated events는 런타임에 어떻게 얹히는가 |
| 07 | `react-internals` | `04-runtime-demo-app` | verified | 공유 런타임 위에서 실제 기능 조합은 어떻게 보이는가 |
| 08 | `frontend-portfolio` | `01-ops-triage-console` | verified | 데이터가 많은 내부도구 UI를 어떻게 설계하고 검증하는가 |
| 09 | `frontend-portfolio` | `02-client-onboarding-portal` | verified | 고객-facing form과 onboarding 흐름은 어떻게 구성하는가 |

## Why These Three Tracks

- `frontend-foundations`: 브라우저, 시맨틱 구조, 이벤트, 비동기 UI를 React 없이 먼저 이해한다.
- `react-internals`: React가 감추는 추상화를 직접 구현하면서 mental model을 깊게 만든다.
- `frontend-portfolio`: 채용 관점에서 실제로 보여 줄 수 있는 제품형 결과물을 만든다.

이 세 축이 같이 있어야 "웹 기초는 아는데 제품이 없다" 또는 "React 앱은 만들지만 브라우저 이해가 얕다" 같은 비어 있는 축이 줄어든다.

## Phase Breakdown Appendix

`react-internals`는 원래 7단계 세분화였지만, 주니어 끝자락 기준으로는 너무 길었다. 활성 경로는 4개 프로젝트만 남기고, 세부 단계 reasoning은 트랙 부록 문서로 보존한다.

- 세부 매핑: `study/react-internals/docs/phase-map.md`
- 레거시 근거: `docs/legacy-audit.md`

## Verification Reading

- `verified`: fresh install 기준 검증을 통과한 프로젝트
- `planned`: 구조와 문제 경계는 고정했지만 구현/검증은 아직 없는 프로젝트
- `verify:core`: 현재 `verified` 상태인 핵심 프로젝트만 실행

현재 기준 `verify:core`에 포함되는 것은 아래 아홉 단계다.

- `study/frontend-foundations/01-semantic-layouts-and-a11y`
- `study/frontend-foundations/02-dom-state-and-events`
- `study/frontend-foundations/03-networked-ui-patterns`
- `study/react-internals/01-vdom-foundations`
- `study/react-internals/02-render-pipeline`
- `study/react-internals/03-hooks-and-events`
- `study/react-internals/04-runtime-demo-app`
- `study/frontend-portfolio/01-ops-triage-console`
- `study/frontend-portfolio/02-client-onboarding-portal`
