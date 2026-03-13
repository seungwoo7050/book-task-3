# BOJ 5397 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 키로거 문제를 읽고, 커서 이동이 포함된 문자열 편집을 어떻게 시뮬레이션할지 정한다.
- 진행: 처음엔 단순히 문자열 하나에 `insert`를 쓰면 되지 않나 생각했다. 그런데 커서가 `<`, `>`로 움직이고 `-`로 삭제까지 들어오면, 매번 중간 삽입/삭제가 일어나서 리스트로는 O(L²)이 된다.
- 이슈: 입력 길이가 최대 100만이라 O(L²)은 시간 초과가 확실하다.
- 판단: 커서를 기준으로 왼쪽/오른쪽을 두 개의 스택으로 나누면, 모든 연산이 push/pop으로 O(1)이 된다. 이 아이디어가 전환점이었다.

### Session 2
- 목표: 두 스택 모델을 코드로 구현한다.
- 진행: `left` 스택은 커서 왼쪽 문자들, `right` 스택은 커서 오른쪽 문자들을 역순으로 보관한다. `<`이면 left에서 pop해서 right에 push, `>`이면 반대, `-`이면 left에서 pop, 일반 문자면 left에 push.

이 시점의 핵심 코드:

```python
for ch in keys:
    if ch == '<':
        if left:
            right.append(left.pop())
    elif ch == '>':
        if right:
            left.append(right.pop())
    elif ch == '-':
        if left:
            left.pop()
    else:
        left.append(ch)
```

처음엔 `right`를 역순으로 보관한다는 게 직관적이지 않았다. 하지만 이렇게 하면 `>`를 눌렀을 때 right에서 pop하면 바로 커서 바로 오른쪽 문자가 나온다. 나중에 결합할 때만 `reversed(right)`로 뒤집으면 된다.

CLI:

```bash
$ make -C study/Core-01-Array-List/5397/problem run-py
```

```text
ABCD
CDYX
```

- 이슈: 빈 스택에서 pop하는 경우를 놓칠 뻔했다. `if left:` 가드를 넣지 않으면 `<`가 맨 앞에서 눌렸을 때 에러가 난다.
- 다음: 테스트 케이스가 여러 개 들어오는 구조이므로 케이스 간 상태 초기화를 빠뜨리지 않았는지 점검한다.
