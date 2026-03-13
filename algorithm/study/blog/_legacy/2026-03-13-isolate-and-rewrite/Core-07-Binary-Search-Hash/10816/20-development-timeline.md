# BOJ 10816 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: I/O 최적화와 edge case를 점검한다.
- 진행: `sys.stdin.readline`을 입력에 사용하고, 출력은 한 줄로 join해서 한 번에 출력한다.
- 이슈: N=0인 경우는 문제 조건상 없지만, 쿼리에 나오는 숫자가 카드에 전혀 없으면 전부 0으로 출력된다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-07-Binary-Search-Hash/10816/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제는 해시맵(Counter)이 왜 필요한지 보여주는 기본 예제다.
  - 이분 탐색(lower_bound/upper_bound)으로도 풀 수 있지만, Python에서는 Counter가 더 간결하고 빠르다.
  - "전처리 + O(1) 질의" 패턴은 여러 변형 문제에서 반복된다.
