# 문제 정의

프로비넌스: `authored`

## 문제

directory/explorer UI에서 request state와 navigation state를 함께 다루려면 loading, empty, error, retry, abort, stale response를 모두 통제해야 한다. 이 프로젝트는 비동기 UI가 "서버처럼 느껴지는가"를 검증 가능한 형태로 구현한다.

## 제공 자산

- 이 문서: 문제 정의와 범위
- `data/`: 별도 입력 fixture가 필요 없는 단계를 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- 실제 서버 대신 mock API를 사용한다.
- request race와 abort를 무시하지 않고 명시적으로 처리해야 한다.
- URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다.

## 포함 범위

- loading, empty, error, retry
- abort and request race
- mock API latency
- query-param driven navigation
- integration and E2E smoke

## 제외 범위

- 실제 서버 운영
- authentication
- server-side rendering

## 요구 산출물

- `vanilla/`에 실행 가능한 explorer 구현
- request lifecycle과 query navigation 경계를 설명하는 공개 문서
- service, state, 화면 흐름을 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/networked-ui-patterns
```

- `vitest`: service helper, request race 보호, explorer state 확인
- `playwright`: retry, query-driven navigation, keyboard smoke 확인
