# BOJ 2170 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case 점검 — 모든 구간이 겹치는 경우, 완전히 포함되는 구간.
- 진행: 구간 `(1, 5)`와 `(2, 3)`처럼 하나가 다른 것에 완전히 포함되는 경우, `max(cur_end, e)`에서 cur_end가 이미 더 크니까 자동으로 처리된다.
- 이슈: 정렬 기준이 `(시작, 끝)` 튜플 기본 정렬이라 시작이 같으면 끝이 작은 게 먼저 온다. 하지만 어차피 병합 로직에서 max를 쓰니까 순서가 바뀌어도 결과는 같다.

### Session 4
- 검증: C++ 구현은 pair<int,int> 정렬 + 같은 sweep 로직.

CLI:

```bash
$ make -C study/Core-06-Sorting/2170/problem run-cpp
$ make -C study/Core-06-Sorting/2170/problem test
```

```text
5
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - interval merge 패턴은 정렬 한 번 + 선형 순회 한 번으로 O(N log N)이다.
  - 가장 실수하기 쉬운 지점은 마지막 구간을 루프 밖에서 따로 더하는 것이다.
  - "좌표가 너무 크면 배열을 못 쓴다"는 직관이 정렬 기반 접근으로 이끌었다. 좌표 압축과 다른 방향의 해결이다.
