# 20 Core Mechanics

## Day 1
### Session 2

`Follower.apply()`에서 가장 중요한 줄은 아래 조건이다.

```python
if entry.offset <= self.last_applied_offset:
    continue
```

이 조건 하나로 idempotency가 생긴다. 같은 로그 배치를 다시 받아도 이미 적용한 offset은 건너뛴다.

그리고 catch-up은 watermark 기반이다.

```python
def replicate_once(leader: Leader, follower: Follower) -> int:
    entries = leader.log_from(follower.watermark() + 1)
    return follower.apply(entries)
```

full sync가 아니라 "내 watermark 이후"만 가져온다.

- 목표: incremental + idempotent 복제 경계 확인
- 진행: `test_follower_apply_is_idempotent`, `test_replicate_once_incremental_and_deletes` 대조

CLI:

```bash
cd python/ddia-distributed-systems/projects/02-leader-follower-replication
sed -n '1,140p' src/leader_follower/core.py
sed -n '10,60p' tests/test_replication.py
```

delete도 같은 로그 경로를 탄다.

- leader에서 `delete` append
- follower apply에서 `store.pop(key, None)`

즉 put/delete 모두 "동일한 ordered operation stream"으로 다룬다.

다음 질문:

- 리더 장애/선출이 없을 때 authority는 어디서 고정되는가
- shard가 생기면 watermark를 shard별로 분리해야 하나