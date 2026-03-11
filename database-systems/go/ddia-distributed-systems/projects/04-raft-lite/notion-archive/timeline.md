# 04-raft-lite 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p go/ddia-distributed-systems/projects/04-raft-lite
cd go/ddia-distributed-systems/projects/04-raft-lite

go mod init study.local/go/ddia-distributed-systems/projects/04-raft-lite
```

디렉터리 구조 생성:
```bash
mkdir -p cmd/raft-lite
mkdir -p internal/raft
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
```

외부 의존성 없음. 순수 인메모리 시뮬레이션.

## Phase 1 — 문제 정의

### 1-1. problem/README.md 작성
- 동기 시뮬레이터에서 Raft 핵심 구현
- Production persistence/snapshotting은 범위 밖
- 출처: `legacy/distributed-cluster/consensus`

### 1-2. docs/concepts/ 작성
- `election-cycle.md`: heartbeat → timeout → candidate → RequestVote → majority → leader. 랜덤 대신 고정 timeout으로 결정적 테스트.
- `commit-rule.md`: 현재 term entry가 과반 복제되었을 때만 commitIndex 전진. 이전 term entry 직접 커밋 방지.

## Phase 2 — 메시지 타입 정의

파일: `internal/raft/raft.go`

### 2-1. 상태 상수
```go
const (
    Follower  = "follower"
    Candidate = "candidate"
    Leader    = "leader"
)
```

### 2-2. LogEntry
```go
type LogEntry struct {
    Index   int
    Term    int
    Command string
}
```

### 2-3. RPC 메시지 타입
- `voteRequest`: Term, CandidateID, LastLogIndex, LastLogTerm
- `voteResponse`: Term, VoteGranted
- `appendRequest`: Term, LeaderID, PrevLogIndex, PrevLogTerm, Entries, LeaderCommit
- `appendResponse`: Term, Success

## Phase 3 — Node 구현

### 3-1. Node 구조체
```go
type Node struct {
    ID, State, VotedFor string
    Peers               []string
    Term, CommitIdx     int
    Log                 []LogEntry
    sendRPC             func(string, string, any) any
    nextIndex, matchIndex map[string]int
    electionTTL, electionAge, heartbeat, heartAge int
    votes               map[string]struct{}
}
```
- `sendRPC`: 의존성 주입으로 전달 (실제 네트워크 vs 시뮬레이션 모두 가능)
- `CommitIdx`: -1로 초기화 (아무것도 커밋되지 않은 상태)

### 3-2. Tick 구현
- Leader: heartAge 증가, 주기 도달 시 `sendHeartbeats()`
- Follower/Candidate: electionAge 증가, TTL 도달 시 `startElection()`

### 3-3. startElection 구현
1. State → Candidate, Term++
2. 자기 자신에게 투표
3. 모든 peer에게 RequestVote 전송
4. higher term 응답 → `stepDown()`
5. 과반 투표 → `becomeLeader()`

### 3-4. becomeLeader 구현
- State → Leader
- 모든 peer의 nextIndex를 자기 로그 끝으로 초기화
- matchIndex를 -1로 초기화
- 즉시 heartbeat 전송

### 3-5. stepDown 구현
- State → Follower, Term 갱신, VotedFor 초기화
- electionAge 리셋

### 3-6. HandleRequestVote 구현
- higher term → stepDown
- lower term → 거부
- 같은 term: VotedFor 확인 + up-to-date 검사
- up-to-date: `LastLogTerm > mine || (LastLogTerm == mine && LastLogIndex >= mine)`

### 3-7. HandleAppendEntries 구현
- term 검사 + stepDown
- electionAge 리셋 (heartbeat 효과)
- PrevLogIndex consistency check:
  - 로그 길이 부족 → 실패
  - term 불일치 → 해당 index 이후 잘라내기 + 실패
- Entry 추가: index 충돌 시 잘라내고 새 entry 삽입
- LeaderCommit 반영: `min(LeaderCommit, 마지막 로그 index)`

### 3-8. ClientRequest 구현
- Leader가 아니면 nil 반환
- 새 LogEntry 생성 (Index=len(Log), Term=현재 term)
- 로컬 로그에 추가

### 3-9. sendHeartbeats + replicateTo
- 각 peer에 대해:
  - nextIndex부터 로그 entry 전송
  - Success → nextIndex/matchIndex 갱신
  - Failure → nextIndex 감소 (한 칸씩 뒤로)
  - higher term → stepDown
- 이후 `advanceCommitIndex()` 호출

### 3-10. advanceCommitIndex
- 로그 끝부터 역순 탐색
- 현재 term entry만 대상
- 자신 포함 과반이 matchIndex ≥ index이면 CommitIdx 갱신

## Phase 4 — Cluster 시뮬레이터

### 4-1. Cluster 구조체
```go
type Cluster struct {
    nodes  map[string]*Node
    downed map[string]struct{}
    order  []string
}
```

### 4-2. NewCluster
- 노드별 election timeout: `5 + i*2` (결정적 순서를 위해)
- sendRPC 클로저: `cluster.deliverRPC` 호출

### 4-3. Tick / Leader / DownNode / UpNode
- `Tick`: order 순서대로 down 노드 제외하고 각 노드 Tick
- `Leader`: 현재 Leader 상태인 노드 반환
- `DownNode/UpNode`: downed 맵으로 장애 시뮬레이션

### 4-4. deliverRPC
- down된 target → nil 반환 (네트워크 단절 시뮬레이션)
- RPC 타입에 따라 `HandleRequestVote` / `HandleAppendEntries` 호출

### 4-5. majority / min 헬퍼
```go
func majority(size int) int { return size/2 + 1 }
```

## Phase 5 — 테스트 작성

파일: `tests/raft_test.go`

```bash
GOWORK=off go test -v ./tests/
```

| 테스트 | 검증 내용 |
|--------|----------|
| TestLeaderElection | 20 tick 내 리더 선출, 리더 정확히 1명 |
| TestLeaderFailover | 리더 down → 새 리더 선출, 다른 노드 |
| TestLogReplicationAndCommit | 2개 command → 모든 노드에 복제 + 커밋 |
| TestHigherTermForcesStepDown | follower term 강제 상승 → 기존 리더 step-down |

`electLeader` 헬퍼: 최대 N tick 동안 Leader 대기.

## Phase 6 — 데모 CLI

파일: `cmd/raft-lite/main.go`

```bash
cd cmd/raft-lite
go run .
```

예상 출력:
```
leader=n1 commit=0 log_len=1
```

시나리오: 3노드 클러스터 → 리더 선출 대기 → "SET alpha 1" 요청 → 10 tick 복제 → 상태 출력

## Phase 7 — 검증 및 마무리

```bash
GOWORK=off go test -v ./tests/
gofmt -w internal/ cmd/ tests/
go vet ./...
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (raft.go) |
| 소스 코드 | ~370줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 4개 |
| 외부 의존성 | 없음 |
| 핵심 구조체 | Node, Cluster, LogEntry |
| RPC 메시지 | voteRequest/Response, appendRequest/Response |

## 이전/이후 프로젝트와의 관계

- **02-leader-follower-replication**: 리더-팔로워 복제를 사용하지만, "누가 리더인가"를 합의로 결정
- **01-rpc-framing**: 실제 분산 환경에서는 RPC 위에 Raft 메시지를 전달
- **05-clustered-kv-capstone**: RPC + Replication + Sharding + Raft를 모두 합쳐 완전한 분산 KV 스토어 구현
