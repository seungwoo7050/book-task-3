# Core Invariants

## 1. offset는 log identity이자 replay 경계다

[`ReplicationLog.append()`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py)는 새 offset을 `len(self.entries)`로 정한다. 별도 sequence generator나 wall clock이 없다. 그래서 이 랩의 ordering은 "리스트에 append된 순서" 자체다.

테스트 [`test_replication_log_assigns_sequential_offsets()`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py)는 `0`, `1`이 순서대로 붙는지만 확인한다. 겉보기엔 작은 assert지만, follower가 offset을 replay 경계로 사용하기 때문에 이 순차성은 나중에 idempotency의 바닥이 된다.

## 2. follower watermark는 "어디까지 적용했는가"만 기억한다

Follower는 전체 log를 저장하지 않는다. 대신 `last_applied_offset` 하나만 들고 있다.

```python
def watermark(self) -> int:
    return self.last_applied_offset
```

이 값은 `replicate_once()`에서 다음 fetch 시작점을 정할 때 사용된다.

```python
entries = leader.log_from(follower.watermark() + 1)
```

즉, follower의 state machine은 "leader log의 전체 복사본"이 아니라 "현재 key-value state + 마지막으로 본 offset"으로 요약된다. 이게 이 랩이 설명하려는 watermark 기반 incremental sync의 핵심이다.

## 3. idempotent apply는 중복 batch를 skip하는 것으로 만든다

`Follower.apply()`의 가장 중요한 줄은 아래 조건이다.

```python
if entry.offset <= self.last_applied_offset:
    continue
```

이 조건 때문에 follower는 이미 본 offset 이하의 entry를 다시 받더라도 건너뛴다. 2026-03-14에 추가로 아래 snippet을 실행했다.

```python
initial_apply 2 1 {'a': '1', 'b': '2'}
duplicate_apply 0 1 {'a': '1', 'b': '2'}
incremental_apply 2 3 {'b': '3'}
replay_batch 0 3 {'b': '3'}
```

여기서 중요한 건 `duplicate_apply`와 `replay_batch`가 둘 다 `0`을 돌려준다는 점이다. follower는 같은 entry를 다시 해석해 state를 덮어쓰지 않는다. 이미 watermark가 앞서 있으면 배치 전체가 무효화된다. docs의 [`idempotent-follower.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/idempotent-follower.md)가 말하는 "same batch replay is safe"가 바로 이 분기로 구현된다.

## 4. delete도 특별 취급하지 않고 같은 stream에 태운다

`delete`는 별도 tombstone log 타입이 아니라 `operation="delete", value=None`인 일반 entry다. follower는 아래 한 줄로 이를 처리한다.

```python
if entry.operation == "delete":
    self.store.pop(entry.key, None)
```

즉, 이 랩에서 복제는 "state snapshot 복사"가 아니라 "ordered mutation replay"라는 사실이 delete에서 더 분명해진다. leader가 `a`를 지운 뒤 follower가 그 mutation을 같은 offset stream에서 받아서 적용하면 된다.

## 5. 소스만 읽으면 보이는 추가 경계

테스트가 직접 잡지 않지만 소스상 분명한 사실도 있다.

- `Follower.apply()`는 unknown `operation`을 만나도 예외를 던지지 않고 offset만 전진시킬 수 있다.
- `Leader.delete()`는 key가 없어도 `pop(..., None)` 뒤 delete entry를 남긴다.
- `ReplicationLog.from_offset()`는 음수 offset이 오면 `max(offset, 0)`으로 보정한다.

이 셋은 production-safe validation이라기보다, 이번 랩이 "ordered log와 incremental replay" 설명에 필요한 최소 semantics만 남겨 둔 결과다.
