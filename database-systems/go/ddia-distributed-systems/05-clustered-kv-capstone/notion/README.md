# 학습 노트 안내

이 노트 묶음은 Go DDIA 트랙의 마지막 캡스톤을 다시 만드는 사람을 위한 재현용 설명서입니다. 이 프로젝트는 routing, replication, disk-backed recovery를 하나로 합치기 때문에 “이전 4개 프로젝트가 실제로 연결되는가”를 검증하기에 가장 좋은 문서입니다.

## 왜 05가 재현성에 좋은가
- 구현은 `../internal/capstone/capstone.go` 한 파일에 거의 모두 모여 있습니다.
- 테스트 3개가 end-to-end 시나리오를 직접 보여 줍니다.
- 데모 출력이 현재 topology를 그대로 드러냅니다.

## 권장 재현 순서
1. `../problem/README.md`와 `../docs/concepts/replicated-write-pipeline.md`를 읽어 시스템 경계를 먼저 맞춥니다.
2. `../internal/capstone/capstone.go`에서 `Store`, `shardRing`, `Cluster` 순서로 읽습니다.
3. `../tests/capstone_test.go`를 보며 route, catch-up, restart recovery 시나리오를 확인합니다.
4. `../cmd/clustered-kv/main.go`를 실행해 실제 shard와 follower가 어떻게 선택되는지 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 통합 포인트를 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: topology, 성공 기준, 재현 입력과 출력, 범위 밖 항목을 정리합니다.
- `01-approach-log.md`: store, shard ring, cluster를 어떤 순서로 붙이면 재현이 쉬운지 설명합니다.
- `02-debug-log.md`: route 실패, catch-up 누락, restart recovery 실패를 어떻게 재현하고 찾는지 적어 둡니다.
- `03-retrospective.md`: 왜 이 단계가 재현성 학습과 포트폴리오 설명에 좋은지 정리합니다.
- `04-knowledge-index.md`: 핵심 용어, 파일 맵, 명령, 기대 출력, 다음 확장 포인트를 모아 둡니다.

## 바로 확인할 명령
```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
go test ./... -run 'TestWriteRoutesToLeaderAndReplicates|TestFollowerCatchUpAndDelete|TestRestartNodeLoadsFromDisk' -v
go run ./cmd/clustered-kv
```

## 기대 출력
```text
key=alpha shard=shard-a follower=node-2 value=1 ok=true
```

## 검증 앵커
- 테스트: `TestWriteRoutesToLeaderAndReplicates`, `TestFollowerCatchUpAndDelete`, `TestRestartNodeLoadsFromDisk`
- 데모 경로: `../cmd/clustered-kv/main.go`
- 개념 문서: `../docs/concepts/replicated-write-pipeline.md`, `../docs/concepts/static-topology.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있고, 여기서는 다시 구현할 때 바로 필요한 정보만 남깁니다.
