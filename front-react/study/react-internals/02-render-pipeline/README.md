# 02 Render Pipeline

상태: `verified`

이 프로젝트는 `legacy/reconciliation`과 `legacy/fiber-architecture`를 묶어, 최소 DOM 변경 계산과 render/commit 분리를 하나의 파이프라인 관점에서 설명하는 단계다.

## 왜 주니어 경로에 필요한가

React는 "다시 그린다"로 끝나지 않는다. 무엇이 바뀌었는지 계산하고, 그 계산을 언제 commit할지 분리하는 사고가 있어야 성능과 한계를 설명할 수 있다.

## Prerequisite

- `01-vdom-foundations`
- VNode와 동기 재귀 render 이해

## 구조

- `problem/`: 레거시 원문과 제공 자산 위치
- `ts/`: diff/patch와 render pipeline 구현 자리
- `docs/`: render/commit reasoning 문서
- `notion/`: 로컬 전용 과정 로그

## Build/Test Command

```bash
cd study
npm run test --workspace @front-react/render-pipeline
npm run typecheck --workspace @front-react/render-pipeline
npm run verify --workspace @front-react/render-pipeline
```

검증 범위는 아래와 같다.

- `diffProps`, keyed/unkeyed child diff
- DOM patch create/remove/update ordering
- render phase와 commit phase 분리
- interrupted work 이후 일관된 commit 결과

## 다음 단계로 이어지는 한계

이 단계는 업데이트 파이프라인을 설명하지만, 함수 컴포넌트 상태와 effect, delegated event는 아직 없다. 그 축은 `03-hooks-and-events`로 이어진다.
