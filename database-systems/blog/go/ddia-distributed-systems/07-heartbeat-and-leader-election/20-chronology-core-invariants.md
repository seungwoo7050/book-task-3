# 20 핵심 상태 전이: silence, majority, higher-term step-down

이 lab의 핵심은 복잡한 consensus가 아니라 세 단계다. silence age가 suspect로 바뀌고, election이 majority를 받아 leader가 되고, 더 높은 term heartbeat가 옛 authority를 접는다.

## Session 1 — `Tick`은 suspicion과 election을 분리해 둔다

`Node.Tick()`은 follower/candidate 쪽에서 두 임계값을 나눠 본다.

```go
node.silenceAge++
if node.silenceAge >= node.suspicionTTL {
	node.Suspected = true
}
if node.silenceAge >= node.electionTTL {
	node.startElection()
}
```

이 분리가 중요한 이유는 heartbeat failure가 곧바로 election으로 이어지지 않기 때문이다. suspicion이 먼저 보이고, 한 tick 이상 더 지나야 선거가 시작된다. demo에서 `leader-down` 뒤 `tick=8 suspected=[node-2]`, 그 다음 `tick=9 reelected=node-2 term=2`가 나오는 이유가 바로 이 분리다.

## Session 2 — majority 없이는 isolated node도 candidate에서 끝난다

선거 로직은 `startElection()` 하나에 압축돼 있다.

```go
node.State = Candidate
node.Term++
node.VotedFor = node.ID
node.votes = map[string]struct{}{node.ID: {}}
...
if len(node.votes) >= majority(len(node.Peers)+1) {
	node.becomeLeader()
}
```

이 구조 때문에 isolated node는 self-vote로 term을 올릴 수는 있어도 leader가 되지는 못한다. 테스트 `TestIsolatedNodeCannotPromoteItself`도 바로 이 경계를 잡고 있다. 이 lab에서 majority는 split-brain을 막는 최소 안전장치이지, log up-to-date 판정까지 포함한 full Raft vote rule은 아니다.

## Session 3 — higher term은 authority를 즉시 접게 만든다

`HandleHeartbeat`는 old leader recovery 경계를 보여 주는 핵심 함수다.

```go
func (node *Node) HandleHeartbeat(req heartbeatRequest) heartbeatResponse {
	if req.Term < node.Term {
		return heartbeatResponse{Term: node.Term}
	}
	if req.Term > node.Term || node.State != Follower {
		node.stepDown(req.Term)
	}
	node.silenceAge = 0
	node.Suspected = false
	return heartbeatResponse{Term: node.Term}
}
```

여기서 중요한 건 `req.Term > node.Term || node.State != Follower` 조건이다. 즉 더 높은 term이면 물론 내려오고, follower가 아닌 상태로 heartbeat를 받아도 step-down한다. 테스트 `TestHigherTermHeartbeatForcesOldLeaderToStepDown`은 recovery한 옛 leader가 결국 `Follower`와 새 term으로 정리된다는 점을 고정한다.

이렇게 보면 이 lab은 authority 교체의 세 장면을 아주 명확하게 분리한다.

- failure signal 생성
- majority 기반 authority 획득
- higher-term authority 수용
