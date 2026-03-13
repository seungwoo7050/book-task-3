# BOJ 5397 — 개발 타임라인 (후반)

## Phase 2
### Session 3
- 목표: 출력 조합 방식을 확정하고 C++ 비교 구현을 점검한다.
- 진행: 최종 문자열은 `''.join(left) + ''.join(reversed(right))`로 만든다. `sys.stdout.write`로 출력해서 I/O 비용을 줄였다.
- 이슈: 처음에 `print`를 써서 각 케이스마다 flush가 일어났는데, 케이스 수가 많으면 느려진다.

### Session 4
- 진행: C++ 구현도 같은 두 스택 모델이다. `std::string`을 두 개 쓰고 최종에 합친다.
- 검증: 동일 fixture에서 같은 출력을 확인했다.

CLI:

```bash
$ make -C study/Core-01-Array-List/5397/problem run-py
$ make -C study/Core-01-Array-List/5397/problem run-cpp
$ make -C study/Core-01-Array-List/5397/problem test
```

```text
Test 1: PASS
Results: 1/1 passed, 0 failed
```

### Session 5
- 정리:
  - 이 문제의 핵심은 자료구조 선택이었다. 커서가 있는 문자열 편집에서 "왼쪽 스택 + 오른쪽 스택"이라는 모델을 떠올리기까지가 가장 어려웠다.
  - 처음엔 리스트 중간 삽입으로 생각했는데, 비용 모델을 따져보니 바로 탈락이었다.
  - `right` 스택의 역순 보관 규칙을 머릿속에 고정하고 나면, 나머지는 조건 분기를 빠짐없이 쓰기만 하면 된다.
  - 에디터(1406)와 이 문제가 거의 같은 구조라는 걸 나중에 알았다.
