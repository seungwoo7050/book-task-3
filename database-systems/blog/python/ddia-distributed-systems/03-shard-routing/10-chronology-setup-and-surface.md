# 10 hash mod 가 아니라 이동 비용을 보는 라우팅

## Day 1
### Session 1

처음엔 shard routing을 `hash(key) % N`으로 생각했다. 그런데 코드에는 ring과 virtual node가 먼저 나온다.

```python
class Ring:
    def __init__(self, virtual_nodes: int = 150) -> None:
        self.virtual_nodes = virtual_nodes or 150
        self.ring: list[RingEntry] = []
        self._nodes: set[str] = set()
```

핵심 질문도 달라진다. "어디로 라우팅하나"뿐 아니라 "멤버십 변경 시 몇 개나 옮기나"까지 포함된다.

- 목표: 분산도와 재배치 비용을 동시에 관찰하는 라우팅 구조 파악
- 진행: `node_for_key`, `assignments`, `moved_keys`를 우선 확인

CLI:

```bash
cd python/ddia-distributed-systems/projects/03-shard-routing
grep -n "def test_" tests/test_shard_routing.py
```

```text
4:def test_empty_and_single_node_routing():
11:def test_distribution_and_rebalance():
35:def test_batch_routing():
```

`test_distribution_and_rebalance`가 바로 이 슬롯의 주제다.

다음 질문:

- key hash에서 ring entry를 찾는 알고리즘은 어떻게 구현되나
- node 추가/제거 시 이동량은 어떻게 측정하나
