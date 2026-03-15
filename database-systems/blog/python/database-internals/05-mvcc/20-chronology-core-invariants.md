# 20 핵심 invariant 붙잡기: snapshot watermark, conflict cleanup, GC

이 슬롯의 코드는 길지 않지만, visibility semantics를 만드는 지점은 꽤 또렷하다. `VersionStore`는 version chain 자체를 들고 있고, `TransactionManager`는 그 chain 위에 snapshot, commit, abort, gc 규칙을 얹는다. 결국 중요한 건 값을 저장하는 일보다 어떤 tx_id가 어떤 version을 볼 수 있는가다.

## Phase 2-1. `begin()`이 transaction마다 snapshot watermark를 고정한다

`TransactionManager.begin()`은 새 tx_id를 발급한 뒤 `snapshot = max(self.committed, default=0)`를 잡는다. 즉 transaction이 시작할 때 보이는 committed horizon이 한 번 결정되면, 이후 다른 transaction이 더 최신 version을 commit해도 이 transaction의 snapshot은 바뀌지 않는다.

이 규칙 덕분에 `test_snapshot_isolation`이 성립한다. 이번 보조 재실행에서도 같은 흐름이 나왔다.

```text
snapshot_read v1
```

즉 `t2`가 시작한 뒤 `t3`가 `x = v2`를 commit해도, `t2`는 자기 snapshot 이하의 마지막 committed version인 `v1`만 본다.

## Phase 2-2. `read()`는 snapshot 규칙 위에 read-your-own-write 예외를 얹는다

`read()`는 먼저 transaction의 `write_set`을 확인한다. key가 거기 있으면 chain에서 `version.tx_id == tx_id`인 version을 찾아 바로 돌려준다. 이 한 단계 때문에 자기 자신의 uncommitted write는 snapshot 규칙과 상관없이 읽힌다.

그 다음에야 `version_store.get_visible(key, tx.snapshot, self.committed)`를 부른다. 즉 read path는 두 층이다.

1. 내 write set 우선
2. snapshot 이하 committed version

이 구조가 꽤 중요하다. read-your-own-write가 별도 격리 수준이 아니라, snapshot isolation 위에 얹는 특별 규칙이라는 사실이 코드로도 드러나기 때문이다.

## Phase 2-3. `commit()`은 first-committer-wins를 chain 순회로 구현한다

`commit()`은 write set의 각 key에 대해 version chain을 순회하면서,

- `version.tx_id > tx.snapshot`
- `version.tx_id != tx_id`
- `self.committed.get(version.tx_id, False)`

를 만족하는 version이 있으면 conflict로 본다. 즉 내 snapshot 이후에 같은 key를 다른 committed tx가 이미 썼다면 나는 commit할 수 없다.

중요한 건 실패할 때 그냥 에러만 던지지 않는다는 점이다. `_abort_internal()`을 먼저 불러서 내 tx가 만든 version들을 chain에서 제거한 뒤 `ValueError`를 던진다. 이번 보조 재실행에서도 이 cleanup이 그대로 보였다.

```text
conflict ValueError write-write conflict on key "y"
chain_after_conflict [(4, 'a', False)]
```

즉 conflict 후에는 loser transaction의 version이 chain에 남아 있지 않다.

## Phase 2-4. `gc()`는 active snapshot 아래의 옛 version을 거의 한 개만 남긴다

`gc()`도 현재 semantics를 정확히 읽어야 한다. `TransactionManager.gc()`는 active transaction 중 가장 작은 snapshot을 찾고, 없으면 `min_snapshot = self.next_tx_id`가 된다. 그 값을 `VersionStore.gc(min_snapshot)`에 넘기면, 각 key chain에서

- `tx_id >= min_snapshot`인 recent versions는 유지
- `tx_id < min_snapshot`인 old versions 중 첫 번째만 추가 유지

한다.

현재 chain은 newest-first 정렬이라, active snapshot이 없을 때 old bucket의 첫 번째는 사실상 최신 committed version 하나다. 이번 보조 재실행에서도 그 결과가 분명했다.

```text
before_gc [(3, 'v3', False), (2, 'v2', False), (1, 'v1', False)]
after_gc [(3, 'v3', False)]
```

즉 active reader가 없으면 chain이 거의 single-version state로 접힌다. README는 "stale version GC"라고 말하지만, 현재 구현은 꽤 aggressive하게 최신 one-version만 남길 수 있다.
