# 07 Heartbeat and Leader Election 시리즈 맵

`07 Heartbeat and Leader Election`은 full consensus 이전 단계에서 authority 교체만 떼어 내 보여 주는 lab이다. 이번 문서 묶음은 "leader election이 된다"는 결과보다, silence age가 suspect로 바뀌고, deterministic timeout이 candidate를 만들고, majority vote와 higher-term heartbeat가 authority를 다시 접는 순서를 따라가는 데 집중한다.

## 이번 Todo에서 다시 잡은 질문

- 이 구현의 failure detector는 얼마나 단순한가?
- leader 선출은 randomized race인가, 아니면 deterministic timeout ladder인가?
- recovered old leader는 어떤 신호에서 follower로 돌아오는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 이번 재작성의 근거

- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/problem/README.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/README.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/docs/concepts/heartbeat-failure-detector.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/docs/concepts/majority-election.md`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests/election_test.go`
- `database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/cmd/leader-election/main.go`

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
```

## 보조 문서

- [_evidence-ledger.md](_evidence-ledger.md)
- [_structure-outline.md](_structure-outline.md)

## 이번에 명시적으로 남긴 경계

- timeout은 random이 아니라 `3+index*2`, `4+index*2`로 고정된다.
- transport는 실제 네트워크가 아니라 `deliverRPC` 함수 호출이다.
- heartbeat payload의 `LeaderID`는 carried field이지만 현재 authority 판정은 사실상 term과 follower state에 의존한다.
- election은 vote와 heartbeat만 다루며 log replication, commit rule, partition 모델링은 없다.
