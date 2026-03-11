# 지식 인덱스

## 핵심 용어
- `heartbeat`: leader가 살아 있음을 알리는 주기적 신호입니다.
- `suspicion`: leader가 죽었을 수 있다고 follower가 판단한 상태입니다.
- `term`: leader authority 세대를 구분하는 숫자입니다.
- `step-down`: 더 높은 term을 보고 authority를 내려놓는 동작입니다.

## 재현 순서용 파일 맵
- `../internal/election/election.go`: `Node`, `Cluster`, vote/heartbeat 처리 전체가 있습니다.
- `../tests/election_test.go`: 정상 heartbeat, failover, isolated node, recovered step-down을 검증합니다.
- `../cmd/leader-election/main.go`: suspicion과 reelection을 눈으로 보는 데모입니다.
- `../docs/concepts/heartbeat-failure-detector.md`: failure signal을 설명합니다.

## 바로 실행할 명령
```bash
cd go/ddia-distributed-systems/07-heartbeat-and-leader-election
go test ./... -run TestLeaderFailureTriggersSingleReelection -v
go test ./... -run TestHigherTermHeartbeatForcesOldLeaderToStepDown -v
go run ./cmd/leader-election
```

## 기대 결과
- healthy leader 아래에서는 suspicion이 계속 누적되지 않습니다.
- leader down 뒤 새 leader term이 증가합니다.
- recovered old leader는 follower로 돌아갑니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/election_test.go`
- 데모 파일: `../cmd/leader-election/main.go`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
