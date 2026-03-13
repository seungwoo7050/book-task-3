# BOJ 15649 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 출력 최적화와 edge case를 점검한다.
- 진행: 출력을 리스트에 모아서 `'\n'.join(out)`으로 한 번에 쓰면 I/O가 빨라진다.
- 이슈: N=M이면 N!개의 완전 순열이 출력된다. N=1, M=1이면 "1" 하나만 출력.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-04-Recursion-Backtracking/15649/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제는 백트래킹의 가장 기본 형태다. "선택 → 재귀 → 해제"의 대칭 구조를 연습하기에 좋다.
  - `used` 배열 vs `in seq` 체크 — 둘 다 되지만 시간 복잡도가 다르다. 배열로 O(1) 체크하는 습관을 여기서 잡았다.
  - N-Queen(9663)은 이 패턴에 "대각선까지 체크"를 추가한 확장이다. 여기서 기본을 잡고 나서 9663으로 가면 자연스럽다.
