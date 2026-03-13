# BOJ 1181 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: edge case를 확인한다.
- 진행: 문제 조건상 단어 길이가 1 이상이라 빈 문자열은 없다. N=1이면 입력 하나를 그대로 출력.
- 이슈: `input().strip()` 대신 `input()`만 쓰면 줄바꿈 문자가 포함되어 정렬이 깨진다. strip은 필수다.

### Session 4
- 검증: fixture 통과.

CLI:

```bash
$ make -C study/Core-06-Sorting/1181/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - Python의 tuple 비교와 sorted의 key 함수를 합치면 복합 정렬이 매우 간결하다.
  - set으로 중복을 먼저 없애는 게 정렬 후 순회하며 제거하는 것보다 코드가 깔끔하다.
  - 이 문제는 정렬보다 "문제를 코드로 옮기는 변환의 정확성"이 핵심이다.
