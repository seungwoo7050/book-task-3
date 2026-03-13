# 10 상태 복사가 아니라 로그 재생으로 보기

## Day 1
### Session 1

처음엔 follower 동기화를 "leader state 전체 복사"로 상상했다. 그런데 코드 첫 구조가 그 가정을 깨준다.

```python
@dataclass(slots=True)
class LogEntry:
    offset: int
    operation: str
    key: str
    value: str | None
```

복제 단위는 state snapshot이 아니라 ordered log entry다.

- 목표: replication 핵심이 state copy인지 log shipping인지 확인
- 진행: `ReplicationLog`, `Leader.put/delete`, `Follower.apply` 순서로 읽음

CLI:

```bash
cd python/ddia-distributed-systems/projects/02-leader-follower-replication
grep -n "def test_" tests/test_replication.py
```

```text
4:def test_replication_log_assigns_sequential_offsets():
10:def test_follower_apply_is_idempotent():
24:def test_replicate_once_incremental_and_deletes():
```

테스트가 강조하는 것도 offset 순서, idempotent apply, incremental catch-up이다.

다음 질문:

- follower는 어디까지 적용했는지 어떤 값으로 기억하나
- duplicate entry를 다시 받았을 때 상태를 어떻게 지키나
