# Raft Lite — 분산 시스템에서 "하나의 진실"을 만드는 법

## 들어가며

앞선 프로젝트들에서 우리는 복제(같은 데이터를 여러 곳에)와 샤딩(다른 데이터를 나눠서)을 구현했다. 하지만 한 가지 전제가 빠져 있었다: **누가 리더인지를 어떻게 합의하는가?** Leader-follower replication은 리더가 있다고 가정했지만, 리더가 죽으면? 누가 다음 리더가 되는지를 어떻게 안전하게 결정하는가?

이것이 **분산 합의(consensus)** 문제다. Paxos가 이 문제를 최초로 풀었지만, 이해하기 어렵기로 유명하다. Raft는 동일한 문제를 "이해 가능성"을 최우선으로 설계한 알고리즘이다. 이 프로젝트에서는 production-grade 구현 대신, Raft의 핵심 안전성 속성이 드러나는 **동기 시뮬레이터**를 만든다.

## 세 가지 상태: Follower, Candidate, Leader

모든 노드는 세 상태 중 하나에 있다.

- **Follower**: 기본 상태. 리더의 heartbeat를 기다린다.
- **Candidate**: heartbeat를 받지 못한 follower가 선거를 시작한다.
- **Leader**: 과반 투표를 얻은 candidate. 로그 복제를 주도한다.

시간은 **term**이라는 논리적 단위로 흐른다. 각 term에 최대 한 명의 leader만 존재할 수 있다.

## 선거의 동작

`Tick()`이 시뮬레이션의 시간 단위다. Leader는 주기적으로 heartbeat를 보내고, Follower는 일정 tick 동안 heartbeat를 받지 못하면 선거를 시작한다.

```go
func (node *Node) startElection() {
    node.State = Candidate
    node.Term++
    node.VotedFor = node.ID
    node.votes = map[string]struct{}{node.ID: {}}
    node.electionAge = 0

    lastIndex, lastTerm := node.lastLogInfo()
    for _, peer := range node.Peers {
        raw := node.sendRPC(peer, "requestVote", voteRequest{
            Term:         node.Term,
            CandidateID:  node.ID,
            LastLogIndex: lastIndex,
            LastLogTerm:  lastTerm,
        })
        // ...
    }
    if len(node.votes) >= majority(len(node.Peers)+1) {
        node.becomeLeader()
    }
}
```

선거의 규칙:
1. term을 하나 올린다 (새로운 선거 라운드)
2. 자기 자신에게 투표한다
3. 모든 peer에게 RequestVote를 보낸다
4. 과반 투표를 받으면 리더가 된다

## 투표 규칙: "더 최신인 로그"만 승리한다

투표를 받을 수 있는 조건은 단순하지 않다. Raft의 안전성을 보장하는 핵심 규칙이 여기에 있다.

```go
func (node *Node) HandleRequestVote(req voteRequest) voteResponse {
    if req.Term > node.Term {
        node.stepDown(req.Term)
    }
    if req.Term < node.Term {
        return voteResponse{Term: node.Term, VoteGranted: false}
    }

    lastIndex, lastTerm := node.lastLogInfo()
    upToDate := req.LastLogTerm > lastTerm ||
        (req.LastLogTerm == lastTerm && req.LastLogIndex >= lastIndex)
    canVote := node.VotedFor == "" || node.VotedFor == req.CandidateID
    
    if canVote && upToDate {
        node.VotedFor = req.CandidateID
        return voteResponse{Term: node.Term, VoteGranted: true}
    }
    return voteResponse{Term: node.Term, VoteGranted: false}
}
```

**up-to-date 검사**: candidate의 마지막 로그 entry가 나보다 더 최신이거나 같아야 한다. "더 최신"이란 (1) 마지막 entry의 term이 더 크거나, (2) term이 같으면 index가 더 크거나 같은 것을 의미한다.

이 규칙이 없으면 오래된 로그를 가진 노드가 리더가 되어, 이미 커밋된 entry를 덮어쓸 수 있다.

## AppendEntries: 로그의 일관성

Leader는 주기적으로 follower에게 `AppendEntries`를 보낸다. entry가 없으면 heartbeat, 있으면 로그 복제가 된다.

