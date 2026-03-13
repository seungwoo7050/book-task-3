# 키로거: 검증, edge case, 마지막 설명 축

이제는 구현을 끝냈다고 말하는 단계가 아니라, 어떤 근거로 끝났다고 말할 수 있는지를 정리하는 단계다. 테스트 루프와 마지막 설명 축이 여기서 닫힌다.

## 구현 순서 요약

- `make -C study/Core-01-Array-List/5397/problem test`로 fixture 전체를 다시 돌린다.
- `docs/references/approach.md`의 실수 포인트를 코드 분기와 연결한다.
- `Keylogger & Cursor Simulation — Concept & Background`와 `cpp/src/solution.cpp`를 붙여 마지막 판단 기준을 고정한다.

## Phase 3
### Session 3

- 당시 목표: 한두 개 입력이 맞는 수준을 넘어서 fixture 전체를 통과하는 구조로 묶는다.
- 변경 단위: `problem/script/test.sh`, `docs/references/approach.md`, `docs/concepts/edge-cases.md`
- 처음 가설: 실수 포인트를 문장으로만 남기면 다시 틀리기 쉽고, 테스트 루프와 함께 봐야 실제 방어선이 보인다.
- 실제 조치: `test.sh`의 PASS/FAIL 루프와 `approach.md`의 실수 체크리스트를 나란히 읽으며, 어떤 분기가 어디를 막는지 다시 맞췄다.

CLI 1:

```bash
$ make -C study/Core-01-Array-List/5397/problem test
```

검증 신호:

- `Test 1: PASS`, `Results: 1/1 passed, 0 failed` 순서로 출력됐다.
- 이번 단계에서 특히 다시 확인한 실수 포인트는 아래 셋이었다.

- <, >, - 처리 우선순위 혼동
- 케이스 간 상태 초기화 누락
- 빈 버퍼에서 삭제 시 예외 처리 누락

핵심 코드 1:

```python
    for _ in range(t):
        keys = input().strip()
        left = []   # 커서 왼쪽 문자들
        right = []  # 커서 오른쪽 문자들(역순 보관)

        for ch in keys:
            if ch == '<':
                if left:
                    right.append(left.pop())
            elif ch == '>':
```

왜 이 코드가 중요했는가:

이 코드는 정답을 만드는 줄이면서 동시에 체크리스트를 만족시키는 줄이다. 그래서 `approach.md`의 실수 포인트와 가장 잘 연결된다.

새로 배운 것:

- 테스트를 다시 읽는 순간, “맞았다”보다 “어디서 안 틀리는가”를 더 분명하게 설명할 수 있었다.

다음:

- 마지막으로 개념 문서와 코드가 어느 지점에서 맞물리는지 정리한다.

## Phase 4
### Session 4

- 당시 목표: `Keylogger & Cursor Simulation — Concept & Background`를 실제 코드와 연결해 마지막 설명 축을 세운다.
- 변경 단위: `cpp/src/solution.cpp`, `docs/concepts/*.md`, `python/src/solution.py`
- 처음 가설: 마지막 글에서 남겨야 할 것은 추상 개념이 아니라, 그 개념이 꼭 필요해진 줄이다.
- 실제 조치: Python과 C++ 구현을 나란히 읽으며 같은 전이가 유지되는지 확인했다.

CLI 2:

```bash
$ make -C study/Core-01-Array-List/5397/problem run-cpp
```

검증 신호:

- `BAPC`, `ThIsIsS3662` 순서로 출력됐다.
- 설명용 문서가 아니라 실제 실행 결과와 같은 답이 나온다는 점이 마지막 확인 포인트였다.

핵심 코드 2:

```cpp
    while (t--) {
        string keys;
        cin >> keys;

        list<char> editor;
        auto cursor = editor.end();

        for (char ch : keys) {
            if (ch == '<') {
                if (cursor != editor.begin()) --cursor;
```

왜 이 코드가 중요했는가:

이 블록 덕분에 개념 정리가 공중에 뜨지 않는다. `<, >, - 처리 우선순위 혼동`를 막는 방식과 `키 입력 문자열을 좌/우 버퍼로 시뮬레이션하는 keylogger 처리`가 여기서 한 번에 맞물린다.

핵심 코드 3:

```python
        # 합치기: left 스택 + 뒤집힌 right 스택
        sys.stdout.write(''.join(left) + ''.join(reversed(right)) + '\n')

if __name__ == "__main__":
    solve()
```

왜 이 코드가 중요했는가:

끝을 어떻게 닫느냐가 생각보다 중요했다. `키로거`에서는 마지막 출력 정리가 구현의 완성도를 가장 직접적으로 드러냈다.

새로 배운 것:

- C++ 쪽까지 다시 확인하고 나니, 이 문제에서 중요한 건 표현 방식이 아니라 `키 입력 문자열을 좌/우 버퍼로 시뮬레이션하는 keylogger 처리`를 끝까지 보존하는 전이 순서라는 점이었다.
- 그래서 `Core-01-Array-List`의 질문인 `순차 자료구조 선택이 편집과 이동 비용을 어떻게 바꾸는가?`도 결과 요약이 아니라, 상태와 순서를 어떻게 붙잡는가의 문제로 읽히게 됐다.

다음:

- 이 시리즈는 여기서 닫히지만, 다음 문제를 읽을 때도 `문제 계약 -> 첫 상태 -> fixture 검증` 순서를 그대로 재사용할 수 있다.
