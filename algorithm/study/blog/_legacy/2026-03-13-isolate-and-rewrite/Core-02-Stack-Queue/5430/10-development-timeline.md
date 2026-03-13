# BOJ 5430 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 함수 R(뒤집기)과 D(첫 번째 원소 삭제)를 문자열로 받아 배열에 적용하는 방법을 정한다.
- 진행: 처음엔 R이 올 때마다 배열을 진짜로 뒤집으려 했다. 그런데 함수 문자열이 최대 10만 자이고, 매번 reverse를 하면 O(n)이 반복되니까 전체가 O(n²)이 된다.
- 이슈: 진짜로 뒤집지 않고, "지금 뒤집혀 있는 상태인가?"를 플래그로 관리하면 R이 O(1)이 된다.
- 판단: `is_reversed` 플래그를 두고, D 연산 때 플래그 상태에 따라 앞에서 빼거나 뒤에서 뺀다. deque를 쓰면 양끝 제거가 O(1)이다. 이 lazy evaluation 아이디어가 핵심이었다.

### Session 2
- 목표: 입력 파싱과 lazy evaluation을 구현한다.
- 진행: 배열 입력이 `[1,2,3,4]` 형태의 문자열이라 파싱이 좀 까다롭다. 빈 배열 `[]`과 n=0 케이스를 따로 처리해야 했다.

이 시점의 핵심 코드:

```python
is_reversed = False
for cmd in p:
    if cmd == 'R':
        is_reversed = not is_reversed
    elif cmd == 'D':
        if not dq:
            error = True
            break
        if is_reversed:
            dq.pop()
        else:
            dq.popleft()
```

처음엔 `is_reversed`가 True일 때 D를 어디서 빼야 하는지 헷갈렸다. 논리적으로 "뒤집힌 상태에서 첫 번째 원소"는 원래 배열의 마지막이니까 `pop()`이 맞다.

CLI:

```bash
$ make -C study/Core-02-Stack-Queue/5430/problem run-py
```

```text
[2,1]
error
```

- 다음: 빈 배열에서 D를 호출하면 error를 출력하는 조건을 꼼꼼히 처리한다.
