# 02 DOM State And Events

상태: `verified`

이 프로젝트는 filterable task/workspace board를 통해 DOM state sync, event handling, event delegation, localStorage, URL query state를 직접 다룬다.

## 왜 주니어 경로에 필요한가

프레임워크 state 관리 이전에 브라우저 상태와 상호작용이 실제로 어떻게 이어지는지 이해해야 한다. 이 단계는 "이벤트가 발생했을 때 어떤 상태를 어디에 저장하고 어떻게 다시 그릴 것인가"를 직접 풀게 한다.

## Prerequisite

- `01-semantic-layouts-and-a11y`
- 기본적인 DOM API 이해

## 구조

- `problem/`: authored brief와 입력/스크립트 자리
- `vanilla/`: filterable board 구현 자리
- `docs/`: DOM/event/state reasoning 문서
- `notion/`: 로컬 전용 작업 로그

## Build/Test Command

```bash
cd study
npm run dev --workspace @front-react/dom-state-and-events
npm run verify --workspace @front-react/dom-state-and-events
```

## 다음 단계로 이어지는 한계

이 단계는 브라우저 내부 상태와 이벤트에 집중하므로 네트워크 지연, retry, abort 같은 비동기 UI 문제는 충분히 다루지 않는다. 그 축은 `03-networked-ui-patterns`로 이어진다.

## 검증 메모

- 검증 일시: 2026-03-08
- `vitest`: `6`개 테스트 통과
- `playwright`: `2`개 E2E 시나리오 통과
