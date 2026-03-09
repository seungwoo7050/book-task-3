# 05-clustered-kv-capstone 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/ddia-distributed-systems/05-clustered-kv-capstone
cd go/ddia-distributed-systems/05-clustered-kv-capstone

go mod init study.local/ddia-distributed-systems/05-clustered-kv-capstone
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/clustered-kv
mkdir -p internal/capstone
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

### go.mod 의존성 설정
```bash
go mod edit -require study.local/shared@v0.0.0
go mod edit -replace study.local/shared=../../shared
```

shared/hash 패키지 사용 (MurmurHash3 for shard routing).

추가 표준 라이브러리: `os`, `path/filepath`, `bufio`, `encoding/json`, `slices`.

## Phase 1 — 문제 정의

### 1-1. problem/README.md 작성
- 정적 토폴로지 + 정적 리더 배치의 소규모 클러스터형 KV store
- 레거시에 없던 신규 통합 프로젝트
- 핵심 연결 요소: shard router, disk-backed store, leader-follower replication

### 1-2. docs/concepts/ 작성
- `static-topology.md`: 멤버십 변경 없이 초기 설정 고정. reconfiguration 복잡도 배제.
- `replicated-write-pipeline.md`: route → leader append → follower catch-up → routed read

## Phase 2 — Store 구현 (디스크 저장소)

파일: `internal/capstone/capstone.go`

### 2-1. Operation 구조체
```go
type Operation struct {
    Offset int     `json:"offset"`
    Type   string  `json:"type"`
    Key    string  `json:"key"`
    Value  *string `json:"value,omitempty"`
}
```
- 02-replication의 LogEntry와 동일한 구조
- JSON 직렬화 태그 추가 (디스크 저장)

### 2-2. Store 구조체
```go
type Store struct {
    path string
    data map[string]string
    log  []Operation
}
```
- 이중 상태: 인메모리 맵 (읽기) + 인메모리 로그 (복제)
- 디스크 파일 경로 보유

### 2-3. LoadStore (디스크 복원)
```go
func LoadStore(path string) (*Store, error)
```
- `os.MkdirAll` → 디렉터리 미존재 시 생성
- `os.OpenFile(CREATE|RDONLY)` → 파일 미존재 시 빈 파일 생성
- `bufio.Scanner`로 JSON Lines 한 줄씩 읽기
- 각 Operation을 `applyInMemory` + log 슬라이스에 추가
- 노드 재시작의 핵심 메커니즘

### 2-4. AppendPut / AppendDelete
- Operation 생성 (offset = `len(store.log)`)
- `Apply(op)` 호출

### 2-5. Apply (idempotent)
- `op.Offset < len(store.log)` → skip (이미 적용)
- `op.Offset != len(store.log)` → non-sequential 에러
- 디스크에 JSON 한 줄 append (WRONLY|APPEND 모드)
- 인메모리 적용

### 2-6. EntriesFrom / Watermark / Get
- `EntriesFrom(offset)`: 방어적 복사로 로그 슬라이스 반환
- `Watermark()`: `len(log) - 1`
- `Get(key)`: 인메모리 맵 조회

### 2-7. applyInMemory
- `"put"` → data 맵에 저장
- `"delete"` → data 맵에서 삭제

## Phase 3 — Shard Ring (내장 consistent hash)

### 3-1. ringEntry / shardRing
- 03-shard-routing의 Ring을 capstone 내부에 재구현
- `ShardID` 기반 (NodeID 대신)

### 3-2. AddShard / ShardForKey
- 동일한 알고리즘: `shardID#v<i>` → MurmurHash3 → 정렬된 ring에 삽입
- `ShardForKey`: key hash → ring에서 `>=` 첫 entry → wrap-around

### 3-3. itoa 헬퍼
- 03-shard-routing에서 복사

## Phase 4 — Cluster 통합

### 4-1. ReplicaGroup / Node / Cluster
```go
type ReplicaGroup struct {
    ShardID   string
    Leader    string
    Followers []string
}

type Node struct {
    ID     string
    stores map[string]*Store
}

type Cluster struct {
    dataDir, router, groups, nodes, autoReplicate
}
```

### 4-2. NewCluster 초기화
- groups 순회 → router에 shard 추가
- leader + followers 모든 멤버에 대해:
  - Node 생성 (미존재 시)
  - `LoadStore(dataDir/nodeID/shardID.log)` → 노드에 등록
- 디스크 디렉터리 구조: `dataDir/<nodeID>/<shardID>.log`

### 4-3. Put / Delete
1. `RouteShard(key)` → shardID
2. `groups[shardID].Leader` → leader 노드의 store에 AppendPut/Delete
3. `autoReplicate == true` → 각 follower에 `SyncFollower`

### 4-4. SyncFollower
- leader store의 `EntriesFrom(follower.Watermark() + 1)`
- 각 entry를 follower store에 `Apply`
- 반환값: 적용 건수

### 4-5. Read / ReadFromNode
- `Read`: 라우팅 → 리더에서 읽기
- `ReadFromNode`: 특정 노드에서 직접 읽기, replica 아닌 경우 에러

### 4-6. RestartNode
- 해당 노드의 모든 shard store를 `LoadStore`로 재로드
- 디스크에서 인메모리 상태 완전 복원

## Phase 5 — 테스트 작성

파일: `tests/capstone_test.go`

```bash
GOWORK=off go test -v ./tests/
```

| 테스트 | 검증 내용 |
|--------|----------|
| TestWriteRoutesToLeaderAndReplicates | Put → 리더+팔로워 모두 값 존재 |
| TestFollowerCatchUpAndDelete | autoReplicate=false → lag → SyncFollower → catch-up → Delete 복제 |
| TestRestartNodeLoadsFromDisk | Put + RestartNode → 재시작 후 값 유지 |

`newCluster` 헬퍼:
- `t.TempDir()` → 테스트 격리
- 2 shard, 3 node 구성, 64 virtual nodes

## Phase 6 — 데모 CLI

파일: `cmd/clustered-kv/main.go`

```bash
cd cmd/clustered-kv
go run .
```

예상 출력:
```
key=alpha shard=shard-X follower=node-Y value=1 ok=true
```

시나리오: 2 shard 클러스터 → Put("alpha","1") → follower에서 읽기

주의: 데모 실행 시 `.demo-data/` 디렉터리가 생성됨.

## Phase 7 — 검증 및 마무리

```bash
GOWORK=off go test -v ./tests/
gofmt -w internal/ cmd/ tests/
go vet ./...
```

데모 데이터 정리:
```bash
rm -rf .demo-data/
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (capstone.go) |
| 소스 코드 | ~300줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 3개 |
| 외부 의존성 | shared/hash (MurmurHash3) |
| 핵심 구조체 | Store, Cluster, ReplicaGroup, Node, shardRing |

## 통합 맵: 이전 프로젝트들이 어디에 녹아 있는가

| 이전 프로젝트 | 캡스톤에서의 역할 |
|--------------|-----------------|
| 01-rpc-framing | in-process 함수 호출로 대체 (네트워크 없음) |
| 02-leader-follower-replication | SyncFollower + Watermark + Idempotent Apply |
| 03-shard-routing | shardRing + ShardForKey (consistent hash) |
| 04-raft-lite | 정적 리더로 단순화 (합의 없음) |
| DB-04 wal-recovery | Store의 JSON append-only log + LoadStore 복원 |
