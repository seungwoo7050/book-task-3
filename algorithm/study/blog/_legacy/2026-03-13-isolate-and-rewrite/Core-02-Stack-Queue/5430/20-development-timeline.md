# BOJ 5430 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 출력 형식을 확정하고 edge case를 점검한다.
- 진행: 출력할 때 `is_reversed`가 True면 deque를 한 번 뒤집어서 출력해야 한다. `[` + 쉼표로 join + `]` 형식이다.
- 이슈: n=0이면서 D가 없는 경우, 빈 배열 `[]`을 정상 출력해야 한다. 이걸 error로 처리하면 틀린다.
- 판단: "빈 배열 + R만" → `[]` 정상 출력, "빈 배열 + D" → error.

### Session 4
- 진행: C++ 구현도 같은 lazy reverse + deque 전략이다. 파싱 부분만 stringstream으로 처리했다.
- 검증: 두 구현 모두 동일 fixture 통과.

CLI:

```bash
$ make -C study/Core-02-Stack-Queue/5430/problem run-cpp
$ make -C study/Core-02-Stack-Queue/5430/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제의 핵심 전환점은 "R을 실제로 실행하지 않는다"는 판단이었다. 처음엔 당연히 뒤집어야 한다고 생각했는데, 플래그 하나로 방향만 기억하면 된다는 걸 깨닫는 데 시간이 걸렸다.
  - 입력 파싱이 생각보다 까다로웠다. `[1,2,3,4]` 문자열에서 대괄호를 벗기고 쉼표로 split하는 것, n=0일 때 빈 문자열 처리가 실수하기 쉬운 지점이다.
  - "lazy evaluation"이라는 단어를 알고 있었지만, 이 문제에서 직접 써보니 왜 유용한지 체감이 됐다.
