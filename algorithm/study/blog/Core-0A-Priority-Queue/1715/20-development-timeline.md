# BOJ 1715 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case 점검.
- 진행: N=1이면 `while len(heap) > 1` 조건에 안 들어가서 total=0을 출력한다. 정상.
- 이슈: 모든 묶음 크기가 같으면? 어떤 순서로 합쳐도 같은가? 아니다 — 크기가 같아도 가장 작은 둘을 먼저 합치는 게 (최소한 같거나) 유리하다. 이유는 작은 값이 깊은 레벨에 오래 남으면 누적이 적기 때문이다.

### Session 4
- 검증: C++ 구현도 priority_queue(min-heap) 기반 같은 전략.

CLI:

```bash
$ make -C study/Core-0A-Priority-Queue/1715/problem run-cpp
$ make -C study/Core-0A-Priority-Queue/1715/problem test
```

```text
100
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Huffman 원리를 직접 적용하는 문제였다. 처음엔 "합친 결과를 다시 힙에 넣는다"는 발상이 낯설었다.
  - Greedy 선택의 근거는 "빈도가 낮은(작은) 것을 깊이 묻으면 전체 비용이 줄어든다"는 것이다.
  - priority_queue가 왜 필요한지 체감한 문제다. 매번 최솟값 두 개를 O(log N)에 뽑아야 하니까, 정렬만으로는 합친 결과를 다시 정렬된 위치에 넣기 어렵다.
