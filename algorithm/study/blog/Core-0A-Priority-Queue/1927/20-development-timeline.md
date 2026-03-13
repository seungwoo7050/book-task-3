# BOJ 1927 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: I/O 최적화와 edge case를 점검한다.
- 진행: 출력을 리스트에 모아서 `'\n'.join`으로 한 번에 쓴다. 매번 print하는 것보다 훨씬 빠르다.
- 이슈: 연속으로 0이 들어오면 힙에서 순서대로 최솟값이 빠진다. 힙이 비면 0 출력.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-0A-Priority-Queue/1927/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제는 heapq의 기본 사용법을 익히는 입문 문제다.
  - Python의 heapq가 min-heap이라는 사실을 알면 바로 풀리지만, max-heap이 필요한 문제(11279)에서는 부호 반전이 필요하다.
  - I/O 최적화가 의외로 중요하다. 10만 번 print하면 시간 초과가 날 수 있다.
