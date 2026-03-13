# BOJ 1406 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case와 출력 성능을 점검한다.
- 진행: 빈 `left`에서 L이나 B가 오면 `if left:` 가드로 무시된다. 빈 `right`에서 D가 오면 무시.
- 이슈: 출력은 `''.join(left) + ''.join(reversed(right))`인데, 줄바꿈 포함해서 `print`로 한 번에 출력한다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-01-Array-List/1406/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제와 키로거(5397)는 사실상 같은 구조다. 두 스택 모델이 커서 기반 편집의 정석이라는 걸 두 문제를 통해 확인했다.
  - 처음엔 리스트 insert로 풀려다가 시간 초과를 예상하고 전략을 바꿨다. "O(1) 연산만으로 구성할 수 있는가"를 먼저 묻는 습관이 중요하다.
  - `cmd[2]` vs `cmd.split()[1]` — I/O 최적화가 생각보다 결과를 바꾼다.
