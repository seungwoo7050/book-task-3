# 문제 인식 — 왜 demo app이 필요한가

## internals 트랙의 마지막 질문

세 프로젝트에 걸쳐 VNode 생성(01), diff/patch와 fiber reconciliation(02), hook과 delegated event(03)를 만들었다. 각각 동작하고 테스트도 통과한다. 하지만 "이 runtime으로 실제 기능을 만들면 어떤 일이 일어나는가?"에는 아직 답하지 않았다.

단위 테스트는 개별 모듈의 정확성을 검증하지만, 모듈이 합쳐져서 하나의 앱 흐름을 이룰 때 나타나는 문제는 다른 종류다. 검색 입력에서 debounce가 effect cleanup으로 돌아가고, 검색 결과가 바뀌면 pagination이 리셋되고, 모든 상호작용이 metrics panel에 반영되는 — 이런 조합을 테스트해야 runtime의 실제 능력과 한계가 드러난다.

## 이 프로젝트의 역할

이 프로젝트는 "capstone"이다. 새로운 runtime 기능을 구현하는 게 아니라, 기존 runtime을 소비(consume)하며 세 가지를 확인한다:

1. **workspace dependency 경계가 실제로 유지되는가**: hooks-and-events 패키지만 import하고, app은 기능 조합에 집중한다.
2. **hooks와 events가 현실적인 UI 패턴을 감당하는가**: debounced search, pagination, render metrics — 세 가지 기능이 동시에 돌아간다.
3. **어디에서 한계가 드러나는가**: profiler API 없음, async data fetching 미지원, true infinite scroll 불가 — 이 한계를 명시적으로 문서화한다.

## 다루는 범위

- debounced search: 커스텀 hook(`useDebouncedValue`)으로 검색어 지연 적용
- paginated results: PAGE_SIZE 단위로 검색 결과를 점진적 노출
- render metrics panel: 렌더 횟수, commit 시간, visible 개수, active query 추적
- shared runtime import: `@front-react/hooks-and-events`에서 createElement, render, useState, useEffect 사용
- Vite dev server: 브라우저에서 실제 동작 확인 가능

## 다루지 않는 범위

- 서버 사이드 렌더링, 라우팅
- async data fetching, suspense
- production-grade profiling (metrics는 학습용 관찰값)
- 접근성 완성도 (ARIA 최소한만)
- responsive design의 깊은 수준 (기본 media query만)

## 이 프로젝트가 끝나면

react-internals 트랙이 종료된다. "직접 만든 runtime이 어디까지 설명 가능하고 어디서 멈추는지"를 demo와 문서로 보여 줬으면, 실제 채용용 제품형 UI는 frontend-portfolio 트랙이 이어받는다.
