# Core Invariants

## 1. transaction snapshot은 "begin 시점 최대 committed tx id"다

`Begin()`은 현재 `Committed` map에서 가장 큰 tx id를 찾아 snapshot으로 저장한다.

```go
maxCommitted := 0
for id := range manager.Committed {
    if id > maxCommitted {
        maxCommitted = id
    }
}
```

즉 snapshot은 wall clock이 아니라 commit watermark다. docs의 [`snapshot-visibility.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/docs/concepts/snapshot-visibility.md)가 말하는 "시작 시점 committed watermark"가 그대로 구현된 셈이다.

## 2. read-your-own-write는 visible committed version보다 먼저 검사된다

`Read()`는 먼저 transaction의 `WriteSet`을 본다. 해당 key를 이 tx가 썼다면, version chain에서 자기 tx id와 일치하는 version을 찾아 곧바로 돌려준다.

즉 일반 visibility 규칙보다 read-your-own-write가 우선한다. 이 덕분에 아직 commit되지 않은 내 write도 같은 transaction 안에서는 보인다.

## 3. visible version은 snapshot 이하이면서 committed인 첫 version이다

`VersionStore.GetVisible()`는 chain을 앞에서부터 순회하며 아래 조건을 만족하는 첫 version을 반환한다.

- `version.TxID <= snapshot`
- `committed[version.TxID] == true`

그리고 chain은 `Append()` 시 tx id 내림차순 순서로 유지된다. 즉 가장 최신 version부터 보되, snapshot을 넘거나 아직 commit되지 않은 것은 건너뛴다.

## 4. first-committer-wins conflict는 commit 시 write set 기준으로 검사된다

`Commit()`은 자기 `WriteSet`의 각 key에 대해 version chain을 훑으며, snapshot 이후에 다른 committed tx가 같은 key를 썼는지 본다.

```go
if version.TxID > tx.Snapshot && version.TxID != txID && manager.Committed[version.TxID] {
    manager.abortInternal(txID, tx)
    return fmt.Errorf("write-write conflict on key %q", key)
}
```

즉 conflict detection은 write time이 아니라 commit time에 일어난다. 그리고 conflict가 나면 abort cleanup까지 즉시 수행한다.

## 5. GC는 active snapshot보다 오래된 version을 한 개만 남긴다

`GC()`는 모든 active tx 중 가장 작은 snapshot을 구하고, `VersionStore.GC(minSnapshot)`에 넘긴다. `VersionStore.GC()`는 `txID >= minSnapshot`인 recent versions는 유지하고, 더 오래된 old versions는 그중 첫 하나만 남긴다.

그래서 추가 재실행의 `gc_chain_len 1`처럼, 더 이상 어떤 active snapshot도 필요로 하지 않는 오래된 version들은 한 개 대표만 남기고 잘려 나갈 수 있다.

이 정책은 aggressive하지만 현재 lab 목적에는 맞다. MVCC semantics를 설명하면서도 version chain이 끝없이 길어지는 걸 막기 때문이다.
