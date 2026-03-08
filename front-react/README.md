# front-react

이 저장소는 "초보자 -> 주니어 끝자락 프론트 엔지니어" 경로를 study-first 방식으로 정리한 학습 저장소다. 목표는 단순히 React 사용법을 익히는 것이 아니라, 웹 플랫폼 기초와 React mental model, 제품형 UI 구현과 검증 습관까지 하나의 읽기 쉬운 커리큘럼으로 묶는 것이다.

루트 구조의 의미는 고정한다.

- `legacy/`: 기존 학습 자산을 보존하는 읽기 전용 참조 트리
- `study/`: 새 커리큘럼과 실행 가능한 구현을 쌓는 활성 작업 공간
- `docs/`: 저장소 전체에 공통으로 적용되는 커리큘럼, 검증, 템플릿 문서

이 저장소는 git 메타데이터를 전제로 설명하지 않는다. 문서와 명령은 현재 파일 경로와 실제 실행 가능한 워크스페이스 기준으로만 적는다.

## 핵심 경로

활성 커리큘럼은 3트랙 9프로젝트로 고정한다.

1. `frontend-foundations`: semantic HTML, CSS, DOM, event, async, browser UI 기초
2. `react-internals`: React 런타임 핵심 추상화와 한계 이해
3. `frontend-portfolio`: 채용용으로 직접 시연 가능한 제품형 앱

현재 기준 핵심 코스는 아래 순서를 따른다.

1. `study/frontend-foundations/01-semantic-layouts-and-a11y`
2. `study/frontend-foundations/02-dom-state-and-events`
3. `study/frontend-foundations/03-networked-ui-patterns`
4. `study/react-internals/01-vdom-foundations`
5. `study/react-internals/02-render-pipeline`
6. `study/react-internals/03-hooks-and-events`
7. `study/react-internals/04-runtime-demo-app`
8. `study/frontend-portfolio/01-ops-triage-console`
9. `study/frontend-portfolio/02-client-onboarding-portal`

## 왜 3트랙인가

- `frontend-foundations`가 없으면 React 바깥의 브라우저 기초가 비어 있다.
- `react-internals`가 없으면 React를 쓰는 이유와 한계를 깊게 이해하기 어렵다.
- `frontend-portfolio`가 없으면 채용 관점에서 "실제로 맡길 수 있는 제품형 프론트" 신호가 약하다.

즉, 이 저장소는 단일 프레임워크 튜토리얼이 아니라 "웹 기초 -> React 이해 -> 제품 구현"의 연결을 의도적으로 만든다.

## 현재 상태

- `legacy/`는 6단계 React internals 자산을 보존하고 있다.
- `study/frontend-foundations/`는 새로 추가된 핵심 시작 트랙이다.
- `study/react-internals/`는 7단계 세분화를 4개 핵심 단계 + 세부 부록으로 압축했다.
- `study/frontend-portfolio/`는 내부도구형 앱과 고객-facing 앱을 함께 다루는 2앱 체제로 확장한다.
- 2026-03-08 기준 핵심 3트랙 9프로젝트가 모두 `verified` 상태다.

## 의도적으로 범위 밖인 것

이 저장소는 주니어 끝자락까지를 목표로 하며, 아래 범위는 의도적으로 제외한다.

- 실시간 협업과 복잡한 동시성 충돌 해결
- 대규모 SSR caching 전략
- micro-frontends
- production backend 운영
- 대규모 observability/infra

## 시작점

- 저장소 공통 문서: [docs/README.md](docs/README.md)
- 전체 커리큘럼 맵: [docs/curriculum-map.md](docs/curriculum-map.md)
- 역량 매핑: [docs/junior-skill-matrix.md](docs/junior-skill-matrix.md)
- 웹 기초 트랙: [study/frontend-foundations/README.md](study/frontend-foundations/README.md)
- React internals 트랙: [study/react-internals/README.md](study/react-internals/README.md)
- 제품형 포트폴리오 트랙: [study/frontend-portfolio/README.md](study/frontend-portfolio/README.md)

## 검증 기본 원칙

- 패키지 매니저는 `npm`으로 고정한다.
- Node 기준 버전은 20 LTS다.
- 검증은 `study/` 워크스페이스에서 fresh install 후 수행한다.
- `verify:core`는 현재 `verified` 상태인 핵심 프로젝트만 순서대로 실행한다.
- 레거시 자산은 참조만 하고 수정하지 않는다.
