# 지식 인덱스

## 핵심 용어
- `shard`: key 공간을 나눠 각 replica group이 맡는 단위입니다.
- `replica group`: 같은 shard를 가진 leader와 follower 집합입니다.
- `catch-up`: 뒤처진 follower가 leader의 operation log를 따라잡는 과정입니다.
- `watermark`: follower가 어디까지 operation을 적용했는지 나타내는 위치입니다.
- `restart recovery`: 재시작 후 disk log를 다시 읽어 state를 복원하는 동작입니다.

## 재현 순서용 파일 맵
- `../internal/capstone/capstone.go`: 구현 전체가 있는 중심 파일입니다.
- `../tests/capstone_test.go`: route, catch-up, restart recovery를 시나리오별로 검증합니다.
- `../cmd/clustered-kv/main.go`: 가장 짧은 end-to-end 데모입니다.
- `../docs/concepts/replicated-write-pipeline.md`: write가 leader에서 follower까지 가는 순서를 정리합니다.

## 바로 실행할 명령
```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run TestWriteRoutesToLeaderAndReplicates -v
go test ./... -run TestFollowerCatchUpAndDelete -v
go test ./... -run TestRestartNodeLoadsFromDisk -v
go run ./cmd/clustered-kv
```

## 기대 결과
### 데모 출력
```text
key=alpha shard=shard-a follower=node-2 value=1 ok=true
```

### 테스트가 확인하는 대표 사실
- `TestWriteRoutesToLeaderAndReplicates`: leader와 follower 모두 `alpha=1`
- `TestFollowerCatchUpAndDelete`: lag 상태를 재현한 뒤 catch-up과 delete replication을 확인
- `TestRestartNodeLoadsFromDisk`: restart 후에도 `gamma=3` 유지

## topology 메모
- `shard-a`: leader=`node-1`, follower=`node-2`
- `shard-b`: leader=`node-2`, follower=`node-3`
- virtual nodes: 64

## 다음 확장 연결
- 현재는 static topology가 전제입니다.
- 다음 확장은 leader election, membership change, rebalancing입니다.
- 이 프로젝트가 고정한 가장 중요한 인터페이스는 `Cluster`와 `Store` 사이의 경계입니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/capstone_test.go`
- 다시 돌릴 테스트 이름: `TestWriteRoutesToLeaderAndReplicates`, `TestFollowerCatchUpAndDelete`, `TestRestartNodeLoadsFromDisk`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
