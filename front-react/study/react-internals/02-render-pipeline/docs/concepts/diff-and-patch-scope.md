# Diff And Patch Scope

`02-render-pipeline`의 핵심은 React 전체 reconciliation을 복제하는 것이 아니라, "업데이트 파이프라인이 왜 필요한가"를 선명하게 보여 주는 최소 규칙을 만드는 데 있다.

## 포함한 범위

- prop 변경과 제거 계산
- keyed / unkeyed child 비교
- create / remove / replace / update patch
- patch ordering에 따른 DOM 반영

## 의도적으로 뺀 범위

- keyed reorder를 완전히 최적화하는 알고리즘
- priority lanes
- concurrent rendering semantics 전체
- class component lifecycle

## 이유

이 단계에서 중요한 것은 patch의 종류를 많이 늘리는 것이 아니라, render 단계에서 변경 집합을 만들고 commit 단계에서만 DOM을 바꾼다는 mental model을 만드는 것이다. 범위를 넓히면 코드량은 늘지만 학습 포인트는 흐려진다.
