# BOJ 2164 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case를 점검한다.
- 진행: N=1이면 루프 조건 `len(q) > 1`이 False라서 바로 `q[0] = 1`을 출력한다. N=2이면 1을 버리고 2가 맨 밑으로 갔다가(하나뿐이라) 남는다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-02-Stack-Queue/2164/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제는 deque의 존재 이유를 보여주는 가장 단순한 예제다.
  - 문제 자체는 쉽지만, "리스트 vs deque"의 시간 복잡도 차이를 체감하는 데 가치가 있다.
  - 수학적으로는 요세푸스 문제와 비슷한 구조다. N이 작았다면 2의 거듭제곱 패턴으로 공식을 쓸 수도 있다.
