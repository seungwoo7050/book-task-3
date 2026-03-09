# BOJ 1715 — 디버깅 기록

## 함정 1: N=1일 때

**증상**: 묶음이 1개면 합칠 필요 없어서 답은 0

**원인**: `while len(heap) > 1` 조건이 자연스럽게 처리

## 함정 2: heapify vs 반복 push

`heapify`는 $O(N)$, 반복 `heappush`는 $O(N \log N)$. 성능 차이는 이 규모에서 무관하지만 습관적으로 `heapify` 사용.

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

PASS.
