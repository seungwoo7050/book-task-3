# BOJ 1931 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case를 점검한다.
- 진행: 길이 0인 회의 `(2,2)`, `(2,2)`가 두 개 있으면 둘 다 선택 가능하다. `start >= last_end` 조건에서 `>=`가 이를 허용한다.
- 이슈: N=1이면 무조건 답 1. 모든 회의가 겹치면 답 1.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-09-Greedy/1931/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Activity selection은 그리디의 교과서적 예제다. "종료 시간 기준 정렬"이라는 한 줄이 greedy choice property를 보장한다.
  - 정렬 키에 (종료, 시작)을 쓰는 건 길이 0 회의 때문이다. 처음에 이걸 빠뜨려서 한 번 틀렸다.
  - "짧은 회의 우선"이 왜 틀린지 반례를 직접 그려봐야 한다. `(1,5), (2,3), (4,5)` 같은 입력에서 확인된다.
