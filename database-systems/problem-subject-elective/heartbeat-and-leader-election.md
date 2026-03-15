# heartbeat-and-leader-election 문제지

## 왜 중요한가

leader가 주기적으로 heartbeat를 보내야 합니다. follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다. election은 term을 올리고 majority vote를 받아야만 leader가 될 수 있습니다. higher term을 본 old leader는 즉시 follower로 step-down해야 합니다.

## 목표

시작 위치의 구현을 완성해 leader가 주기적으로 heartbeat를 보내야 합니다, follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다, election은 term을 올리고 majority vote를 받아야만 leader가 될 수 있습니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/cmd/leader-election/main.go`
- `../go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/internal/election/election.go`
- `../go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/tests/election_test.go`

## starter code / 입력 계약

- `../go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election/cmd/leader-election/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- leader가 주기적으로 heartbeat를 보내야 합니다.
- follower는 heartbeat silence가 길어지면 leader를 suspect해야 합니다.
- election은 term을 올리고 majority vote를 받아야만 leader가 될 수 있습니다.
- higher term을 본 old leader는 즉시 follower로 step-down해야 합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `NewNode`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestHealthyLeaderKeepsSendingHeartbeats`와 `TestLeaderFailureTriggersSingleReelection`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/07-heartbeat-and-leader-election && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`heartbeat-and-leader-election_answer.md`](heartbeat-and-leader-election_answer.md)에서 확인한다.
