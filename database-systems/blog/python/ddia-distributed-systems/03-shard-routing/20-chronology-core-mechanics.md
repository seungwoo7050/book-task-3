# 20 Core Mechanics

## Day 1
### Session 2

라우팅 본체는 `bisect` 한 번이다.

```python
target = hash_value(key)
hashes = [entry.hash_value for entry in self.ring]
index = bisect.bisect_left(hashes, target)
if index == len(self.ring):
    index = 0
return self.ring[index].node_id, True
```

target 이상 첫 entry를 찾고, 끝까지 가면 0으로 wrap-around 한다. consistent hashing ring의 최소 구현이다.

다음은 이동량 계산.

```python
current = self.assignments(keys)
return sum(1 for key in keys if previous.get(key) and previous[key] != current.get(key))
```

node 추가 전/후 assignment를 비교해 reassigned key 개수를 센다.

- 목표: ring lookup과 rebalance accounting이 어떻게 결합되는지 확인
- 진행: `test_distribution_and_rebalance` 대조

CLI:

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
sed -n '1,140p' src/shard_routing/core.py
sed -n '11,40p' tests/test_shard_routing.py
```

### Session 3

`Router.route_batch()`는 이후 capstone을 위한 다리 역할을 한다.

```python
grouped.setdefault(node_id, []).append(key)
```

node별 키 묶음을 한 번에 얻을 수 있어서, shard별 write pipeline으로 쉽게 연결된다.

다음 질문:

- static ring을 dynamic membership protocol로 확장하려면 어떤 상태가 더 필요할까
- replica group 개념이 붙으면 node 대신 shard group을 반환해야 하나