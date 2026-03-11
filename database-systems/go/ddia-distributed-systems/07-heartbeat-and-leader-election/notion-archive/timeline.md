# 07-heartbeat-and-leader-election 개발 타임라인

## 1. 프로젝트 골격 만들기

```bash
mkdir -p go/ddia-distributed-systems/07-heartbeat-and-leader-election/{cmd/leader-election,docs/concepts,docs/references,internal/election,notion,notion-archive,problem,tests}
cd go/ddia-distributed-systems/07-heartbeat-and-leader-election
go mod init study.local/ddia-distributed-systems/07-heartbeat-and-leader-election
```

## 2. 질문을 election으로 제한

처음 설계할 때부터 log replication은 제외했다. 이번 단계의 목표는 다음 하나뿐이었다.

> leader가 사라졌을 수 있을 때, 어떤 규칙으로 단 하나의 새 leader를 고를 것인가?

그래서 타입도 `Node`, `Cluster`, vote/heartbeat message만 남겼다.

## 3. timeout 구조 결정

각 node에 두 종류의 임계값을 뒀다.

- `suspicionTTL`
- `electionTTL`

이렇게 분리하면 데모에서 “먼저 의심하고, 그 다음 선거가 일어난다”는 장면을 눈으로 보여 줄 수 있다.

## 4. 테스트 추가

| 테스트명 | 검증 대상 |
| --- | --- |
| `TestHealthyLeaderKeepsSendingHeartbeats` | 정상 heartbeat 아래에서 term과 leader 유지 |
| `TestLeaderFailureTriggersSingleReelection` | leader down 뒤 단일 새 leader 선출 |
| `TestIsolatedNodeCannotPromoteItself` | 과반 없는 고립 node 승격 금지 |
| `TestHigherTermHeartbeatForcesOldLeaderToStepDown` | 복귀한 old leader의 step-down |

## 5. 데모 출력 설계

`go run ./cmd/leader-election`은 authority 변화만 보이도록 네 줄로 고정했다.

```text
tick=4 leader=node-1 term=1 suspected=[]
leader-down id=node-1
tick=8 suspected=[node-2]
tick=9 reelected=node-2 term=2
recovered=node-1 state=follower term=2
```

첫 줄은 정상 leader 선출, 둘째와 셋째 줄은 failure detector, 넷째 줄은 reelection, 마지막 줄은 recovered old leader의 step-down을 보여 준다.

## 6. 검증 명령

```bash
cd go/ddia-distributed-systems/07-heartbeat-and-leader-election
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leader-election
```

## 7. 핵심 파일

| 항목 | 위치 |
| --- | --- |
| 핵심 구현 | `internal/election/election.go` |
| 테스트 | `tests/election_test.go` |
| 데모 | `cmd/leader-election/main.go` |
| 개념 문서 | `docs/concepts/heartbeat-failure-detector.md` |

## 8. 다시 구현할 때 주의점

- self vote 하나로 majority가 되지 않게 계산할 것
- heartbeat 수신 시 suspicion flag와 silence age를 함께 리셋할 것
- higher term 관측 시 old leader authority를 즉시 제거할 것
