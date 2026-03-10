# 디버그 포인트

이 파일은 “분산 흐름이 어디서 끊기는가”를 빠르게 재현하기 위한 메모입니다. 05번 문서의 핵심은 통합 경로이므로, 각 항목을 route, catch-up, restart 순서로 정리했습니다.

## 1. write가 잘못된 shard로 가는 경우
- 의심 파일: `../internal/capstone/capstone.go`
- 재현 명령:

```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run TestWriteRoutesToLeaderAndReplicates -v
go run ./cmd/clustered-kv
```

- 정상 기대: `key=alpha shard=shard-a follower=node-2 value=1 ok=true`
- 깨졌을 때 보이는 징후: shard가 예상과 다르거나, follower 읽기에서 `ok=false`가 나옵니다.
- 확인 테스트: `TestWriteRoutesToLeaderAndReplicates`
- 다시 볼 질문: `RouteShard(key)` -> `Group(shardID)` -> `Leader` 체인이 한 경로로만 연결되는가?

## 2. follower catch-up이 lag를 해소하지 못하는 경우
- 의심 파일: `../internal/capstone/capstone.go`, `../tests/capstone_test.go`
- 재현 명령:

```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run TestFollowerCatchUpAndDelete -v
```

- 정상 기대:
  - `SetAutoReplicate(false)` 뒤에는 follower가 lagging
  - `SyncFollower` 뒤에는 follower가 `beta=2`를 읽음
  - `Delete("beta")` 뒤에는 follower에서도 값이 사라짐
- 깨졌을 때 보이는 징후: `applied != 1`, follower에서 여전히 old value가 보이거나 delete가 반영되지 않습니다.
- 확인 테스트: `TestFollowerCatchUpAndDelete`
- 다시 볼 질문: `EntriesFrom(follower.Watermark() + 1)`가 delete operation까지 포함해 순서대로 적용되는가?

## 3. restart 후 disk state가 안 살아나는 경우
- 의심 파일: `../internal/capstone/capstone.go`
- 재현 명령:

```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run TestRestartNodeLoadsFromDisk -v
```

- 정상 기대: follower를 재시작한 뒤에도 `gamma=3`을 읽을 수 있어야 합니다.
- 깨졌을 때 보이는 징후: restart 뒤 `ok=false`이거나 빈 store처럼 동작합니다.
- 확인 테스트: `TestRestartNodeLoadsFromDisk`
- 다시 볼 질문: `RestartNode`가 해당 노드의 모든 shard store를 `LoadStore`로 다시 열고 있는가?

## 4. follower 중복 적용이 상태를 망치는 경우
- 의심 파일: `../internal/capstone/capstone.go`
- 재현 힌트: 같은 follower에 `SyncFollower`를 여러 번 호출했을 때 상태가 달라지면 안 됩니다.
- 정상 기대: 이미 적용한 offset는 skip되고, 값과 watermark는 그대로여야 합니다.
- 깨졌을 때 보이는 징후: duplicate apply 후 log 길이가 이상하게 늘어나거나 value가 뒤집힙니다.
- 다시 볼 질문: `Store.Apply`가 `op.Offset < len(store.log)`일 때 idempotent skip을 하는가?
