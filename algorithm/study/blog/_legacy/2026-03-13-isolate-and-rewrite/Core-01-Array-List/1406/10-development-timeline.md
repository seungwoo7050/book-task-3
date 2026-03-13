# BOJ 1406 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 커서가 있는 에디터를 시뮬레이션한다. L, D, B, P 명령을 처리한다.
- 진행: 처음엔 문자열 하나에 커서 인덱스를 두고 `insert`, `delete`를 쓰려 했다. Python의 리스트 insert가 O(N)이라 M개 명령이면 O(NM)이 된다.
- 이슈: M이 최대 50만이고 문자열 길이도 최대 10만이니까 O(NM)은 너무 느리다. O(M) 또는 O(M log M)이 필요하다.
- 판단: 키로거(5397)와 같은 아이디어 — 커서 기준 좌/우 스택 두 개를 사용하면 모든 연산이 O(1)이다.

### Session 2
- 목표: 두 스택 모델을 구현한다.

이 시점의 핵심 코드:

```python
left = list(s)  # 초기 문자열이 커서 왼쪽에 전부 있다
right = []

for _ in range(m):
    cmd = input().strip()
    if cmd == 'L':
        if left:
            right.append(left.pop())
    elif cmd == 'D':
        if right:
            left.append(right.pop())
    elif cmd == 'B':
        if left:
            left.pop()
    elif cmd[0] == 'P':
        left.append(cmd[2])
```

키로거와 거의 같은 구조인데, 차이점은 초기 문자열이 이미 있다는 것과 명령어 형식이 다르다는 것이다. `P $` 명령에서 문자를 추출하는 `cmd[2]`를 처음엔 `cmd.split()[1]`로 써서 느렸다.

CLI:

```bash
$ make -C study/Core-01-Array-List/1406/problem run-py
```

```text
abcdyx
```

- 다음: 빈 스택에서 L, B 명령이 왔을 때 무시되는지 확인한다.
