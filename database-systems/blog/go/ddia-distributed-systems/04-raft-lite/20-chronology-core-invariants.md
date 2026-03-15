# Core Invariants

## 1. election은 fixed TTL이지만 term progression semantics는 그대로다

`NewCluster()`는 각 node에 `5+i*2` 같은 고정 election TTL을 준다. docs의 [`election-cycle.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/concepts/election-cycle.md)가 말하듯, 랜덤 대신 고정값을 써서 테스트를 결정적으로 만든 것이다.

하지만 election semantics 자체는 그대로다.

- follower/candidate는 TTL이 차면 `startElection()`
- term 증가
- self vote
- 과반수면 leader

즉 timing model만 단순화했고, term/vote rules는 유지했다.

## 2. vote는 up-to-date log rule을 만족할 때만 준다

`HandleRequestVote()`는 candidate log가 더 최신이거나 같은지 확인한다.

```go
upToDate := req.LastLogTerm > lastTerm || (req.LastLogTerm == lastTerm && req.LastLogIndex >= lastIndex)
canVote := node.VotedFor == "" || node.VotedFor == req.CandidateID
```

즉 term이 같아도 candidate log가 뒤처져 있으면 vote를 주지 않는다. 이 규칙 덕분에 stale log를 가진 candidate가 leader가 되는 걸 막는다.

## 3. AppendEntries consistency mismatch는 follower log를 잘라낸다

`HandleAppendEntries()`는 `PrevLogIndex`와 `PrevLogTerm`이 맞지 않으면 실패한다. 특히 같은 index지만 term mismatch가 나면 아래처럼 follower log를 그 지점 앞까지 잘라낸다.

```go
if node.Log[req.PrevLogIndex].Term != req.PrevLogTerm {
    node.Log = node.Log[:req.PrevLogIndex]
    return appendResponse{Term: node.Term, Success: false}
}
```

즉 follower는 conflict가 난 suffix를 버리고 leader가 보내는 더 일관된 log를 다시 받아들일 준비를 한다.

## 4. commit rule은 current term entry에 대해서만 majority를 계산한다

`advanceCommitIndex()`는 역순으로 index를 보면서 `node.Log[index].Term != node.Term`이면 건너뛴다. 그리고 `matchIndex`가 그 index 이상인 follower 수를 세어 과반수를 만족할 때만 `CommitIdx`를 올린다.

즉 docs의 [`commit-rule.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/concepts/commit-rule.md)가 설명하는 "현재 term entry만 majority로 commit" 규칙이 그대로 구현돼 있다.

## 5. higher term response는 leader를 즉시 follower로 내린다

`startElection()`과 `replicateTo()` 둘 다 더 높은 `resp.Term`을 보면 `stepDown(resp.Term)`을 호출한다. 즉 leader든 candidate든 higher term을 본 순간 더 이상 자신의 authority를 유지하지 않는다.

추가 재실행의 `failover_leader n2 2`도 바로 이 규칙의 결과다. term 1 leader가 내려가고 term 2 leader가 새로 올라온다.