```go
func (node *Node) HandleAppendEntries(req appendRequest) appendResponse {
    node.electionAge = 0  // heartbeat 수신 → 선거 타이머 리셋

    if req.PrevLogIndex >= 0 {
        if req.PrevLogIndex >= len(node.Log) {
            return appendResponse{Term: node.Term, Success: false}
        }
        if node.Log[req.PrevLogIndex].Term != req.PrevLogTerm {
            node.Log = node.Log[:req.PrevLogIndex]
            return appendResponse{Term: node.Term, Success: false}
        }
    }
    // 일관성 확인 후, entry 추가
    // ...
}
```

**Consistency check**: `PrevLogIndex`와 `PrevLogTerm`으로 follower의 로그가 leader와 같은지 확인한다. 불일치하면? Leader는 `nextIndex`를 하나 줄여서 다음에 더 이전의 entry부터 보낸다. 이렇게 한 칸씩 뒤로 가다 보면, 결국 일치하는 지점을 찾아 그 이후를 모두 같은 내용으로 채울 수 있다.

## 커밋 규칙: 과반이 가져야 커밋

Leader가 로컬에 entry를 추가했다고 바로 커밋하는 게 아니다. **현재 term의 entry가 과반 노드에 복제되었을 때만** `commitIndex`를 올린다.

```go
func (node *Node) advanceCommitIndex() {
    for index := len(node.Log) - 1; index > node.CommitIdx; index-- {
        if node.Log[index].Term != node.Term {
            continue
        }
        replicated := 1
        for _, peer := range node.Peers {
            if node.matchIndex[peer] >= index {
                replicated++
            }
        }
        if replicated >= majority(len(node.Peers)+1) {
            node.CommitIdx = index
            break
        }
    }
}
```

`node.Log[index].Term != node.Term`을 건너뛰는 것이 중요하다. 이전 term의 entry는 현재 term의 entry가 커밋될 때 함께 커밋될 수 있지만, 직접 커밋 대상이 되지는 않는다. 이 규칙이 없으면 Raft 논문의 "Figure 8 문제"가 발생할 수 있다.

## Higher-Term Step-Down

어떤 노드든 자신보다 높은 term을 발견하면, 즉시 follower로 돌아간다.

```go
func (node *Node) stepDown(term int) {
    node.State = Follower
    node.Term = term
    node.VotedFor = ""
    node.electionAge = 0
}
```

이것이 Raft의 "monotonic term" 원칙이다. term은 논리적 시간이고, 더 높은 시간을 가진 노드가 더 최신의 정보를 가졌을 가능성이 높다.

## 클러스터 시뮬레이터

`Cluster` 구조체가 여러 노드를 묶고, RPC 전달을 시뮬레이션한다. 실제 네트워크 대신 함수 호출로 메시지를 전달한다.

```go
func NewCluster(nodeIDs []string) *Cluster {
    // 각 노드에 다른 election timeout 부여: 5+i*2
    // sendRPC는 cluster.deliverRPC를 호출하는 클로저
}
```

노드별로 다른 election timeout(`5+i*2`)을 부여하여, 동시에 선거를 시작하는 split vote를 방지한다. 실제 Raft는 랜덤 timeout을 쓰지만, 테스트 결정성을 위해 고정값을 사용한다.

`DownNode`/`UpNode`로 노드 장애를 시뮬레이션한다. down된 노드는 Tick이 건너뛰어지고, RPC에 nil을 반환한다.

## 테스트가 증명하는 것들

4개 테스트가 Raft의 핵심 안전성 속성을 검증한다:

1. **LeaderElection**: 20 tick 안에 리더 선출 + 리더는 정확히 1명
2. **LeaderFailover**: 리더 다운 → 새 리더 선출, 이전 리더와 다른 노드
3. **LogReplicationAndCommit**: 클라이언트 요청 → 모든 노드에 로그 복제 + 커밋
4. **HigherTermForcesStepDown**: follower의 term을 임의로 올리면 기존 리더가 step down

## 돌아보며

이 프로젝트는 Raft의 "이해 가능한 합의"라는 설계 목표를 직접 체험하는 것이다. 370줄의 코드에 leader election, log replication, commit advancement, step-down이 모두 들어 있다. 실제 production Raft 구현(etcd의 raft 라이브러리 등)에는 snapshot, membership change, pre-vote 등이 추가되지만, 핵심 안전성 속성은 이 370줄과 동일하다.

다음이자 마지막 프로젝트는 이 모든 것을 합치는 것이다: RPC + Replication + Sharding + Raft → Clustered KV Store.
