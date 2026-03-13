# BOJ 2164 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 1부터 N까지 카드가 쌓여 있을 때, "맨 위 버리기, 다음 카드 맨 밑으로" 반복해서 마지막 남는 카드를 구한다.
- 진행: 처음엔 이게 수학적 패턴이 있는지 고민했다. 그런데 N이 최대 50만이니까 시뮬레이션도 O(N)이면 충분하다.
- 이슈: 리스트로 시뮬레이션하면 앞에서 제거가 O(N)이라 전체 O(N²)이 된다. deque를 써야 O(1)이다.
- 판단: deque에 1~N을 넣고, popleft로 버리고, 다시 popleft한 걸 append하면 된다.

### Session 2
- 목표: deque 시뮬레이션을 구현한다.

이 시점의 핵심 코드:

```python
q = deque(range(1, n + 1))

while len(q) > 1:
    q.popleft()
    q.append(q.popleft())

print(q[0])
```

세 줄이 전부다. 처음엔 "이게 끝인가?" 싶었지만, deque의 popleft가 O(1)이기 때문에 전체 O(N)으로 끝난다. 리스트 pop(0)을 썼다면 동일 로직이지만 O(N²)이다.

CLI:

```bash
$ make -C study/Core-02-Stack-Queue/2164/problem run-py
```

```text
6
```

- 다음: N=1일 때 while 루프에 안 들어가고 1을 출력하는지 확인한다.
