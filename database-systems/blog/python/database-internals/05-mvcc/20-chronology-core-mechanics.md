# 20 Core Mechanics

## Day 1
### Session 3

visibility 핵심은 `get_visible()` 한 함수에 모여 있다.

```python
for version in self.store.get(key, []):
    if version.tx_id <= snapshot and committed.get(version.tx_id, False):
        return Version(version.value, version.tx_id, version.deleted)
```

체인 순회 순서는 최신 tx_id부터고, 조건은 두 개다.

1. 내 snapshot 이하인가
2. commit 완료된 tx인가

둘 다 만족하는 첫 버전이 "내가 볼 수 있는 최신"이다.

- 목표: snapshot isolation read semantics를 코드와 테스트로 고정
- 진행: `test_snapshot_isolation` 대조

`read-your-own-write`도 따로 fast path가 있다.

```python
if key in tx.write_set:
    for version in self.version_store.store.get(key, []):
        if version.tx_id == tx_id:
            return None if version.deleted else version.value
```

같은 tx가 아직 commit하지 않은 write는 자기 자신에게는 보여야 한다.

### Session 4

충돌 검사는 commit 시점에 몰아둔다.

```python
if version.tx_id > tx.snapshot and version.tx_id != tx_id and self.committed.get(version.tx_id, False):
    self._abort_internal(tx_id, tx)
    raise ValueError(f'write-write conflict on key "{key}"')
```

first-committer-wins 모델이다. 시작 이후 다른 tx가 같은 key를 먼저 commit했다면 현재 tx는 abort된다.

CLI:

```bash
cd python/database-internals/projects/05-mvcc
sed -n '1,180p' src/mvcc_lab/core.py
sed -n '30,120p' tests/test_mvcc.py
```

다음 질문:

- long-running tx가 많을 때 gc 기준은 어떻게 잡히는가
- phantom 방지를 위해서는 key-level version chain 외에 무엇이 필요할까