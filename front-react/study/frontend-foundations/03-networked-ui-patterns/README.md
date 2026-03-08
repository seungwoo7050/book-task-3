# 03 Networked UI Patterns

상태: `verified`

이 프로젝트는 mock API를 쓰는 directory/explorer 앱을 통해 loading, empty, error, retry, abort, query-param driven navigation을 다룬다.

## 왜 주니어 경로에 필요한가

프론트 업무의 많은 문제는 UI 자체보다 네트워크와 비동기 상태에서 생긴다. 이 단계는 서버가 없어도 서버처럼 보이는 UX를 설계하고 설명할 수 있게 만든다.

## Prerequisite

- `02-dom-state-and-events`
- Promise와 fetch 흐름 이해

## 구조

- `problem/`: authored brief와 입력/스크립트 자리
- `vanilla/`: mock API 기반 explorer 구현 자리
- `docs/`: async UI와 request lifecycle 문서
- `notion/`: 로컬 전용 작업 로그

## Build/Test Command

```bash
cd study
npm run dev --workspace @front-react/networked-ui-patterns
npm run verify --workspace @front-react/networked-ui-patterns
```

## 다음 단계로 이어지는 한계

이 단계는 브라우저와 async UI를 React 없이 다루므로, 컴포넌트 추상화와 React rendering model은 직접 다루지 않는다. 그 질문은 `react-internals` 트랙이 이어받는다.

## 검증 메모

- 검증 일시: 2026-03-08
- `vitest`: `4`개 테스트 통과
- `playwright`: `2`개 E2E 시나리오 통과
