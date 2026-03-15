# 05 Clustered KV Capstone 시리즈 맵

`05 Clustered KV Capstone`은 앞에서 만든 shard routing, leader-follower replication, disk-backed replay를 한 요청 경로로 다시 묶는 프로젝트다. 이번 문서 묶음은 "작은 분산 KV"라는 결과 설명보다, key 한 개가 어떤 shard로 가고, leader log에 어떻게 남고, follower가 언제 catch-up하며, restart 뒤 어디까지 복원되는지를 순서대로 따라가는 데 초점을 둔다.

## 이번 Todo에서 다시 잡은 질문

- key routing 규칙은 어디서 고정되고, leader/follower 배치는 어디까지 정적으로 박혀 있는가?
- write 한 번이 leader append, follower catch-up, on-disk replay까지 어떻게 이어지는가?
- 이 capstone이 보여 주는 복구는 "클러스터 recovery"가 아니라 정확히 어느 범위의 local recovery인가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 이번 재작성의 근거

- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/README.md`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/docs/concepts/static-topology.md`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/docs/concepts/replicated-write-pipeline.md`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/internal/capstone/capstone.go`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/tests/capstone_test.go`
- `database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/cmd/clustered-kv/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
rm -rf .demo-data && GOWORK=off go run ./cmd/clustered-kv
find .demo-data -type f | sort
```

## 보조 문서

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 이번에 명시적으로 남긴 경계

- topology는 `NewCluster` 시점에 고정되며 membership change는 없다.
- replication은 in-process orchestration이며 transport, quorum, election이 없다.
- `RestartNode`는 노드가 이미 가진 log file을 다시 읽을 뿐이고, lagging follower를 자동 catch-up하지는 않는다.
- ordinary `Read`는 항상 shard leader를 읽고, follower freshness 관찰은 `ReadFromNode` 같은 explicit debug surface에서만 드러난다.
