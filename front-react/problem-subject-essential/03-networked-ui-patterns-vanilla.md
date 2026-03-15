# 03-networked-ui-patterns-vanilla 문제지

## 왜 중요한가

directory/explorer UI에서 request state와 navigation state를 함께 다루려면 loading, empty, error, retry, abort, stale response를 모두 통제해야 한다. 이 프로젝트는 비동기 UI가 "서버처럼 느껴지는가"를 검증 가능한 형태로 구현한다.

## 목표

시작 위치의 구현을 완성해 실제 서버 대신 mock API를 사용한다, request race와 abort를 무시하지 않고 명시적으로 처리해야 한다, URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/data.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/main.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.spec.ts`
- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.test.ts`

## starter code / 입력 계약

- `../study/frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 서버 대신 mock API를 사용한다.
- request race와 abort를 무시하지 않고 명시적으로 처리해야 한다.
- URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다.
- loading, empty, error, retry
- abort and request race
- mock API latency
- query-param driven navigation
- integration and E2E smoke
- vanilla/에 실행 가능한 explorer 구현
- request lifecycle과 query navigation 경계를 설명하는 공개 문서
- service, state, 화면 흐름을 검증하는 테스트

## 제외 범위

- 실제 서버 운영
- authentication
- server-side rendering

## 성공 체크리스트

- 핵심 흐름은 `buildUrlState`와 `syncUrl`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `updates query params and loads detail from the directory list`와 `recovers from a simulated failure and keeps keyboard navigation viable`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd study && npm run verify --workspace @front-react/networked-ui-patterns`가 통과한다.

## 검증 방법

```bash
cd study && npm run verify --workspace @front-react/networked-ui-patterns
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`03-networked-ui-patterns-vanilla_answer.md`](03-networked-ui-patterns-vanilla_answer.md)에서 확인한다.
