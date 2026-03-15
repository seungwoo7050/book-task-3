# Core Invariants

## 1. offset는 append 순서 그 자체다

`ReplicationLog.Append()`는 새 offset을 `len(log.entries)`로 만든다.

```go
offset := len(log.entries)
log.entries = append(log.entries, LogEntry{Offset: offset, ...})
```

즉 별도 sequence allocator 없이 append 순서 자체가 ordering이다. 테스트 `TestReplicationLogAssignsSequentialOffsets`도 `0`, `1`이 순서대로 붙는지만 본다. 작지만 이 규칙이 watermark semantics의 바닥이다.

## 2. leader write는 local state를 먼저 바꾸고 그 뒤 log entry를 남긴다

`Leader.Put()`과 `Delete()`는 둘 다 store를 먼저 수정하고 이어서 log append를 수행한다.

```go
leader.store[key] = value
return leader.log.Append("put", key, stringPtr(value))
```

```go
delete(leader.store, key)
return leader.log.Append("delete", key, nil)
```

즉 leader 내부 contract는 "현재 state를 만든 mutation을 ordered log로 남긴다"는 것이다. durability나 quorum은 아직 없지만, 최소한 state와 log가 같은 mutation sequence를 공유한다.

## 3. follower는 `offset <= watermark`면 무조건 skip한다

`Follower.Apply()`의 핵심 분기는 아래다.

```go
if entry.Offset <= follower.lastAppliedOffset {
    continue
}
```

이 조건 때문에 duplicate replay는 무해하다. 추가 재실행의 `duplicate_apply 0 1`도 바로 이 규칙의 결과다. idempotency는 content hash가 아니라 monotonic watermark 비교에서 나온다.

## 4. delete는 ordinary mutation으로 replicated stream 안에 남는다

delete는 tombstone type이나 side channel이 아니라 `Operation = "delete"`인 일반 log entry다. follower는 switch 분기에서 이를 처리한다.

```go
case "delete":
    delete(follower.store, entry.Key)
```

즉 read model 관점에서는 key removal이지만, replication model 관점에서는 ordinary ordered mutation이다. docs의 [`log-shipping.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/log-shipping.md)가 말하는 "delete도 일반 mutation과 같은 방식으로 복제된다"는 문장이 그대로 구현된 것이다.

## 5. source-only nuance: unknown operation은 조용히 무시되면서 watermark는 올라갈 수 있다

`Follower.Apply()` switch에는 `put`, `delete`만 있고 default error가 없다. 즉 unknown operation이 들어오면 아무 데이터 변화 없이 `lastAppliedOffset`만 갱신될 수 있다. 테스트는 이 경계를 다루지 않지만, 현재 lab이 strict protocol validation보다 minimal replication semantics를 우선했다는 신호다.
