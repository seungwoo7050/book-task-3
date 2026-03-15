# Evidence Ledger

## Source files used

- `problem/README.md`
  - 범위와 제외 항목을 먼저 고정했다.
- `README.md`
  - 검증 명령과 public surface를 다시 확인했다.
- `docs/concepts/heartbeat-failure-detector.md`
  - suspicion과 election을 분리해 읽어야 하는 이유를 확인했다.
- `docs/concepts/majority-election.md`
  - isolated node가 leader가 되면 안 되는 이유를 문장으로 확인했다.
- `internal/election/election.go`
  - `Tick`, `startElection`, `HandleHeartbeat`, `deliverRPC`를 직접 추적했다.
- `tests/election_test.go`
  - healthy, failover, isolation, step-down 네 시나리오를 확인했다.
- `cmd/leader-election/main.go`
  - tick 기반 공개 흐름이 어떤 문자열로 드러나는지 다시 확인했다.

## Commands rerun

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
```

## Key outputs

```text
ok  	study.local/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests	(cached)
tick=4 leader=node-1 term=1 suspected=[]
tick=8 suspected=[node-2]
tick=9 reelected=node-2 term=2
recovered=node-1 state=follower term=2
```

## Inferences called out explicitly

- deterministic first leader selection은 `NewCluster`의 fixed TTL ladder와 demo output을 함께 근거로 삼았다.
- recovery된 old leader가 authority를 접는 방식은 `HandleHeartbeat`의 `req.Term > node.Term || node.State != Follower` 조건에서 읽었다.
- `heartbeatRequest{LeaderID string}`는 payload에 실려 다니지만, 현재 step-down 판단은 `LeaderID` 자체를 조회하지 않는다.
