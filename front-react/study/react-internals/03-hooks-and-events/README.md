# 03 Hooks And Events

상태: `verified`

이 프로젝트는 `legacy/hooks-from-scratch`와 `legacy/mini-react`를 묶어, 함수 컴포넌트 상태/effect와 delegated event, runtime integration을 함께 다루는 단계다.

## 왜 주니어 경로에 필요한가

React를 실무에서 쓰려면 state/effect와 event가 한 런타임 안에서 어떻게 이어지는지 설명할 수 있어야 한다. 이 단계는 hooks와 events를 분리된 trivia가 아니라 같은 runtime 축으로 묶는다.

## Prerequisite

- `02-render-pipeline`
- render/commit split 이해

## 구조

- `problem/`: 레거시 원문과 제공 자산 위치
- `ts/`: hook slot, effect lifecycle, delegated events 구현 자리
- `docs/`: hooks/event integration 문서
- `notion/`: 로컬 전용 과정 로그

## Build/Test Command

```bash
cd study
npm run test --workspace @front-react/hooks-and-events
npm run typecheck --workspace @front-react/hooks-and-events
npm run verify --workspace @front-react/hooks-and-events
```

검증 범위는 아래와 같다.

- state update 이후 재렌더
- hook count 변화 감지
- effect setup / cleanup lifecycle
- delegated bubbling / `stopPropagation`
- state, event, effect가 같은 runtime loop로 이어지는 integration

## 다음 단계로 이어지는 한계

이 단계는 공유 런타임 위에서 실제 기능을 조합하는 demo app까지는 다루지 않는다. 그 축은 `04-runtime-demo-app`으로 이어진다.
