# 30 검증과 경계: full consensus가 아닌 결정적 failover 시뮬레이션

이번 Todo에서는 "leader election이 된다"는 말 대신, 어떤 tick에 무슨 상태가 보이는지를 다시 확인했다. 이 project의 장점은 실패와 authority 교체가 지나치게 현실적이지 않기 때문에 오히려 흐름이 또렷하게 드러난다는 점이다.

## Session 1 — 재실행 결과

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/cmd/leader-election	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests	(cached)
```

```bash
$ GOWORK=off go run ./cmd/leader-election
tick=4 leader=node-1 term=1 suspected=[]
leader-down id=node-1
tick=8 suspected=[node-2]
tick=9 reelected=node-2 term=2
recovered=node-1 state=follower term=2
```

이 출력이 보여 주는 사실은 다음과 같다.

- 초기 leader는 deterministic timeout 덕분에 `node-1`이다.
- suspicion은 reelection보다 먼저 관찰된다.
- failover 뒤 term은 증가한다.
- 복구된 old leader는 새 authority를 받아들이고 follower가 된다.

마지막 문장은 조금 더 정확히 적을 필요가 있다. 이 구현에서 recovered old leader가 물러나는 직접 이유는 heartbeat payload 안의 `LeaderID`를 해석해서가 아니다. `HandleHeartbeat`는 `req.Term > node.Term || node.State != Follower`일 때 `stepDown()`을 호출하고, 그 다음 `silenceAge`와 `Suspected`를 리셋한다. 즉 authority 교체의 핵심은 "누가 leader냐"라는 이름표보다 "더 높은 term heartbeat를 받았거나, follower가 아닌 상태로 heartbeat를 받았느냐"에 가깝다.

## Session 2 — 테스트가 고정하는 회귀 신호

테스트 묶음은 네 개다.

- `TestHealthyLeaderKeepsSendingHeartbeats`
- `TestLeaderFailureTriggersSingleReelection`
- `TestIsolatedNodeCannotPromoteItself`
- `TestHigherTermHeartbeatForcesOldLeaderToStepDown`

이 네 테스트는 각각 health, failover, isolation safety, recovery step-down을 담당한다. 특히 `HealthyLeaderKeepsSendingHeartbeats`가 follower suspicion을 꺼 주는 조건까지 같이 검증한다는 점이 중요하다. 이 덕분에 heartbeat는 단순 background noise가 아니라 authority 유지 신호로 읽힌다.

## Session 3 — 현재 한계

- timeout이 random이 아니므로 collision avoidance나 split vote 학습에는 맞지 않는다.
- transport는 in-process RPC call이어서 packet loss, delay, asymmetric partition이 없다.
- vote rule은 log freshness를 보지 않는다.
- heartbeat payload의 `LeaderID`는 demo 출력용 맥락에는 남지만, 현재 step-down 판단 자체에는 쓰이지 않는다.
- commit rule, log replication, AppendEntries consistency가 없다.
- node recovery도 durable storage replay가 아니라 메모리 상태 재참여 정도만 표현한다.

그래서 이 project는 Raft 대체 구현이 아니라, "failure detector와 majority authority 교체를 눈으로 확인하는 결정적 시뮬레이터"로 읽는 편이 정확하다.
