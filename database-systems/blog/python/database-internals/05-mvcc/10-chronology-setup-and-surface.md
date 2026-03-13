# 10 MVCC 를 "최신값"이 아니라 "보이는 최신값"으로 보기

## Day 1
### Session 1

이 프로젝트를 보기 전에는 MVCC를 "버전 여러 개 보관" 정도로만 이해하고 있었다. 코드를 열면 바로 관점이 바뀐다.

```python
@dataclass(slots=True)
class Version:
    value: object
    tx_id: int
    deleted: bool
```

버전은 값만 있는 게 아니라 `tx_id`와 `deleted`까지 포함한다. 즉 read는 "가장 최신"을 고르는 게 아니라, "내 snapshot에서 유효한 최신"을 고르는 문제다.

- 목표: version chain + transaction snapshot이 함께 있어야 하는 이유 파악
- 진행: `TransactionManager.begin/read/write/commit`, `VersionStore.get_visible` 우선 확인

CLI:

```bash
cd python/database-internals/projects/05-mvcc
grep -n "def test_" tests/test_mvcc.py
```

```text
15:def test_snapshot_isolation():
40:def test_write_write_conflict():
85:def test_gc():
```

테스트 이름만으로도 scope가 보인다. visibility, conflict, gc까지 다룬다.

### Session 2

`begin()` 구현에서 snapshot이 어떻게 정해지는지 확인했다.

```python
snapshot = max(self.committed, default=0)
self.transactions[tx_id] = Transaction(snapshot=snapshot, status="active")
```

새 트랜잭션은 "시작 시점까지 커밋된 tx"를 기준으로 세계를 본다. 그래서 이후 커밋된 버전이 있어도 같은 트랜잭션 안에서는 바로 보이지 않을 수 있다.

다음 질문:

- read path에서 snapshot + committed 조건은 어떤 순서로 평가되나
- write-write conflict는 write 시점이 아니라 commit 시점에 왜 검사하나