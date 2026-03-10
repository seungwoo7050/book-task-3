# 접근 기록

## 재현 순서 제안
이 프로젝트는 아래 4단계로 나누면 훨씬 재현하기 쉽습니다.

### 1. 먼저 `Store`만 만든다
- 관련 파일: `../internal/capstone/capstone.go`
- 먼저 구현할 것:
  - `LoadStore`
  - `Apply`
  - `AppendPut`
  - `AppendDelete`
  - `EntriesFrom`, `Watermark`, `Get`
- 이유: 라우팅과 복제 전에 디스크에 기록되고 다시 복원되는 단위를 먼저 고정해야 합니다.

### 2. 그 다음 `shardRing`을 붙인다
- 관련 파일: `../internal/capstone/capstone.go`
- 이유: key가 어디로 가는지 정해져야 leader/follower 논의가 가능합니다.
- 체크 포인트: `ShardForKey("alpha")`가 현재 topology에서 일관된 shard를 반환해야 합니다.

### 3. 마지막에 `Cluster`로 routing + replication을 묶는다
- 관련 파일: `../internal/capstone/capstone.go`, `../tests/capstone_test.go`
- 구현 순서:
  1. `NewCluster`
  2. `Put`, `Delete`
  3. `SyncFollower`
  4. `Read`, `ReadFromNode`
  5. `RestartNode`

### 4. 테스트와 데모로 닫는다
- 관련 파일: `../tests/capstone_test.go`, `../cmd/clustered-kv/main.go`
- 실행 명령:

```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run 'TestWriteRoutesToLeaderAndReplicates|TestFollowerCatchUpAndDelete|TestRestartNodeLoadsFromDisk' -v
go run ./cmd/clustered-kv
```

## 코드가 택한 핵심 판단
### 정적 topology를 먼저 고정한다
- 관련 파일: `../internal/capstone/capstone.go`
- 판단: membership churn까지 넣으면 routing, replication, recovery가 서로 엉키므로, 먼저 shard와 replica group을 명시적으로 선언하는 쪽을 택했습니다.

### leader local apply와 follower catch-up을 분리한다
- 관련 파일: `../internal/capstone/capstone.go`
- 판단: leader는 먼저 자신의 store에 기록하고, follower는 `EntriesFrom(watermark + 1)`로 따라오게 해야 lag와 catch-up을 모두 설명할 수 있습니다.

### disk-backed store를 replication log와 겸용한다
- 관련 파일: `../internal/capstone/capstone.go`
- 판단: `Store`가 JSON lines op log와 in-memory map을 함께 들고 있어, durability와 replication을 한 모델에서 설명할 수 있습니다.

## 기대 출력과 빠른 해석
데모가 정상이라면 다음이 출력됩니다.

```text
key=alpha shard=shard-a follower=node-2 value=1 ok=true
```

이 한 줄은 다음을 동시에 보여 줍니다.
- `alpha`가 `shard-a`로 라우팅되었다.
- 그 shard의 follower는 `node-2`다.
- follower에서도 `value=1`이 보인다.

## 포트폴리오 설명으로 바꿀 때 남길 장면
- key 하나가 route, leader write, follower read까지 이어지는 흐름을 그림 하나로 설명할 수 있습니다.
- `SetAutoReplicate(false)` 후 `SyncFollower`를 수동 호출하는 테스트는 lag와 catch-up을 보여 주기에 좋습니다.
- 정적 topology라는 제한을 솔직하게 밝히면, 무엇을 의도적으로 제외했는지도 명확하게 설명할 수 있습니다.
