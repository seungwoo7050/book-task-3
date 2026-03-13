# BOJ 10816 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N장의 카드가 있을 때, M개의 질의 각각에 대해 해당 숫자가 몇 장 있는지 출력한다.
- 진행: 처음엔 매 질의마다 리스트를 순회해서 count하려 했다. O(NM)이니까 N, M이 각각 50만이면 2500억 연산... 당연히 안 된다.
- 이슈: Counter(해시맵)를 쓰면 전처리 O(N), 질의당 O(1)로 전체 O(N+M)이 된다.
- 판단: `collections.Counter`를 사용한다.

### Session 2
- 목표: Counter 기반 구현을 완성한다.

이 시점의 핵심 코드:

```python
cnt = Counter(cards)
print(' '.join(str(cnt[q]) for q in queries))
```

Counter에 없는 키를 조회하면 0을 반환하니까 별도 예외 처리가 필요 없다. 처음엔 `cnt.get(q, 0)`을 썼는데, Counter는 기본값이 0이라 그냥 `cnt[q]`로 충분하다.

CLI:

```bash
$ make -C study/Core-07-Binary-Search-Hash/10816/problem run-py
```

```text
3 0 0 1 2 0 0 2
```

- 다음: I/O가 느리면 시간 초과가 날 수 있으니 `sys.stdin.readline`을 쓰고 있는지 확인한다.
