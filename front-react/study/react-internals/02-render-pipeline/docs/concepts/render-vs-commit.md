# Render Vs Commit

`01-vdom-foundations`는 새 VNode tree를 바로 DOM으로 재귀 렌더한다. 반면 `02-render-pipeline`은 두 단계를 분리한다.

## Render Phase

- 현재 tree와 다음 tree를 비교한다.
- patch 또는 work unit을 계산한다.
- 이 단계에서는 DOM을 바꾸지 않는다.

테스트에서 `render()` 직후 container가 비어 있는 이유가 바로 이 경계다.

## Commit Phase

- 계산이 끝난 뒤에만 DOM mutation을 적용한다.
- `PLACEMENT`, `UPDATE`, `DELETION` effect를 실제 노드에 반영한다.

## 왜 중요한가

- 계산과 반영을 분리하면 테스트 포인트가 선명해진다.
- interrupted work를 실험해도 partial DOM commit을 막을 수 있다.
- 다음 단계에서 hook state, effect, delegated event를 같은 runtime 흐름에 얹기 쉬워진다.
