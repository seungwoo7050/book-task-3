# 10 범위를 다시 좁히기: authority 교체만 떼어 낸 election lab

이 project를 다시 읽을 때 제일 먼저 정리한 건 "Raft를 구현한다"는 기대를 버리는 일이었다. 문제 문서가 고정하는 건 heartbeat, suspicion, term, majority vote뿐이다. append log나 commit advancement는 아예 범위 밖이다.

## Session 1 — problem 문서가 빼는 것부터 확인하기

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/problem/README.md)는 핵심을 꽤 잘 잘라 준다.

- leader는 heartbeat를 보낸다.
- follower는 silence가 길어지면 suspect한다.
- election은 majority를 받아야 leader가 된다.
- higher term을 보면 old leader는 step-down한다.
- 이 모든 과정은 tick 기반 결정적 시뮬레이션으로 재현된다.

그리고 일부러 뺀 것들도 선명하다.

- log replication
- commit rule
- randomized timeout
- network partition
- pre-vote
- membership change

즉 이 lab은 "authority는 언제 바뀌는가"만 떼어 내 보는 단계다.

## Session 2 — `NewCluster`는 timeout을 랜덤이 아니라 계단식으로 배치한다

핵심 구현 [`internal/election/election.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go)의 `NewCluster`를 보면 이 프로젝트의 색깔이 바로 드러난다.

```go
for index, id := range nodeIDs {
	node := NewNode(id, peers, 3+index*2, 4+index*2, func(target string, rpc string, payload any) any {
		return cluster.deliverRPC(target, rpc, payload)
	})
	cluster.nodes[id] = node
}
```

`node-1`, `node-2`, `node-3`은 각각 다른 suspicion/election TTL을 갖는다.

- `node-1`: suspicion 3, election 4
- `node-2`: suspicion 5, election 6
- `node-3`: suspicion 7, election 8

그래서 첫 leader는 우연히 정해지는 게 아니라 거의 항상 가장 작은 TTL을 가진 `node-1`이다. 이 결정성 덕분에 테스트와 demo가 매번 같은 타이밍을 보여 준다.

## Session 3 — 공개 surface는 네 줄이면 충분하다

demo output은 아래 네 줄이 전부다.

```text
tick=4 leader=node-1 term=1 suspected=[]
leader-down id=node-1
tick=8 suspected=[node-2]
tick=9 reelected=node-2 term=2
recovered=node-1 state=follower term=2
```

이 짧은 출력 안에 이 lab의 거의 모든 질문이 들어 있다.

- 최초 leader는 언제 생기는가
- leader failure 이후 suspicion은 언제 보이는가
- reelection은 언제 끝나는가
- 복구된 old leader는 어떤 state로 남는가

다음 글에서는 이 네 줄을 만드는 핵심 상태 전이를 코드 순서대로 묶는다.
