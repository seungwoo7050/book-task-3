# 01 Semantic Layouts And A11y

상태: `verified`

이 프로젝트는 semantic HTML, form structure, responsive layout, keyboard navigation, accessible state 표현을 먼저 익히는 시작점이다.

## 왜 주니어 경로에 필요한가

React나 디자인 시스템을 쓰더라도 의미 구조와 접근성이 약하면 제품 품질이 무너진다. 이 단계는 가장 기본적인 화면 셸에서 "읽히는 구조"와 "탐색 가능한 상호작용"을 직접 다루게 한다.

## Prerequisite

- HTML/CSS 기본 문법
- 브라우저 개발자 도구 기초

## 구조

- `problem/`: authored brief와 입력/스크립트 자리
- `vanilla/`: 정적이지만 상호작용 가능한 UI shell 구현 자리
- `docs/`: a11y와 시맨틱 구조에 대한 공개 문서
- `notion/`: 로컬 전용 작업 로그

## Build/Test Command

```bash
cd study
npm run dev --workspace @front-react/semantic-layouts-a11y
npm run verify --workspace @front-react/semantic-layouts-a11y
```

## 다음 단계로 이어지는 한계

이 단계는 의미 구조와 상호작용 기초에 집중하므로 DOM 상태 동기화와 event orchestration은 깊게 다루지 않는다. 그 축은 `02-dom-state-and-events`가 이어받는다.

## 검증 메모

- 검증 일시: 2026-03-08
- `vitest`: `5`개 테스트 통과
- `playwright`: `2`개 E2E 시나리오 통과
