# Core Invariants

## 1. placement는 sha256 첫 8바이트 정수 위에서 결정된다

[`hash_value()`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py)는 문자열을 SHA-256으로 해시한 뒤 앞 8바이트를 big-endian 정수로 바꾼다.

```python
return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")
```

즉 이 랩의 consistent hashing은 "언어 런타임 기본 hash"가 아니라 프로세스 간에도 재현 가능한 crypto hash 기반 deterministic mapping 위에 서 있다.

## 2. lookup은 lower bound 검색과 wrap-around로 끝난다

`node_for_key()`는 target hash보다 크거나 같은 첫 ring entry를 `bisect_left`로 찾는다. 끝을 넘으면 `index = 0`으로 감아 돌아간다.

```python
index = bisect.bisect_left(hashes, target)
if index == len(self.ring):
    index = 0
```

이 두 줄이 consistent hash ring의 핵심이다. empty ring이면 `("", False)`를 반환하고, ring이 비어 있지 않으면 항상 어떤 node 하나를 돌려준다. 수동 재실행에서도 `empty ('', False)`를 확인했다.

## 3. duplicate add와 remove는 membership set으로 흡수한다

`Ring`은 `_nodes: set[str]`를 따로 유지한다. 그래서 이미 있는 node를 다시 `add_node()`해도 즉시 return하고, 없는 node를 `remove_node()`해도 `discard()`로 조용히 넘긴다. 이 설계 덕분에 membership 연산이 idempotent하다. 다만 version이나 epoch는 없다. 즉 "누가 최신 membership을 말하고 있는가"를 판단하는 분산 제어면은 아직 존재하지 않는다.

## 4. moved key 계산은 이전 assignment와 현재 assignment의 차이만 센다

`moved_keys()`는 이전 assignment map과 현재 ring에서 다시 계산한 assignment를 비교해, 값이 달라진 key 수를 센다.

```python
current = self.assignments(keys)
return sum(1 for key in keys if previous.get(key) and previous[key] != current.get(key))
```

이 함수는 data movement를 수행하지 않는다. 대신 "이 membership change가 대략 얼마나 비싼가"를 정량화한다. docs의 [`rebalance-accounting.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/rebalance-accounting.md)가 말하는 핵심이 바로 이 비교다.

2026-03-14 수동 실행에서는 1000개 key 기준으로 node-d 추가 후 아래 결과가 나왔다.

```python
moved_after_add 237
```

즉 전체의 23.7%만 이동했다. consistent hashing의 장점이 "절반 이하만 움직인다"는 테스트 조건으로 실제 수치화된 셈이다.

## 5. batch routing은 분산도보다 전송 단위를 위해 존재한다

`Router.route_batch()`는 각 key를 조회한 뒤 node별 배열로 묶는다.

```python
grouped.setdefault(node_id, []).append(key)
```

이 결과 shape는 demo 출력에서도 확인됐다.

```python
{'node-a': ['k1', 'k3', 'k4'], 'node-b': ['k2']}
```

즉 이 랩에서 batch routing의 목적은 "대량 key를 더 빨리 계산한다"가 아니라, "같은 node로 갈 요청을 한 번에 묶는다"는 downstream-friendly shape에 있다.
