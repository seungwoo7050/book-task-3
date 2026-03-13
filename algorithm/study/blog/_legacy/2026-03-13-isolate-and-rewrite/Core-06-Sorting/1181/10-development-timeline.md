# BOJ 1181 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 단어를 길이 우선, 길이가 같으면 사전순으로 정렬하고, 중복은 제거한다.
- 진행: 처음엔 정렬만 하면 되겠다 싶었는데, 중복 제거를 언제 하느냐가 고민이었다. 정렬 전에 해도 되고 후에 해도 되지만, set으로 먼저 중복을 없애는 게 정렬할 원소 수를 줄여서 효율적이다.
- 판단: `set`으로 중복 제거 → `sorted`에 `(len(w), w)` 키 사용.

### Session 2
- 목표: 구현을 완성한다.

이 시점의 핵심 코드:

```python
words = set(input().strip() for _ in range(N))
result = sorted(words, key=lambda w: (len(w), w))
```

두 줄이 전부다. Python의 tuple 비교가 첫 번째 원소 우선, 같으면 두 번째 원소로 넘어가니까 `(len(w), w)` 하나로 복합 정렬이 완성된다.

CLI:

```bash
$ make -C study/Core-06-Sorting/1181/problem run-py
```

```text
i
im
it
no
...
```

- 다음: 빈 문자열이 입력으로 올 수 있는지 문제 조건을 확인한다.
