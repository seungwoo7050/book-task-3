# shard-routing-go 문제지

## 왜 중요한가

deterministic consistent hash ring을 구현해야 합니다. batch routing이 가능해야 합니다. add/remove 이후 reassignment count를 계산해야 합니다. empty ring, single node, multi-node 분산을 검증해야 합니다.

## 목표

시작 위치의 구현을 완성해 deterministic consistent hash ring을 구현해야 합니다, batch routing이 가능해야 합니다, add/remove 이후 reassignment count를 계산해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing/main.go`
- `../go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go`
- `../go/ddia-distributed-systems/projects/03-shard-routing/tests/routing_test.go`

## starter code / 입력 계약

- `../go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- deterministic consistent hash ring을 구현해야 합니다.
- batch routing이 가능해야 합니다.
- add/remove 이후 reassignment count를 계산해야 합니다.
- empty ring, single node, multi-node 분산을 검증해야 합니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `NewRing`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestEmptyAndSingleNodeRouting`와 `TestDistributionAndRebalance`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`shard-routing-go_answer.md`](shard-routing-go_answer.md)에서 확인한다.
